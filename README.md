# LP-PolyBot
Project of Programming Languages subject in Barcelona School of Informatics, FIB - UPC. Fall 2020-2021.

This project consists of an implementation of a Telegram Bot that replies textually and graphically to operations related to convex polygons.

## Set-up
To start using the bot you will need to install the required Python libraries:
```bash
pip3 install -r requirements.txt
```
You will also need a valid Telegram bot token, which has to be stored in a plain text file called `token.txt` in the same directory as the `bot.py` file.

To run the bot, simply execute:

```bash
cd bot
python3 bot.py
```

and you can start chatting!

## Part 1: Class for convex polygons
In this first part I designed and implemented a Python class named `ConvexPolygon` that is in the `polygons.py` file. I also implemented `Point` class to work with. The coordinates of a point are rounded to three decimal places to avoid tolerance problems.

The main ideas of the implementation are:
* A polygon is stored as the list of points ordered clockwise taking the leftest one as reference (lowest one in case of a tie)
* The Graham Scan algorithm is used to compute the convex hull of a set of points.
All functions are documented in the code.

There are some test cases to check the correct functionality of the functions.

For convenience, we will consider some particular cases of polygons (not always recognized as polygons by mathematicians!):

* Empty polygon: a polygon with zero vertices.
* Monogon: a polygon with one vertex (a point).
* Digon: a polygon with two vertices (a segment).

The remaining polygons are more conventional: triangles, quadrilaterals, pentagons, hexagons, etc.

## Part 2: A programming language to work with convex polygons

This part consisted of creating a small programming language to work with convex polygons. `ANTLR` is used to build this programming language.
The grammar accepts the following commmands:

### Comments
Two bars (`//`) introduce a comment up to the end of the line.

### Polygon identifiers
Identifiers are as usual:
`p`, `Q`, `p1`, `p2`, `pol_gr`, ...

### Points and polygons
Points in the commands are given by two pairs of real numbers, in standard notation, to denote the X and Y coordinates. For instance, `0 0` or `3.14 -5.5`.

### Colors
Colors in the commands are given, between curly braces, by three real numbers in [0,1], in standard notation, to denote the RGB color. For instance, `{0 0 0}` denotes black, `{1 0 0}` denotes red, and `{1 0.64 0}` denotes orange.

### The assigment command
The assignment command (`:=`) associates an variable with a convex polygon.
If the polygon identifier is new, it will create it. If it already existed, it will overwrite the previous polygon. New polygons are black by default. It is an error to use a variable not yet defined.

### The `print` command
The `print` command prints a given polygon or a text.

- For polygons, the output contains the vertices in the convex hull of the polygon, in clockwise order, starting from the vertex will lower X (and the vertex with lower Y in case of ties).

- For texts, the text is given as a string of (simple) characters between quotes.

### The `area` command
The `area` command prints the area of the given polygon.

### The `perimeter` command
The `perimeter` command prints the perimeter of the given polygon.

### The `vertices` command
The `vertices` command prints the number of vertices of the convex hull of the given polygon.

### The `centroid` command
The `centroid` command prints the centroid of the given polygon.

### The `color` command
The `color` command associates a color to the given polygon variable.

### The `inside` command
Given two polygons, the `inside` command prints `yes` or `no` to tell whether the first is inside the second or not.

### The `equal` command
Given two polygons, the `equal` command prints `yes` or `no` to tell whether the two polygons are the same or not.

### The `draw` command
The `draw` command draws a list of polygons in a PNG file, each one with its associated color. The image is of 400x400 pixels, with white background and the coordinates of the vertices are scaled to fit in the 398x398 central part of the image, while preserving the original aspect ratio.

### Operators
`*` represents the intersection of two polygons.

`+` represents the convex union of two polygons.

`#` is the unary operator that returns the bounding box of a polygon (it computes a new polygon with the four vertices corresponding to the bounding box of the given polygon).

`!n` is an operator that (applied to a natural number `n`) returns a convex polygon made with `n` points drawn at random in the unit square.

The operator precedence is the following: `()`,`#`,`*`,`+`,`!`.
### Errors
For the sake of simplicity, we assume that all the inputs are valid.

There are some example scripts: `script.txt`,`script2.txt`,`script3.txt` as an example and can be tested with the `test.py` file.

## Part 3: A bot to interact with convex polygons
This last part is an implementation of a Telegram Bot to work with convex polygons reading commands in the programming language and printing (or drawing) the results.
The implementation of this part is in the `bot\bot.py` file.
The bot accepts the following commands:
* `/start` - Welcome message
* `/author` - Information about the author
* `/help` - Shows list of commands
* `/lst` - Display list of defined polygons
* `/clean` - Delete all defined polygons
* Any possible command line from the programming language defined above (starting without slash `/`)

## Author
- [Francesc Martí Escofet](https://github.com/fmartiescofet)