import json
import urlgrab
import os
from PIL import Image
from math import floor

cache = urlgrab.Cache()

outFolder = "comics"
if not os.path.exists(outFolder):
	os.mkdir(outFolder)

def generate_page(index):
	data = cache.get("http://xkcd.com/%d/info.0.json"%index, max_age=-1).read()
	data = json.loads(data)
	assert data["img"].find(".png")!=-1, data
	out = os.path.join(outFolder, "%d.html"%index)
	img = os.path.join(outFolder, "%d.png"%index)

	if not os.path.exists(img):
		cache.urlretrieve(data["img"], img)

	pic = Image.open(img)
	ratio = pic.size[0]/(pic.size[1]*1.0)
	rotate = ratio>1
	print ratio, rotate

	text = data["alt"]
	if rotate:
		sizeLen = 52 * 30
		fmt = """<text text-anchor="middle" x="600" y="y-marker" transform="rotate(90 600 400)" font-size="%d">%s</text>"""
	else:
		sizeLen = 36 * 30
		fmt = """<text text-anchor="middle" x="310" y="y-marker" font-size="%d">%s</text>"""

	maxTags = 3
	
	maxLength = int(floor(len(text)/(maxTags*1.0)))
	while True:
		pos = 0
		tags = []
		fontSize = floor(sizeLen/maxLength)
		while len(text)-pos>maxLength:
			loc = pos+maxLength
			while loc>pos and len(text)>loc and text[loc]!=" ":
				loc -=1
			tags.append(text[pos:loc].strip())
			pos = loc +1
			while pos < len(text) and text[pos] == " ":
				pos +=1
		tags.append(text[pos:])

		if len(tags)>maxTags:
			maxLength +=1
		else:
			break
	print "font", fontSize, maxLength,tags
	tags = [fmt%(fontSize, x) for x in tags]

	if rotate:
		y = 980
	else:
		y = 790
	for i in range(len(tags)-1,-1,-1):
		tags[i] = tags[i].replace("y-marker", str(y))
		y-=40

	html = open(out, "wb")
	print >> html, """<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
        <style type="text/css" title="override_css">
            @page {padding: 0pt; margin:0pt}
            body { text-align: center; font-size: 2em; }
        </style>
    </head>
    <body>
		<img src="%d.svg" />
	</body>
	</html>
	"""%index
	html.close()

	svg = open(os.path.join(outFolder, "%d.svg"%index), "wb")
	print >> svg, """<svg version="1.1" xmlns="http://www.w3.org/2000/svg"
				xmlns:xlink="http://www.w3.org/1999/xlink"
				width="600" height="800">"""
	if rotate:
		print >>svg,"""<image width="800" height="520" xlink:href="%s" transform="rotate(90 300 300)" />
			<text text-anchor="middle" x="600" y="460" transform="rotate(90 600 400)" font-size="60">%d: %s</text>
			%s"""%(os.path.basename(img),index, data["title"], "\n".join(tags))
	else:
		height = y-60
		width = ratio*height
		x = (600 - width)/2
			
		print >>svg, """<image x="%d" y="70" width="%d" height="%d" xlink:href="%s" preserveAspectRatio="none"/>
			<text text-anchor="middle" x="310" y="50" font-size="50">%d: %s</text>
			%s"""%(x, width, height, os.path.basename(img),index, data["title"], "\n".join(tags))

	print >> svg, "</svg>"
	svg.close()

toc = open(os.path.join(outFolder, "toc.html"), "wb")

print >>toc, """<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <title>xkcd</title>
    </head>
    <body class="vcenter">
        <div style="display:none">"""
index = 924
while index>0:
	generate_page(index)
	toc.write("<a title=\"%d\" href=\"%d.html\" />"%(index, index))
	index-=1
	if index == 920:
		break

print >>toc, """</div>
    </body>
</html>"""

toc.close()
