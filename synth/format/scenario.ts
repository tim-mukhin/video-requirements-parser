import type { RelayState } from '../apps/relay/model.ts';
import type { VaultState } from '../apps/vault/model.ts';
import type { MeetState } from '../apps/meet/model.ts';
import type { SlidesState } from '../apps/slides/model.ts';
import type { Lang } from '../i18n.ts';

export type WinId = string;
// "<window>/<element>", element = data-el inside the window's app
export type El = string;
export type Box = [x: number, y: number, w: number, h: number];

// tile - meeting-recording tile the voice comes through (a meeting room is one tile for several people);
// introduced - the name is said in the video; otherwise parsing must yield only a label like Person1, Person2
export type Speaker = { id: string; name: string; voice: string; tile?: string; introduced?: boolean };

export type AppWin =
  | { app: 'relay'; state: RelayState }
  | { app: 'vault'; state: VaultState }
  | { app: 'meet'; state: MeetState }
  | { app: 'slides'; state: SlidesState };
export type AppKind = AppWin['app'];
// browser: window is drawn as a browser; windows sharing a group are tabs of one window, the top one is visible
export type Browser = { url: string; tab: string; group: string };
export type Win = { id: WinId; title: string; bbox: Box; browser?: Browser } & AppWin;

// Markup inside a line: [phrase](kind:target#name)
//   click:a/send   clicks on the first word of the phrase
//   focus:b        brings the window to front (click on title bar)
//   point:a/col    hovers the element until the phrase ends
//   ref:b/dialog   speech refers to the element with no action
//   ref:?          reference that cannot be resolved from the video (correct answer: unresolved)
export type AnchorKind = 'click' | 'focus' | 'point' | 'ref';

export type Action =
  | { click: El }
  | { focus: WinId }
  | { point: El; ms: number }
  | { move: [number, number] }
  // key press without cursor: only its effect is visible on video
  | { key: string; win: WinId }
  // typing, character by character
  | { type: El; text: string };

export type Step =
  | { say: string; who?: string; name?: string }
  | { act: Action; name?: string }
  // system reaction: op is handled by the window app's reducer (or 'os' for the desktop);
  // at - anchor or step name that delay counts from; ms - when the effect is removed
  | { sys: WinId | 'os'; op: object; at?: string; delay?: number; ms?: number; name?: string }
  | { wait: number };

export type BugClass = 'error-shown' | 'silent-fail' | 'wrong-data' | 'state-revert' | 'stuck' | 'intermittent' | 'not-a-bug';

export type BugTruth = {
  class: BugClass;
  title: string;
  expected: { text: string; source: 'speech' | 'implied' };
  actual: string;
  // sys/act/say step names the parser must find
  critical: string[];
  traps?: string[];
};

export type ReqStatus = 'stated' | 'proposed' | 'decided' | 'rejected' | 'open_question';
export type Requirement = {
  id: string;
  text: string;
  status: ReqStatus;
  // line names (say.name) and slide elements the requirement relies on
  evidence: string[];
  proposed_by?: string;
  decided_by?: string;
};

export type Slide = {
  id: string;
  title: string;
  subtitle?: string;
  bullets?: string[];
  table?: { columns: { id: string; label: string }[]; rows: string[][] };
  notes?: string;
};
export type Deck = { id: string; file: string; slides: Slide[] };
// file "attached" to the video; overrides - slides that differ in this file from the ones shown
export type Attachment = { deck: string; format: 'pptx' | 'pdf'; overrides?: Record<string, Slide> };

export type Difficulty = {
  // vague - real-life speech: no context, pauses, guesses and "this thing here"
  speech: 'explicit' | 'deictic' | 'contradicts' | 'silent' | 'vague';
  signal: { kind: 'modal' | 'toast' | 'inline' | 'none'; ms?: number };
  windows: number;
  occluded: boolean;
  distractors: ('notifications' | 'cursor-wander' | 'animations')[];
  attempts: 'once' | 'intermittent' | 'wrong-path-first';
};

export type Degrade = { id: string; height: number; fps: 30 | 15 | 10; crf: number; audio: 'clean' | 'noise' };

// participant tile in a meeting recording: a person or a meeting room with several people
export type Tile = { id: string; name: string; kind: 'person' | 'room'; color: string; figures?: number; muted?: boolean };
// meeting recording: presenter's screen fitted into the frame, people shown separately
export type Recording = { layout: 'strip-top' | 'gallery-right'; title: string; elapsed: number; tiles: Tile[]; frame: { w: number; h: number } };

export type Scenario = {
  id: string;
  lang: Lang;
  kind: 'bug-repro' | 'meeting';
  title: string;
  screen: { w: number; h: number };
  device?: 'desktop' | 'phone';
  recording?: Recording;
  wallpaper: string;
  cast: Speaker[];
  windows: Win[];
  steps: Step[];
  // reuse the voiceover of another scenario with the same lines
  voiceFrom?: string;
  decks?: Deck[];
  attachments?: Attachment[];
  bug?: BugTruth;
  requirements?: Requirement[];
  traps?: string[];
  difficulty: Difficulty;
  variants: Degrade[];
};
