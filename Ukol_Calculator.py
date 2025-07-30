import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from langgraph.graph import StateGraph, END

# Načti .env s OPENAI_API_KEY
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ===== TOOL =====
def multiply(a, b):
    return a * b

def sum(a, b):
    return a + b

def subtract(a, b):
    return a - b    

def divide(a, b):
    if b == 0:
        raise ValueError("Dělení nulou není povoleno.")
    return a / b

tools = {
    "multiply": {
        "function": multiply,
        "schema": {
            "name": "multiply",
            "description": "Násobí dvě čísla",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            }
        }
    },
    "sum": {
        "function": sum,
        "schema": {
            "name": "sum",
            "description": "Sčítá dvě čísla",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            }
        }   
    },
    "subtract": {
        "function": subtract,
        "schema": {
            "name": "subtract",
            "description": "Odečítá dvě čísla",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            }
        },
    },
    "divide": {
        "function": divide,
        "schema": {
            "name": "divide",
            "description": "Dělí dvě čísla",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            }
        }
    }
}
# ===== UZLY =====
def planner(state: dict) -> dict:
    messages = state["messages"]

    response = client.chat.completions.create(
        model="gpt-4.1-mini", 
        messages=messages,
        tools=[{"type": "function", "function": tools["multiply"]["schema"]}]
    )

    ai_msg = response.choices[0].message
    state["messages"].append(ai_msg)

    if ai_msg.tool_calls:
        tool_call = ai_msg.tool_calls[0]
        state["tool_call_id"] = tool_call.id
        state["tool_name"] = tool_call.function.name
        state["tool_args"] = json.loads(tool_call.function.arguments)
        state["next"] = "tool"
    else:
        state["next"] = "final"

    return state


def tool(state: dict) -> dict:
    tool_name = state["tool_name"]
    args = state["tool_args"]

    result = tools[tool_name]["function"](**args)

    # Přidej výstup jako zprávu od toolu
    state["messages"].append({
        "role": "tool",
        "tool_call_id": state["tool_call_id"],
        "content": str(result)
    })

    state["next"] = "final"
    return state


def final(state: dict) -> dict:
    messages = state["messages"]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    content = response.choices[0].message.content
    print("AI odpověď:", content)
    return state


# ===== GRAF =====
builder = StateGraph(dict)

builder.add_node("planner", planner)
builder.add_node("tool", tool)
builder.add_node("final", final)

builder.set_entry_point("planner")

# místo podmínky použijeme switch logiku na základě `state["next"]`
builder.add_conditional_edges(
    "planner",
    lambda state: state["next"],
    {
        "tool": "tool",
        "final": "final"
    }
)
builder.add_edge("tool", "final")
builder.set_finish_point("final")

graph = builder.compile()


# ===== VSTUP =====
state = {
    "messages": [
        {"role": "system", "content": "Jsi pomocný agent, který fungule pomocí nástrojů jako jednoduchá kalkulačka."},
        {"role": "user", "content": "vyděl 10 a 0?"}
    ]
}

# ===== SPUŠTĚNÍ =====
graph.invoke(state)
