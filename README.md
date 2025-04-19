# SWF Checker

This was written by @idkwhereisthisname, it is a tool that can detect whether a SWF file is compatible with Wii injects using FriishProduce.

It checks for:
* ActionScript verson
* the Flash version
* Size issues

### Usage

If a SWF was made with ActionScript 2 (or 1) and Flash version 8 (or older), it will say it can work with the Wii. If the game's stage resolution (in pixels) is larger than 700x500 pixels, it will warn about possible overlapping/clipping on the Wii.
