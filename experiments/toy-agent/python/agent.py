"""A toy coding agent in ~80 lines, using the official Anthropic SDK.

The whole agent is `run_turn`: call the model, run any tools it asks for, feed
the results back, repeat until it stops asking. That loop IS the agent.
"""

import os
import anthropic

MODEL = "claude-opus-4-8"
client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment

# --- Tool definitions: the only things the agent can do in the world ----------
TOOLS = [
    {
        "name": "list_files",
        "description": "List the files and directories in a directory. "
                       "Call this to explore the codebase before reading files.",
        "input_schema": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory to list. Defaults to the current directory.",
                },
            },
        },
    },
    {
        "name": "read_file",
        "description": "Read the full contents of a file. Call this when you "
                       "need to see what is inside a specific file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to the file to read."},
            },
            "required": ["path"],
        },
    },
]


# --- Tool implementations: your code decides what actually happens -------------
def list_files(directory="."):
    try:
        return "\n".join(sorted(os.listdir(directory)))
    except OSError as e:
        return f"error: {e}"


def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except OSError as e:
        return f"error: {e}"


def execute_tool(name, tool_input):
    if name == "list_files":
        return list_files(tool_input.get("directory", "."))
    if name == "read_file":
        return read_file(tool_input.get("path", ""))
    return f"error: unknown tool {name}"


# --- The loop ------------------------------------------------------------------
def run_turn(messages):
    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=16000,
            tools=TOOLS,
            messages=messages,
        )
        # Echo the assistant's turn (text + tool_use blocks) back into history.
        messages.append({"role": "assistant", "content": response.content})

        for block in response.content:
            if block.type == "text":
                print(block.text)

        tool_uses = [b for b in response.content if b.type == "tool_use"]
        if not tool_uses:
            return  # no tool requested -> the turn is done

        tool_results = [
            {
                "type": "tool_result",
                "tool_use_id": tu.id,
                "content": execute_tool(tu.name, tu.input),
            }
            for tu in tool_uses
        ]
        messages.append({"role": "user", "content": tool_results})


def main():
    messages = []
    print("Toy agent. Ask about files in this directory. Ctrl-D to quit.")
    while True:
        try:
            user = input("you> ")
        except EOFError:
            break
        messages.append({"role": "user", "content": user})
        run_turn(messages)


if __name__ == "__main__":
    main()
