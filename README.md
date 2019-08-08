# lossless-flip
A quick explorer context menu utility to flip (rotate 180°) .MP4 files using rotation metadata.
This will only work if the encoded file has the rotation tag included in its metadata.

I use this utility to quickly flip videos that have been filmed with an inverted gimbal.
(Some people like holding the Ronin-M upside-down. No judgement.)
This obviously causes strife whenever you want to check over the files later before any editing has taken place.
Plus it just gets a little messy.
 
## Setup
 
1. Run "pip install win10toast" (assuming you have Python installed)
2. Clone this repo someplace nice on your system.
3. Copy the "Lossless Flip" shortcut to "shell:sendto"
4. Within the shorcut properties, change "target" to the filepath of "lossless-flip.cmd"
5. Give it a test!

## To do

- Batch processing (whole directories at once)
- Better error management (though there's not much to go wrong)
- Use OpenCV to detect orientation and apply rotation automatically
