# Customized Terminal

- Features: copy as HTML, copy as LaTeX
- Platform: Ubuntu

## Installation/Useage

- Make sure the following packages are installed in the system. Otherwise, install with `apt`:
    - libgtk2.0
    - libgtk-3-0
    - libgirepository1.0-dev
    - libcairo2-dev
    - python-vte

- Install dependent Python packages with `pip3 install -r requirements.txt`
- Run `main.py` with Python3

## Rendering LaTeX

Make sure to use `xcolor` and `listings` package, as well as include `template.tex` in your LaTeX source file in order to compile correctly. 

## Potential Problems
- The [colour](https://pypi.org/project/colour/) package may collide with [colour-science](https://pypi.org/project/colour-science/) package. 