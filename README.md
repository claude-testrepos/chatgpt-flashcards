# GPT Study Assistant

Turns lecture notes into flashcards, summaries and an interactive quiz graded by GPT. Made during midterms when ChatGPT came out.

## Setup

```
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
```

## Usage

```
python study.py cards examples/os-lecture-07.md --anki cards.csv
python study.py summary notes.md
python study.py quiz notes.md -n 5
```
