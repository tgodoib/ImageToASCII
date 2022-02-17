# ImageToASCII
Convert an image to a text formed from ASCII characters

## Usage
To use in development mode, type:
```
$ source venv/bin/activate
$ export FLASK_APP=App
$ flask run
```

## How it works
**First we choose which characters the text should contain** 

In this case, the characters are from 33 to 127 and 192 to 256 from the ASCII table

**Then, for each character in the list, we render it in an image**

Each image is 10px by 10px. That's because 
a) we want this process to be quick 
b) each letter in the final text is going to be small, 
so we just might as well render it being that tiny.

**For each image, we then calculate its "density"**

Density in this case meaning how bright the image is.
It works by calculating the average brightness of all its 100 pixels.
All values are storage in a binary tree, so they can be easily and quickly searched.

**Then we separate the chosen image in regions and calculate their brightness**

This calculation is done the same way we did for the rendered characters.

**Finally, we print out the best character for each region**

Once we have the regions brightness, we just have to search the characters
with the closest brightness in the binary tree and print it out!

##Some considerations
- When printing out the characters, its important they're displayed in 
a monospace font
- Preferably, the line height should match the characters width so the aspect ratio is preserved