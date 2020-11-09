# Crossword Creator
GUI for making crossword puzzles. Built with python and pyqt5.

![sample](/assets/image.png)

## Features
* Save and load in-progress crosswords
* UI for adding letters and blocks
* Edit in across or down mode (press shift to switch)
* Word suggestions (dictionary not included)
* Automatic puzzle generator

## Installing and Running

Dependencies are managed with [Pipenv](https://github.com/pypa/pipenv)

From the root directory:

`pipenv install`

`pipenv shell`

`python -m crossword`

To run tests:

`python -m unittest discover tests/`

To run generator:
`python generate.py <path to crossword file`

## File Format
Saved crosswords are stored in txt files.
* Letters are capitalized
* Spaces are empty squares
* Blocks are periods

```
..CAP
WALDO
EQUAL
DUMMY
SAP..
```

## Dictionary
The dictionary I used is from [xwordinfo.com](https://www.xwordinfo.com/WordList/)

Since it's not free, I can't include it in the repo.

## Saving and Loading
Crosswords are stored as txt files in the `saved/` folder.

I included `example.txt` to show the formatting.

## Future Improvements
* Save and load multiple files
* Calculate puzzle stats
