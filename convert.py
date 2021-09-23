#!/usr/bin/env python3

from PIL import Image
import os

FRAME_RATE = 15

# Ensure directories exist
if not os.path.exists("png"):
	os.mkdir("png")
if not os.path.exists("frame"):
	os.mkdir("frame")

# Convert to PNG sequence
print("Generating PNGs...")
os.system(f"ffmpeg -i bad-apple.mp4 -r {FRAME_RATE} -s 120:42 png/%d.png -y -loglevel error")

# Convert to MP3
print("Generating MP3...")
os.system(f"ffmpeg -i bad-apple.mp4 bad-apple.mp3 -y -loglevel error")

# Get list of images
dirlist = [item for item in os.listdir("png") if item[0] in "0123456789"]
dirlist.sort(key=lambda a: int(a[:-4]))

print("Generating HTML files...")
for item in dirlist:
	num = int(item[:-4])
	print(num)

	# Make HTML file
	with open(f"frame/{item[:-4]}.html", "w") as f:
		f.write(f'<!DOCTYPE html><html><head><meta charset="utf-8"><title>Bad Apple!!</title><meta http-equiv="refresh" content="0; URL={"../index" if item == dirlist[-1] else num + 1}.html"></head><body><pre>\n')
		out = ""
		with Image.open(f"png/{item}") as img:
			for y in range(img.height):
				for x in range(img.width):
					px = img.getpixel((x, y))[0]
					if px < 64:
						out += "#"
					elif px < 128:
						out += "="
					elif px < 192:
						out += '+'
					else:
						out += "_"  # Chrome is dumb with spaces in a pre
				out += "\n"

		f.write(out)
		f.write("</pre></body></html>")
