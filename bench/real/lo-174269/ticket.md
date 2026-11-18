# Naming bookmarks: using a semicolon does not get a warning but can not get an Insert button

Source: https://bugs.documentfoundation.org/show_bug.cgi?id=174269  (reporter: <email>, filed 2026-10-31)

Description:
Go to Insert - Bookmark, and in the Name field try those characters:
Forbidden characters are:  / \ @ * ? " ; , # 

Just semicolon is behaving different, no warning when inserted, but bookmark can no be inserted, "Insert" button is not active.

[Another issue is in documentation, there are mentioned many others forbidden characters, but some of them work well. I have another bug report for that: / \ @ : * ? " ; , . #]

Steps to Reproduce:
-

Actual Results:
-

Expected Results:
-

Reproducible: Always

User Profile Reset: No

Additional Info:
-

## Reporter's follow-ups

Also, when inserting a wrong character, there we have a message in the ialog, that does not include the semicolon character.

So, the problem is in the code that allows semicolon, but also in the dialog.

---

So, to be more clear:

Go to Insert - Bookmark, and in the Name field try each one of those characters:
/ \ @ * ? " ; , #

They are forbidden characters.

Actual result: 
All characters, EXCEPT semicolon, generates a warning when introduced in the Name field. → so, this is the bug, we have an exception that it is not working
Also, in the warning message, below the Name field, we don’t have the semicolon character. → this is also a bug

Expected result: 
All those characters generates a warning when introduced in the Name field.
In the warning message, below the Name field, we have all the characters that are forbidden, including the semicolon.

---

In the file sw/source/uibase/utlui/content.cxx line 3459 we have:

OUString sForbiddenChars;
    if (ContentTypeId::BOOKMARK == nType)
    {
        sForbiddenChars = "/\\@:*?\";,.#";
    }

But in UI we can insert bookmarks with dots and colon.

---

[attachment: recording.mp4]
video testing the bug

---

I found that in /sw/source/ui/inc/bookmark.hxx line 91, we have:

static constexpr OUString aForbiddenChars = u"/\\@*?\",#"_ustr;

We are missing from here some forbidden characters: I inserted here ';' and if inserted we get a warning when inserted.

My questions is: are '.' or ':' allowed? 
Do we have a documentation on the characters permitted? Some standards?
