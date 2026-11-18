# [Bug]: "Search everywhere" returns no result if search term is short

Source: https://github.com/nextcloud/server/issues/56859  (reporter: Summon528, filed 2025-12-05)

### ⚠️ This issue respects the following points: ⚠️

- [x] This is a **bug**, not a question or a configuration/webserver/proxy issue.
- [x] This issue is **not** already reported on [Github](https://github.com/nextcloud/server/issues?q=is%3Aopen+is%3Aissue+label%3Abug) OR [Nextcloud Community Forum](https://help.nextcloud.com/) _(I've searched it)_.
- [x] Nextcloud Server **is** up to date. See [Maintenance and Release Schedule](https://github.com/nextcloud/server/wiki/Maintenance-and-Release-Schedule) for supported versions.
- [x] I agree to follow Nextcloud's [Code of Conduct](https://nextcloud.com/contribute/code-of-conduct/).

### Bug description

When the search term is short (< 3 char), the search everywhere page (`/apps/files/search?query=xx`) shows no result  instead of a good error feedback. This can cause very confusing behavior.

Take this screen recording from the demo site for example,
1. User searched for "ne" => got result => good
2. User clicked "search everywhere", probably expect to get **_more_** result => instead, saw a "no result" screen
3. User enter more chars and the result behave normally

[attachment: recording.mp4]

### Steps to reproduce

1. Navigate to `/apps/files/search?query=xx` and observe that it will never return a result no matter what the query is

### Expected behavior

Not really sure,
Maybe we should show another error message, but it will still be confusing consider that clicking "search everywhere" erase the result.
Or maybe we should just search anyway

### Additional info

I discovered this issue because I'm dealing with CJK characters, I also noticed that an PR #21777 a while ago reduced search limit to 2 chars, is there any reason that this page has the 3-char limit?

As for the env, It's reproducible on the demo site, so the env is whatever that env is.

## Reporter's follow-ups

A solution could be
- Hide the "Search everywhere" button if the search term is 1 char
- Allow searching for 2 char in the "Search everywhere" page
