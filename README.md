# Cheat Sheets Generator

This project contains Python scripts that generate PDF cheat sheets for various technologies, including Docker, Git, and Laravel. Each script uses the ReportLab library to create colorful, well-formatted PDF documents with command references.

## Files

- `docker_cheat_sheet_generator.py`: Python script to generate a Docker commands cheat sheet PDF.
- `docker_cheat_sheet.pdf`: Generated Docker cheat sheet PDF.
- `git_cheat_sheet_generator.py`: Python script to generate a Git commands cheat sheet PDF.
- `git_cheat_sheet.pdf`: Generated Git cheat sheet PDF.
- `laravel_cheat_sheet_generator.py`: Python script to generate a Laravel cheat sheet PDF.
- `laravel_cheat_sheet.pdf`: Generated Laravel cheat sheet PDF.

## Requirements

- Python 3.x
- ReportLab library: Install via `pip install reportlab`

## Usage

To generate the cheat sheet PDFs, run the corresponding Python scripts from the command line:

```bash
python docker_cheat_sheet_generator.py
python git_cheat_sheet_generator.py
python laravel_cheat_sheet_generator.py
```

The generated PDF files will be saved in the same directory as the scripts.

## Description

Each generator script creates a professional 2-page A4 PDF with:
- Modern color schemes
- Organized sections for commands
- Clear descriptions and examples
- Formatted tables for easy reference

These cheat sheets are useful for quick reference during development and learning.
