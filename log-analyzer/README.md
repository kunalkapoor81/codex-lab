# log-analyzer

A simple Python project to analyze an `app.log` file.

## Features

- Reads `app.log`
- Counts number of `ERROR`, `WARNING`, and `INFO` log entries
- Extracts timestamps from `ERROR` lines
- Generates a `report.txt` summary

## Project Structure

```
log-analyzer/
├── analyzer.py
├── main.py
├── README.md
└── requirements.txt
```

## Requirements

- Python 3.10+

Install dependencies (none required, but file included for consistency):

```bash
pip install -r requirements.txt
```

## How to Run

1. Place your `app.log` file in the `log-analyzer` directory.
2. Run:

```bash
python main.py
```

3. The tool generates `report.txt` in the same directory.

## Expected Log Format

The timestamp extractor expects lines that begin with a timestamp like:

- `YYYY-MM-DD HH:MM:SS ...`
- or `YYYY-MM-DDTHH:MM:SS ...`

Example:

```
2026-03-26 10:11:12 INFO App started
2026-03-26 10:11:13 WARNING Slow response
2026-03-26 10:11:14 ERROR Database unavailable
```
