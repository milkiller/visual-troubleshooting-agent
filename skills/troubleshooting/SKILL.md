---
name: troubleshooting
description: Diagnose and fix common development environment problems from screenshots and error messages.
---

**# Troubleshooting Skill**

**## When to use**
Use this skill when the user provides:
\- error screenshots
\- terminal errors
\- development environment problems

**## Workflow**

Follow this troubleshooting process:

1\. Analyze the screenshot, traceback, or error message.

2\. Classify the problem:
   - environment issue
   - source code issue
   - configuration issue

3\. Select tools based on the problem type.

4\. Execute the selected action.

5\. After receiving tool results:
   - analyze the result
   - decide the next action
   - continue until the problem is solved

6\. Always verify the final fix.

**## Available tools**

\- shell_tool:
  Execute safe terminal commands for diagnosis, searching files, and environment repair.

\- read_file:
  Read source code before making code modifications.

\- file_edit:
  Modify source code using exact old and new code blocks.

\- verify_command:
  Run verification commands after changes to confirm the problem is solved.

**## Tool usage rules**

Before executing commands:

1\. Include the reason in the "analysis" field.
2\. Only run commands related to the detected problem.
3\. Verify the result after execution.

**## Supported problems**

\- Python missing package
\- Python environment issues
\- Command errors

**## Output format**

Always return JSON only.

Schema:

{
 "analysis": "",
 "action": "",
 "command": "",
 "file": "",
 "old": "",
 "new": "",
 "verify_command": ""
}

**## Code debugging**

When the problem is caused by source code:

1\. Locate the target file.
2\. Read the relevant code.
3\. Identify the incorrect logic.
4\. Generate an edit_file action with:
   - exact old code
   - corrected new code
5\. Verify the program after editing.

Do not only explain the solution.

**## Decision rules**

\- If the error is caused by missing packages or environment:
  use run_command.

\- If the error is related to source code:

  1\. If the file path is unknown:
     use run_command to search.

  2\. If the file path is known but code context is missing:
     use read_file.

  3\. If the incorrect code is confirmed:
     use file_edit.

  4\. After modification:
     use verify_command.

\- Never directly edit code without confirming the target file and code content.

**## File location rules**

\- Never guess a file path.
\- If the screenshot does not contain a reliable file path:
    use run_command to search first.
\- Only use edit_file after confirming the target file.
\- Use search results as evidence before selecting a file.
\- If a previous edit fails because the target code is not found, search again instead of retrying the same edit.

**## Vision debugging rules**

When information comes from screenshots:

\- Extract error messages, file paths, and code snippets from the image.
\- Do not assume a file name if it is not visible.
\- If the screenshot does not provide enough file information:
  search the project before editing.

**## File editing**

When code logic is incorrect:
\- Use edit_file action.
\- Provide exact old code and corrected new code.
\- Modify only the necessary part of the file.

**## Iterative reasoning rules**

After every tool execution:

\- Treat the tool result as new evidence.
\- Re-evaluate the problem.
\- Select the next action if the problem is not solved.
\- Stop only after verification succeeds.