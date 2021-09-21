#!/usr/bin/env python3

from PIL import Image
import os

# Ensure directories exist
if not os.path.exists("png"):
	os.mkdir("png")
if not os.path.exists("frame"):
	os.mkdir("frame")
if not os.path.exists("mp3"):
	os.mkdir("mp3")

# Convert to PNG sequence
os.system(f"ffmpeg -i bad-apple.mp4 -r 10 -s 64:24 png/%d.png -y -loglevel error")

# Get list of images
dirlist = [item for item in os.listdir("png") if item[0] in "0123456789"]
dirlist.sort(key=lambda a: int(a[:-4]))

for item in dirlist:
	num = int(item[:-4])
	print(num)

	# Get audio
	os.system(f"ffmpeg -i bad-apple.mp3 -ss 00:{num // 600:02d}:{(num % 600) / 10:.2f} -t 00:00:00.1 mp3/{num}.mp3 -y -loglevel error")

	# Make HTML file
	with open(f"frame/{item[:-4]}.html", "w") as f:
		f.write(f'<!DOCTYPE html><html><head><meta charset="utf-8"><title>Bad Apple!!</title><meta http-equiv="refresh" content="0.1; URL={"../index" if item == dirlist[-1] else num + 1}.html"></head><body><audio nocontrols autoplay><source src="../mp3/{num}.mp3" type="audio/mpeg"></audio><pre>\n')
		out = ""
		with Image.open(f"png/{item}") as img:
			img = img.quantize(2)
			for y in range(img.height):
				for x in range(img.width):
					if img.getpixel((x, y)):
						out += "_"  # Chrome is dumb with spaces in a pre
					else:
						out += "#"
				out += "\n"

		f.write(out)
		f.write("</pre></body></html>")
