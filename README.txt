To run:
    python bb_pb.py

A live camera view will display, with a small inset showing a zoomed-in view of the image center, which will hopefully help with focusing (let me know if it doesn't).
The preview resolution is low to make the live feed smoother; if you prefer higher resolution, you cam increase preview_res to (1280, 960) or (1440, 1080), but the feed will be choppier.

Press 'c' to capture or 'q' to quit. 

After capture, the output image will be displayed at the preview resolution. The inset is not part of the final image.
If you like it, press 'k' to keep, 'r' to retake, or 'q' to not save and quit.

Images are saved to the output directory in bumblebee_photobooth.
To view the image at full resoltion, open the image file in the output directory. 

