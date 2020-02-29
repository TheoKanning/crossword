# Crossword Creator
GUI for making crossword puzzles. Built with python and pyqt5.

[image]: ./image.png
![sample][image]

## Features
* Save and load in-progress crosswords
* UI for adding letters and blocks
* Automatic word suggestions (dictionary not included)

## Installing and Running

Dependencies are managed with [Pipenv](https://github.com/pypa/pipenv)

From the root directory:

`pipenv install`

`pipenv shell`

`python crossword/app.py`

To run tests:

`python -m unittest discover tests/`

## Dictionary
The dictionary I used is from [xwordinfo.com](https://www.xwordinfo.com/WordList/)

Since it's not free, I can't include it in the repo.

## Saving and Loading
Crosswords are stored as txt files in the `saved/` folder.

I included `example.txt` to show the formatting.

## Future Improvements
* Allow vertical suggestions and auto-focusing
* Save and load multiple files
* Calculate puzzle stats
