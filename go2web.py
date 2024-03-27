#!/usr/bin/env python3
import argparse
import json
from bs4 import BeautifulSoup as bs
from colorama import Fore
from http_request import get

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Make easily requests to a web server using this CLI application")

    parser.add_argument("-u", "--url", metavar="<URL>",
                        help="make an HTTP request to the specified URL and print the response"
                        )
    parser.add_argument("-s", "--search", metavar="<search-term>",
                        help="make an HTTP request to search the term using your favorite search engine and print top 10 results"
                        )
    args = parser.parse_args()
    if args.url:
        response = get(args.url)
        is_json = response.headers.get(
            "Content-Type") and response.headers.get("Content-Type").startswith("application/json")
        if is_json:
            print(Fore.GREEN + "JSON Response" + Fore.RESET)
            print(Fore.YELLOW +
                  json.dumps(json.loads(response.body), indent=4) + Fore.RESET)
        else:
            print(Fore.GREEN + "HTML Response" + Fore.RESET)
            soup = bs(response.body, "html.parser")
            content_tags = soup.find_all(
                ["p", "h1", "h2", "h3", "h4", "h5", "h6"])
            for tag in content_tags:
                if not tag.get_text():
                    continue
                color = Fore.BLUE if tag.name == "h1" else Fore.CYAN if tag.name.startswith(
                    "h") else Fore.WHITE
                print(color + tag.get_text() + Fore.RESET)
    elif args.search:
        print(f"{Fore.GREEN}Search results for \"{args.search}\":{Fore.RESET}")
        response = get(f"https://www.google.com/search?q={args.search}")
        soup = bs(response.body, "html.parser")
        headers = soup.select("a h3")
        for index, header in enumerate(headers, start=1):
            anchor = header.find_parent("a")
            print(f"{index}. {Fore.BLUE}{header.get_text()}{Fore.RESET}")
            print(
                f"\t{Fore.CYAN}https://www.google.com{anchor.get('href')}{Fore.RESET}")

    else:
        parser.print_help()
