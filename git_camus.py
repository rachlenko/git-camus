#!/usr/bin/env python3
""" A simple script to generate commit messages using GitHub Copilot Chat API"""
# -*- coding: utf-8 -*-

import os
import subprocess
import requests


def git_diff_output():
    """Run `git diff` and capture the output"""
    return subprocess.check_output(["git", "status", "-s"], text=True)


def generate_commit_message():
    """Format the `git diff` output as input for the
    GitHub Copilot Chat API
    """
    return {
        "prompt": f"""read following files and generate 
         commit message:\n {git_diff_output()}""",
        "max_tokens": 50,
    }


def call_copilot_chat_api(token, input_msg):
    """Call the GitHub Copilot Chat API"""
    try:
        response = requests.post(
            "https://api.github.com/copilot-chat",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json=input_msg,
        )
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.json()  # Return the JSON response
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Print the HTTP error
    except Exception as err:
        print(f"An error occurred: {err}")  # Print any other error
    return None  # Return None if an error occurred

def main():
    """_summary_"""
    token = os.environ.get("GITHUB_COPILOT_TOKEN")
    diff_output = git_diff_output()
    response = call_copilot_chat_api(token, diff_output)
    # print(f"DEBUG {response.json()}")
    # commit_message = response.json().get("choices", [{}])[0].get("text", "").strip()
    # print(commit_message)
    print(response)


# Example usage
if __name__ == "__main__":
    main()
