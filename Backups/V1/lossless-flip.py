import sys
import os
import mmap
from win10toast import ToastNotifier

toaster = ToastNotifier()
cwd = os.getcwd()
ico = f"{cwd}\\flip.ico"

if len(sys.argv) < 1 :
	print("""
change rotation metadata in mp4 files
see: https://superuser.com/a/1307206/1010278
usage: %s file.mp4
""" % sys.argv[0])
	sys.exit(0)

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

with open(sys.argv[1], "r+b") as f:
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
			if all.index(a) == 0:
				mm.write(all[2])
				toaster.show_toast("Lossless Flip", "Rotated 180°", icon_path=ico)
			elif all.index(a) == 2:
				mm.write(all[0])
				toaster.show_toast("Lossless Flip", "Reset to 0°")
		else:
			print("no rotation metadata found")
			toaster.show_toast("Lossless Flip", "Sorry! Unsupported file.", icon_path=ico)
			quit()
		
		