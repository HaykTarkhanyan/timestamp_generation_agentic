# Existing draft timestamps may be LLM contamination

When a video's description already contains plausible-looking timestamps that "weren't there yesterday", check for tell-tale LLM artifacts. Found in Δας 21's existing description:
```
Կցանկանա՞ք, որ օգնեմ վիդեոյի համար գրել նաև կարճ նկարագրություն (description) կամ ընտրել համապատասխան YouTube թեգեր։
```
This is a follow-up question from an LLM chat session, accidentally pasted into the YouTube description. Treat the existing timestamps as LLM-drafted (probably unreviewed) rather than human-authored.
