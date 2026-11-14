import { existsSync, mkdirSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { bundle } from '@remotion/bundler';
import { renderFrames, renderStill, selectComposition } from '@remotion/renderer';
import { byKey, compId } from '../../scenarios/index.ts';
import { compile } from '../compile/timeline.ts';
import type { Voice } from '../compile/timeline.ts';
import type { Layout } from '../render/cursor.ts';

// quick frames to check a scenario without rendering video: npm run stills <id> <sec> [sec...]
const ROOT = path.resolve(import.meta.dirname, '../..');
const [id, ...times] = process.argv.slice(2);
const sc = byKey(id);
const OUT = path.join(ROOT, 'out', id, 'stills');
mkdirSync(OUT, { recursive: true });
const vp = path.join(ROOT, 'out', sc.lang, sc.voiceFrom ?? sc.id, 'voice', 'voice.json');
const voice: Voice | undefined = existsSync(vp) ? JSON.parse(readFileSync(vp, 'utf8')) : undefined;
const tl = compile(sc, voice);
const serveUrl = await bundle({ entryPoint: path.join(ROOT, 'synth/index.ts'), publicDir: path.join(ROOT, 'public') });
const probeProps = { id, tl, probe: true };
const segs: Layout = new Array(tl.segments.length);
await renderFrames({
  serveUrl,
  composition: await selectComposition({ serveUrl, id: `${compId(id)}-probe`, inputProps: probeProps }),
  inputProps: probeProps,
  imageFormat: 'none',
  logLevel: 'error',
  outputDir: null,
  concurrency: 2,
  onStart: () => {},
  onFrameUpdate: () => {},
  onBrowserLog: (l) => {
    if (!l.text.startsWith('PROBE ')) return;
    const p = JSON.parse(l.text.slice(6));
    if (!segs[p.seg] && [...p.wins, ...p.items].every((x: { bbox: unknown[] }) => x.bbox.every((v) => Number.isFinite(v)))) segs[p.seg] = p;
  },
});
const props = { id, tl, layout: segs };
const composition = await selectComposition({ serveUrl, id: compId(id), inputProps: props });
for (const t of times) {
  const output = path.join(OUT, `${t}.png`);
  await renderStill({ serveUrl, composition, inputProps: props, frame: Math.min(composition.durationInFrames - 1, Math.round(Number(t) * tl.fps)), output, logLevel: 'error' });
  console.log(output);
}
