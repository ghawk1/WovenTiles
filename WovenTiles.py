# George Hawk
# WovenTiles.py
# 12 December 2019
#
# This program takes an image and converts it into a black and white weave patterned image

import sys
from PIL import Image
from numpy import transpose

# computes an average rgb value across any number of given pixels
def average(pixels):
    count = len(pixels)*3 #calculates the total number of values to be averages
    av = 0 #initialize total sum
    for pixel in pixels: #for each pixel in the list
        for rgb in pixel: #for each color value in the pixel
            av = av + rgb #add the value to the total sum
    return (av/count)/255 #return the rounded average

# computes the brightness average brightness for each box
def getBrightness(pixels, dim, width, height):
    brightness = [] #initialize all of the brightnesses
    for i in range(0, width, dim): #for each row of pixel/square of pixels
        bright = [] #initialize the brightnesses for this row of pixels/square of pixels
        for j in range(0, height, dim): ##for each column of pixels/square of pixels
            pix = [] #initialize the brightness for this square of pixels
            for k in range(dim): #for each pixel in the square of pixels
                for l in range(dim): 
                    pix.append(pixels[i+k,j+l]) #add the pixels to the list of 
            bright.append(average(pix)) #adds the pixel brightness to the row
        brightness.append(bright) #adds the row to the whole list
    return brightness

# adds our weave pattern to the pixels in our new image
def makeWeave(pixels, newPixels, newWidth, newHeight, thickness, dim):
    side = int((dim-thickness)/2) #calculates the thickness of the side of the weave
    for i in range(0, newWidth, dim): #for each row of pixels
        for j in range(0, newHeight, dim): #for each pixel in the row
            pattern = pixels[int(i/dim)][int(j/dim)] #get the desired pattern for the specific tile
            if pattern == 0: #if the desired pattern is black column over black row
                for k in range(dim): #for each row of the tile
                    for l in range(dim): #for each pixel in the row
                        if k > side-1 and k < side+thickness and (l < side or l > side+thickness-1): #if we are on the edge of the tile                 
                            newPixels[i+k, j+l] = (0, 0, 0) #set the pixel color to black
                        elif l > side-1 and l < thickness+side: #if we are in the middle
                            newPixels[i+k, j+l] = (0, 0, 0) #set the pixel color to black
            elif pattern == 1: #if the desired pattern is black row over white column
                for k in range(dim): #for each row of the tile
                    for l in range(dim): #for each pixel in the row
                        if k > side-1 and k < side+thickness and (l < side or l > side+thickness-1): #if we are on the edge of the tile                    
                            newPixels[i+k, j+l] = (255, 255, 255) #set the pixel color to white
                        elif l > side-1 and l < thickness+side: #if we are in the middle #if we are in the middle
                            newPixels[i+k, j+l] = (0, 0, 0) #set the pixel color to black
            elif pattern == 2: #if the desired pattern is black column over white row
                for k in range(dim): #for each row of the tile
                    for l in range(dim): #for each pixel in the row
                        if (k < side or k > side+thickness-1) and (l > side-1 and l < side+thickness): #if we are on the edge of the tile                    
                            newPixels[i+k, j+l] = (255, 255, 255) #set the pixel color to white
                        elif k > side-1 and k < thickness+side: #if we are in the middle
                            newPixels[i+k, j+l] = (0, 0, 0) #set the pixel color to black
            elif pattern == 3: #if the desired pattern is white column over black row
                for k in range(dim): #for each row of the tile
                    for l in range(dim): #for each pixel in the row
                        if (k < side or k > side+thickness-1) and (l > side-1 and l < side+thickness): #if we are on the edge of the tile                    
                            newPixels[i+k, j+l] = (0, 0, 0) #set the pixel color to black
                        elif k > side-1 and k < thickness+side: #if we are in the middle
                            newPixels[i+k, j+l] = (255, 255, 255) #set the pixel color to white
            elif pattern == 4: #if the desired pattern is white column over black row
                for k in range(dim): #for each row of the tile
                    for l in range(dim): #for each pixel in the row
                        if k > side-1 and k < side+thickness and (l < side or l > side+thickness-1): #if we are on the edge of the tile                        
                            newPixels[i+k, j+l] = (0, 0, 0) #set the pixel color to black
                        elif l > side-1 and l < thickness+side: #if we are in the middle
                            newPixels[i+k, j+l] = (255, 255, 255) #set the pixel color to white
            elif pattern == 5: #if the desired pattern is white row over white column
                for k in range(dim): #for each row of the tile
                    for l in range(dim): #for each pixel in the row
                        if (k < side or k > side+thickness-1) and (l > side-1 and l < side+thickness): #if we are on the edge of the tile                      
                            newPixels[i+k, j+l] = (255, 255, 255) #set the pixel color to white
                        elif k > side-1 and k < thickness+side: #if we are in the middle
                            newPixels[i+k, j+l] = (255, 255, 255) #set the pixel color to white
    return 0

# get the row and column vectors
def getVectors(pixels):
    rows = [] #initialize row vector
    for row in pixels: #for each row in the list of pixels
        rows.append(sum(row)) #add the sum of the values of the row to row vector
    columns = [] #initialize column vector
    for column in transpose(pixels).tolist(): #for each column in the list of pixels
        columns.append(sum(column)) #add the sum of the values of the column to column vector
    return [row, column]

# optimize the color of the ropes
def getRopes(vectors, half, threshold):
    ropes = [] #initialize our rope output
    n = sum(vectors[0])/len(vectors[0]) #calculate the average needed to pick a color
    for vector in vectors: #for both our row and column vector
        x = 0 #initialize counter of how many times in a row a color is picked
        rows = [] #initialize the list of ropes for the given vector
        for row in vector: #for each row in the row vector
            if not rows: #if we haven't added any colors yet
                if row <= n: #if the row value is less than the average
                    rows.append('black') #add a black rope
                    x = x + 1 #increase the rope counter
                else: #if the row value is more than the average
                    rows.append('white') #add a white rope
                    x = x + 1 #increase the rope counter #increase the rope counter
            else: #if we already have ropes in our list
                if row <= n: #if the row value is less than the average
                    if rows[len(rows)-1] == 'black': #if the last rope we added was black
                        if x == threshold: #if we have already reached our threshold
                            x = 1 #reset the counter to 1
                            rows.append('white') #add a white rope
                        else: #if we haven't reached our threshold yet
                            x = x + 1 #increase the rope counter
                            rows.append('black') #add a black rope
                    else: #if the last rope we added was white
                        x = 1 #reset the counter to 1
                        rows.append('black') #add a black rope
                else: #if the value is more than the average
                    if rows[len(rows)-1] == 'white': #if the last rope we added was white
                        if x == threshold: #if we have already reached our threshold
                            x = 1 #reset the counter to 1
                            rows.append('black') #add a black rope
                        else: #if we haven't reached our threshold yet
                            x  = x + 1 #increase the rope counter
                            rows.append('white') #add a white rope
                    else: #if the last rope we added was black
                        x = 1 #reset the counter to 1
                        rows.append('white') #add a white rope
        ropes.append(rows) #add the list of ropes to our output
    return ropes

# optimize the color of the ropes based on two ropes
def getRopes2(vectors):
    ropes = [] #initialize the list to hols the row and column rope colors
    for vector in vectors: #tfor both the row and column vectors
        rows = [] #initialize the list of rope colors
        for i in range(0, len(vector), 2): #for each rows brightness
            if vector[i] > vector[i+1]: #if the brightness of the first row is brighter than the second
                rows.append('white') #add a white rope
                rows.append('black') #add a black rope
            else: #if the brightness of the second row is brighter than the first
                rows.append('black') #add a black rope
                rows.append('white') #add a white rope
        ropes.append(rows) #add the ropes to our list
    return ropes

# decides the pattern for each pixel based only on whether each pixel is brighter or darker than an average with three divisions
def decide1(pixels, quarter, half, trequart): 
    patterns = [] #initialze our pattern output
    for row in pixels: #for each row in the list of pixels
        patrow = [] #initialize the list of patterns for a given row
        for pixel in row: #for each pixel in a given row
            if pixel <= quarter: #if the brightness value is less the the first division
                patrow.append(0) #add a black on black pattern
            elif pixel <= half: #if the brightness value is less than the second division
                patrow.append(1) #add the black over white pattern
            elif pixel <= trequart: #if the brightness value is less than the third division
                patrow.append(3) #add the white over black pattern
            else: #if the brightness value is greater than the third division
                patrow.append(5) #add the white on white pattern
        patterns.append(patrow) #add the row of patterns to our output
    return patterns

# decides the pattern for each pixel based only on whether each pixel is brighter or darker than an average with one division
def decide2(pixels, half):
    patterns = [] #initialze our pattern output
    for row in pixels: #for each row in the list of pixels
        patrow = [] #initialize the list of patterns for a given row
        for pixel in row: #for each pixel in a given row
            if pixel <= half: #if the brightness value is less than the second division
                patrow.append(1) #add the black over white pattern
            else: #if the brightness value is greater than the second division
                patrow.append(3) #add the white over black pattern
        patterns.append(patrow) #add the row of patterns to our output
    return patterns

# decides the pattern for each pixel based on predecided ropes and if a pixel's average brightness
def decide3(pixels, ropes, half):
    patterns = [] #initialze our pattern output
    for j in range(len(ropes[1])): #for each rope in the column ropes
        row = [] #initialize the list of patterns for a given row
        for i in range(len(ropes[0])): #for each rope in the row ropes
            if ropes[0][i] == ropes[1][j] and ropes[0][i] == 'black': #if both ropes are black
                row.append(0) #add black on black pattern
            elif ropes[0][i] == ropes[1][j] and ropes[0][i] == 'white': #if both ropes are white
                row.append(5) #add white on white pattern
            elif ropes[0][i] == 'black' and ropes[1][j] == 'white': #if the row rope is black and the column rope is white
                if pixels[j][i] <= half: #if the brightness of the pixel is less than half
                    row.append(1) #add black row over white column pattern
                else: #if the brightness of the pixel is more than half
                    row.append(3) #add white column over black row
            elif ropes[0][i] == 'white' and ropes[1][j] == 'black': #if the row rope is white and the column rope is black
                if pixels[j][i] <= half: #if the brightness of the pixel is less than half
                    row.append(2) #add black column over white row pattern
                else: #if the brightness of the pixel is more than half
                    row.append(4) #add white row over black column patter
        patterns.append(row) #add the row to our ouptput
    return patterns

# get the median quarter, half, and three quarters
def getDivs(pixels):
    allPix = [] #initialize the list of all pixels
    for row in pixels: #for each row in our list of pixels
        allPix = allPix + row #add the row of pixels to out list of all pixels
    sort = sorted(allPix) #sort all the pixels
    quarter = round(len(sort)/4) #find the quarter index
    return [sort[quarter], sort[quarter*2], sort[quarter*3]]

# gets the cost of the new image in comparison to the original image
def getCost(pixels, patterns, quarter, trequart):
    total = 0 #initialize the total cost
    for i in range(len(pixels)): #for each row in the list of pixels
        for j in range(len(pixels[0])): #for each pixel in the row
            if patterns[i][j] == 0: #if the pattern is black on black
                total = total + (pixels[i][j])**2 #add the squared difference to the total
            elif patterns[i][j] < 3: #if the pattern is black over white
                total = total + (pixels[i][j] - quarter)**2 #add the squared difference to the total
            elif patterns[i][j] < 5: #if the pattern is white over black
                total = total + (pixels[i][j] - trequart)**2 #add the squared difference to the total
            else: #if the pattern is white on white
                total = total + (pixels[i][j]  - 1)**2 #add the squared difference to the total
    return total

    
def main():
    args = sys.argv #set a variable for the agrument values
    fname = args[1] #set a variable for the picture file
    try: #if there is a second argument
        dim = int(args[2]) #set a variable with the given pixel dimension
    except: #if there is no second argument
        dim = 1 #set a variable with a pixel dimension of 1
    try: #if there is a third argument
        newDim = int(args[3]) #set a variable for the dimension of each tile in the new image
    except: #if there is no third argument
        newDim = 32 #set a variable for the dimension of each tile in the new image
    try: #if there is a fourth argument
        thickness = int(args[4]) #set a variable for the thickness of each rope
    except: #if there is no fourth argument
        thickness = 20 #set a variable for the thickness of each rope
    try: #if there is a fifth argument
        decide = int(args[5]) #set a variable for the way the patterns are decided
    except: #if there is no fifth argument
        decide = 1 #set a variable for the way the patterns are decided
    try: #if there is a sixth argument
        threshold = int(args[6]) #set a variable for the threshold of how many ropes of the same color can be added in the third decision
    except: #if there is no sixth argument
        threshold = -1 #set a variable for the threshold of how many ropes of the same color can be added in the third decision
    image = Image.open(fname).convert("RGB") #open the desired image in the RGB format
    width = image.size[0] - image.size[0]%dim  #calculate the width of the image 
    height = image.size[1] - image.size[1]%dim #calculate the height of the image
    if decide == 4: #if we optimize with pattern 4
        width = width - width%(dim*2) #make sure the width is divisible by 2
        height = height - height%(dim*2) #make sure the height is divisible by 2
    pixels = image.load() #load the RGB values of image
    brightness = getBrightness(pixels, dim, width, height) #get the average brightnesses of each pixel
    divs = getDivs(brightness) #gets the median divisions of all the pixel brightnesses
    #divs = [0.25, 0.5, 0.75] #sets the divisions of pixel brightnesses to even divisions of 1
    vectors = getVectors(brightness) #get the row and column vectors
    newWidth = int((width/dim)*newDim) #calculate the width of our ouputed image
    newHeight = int((height/dim)*newDim) #calculate the height of our outputed image
    newPic = Image.new("RGB", (newWidth, newHeight), "grey") #initialize a blank image for output
    newPixels = newPic.load() #get the blank pixel values
    if decide == 1: #if we want to decide the patterns with type 1
        patterns = decide1(brightness,  divs[0], divs[1], divs[2]) #get the pattern for each pixel
    elif decide == 2: #if we want to decide the patterns with type 2
        patterns = decide2(brightness, divs[1]) #get the pattern for each pixel
    elif decide == 3: #if we want to decide the patterns with type 3
        ropes = getRopes(vectors, divs[1], threshold) #get the rope colors
        patterns = decide3(brightness, ropes, divs[1]) #get the pattern for each pixel
    elif decide == 4: #if we want to decide the patterns with type 4
        ropes = getRopes2(vectors) #get the special rope colors
        patterns = decide3(brightness, ropes, divs[1]) #get the pattern for each pixel
    cost = round(getCost(brightness, patterns, divs[0], divs[2])) #calculate the cost of the new image
    makeWeave(patterns, newPixels, newWidth, newHeight, thickness, newDim) #add the tile pattern to our new image
    newPic.show() #display our new image
    #newFile = fname[:3] + '-' + str(dim) + '-' + str(decide) + '-' + str(cost) + '.jpg' #create a file name for the image to be saved to
    #print(newFile) #print the file name
    #newPic.save(newFile, "JPEG") #save the new image
    
if __name__ == "__main__":
    main()
    