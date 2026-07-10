---
name: commit-message
description: Draft a git commit message for the current staged diff in professional English. Explains what changed and why, uses the project's conventional-commit prefix style, and never leaves any AI-authored trailer or signature.
---

# commit-message

Produce a commit message for the currently staged changes that a human
engineer could have written and would want to sign.

## Steps

1. Read the staged diff:
   ```sh
   git diff --cached --stat
   git diff --cached
   ```
   If nothing is staged, stop and tell the user to stage the changes first.

2. Look at recent history to match the project's style:
   ```sh
   git log --oneline -20
   ```
   This project uses conventional-commit prefixes (`feat:`, `fix:`,
   `chore:`, `docs:`, `refactor:`, `test:`, `perf:`, `ci:`).

3. Draft the message:
   - **Subject line**: imperative mood, under 72 characters, starts
     with the correct conventional-commit prefix. State the change,
     not the motivation.
   - **Body** (only if the change is non-trivial): explain what
     changed and why. Wrap at 72 columns. Reference issue or PR
     numbers if the user provided them.
   - Keep the tone plain and professional. No jokes, no philosophical
     asides, no emoji.

4. Hard rules — do not violate:
   - **No AI attribution of any kind.** Never add:
     - `Co-Authored-By: Claude ...`
     - `Generated with Claude Code`
     - `🤖 Generated with ...`
     - "AI-assisted", "written with Claude", or similar phrases
       anywhere in subject, body, or trailer.
   - **Do not sign the commit** with a bot / tool identity.
   - Do not mention this skill, prompts, or the model in the message.

5. Show the draft to the user and wait for confirmation before
   committing. If they approve, run:
   ```sh
   git commit -m "<subject>" -m "<body>"
   ```
   (Or a single `-m` if there is no body.) Use a heredoc when the body
   contains characters that would fight shell quoting.

## Style checklist before you present the draft

- [ ] Subject ≤ 72 chars, imperative, correct prefix.
- [ ] Body (if present) wrapped ≤ 72 chars per line.
- [ ] No AI / Claude / bot references anywhere.
- [ ] Reads like a human engineer wrote it.
- [ ] Describes the change, not the process of arriving at it.
