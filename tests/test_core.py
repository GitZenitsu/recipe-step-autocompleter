"""Tests for the four milestones in app/core.py and the command-line tool."""
from app import core
from app.cli import main


def test_milestone_1():
    corpus = core.milestone_1()
    assert len(corpus) >= 30
    assert all(isinstance(step, str) and step.strip() for step in corpus)
    assert core.tokenize("Heat OIL, in a pan!") == ["heat", "oil", "in", "a", "pan"]


def test_milestone_2():
    model = core.milestone_2(k=0.1)
    assert model["n"] == 3 and "pan" in model["vocab"]
    # every smoothed distribution adds up to 1
    for k in (0.1, 1):
        total = sum(core.probability(model, ["add", "salt"], w, k=k) for w in model["vocab"])
        assert abs(total - 1.0) < 1e-9
    # maximum likelihood: "add salt" is always followed by "and" in the corpus
    assert core.probability(model, ["add", "salt"], "and", k=0) == 1.0
    assert core.probability(model, ["add", "salt"], "pan", k=0) == 0.0
    # smoothing gives unseen words a small non-zero probability
    assert core.probability(model, ["add", "salt"], "pan") > 0


def test_milestone_3():
    model = core.milestone_2()
    top = core.suggest_next(model, "add salt", top=3)
    assert top[0][0] == "and"
    assert [p for _, p in top] == sorted((p for _, p in top), reverse=True)
    finished = core.milestone_3(model, "heat oil in a")
    assert finished.startswith("heat oil in a") and len(finished.split()) > 4
    # a context the model has never seen still gets suggestions (backoff)
    assert len(core.suggest_next(model, "zzz qqq", top=3)) == 3


def test_milestone_4(capsys):
    text = core.milestone_4("bring a large")
    assert "Likely next words:" in text and "Suggested step:" in text
    assert "pot" in text
    main(["suggest", "add", "salt"])
    assert "and" in capsys.readouterr().out
