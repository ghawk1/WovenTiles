# WovenTiles
This program takes an image and converts it into a black and white weave patterned image

To use this program, one must have a desired image file name.
This should be the 1st argument in the command line, after WovenTiles.py

This program also takes five other arguments as described below:

arg0: WovenTiles.py
arg1: File name
arg2: Pixel dimension
arg3: Tile dimension
arg4: Rope thickness
arg5: Pattern number
arg6: Rope threshold

Further description of each argument:
    arg0: WovenTiles.py
        This is the name of the program that you are running...
        
    arg1: File name
        This is the name of the image file that will be turned into a black and white image.
        Pretty much any format of image should be fine; we have not run into problems with
        this yet.
        
    arg2: Pixel dimension
        This argument will be the pixel dimension of the boxes of pixels the program gets an
        average from. For example, if the value of 2 is chosen for this argument, the program
        will average the brightnesses of a 2x2 square of pixels instead of looking at each pixel
        individually. This number can affect whether or not the whole image is returned, or if
        the image will be cropped in order to have each tile work out mathematically.
    
    arg3: Tile dimension
        This argument is an integer number of the desired pixel dimension of each weave tile
        in the outputted image. In other words, it is how many pixels tall and wide each tile
        in the outputted image will be.
        
    arg4: Rope thickness
        This argument is an integer number of the desired rope thickness for each rope in the
        outputted image. This number should be less than the tile dimension as the rope must
        fit into a tile.
        
    arg5: Pattern number
        This argument will either be 1, 2, or 3 deppending on which type of weave pattern is
        desired. The weave patterns are as follows:
        Pattern 1:
            This pattern represents the original image most closely, but does not produce a very
            realistic weave pattern. Deppending on if the brightness of a pixel is in the
            bottom quartile, second lowest quartile, second highest quartile, or highest quartile,
            the program will assign a tile pattern that corresponds the brightness level of this.
            As this pattern has four different options for color, and full freedom of where to
            use these colors, it produces a realistic image.
        Pattern 2:
            This patttern represents the image relatively well, and has a weave pattern that would
            be able to be replicated in the real world. All vertical ropes are white, and all
            horizontal ropes are black. Then based on if the brightness of the specific pixel
            is above or below half, it will assign either white on top of black, or black on top
            of white respectively.
        Pattern 3:
            In this pattern, we tried to optimize the colors of the ropes that were chosen. Once
            the ropes are chosen, we once again choose white on black or black on white based
            on the brightness of that specific pixel. It usually ends up looking pretty patchy,
            because it turns out that most images have large patches of similarly bright pixels. 
        Pattern 4:
            In this pattern, we optimized between every two consecutive ropes. By this we mean
            given two consecutive rows, if the first row had a higher average brightness than
            the second row, we would add a white rope then a black rope. If the second rope had
            a higher average brightness then we would add a black rope and then a white rope. After
            this, we would look at the next two ropes and repeat. Then the individual pixels are
            decided by the same way as pattern 3 and 4.
    
    arg6: Rope threshold
        This argument is an integer number of the desired number of ropes of the same color the
        user wants to allow the program to have in a row. For example, if the number 3 is chosen
        for this argument, then the program will only allow three black or three white ropes to be
        added in a row before switching to the other color. This parameter allows for creating a
        very realistic weave pattern because it allows for the ability of the weave to stick
        together, given a small enough value chosen. In order to create an alternating stirng
        pattern, one can choose a threshold of 1. This parameter should only be used along with
        Pattern 3.
        
An example of a possible instance of this program being run would be the following:
    # python WovenTiles.py cat.jpg 1 16 8 3 2
This would create a woven black and white image of the image found in the file 'cat.jpg' with each
individual pixel's brightness being used, with weave tiles of 16x316 pixels, a rope thickness of
8 pixels, with Pattern 3, and a threshold of two ropes of the same color allowed.
    
While the file name argument is required, if no other parameters are entered, the program will
run as if the following parameters were chosen:
    # python WovenTiles.py 'filename' 1 32 20 1 -1
    

There are currently no known bugs in this program.
Thank you!


