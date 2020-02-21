import sys
import os
import time
import mmap
import glob
import subprocess
from win10toast import ToastNotifier
from multiprocessing_on_dill import Process
import enlighten
import pyfiglet
#import #logging
from colorama import init
from colorama import Fore, Back, Style

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

def flipFile(argument):
	if ('.mp4' in argument) or ('.mov' in argument):
		pass
		
	else:
		print(Back.RED + "FAILED " + Style.RESET_ALL + "'" + os.path.basename(argument) + "'")
		#logging.warning("Type_Fail: " + argument)
		type_fail_list.append(argument)
		return "type_fail"


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
				print(Fore.GREEN + "FLIPPING " + Style.RESET_ALL + "'" + os.path.basename(argument) + "'")
				mm.seek(jj)
				# if unrotated, rotate
				if all.index(a) == 0:
					mm.write(all[2])
					# if rotated, reset
				elif all.index(a) == 2:
					mm.write(all[0])
			else:
				print(Back.WHITE + Fore.RED + "FAILED " + Style.RESET_ALL + "'" + os.path.basename(argument) + "'")
				metadata_fail_list.append(argument)
				#logging.warning("Metadata_Fail: " + argument)
				return "metadata_fail"
		return "success"
	
	
###############
#HEAVY LIFTING#
###############

if __name__ == "__main__":	

	
	# #logging
	#logging.basicConfig(filename="fliplog.log",
                            # filemode='a',
                            # format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            # datefmt='%H:%M:%S',
                            # level=#logging.DEBUG)		
	
	# Title
	ascii_banner = pyfiglet.figlet_format("Lossless Flip")
	print(ascii_banner)
	

	if len(sys.argv) < 2:
		print("Didn't pass any files!")
		toaster.show_toast("Lossless Flip","Incompatible/insufficient file list.", threaded=True)
		input(Back.RED + "Press Enter to continue...")
		
	else:
		self = sys.argv[0]
		arguments = sys.argv[1:]
		bar_format = u'{desc}{desc_pad}{percentage:3.0f}%|{bar}| ' + \
					u'S:{count_0:{len_total}d} ' + \
					u'F:{count_2:{len_total}d} ' + \
					u'E:{count_1:{len_total}d} ' + \
					u'[{elapsed}<{eta}, {rate:.2f}{unit_pad}{unit}/s]'

		success = enlighten.Counter(total=len(arguments), unit='files',
									color='green', bar_format=bar_format)
		errors = success.add_subcounter('white')
		failures = success.add_subcounter('red')

		for argument in arguments:
			result = flipFile(argument)
			if result == "metadata_fail":
				errors.update()
			if result == "type_fail":
				failures.update()
			else:
				success.update()		
		print("\n\n")
			
			
		
				
		# Warn failed files	
		if metadata_fail_list:
			print(Back.WHITE + Fore.RED + f"{len(metadata_fail_list)} .MP4 files" + Style.RESET_ALL + " couldn't be rotated"
			+ " (Missing rotation metadata tag)")
			
		if type_fail_list:
			if len(type_fail_list) > 1:
				print(Back.RED + f"{len(type_fail_list)} files" + Style.RESET_ALL + " were unsupported file types" )
			else:
				print(Back.RED + f"{len(type_fail_list)} file" + Style.RESET_ALL + " was an unsupported file type" )
		
		total_errors = len(metadata_fail_list) + len(type_fail_list)
		toaster.show_toast("Lossless Flip",f"Done! {total_errors} errors", threaded=True)
		if total_errors > 0:
			input("Press Enter to continue...")
		else:
			pexit = enlighten.Counter(total=5, desc='Exiting...', unit='seconds', colour='green')
			for i in range(5):
				time.sleep(1)
				pexit.update()
			

		
		