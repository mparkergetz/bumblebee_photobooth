** Be sure to set preview_res (line 7) to the resolution of whatever monitor is in use **

To run:
    python bb_pb.py

A live camera view will display, with a small inset showing a zoomed-in view of the image center, which will hopefully help with focusing (let me know if it doesn't).
Sorry it's so choppy - if you want a smooth feed just for framing the shot, lower the preview resolution (preview_res parameter given to the main function).

Press 'c' to capture or 'q' to quit. 

After capture, the output image will be displayed at the preview resolution. The inset is not part of the final image.
If you like it, press 'k' to keep, 'r' to retake, or 'q' to not save and quit.

Images are saved to the output directory in bumblebee_photobooth.
To view the image at full resoltion, open the image file in the output directory. 

