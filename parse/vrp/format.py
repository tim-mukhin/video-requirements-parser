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


class Speaker(TypedDict):
    id: str  # the name if it is spoken or shown on a personal tile, otherwise Person1, Person2
    name: str | None
    tile: str | None  # meeting tile caption ("Room 4")


class Utterance(TypedDict):
    id: str
    speaker: str
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
