from PIL import Image
import sys

import pyocr
import pyocr.builders

#----------------------------------------------------------------------
# Check for the OCR tools and the avaliable language and uage language.
tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
# The tools are returned in the recommended order of usage
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))
# Ex: Will use tool 'libtesseract'

langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))
lang = langs[0]
print("Will use lang '%s'" % (lang))
# Ex: Will use lang 'eng'
#----------------------------------------------------------------------



#----------------------------------------------------------------------
# txt is a Python string
txt = tool.image_to_string(
    Image.open('test/image.png'),
    lang=lang,
    builder=pyocr.builders.TextBuilder()
)

with open("test/doc.txt", "w") as f:  
    f.write(txt)  

print(txt)
print('----------------------------------')


word_boxes = tool.image_to_string(
    Image.open('test/image.png'),
    lang="eng",
    builder=pyocr.builders.WordBoxBuilder()
)
#print the word with their pixel position
#print(line_and_word_boxes)
#----------------------------------------------------------------------

# #Converting to PDF
# from fpdf import FPDF 
   
# # save FPDF() class into  
# # a variable pdf 
# pdf = FPDF()    
   
# # Add a page 
# pdf.add_page() 
   
# # set style and size of font  
# # that you want in the pdf 
# pdf.set_font("Arial", size = 15) 
  
# # open the text file in read mode 
# f = open("test/doc.txt", "r") 
  
# # insert the texts in pdf 
# for x in f: 
#     pdf.cell(200, 10, txt = x, ln = 1, align = 'C') 
   
# # save the pdf with name .pdf 
# pdf.output("test/docpdf.pdf")  

#----------------------------------------------------------------------

if tool.can_detect_orientation():
    try:
        orientation = tool.detect_orientation(
            Image.open('test/image.png'),
            lang='eng'
        )
    except pyocr.PyocrException as exc:
        print("Orientation detection failed: {}".format(exc))
        sys.exit(1)
    print("Orientation: {}".format(orientation))
# Ex: Orientation: {
#   'angle': 90,
#   'confidence': 123.4,
# }

import sys
from fpdf import FPDF

orient = "land"
infile = "test/doc.txt"
outfile = "file.pdf"

if orient == 'land':
    pdf = FPDF(‘L’, ‘in’, ‘Letter’)
    font_height = 0.12
else:
    pdf = FPDF(‘P’, ‘in’, ‘Letter’)
    font_height = 0.16

pdf.add_page()
pdf.set_margins(0.25, 0.25)
pdf.set_auto_page_break(True, margin = 0.25)
if orient == ‘land’:
    pdf.set_font(‘Courier’, ”, 8)
else:
    pdf.set_font(‘Courier’, ”, 10)
pdf.set_xy(0.25, 0.25)

f = open(infile)
for line in f:
    pdf.write(font_height, line)
f.close()
pdf.output(outfile, ‘F’)