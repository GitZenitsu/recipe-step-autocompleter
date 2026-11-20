# Recipe Step Autocompleter

[![Built with askThili](https://ask.thili.ai/api/v1/public/projects/jq9bcg5gtc/badge.svg)](https://ask.thili.ai/b/jq9bcg5gtc)

This Recipe Step Autocompleter is a command-line tool designed for home cooks. It helps complete incomplete recipe instructions, ensuring smooth cooking and no missed steps. It uses a word-level n-gram model to suggest the next word and to finish the whole step.

## What you are building

**Goal.** A command-line tool that helps home cooks autocomplete incomplete recipe instructions, ensuring they don't miss steps and can follow recipes smoothly.

**Done when.** The tool takes a partial recipe instruction from the user on the command line and gives a logical next word or phrase to complete it, based on a trained n-gram model.

## Milestones

- [x] **1. Compile a corpus of cooking recipe instructions.** 44 steps from eight small recipes, written for this project (see Data below).
- [x] **2. Implement n-gram counting and maximum-likelihood probabilities with smoothing.** Trigram counts with add-k smoothing and backoff to shorter contexts.
- [x] **3. Create a function to generate recipe step continuations.** `suggest_next` ranks next words and `milestone_3` finishes a step word by word.
- [x] **4. Build a CLI for users to input partial steps and get suggestions.** `python -m app.cli suggest ...` and an `interactive` mode.

## How it works

The model counts which word follows each pair of words in the corpus (a trigram model). A probability is the count divided by the total for that context, with a small amount `k` added to every word so that unseen words never get probability zero (`k=1` is Laplace smoothing, `k=0` is plain maximum likelihood, and the default is `k=0.1`). If the last two words were never seen together, the model backs off to just the last word, then to overall word frequency.

## Run it

You need Python 3.12 and git.

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m app.cli hello
python -m app.cli suggest heat oil in a
python -m app.cli interactive
pytest
```

On Windows, activate the environment with `.venv\Scripts\activate` instead.

## Results

Real output from the tool:

```
$ python -m app.cli suggest heat oil in a
Partial step: "heat oil in a"
Likely next words:
  pan  (20%)
  bowl  (15%)
  large  (10%)
Suggested step: "heat oil in a pan over medium heat"
```

```
$ python -m app.cli suggest bring a large
Likely next words:
  pot  (16%)
  bowl  (8%)
  (end of step)  (1%)
Suggested step: "bring a large pot of salted water to a boil"
```

```
$ python -m app.cli suggest add salt
Likely next words:
  and  (34%)
  ...
Suggested step: "add salt and pepper to taste"
```

The tests check that probabilities add up to 1, that maximum likelihood gives exactly 1.0 for "add salt" followed by "and", that smoothing gives unseen words a small non-zero probability, and that unseen contexts still get suggestions.

## Data

The corpus is 44 short recipe steps (about 120 distinct words) that I wrote myself for pasta, omelette, fried rice, pancakes, tomato soup, salad and tea. No outside data or downloads are used.

## Limits

- The corpus is tiny, so the model only knows these eight recipes. A word it has never seen gets the same weak guess as any other.
- The model sees only the last two words, so it forgets the start of a step. Longer continuations can drift: "serve hot" is finished as "serve hot in a pan over medium heat", which is wrong.
- Greedy completion always takes the single most likely word, so the same input always gives the same output.
- Probabilities are small because they are spread over the whole vocabulary, so look at the ranking more than the percentage.
- There is no held-out accuracy measure, since the corpus is too small to split.

## Files

- `app/core.py`: corpus, n-gram model, smoothing, suggestions and continuation
- `app/cli.py`: command-line tool
- `tests/test_core.py`: tests for the four milestones
- `tests/test_smoke.py`: starter plumbing checks
- `app/llm.py`, `app/storage.py`: starter helpers, unused by this project

## Settings and secrets

This project needs no keys. If you add any, keep them in `.env`, which is ignored by git. **Never commit `.env` or paste a key into code.**

## Stretch ideas

- Let the user pick from the top N suggestions.
- Add new recipe steps to the corpus and retrain on the fly.
- Suggest full phrases using sampling instead of always taking the top word.
