"""Parser output format: evidence.json. One format for every kind of video - bug repro, phone, browser, meeting recording.

Elements are addressed by a box and text in video frame pixels, never by internal names: the parser and the converter of
the generator's ground truth write the same file, and the evaluator compares them by time, text and box overlap.
What was seen is kept apart from what was inferred: every event has a source, every claim from speech has `verified`.
"""
from typing import Literal, NotRequired, TypedDict

SCHEMA = "video-evidence/0.1"

Box = list[int]  # [x, y, w, h] in pixels of the master video frame


class Video(TypedDict):
    file: str
    width: int
    height: int
    fps: float
    duration_ms: int


class Region(TypedDict):
    id: Literal["screen", "people"]  # in a meeting recording only "screen" is parsed
    bbox: Box


class Word(TypedDict):
    w: str
    start_ms: int
    end_ms: int


class NameFact(TypedDict):
    name: str  # as heard
    source: Literal["introduced", "addressed"]  # "This is Lukas"; "Lukas, are you there?" and this voice answered
    utterance: NotRequired[str]  # where it was said (in Speaker.names)
    by: NotRequired[str]  # the utterance that called the name
    on_screen: NotRequired[str]  # the same name spelled differently on screen ("Lucas" heard, "Lukas" shown)


class Speaker(TypedDict):
    id: str  # Voice1, Voice2 ... from diarization; "unknown" when no voice covers an utterance
    utterances: int
    seconds: float
    tiles: dict[str, int]  # lit tile caption -> utterances
    shares_tile: dict[str, list[str]]  # a tile lit for other voices too (a meeting room)
    names: list[NameFact]  # empty: name unknown


class VoicePart(TypedDict):
    voice: str | None
    start_ms: int
    end_ms: int
    text: str
    margin: float  # cosine margin to the second-nearest voice


class Utterance(TypedDict):
    id: str
    speaker: str  # the voice of most of the utterance
    voice: NotRequired[str | None]
    parts: NotRequired[list[VoicePart]]  # two voices share the utterance
    voice_doubt: NotRequired[float]  # the margin to the second-nearest voice, when it is small
    tile: NotRequired[str]  # the tile lit during it
    names: NotRequired[list[NameFact]]
    start_ms: int
    end_ms: int
    text: str
    words: list[Word]


class TextBlock(TypedDict):
    bbox: Box
    text: str


class Screen(TypedDict):
    """A stable screen state between changes."""
    id: str
    start_ms: int
    end_ms: int
    frame: str | None  # path to the evidence frame
    texts: list[TextBlock]


EventKind = Literal[
    "appear",  # an element appeared: toast, dialog, message, console line
    "disappear",
    "text_change",  # text changed in place: status, upload percent
    "visual_change",  # pixels of an element changed, its text did not: an icon, a check mark, a lock
    "window_change",  # another window or tab came to the front
    "screen_change",  # slide, application or the whole screen changed
    "click",
    "point",  # the cursor hovers and stays
    "key",  # a key press: only its effect is visible
    "type",  # typing
    "move",  # content moved in place of changing: a menu that jumps, a page that shifts for one frame (dx, dy, peak, back)
    "scroll",  # a large area moved up or down
    "drag",  # content followed the cursor (at -> to, onto, after: what changed after the drop)
    "flicker",  # one place going back and forth between two looks, or the cursor between two shapes (count)
]


class Event(TypedDict):
    id: str
    t_ms: int
    end_ms: int | None  # for appear - when it disappeared (a toast shown for 0.3 s)
    kind: EventKind
    bbox: Box | None
    text: str | None
    before: NotRequired[str | None]
    after: NotRequired[str | None]
    visible: bool  # False - the change happened in a covered part of the screen
    source: Literal["pixel", "ocr", "cursor", "touch", "model", "truth"]
    evidence: list[str]  # frames before / during / after
    crop: NotRequired[str]  # cut-out of the element from the evidence frame
    at: NotRequired[list[int]]  # click, point: the cursor tip or the touch centre
    cursor: NotRequired[str | None]  # click, point: cursor shape - arrow, hand, text (I-beam), other
    look: NotRequired[dict]  # visual_change: {"light": [before, after], "contrast": [before, after]}, gray 0-255
    reaction: NotRequired[str]  # point: how the element under the hover changed ("faded, contrast 40 → 3: ...")


class Target(TypedDict):
    bbox: Box
    text: str


class Link(TypedDict):
    """Deictic speech ("right here", "this column") and what it points at."""
    utterance: str
    phrase: str
    start_ms: int
    end_ms: int
    target: Target | None  # None - cannot be resolved from the video
    relation: Literal["click", "focus", "point", "mentions"]


class SlideShown(TypedDict):
    index: int | None  # page number in the attached file, if matched
    title: str
    start_ms: int
    end_ms: int


class Step(TypedDict):
    t_ms: int
    action: str  # click, type, key, focus_window, point
    target_text: str | None
    window: str | None


class Claim(TypedDict):
    """A statement from speech that the screen can confirm or refute ("it used to work", "the file is too big")."""
    text: str
    utterance: str
    verified: bool | None  # None - nothing in the video to check it against


class Bug(TypedDict):
    title: str
    kind: Literal["error-shown", "silent-fail", "wrong-data", "state-revert", "stuck", "intermittent", "not-a-bug"]
    steps: list[Step]
    expected: dict  # {text, source: speech | implied}
    actual: str
    key_events: list[str]  # ids of the events the conclusion rests on
    claims: list[Claim]


class Requirement(TypedDict):
    id: str
    text: str
    status: Literal["stated", "proposed", "decided", "rejected", "open_question"]
    proposed_by: str | None
    decided_by: str | None
    evidence: list[str]  # utterance and event ids


class Findings(TypedDict):
    bug: NotRequired[Bug]
    requirements: NotRequired[list[Requirement]]


class Check(TypedDict):
    """A fact across passes: an error on screen nobody mentions, a value that went back by itself, a change in a window
    covered by the front one, a claim in speech that nothing on screen shows."""
    kind: Literal["unmentioned", "revert", "covered", "claim"]
    t_ms: int
    end_ms: NotRequired[int]
    text: str
    refs: list[str]  # event and utterance ids


class Speech(TypedDict):
    speakers: list[Speaker]
    utterances: list[Utterance]


class Input(TypedDict):
    cursor_share: float  # share of the video the cursor position is known; 0 - no cursor found at all
    cursor_lost: list[list[int]]  # [start_ms, end_ms] stretches of a second or more with the cursor not found
    touch_screen: str | None  # why the video looks like a phone or tablet (a guess); None - a desktop or unknown
    touch: int  # taps seen as touch marks
    typed: int  # typing seen as text growing in place


class Evidence(TypedDict):
    schema: str
    video: Video
    regions: list[Region]
    speech: Speech
    screens: list[Screen]
    events: list[Event]
    links: list[Link]
    slides: list[SlideShown]
    checks: list[Check]
    findings: Findings
    input: Input
