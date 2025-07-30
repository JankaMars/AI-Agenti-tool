import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor

#načtení enviromentálních proměnných
load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))    



# Funkce, kterou budeme volat
def add_numbers(a, b):
    return a + b

# Definice nástroje (funkce pro AI)
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_numbers",
            "description": "Sečte dvě čísla",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "První číslo"},
                    "b": {"type": "number", "description": "Druhé číslo"}
                },
                "required": ["a", "b"]
            }
        }
    }
]

# Zpráva od uživatele
messages = [
    {"role": "system", "content": "Jsi asistent, který umí sčítat čísla."},
    {"role": "user", "content": "Kolik je 10 + 32 + 25?"}
]

# Požadavek na model – AI si sama vybere nástroj
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=messages,
    tools=tools,
    tool_choice={"type": "function", "function": {"name": "add_numbers"}}
)

tool_call = response.choices[0].message.tool_calls[0]
tool_call_id = tool_call.id
function_name = tool_call.function.name
arguments = json.loads(tool_call.function.arguments)

# Spustíme funkci lokálně
if function_name == "add_numbers":
    result = add_numbers(**arguments)

# Přidáme odpověď funkce do zpráv – POZOR na správné ID!
messages.append(response.choices[0].message)
messages.append({
    "role": "tool",
    "tool_call_id": tool_call_id,
    "content": str(result)
})

final_response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=messages
)

# Výpis odpovědi
print(final_response.choices[0].message.content)