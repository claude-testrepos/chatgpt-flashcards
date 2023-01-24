import os
import sys

import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

notes = open(sys.argv[1]).read()
prompt = f"Make 10 flashcards (Q: ... A: ...) from these lecture notes:\n\n{notes}\n\nFlashcards:"

resp = openai.Completion.create(model="text-davinci-003", prompt=prompt, max_tokens=800, temperature=0.3)
print(resp["choices"][0]["text"].strip())
