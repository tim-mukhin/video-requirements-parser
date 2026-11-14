import React from 'react';
import { Composition, staticFile } from 'remotion';
import type { CalculateMetadataFunction } from 'remotion';
import { SCENARIOS, byKey, compId } from '../../scenarios/index.ts';
import type { Timeline } from '../compile/timeline.ts';
import { Desktop } from './Desktop.tsx';
import { SLIDE_H, SLIDE_W, SlideView } from '../apps/meet/SlideView.tsx';
import type { Slide } from '../format/scenario.ts';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { loadFont } from '@remotion/google-fonts/Inter';
import type { Layout } from './Desktop.tsx';

type Props = { id: string; tl?: Timeline; layout?: Layout; probe?: boolean };

const load = async (p: Props): Promise<Required<Pick<Props, 'tl'>> & Props> => {
  if (p.tl) return { ...p, tl: p.tl };
  const r = await fetch(staticFile(`${p.id}/props.json`));
  if (!r.ok) throw new Error(`missing out/${p.id}/props.json: run npm run build ${p.id} first`);
  return { ...p, ...(await r.json()) };
};

const meta: CalculateMetadataFunction<Props> = async ({ props }) => {
  const p = await load(props);
  return {
    props: p,
    width: p.tl.w,
    height: p.tl.h,
    fps: p.tl.fps,
    durationInFrames: p.probe ? p.tl.segments.length : Math.ceil(p.tl.duration * p.tl.fps),
  };
};

const { fontFamily } = loadFont('normal', { weights: ['400', '600', '700'], subsets: ['latin', 'cyrillic'] });

type DeckProps = { id: string; deck: string; slides?: Slide[] };
const DeckPage: React.FC<DeckProps> = ({ id, deck, slides }) => {
  const frame = useCurrentFrame();
  const d = byKey(id).decks!.find((x) => x.id === deck)!;
  const list = slides ?? d.slides;
  return (
    <AbsoluteFill style={{ fontFamily }}>
      <SlideView slide={list[frame]} n={frame + 1} total={list.length} deck={d.file.replace(/\.\w+$/, '')} />
    </AbsoluteFill>
  );
};

const Scene: React.FC<Props> = ({ id, tl, layout, probe }) => <Desktop sc={byKey(id)} tl={tl!} layout={layout} probeMode={probe} />;

export const Root: React.FC = () => (
  <>
    {SCENARIOS.map((s) => [s, `${s.lang}/${s.id}`] as const).map(([s, key]) => (
      <React.Fragment key={key}>
        <Composition id={compId(key)} component={Scene} defaultProps={{ id: key } as Props} calculateMetadata={meta} width={s.screen.w} height={s.screen.h} fps={30} durationInFrames={1} />
        <Composition id={`${compId(key)}-probe`} component={Scene} defaultProps={{ id: key, probe: true } as Props} calculateMetadata={meta} width={s.screen.w} height={s.screen.h} fps={30} durationInFrames={1} />
        {(s.decks ?? []).map((d) => (
          <Composition key={d.id} id={`${compId(key)}--${d.id}`} component={DeckPage} defaultProps={{ id: key, deck: d.id } as DeckProps} width={SLIDE_W} height={SLIDE_H} fps={30} durationInFrames={d.slides.length} />
        ))}
      </React.Fragment>
    ))}
  </>
);
