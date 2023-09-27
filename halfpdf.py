#!python3
# version v0.01 - 2023-09-27
# Author A.Hanselmann,(c) GNU GPL 3.0

#2do comandline width/height/padding input
# to install "fitz" library run "pip install pymupdf"

import fitz
import os,argparse,sys

# --------------------------------------
# argument parser setop
parser = argparse.ArgumentParser(
                    prog='halfpdf',
                    description='generates a pdf with 2 pages for every page',
                    epilog='Consider running in cli mode (not implemented)')

parser.add_argument('filename')    
parser.add_argument('-dd', '--script1del',
                    action='store_true', help='remove from output specific ( blank ) pages')
parser.add_argument('-l', '--limited',
                    action='store_true', help='limit number of pages processd to 30')
parser.add_argument('-v', '--verbose',
                    action='store_true', 
    help='display crop area and pagenumbers')
parser.add_argument('-s','--split', 
                    action='store_true',
help='split a page in 2 vertical equal areas (e.g a4-> top a5 and bottom a5')
parser.add_argument('-1', '--script1',
                    action='store_true', 
    help='cut for settings script1')
parser.add_argument('-2', '--script2',
                    action='store_true', 
    help='cut for settings script2')
parser.add_argument('-3', '--script3',
                    action='store_true', 
    help='cut for settings script3 (modify code here)')
parser.add_argument('-tf', '--topframe',nargs=4,
    help='give coordinates for topframe (topleft_x,tleft_y,bottomright_x, bottomright_y). Topleft corner is (0,0). (not implemented)')
parser.add_argument('-bf', '--bottomframe',nargs=4,
    help='give coordinates for top frame (topleft_x,tleft_y,bottomright_x, bottomright_y. Topleft corner is (0,0). (not implemented)')

# parse arguments
args = parser.parse_args()

# check on mode
if not args.script1 and not args.script2 and not args.script3 and not args.split:
    print('nothing to do. Coose mode (e.g script1 )  or activate mode --split')
    sys.exit()

# readin file twice, file is first positioal argument
doc1=fitz.open(args.filename)
doc2=fitz.open(args.filename)

# read first page. if this were to have a different layout from the rest
# the cutting process is going to fail
p=doc1[0]

(xstart, ystart, xend, yend ) = p.cropbox
ypadding =0

# check on simple split mode
if args.split: 
    width = xend - xstart 
    height = (yend-ystart)/2 
# check other modes 1/2/3, modify 3 for your own values
elif args.script1:
    (xstart,width) = (20,565)
    (ystart,yend) = (50,792)
    height = 390
elif args.script2:
    (xstart,width) = (xstart+20,xend-xstart-30)
    (ystart,yend) = (ystart+50,yend-50)
    height = (yend-ystart)/2
    ypadding=20
# enter your own values here
elif args.script3:
    (xstart,width) = (xstart+20,xend-xstart)
    (ystart,yend) = (ystart+50,yend-50)
    height = (yend-ystart)/2+20

# set pages processed, dummy unless --limit is specified
maxpages=30

if not args.limited or maxpages > doc1.page_count:
   maxpages=doc1.page_count

# generate outputfilename from inputfile_out.pdf'
filename=os.path.splitext(args.filename)
outfile=f'{filename[0]}_out{filename[1]}'


if args.verbose:
    print("Document has dimensions=",p.cropbox, " (topx,topy,botx,boty)")
    print(f'The input is truncated/has  {maxpages} pages, output {2 * maxpages} pages', 
        f'(width={width} height={height})')
    print(f'outfile is {outfile}')

    print('cutting into top and  bottom frames: format (xtop,ytop,width,yend)')

    print("TOP--- ({:>5},{:>5},{:>5},{:>5})".format(
xstart,ystart,width,ystart+height))
    print("BOTTOM ({:>5},{:>5},{:>5},{:>5})".format(
xstart,yend-height,width,yend))

# --------------------------------------
# main part: do the cutting
for a in range(maxpages):

    pageup=doc1[a]
    pagedown=doc2[a]

    pageup.set_cropbox(fitz.Rect(xstart, ystart, width, ystart+height+ypadding))
    pagedown.set_cropbox(fitz.Rect(xstart, yend-height-ypadding, width, yend))


# assemble new pdf
d=fitz.Document()
for a in range(maxpages):

    d.insert_pdf(doc1,a,a)
    d.insert_pdf(doc2,a,a)


# if option checked, delete empty pages at beginning
if args.script1del:
    l=[0,4,5,6,7,8,]
    l.extend(range(12,2*maxpages))

    d.select (l)

# save and exit
d.save(outfile,garbage=3)



