# Springer Free Ebooks - April 2020
Springer released around 400+ key textbooks for free during the COVID-19 crisis. Links will be available at least until the end of July according to their [press release](https://group.springernature.com/gp/group/media/press-releases/freely-accessible-textbook-initiative-for-educators-and-students/17858180?utm_medium=social&utm_content=organic&utm_source=facebook&utm_campaign=SpringerNature_&sf232256230=1).

This repository uses the information gathered in a spreadsheet regarding these books and downloads them. I've seen other scripts do the same but they don't do async downloads so they usually take hours to download the +10GB of books. This async implementation using [aiohttp](https://github.com/aio-libs/aiohttp) should take less than an hour in most cases.

## What the script does
- Loads the file `books.csv` contained in this repo. Original spreadsheet can be viewed [here](https://docs.google.com/spreadsheets/d/1HzdumNltTj2SHmCv3SRdoub8SvpIEn75fa4Q23x0keU/edit).
- Creates a folder structure which will separate books by category.
- Will download pdf version and epub version when available.


## Usage
```
pip install -r requirements.txt
python download.py
```

## Notes
- If the programs exits due to `Timeout` error, launching it again should solve the issue.
- Books that are already downloaded are ignored the next time the script is launched.
- Tested this from Colombia and download took around 40 minutes.

