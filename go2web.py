#!/usr/bin/env python3
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Make easily requests to a web server using this CLI application")

    parser.add_argument("-u", "--url", help="URL to connect to")
    parser.add_argument("-p", "--port", help="Port to connect to")
    parser.add_argument("-d", "--directory", help="Directory to connect to")

    args = parser.parse_args()
