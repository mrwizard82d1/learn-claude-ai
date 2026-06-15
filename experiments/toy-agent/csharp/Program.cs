// A toy coding agent using the official Anthropic .NET SDK.
//
// The loop lives in RunTurn(): call the model, run any tools it asks for, feed
// the results back, repeat until it stops asking. Same loop as the other three
// implementations — just typed and explicit.

using System.Text.Json;
using Anthropic;
using Anthropic.Models.Messages;

var client = new AnthropicClient(); // reads ANTHROPIC_API_KEY

// --- Tool definitions: the only things the agent can do in the world ---------
var tools = new List<ToolUnion>
{
    new Tool
    {
        Name = "list_files",
        Description = "List the files and directories in a directory. "
                    + "Call this to explore the codebase before reading files.",
        InputSchema = new()
        {
            Properties = new Dictionary<string, JsonElement>
            {
                ["directory"] = JsonSerializer.SerializeToElement(
                    new { type = "string", description = "Directory to list. Defaults to the current directory." }),
            },
        },
    },
    new Tool
    {
        Name = "read_file",
        Description = "Read the full contents of a file. Call this when you "
                    + "need to see what is inside a specific file.",
        InputSchema = new()
        {
            Properties = new Dictionary<string, JsonElement>
            {
                ["path"] = JsonSerializer.SerializeToElement(
                    new { type = "string", description = "Path to the file to read." }),
            },
            Required = ["path"],
        },
    },
};

var messages = new List<MessageParam>();
Console.WriteLine("Toy agent. Ask about files in this directory. Ctrl-D to quit.");
while (true)
{
    Console.Write("you> ");
    var line = Console.ReadLine();
    if (line is null) break;
    messages.Add(new() { Role = Role.User, Content = line });
    await RunTurn();
}

// --- The loop ----------------------------------------------------------------
async Task RunTurn()
{
    while (true)
    {
        var response = await client.Messages.Create(new MessageCreateParams
        {
            Model = Model.ClaudeOpus4_8,
            MaxTokens = 16000,
            Tools = tools,
            Messages = messages,
        });

        // Rebuild the assistant turn (no .ToParam() in C# — reconstruct per variant)
        // and collect tool results in the same pass.
        var assistantContent = new List<ContentBlockParam>();
        var toolResults = new List<ContentBlockParam>();

        foreach (var block in response.Content)
        {
            if (block.TryPickText(out TextBlock? text))
            {
                Console.WriteLine(text.Text);
                assistantContent.Add(new TextBlockParam { Text = text.Text });
            }
            else if (block.TryPickToolUse(out ToolUseBlock? toolUse))
            {
                assistantContent.Add(new ToolUseBlockParam
                {
                    ID = toolUse.ID,
                    Name = toolUse.Name,
                    Input = toolUse.Input,
                });
                var input = JsonSerializer.SerializeToElement(toolUse.Input);
                toolResults.Add(new ToolResultBlockParam
                {
                    ToolUseID = toolUse.ID,
                    Content = ExecuteTool(toolUse.Name, input),
                });
            }
        }

        messages.Add(new() { Role = Role.Assistant, Content = assistantContent });

        if (toolResults.Count == 0) return; // no tool requested -> turn is done

        messages.Add(new() { Role = Role.User, Content = toolResults });
    }
}

// --- Tool implementations ----------------------------------------------------
static string ExecuteTool(string name, JsonElement input)
{
    try
    {
        switch (name)
        {
            case "list_files":
                var dir = input.TryGetProperty("directory", out var d) ? d.GetString()! : ".";
                return string.Join("\n",
                    Directory.GetFileSystemEntries(dir).Select(Path.GetFileName).OrderBy(x => x));
            case "read_file":
                var path = input.TryGetProperty("path", out var p) ? p.GetString()! : "";
                return File.ReadAllText(path);
            default:
                return $"error: unknown tool {name}";
        }
    }
    catch (Exception e)
    {
        return $"error: {e.Message}";
    }
}
