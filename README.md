# Album-SSE

## Description
A fade-in fade-out album using SSE and other mothods.
# Requirement
- python 3
- pyqt 5
- Pillow
- matplotlib
# Usage
- Create a folder and store your images. 
  - Remind that all the images should have the same pixel size!!
  - For example: all images has size of `(640, 480)`.
- commond: python GUI.py
# Note
If you run this code on Windows, there is somewhere you need to change in `SSE.c` or `sse.c`, and after you modified the `.c` file, you need to compile the '.c' file to `libsse.so` with `gcc` commond. Because it been half a year ago, I have forgot where should be changed, so good luck to you.
