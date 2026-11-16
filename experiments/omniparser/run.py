"""OmniParser v2 on parser clicks: element under the click point + Florence-2 icon caption."""
import argparse
import json
import random
import time
from pathlib import Path

import cv2
import numpy as np
import torch
from PIL import Image

HERE = Path(__file__).parent
OUT = HERE.parent.parent / "out" / "en"
W = HERE / "weights"
RUNS = HERE / "runs"

KEYWORDS = {
    "attach": ["paperclip", "paper clip", "clip", "attach", "link"],
    "schedule": ["clock", "schedule", "time", "timer", "alarm", "history", "watch"],
    "send": ["send", "arrow", "plane", "submit", "right", "forward", "play", "next"],
}


def action_of(text):
    t = (text or "").lower()
    if "schedule" in t:
        return "schedule"
    if t.startswith("attach"):
        return "attach"
    if t == "send":
        return "send"
    return None


def judge(caption, gt_text):
    act = action_of(gt_text)
    if act is None:
        return None
    c = (caption or "").lower()
    hit = {a for a, kws in KEYWORDS.items() if any(k in c for k in kws)}
    if act in hit and len(hit) == 1:
        return "right"
    if act in hit:
        return "ambiguous"
    return "wrong"


def covering(items, t, start="start_ms", end="end_ms"):
    for s in items:
        if s[start] <= t and (s[end] is None or t < s[end]):
            return s
    return items[-1]


def gt_element(states, t, x, y):
    s = covering(states, t)
    best = None
    for el in s["elements"]:
        if el.get("visibility") != "visible":
            continue
        bx, by, bw, bh = el["bbox"]
        if bx <= x <= bx + bw and by <= y <= by + bh:
            if best is None or bw * bh < best["bbox"][2] * best["bbox"][3]:
                best = el
    return best


def build_cases(control_n):
    cases = []
    for ev_path in sorted(OUT.glob("*/parsed/evidence.json")):
        vid = ev_path.parent.parent.name
        e = json.loads(ev_path.read_text())
        states = json.loads((OUT / vid / "truth" / "ui-states.json").read_text())
        timeline = json.loads((OUT / vid / "truth" / "timeline.json").read_text())
        acts = [a for a in timeline if a["kind"] == "action" and a.get("type") == "click"]
        for ev in e["events"]:
            if ev["kind"] != "click":
                continue
            t, (x, y) = ev["t_ms"], ev["at"]
            el = gt_element(states, t - 1, x, y)
            act = min(acts, key=lambda a: abs(a["t_ms"] - t), default=None)
            if act and abs(act["t_ms"] - t) > 300:
                act = None
            scr = covering(e["screens"], t - 1)
            cases.append({
                "video": vid, "event": ev["id"], "t_ms": t, "at": [x, y], "source": ev["source"],
                "ocr_text": ev["text"], "fps": e["video"]["fps"],
                "frame_before": str(OUT / vid / "parsed" / scr["frame"]),
                "gt_el": el and el["id"], "gt_role": el and el["role"], "gt_text": el and el["text"],
                "truth_target": act and act["target"], "truth_text": act and act["target_text"],
            })
    icon = [c for c in cases if c["ocr_text"] is None]
    text = [c for c in cases if c["ocr_text"] is not None]
    random.Random(0).shuffle(text)
    for c in text[:control_n]:
        c["control"] = True
    return icon + text[:control_n]


def frame_at(case):
    cache = RUNS / "frames" / f"{case['video']}_{case['event']}_at.jpg"
    if not cache.exists():
        cache.parent.mkdir(parents=True, exist_ok=True)
        cap = cv2.VideoCapture(str(OUT / f"{case['video']}.mp4"))
        cap.set(cv2.CAP_PROP_POS_FRAMES, round(case["t_ms"] * case["fps"] / 1000))
        ok, img = cap.read()
        assert ok, case
        cv2.imwrite(str(cache), img)
    return str(cache)


class Omni:
    def __init__(self, device, detector):
        from transformers import AutoModelForCausalLM, AutoProcessor
        self.device, self.detector = device, detector
        if detector == "v8":
            from ultralytics import YOLO
            self.yolo = YOLO(str(W / "icon_detect" / "model.pt"))
        else:
            self.v3 = torch.jit.load(str(W / "icon_detect_v3" / "model.pt"), map_location="cpu").eval().to(device)
        self.proc = AutoProcessor.from_pretrained("microsoft/Florence-2-base", trust_remote_code=True)
        self.cap = AutoModelForCausalLM.from_pretrained(
            str(W / "icon_caption"), torch_dtype=torch.float32, trust_remote_code=True).to(device).eval()

    def detect(self, img, imgsz=None):
        if self.detector == "v3":
            return self.detect_v3(img)
        r = self.yolo.predict(source=img, conf=0.05, iou=0.7, imgsz=imgsz or list(img.shape[:2]),
                              device=self.device, verbose=False)[0]
        return r.boxes.xyxy.cpu().numpy(), r.boxes.conf.cpu().numpy()

    @torch.inference_mode()
    def detect_v3(self, img, size=1280):
        from torchvision.ops import nms
        h, w = img.shape[:2]
        scale = min(size / w, size / h)
        canvas = np.full((size, size, 3), 114, np.uint8)
        canvas[:round(h * scale), :round(w * scale)] = cv2.resize(img, (round(w * scale), round(h * scale)))
        x = torch.from_numpy(canvas).permute(2, 0, 1).float()[None].to(self.device) / 255.0
        outs = self.v3(x)
        boxes, scores = [], []
        for i, stride in enumerate((8, 16, 32)):
            cls = outs[2 * i].sigmoid()[0, 0]
            l, t, r, b = outs[2 * i + 1][0]
            g = cls.shape[-1]
            gy, gx = torch.meshgrid(torch.arange(g, device=x.device), torch.arange(g, device=x.device), indexing="ij")
            cx, cy = gx + 0.5, gy + 0.5
            boxes.append(torch.stack([(cx - l) * stride, (cy - t) * stride, (cx + r) * stride, (cy + b) * stride], -1).reshape(-1, 4))
            scores.append(cls.reshape(-1))
        boxes, scores = torch.cat(boxes).cpu(), torch.cat(scores).cpu()
        keep = scores > 0.05
        boxes, scores = boxes[keep], scores[keep]
        keep = nms(boxes, scores, 0.45)
        boxes = (boxes[keep] / scale).numpy()
        boxes[:, 0::2] = boxes[:, 0::2].clip(0, w)
        boxes[:, 1::2] = boxes[:, 1::2].clip(0, h)
        return boxes, scores[keep].numpy()

    @torch.inference_mode()
    def caption(self, crops, size):
        if size == 64:
            pils = [Image.fromarray(cv2.resize(c, (64, 64))) for c in crops]
            inputs = self.proc(images=pils, text=["<CAPTION>"] * len(pils), return_tensors="pt", do_resize=False)
        else:
            pils = [Image.fromarray(c) for c in crops]
            inputs = self.proc(images=pils, text=["<CAPTION>"] * len(pils), return_tensors="pt")
        ids = self.cap.generate(input_ids=inputs["input_ids"].to(self.device),
                                pixel_values=inputs["pixel_values"].to(self.device),
                                max_new_tokens=20, num_beams=1, do_sample=False)
        return [s.strip() for s in self.proc.batch_decode(ids, skip_special_tokens=True)]


def sync(device):
    if device == "mps":
        torch.mps.synchronize()


def hit_box(boxes, x, y, pad=12):
    inside = [(b, (b[2] - b[0]) * (b[3] - b[1])) for b in boxes if b[0] <= x <= b[2] and b[1] <= y <= b[3]]
    if inside:
        return min(inside, key=lambda p: p[1])[0], "inside"
    near = [(b, max(b[0] - x, 0, x - b[2]) + max(b[1] - y, 0, y - b[3])) for b in boxes]
    near = [p for p in near if p[1] <= pad]
    if near:
        return min(near, key=lambda p: p[1])[0], "near"
    return None, "none"


def timed(device, fn):
    sync(device)
    t0 = time.perf_counter()
    r = fn()
    sync(device)
    return r, (time.perf_counter() - t0) * 1000


def run_case(om, case, size, crop=200):
    out = {}
    x, y = case["at"]
    for src in ("before", "at"):
        path = case["frame_before"] if src == "before" else frame_at(case)
        rgb = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
        h, w = rgb.shape[:2]
        # full frame: detector, box under click, caption that box
        (boxes, _), t_det = timed(om.device, lambda: om.detect(rgb))
        b, how = hit_box(boxes, x, y)
        r = {"n_boxes": len(boxes), "t_detect_ms": round(t_det), "hit": how}
        if b is not None:
            x0, y0, x1, y1 = [int(v) for v in b]
            r["box"] = [x0, y0, x1, y1]
            (cap,), t_cap = timed(om.device, lambda: om.caption([rgb[y0:y1, x0:x1]], size))
            r.update(caption=cap, t_caption_ms=round(t_cap), verdict=judge(cap, case["gt_text"]))
        out[f"full_{src}"] = r
        # crop 200x200 around click
        cx0, cy0 = max(0, min(w - crop, x - crop // 2)), max(0, min(h - crop, y - crop // 2))
        patch = rgb[cy0:cy0 + crop, cx0:cx0 + crop]
        (cap,), t_cap = timed(om.device, lambda: om.caption([patch], 768))
        out[f"cropcap_{src}"] = {"caption": cap, "t_caption_ms": round(t_cap), "verdict": judge(cap, case["gt_text"])}
        (boxes, _), t_det = timed(om.device, lambda: om.detect(patch, imgsz=640))
        b, how = hit_box(boxes, x - cx0, y - cy0)
        r = {"n_boxes": len(boxes), "t_detect_ms": round(t_det), "hit": how}
        if b is not None:
            x0, y0, x1, y1 = [int(v) for v in b]
            r["box"] = [x0 + cx0, y0 + cy0, x1 + cx0, y1 + cy0]
            (cap,), t_cap = timed(om.device, lambda: om.caption([patch[y0:y1, x0:x1]], size))
            r.update(caption=cap, t_caption_ms=round(t_cap), verdict=judge(cap, case["gt_text"]))
        out[f"cropdet_{src}"] = r
    return out


def full_pipeline_timing(om, cases, size, n):
    """OmniParser as shipped: detect + caption every box on the frame (batch 128)."""
    res = []
    for case in cases[:n]:
        rgb = cv2.cvtColor(cv2.imread(case["frame_before"]), cv2.COLOR_BGR2RGB)
        (boxes, _), t_det = timed(om.device, lambda: om.detect(rgb))
        crops = [rgb[int(b[1]):int(b[3]), int(b[0]):int(b[2])] for b in boxes]
        crops = [c for c in crops if c.size]

        def cap_all():
            return [s for i in range(0, len(crops), 128) for s in om.caption(crops[i:i + 128], size)]
        _, t_cap = timed(om.device, cap_all)
        res.append({"frame": case["frame_before"], "n_boxes": len(crops),
                    "t_detect_ms": round(t_det), "t_caption_all_ms": round(t_cap)})
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="mps")
    ap.add_argument("--detector", default="v8", choices=["v8", "v3"])
    ap.add_argument("--size", type=int, default=64, help="caption input: 64 (do_resize=False) or 768")
    ap.add_argument("--control", type=int, default=12)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--pipeline-frames", type=int, default=4)
    a = ap.parse_args()
    cases = build_cases(a.control)
    if a.limit:
        cases = cases[:a.limit]
    om = Omni(a.device, a.detector)
    rgb = cv2.cvtColor(cv2.imread(cases[0]["frame_before"]), cv2.COLOR_BGR2RGB)
    om.detect(rgb), om.caption([rgb[:64, :64]], a.size), om.caption([rgb[:200, :200]], 768)  # warm-up
    t0 = time.time()
    for i, c in enumerate(cases):
        c["res"] = run_case(om, c, a.size)
        print(i, c["video"], c["event"], c["gt_text"], "|",
              c["res"]["full_before"].get("caption"), "|", c["res"]["cropcap_at"]["caption"], flush=True)
    pipe = full_pipeline_timing(om, cases, a.size, a.pipeline_frames)
    RUNS.mkdir(exist_ok=True)
    out = RUNS / f"results_{a.detector}_{a.device}_{a.size}{'_lim' if a.limit else ''}.json"
    out.write_text(json.dumps({"detector": a.detector, "device": a.device, "size": a.size, "wall_s": round(time.time() - t0),
                               "cases": cases, "pipeline": pipe}, indent=1, ensure_ascii=False))
    print("wrote", out)


if __name__ == "__main__":
    main()
