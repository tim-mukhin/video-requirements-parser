# real/kde-528786

_claude-sonnet-5.5@default, 16 s; looked at: nothing_

In KDE System Settings, the Default button in a category such as Accessibility resets every page in that category, not only the page the user is on. Users who only want to undo changes on one page can lose settings on other pages, and nothing warns them beforehand. The report comes from the ticket text alone, with no video.

## System Settings Default button resets the entire category without warning, not just the current page

Class: **wrong-data**

Environment: System Settings on CachyOS Linux, KDE Plasma 6.8.2, Frameworks 6.31.0, Qt 6.12.0, Wayland, kernel 7.3.3-1-cachyos. The reporter says they use Union (apparently the Union style). Example category: Accessibility. No accounts or organizations are mentioned.

Steps:

1. Open System Settings and go to a category that has a Default button, e.g. Accessibility. (00:00.0; )
2. Change settings on one page of that category and apply them. (00:00.0; )
3. Click the Default button to undo those changes. (00:00.0; )

Expected (speech): Either only the current page is reset to Default, or clicking the button shows a message warning that the entire category will be reset. The reporter's follow-up suggests a prompt offering 'This page' or 'The entire [category] menu'.

Actual: The entire category (menu) is reset to Default, including pages the user did not change, with no warning.

Key events: 

Claims:

- "The Default button resets the whole category rather than only the current page." [The entire menu is reset to Default.]: not shown - No video was available. The claim comes from the ticket text only.
- **R1** [proposed] The Default button resets only the page the user is on. (proposed by reporter) - ticket expected result 1
- **R2** [proposed] Clicking Default shows a message warning that the entire category will be reset. (proposed by reporter) - ticket expected result 2
- **R3** [proposed] Clicking Default offers a choice between 'This page' and 'The entire [menu name] menu'. (proposed by reporter) - reporter follow-up
