"""Command-line entry point: `python -m app.cli --help`."""
import argparse

from app import core


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="recipe-step-autocompleter", description="Home cooks use this CLI tool to autocomplete incomplete recipe instructions, ensuring they don't miss steps and can follow recipes smoothly.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("hello", help="check that everything is wired up")
    suggest = sub.add_parser("suggest", help="suggest the next words and a full step for a partial step")
    suggest.add_argument("text", nargs="*", help="the partial step, e.g. heat oil in a")
    suggest.add_argument("--top", type=int, default=3, help="how many next words to show")
    sub.add_parser("interactive", help="type partial steps one after another")
    args = parser.parse_args(argv)
    if args.command == "hello":
        print("Recipe Step Autocompleter is ready. Open README.md for your milestones.")
    elif args.command == "suggest":
        print(core.milestone_4(" ".join(args.text), top=args.top))
    elif args.command == "interactive":
        print("Type a partial recipe step, or 'quit' to exit.")
        while True:
            text = input("\nPartial step: ").strip()
            if text.lower() == "quit":
                break
            print(core.milestone_4(text))


if __name__ == "__main__":
    main()
