import argparse
import csv
import random
from pathlib import Path

from llm import chat, chat_json, chunks


def flashcards(notes, n):
    cards = []
    for part in chunks(notes):
        cards += chat_json(
            f"Create {n} flashcards from these notes as a JSON list of "
            f'{{"q": "...", "a": "..."}} objects.\n\nNOTES:\n{part}'
        )
    return cards


def summarize(notes):
    partials = [chat(f"Summarize these notes as bullet points:\n\n{p}") for p in chunks(notes)]
    if len(partials) == 1:
        return partials[0]
    return chat("Merge these bullet-point summaries into one, removing duplicates:\n\n" + "\n\n".join(partials))


def quiz(cards):
    random.shuffle(cards)
    score = 0
    for i, c in enumerate(cards, 1):
        ans = input(f"\n[{i}/{len(cards)}] {c['q']}\n> ")
        verdict = chat(
            f"Question: {c['q']}\nReference answer: {c['a']}\nStudent answer: {ans}\n"
            "Is the student answer correct? Reply 'CORRECT' or 'WRONG: <short explanation>'."
        , temperature=0)
        ok = verdict.strip().upper().startswith("CORRECT")
        score += ok
        print("✅" if ok else f"❌ {verdict}  (answer: {c['a']})")
    print(f"\nscore: {score}/{len(cards)}")


def main():
    p = argparse.ArgumentParser(description="Turn lecture notes into study material")
    p.add_argument("command", choices=["cards", "summary", "quiz"])
    p.add_argument("notes", type=Path)
    p.add_argument("-n", type=int, default=10, help="flashcards per chunk")
    p.add_argument("--anki", type=Path, help="export flashcards as Anki CSV")
    args = p.parse_args()
    notes = args.notes.read_text()

    if args.command == "summary":
        print(summarize(notes))
        return
    cards = flashcards(notes, args.n)
    if args.command == "quiz":
        quiz(cards)
    elif args.anki:
        with args.anki.open("w", newline="") as fh:
            csv.writer(fh).writerows((c["q"], c["a"]) for c in cards)
        print(f"wrote {len(cards)} cards to {args.anki}")
    else:
        for c in cards:
            print(f"Q: {c['q']}\nA: {c['a']}\n")


if __name__ == "__main__":
    main()
