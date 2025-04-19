from pathlib import Path
import argparse
import os
import requests

from blog_post_extractor.extract_blog_post import extract_blog_post


def cmd_extract(args):
    # Ensure output has .html extension
    output_path = args.output
    if not output_path.endswith(".html"):
        output_path += ".html"
    if not os.path.exists(output_path):
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 "
                "Safari/605.1.15"
            )
        }
        response = requests.get(args.url, headers=headers)
        response.raise_for_status()
        enc = response.encoding or "utf-8"
        with open(output_path, "w", encoding=enc) as f:
            f.write(response.text)
        print(f"Downloaded {args.url} to {output_path}")
    else:
        print(f"File '{output_path}' already exists. Skipping download.")

    html_body = open(output_path, "r", encoding="utf-8").read()
    title, blog_entries = extract_blog_post(html_body)
    md_body = []
    md_body.append(title)
    for entry in blog_entries:
        md_body.append(f"{entry}")
        md_body.append("\n")

    md_filename = "read_mode_article.md"
    md_file_path = Path(f"./{md_filename}")
    with md_file_path.open("w") as f:
        f.write("\n".join(md_body))

def main():
    parser = argparse.ArgumentParser(description="Blog Post Extractor CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Extract subcommand
    extract_parser = subparsers.add_parser("extract", help="Extract blog post from URL")
    extract_parser.add_argument(
        "--url", required=True, help="URL of the blog post to extract"
    )
    extract_parser.add_argument("--output", required=True, help="Output file path")
    extract_parser.set_defaults(func=cmd_extract)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
