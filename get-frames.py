import sys
import subprocess
import os
import re
import math
import os.path
from os import path

#Def variables
csd = os.path.dirname(os.path.realpath(__file__))

#Def functions
def get_metadata(video_file, requesting):
	args = f"-v error -select_streams v -of default=noprint_wrappers=1:nokey=1 -show_entries {requesting}"
	result = subprocess.Popen(f"C:\\Program Files\\ffmpeg\\ffprobe {args} {video_file}", stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
	raw_stdout = str(result.stdout.readlines())
	#print(raw_stdout)
	cleaned_stdout = re.sub("\D", "", raw_stdout)
	return cleaned_stdout

def get_middle_frame(total_frames):
	mid_frame = math.ceil(int(total_frames)/2)
	return mid_frame
	
def frames_to_TC (frames):
    h = int(frames / 86400) 
    m = int(frames / 1440) % 60 
    s = int((frames % 1440)/24) 
    f = frames % 1440 % 24
    return ( "%02d:%02d:%02d:%02d" % ( h, m, s, f))
	
def extractFrame(video_file, frame_to_extract):
	out_name, out_ext = os.path.splitext(video_file)
	out_file = out_name + "-" + frame_to_extract + out_ext
	print(f"out file is {out_file}")
	
	args_1 = "-v error -ss "
	args_2 = "-i"
	args_3 = "-frames:v 1"
	result = subprocess.Popen(f"C:\\Program Files\\ffmpeg\\ffmpeg {args_1} {frame_to_extract} {args_2} {video_file} {args_3} {out_file} ", 
								stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
	
	# example ffmpeg -i yosemiteA.mp4 -ss 00:00:18.123 -frames:v 1 yosemite.png
	
	raw_stdout = str(result.stdout.readlines())
	clean_stdout = re.sub("\D", "", raw_stdout)
	print(raw_stdout)
	return out_file

#Main
test_file = f"{csd}\\test.mp4"
if path.exists(test_file):
	fps = get_metadata(test_file, "stream=r_frame_rate")
	fps = fps[:-1]
	print(f"Video FPS: {fps}")
	total_frames = get_metadata(test_file, "stream=nb_frames")
	print(f"total duration in frames: {total_frames}")
	mid_frame = get_middle_frame(total_frames)
	print(f"frame in middle of video: {mid_frame}")
	mid_timecode = frames_to_TC(mid_frame)
	print(f"Middle timecode is: {mid_timecode}")
	out_file = extractFrame(test_file, mid_timecode)
	
	
	
else:
	print("FFProbe was sent an invalid path.")