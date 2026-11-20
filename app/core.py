"""Recipe Step Autocompleter: core logic.

A word-level n-gram model (trigram by default) trained on a small corpus of recipe steps.
Counts are turned into probabilities with add-k smoothing (k=1 is Laplace, k=0 is plain
maximum likelihood), and unseen contexts back off to shorter ones.
Only the Python standard library is used.
"""
import re
from collections import Counter, defaultdict
from functools import lru_cache

START, END = "<s>", "</s>"


# --- Milestone 1: Compile a corpus of cooking recipe instructions.
def milestone_1():
    """Return a list of recipe steps (one string each), written for this project."""
    return [
        # pasta with tomato sauce
        "bring a large pot of salted water to a boil",
        "add the pasta and cook for ten minutes until tender",
        "drain the pasta and set it aside",
        "heat oil in a pan over medium heat",
        "add chopped garlic and cook for one minute",
        "add the tomatoes and simmer for fifteen minutes",
        "stir in the pasta and mix well",
        "add salt and pepper to taste",
        "serve hot with grated cheese on top",
        # omelette
        "crack the eggs into a bowl and whisk well",
        "add salt and pepper to taste",
        "heat butter in a pan over medium heat",
        "pour the eggs into the pan and cook for two minutes",
        "fold the omelette in half and cook for one more minute",
        "serve hot on a warm plate",
        # fried rice
        "rinse the rice and cook it in boiling water for fifteen minutes",
        "drain the rice and let it cool",
        "heat oil in a pan over high heat",
        "add chopped onion and cook for two minutes",
        "add the rice and stir well",
        "add soy sauce and mix well",
        "add salt and pepper to taste",
        "serve hot in a bowl",
        # pancakes
        "mix the flour sugar and baking powder in a bowl",
        "add the milk and eggs and whisk until smooth",
        "heat butter in a pan over medium heat",
        "pour a ladle of batter into the pan and cook for two minutes",
        "flip the pancake and cook for one more minute",
        "serve warm with honey on top",
        # tomato soup
        "heat oil in a large pot over medium heat",
        "add chopped onion and cook for five minutes until soft",
        "add the tomatoes and water and bring to a boil",
        "simmer for twenty minutes and stir well",
        "blend the soup until smooth",
        "add salt and pepper to taste",
        "serve hot in a bowl with bread",
        # salad
        "wash and chop the vegetables",
        "mix the vegetables in a large bowl",
        "add olive oil and lemon juice and mix well",
        "add salt and pepper to taste",
        "serve cold on a plate",
        # tea
        "bring the water to a boil in a pot",
        "add the tea leaves and simmer for three minutes",
        "add milk and sugar and stir well",
        "strain the tea into a cup and serve hot",
    ]


def tokenize(text):
    """Lowercase words only; punctuation is dropped."""
    return re.findall(r"[a-z0-9']+", text.lower())


# --- Milestone 2: Implement n-gram counting and maximum-likelihood probabilities with smoothing.
def milestone_2(corpus=None, n=3, k=0.1):
    """Count n-grams of every order up to `n` and return a model dict.

    counts[context][word] = how many times `word` followed `context` (a tuple of words,
    from the empty tuple up to n-1 words). `k` is the add-k smoothing amount.
    """
    corpus = corpus if corpus is not None else milestone_1()
    counts = defaultdict(Counter)
    vocab = set()
    for step in corpus:
        tokens = [START] * (n - 1) + tokenize(step) + [END]
        for i in range(n - 1, len(tokens)):
            word = tokens[i]
            vocab.add(word)
            for size in range(n):                       # context lengths 0 .. n-1
                counts[tuple(tokens[i - size:i])][word] += 1
    return {"n": n, "k": k, "counts": counts, "vocab": sorted(vocab)}


def _context_for(model, words):
    """Longest context (up to n-1 words) that was seen in training, backing off if needed."""
    history = [START] * (model["n"] - 1) + list(words)
    for size in range(model["n"] - 1, -1, -1):
        context = tuple(history[len(history) - size:]) if size else ()
        if context in model["counts"]:
            return context
    return ()


def probability(model, words, word, k=None):
    """P(word | the last words), with add-k smoothing (k=0 gives maximum likelihood)."""
    k = model["k"] if k is None else k
    context = _context_for(model, words)
    counter = model["counts"][context]
    total = sum(counter.values())
    return (counter[word] + k) / (total + k * len(model["vocab"]))


# --- Milestone 3: Create a function to generate recipe step continuations.
def suggest_next(model, text, top=3):
    """Most likely next words after `text`, as a list of (word, probability)."""
    words = tokenize(text)
    scored = [(w, probability(model, words, w)) for w in model["vocab"]]
    scored.sort(key=lambda pair: (-pair[1], pair[0]))
    return scored[:top]


def milestone_3(model=None, text="heat oil in a", max_words=10):
    """Continue `text` one most-likely word at a time until the step ends."""
    model = model if model is not None else _default_model()
    words = tokenize(text)
    for _ in range(max_words):
        word = suggest_next(model, " ".join(words), top=1)[0][0]
        if word == END:
            break
        words.append(word)
    return " ".join(words)


# --- Milestone 4: Build a CLI for users to input partial steps and get suggestions.
def milestone_4(text, model=None, top=3):
    """The text the command-line tool prints for a partial step."""
    model = model if model is not None else _default_model()
    lines = [f'Partial step: "{text}"', "Likely next words:"]
    for word, prob in suggest_next(model, text, top):
        shown = "(end of step)" if word == END else word
        lines.append(f"  {shown}  ({prob:.0%})")
    lines.append(f'Suggested step: "{milestone_3(model, text)}"')
    return "\n".join(lines)


@lru_cache(maxsize=1)
def _default_model():
    return milestone_2()
