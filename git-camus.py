#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import requests

GITHUB_TOKEN = os.environ.get('GITHUB_COPILOT_TOKEN')

#write function calling to github copilot chat and generate commit message from input taken git diff request



def generate_commit_message():
    # Step 1: Run `git diff` and capture the output
    git_diff_output = subprocess.check_output(['git', 'status'], text=True)
    
    # Step 2: Format the `git diff` output as input for the GitHub Copilot Chat API
    copilot_input = {
        "prompt": f"Generate a commit message for the following git diff:\n{git_diff_output}",
        "max_tokens": 50
    }
    
    # Step 3: Call the GitHub Copilot Chat API
    token_str = f'Bearer {GITHUB_TOKEN}'
    response = requests.post(
        'https://api.github.com/copilot-chat',
        headers={'Authorization': token_str },
        json=copilot_input
    )
    
    # Step 4: Parse the response to extract the commit message
    commit_message = response.json().get('choices', [{}])[0].get('text', '').strip()
    
    # Step 5: Return the commit message
    return commit_message

# Example usage
if __name__ == "__main__":
    commit_message = generate_commit_message()
    print(f"Generated Commit Message: {commit_message}")
