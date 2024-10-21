import numpy
import math
import colorsys
from mpmath import sec
import streamlit as st

def rgbToHex(color):
	return '#%02x%02x%02x' % (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))

def point(angle, radius):
	return (math.sin(angle) * radius, math.cos(angle) * radius)

def generateColor(color):
	return f"rgb({int(color[0] * 255)}, {int(color[1] * 255)}, {int(color[2] * 255)});"

def roundedPolygon(
	sideCount: int,
	radius: float,
	cornerRadius: float,
	x: float = 0,
	y: float = 0,
	degreesAngle: float = 0,
	adjustRadius: bool = True
) -> str:
	radiansOffset = math.radians(degreesAngle)

	interiorAngle = ( math.pi * ( sideCount - 2 ) ) / ( 2 * sideCount )
	pointDistance = cornerRadius / math.tan(interiorAngle)

	shortDiagonal = pointDistance * math.sin(interiorAngle)

	longDiagonalLower = math.sqrt(cornerRadius ** 2 - shortDiagonal ** 2)
	longDiagonalUpper = pointDistance * math.cos(interiorAngle)
	longDiagonal = longDiagonalLower + longDiagonalUpper

	arcAngle = math.acos(longDiagonalLower / cornerRadius)
	arcDistance = radius - cornerRadius if adjustRadius else longDiagonal

	controlPointRatio = 4 / ( 3 * ( sec(arcAngle) + 1 ) )

	path = []

	for sideIndex in range(sideCount):
		degreesAngle = sideIndex * math.pi * 2 / sideCount + radiansOffset
		arcCentre = point(degreesAngle, arcDistance)
		
		centrePoint = point(degreesAngle, arcDistance + longDiagonal)
		firstPoint = numpy.add(arcCentre, point(degreesAngle - arcAngle, cornerRadius))
		secondPoint = numpy.add(arcCentre, point(degreesAngle + arcAngle, cornerRadius))

		firstControlPoint = numpy.add(firstPoint, numpy.multiply(numpy.subtract(centrePoint, firstPoint), controlPointRatio))
		secondControlPoint = numpy.add(secondPoint, numpy.multiply(numpy.subtract(centrePoint, secondPoint), controlPointRatio))

		if sideIndex == 0:
			path.append(f"M {firstPoint[0] + x} {firstPoint[1] + y}")
		else:
			path.append(f"L {firstPoint[0] + x} {firstPoint[1] + y}")
			
		path.append(f"C {firstControlPoint[0] + x} {firstControlPoint[1] + y} {secondControlPoint[0] + x} {secondControlPoint[1] + y} {secondPoint[0] + x} {secondPoint[1] + y}")

	path.append("Z")

	return " ".join(path)

def generateSVG(
	primary: tuple = (177, 255, 0),
	sideCount: int = 6,
	text: str = "HC",
	radius: int = 147,
	strokeWidth: float = 9.97701,
	textSize: int = None,
	cornerRadius: int = None,
	textPosition: tuple = None,
	polygonAngle: int = None,
	x: int = 0,
	y: int = 0,
) -> str:
	if cornerRadius == None: cornerRadius = radius * 0.2

	if sideCount == 3:
		if textSize == None: textSize = 115
		if textPosition == None: textPosition = (148, 132)
		if polygonAngle == None: polygonAngle = 164
	else:
		if textSize == None: textSize = 136
		if textPosition == None: textPosition = (154, 128)
		if polygonAngle == None: polygonAngle = ( 90 if sideCount % 2 else -90 ) / sideCount + 3

	hsv = colorsys.rgb_to_hsv(primary[0] / 255, primary[1] / 255, primary[2] / 255)
	secondary = colorsys.hsv_to_rgb(( hsv[0] + 0.03333 ) % 1, hsv[1], max(hsv[2] - 0.16, 0))
	lighting = rgbToHex(colorsys.hsv_to_rgb(( hsv[0] + 0.02777 ) % 1, 0.21, 0.46))

	primary = tuple(value / 255 for value in primary)

	backgroundGradient = [
		colorsys.hsv_to_rgb((hsv[0] - 0.11666) % 1, 0.13, 0.15),
		colorsys.hsv_to_rgb((hsv[0] - 0.05000) % 1, 0.05, 0.15),
		colorsys.hsv_to_rgb((hsv[0] - 0.08333) % 1, 0.14, 0.15)
	]

	polygonPath = roundedPolygon(sideCount, radius - strokeWidth / 2, cornerRadius, x=radius + x, y=radius + y, degreesAngle=polygonAngle)

	return f"""<?xml version="1.0" encoding="utf-8"?>
<svg width="{radius * 2 + x}px" height="{radius * 2 + y}px" preserveAspectRatio="none"
	xmlns="http://www.w3.org/2000/svg"
	xmlns:xlink="http://www.w3.org/1999/xlink">
	<defs>
		<filter id="point-light-filter-0" primitiveUnits="objectBoundingBox" color-interpolation-filters="sRGB" x="-50%" y="-50%" width="200%" height="200%">
			<feSpecularLighting result="specular-lighting" lighting-color="{lighting}" specularConstant="1.81" specularExponent="13">
				<fePointLight x="0.5" y="0.5" z="0.5"/>
			</feSpecularLighting>
			<feDiffuseLighting result="diffuse-lighting" lighting-color="{lighting}" diffuseConstant="0.2">
				<fePointLight x="0.5" y="0.5" z="0.5"/>
			</feDiffuseLighting>
			<feMerge result="lighting">
				<feMergeNode in="diffuse-lighting"/>
				<feMergeNode in="specular-lighting"/>
			</feMerge>
			<feComposite in="SourceGraphic" in2="lighting" operator="arithmetic" k1="1" k2="0.41" k3="0" k4="0"/>
		</filter>
		<linearGradient id="gradient-0-0" gradientUnits="userSpaceOnUse" x1="254.441" y1="95.568" x2="254.441" y2="381.342" xlink:href="#gradient-0"/>
		<linearGradient id="gradient-0">
			<stop offset="0" style="stop-color: {generateColor(backgroundGradient[0])}"/>
			<stop offset="0.329" style="stop-color: {generateColor(backgroundGradient[1])}"/>
			<stop offset="0.668" style="stop-color: {generateColor(backgroundGradient[2])}"/>
			<stop offset="1" style="stop-color: rgb(26, 26, 26);"/>
		</linearGradient>
		<linearGradient id="gradient-4-0" gradientUnits="userSpaceOnUse" x1="254.441" y1="129.484" x2="254.441" y2="347.426" gradientTransform="matrix(0.856583, -0.947811, 1.205319, 1.089302, -251.460723, 228.820822)" xlink:href="#gradient-4"/>
		<linearGradient id="gradient-4">
			<stop offset="0.206" style="stop-color: {generateColor(primary)};"/>
			<stop offset="1" style="stop-color: {generateColor(secondary)};"/>
		</linearGradient>
		<filter id="drop-shadow-filter-1" color-interpolation-filters="sRGB" x="-50%" y="-50%" width="200%" height="200%">
			<feGaussianBlur in="SourceAlpha" stdDeviation="1"/>
			<feOffset dx="3" dy="3"/>
			<feComponentTransfer result="offsetblur">
				<feFuncA id="spread-ctrl" type="linear" slope="0.58"/>
			</feComponentTransfer>
			<feFlood flood-color="rgba(0,0,0,0.3)"/>
			<feComposite in2="offsetblur" operator="in"/>
			<feMerge>
				<feMergeNode/>
				<feMergeNode in="SourceGraphic"/>
			</feMerge>
		</filter>
		<linearGradient id="gradient-4-2" gradientUnits="userSpaceOnUse" x1="250" y1="211.367" x2="250" y2="288.632" gradientTransform="matrix(2.117156, -1.023286, 0.783822, 1.621715, -440.789734, 135.68454)" xlink:href="#gradient-4"/>
		<filter id="filter-1" color-interpolation-filters="sRGB" x="-50%" y="-50%" width="200%" height="200%">
			<feGaussianBlur in="SourceAlpha" stdDeviation="1"/>
			<feOffset dx="3" dy="3"/>
			<feComponentTransfer result="offsetblur">
				<feFuncA id="feFuncA-1" type="linear" slope="0.58"/>
			</feComponentTransfer>
			<feFlood flood-color="rgba(0,0,0,0.3)"/>
			<feComposite in2="offsetblur" operator="in"/>
			<feMerge>
				<feMergeNode/>
				<feMergeNode in="SourceGraphic"/>
			</feMerge>
		</filter>
		<linearGradient id="gradient-4-1" gradientUnits="userSpaceOnUse" x1="250" y1="211.367" x2="250" y2="288.632" gradientTransform="matrix(2.117156, -1.023286, 0.783822, 1.621715, -441.128571, 135.533746)" xlink:href="#gradient-4"/>
	</defs>
	<g style="filter: url('#point-light-filter-0');" id="object-0">
		<rect style="filter: none; stroke-width: 6px; fill: rgb(64, 64, 64); visibility: hidden; shape-rendering: geometricprecision;" y="1.147" width="500" height="497.706"/>
		<path d="{polygonPath}" style="paint-order: fill; fill-rule: nonzero; stroke: url('#gradient-4-0'); filter: url('#drop-shadow-filter-1'); stroke-width: {strokeWidth}px; fill: url('#gradient-0-0'); shape-rendering: geometricprecision;"/>
		<text letter-spacing="{textSize / 16}" style="font-family: &quot;Virtual Rave&quot;; font-size: {textSize}px; font-weight: 600; stroke-linejoin: round; stroke-width: 7px; text-anchor: middle; white-space: pre; fill: url(&quot;#gradient-4-2&quot;); filter: url(&quot;#filter-1&quot;);" x="{textPosition[0] + x}" y="{textPosition[1] + textSize / 2 + y}">{text}</text>
	</g>
</svg>
"""

def main():
	padding = 32

	st.title("Hexcede Generator")

	primary_color = st.color_picker("Pick a primary color", "#B1FF00")
	primary_color = tuple(int(primary_color[i:i+2], 16) for i in (1, 3, 5))

	side_count = st.slider("Side Count", min_value=3, max_value=64, value=6)

	text = st.text_input("Text", value="HC")

	text_size = st.slider("Font Size", min_value=10, max_value=200, value=136, help="I suggest a font size 105 for triangles but 136 for everything else if you're using 2 characters.")

	col1, col2 = st.columns(2)
	with col1: text_x = st.number_input("Text Position X", min_value=0, max_value=300, value=154)
	with col2: text_y = st.number_input("Text Position Y", min_value=0, max_value=300, value=128)

	svg = generateSVG(
		primary=primary_color,
		sideCount=side_count,
		text=text,
		textSize=text_size,
		textPosition=(text_x, text_y),
		x=padding,
		y=padding
	)

	canvasSize = ( 147 + padding ) * 2
	html = f"""
<style>
@font-face {{
  font-family: 'Virtual Rave';
  src: url("./static/Virtual%20Rave.ttf") format("truetype");
}}
</style>
<canvas id="svgCanvas" width="{canvasSize}" height="{canvasSize}" style="border:1px solid #000000;"></canvas>
<script>
	var svgString = `{svg}`;
	var canvas = document.getElementById('svgCanvas');
	var ctx = canvas.getContext('2d');

	var img = new Image();
	var svgBlob = new Blob([svgString], {{type: 'image/svg+xml;charset=utf-8'}});
	var url = URL.createObjectURL(svgBlob);

	img.onload = function() {{
		ctx.drawImage(img, 0, 0);
		URL.revokeObjectURL(url);
	}};

	img.src = url;
</script>
"""

	st.components.v1.html(html, height=canvasSize)
	st.download_button(label="Download as SVG", data=svg, file_name="image.svg", mime="image/svg")

if __name__ == "__main__":
	main()
