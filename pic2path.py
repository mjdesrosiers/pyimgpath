from PIL import Image
import copy
import sys
import time
from random import shuffle
from itertools import permutations

COLOR_BLACK = 1;
XSCALE = 5;
YSCALE = 150;
XOFFSET = 0;
YOFFSET = 0;

datafile2 = open("data_test.txt", 'w')

def findshape(imagearr):
	"""
	findshapes
		Arguments: 		imagearr - a 2D array of 1's (black) and 0's (white) representing the whole image
		Returns: 		outarray - a 2D array of 1's (black) and 0's (white) representing the input image minus the found shape
						shapearr - a 2D array of 1's (black) and 0's (white) representing the shape that was found
		Decription: 	Finds a shape from within the image
		Methodology:
			-from bottom to top, left to right
				-Locate bottom left of shape
				-repeat until list of pixels to check is empty
					-search left, right, up, then down for black pixels
						-if a pixel is black and hasn't already been checked, add it to list of pixels to check
						-add current pixel to list of checked pixels
					-proceed to next pixel in list of pixels to check
	"""		

	# find a contiguous shape within the black and white image
	# returns (shapearr, newarr)
	# shapearr is the array where the shape is
	# new arr is the input array with the shape taken out
	
	# get the width and height of the image in
	height, width = (len(imagearr), len(imagearr[0]))
	
	# create two arrays that are empty, of the same size
	shapearr = [[0 for i in range(width)] for j in range(height)]
	
	# get the starting coordinates of the first found shape
	startx, starty = -1, -1;
	
	#iterate through the rows of the image array, starting at the bottom
	for i in reversed(xrange(0, height)):	
		#for each row
		try: 
			starty = i							#sets the starting row for the shape
			startx = imagearr[i].index(1)		#finds the first column with index of "1" (pixel is black)
												#if no column in the current row has an index on "1" a ValueError is returned
			break;
			
		#skips this row if index of "1" is not found in the row
		except ValueError:
			pass;
	
	if startx == -1:
		raise(ValueError('No shape found in input image.'))
			
	# start an array, seed it with the starting position we found
	cellstocheck = [(startx, starty)]
	# start an alreadychecked array, so we don't infinitely recurse
	alreadysearched = [];
	npixels = 0;
	
	while len(cellstocheck) != 0:
		# get a position
		(currentx, currenty) = cellstocheck.pop()
		# say we've searched it
		alreadysearched.append((currentx, currenty))
		
		
		if imagearr[currenty][currentx]:							#if the current pixel is black
			npixels += 1;											#add to the pixel count		
			shapearr[currenty][currentx] = 1;						#set the pixel in the shape array to black
			
			#won't check leftwards if at the far left of array
			if currentx != 0:													
				#check if the cell to the left has already been checked
				#if cell hasn't been checked, add it to array of cells to check
				try	:					
					alreadysearched.index((currentx-1,currenty))	
				except ValueError:
					cellstocheck.append((currentx-1,currenty))		
			
			#won't check rightwards if at the far right of array			
			if currentx != width-1:
				#check if the cell to the right has already been checked
				#if cell hasn't been checked, add it to array of cells to check
				try	:
					alreadysearched.index((currentx+1,currenty))
				except ValueError:
					cellstocheck.append((currentx+1,currenty))

			#won't check upwards if at the top of array
			if currenty != 0:
				#check if the cell upwards has already been checked
				#if cell hasn't been checked, add it to array of cells to check
				try	:
					alreadysearched.index((currentx,currenty-1))
				except ValueError:
					cellstocheck.append((currentx,currenty-1))
					
			#won't check downwards if at the bottom of array		
			if currenty != (height-1):
				#check if the cell downwards has already been checked
				#if cell hasn't been checked, add it to array of cells to check
				try:
					alreadysearched.index((currentx,currenty+1))
				except ValueError:
					cellstocheck.append((currentx,currenty+1))	
	
	#deep copies the image array (makes a copy not linked in memory)
	outarray = copy.deepcopy(imagearr)
	
	#erases the image that is found from the copied image array (sets all the black pixels to white)
	for i, row in enumerate(shapearr):
		for j, data in enumerate(row):
			if data:
				outarray[i][j] = 0;
	
	#if the number of pixels in the shape is less than 10, clear the shape array (change ALL pixels to white)
	if npixels < 10:
		shapearr = [[0 for i in range(width)] for j in range(height)];

	#return outarray which is the input image array with the current shape subtracted
	#and shapearr which is an array that contains only the current shape
	return (outarray, shapearr)


def shapetopaths(shapearr, write_to_file):
	"""
	shapetopaths
		Arguments: 		shapearr - a 2D array of 1's (black) and 0's (white) representing a shape
		Returns: 		N/A
		Decription: 	converts a single shape into a set of SPIN commands that will draw it
		Methodology:
			-repeat until all shapes drawn
				-Locate bottom left of shape and top of shape
				-Repeat until top of shape is reached
					-scan each line with arraytoprintcmds to get drawing coordinates
					-reverse scan direction
				-clean up drawing coordinates
				-write SPIN commands to file
	"""		

	#retrieves the dimensions of the shape array
	height, width = (len(shapearr), len(shapearr[0]))

	startx, starty, endy = 0, 0, 0;
	
	#iterate through the rows of the image array, starting at the bottom
	for i in reversed(xrange(0, height)):
		#for each row check if the row is not empty
		try: 
			starty = i								#sets the starting row for the shape
			startx = shapearr[i].index(1)			#finds the first column with index of "1" (pixel is black)
													#if no column in the current row has an index on "1" a ValueError is returned
			break;
			
		#skips this row if index of "1" is not found in the row, proceeds to the next row up
		except ValueError:
			2+2;
			
			
	#iterate through the rows of the image array, starting at the top
	for i in xrange(0, height):
		#for each row check if the row is not empty
		try: 
			endy = i								#sets the ending row for the shape (highest row)
			shapearr[i].index(1)					#finds the first column with index of "1" (pixel is black)
													#if no column in the current row has an index on "1" a ValueError is returned
			break
			
		#skips this row if index of "1" is not found in the row, proceeds to the next row down		
		except ValueError:
			pass;
	
	
	
	currentx, currenty = startx, starty
	
	fw = 1				#sets values corresponding to forward and backward scans
	bw = -1
	
	dir = fw			#starts out scanning forward
	
	oldx = 0;			
	
	coordslist = [];
	
	#iterates through the rows of the shape, from bottom to top
	for i in reversed(range(endy, starty+1)):
		#print("move to y = " + str(height-i))
		
		#alternates scanning rows forwards then backwards
		if dir == fw:	#scans forwards
		
			#gets a set of coordinates to move to
			(oldx, outcoords) = arraytoprintcmds(shapearr[i], i, oldx, dir=fw)
			#appends the coordinate movements from the last line to the existing list of coordinate movements
			for coord in outcoords:
				coordslist.append(coord)
			dir = bw		#switch directions
			
		else:	#scans backwards
			#gets a set of coordinates to move to
			(oldx, outcoords) = arraytoprintcmds(shapearr[i], i, oldx, dir=bw)
			#appends the coordinate movements from the last line to the existing list of coordinate movements
			for coord in outcoords:
				coordslist.append(coord)
			dir = fw		#switch directions
	
	#cleanup the list of coordinate list to eliminate unnecessary move commands when the x-coordinate remains
	#constant multiple movements
	coordslist = cleanup(copy.deepcopy(coordslist))
	
	#make sure there are movements to be made
	if len(coordslist) == 0:
		return
		
	#get the first set to coordinates
	x1, y1 = coordslist[0]
	if write_to_file:		
		#datafile.write("MT(" + str(x1+XOFFSET) + "," + str(y1) + ")\n");	#move once to the desired location
		datafile.write(str(x1+XOFFSET)+","+str(y1+YOFFSET)+"\n")
		#datafile.write("MT(" + str(x1+XOFFSET) + "," + str(y1) + ")\n"); 	#move again to the desired location to mitigate overshoot
		datafile.write(""+str(x1+XOFFSET)+","+str(y1+YOFFSET)+"\n")
		datafile.write("1,1\n")										#set the pen down
		
		#iterate through the sets of coordinates in the list
		for x, y in coordslist[1:]:
			datafile.write(""+str(x+XOFFSET)+","+str(y+YOFFSET)+"\n")
		"""
	#also doesnt do anything anymore because -1,0 and -1,-1 coordinates arent appended to the end of lines
			if x == -1:
				if y == 0:
					datafile.write("PU\n");
				else:
					datafile.write("PD\n");
	#end of "also doesnt do anything anymore?"
			
			
			#will always evaluate here because block above doesnt do anything?
			else:
				datafile.write("MT(" + str(x+XOFFSET) + "," + str(y) + ")\n");
			"""
			
		#move the pen up at the end of the shape		
		#datafile.write("PU\n")
		datafile.write("1,0\n")	
		

	return coordslist;


def arraytoprintcmds(line, starty, oldx, dir):
	"""
	arraytoprintcmds
		Arguments: 		line - an array of 1's and 0's representing a horizontal row of pixels
						starty - the row index of the array argument "line"
						oldx - no longer used
						dir - either 1 (forward) or -1 (backward) specifying the direction of scan
		Returns: 		endx - the index of the last black pixel in the current row
						setofcoords - an array of coordinates that should be moved to in order to draw the shape
		Decription: 	converts a single line into a set of coordinates to be drawn
		Methodology:
			-repeat until end of line array
				-Scan line to find first black pixel
				-Scan line to find next white pixel
				-convert local indices of line to global coordinates used for printing
				-append coordinates to setofcoords to be returned
	"""	
	#initialize local variables
	width = len(line)
	current_x = 0
	more_exist = True
	line_start, line_end = 0, 0;	
	endx = 0;
	setofcoords = [];
	
	
	if dir == 1:											#scanning forward	
		while more_exist:									#while there are still more lines to scan									
			try:
				#for each line array
				line_start = line[current_x:].index(1)				#scan the line for a local index of the first black pixel
				line_end = line[current_x+line_start:].index(0)		#find a local index of the next white pixel past the last black one
				line_start += current_x								#convert the local start index to global start index
				line_end += line_start								#convert the local end index to global end index
				#datafile.write("\tdrawing line from " + str(line_start) + " to " + str(line_end-1))

				sxpos = XSCALE * line_start							#convert the line indices to the x-coordinate system of quad encoder		
				expos = XSCALE * line_end							#convert the line indices to the x-coordinate system of quad encoder
				ypos = 	YSCALE * starty								#convert the current y index to our y-coordinate system
				
				
		#do these do anything anymore???
				if abs(sxpos-oldx) > 30:
					# setofcoords.append((-1, 0))
					pass;
				setofcoords.append((ypos, sxpos))
				if abs(sxpos-oldx) > 30:
					# setofcoords.append((-1, -1))
					pass;
		#end of "do these do anything???"	
			#---> if they don't do anything, I don't think the oldx argument is necessary anymore
				
				
				#make sure the line is not one pixel wide	
				if abs(sxpos-expos) != XSCALE:
					#add the row and the final x position coordinates to an array
					setofcoords.append((ypos, expos))
				
				endx = expos							#update the endx that will be returned
				current_x = line_end+1					#move the position of current x so the rest of the line can be searched
				#raw_input();
				
				
			except ValueError:
				more_exist = False
				pass		
	
	#scanning backwards		
	else:								#same as forwards but with reversed indexing						
		while more_exist:
			max = width - 1
			bwline = (copy.deepcopy(line))
			bwline.reverse()
			try:
				line_start = bwline[current_x:].index(1)+current_x
				line_end = bwline[line_start:].index(0)-1+line_start
				#datafile.write("\tdrawing line from " + str(max-line_start) + " to " + str(max-line_end))
				sxpos = XSCALE * (max-line_start)
				expos = XSCALE * (max-line_end)
				ypos = 	YSCALE * starty
				
				
		#do these do anything anymore???
				if abs(sxpos-oldx) > 30:
					# setofcoords.append((-1, 0))
					pass;
				setofcoords.append((ypos, sxpos))
				if abs(sxpos-oldx) > 30:
					# setofcoords.append((-1, -1))
					pass;
		#end of "do these do anything anymore???"			
			#---> if they don't do anything, I don't think the oldx argument is necessary anymore		
					
				if abs(sxpos-expos) != XSCALE:
					setofcoords.append((ypos, expos))
				endx = expos
				current_x = line_end+1
			except ValueError:
				more_exist = False
				pass
				
	return (endx, setofcoords)
	

def cleanup(coordslist):
	"""
	cleanup
		Arguments: 		coordslist - a list of coordinates to be optimized
		Returns: 		coordslist - the optimized list of coordinates
		Decription: 	removes extraneous coordinate movements
		Methodology:
			-iterate through coordinate list
			-look for consecutive coordinates with constant x coordinate
			-deletes intermediate coordinates, leaving only 2 consecutive
			 coordinates with the same x
	"""	
	
	# optimizations:
	#	-for long sequences along the x-axis, combine these into one command
	#		by dropping off all the intermediary commands
	
	# break it up by penup/down commands
	
	npaths = 0;
	
	# get the number of total seperate paths sorted by penup/pendown commands
	elems_to_drop = [];
	pen_cmd_nums = [];
	for i, (x, y) in enumerate(coordslist[:-1]):
	
		# if the next x coordinate is equal to the current one, 
		# and isn't a pen command,		
		if y == coordslist[i+1][1] and x != -1 and (i not in elems_to_drop):
			endnum = i;
			
			# seek through the rest of the list:
			for j, (xi, yi) in enumerate(coordslist[i:]):
				# if we've found a different x coordinate,
				if yi != y:
					break;
				else:
					endnum += 1;
			
			for numtodrop in range(i+1, endnum-1):
				elems_to_drop.append(numtodrop);
	for numtodrop in reversed(elems_to_drop):
		del(coordslist[numtodrop])			
	
	return coordslist

def length(x1, y1, x2, y2):
	return pow((pow(x1-x2, 2) + pow(y1-y2,2)),.5)
	
def greedy_sort(coordslist):
	prevx, prevy = 0, 0;
	possibilities = range(0, len(coordslist))
	zero_lens = [];
	for i, coords  in enumerate(coordslist):
		if coordslist[i] == None:
			zero_lens.append(i)
			
	for index in reversed(zero_lens):
		del(possibilities[index])
	
	order = [];
	while len(possibilities) != len(order):
		mindistance = sys.float_info.max
		minnumber = -1;
		
		for possibility in possibilities:
			if possibility not in order:
				startx, starty = coordslist[possibility][0]
				startx /= YSCALE
				starty /= XSCALE
				
				if length(prevx, prevy, startx, starty) < mindistance:
					mindistance = length(prevx, prevy, startx, starty)
					minnumber = possibility
		
		prevx, prevy = coordslist[minnumber][-1]
		
		prevx /= YSCALE
		prevy /= XSCALE
	
		order.append(minnumber)
	
	return order
	
	
def main(filename, optimize = False):
	"""
	Main
		Arguments: 		filename - name of the image file to be analyzed
		Returns: 		N/A
		Decription: 	prints a series of spin commands to a data file
		Methodology:
			-Open Image
			-Convert image to array of 1's (black) and 0's (white)
			-Repeat until shapes exhausted
				-Find shape with "findshape"
				-Convert shape to path with "shapetopath"
					-Process shape for coordinates to move to with "arraytoprintcmds"
					-Clean up movement coordinates with "cleanup"
					-write movement coordinates to file
	"""
	#open the file and get the image size
	im = Image.open(filename);		
	height, width = im.size;
		
	# make an empty array for the pixel data
	pixelarray = [[0 for i in range(height)] for j in range(width)];
	
	# this loop turns the (rgba) tuples into 0(white) and 1(black)
	for i, row in enumerate(pixelarray):
		for j, data in enumerate(row):
			if not im.getpixel((j, i))[0]:
				pixelarray[i][j] = 1;

	nomoreshapes = False
	nshapes = 0;
	shapesarr = [];
	
	#repeat until all shapes are found
	while not nomoreshapes:
		try:
			starttime = time.time()									#note when time when we start to find a shape
			(newarr, shapearr) = findshape(pixelarray)				#get a shape array and the updated image array		
			pixelarray = newarr										#update the image array so the next shape can be found								
			nshapes += 1;											#increment the shape counter
			
			#print info about how long it took to find the current shape
			print("found shape " + str(nshapes) + " in " + str(round(time.time()-starttime,2)) + " s")	
			
			shapesarr.append(shapearr);
			
		
		except ValueError:
			print("done finding shapes")
			nomoreshapes = True
			pass	
	
	print("with nshapes = " + str(nshapes))	
	
	if optimize:
		pathsarr = []
		for shape in shapesarr:
			pathsarr.append(shapetopaths(shape, False))
			
		pathorder = greedy_sort(copy.deepcopy(pathsarr))
		print(pathorder)
		for shapenum in pathorder:
			#datafile.write("'BEGIN SHAPE " + str(shapenum) + '\n')
			#analyze the shape and write SPIN commands to the file
			shapetopaths(shapesarr[shapenum], True)
			#print a SPIN comment denoting the end of a shape and its number
			#datafile.write("'END SHAPE   " + str(shapenum) + '\n')
		
	else:
		for i, shape in enumerate(shapesarr):
			#datafile.write("'BEGIN SHAPE " + str(i) + '\n')
			#analyze the shape and write SPIN commands to the file
			shapetopaths(shape, True)
			#print a SPIN comment denoting the end of a shape and its number
			#datafile.write("'END SHAPE   " + str(i) + '\n')
	
			
	
#seems like this does something simple but code is technical and I'd rather just ask you
if __name__ == "__main__":	
	if len(sys.argv) >= 2:
		global datafile
		datafile = open(str(sys.argv[1][:-4])+".csv", 'w')		
		starttime = time.time()
		if len(sys.argv) ==3 and sys.argv[2]=="-o":
			main(sys.argv[1], optimize = True)
		else:
			main(sys.argv[1], optimize = False)
			
		print("took " + str(time.time() - starttime) + " s")

		
	else:	
		print("usage: \npython imagestuff.py filename")		