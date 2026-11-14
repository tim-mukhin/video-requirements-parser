import { mkdirSync, rmSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import path from 'node:path';
import PptxGenJS from 'pptxgenjs';
import { renderStill, selectComposition } from '@remotion/renderer';
import type { Attachment, Deck, Scenario, Slide } from '../format/scenario.ts';
import { compId } from '../../scenarios/index.ts';

const slidesOf = (deck: Deck, a: Attachment): Slide[] => deck.slides.map((s) => a.overrides?.[s.id] ?? s);

async function pdf(serveUrl: string, sc: Scenario, deck: Deck, a: Attachment, out: string) {
  const slides = slidesOf(deck, a);
  const key = `${sc.lang}/${sc.id}`;
  const inputProps = { id: key, deck: deck.id, slides };
  const composition = await selectComposition({ serveUrl, id: `${compId(key)}--${deck.id}`, inputProps });
  const tmp = `${out}.pages`;
  mkdirSync(tmp, { recursive: true });
  const pages: string[] = [];
  for (let i = 0; i < slides.length; i++) {
    const p = path.join(tmp, `${String(i).padStart(2, '0')}.pdf`);
    await renderStill({ serveUrl, composition, inputProps, frame: i, output: p, imageFormat: 'pdf', logLevel: 'error' });
    pages.push(p);
  }
  execFileSync('pdfunite', [...pages, out]);
  rmSync(tmp, { recursive: true });
}

async function pptx(deck: Deck, a: Attachment, out: string) {
  const p = new PptxGenJS();
  p.layout = 'LAYOUT_WIDE';
  const name = deck.file.replace(/\.\w+$/, '');
  for (const [i, s] of slidesOf(deck, a).entries()) {
    const sl = p.addSlide();
    sl.background = { color: 'FFFFFF' };
    sl.addShape(p.ShapeType.rect, { x: 0, y: 0, w: 0.15, h: 7.5, fill: { color: '0F766E' }, line: { color: '0F766E' } });
    sl.addText(`${name}`, { x: 0.9, y: 7.0, w: 8, h: 0.3, fontSize: 10, color: '94A3B8' });
    sl.addText(`${i + 1} / ${deck.slides.length}`, { x: 11.3, y: 7.0, w: 1.6, h: 0.3, fontSize: 10, color: '94A3B8', align: 'right' });
    if (!s.bullets && !s.table) {
      sl.addText(s.title, { x: 1.1, y: 2.4, w: 11, h: 1.2, fontSize: 44, bold: true, color: '0F172A' });
      if (s.subtitle) sl.addText(s.subtitle, { x: 1.1, y: 3.7, w: 11, h: 0.6, fontSize: 20, color: '475569' });
      continue;
    }
    sl.addText(s.title, { x: 0.9, y: 0.5, w: 11.5, h: 0.8, fontSize: 32, bold: true, color: '0F172A' });
    if (s.bullets) {
      sl.addText(s.bullets.map((b) => ({ text: b, options: { bullet: true, breakLine: true } })), { x: 0.9, y: 1.6, w: 11.5, h: 4.8, fontSize: 20, color: '0F172A', valign: 'top', paraSpaceAfter: 12 });
    }
    if (s.table) {
      const head = s.table.columns.map((c) => ({ text: c.label, options: { bold: true, fill: { color: 'F1F5F9' } } }));
      sl.addTable([head, ...s.table.rows.map((r) => r.map((text) => ({ text })))], { x: 0.9, y: 1.6, w: 11.5, fontSize: 14, border: { type: 'solid', color: 'CBD5E1', pt: 1 } });
    }
  }
  await p.writeFile({ fileName: out });
}

export async function exportAttachments(serveUrl: string, sc: Scenario, dir: string) {
  mkdirSync(dir, { recursive: true });
  const files: string[] = [];
  for (const a of sc.attachments ?? []) {
    const deck = sc.decks!.find((d) => d.id === a.deck)!;
    const out = path.join(dir, deck.file.replace(/\.\w+$/, `.${a.format}`));
    if (a.format === 'pdf') await pdf(serveUrl, sc, deck, a, out);
    else await pptx(deck, a, out);
    files.push(out);
  }
  return files;
}
