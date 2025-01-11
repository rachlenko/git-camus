#!/usr/bin/env python3
"""A simple script to generate commit messages using GitHub Copilot Chat API"""
# -*- coding: utf-8 -*-

import os
import subprocess
from typing import Optional, Dict

import requests
import click
import sys




def git_diff_output() -> str:
    """Run `git diff` and capture the output"""
    return subprocess.check_output(["git", "status", "-s"], text=True)


def generate_commit_message()-> dict[str, str | int]:
    """Format the `git diff` output as input for the
    GitHub Copilot Chat API
    """
    return {
        "prompt": f"""read following files and generate
         commit message:\n {git_diff_output()}""",
        "max_tokens": 50,
    }


def call_copilot_chat_api(token , input_msg):
    """Call the GitHub Copilot Chat API"""
    response: dict[Optional, Optional] = {}
    try:
        response = requests.post(
            'https://api.github.com/copilot-chat',
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=input_msg,
        )
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.json()  # Return the JSON response
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Print the HTTP error
    except Exception as err:
        print(f"An error occurred: {err}")  # Print any other error
    return  response # Return None if an error occurred


def main() -> None:
    """_summary_"""
    click.command()
    click.option("--token", required=True, help="GitHub Copilot token")
    click.option("--diff", required=True, help="Git diff output")
    click.option("--setup", help="Setup GitHub Copilot token")
    click.option("--version", help="Print version")
    click.option("--help", help="Print help")

    if os.environ.get("GITHUB_COPILOT_TOKEN"):
        token = os.environ.get("GITHUB_COPILOT_TOKEN")
    else:
        token = click.prompt("Enter your GitHub Copilot token")
        # if os is windows
        if "nt" in os.name:
            print(
                f"""
            # save following lines into git-camus.bat file and run it
            # or define the environment variables in your shell profile

            set GITHUB_COPILOT_TOKEN="{token}"
            set PYTHONIOENCODING="utf-8"
            python3 git_camus.py %*
            """
            )
            sys.exit(0)
        else:
            print(
                f"""
            # save following lines into git-camus.sh file and run it
            # or define the environment variables in your shell profile

            export GITHUB_COPILOT_TOKEN="{token}"
            export PYTHONIOENCODING="utf-8"
            python3 git_camus.py $@
            """
            )
            sys.exit(0)

    diff_output = git_diff_output()
    response = call_copilot_chat_api(token, diff_output)
    # print(f"DEBUG {response.json()}")
    # commit_message = response.json().get("choices", [{}])[0].get("text", "").strip()
    # print(commit_message)
    print(response)


# Example usage
if __name__ == "__main__":
    test = generate_commit_message()
    print(dir(test))


    #main()
