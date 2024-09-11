# import os
import pytest
import sys
# import subprocess
# import sys

# try :
#     import git_camus
# except ImportError as e:
#     print(e)
#import os.path.join(sys.path.pwd(), "git_camus") import git_diff_output, call_copilot_chat_api

def test_always_passes():
    assert True

def test_always_fails():
    assert False
    
    
# Assuming the functions are imported from git_camus.py
# from git_camus import git_diff_output, call_copilot_chat_api
def test_git_diff_output():
        diff_output = git_diff_output()
        # Assertions
        assert diff_output == subprocess.check_output(["git", "status", "-s"], text=True)

# # def test_generate_commit_message():
#     # Mock environment variable
#     with patch.dict(os.environ, {"GITHUB_COPILOT_TOKEN": "fake_token"}):
#         # Mock git_diff_output function
#         with patch('git_camus.git_diff_output', return_value="sample diff output"):
#             # Mock call_copilot_chat_api function
#             mock_response = MagicMock()
#             mock_response.json.return_value = {
#                 "choices": [{"text": "Sample commit message"}]
#             }
#             with patch('git_camus.call_copilot_chat_api', return_value=mock_response):
#                 # Execute the code block
#                 token = os.environ.get("GITHUB_COPILOT_TOKEN")
#                 diff_output = git_camus.git_diff_output()
#                 response = git_camus.call_copilot_chat_api(token, diff_output)
#                 print(f"DEBUG {response.json()}")
#                 commit_message = response.json().get("choices", [{}])[0].get("text", "").strip()          
#                 # Assertions
#                 # assert token == "fake_token"
#                 assert diff_output == "sample diff output"
#                 assert response.json() == {"choices": [{"text": "Sample commit message"}]}
#                 assert commit_message == "Sample commit message"
    