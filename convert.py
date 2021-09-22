#!/usr/bin/env python3

from PIL import Image
import os

FRAME_RATE = 4

# Ensure directories exist
if not os.path.exists("png"):
	os.mkdir("png")
if not os.path.exists("frame"):
	os.mkdir("frame")
if not os.path.exists("ogg"):
	os.mkdir("ogg")

# Convert to PNG sequence
print("Generating PNGs...")
os.system(f"ffmpeg -i bad-apple.mp4 -r {FRAME_RATE} -s 120:42 png/%d.png -y -loglevel error")

# Convert to OGG for index test song
print("Generating OGG...")
os.system(f"ffmpeg -i bad-apple.mp4 -vn -acodec libvorbis bad-apple.ogg -y -loglevel error")

# Get list of images
dirlist = [item for item in os.listdir("png") if item[0] in "0123456789"]
dirlist.sort(key=lambda a: int(a[:-4]))

print("Generating HTML files...")
for item in dirlist:
	num = int(item[:-4])
	print(num)

	# Get audio
	os.system(f"ffmpeg -i bad-apple.ogg -ss 00:{num // (60 * FRAME_RATE):02d}:{(num % (60 * FRAME_RATE)) / FRAME_RATE:.2f} -t 00:00:{1 / FRAME_RATE:.2f} -acodec copy ogg/{num}.ogg -y -loglevel error")

	# Make HTML file
	with open(f"frame/{item[:-4]}.html", "w") as f:
		f.write(f'<!DOCTYPE html><html><head><meta charset="utf-8"><title>Bad Apple!!</title><meta http-equiv="refresh" content="{1 / FRAME_RATE - 0.1:.2f}; URL={"../index" if item == dirlist[-1] else num + 1}.html"></head><body><audio autoplay><source src="../ogg/{num}.ogg" type="audio/ogg"></audio><pre>\n')
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
