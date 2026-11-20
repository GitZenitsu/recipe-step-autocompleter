# Recipe Step Autocompleter

[![Built with askThili](https://ask.thili.ai/api/v1/public/projects/jq9bcg5gtc/badge.svg)](https://ask.thili.ai/b/jq9bcg5gtc)

This Recipe Step Autocompleter is a command-line tool designed for home cooks. It helps complete incomplete recipe instructions, ensuring smooth cooking and no missed steps. The tool leverages next-word prediction and text generation capabilities to suggest logical continuations for recipe instructions.

## What you are building

**Goal.** You will build a command-line interface (CLI) tool that helps home cooks autocomplete incomplete recipe instructions, ensuring they don't miss steps and can follow recipes smoothly.

**Done when.** The tool successfully takes a partial recipe instruction from the user via a command-line interface and provides a logical next word or phrase to complete it, based on a trained n-gram model.

## Milestones

Tick these off as you go, and commit after each one.

- [ ] **1. Compile a corpus of cooking recipe instructions.**  
      Hint: Gather diverse cooking recipe texts to form your training data.
- [ ] **2. Implement n-gram counting and maximum-likelihood probabilities with smoothing.**  
      Hint: Use dictionaries or counters to store n-gram counts and calculate probabilities, applying Laplace smoothing.
- [ ] **3. Create a function to generate recipe step continuations.**  
      Hint: Create a function that takes a sequence of words and predicts the most likely next word.
- [ ] **4. Build a CLI for users to input partial steps and get suggestions.**  
      Hint: Design a simple command-line interface to accept user input and display predictions.

## Run it

You need Python 3.12 and git.

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # then choose a model; see the comments inside
python -m app.cli hello
pytest
```

Your work goes in `app/core.py` (one stub per milestone) and `tests/test_core.py`. The first tests pass already; they
check the plumbing.

## Settings and secrets

Model settings live in `.env`, which is ignored by git. **Never commit `.env` or paste a key into code.** If a key ever
reaches GitHub, treat it as leaked and make a new one.

## Stretch ideas

- Allow the user to select from the top N suggested next words.
- Implement a feature to add new recipe instructions to the corpus, retraining the model on the fly.
- Improve text generation to suggest full phrases or sentences instead of just single words.
