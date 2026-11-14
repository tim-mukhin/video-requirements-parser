export type SlidesState = { deck: string; slide: number; mode: 'editor' | 'show' };

export function slidesClick(s: SlidesState, el: string): SlidesState {
  if (el.startsWith('thumb:')) return { ...s, slide: Number(el.slice(6)) };
  if (el === 'present') return { ...s, mode: 'show' };
  return s;
}

export function slidesKey(s: SlidesState, key: string, slides: number): SlidesState {
  if (key === 'next') return { ...s, slide: Math.min(slides - 1, s.slide + 1) };
  if (key === 'prev') return { ...s, slide: Math.max(0, s.slide - 1) };
  if (key === 'present') return { ...s, mode: 'show' };
  if (key === 'esc') return { ...s, mode: 'editor' };
  return s;
}

export const slidesWho = () => ({});
