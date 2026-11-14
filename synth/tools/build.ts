import { existsSync, mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import path from 'node:path';
import { bundle } from '@remotion/bundler';
import { renderFrames, renderMedia, selectComposition } from '@remotion/renderer';
import { byKey, compId } from '../../scenarios/index.ts';
import { compile } from '../compile/timeline.ts';
import type { Voice } from '../compile/timeline.ts';
import { truth } from '../compile/truth.ts';
import { exportAttachments } from './attachments.ts';
import type { Layout } from '../render/Desktop.tsx';

const ROOT = path.resolve(import.meta.dirname, '../..');
// key = <lang>/<id>, the same string is the output path under out/
const key = process.argv[2];
const sc = byKey(key);
const id = sc.id;
const OUT = path.join(ROOT, 'out', key);
const J = (f: string, v: unknown) => writeFileSync(path.join(OUT, f), JSON.stringify(v, null, 1));
const log = (s: string) => console.log(`[${key}] ${s}`);
mkdirSync(path.join(OUT, 'truth'), { recursive: true });

const VOICE = path.join(ROOT, 'out', sc.lang, sc.voiceFrom ?? id, 'voice');
const voicePath = path.join(VOICE, 'voice.json');
const voice: Voice | undefined = existsSync(voicePath) ? JSON.parse(readFileSync(voicePath, 'utf8')) : undefined;
const tl = compile(sc, voice);
log(`${voice ? 'voiced' : 'no voice, estimated timing'}: ${tl.duration.toFixed(1)} s, ${tl.events.length} events, ${tl.segments.length} states`);

const serveUrl = await bundle({ entryPoint: path.join(ROOT, 'synth/index.ts'), publicDir: path.join(ROOT, 'public') });

const probeProps = { id: key, tl, probe: true };
const probeComp = await selectComposition({ serveUrl, id: `${compId(key)}-probe`, inputProps: probeProps });
const segs: Layout = new Array(tl.segments.length);
await renderFrames({
  serveUrl,
  composition: probeComp,
  inputProps: probeProps,
  imageFormat: 'none',
  logLevel: 'error',
  outputDir: null,
  onStart: () => {},
  onFrameUpdate: () => {},
  onBrowserLog: (l) => {
    if (!l.text.startsWith('PROBE ')) return;
    const p = JSON.parse(l.text.slice(6));
    const whole = [...p.wins, ...p.items].every((x: { bbox: unknown[] }) => x.bbox.every((v) => Number.isFinite(v)));
    if (whole && !segs[p.seg]) segs[p.seg] = { t: p.t, wins: p.wins, items: p.items };
  },
});
const missing = segs.flatMap((s, i) => (s ? [] : [i]));
if (missing.length) throw new Error(`no complete DOM snapshot for states ${missing.join(',')}`);
log(`captured DOM: ${segs.length} states`);
J('props.json', { id: key, tl, layout: segs });

const mainProps = { id: key, tl, layout: segs };
const comp = await selectComposition({ serveUrl, id: compId(key), inputProps: mainProps });
const silent = path.join(OUT, 'silent.mp4');
await renderMedia({ serveUrl, composition: comp, inputProps: mainProps, codec: 'h264', crf: 16, muted: true, outputLocation: silent, concurrency: 8 });
log('video rendered');

const ff = (args: string[]) => execFileSync('ffmpeg', ['-y', '-loglevel', 'error', ...args], { stdio: 'inherit' });
// finished videos sit flat in out/<lang>/, everything intermediate in out/<lang>/<id>/
const VIDEOS = path.join(ROOT, 'out', sc.lang);
for (const f of readdirSync(OUT)) if (/^video(-\w+)?\.mp4$/.test(f)) rmSync(path.join(OUT, f));
const master = path.join(VIDEOS, `${id}.mp4`);
if (voice) {
  const ins = tl.lines.flatMap((l) => ['-i', path.join(VOICE, `${l.id}.wav`)]);
  const delays = tl.lines.map((l, i) => `[${i + 1}:a]adelay=${Math.round(l.start * 1000)}:all=1[a${i}]`).join(';');
  const mix = `${delays};${tl.lines.map((_, i) => `[a${i}]`).join('')}amix=inputs=${tl.lines.length}:normalize=0,loudnorm=I=-18:TP=-1.5,aresample=48000,apad[aout]`;
  ff(['-i', silent, ...ins, '-filter_complex', mix, '-map', '0:v', '-map', '[aout]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', master]);
} else {
  ff(['-i', silent, '-c', 'copy', master]);
}

const variants = sc.variants.map((v) => {
  const file = v.id === 'clean' ? `${id}.mp4` : `${id}.${v.id}.mp4`;
  if (v.id === 'clean') return { ...v, file, scale: 1 };
  const vf = `scale=-2:${v.height}:flags=bicubic,fps=${v.fps}`;
  const audio = !voice
    ? ['-an']
    : v.audio === 'noise'
      ? ['-filter_complex', `anoisesrc=c=pink:a=0.025:d=${tl.duration.toFixed(2)}[n];[0:a][n]amix=inputs=2:normalize=0:duration=first[a]`, '-map', '0:v', '-map', '[a]', '-c:a', 'aac', '-b:a', '96k']
      : ['-c:a', 'copy'];
  ff(['-i', master, '-vf', vf, '-c:v', 'libx264', '-crf', String(v.crf), '-preset', 'medium', '-pix_fmt', 'yuv420p', ...audio, path.join(VIDEOS, file)]);
  return { ...v, file, scale: v.height / tl.h };
});
log(`variants: ${variants.map((v) => v.file).join(', ')}`);

const t = truth(sc, tl, segs);
J('truth/transcript.json', t.transcript);
J('truth/ui-states.json', t.states);
J('truth/timeline.json', t.timeline);
J('truth/links.json', t.links);
if (t.report) J('truth/report.json', t.report);
J('truth/speakers.json', t.speakers);
if (t.requirements) J('truth/requirements.json', t.requirements);
if (t.slides) J('truth/slides.json', t.slides);
const attached = await exportAttachments(serveUrl, sc, path.join(OUT, 'attachments'));
if (attached.length) log(`attached: ${attached.map((f) => path.basename(f)).join(', ')}`);
J('manifest.json', {
  schema_version: '0.1',
  video_id: id,
  lang: sc.lang,
  kind: sc.kind,
  title: sc.title,
  duration_ms: Math.round(tl.duration * 1000),
  frame: { w: tl.w, h: tl.h },
  device: sc.device ?? "desktop",
  timing: voice ? 'tts+whisper' : 'estimated',
  difficulty: sc.difficulty,
  variants: variants.map((v) => ({ id: v.id, file: `../${v.file}`, height: v.height, fps: v.fps, crf: v.crf, audio: voice ? v.audio : 'none', bbox_scale: v.scale })),
  environment: t.environment,
  regions: t.regions,
  attachments: attached.map((f) => `attachments/${path.basename(f)}`),
  traps: t.traps,
  truth: {
    transcript: 'truth/transcript.json',
    speakers: 'truth/speakers.json',
    ui_states: 'truth/ui-states.json',
    timeline: 'truth/timeline.json',
    links: 'truth/links.json',
    report: t.report ? 'truth/report.json' : null,
    requirements: t.requirements ? 'truth/requirements.json' : null,
    slides: t.slides ? 'truth/slides.json' : null,
  },
});
log(`done: ${OUT}`);
