import sys
import os
import time
import mmap
import glob
from win10toast import ToastNotifier
from multiprocessing_on_dill import Process

toaster = ToastNotifier()
csd = sys.path[0]
ico = f"{csd}\\flip.ico"

###########
#Variables#
###########
metadata_fail_list = []
type_fail_list = []


######################
#Function Definitions#
######################

def getFiles(argument):
	#If argument is a directory
	if (os.path.isfile(argument)) == False:
		#Get all Mp4s
		for file in os.listdir(argument):
			if file.endswith('.mp4'):
				flipFile(file)
			else:
				type_fail_list.append(file)
	#If argument is a file
	else:
		if argument.find('.mp4'):
			flipFile(argument)
		else:
			type_fail_list.append(argument)
	return
			

def flipFile(file_to_flip):
	zero = bytes([  0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
			  0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
			 64] )

	r90  = bytes([   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0, 255, 255,   0,   0,
					 0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
					 64])

	r180 = bytes([ 255, 255,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
				   255, 255,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
				   64])

	r270 = bytes([   0,   0,   0,   0, 255, 255,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,
					 0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
					 64])          

	all = [zero, r90, r180, r270]

	with open(argument, "r+b") as f:
		mm = mmap.mmap(f.fileno(), 0)
		jj = mm.find(b'vide')
		mm.seek(jj-160)
		jj = mm.find(bytes([64])) - 32
		mm.seek(jj)
		if jj > 0 :
			a = mm.read(33)
			if a in all:
				print("found rotation metadata:", all.index(a))
				mm.seek(jj)
				# if unrotated, rotate
				if all.index(a) == 0:
					mm.write(all[2])
					# if rotated, reset
				elif all.index(a) == 2:
					mm.write(all[0])
			#if can't rotate, skip file
			else:
				metadata_fail_list.append(file_to_flip)
		return
	
	
###############
#HEAVY LIFTING#
###############

if __name__ == "__main__":	

	if len(sys.argv) > 2:
		print("Didn't pass any directory/files!")
		time.sleep(3)
		quit()
	else:
		self = sys.argv[0]
		arguments = sys.argv[1:]
		for argument in arguments:
			getFiles(argument)
				
		# Warn failed files	
		if metadata_fail_list:
			print(f"{len(metadata_fail_list)} .MP4 files couldn't be rotated")
		if type_fail_list:
			print(f"{len(type_fail_list)} files were unsupported file types")
		toaster.show_toast("Lossless Flip","Done! Check console for errors.")

		
		