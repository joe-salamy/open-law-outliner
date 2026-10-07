# Open Law Outliner

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python script that compresses verbose law school notes into compact outline form using find-and-replace abbreviations.

## What it does

Law school exams reward speed. This tool takes dense prose notes and shrinks them — replacing full words with standard legal shorthand, dropping articles, and contracting common phrases. The result is a scannable outline you can actually read under time pressure.

**Examples of what gets shortened:**

- `Plaintiff` → `P`, `Defendant` → `D`
- `jurisdiction` → `jdx`, `Summary judgment` → `SJ`
- `the`, `a`, `an`, `is`, `are`, `was` → _(deleted)_
- `and` → `+`, `with` → `w/`, `because` → `bc`
- `First Amendment` → `1A`, `Fourteenth Amendment` → `14A`
- All 50 US state names → standard two-letter codes

## Requirements

- Python 3 (no external dependencies)

## Getting your notes into the tool

This script reads a plain text file. If your notes live in Google Docs, the easiest way to get them into a text file is to copy them as **Markdown**.

**What is Markdown?** Markdown is a lightweight way to write formatted text using plain characters — for example, `**bold**` renders as **bold** and `# Heading` becomes a heading. Many apps support it, and it copies cleanly into plain text files without carrying over invisible formatting garbage.

**Enabling Markdown in Google Docs:**

1. In your Google Doc, click **Tools → Preferences → General**
2. Check the box for **Enable Markdown**
3. Click **OK**

Now when you want to copy your notes:

1. Highlight the text you want
2. Right-click → **Copy as Markdown**
3. Open (or create) your `input_text.txt` file and right-click → **Paste**

## Navigating to the folder in your terminal

Before running the script, you need to open a terminal and navigate to the folder where you saved this project.

**On Windows:**

1. Open **File Explorer** and go to the folder containing `main.py`
2. Click the address bar at the top (it will highlight the full path, e.g. `C:\Users\YourName\Documents\open-law-outliner`)
3. Copy that path
4. Open **Terminal** (search for it in the Start menu) or **PowerShell**
5. Type the following and press Enter, replacing the path with your own:

```
cd C:\Users\YourName\Documents\open-law-outliner
```

**On Mac:**

1. Open **Finder** and go to the folder containing `main.py`
2. Right-click the folder → **Get Info**, then copy the path shown under **Where**
3. Open **Terminal** (in Applications → Utilities)
4. Type the following and press Enter:

```
cd /Users/YourName/Documents/open-law-outliner
```

Once you're in the right folder, you're ready to run the script.

## Usage

**Default (reads `input_text.txt`, writes `output_text.txt`):**

```
python main.py
```

**Custom file paths:**

```
python main.py --input notes.txt --output outline.txt
```

**Options:**

```
  --input   Input file path  (default: input_text.txt)
  --output  Output file path (default: output_text.txt)
```

## Adding custom abbreviations

All replacements live in the tables near the top of `main.py`. Matching is case-insensitive, whole-phrase, and longest-match-first, so one entry covers both cases. Add yours to the relevant list:

```python
_FIXED = [
    ("promissory estoppel", "PE"),  # used verbatim
]
_CASED = [
    ("tortfeasor", "tf"),  # first letter follows the match: Tortfeasor -> Tf
]
_DELETIONS = [
    "hereinafter",  # removed entirely
]
```

Amendments, numbers, ordinals, and `not`/`have` contractions are generated from small loops — extend the word lists, not the tables. No other changes needed.
