// A toy coding agent in F#, talking to the raw HTTP API (no SDK).
//
// The loop is `runTurn`, a recursive function: call the model, run any tools it
// asks for, append the results, and recurse until it stops asking. Hitting the
// API directly means you see the exact JSON — and echoing the assistant turn
// back is trivial (just clone the response's content array verbatim).

open System
open System.IO
open System.Net.Http
open System.Text
open System.Text.Json.Nodes

let model = "claude-opus-4-8"
let url = "https://api.anthropic.com/v1/messages"

let http = new HttpClient()
http.DefaultRequestHeaders.Add("x-api-key", Environment.GetEnvironmentVariable "ANTHROPIC_API_KEY")
http.DefaultRequestHeaders.Add("anthropic-version", "2023-06-01")

// --- Tool definitions: the only things the agent can do in the world ---------
let tools =
    JsonNode.Parse """
    [
      { "name": "list_files",
        "description": "List the files and directories in a directory. Call this to explore the codebase before reading files.",
        "input_schema": { "type": "object",
          "properties": { "directory": { "type": "string", "description": "Directory to list. Defaults to the current directory." } } } },
      { "name": "read_file",
        "description": "Read the full contents of a file. Call this when you need to see what is inside a specific file.",
        "input_schema": { "type": "object",
          "properties": { "path": { "type": "string", "description": "Path to the file to read." } },
          "required": ["path"] } }
    ]"""

// --- Tool implementations ----------------------------------------------------
let private str (node: JsonNode) (key: string) (dflt: string) =
    match node[key] with
    | null -> dflt
    | v -> v.GetValue<string>()

let executeTool (name: string) (input: JsonNode) : string =
    try
        match name with
        | "list_files" ->
            let dir = str input "directory" "."
            Directory.GetFileSystemEntries dir
            |> Array.map Path.GetFileName
            |> Array.sort
            |> String.concat "\n"
        | "read_file" -> File.ReadAllText(str input "path" "")
        | other -> sprintf "error: unknown tool %s" other
    with ex -> sprintf "error: %s" ex.Message

// --- One round trip to the API -----------------------------------------------
let callApi (messages: JsonArray) : JsonNode =
    let body = JsonObject()
    body["model"] <- JsonValue.Create model
    body["max_tokens"] <- JsonValue.Create 16000
    body["tools"] <- tools.DeepClone()
    body["messages"] <- messages.DeepClone()
    use content = new StringContent(body.ToJsonString(), Encoding.UTF8, "application/json")
    let resp = http.PostAsync(url, content).GetAwaiter().GetResult()
    let text = resp.Content.ReadAsStringAsync().GetAwaiter().GetResult()
    if not resp.IsSuccessStatusCode then failwithf "API error %A: %s" resp.StatusCode text
    JsonNode.Parse text

// --- The loop ----------------------------------------------------------------
let rec runTurn (messages: JsonArray) =
    let response = callApi messages
    let content = response["content"].AsArray()

    // Echo the assistant turn back into history (clone — a node has one parent).
    let assistant = JsonObject()
    assistant["role"] <- JsonValue.Create "assistant"
    assistant["content"] <- content.DeepClone()
    messages.Add assistant

    let toolUses =
        content
        |> Seq.filter (fun b -> b["type"].GetValue<string>() = "tool_use")
        |> Seq.toList

    if List.isEmpty toolUses then
        for b in content do
            if b["type"].GetValue<string>() = "text" then printfn "%s" (b["text"].GetValue<string>())
    else
        let results = JsonArray()
        for tu in toolUses do
            let r = JsonObject()
            r["type"] <- JsonValue.Create "tool_result"
            r["tool_use_id"] <- JsonValue.Create(tu["id"].GetValue<string>())
            r["content"] <- JsonValue.Create(executeTool (tu["name"].GetValue<string>()) tu["input"])
            results.Add r
        let userMsg = JsonObject()
        userMsg["role"] <- JsonValue.Create "user"
        userMsg["content"] <- results
        messages.Add userMsg
        runTurn messages

[<EntryPoint>]
let main _ =
    let messages = JsonArray()
    printfn "Toy agent. Ask about files in this directory. Ctrl-D to quit."
    let mutable running = true
    while running do
        Console.Write "you> "
        match Console.ReadLine() with
        | null -> running <- false
        | line ->
            let userMsg = JsonObject()
            userMsg["role"] <- JsonValue.Create "user"
            userMsg["content"] <- JsonValue.Create line
            messages.Add userMsg
            runTurn messages
    0
