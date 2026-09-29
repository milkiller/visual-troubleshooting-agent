from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from tools.shell_tool import run_command
from tools.verify_tool import verify_command
from tools.vision.qwen_vision import analyze_screenshot
from tools.file_edit_tool import edit_file
from tools.file_read_tool import read_file
import os
import json


# =====================
# Load API
# =====================

load_dotenv()

api_key = os.getenv("STEP_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.stepfun.com/step_plan/v1"
)


# =====================
# Load Skill
# =====================

skill = Path(
    "skills/troubleshooting/SKILL.md"
).read_text()


# =====================
# Input
# =====================

mode = input(
    "Choose input mode (text/image): "
).strip().lower()


if mode == "image":

    image_path = input(
        "Enter screenshot path: "
    ).strip()

    user_problem = analyze_screenshot(
        image_path
    )

    print("\nVision Result:")
    print(user_problem)


else:

    print(
        "Describe your problem (finish with empty line):"
    )

    lines = []

    while True:
        line = input()

        if line == "":
            break

        lines.append(line)


    user_problem = "\n".join(lines)


print("\nUSER PROBLEM:")
print(user_problem)



# =====================
# Agent Memory
# =====================

messages = [

    {
        "role": "system",
        "content": skill + """

You are an autonomous troubleshooting agent.

Return ONLY valid JSON.

Available actions:

- run_command
- read_file
- edit_file
- none


Rules:

1. If the problem is environment related:
use run_command.

2. If the problem is code related and the file location is unknown:
NEVER stop.
Use run_command to search the current project for relevant source files.

3. After locating a candidate file:
use read_file to inspect the actual code before editing.

4. If the incorrect code is confirmed:
use edit_file.

5. After modification:
always verify the fix.

6. Use action "none" only when:
- the problem has been successfully verified as solved, or
- there is truly no actionable information and project search is impossible.


JSON format:

{
 "analysis": "",
 "action": "",
 "command": "",
 "file": "",
 "old": "",
 "new": "",
 "verify_command": ""
}

"""
    },

    {
        "role": "user",
        "content": user_problem
    }

]



# =====================
# Agent Loop
# =====================

while True:


    response = client.chat.completions.create(
        model="step-5-preview",
        messages=messages
    )


    agent_output = (
        response
        .choices[0]
        .message
        .content
    )


    print("\n================")
    print("Agent Output:")
    print(agent_output)


    clean_json = (
        agent_output
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )


    try:

        action_data = json.loads(
            clean_json
        )

    except Exception:

        print(
            "Agent returned invalid JSON."
        )

        break



    action = action_data.get(
        "action"
    )


    # =====================
    # Finish
    # =====================

    if action == "none":

        print(
            "\nTask finished."
        )

        break



    # =====================
    # Shell
    # =====================

    elif action == "run_command":

        print(
            "\nExecuting:"
        )

        print(
            action_data["command"]
        )


        result = run_command(
            action_data["command"]
        )


    # =====================
    # Read File
    # =====================

    elif action == "read_file":

        print(
            "\nReading:"
        )

        print(
            action_data["file"]
        )


        result = read_file(
            action_data["file"]
        )


    # =====================
    # Edit File
    # =====================

    elif action == "edit_file":

        print(
            "\nEditing:"
        )

        print(
            action_data["file"]
        )


        result = edit_file(

            action_data["file"],

            action_data["old"],

            action_data["new"]

        )


        if (
            result.get("success")
            and action_data.get("verify_command")
        ):

            print(
                "\nVerifying..."
            )

            verify_result = verify_command(
                action_data["verify_command"]
            )


            result = {
                "edit_result": result,
                "verify_result": verify_result
            }



    else:

        result = {
            "error":
            "Unknown action"
        }



    print(
        "\nTool Result:"
    )

    print(result)



    # =====================
    # Feed result back
    # =====================

    messages.append(

        {
            "role": "assistant",
            "content": agent_output
        }

    )


    messages.append(

        {
            "role": "user",
            "content":
            f"""
Tool execution result:

{result}

Continue solving the original problem.
Return JSON only.
"""
        }

    )