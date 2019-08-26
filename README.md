# Knotwork 
[![Build Status](https://travis-ci.org/MrBenGriffin/Knot.svg?branch=master)](https://travis-ci.org/MrBenGriffin/Knot?branch=master) 
[![Coverage Status](https://coveralls.io/repos/github/MrBenGriffin/Knot/badge.svg?branch=master)](https://coveralls.io/github/MrBenGriffin/Knot?branch=master)
![Logo](assets/logo.png)

# To Install Fonts onto IOS (iPhone or iPad)
The fonts are wrapped in a configuration profile, which is a way of saying that the fonts are safe to use.
[click here, click on 'Download' and then approve the profile in Settings](assets/KNOTSZoomorphFonts.mobileconfig)

## The Font
You will need the font 'KNOTS Zoo' (any variant) installed with ligatures set for this to show what it is doing.

Although the font is included in this project, if you are not on iOS I recommend you go to https://fontlibrary.org/en/font/knots to get the very latest versions!

You can use the font directly in any text editors that support ligatures or character alternatives.
You can use the box drawing characters (Unicode U+2500) and character alternatives in e.g. Adobe via the glyphs window.
You can also use the built in ligature support, which is pretty straightforward,

Each Celtic character has 4 edges, which are treated here in a clockwise order starting at the top of the character.
If the edge is not connected, then type an O.  If it is connected, there are two primary choices:
"Straight" or "Twisted". A vertical straight knot is IOIO, while a vertical twisted knot is XOXO

![Ligature](assets/liga.png)

Whenever one is using a twist, one can replace it with a Head (H) on one side, and a Beak (B) on the other.
This dramatically increases the combinations of knots... For instance, the original character XXXX now has 80 variations, 
starting with BBBB, BBBH, BBBX, BBHB, BBHH, BBHX .... XXXX

![Permutations](assets/XXXXVariations.png)

So, one can type out knots such as..
```bash
OHXOOXOBOOOXOIXOOOBIOXIOOOHX
XIOOOXOIOXOXXOOXHOHOIOXOBOXO
OBIOOHOHOHOBOOXBBOHOXOXOXOOO
IXOOOOXXOXBOXXXXBOOXXXOOOOIX
OOXOXOXOHOBOXBOOOBOHOHOHIOOB
XOBOXOIOHOHOOXXOOXOXOIOXOOXI
HXOOIOOXBIOOXOOIOXOOOBOXXOOH
```
and it should appear as

![Permutations](assets/result.png)

This also works with lower case - but one glyph will change in lower case.
The "IIII" has an alternative form when typed as "iiii". This is great when working on connections.

![Permutations](assets/IIIIAlt.png)


## application requires:
Python 3  
The GUI is not yet available! (When the GUI is working, you may need tkinter!)

# Launching The application:
```bash
python3 ./text.py -x11 -y11 
```
This takes any of the following parameters. Each one affects the knot work generated.

```bash
  -h, --help            show this help message and exit
  -x {...Infinity}, --width {...Infinity}
                        Width. The number of cells wide. (default: 9)
  -y {...Infinity}, --height {...Infinity}
                        Height. The number of cells high. (default: 9)
  -sb {0.0}, --straights {0.0}
                        Balance between Twists and Straights. 0.0 = twists,
                        1.00 = straights. (default: 0.2)
  -zb {0.0}, --zoo {0.0}
                        Balance between Twists and Zoomorphs. 0.0 = twists,
                        1.00 = zoomorphs. (default: 0.2)
  -s {N,H,V,F,R}, --symmetry {N,H,V,F,R}
                        N: None; H: Horizontal Mirror; V: Vertical Mirror; F:
                        Flip (rotate 180); R: Rotate 90 (when width and height
                        are the same). (default: R)
  -b BORDER, --border BORDER
                        If this is set, then the knot-work will be a border
                        this thick. (default: None)
  -ht, --htile          The knot-work will tile horizontally. (default: False)
  -vt, --vtile          The knot-work will tile vertically. (default: False)
  -c {...Infinity}, --connectivity {...Infinity}
                        Slightly adjusts connections. Larger numbers make
                        longer threads. (default: 12)
  
   -w {M,S,F}, --worker {M,S,F}
                        Miner builds corridors, Spiral makes spirals, Filler
                        is a full network (default: M)

   -r RANDOM, --random RANDOM
                        Random seed. If this is non-zero you should always get
                        the same knot for the parameters. (default:
                        os.urandom)
  -e {HIBOX,E000}, --encoding {HIBOX,E000}
                        Output encoding - either HIBOX ligatures or Unicode
                        PUA 0xE000

```
You can still draw mazes also, by turning the Straights balance right up

![Maze](assets/maze.png)

But this project is mainly for drawing celtic knot-work, with zoomorphics thrown in just for fun!
Parameters 3 and 4 have a very strong effect - have a look at some examples

![Samplers](assets/samples.png)

There are three interesting miners here.
## Mazer
The maze-generating miner. Appears to produce the best mazes so far...

## Spiral
A spiral-generating miner. Generates nice spirals

## Clone
Copies another Miner, either mirroring or rotating.

This codebase was forked from https://github.com/MrBenGriffin/Amaze.

