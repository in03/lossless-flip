import sys
import mmap 

if len(sys.argv) < 2 :
	print("""
change rotation metadata in mp4 files
see: https://superuser.com/a/1307206/1010278
usage: %s file.mp4 0-3
0: 0 degree 
1: 90 
2: 180
3: 270 
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
ii = int(sys.argv[2])

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
            mm.write(all[ii])
        else:
            print("no rotation metadata found")