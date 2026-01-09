# Gemini Function Calling

Function calling enables Gemini models to interact with external tools and APIs by generating structured function calls that your application can execute.

## Basic Concept

1. **Define** function declarations with schemas
2. **Send** user message + function definitions to model
3. **Model** decides to call functions and generates arguments
4. **You** execute the functions
5. **Send** results back for final response

## Function Declaration Schema

```python
from google import genai
from google.genai import types

function_declaration = types.FunctionDeclaration(
    name="get_weather",
    description="Get the current weather in a location",
    parameters=types.Schema(
        type="object",
        properties={
            "location": types.Schema(
                type="string",
                description="The city and country, e.g., Paris, France"
            ),
            "unit": types.Schema(
                type="string",
                enum=["celsius", "fahrenheit"],
                description="Temperature unit"
            )
        },
        required=["location"]
    )
)
```

## Complete Example

```python
from google import genai
from google.genai import types
import json

client = genai.Client()

# Step 1: Define function
get_weather = types.FunctionDeclaration(
    name="get_weather",
    description="Get the current weather for a location",
    parameters=types.Schema(
        type="object",
        properties={
            "location": types.Schema(
                type="string",
                description="City name, e.g., Tokyo, Japan"
            ),
            "unit": types.Schema(
                type="string",
                enum=["celsius", "fahrenheit"]
            )
        },
        required=["location"]
    )
)

# Create tool
tools = types.Tool(function_declarations=[get_weather])

# Step 2: Send request with tools
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What's the weather in Paris?",
    config=types.GenerateContentConfig(tools=[tools])
)

# Step 3: Check for function calls
function_call = response.candidates[0].content.parts[0].function_call

if function_call:
    # Step 4: Execute function (your implementation)
    def execute_get_weather(location, unit="celsius"):
        # In reality, call a weather API
        return {"temperature": 22, "condition": "sunny", "unit": unit}

    args = dict(function_call.args)
    result = execute_get_weather(**args)

    # Step 5: Send function result back
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Content(role="user", parts=[
                types.Part(text="What's the weather in Paris?")
            ]),
            types.Content(role="model", parts=[
                types.Part(function_call=function_call)
            ]),
            types.Content(role="user", parts=[
                types.Part(function_response=types.FunctionResponse(
                    name=function_call.name,
                    response=result
                ))
            ])
        ],
        config=types.GenerateContentConfig(tools=[tools])
    )

    print(response.text)
    # "The weather in Paris is sunny with a temperature of 22°C."
```

## REST API Format

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{"text": "What is the weather in Paris?"}]
    }],
    "tools": [{
      "function_declarations": [{
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City name"
            },
            "unit": {
              "type": "string",
              "enum": ["celsius", "fahrenheit"]
            }
          },
          "required": ["location"]
        }
      }]
    }]
  }'
```

## Function Calling Modes

```python
config = types.GenerateContentConfig(
    tools=[tools],
    tool_config=types.ToolConfig(
        function_calling_config=types.FunctionCallingConfig(
            mode="AUTO"  # or "ANY", "NONE", "VALIDATED"
        )
    )
)
```

| Mode | Behavior |
|------|----------|
| `AUTO` | Model decides whether to call functions (default) |
| `ANY` | Model must call a function, schema enforced |
| `NONE` | Disable function calling |
| `VALIDATED` | Schema compliance with flexible response types |

### Force Specific Function

```python
tool_config=types.ToolConfig(
    function_calling_config=types.FunctionCallingConfig(
        mode="ANY",
        allowed_function_names=["get_weather"]  # Only allow this function
    )
)
```

## Parallel Function Calling

Gemini can call multiple functions in a single response:

```python
# User: "What's the weather in Paris and London?"

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What's the weather in Paris and London?",
    config=types.GenerateContentConfig(tools=[tools])
)

# Model may return multiple function calls
for part in response.candidates[0].content.parts:
    if part.function_call:
        print(f"Call: {part.function_call.name}({dict(part.function_call.args)})")
# Output:
# Call: get_weather({'location': 'Paris'})
# Call: get_weather({'location': 'London'})
```

### Handle Multiple Calls
```python
# Execute all function calls
results = []
for part in response.candidates[0].content.parts:
    if part.function_call:
        result = execute_function(part.function_call.name, dict(part.function_call.args))
        results.append(types.Part(
            function_response=types.FunctionResponse(
                name=part.function_call.name,
                response=result
            )
        ))

# Send all results back
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        # Original user message
        types.Content(role="user", parts=[types.Part(text=original_query)]),
        # Model's function calls
        response.candidates[0].content,
        # All function responses
        types.Content(role="user", parts=results)
    ],
    config=types.GenerateContentConfig(tools=[tools])
)
```

## Complex Schema Example

```python
schedule_meeting = types.FunctionDeclaration(
    name="schedule_meeting",
    description="Schedule a new meeting in the calendar",
    parameters=types.Schema(
        type="object",
        properties={
            "title": types.Schema(
                type="string",
                description="Meeting title"
            ),
            "datetime": types.Schema(
                type="string",
                description="ISO 8601 datetime, e.g., 2025-01-15T14:00:00Z"
            ),
            "duration_minutes": types.Schema(
                type="integer",
                description="Duration in minutes"
            ),
            "attendees": types.Schema(
                type="array",
                items=types.Schema(
                    type="object",
                    properties={
                        "email": types.Schema(type="string"),
                        "name": types.Schema(type="string"),
                        "required": types.Schema(type="boolean")
                    },
                    required=["email"]
                ),
                description="List of attendees"
            ),
            "recurrence": types.Schema(
                type="string",
                enum=["none", "daily", "weekly", "monthly"]
            ),
            "notes": types.Schema(
                type="string",
                description="Optional meeting notes"
            )
        },
        required=["title", "datetime", "duration_minutes", "attendees"]
    )
)
```

## Automatic Function Calling (Python SDK)

The Python SDK can automatically convert Python functions to declarations:

```python
def get_weather(location: str, unit: str = "celsius") -> dict:
    """Get the current weather for a location.

    Args:
        location: City name, e.g., "Paris, France"
        unit: Temperature unit, either "celsius" or "fahrenheit"

    Returns:
        Weather information including temperature and conditions
    """
    # Your implementation
    return {"temperature": 22, "condition": "sunny"}

# SDK converts the function to a declaration automatically
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What's the weather in Tokyo?",
    config=types.GenerateContentConfig(
        tools=[get_weather]  # Pass function directly
    )
)
```

## Built-in Tools

### Google Search Grounding
```python
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What are the latest AI news?",
    config=types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())]
    )
)
```

### Code Execution
```python
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Calculate the factorial of 20",
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution=types.CodeExecution())]
    )
)
```

### Combining Custom Functions + Built-in Tools
```python
config = types.GenerateContentConfig(
    tools=[
        types.Tool(function_declarations=[my_custom_function]),
        types.Tool(google_search=types.GoogleSearch()),
        types.Tool(code_execution=types.CodeExecution())
    ]
)
```

## Best Practices

### 1. Write Clear Descriptions
```python
# Good
description="Get the current stock price for a ticker symbol. Returns price in USD."

# Bad
description="Get stock"
```

### 2. Use Enums for Limited Options
```python
"unit": types.Schema(
    type="string",
    enum=["celsius", "fahrenheit"]
)
```

### 3. Provide Parameter Descriptions
```python
"location": types.Schema(
    type="string",
    description="City and country, e.g., 'Tokyo, Japan'"
)
```

### 4. Keep Tool Sets Manageable
- **Optimal:** 10-20 functions
- Too many functions can confuse the model

### 5. Validate Before Execution
```python
def validate_and_execute(function_call):
    name = function_call.name
    args = dict(function_call.args)

    # Validate
    if name == "get_weather":
        if "location" not in args:
            return {"error": "location is required"}
        if args.get("unit") not in [None, "celsius", "fahrenheit"]:
            return {"error": "invalid unit"}

    # Execute
    return execute_function(name, args)
```

## Error Handling

```python
# Return error as function response
error_response = types.Part(
    function_response=types.FunctionResponse(
        name=function_call.name,
        response={"error": "Location not found", "details": "..."}
    )
)

# Model will handle the error gracefully
```

## Differences from OpenAI

| Aspect | OpenAI | Gemini |
|--------|--------|--------|
| Schema location | Nested under `function:` | Direct in declaration |
| Response field | `tool_calls` | `function_call` in parts |
| Result role | `tool` | `user` with function_response |
| Strict mode | `strict: true` | Use `mode: "VALIDATED"` |

## Official Documentation
- Function Calling: https://ai.google.dev/gemini-api/docs/function-calling
- Vertex AI: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling
