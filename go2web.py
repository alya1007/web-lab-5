#!/usr/bin/env python3
import argparse

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
        print(f"Making request to {args.url}")
    elif args.search:
        print(f"Searching for {args.search}")
    else:
        parser.print_help()
