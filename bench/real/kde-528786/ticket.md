# System Settings Default button should warn that it's the entire category that will be reset, instead of just the page the user is in

Source: https://bugs.kde.org/show_bug.cgi?id=528786  (reporter: <email>, filed 2026-11-13)

[attachment: recording.mp4]
Issue in System Settings

STEPS TO REPRODUCE
1. Go to any category that offers a Default button, ex: Accessibility.
2. Make and apply changes to settings in one page.
3. Use the Default button to undo those changes.

OBSERVED RESULT
The entire menu is reset to Default.

EXPECTED RESULT
One of the two:
1. Only the page the user is in should be reset to Default.
2. Clicking the button should give a message warning that the entire menu will be reset to Default.

SOFTWARE/OS VERSIONS
Operating System: CachyOS Linux 
KDE Plasma Version: 6.8.2
KDE Frameworks Version: 6.31.0
Qt Version: 6.12.0
Kernel Version: 7.3.3-1-cachyos (64-bit)
Graphics Platform: Wayland
Processors: 8 × 11th Gen Intel® Core™ i5-11300H @ 3.10GHz
Memory: 9 GB of RAM (8.1 GB usable)
Graphics Processor 1: Intel® Iris® Xe Graphics
Graphics Processor 2: NVIDIA GeForce GTX 1650
Manufacturer: LENOVO
Product Name: 82MG
System Version: IdeaPad Gaming 3 15IHU6

ADDITIONAL INFORMATION
Using Union.

## Reporter's follow-ups

Or better yet, if the user clicks on Default, it should offer "This page" and "The entire [name_of_the_menu] menu" for the user to pick.
