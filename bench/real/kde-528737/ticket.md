# Columns view: Really long names aren't truncated and lead to odd behavior

Source: https://bugs.kde.org/show_bug.cgi?id=528737  (reporter: <email>, filed 2026-11-12)

[attachment: recording.mp4]
Showing the reproduction steps and the unexpected behaviour

DESCRIPTION
When the current folder contains an item with a really long name there is some behavior that seems really odd and that I'm not sure is intended. 

STEPS TO REPRODUCE
1.  Create a file with a really long name. Like 200 characters. In a nested folder with more folder inside.
2. Navigate to the folder with said file
3. Click on one of the sub folders

OBSERVED RESULT
The current folder fills the screen with the next layer not visible. Sliding the scroll bar a little ways over and clicking on another folder doesn't open it, but scoots the column to fit the window. Resizing the window in this state truncates the really long name and shows a much more normal view. 

EXPECTED RESULT
Not 100% sure how this should work, but currently this doesn't feel right. It should probably match what the resized view shows the whole time. 

SOFTWARE/OS VERSIONS
Operating System: Arch Linux 
KDE Plasma Version: 6.8.2
Graphics Platform: Wayland
Dolphin: 27.03.70
KDE Frameworks: 6.32.0
Qt: Using 6.12.0 and built against 6.12.0
Arch Linux (Wayland)
Build ABI: x86_64-little_endian-lp64
Kernel: linux 7.2.15-zen1-1-zen
Processors: 16 × AMD Ryzen 7 5800X3D 8-Core Processor
Memory: 16 GiB of RAM (15.5 GiB usable)
Graphics Processor: AMD Radeon RX 9070 XT
