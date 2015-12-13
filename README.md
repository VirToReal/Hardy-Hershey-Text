# Hardy-Hershey-Text
Inkscape Addon for Hershey Text ***with Layouts***

This Extension is based on the already included Inkscape-Extension "Hershey Text" of Windell H. Oskay, www.evilmadscientist.com

# Included Features
- Added Layout managment System with xml Files - You define a Layout and the Extension will place Text at your wish
- Added new Single-Line Font "standard" by Andrew Mustun (QCad - http://qcad.org)
- Added Text Manipulation Parameters

# Known Issues
- there is no fancy Error-Reporting at the moment, if your .xml code is incorrect.

# Installation
This Extension is just tested with Linux at moment, should work with Windows too
- Place the hardyhershex.inx / hardyhershey.py / hardyhersheydata.py in the "extension" Folder of your Inkscape Installation - In Linux it should be here "/usr/share/inkscape/extensions/". 
- Open the Extension be selecting the "Extensions" -> "Render" -> "Hardy Hershey Text". 

# Define Layouts
- Make an .xml File with like the "example.xml" File, follow the Descriptions in the File or like the one below
- Use Layout 1 - 11, or edit the Names in the .inx File, the one in your .xml have to match with the ones in the .inx file
- Select the "Layout" Tab in the Extension and direct the Source-File of your XML File "/home/user/hello.xml" for example

# Use Layouts
- .xml File ready? 
- open "Render Text" in the "Extension" Tab, select a "Layout" you defined in the .xml file
- Select the "Action" -> "Use Layout" at the Drop-Down Menu
- Switch to "Layout" Tab, enter your Text in the Lines you defined in your Layout
- Press Apply and be glad :)

# Description of the XML File
***Text:***
	<coords>Line1</coords> Places the 1. Line of Text which is determined in the Inkscape-Plugin
	coords Attributes for manipulation an positioning of Text (Orgin-Point left/bottom)
	("x") X Position of Text-Field in mm (depending on Text Alignment / left = left-mid position of Text / right = right-mid position of text / center = mid position of text
	("y") Y Position of Text-Field in mm (Bottom Origin-Point)
	("align") Text Alignment (left/right/center/textcenter) // textcenter = orgin point is the center of text itself
	("tsize") Text Size in mm (Deviations between each Font)
	("fontf") Font Style
	("sbtwl") Space Between Letters (font specific value)
	("vertoff") Vertical Offset of Text (font specific value)
	("vcp") Vertical Compressing of Text (in %) (use "-" for negative compressing)
	("hcp") Horizontal Compressing of Text (in %) (use "-" for negative compressing)
	("margin") Left/Right Margin of Text in mm (if left/right, also on centered -> margin will be on both sides - If X Axis for Text-Positioning is defined, Margin will take effect on the opposite end)

***Render Graphics:***
	Lines:  <coords x="0" y="26" endx="10" endy="26">Stroke</coords> // Place the beginning of the Line with the x y Coordinates and the end x y Coordinates (in mm)

***Automatism:***
	FOR: <coords x="9" y="2.5" sbtwl="0" fontf="standard" align="textcenter" margin="3" tsize="5" vcp="0">FOR</coords> // Graps the the Value of Line 1 and Line 2, get its first Letters, and the count difference of Value in Line 1 and Line 2. Example ( Line 1: F10; Line 2: F12 ) now he places the <coords>-Commands with its "FOR"-Values and count up from Line 1 to the amount of <coords>-Commands with the Step you defined with Line 2.
	From the Above Example with 5x <coords>-Command Lines: F10 F12 F14 F16 F18
