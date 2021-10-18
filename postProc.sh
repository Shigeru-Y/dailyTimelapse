#!/bin/bash
# Move timelapse movie file from inputBuffer to html buffer and convert to h264.
cd $HOME
for FULL in $INPUT_BUFFER/2*.mp4
do
 	echo Processing $FULL
	BODY=`basename $FULL .mp4`
	/usr/local/bin/ffmpeg -i $FULL -movflags faststart -vcodec libx264 -acodec libfaac $HTTP_DIR/$BODY-h264.mp4
	mv $FULL $HTTP_DIR/BackUp
done

