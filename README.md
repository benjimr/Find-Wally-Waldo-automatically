This program will attepmpt to find Wally in an a Where's Wally image, based on his red and white stripes and shape.

## How to use
First the user must choose whether they want the output to be shown step by step via command line text input
Next they will select the image for the program to use using easygui
If they have chosen to go step by step, they can press any key to move on to the next step.

## Scalability
I have based as many of my parameters as possible off the image, such as deciding
filtering parameters based on image width and height

## Optimization
Due to the nature of the filter() function this program can take a little while to
complete. On an image sized 1024x724 it takes my computer approximately 5 seconds
If it is a large image it will be automatically resized.

## Results
<table style="text-align:center; float:center;">
<tr>
<td style="width:300px; text-align:center;">
<img src="https://i.imgur.com/BZfTWtx.jpg" alt="Original" width="300"/><br>Original
</td>

<td style="width:300px; text-align:center;">
<img src="https://i.imgur.com/sjiAXFm.jpg" alt="Contoured" width="300"/><br>Final Candidates
</td>
</tr>

<tr>
<td style="width:300px; text-align:center;" colspan="2">
<img src="https://i.imgur.com/n9UGxeX.jpg" alt="Processed 1" width="300"/><br>There's Wally!
</td>
</tr>
</table>


## Summary of Functions
process() : controls the process of finding Wally

filter() : decides which pixels from the red and white masks are important

checkSurrounding() : used in filter(), checks the amounts of red and white pixels
in area surrounding a specified pixel

getImage() : gets the user specified image

checkStepByStep() : used to check if user wants step by step output

main(): controls the flow of the program
 
## Steps

The general idea is to keep removing as much information from the image as possible
while not removing Wally or degrading him past the point of recognition.
To do this I carry out the following steps

1.Select red and white colour ranges.

* Using values chosen to most closely match Wally, but not too wide a range as to let in extra pixels.
* This should remove a lot of the obviously unimportant information.


2.Erode the red and white masks using horizontal rectanglular structuring element

* Assuming step 1 worked, each mask should have Wally represented as horizontal stripes. So, here I erode the image using structuring element of this shape to try and remove red and white not of this shape.


3.Filter the red and white pixels in to a new image

* Using the eroded masks we run the filter() function. This function will carry out the following steps
  1. Create a new image of the same size as the input
  2. Loop through the pixels 1 by 1
  3. At each white and red pixel check the surrounding pixels and count how many are red and white
  4. Depending on how many pixels are red and white in the surrounding area we will set the pixel in new image. The conditions here are decided based on analysis of Wally and some trial and error. For example when considering a white pixel we need it to be near a certain amount of red, but not too much red. Also not too much white. With the chosen values it will remove pixels where the level of white and red pixels in the vicinity are not met, or exceeded.


4.Open the filtered mask to remove small bits that made it through
* Inevitably some incorrect pixels will fall in to the same conditional situation as the correct one. To handle this we open the image, this will remove all the small pixels that made it through this far. Leaving Wally as the largest contour.

5.Find the contours on the image

6.Select largest contour, it should be Wally at this point

7.Draw bounding box and text around this contour

##### Some notes:
On top of the above process I also attempted to consider skin colour as well but ruled it out.
The idea was that by including skin in the filtering process, it could allow for Wally to be a much larger contour at the end.
This would, in theory make it more certain that Wally would be the largest contour in the image.
After implementing this it turned out that by including a 3rd colour range, far too many pixels were being considered
meaning not only was Wally coming out as a larger contour, so was everything else. In the end it actually decreased accuracy.
To implement it this way I would likely need to use some form of pattern recognition rather than just colour segmentation.
