# real/treeherder-2092716

_gpt-6-sol@default, 35 s; looked at: frames/moments/p002.jpg, frames/moments/p007.jpg, frames/moments/p006.jpg, frames/0000.0.jpg, frames/0003.5.jpg, frames/0005.5.jpg, frames/0001.5.jpg, frames/0002.5.jpg, frames/0003.0.jpg, frames/0005.0.jpg, frames/0006.5.jpg, frames/0007.5.jpg, frames/moments/p001.jpg, frames/moments/p004.jpg, frames/moments/p008.jpg, frames/0004.0.jpg, frames/0004.5.jpg, frames/0006.0.jpg, frames/000040.jpg_

In Treeherder’s Failure Summary, gray action-button icons become invisible or nearly invisible on hover and return when the pointer leaves. This makes the buttons hard to identify at the point of use.

## Failure Summary action icons become nearly invisible on hover

Class: **silent-fail**

Environment: Treeherder Failure Summary for “AssertionError: in-tree files should pass the linter,” with an associated i2009222 entry. The browser, sign-in state, and color-scheme preference are not visible.

Steps:

1. With the Failure Summary already open, hover the gray internal-issue button beside the assertion failure. (00:01.5; p001, p002)

Expected (implied): The button icon remains visible while hovered.

Actual: The icon becomes indiscernible on hover and reappears after the pointer leaves. The pin button and the right-hand issue button show the same hover effect.

Key events: p001, p002, p003, p004, p007, p010

Missed by the author:

- The visible failure is “AssertionError: in-tree files should pass the linter” and has an i2009222 entry [p001, p003].
- The timeline’s brief “Filea” text is part of the right-hand button’s tooltip, not an error; its icon becomes hard to see on hover and returns afterward [p006, p007, p010].

Claims:

- "The icon disappears while hovering a gray Failure Summary button." [ticket: ACTUAL RESULTS]: confirmed - The first button is blank during hover and its icon returns afterward; the pin and right-hand buttons show the same contrast.
- "The issue occurs in Chrome and Firefox, regardless of color scheme or sign-in state." [ticket: Notes]: not shown - The recording does not show browser identity, preferences, or account state.
- "Reproduction starts by clicking a red or orange task." [ticket: STR 1–2]: not shown - The recording begins with the Failure Summary already open.
