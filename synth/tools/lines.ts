import { mkdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { byKey } from '../../scenarios/index.ts';
import { lines } from '../compile/timeline.ts';

const ROOT = path.resolve(import.meta.dirname, '../..');
const id = process.argv[2];
const sc = byKey(id);
const out = path.join(ROOT, 'out', id);
mkdirSync(out, { recursive: true });
const voiceOf = (who: string) => sc.cast.find((c) => c.id === who)!.voice;
const data = lines(sc).map((l) => ({ id: l.id, lang: sc.lang, voice: voiceOf(l.who), text: l.text, words: l.words }));
writeFileSync(path.join(out, 'lines.json'), JSON.stringify(data, null, 1));
console.log(`${path.join(out, 'lines.json')}: ${data.length} lines`);
