// Rewrite truth/*.json of built scenarios without rendering: the DOM snapshot from props.json plus the scenario.
// For ground-truth-only edits (bug markup, names of steps); a change to timing or screens needs `npm run build`.
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { byKey } from '../../scenarios/index.ts';
import { compile } from '../compile/timeline.ts';
import type { Voice } from '../compile/timeline.ts';
import { truth } from '../compile/truth.ts';

const ROOT = path.resolve(import.meta.dirname, '../..');
for (const key of process.argv.slice(2)) {
  const sc = byKey(key);
  const OUT = path.join(ROOT, 'out', key);
  const props = JSON.parse(readFileSync(path.join(OUT, 'props.json'), 'utf8'));
  const voicePath = path.join(ROOT, 'out', sc.lang, sc.voiceFrom ?? sc.id, 'voice', 'voice.json');
  const voice: Voice | undefined = existsSync(voicePath) ? JSON.parse(readFileSync(voicePath, 'utf8')) : undefined;
  const tl = compile(sc, voice);
  const sig = (t: typeof tl) => JSON.stringify([t.duration, t.segments, t.events.map((e) => [e.t, e.src, e.win]), t.lines.map((l) => [l.start, l.end, l.text])]);
  if (sig(tl) !== sig(props.tl)) throw new Error(`${key}: the scenario timeline differs from the rendered one, run npm run build`);
  const t = truth(sc, tl, props.layout);
  const J = (f: string, v: unknown) => writeFileSync(path.join(OUT, f), JSON.stringify(v, null, 1));
  J('truth/transcript.json', t.transcript);
  J('truth/ui-states.json', t.states);
  J('truth/timeline.json', t.timeline);
  J('truth/links.json', t.links);
  if (t.report) J('truth/report.json', t.report);
  J('truth/speakers.json', t.speakers);
  if (t.requirements) J('truth/requirements.json', t.requirements);
  if (t.slides) J('truth/slides.json', t.slides);
  console.log(`[${key}] truth rewritten`);
}
