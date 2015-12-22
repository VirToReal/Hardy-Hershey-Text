# Copyright 2011, Windell H. Oskay, www.evilmadscientist.com
# Modifications 2015, Benjamin Hirmer, www.virtograv.de
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import hardyhersheydata			#data file w/ Hershey font data
import inkex
import simplestyle
import re
import xml
from xml.dom import minidom

Debug = False # Set True for Debug-Mode

# Public Constants 
pxmm = 3.544 # Pixel/mm
mmpcpx1 = 6.05 # MM/Percent-PX Ratio for Standard Hershey Fonts
mmpcpx2 = 2.67 # MM/Percent-PX Ratio for added QCad-Single-Line Fonts
axaqcf = 2 # Allocate X-Axis QCad Fonts / Because thier Builded Frame is not like the Hershey ones
ayahf = -9 # Hershey fonts have no "0"-Line, this Constant defines it
yorigin = 1053 #Pixel to 0 Position of Inkscape-Document
pattern = re.compile('([a-zA-Z]{1,15})+([0-9.]{1,15})') # RegEx interpreting Looping

i = 1


def available(value):
	try:
	    value = float(value)
	except ValueError:
	    pass
	return bool(value)

def draw_svg_text(char, face, offset, vertoffset, parent):
	style = { 'stroke': '#000000', 'fill': 'none', 'stroke-width': '0.5', 'stroke-miterlimit': '4', }
	pathString = face[char]
	splitString = pathString.split()  
	midpoint = offset - int(splitString[0]) 
	pathString = pathString[pathString.find("M"):] #portion after first move
	trans = 'translate(' + str(midpoint) + ',' + str(vertoffset) + ')'
	text_attribs = {'style':simplestyle.formatStyle(style), 'd':pathString, 'transform':trans}
	inkex.etree.SubElement(parent, inkex.addNS('path','svg'), text_attribs) 
	if Debug:
	  inkex.debug("Char: " + str(char) + " PathString: " + str(pathString) + str(" Midpoint: " + str(midpoint) + " SplitString0: " + str(splitString[0]) + " SplitString1: " + str(splitString[1]) + "\n")) 
	return midpoint + int(splitString[1])	#new offset value

def make_string(string, font, spacing, spacing1, spacing2, group):
	#evaluate text string
	#Check which Font is selected 
	w = 0
	letterVals = [ord(q) - 32 for q in unicode(string,'utf-8')]
	if Debug:
	  inkex.debug("FOR Q: " + str(letterVals) + " String:" + str(string) + "\n")
	for q in letterVals:
		if Debug:
		  inkex.debug("For Q: " + str(q) + "\n")
		# Ignore unavailable Letters except german umlaute
		if (q == 164 or q == 182 or q == 188 or q == 191 or q == 196 or q == 214 or q == 220 or 0 <= q < 93):
			w = draw_svg_text(q, font, w+spacing1, spacing2, group)
		else:
			w += 2*spacing
			
	return w
      
def draw_stroke(xpa, ypa, endx, endy, parent):
	xpa = float(xpa)
	xpa = xpa * pxmm
  	ypa = float(ypa)
      	ypa = ypa * pxmm  # constant px/mm 
	ypa = -ypa + yorigin # Replace Origin Point to Inkscape-Document Origin Point (x axis is already clear)
	endy = float(endy)
	endy = endy * pxmm
	endy = -endy + yorigin
	endx = float(endx)
	endx = endx * pxmm
	
	if Debug:
	  inkex.debug("Stroke YPA: " + str(ypa) + " Stroke XPA: " + str(xpa) + "\n")
  
  	style = { 'stroke': '#000000', 'fill': 'none', 'stroke-width': '0.5', 'stroke-miterlimit': '4', }
	text_attribs = {'style':simplestyle.formatStyle(style), 'd':'M ' + str(xpa) + ' ' + str(ypa) + ' L ' + str(endx) + ' ' + str(endy)}
	inkex.etree.SubElement(parent, inkex.addNS('path','svg'), text_attribs) 
  
  	ll2g_attribs = {inkex.addNS('label','inkscape'):'Layout Sroke' }
	ll2g = inkex.etree.SubElement(parent, 'h', ll2g_attribs)
	tls = 'translate(0,0)' 
	ll2g.set( 'transform',tls)

def load_xml(filename, sel_layout, textlines, cur_layer): # Load XML File which selected from Configuration Tab
	try:
	  xmldoc = minidom.parse(filename)
	  LayoutsDOM(xmldoc, sel_layout, textlines, cur_layer)
	except xml.parsers.expat.ExpatError, e:
	  inkex.debug("Sorry, something seems wrong with your .xml File:\n" + str(e) + "\n\n")

def LayoutsDOM(layouts, sel_layout, textlines, cur_layer): # Loads the XML DOM end executes its selected Layouts
	layout = layouts.getElementsByTagName("layout")
	handleLayouts(layout, sel_layout, textlines, cur_layer)

def handleLayouts(layouts, sel_layout, textlines, cur_layer): # Handle each single Layout 
	for layout in layouts:
	    handleLayout(layout, sel_layout, textlines, cur_layer)

def handleLayout(layout, sel_layout, textlines, cur_layer): # Cut out its Layout-Title
	handleLayoutTitle(layout.getElementsByTagName("title")[0],layout, sel_layout, textlines, cur_layer)

def handleLayoutTitle(layout, layout2, sel_layout, textlines, cur_layer): # Place Text on its Coordinates and selected Alignment on matching with selected Layout
	layouttitle = layout.firstChild.data
	if layouttitle == sel_layout: 
	  sizex = layout2.getAttribute("x") # Get Width of Layout
	  sizey = layout2.getAttribute("y") # Get Height of Layout
	  handleCoords(layout2.getElementsByTagName("coords"), sizex, sizey, textlines, cur_layer)
	  if Debug:
	    inkex.debug(str("X: " + sizex) + str(" Y: " + sizey))
	    inkex.debug(str("LayoutTitle: " + layouttitle + " Selected Layout: " + str(sel_layout) + "\n"))
	
def handleCoords(coords, sizex, sizey, textlines, cur_layer): # Handle each Coordinates
	for coord in coords:
	    handleCoord(coord, sizex, sizey, textlines, cur_layer)

def handleCoord(coord, sizex, sizey, textlines, cur_layer): # Watch for seperate Alignment and Text Manipulation of eatch Text Coordinates
  	xpa = coord.getAttribute("x") # X Position of Text-Field (depending on text alignment / left = left-mid position of Text / right = right-mid position of text / center = mid position of text
	ypa = coord.getAttribute("y") # Y Position of Text-Field (depending on text alignment / left = left-mid position of Text / right = right-mid position of text / center = mid position of text
	align = coord.getAttribute("align") # Text Align 
	tsize = coord.getAttribute("tsize") # Text Size 
	textf = coord.getAttribute("fontf") # Font Face
	sbtwl = coord.getAttribute("sbtwl") # Space Between Letters
	vco = coord.getAttribute("vertoff") # Vertical Offset of Text
	vcp = coord.getAttribute("vcp") # Vertical Compressing of Text
	hcp = coord.getAttribute("hcp") # Horizontal Compressing of Text
	mrg = coord.getAttribute("margin") # Left/Right Margin of Text (only needed on left/right Text-Alignment)
	val_coord = coord.firstChild.data # This Value contain the Line of Text in the Layout-Tab on GUI
	
	if val_coord == "Stroke":
	  endx = coord.getAttribute("endx") # This Value contain the end x Coordinate in mm for a rendered Stroke
	  endy = coord.getAttribute("endy") # This value contain the end y Coordinate in mm for a rendered Stroke
	
	# Check Textline and Place Text
	if val_coord == 'Line 1':
	  textline = textlines[0]
	elif val_coord == 'Line 2':
	  textline = textlines[1]
	elif val_coord == 'Line 3':
	  textline = textlines[2]
	elif val_coord == 'Line 4':
	  textline = textlines[3]
	elif val_coord == 'Line 5':
	  textline = textlines[4]
	elif val_coord == 'Stroke':
	  draw_stroke(xpa, ypa, endx, endy, cur_layer)
	  textline = False
	elif val_coord == 'FOR':
	  textline1 = textlines[0]
	  textline2 = textlines[1]
	  startPlacerLoop(cur_layer, textline1, textline2, sizex, sizey, xpa, ypa, align, tsize, textf, sbtwl, vco, vcp, hcp, mrg) #Place Looped Text
	  textline = False
	else:
	  textline = False
	  
	if textline:
	  placeLayoutetText(cur_layer, textline, sizex, sizey, xpa, ypa, align, tsize, textf, sbtwl, vco, vcp, hcp, mrg) #Place Text
	if Debug:
	  inkex.debug(str("Koordinaten: " + val_coord) + str(" Ausrichtung: " + align + "\n"))

def startPlacerLoop(cur_layer, textline1, textline2, sizex, sizey, xpa, ypa, align, tsize, textf, sbtwl, vco, vcp, hcp, mrg):
	regline1 = pattern.match(str(textline1))
	regline2 = pattern.match(str(textline2))
	VAR1 = regline1.group(1)
	INT1 = regline1.group(2)
	VAR2 = regline2.group(1)
	INT2 = regline2.group(2)
	INTDIFF = int(INT2) - int(INT1)
	
	global i
	if i < 2:
	  textline = VAR1 + INT1
	else:
	  textline = VAR1 + str(int(INT1) + INTDIFF * (i-1))
	placeLayoutetText(cur_layer, textline, sizex, sizey, xpa, ypa, align, tsize, textf, sbtwl, vco, vcp, hcp, mrg)
	
	if Debug:
	  inkex.debug(str("Looper: " + textline) + str(" Int: " + str(i) + "\n"))
	i += 1
	  

def placeLayoutetText(cur_layer, textline, sizex, sizey, xpa, ypa, align, tsize, textf, sbtwl, vco, vcp, hcp, mrg):
  	
	# Define Standard Values
	if sbtwl == "":
	  sbtwl = 0
	
	if available(vcp): # Define Standard-Values of vcp / Vertical Compressing
	  vcp = float(vcp)
	  vcp = vcp / 100
	else:
	  vcp = 0
	    
	if available(mrg): # Define Standard-Values of mrg / Margin of Text
	  mrg = float(mrg) * pxmm
	else:
	  mrg = 0 * pxmm #Value in mm
	    
	if available(hcp): # Define Standard-Values of hcp / Horizontal Compressing
	  hcp = float(hcp)
	  hcp = hcp / 100
	else:
	  hcp = 0
	  
	if textf != "standard": # Stretch some unproportional Fonts fot matching in Height to each other (approximately)
	    vcp = vcp / 2.27
	    hcp = hcp / 2.27
	    
	if tsize != "": # Resize Text if tsize / Text Size / is defined
	    if Debug:
	      inkex.debug("1. Textsize VCP: " + str(vcp) + " 1. Textsize HCP: " + str(hcp) + "\n")
	
	    if textf != "standard":
	      vcp += float(tsize) / mmpcpx1 # Divide wished Font-Size with its mean height value (in mm) ( Add Values if Compressing is enabled)
	      hcp += float(tsize) / mmpcpx1
	    else:
	      vcp += float(tsize) / mmpcpx2 # Divide wished Font-Size with its mean height value (in mm) ( Add Values if Compressing is enabled)
	      hcp += float(tsize) / mmpcpx2
	    
	    if Debug:
	      inkex.debug("2. Textsize VCP: " + str(vcp) + " 2. Textsize HCP: " + str(hcp) + "\n")
	    
	if xpa == "":
	  xpa = 0
	else:
	  xpa = float(xpa)
	  
	if ypa == "":
	  ypa = 0
	else:
	  ypa = float(ypa)
  
	sizex = float(sizex) * pxmm
	sizey = float(sizey) * pxmm
  
	ll1g_attribs = {inkex.addNS('label','inkscape'):'Layout Line' }
	ll1g = inkex.etree.SubElement(cur_layer, 'g', ll1g_attribs)
	
	# Define allocated X-Coordinate of QCad-Fonts and "0"-Line of Hershey Fonts
	if textf == "standard":
	  axpa = axaqcf * vcp
	  aypa = 0
	else:
	  aypa = ayahf * hcp
	  axpa = 0
	
	textf = eval('hardyhersheydata.' + textf)
	length = make_string(textline, textf, 0, int(sbtwl), vco, ll1g)
	
	if align == 'center': # If Alignment of Text is "centered"
	  if length * vcp + mrg*2 > sizex: # If Text-Length is longer as the allocated Space, compress it automatically
	    vcp = (length - ( length - ( sizex - mrg*2 ) )) / ( length )
	  xpa = (( sizex - (float(length) * (float(vcp))) ) / 2) - axpa # Calculate Center even if Horizontal Compressed 
	  
	elif align == 'left': # If Alignment of Text is "left"
	  if length * vcp + mrg > sizex: # If Text-Length is longer as the allocated Space, compress it automatically
	    vcp = (length - ( length - ( sizex - mrg ) )) / ( length )
	  xpa = mrg - axpa
	  
	elif align == 'right': # If Alignment of Text is "right"
	  if length * vcp + mrg > sizex: # If Text-Length is longer as the allocated Space, compress it automatically
	    vcp = (length - ( length - ( sizex - mrg ) )) / ( length )
	  xpa = sizex - length*vcp - mrg - axpa
	  
	elif align == "textcenter": # If Alignment of Text itself is "centered"
	  xpa = ( xpa * pxmm ) - ( ( length*vcp ) / 2 )
	  
	else:
	  if length * vcp + mrg + xpa*pxmm > sizex: # If Text-Length is longer as the allocated Space, compress it automatically
	    vcp = (length - ( length - ( sizex - mrg - xpa*pxmm ) )) / ( length )
	  xpa = xpa * pxmm - axpa # constant px/mm
	
	ypa = (ypa * pxmm) - aypa # constant px/mm 
	ypa = -ypa + yorigin # Replace Origin Point to Inkscape-Document Origin Point (x axis is already clear)
	
	tlc = 'translate(' + str(xpa) + ',' + str(ypa) + ') ' + 'scale(' + str(vcp) + ', ' + str(hcp) + ')' # Top Left Corner
	ll1g.set( 'transform',tlc)
	
	if Debug:
	  inkex.debug("length: " + str(length) + " sizex: " + str(sizex) + " vcp: " + str(vcp) + "\n")
	
	del (vcp, hcp)

class Hershey( inkex.Effect ):
	def __init__( self ):
		inkex.Effect.__init__( self )
		self.OptionParser.add_option( "--tab",	#NOTE: value is not used.
			action="store", type="string",
			dest="tab", default="splash",
			help="The active tab when Apply was pressed" )
		self.OptionParser.add_option( "--text",
			action="store", type="string", 
			dest="text", default="Hershey Text for Inkscape",
			help="The input text to render")
		self.OptionParser.add_option( "--action",
			action="store", type="string",
			dest="action", default="render",
			help="The active option when Apply was pressed" )
		self.OptionParser.add_option( "--layout",
			action="store", type="string",
			dest="layout", default="none",
			help="Use an Layout when Apply was pressed" )
		self.OptionParser.add_option( "--fontface",
			action="store", type="string",
			dest="fontface", default="rowmans",
			help="The selected font face when Apply was pressed" )
		self.OptionParser.add_option( "--spacing1",
			action="store", type="string", 
			dest="spacing1", default="0",
			help="Spacing between the Letters")
		self.OptionParser.add_option( "--spacing2",
			action="store", type="string", 
			dest="spacing2", default="3",
			help="Spacing between the Glyph-Table")
		self.OptionParser.add_option( "--spacing3",
			action="store", type="string", 
			dest="spacing3", default="0",
			help="Vertical Offset of Text-Segment")
		self.OptionParser.add_option( "--compressy",
			action="store", type="string", 
			dest="compressy", default="0",
			help="Vertical Compressing an Text-Segment")
		self.OptionParser.add_option( "--compressx",
			action="store", type="string", 
			dest="compressx", default="0",
			help="Horizontal Compressing an Text-Segment")
		self.OptionParser.add_option( "--metric",
			action="store", type="string", 
			dest="metric", default="0",
			help="Use Metric or Pixel (True/False)")
		self.OptionParser.add_option( "--ll1",
			action="store", type="string", 
			dest="ll1", default="",
			help="First Layout Line")
		self.OptionParser.add_option( "--ll2",
			action="store", type="string", 
			dest="ll2", default="",
			help="Second Layout Line")
		self.OptionParser.add_option( "--ll3",
			action="store", type="string", 
			dest="ll3", default="",
			help="Third Layout Line")
		self.OptionParser.add_option( "--ll4",
			action="store", type="string", 
			dest="ll4", default="",
			help="Fourth Layout Line")
		self.OptionParser.add_option( "--xmlfile",
			action="store", type="string", 
			dest="xmlfile", default="",
			help="Source of Filename ")
		self.OptionParser.add_option( "--ll5",
			action="store", type="string", 
			dest="ll5", default="",
			help="Fifth Layout Line")

	def effect( self ):

		g_attribs = {inkex.addNS('label','inkscape'):'Hershey Text' }
		g = inkex.etree.SubElement(self.current_layer, 'g', g_attribs)
		font = eval('hardyhersheydata.' + str(self.options.fontface))
		clearfont = hardyhersheydata.futural  
		#Baseline: modernized roman simplex from JHF distribution.
		
		w = 0  #Initial spacing offset
		
		# spacing1 between letters
		if self.options.spacing1 != "":
		  spacing1 = float(self.options.spacing1)
		else:
		  spacing1 = 0
		  
		# spacing2 between the Glyph-Table
		if self.options.spacing2 != "":
		  spacing = float(self.options.spacing2)
		else:
		  spacing = 0
		  
		# spacing3 Vertical Offset of Text-Segment
		if self.options.spacing3 != "":
		  spacing2 = float(self.options.spacing3)
		else:
		  spacing2 = 0
		  
		# compressy Vertical Compressing of Text-Segment
		if self.options.compressy != "":
		  compressy = float(self.options.compressy)
		  compressy = compressy / 100
		else:
		  compressy = 1
		  
		# compressx Horizontal Compressing of Text-Segment
		if self.options.compressx != "":
		  compressx = float(self.options.compressx)
		  compressx = compressx / 100
		else:
		  compressx = 1
		  
		# compressx Horizontal Compressing of Text-Segment
		if self.options.metric == "true":
		  metric = True
		else:
		  metric = False

		if self.options.action == "render":
		  w = make_string(self.options.text, font, spacing, spacing1, spacing2, g)
	
		elif self.options.action == "table":
			#Generate glyph table
			wmax = 0;
			for p in range(0,10):
				w = 0
				v = spacing * (15*p - 67 )
				for q in range(0,10):
					r = p*10 + q 
					if (r < 0) or (r > 95):
						w += 5*spacing
					else:
						w = draw_svg_text(r, clearfont, w+spacing1, v, g)
						w = draw_svg_text(r, font, w+spacing1, v, g)
						w += 5*spacing
				if w > wmax:
					wmax = w
			w = wmax
			
		elif self.options.action == "layout":
		  
		  #Generate from Layout
		  if self.options.layout != "":
		    
			textlines = self.options.ll1, self.options.ll2, self.options.ll3, self.options.ll4, self.options.ll5 # Make Tuple out of Layout Text-Lines
			load_xml(self.options.xmlfile, self.options.layout, textlines, self.current_layer) # Submit Layout
			
			
		t = 'translate(' + str( self.view_center[0] - w*compressx/2) + ',' + str( self.view_center[1] ) + ')' + ' scale(' + str(compressy) + ', ' + str(compressx) + ')' 
		g.set( 'transform',t)

if __name__ == '__main__':
    e = Hershey()
    e.affect()

