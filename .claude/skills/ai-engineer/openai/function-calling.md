# OpenAI Function Calling

Function calling allows models to generate structured outputs that match your defined schemas, enabling integration with external APIs and tools.

## Basic Concept

1. **Define** function schemas in your request
2. **Send** user message to the model
3. **Model** decides whether to call a function and generates arguments
4. **You** execute the function with the arguments
5. **Send** results back to the model for final response

## Function Definition Schema

```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "Get the current weather in a location",
    "strict": true,
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "The city and state, e.g., San Francisco, CA"
        },
        "unit": {
          "type": "string",
          "enum": ["celsius", "fahrenheit"],
          "description": "Temperature unit"
        }
      },
      "required": ["location"],
      "additionalProperties": false
    }
  }
}
```

## Complete Example (Python)

```python
from openai import OpenAI
import json

client = OpenAI()

# Define tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather in a location",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name, e.g., Paris, France"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": ["location"],
                "additionalProperties": False
            }
        }
    }
]

# Your actual function implementation
def get_weather(location: str, unit: str = "celsius") -> dict:
    # In reality, call a weather API here
    return {"temperature": 22, "unit": unit, "condition": "sunny"}

# Step 1: Send user message with tools
response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
    tools=tools,
    tool_choice="auto"
)

message = response.choices[0].message

# Step 2: Check if model wants to call a function
if message.tool_calls:
    # Step 3: Execute the function
    tool_call = message.tool_calls[0]
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)

    if function_name == "get_weather":
        result = get_weather(**function_args)

    # Step 4: Send function result back
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "user", "content": "What's the weather in Paris?"},
            message,  # Include the assistant's tool_calls message
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            }
        ],
        tools=tools
    )

    print(response.choices[0].message.content)
    # Output: "The weather in Paris is currently sunny with a temperature of 22°C."
```

## Strict Mode (Recommended)

Setting `strict: true` guarantees the model's output matches your schema exactly.

```python
{
    "type": "function",
    "function": {
        "name": "my_function",
        "strict": True,  # <-- Enable strict mode
        "parameters": {
            "type": "object",
            "properties": {...},
            "required": [...],
            "additionalProperties": False  # <-- Required for strict mode
        }
    }
}
```

**Strict mode requirements:**
- `additionalProperties: false` must be set
- All fields must have explicit types
- No `anyOf`, `oneOf`, or unsupported keywords

## Tool Choice Options

```python
# Auto (default) - model decides whether to call functions
tool_choice="auto"

# Required - model MUST call at least one function
tool_choice="required"

# Specific function - force a particular function
tool_choice={"type": "function", "function": {"name": "get_weather"}}

# None - disable function calling
tool_choice="none"
```

## Parallel Function Calling

By default, the model can request multiple function calls in one response:

```python
response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[{
        "role": "user",
        "content": "What's the weather in Paris and London?"
    }],
    tools=tools,
    parallel_tool_calls=True  # Default
)

# message.tool_calls might contain multiple calls:
# [
#   {"id": "call_1", "function": {"name": "get_weather", "arguments": '{"location": "Paris"}'}},
#   {"id": "call_2", "function": {"name": "get_weather", "arguments": '{"location": "London"}'}}
# ]
```

**Disable parallel calls:**
```python
parallel_tool_calls=False
```

## Supported Parameter Types

| JSON Schema Type | Example |
|------------------|---------|
| `string` | `"type": "string"` |
| `number` | `"type": "number"` |
| `integer` | `"type": "integer"` |
| `boolean` | `"type": "boolean"` |
| `array` | `"type": "array", "items": {...}` |
| `object` | `"type": "object", "properties": {...}` |
| `enum` | `"enum": ["value1", "value2"]` |
| `null` | `"type": "null"` |

## Complex Schema Example

```python
tools = [{
    "type": "function",
    "function": {
        "name": "create_calendar_event",
        "description": "Create a new calendar event",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Event title"
                },
                "start_time": {
                    "type": "string",
                    "description": "ISO 8601 datetime"
                },
                "duration_minutes": {
                    "type": "integer",
                    "description": "Duration in minutes"
                },
                "attendees": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "email": {"type": "string"},
                            "name": {"type": "string"}
                        },
                        "required": ["email"],
                        "additionalProperties": False
                    },
                    "description": "List of attendees"
                },
                "recurrence": {
                    "type": "string",
                    "enum": ["none", "daily", "weekly", "monthly"],
                    "description": "Recurrence pattern"
                },
                "is_virtual": {
                    "type": "boolean",
                    "description": "Whether it's a virtual meeting"
                }
            },
            "required": ["title", "start_time", "duration_minutes"],
            "additionalProperties": False
        }
    }
}]
```

## Best Practices

### 1. Write Clear Descriptions
```python
# Good
"description": "Get the current stock price for a given ticker symbol"

# Bad
"description": "Get stock"
```

### 2. Use Enums for Limited Options
```python
"unit": {
    "type": "string",
    "enum": ["celsius", "fahrenheit"]
}
```

### 3. Provide Parameter Descriptions
```python
"location": {
    "type": "string",
    "description": "City and country, e.g., 'Tokyo, Japan'"
}
```

### 4. Keep Tool Sets Manageable
- **Optimal:** 10-20 tools maximum
- **Max arguments per tool:** ~20
- More tools = slower, potentially less accurate

### 5. Use Low Temperature for Determinism
```python
response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[...],
    tools=tools,
    temperature=0  # More deterministic function calls
)
```

### 6. Validate Before Execution
```python
# Always validate function arguments before executing
import json
from pydantic import BaseModel, ValidationError

class WeatherArgs(BaseModel):
    location: str
    unit: str = "celsius"

try:
    args = WeatherArgs(**json.loads(tool_call.function.arguments))
    result = get_weather(args.location, args.unit)
except ValidationError as e:
    result = {"error": str(e)}
```

## Handling Function Errors

```python
try:
    result = my_function(**args)
except Exception as e:
    result = {"error": str(e)}

# Send error back to model
response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "user", "content": original_query},
        assistant_message,
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)  # Include error info
        }
    ],
    tools=tools
)
```

## Differences: Chat Completions vs Responses API

### Chat Completions (Legacy)
```python
{
    "tools": [{
        "type": "function",
        "function": {
            "name": "my_func",
            "parameters": {...}
        }
    }]
}
```

### Responses API (New)
```python
{
    "tools": [
        {"type": "web_search"},  # Built-in tools!
        {"type": "file_search"},
        {"type": "code_interpreter"},
        {
            "type": "function",
            "function": {
                "name": "my_func",
                "parameters": {...}
            }
        }
    ]
}
```

## Official Documentation
- Function Calling Guide: https://platform.openai.com/docs/guides/function-calling
- Tool Use: https://platform.openai.com/docs/guides/tools
