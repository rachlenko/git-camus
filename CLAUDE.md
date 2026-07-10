# git-camus — Project Guidance

## Commit messages

Write every commit message as a human engineer would in a professional
codebase.

- Use clear, plain, professional English. No slang, no filler, no
  philosophical flourishes in the message itself (the tool generates
  those for end users — internal commits stay grounded).
- The subject line states *what* the commit changes, in the imperative
  mood, under 72 characters. Prefer the conventional-commit prefixes
  already used in the history (`feat:`, `fix:`, `chore:`, `docs:`,
  `refactor:`, `test:`).
- If the change is non-trivial, add a body that explains *what*
  changed and *why*. Reference issue numbers when they exist. Wrap the
  body at 72 columns.
- Do not add attribution lines, trailers, or footers that reveal the
  message was produced with AI assistance. This means: no
  `Co-Authored-By: Claude ...`, no `Generated with Claude Code`, no
  emoji robot tags, no "made by Claude", no "AI-assisted" notes. The
  commit must read as if a human wrote it end to end.
- Do not sign commits on the user's behalf with a tool identity.
