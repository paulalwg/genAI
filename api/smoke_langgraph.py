from langgraph.graph import StateGraph, END

# Wir definieren einen sehr einfachen State als dict
def classify(state: dict) -> dict:
    text = state.get("input", "")
    intent = "greeting" if "hallo" in text.lower() or "hi" in text.lower() else "other"
    return {"intent": intent}

def respond(state: dict) -> dict:
    intent = state.get("intent", "other")
    text = state.get("input", "")
    out = "Hi 👋, wie kann ich helfen?" if intent == "greeting" else f"Echo: {text}"
    return {"output": out}

graph = StateGraph(dict)
graph.add_node("classify", classify)
graph.add_node("respond", respond)
graph.set_entry_point("classify")
graph.add_edge("classify", "respond")
graph.add_edge("respond", END)

app = graph.compile()

print(app.invoke({"input": "Hallo Welt"})["output"])
print(app.invoke({"input": "Sag mir was über Docker"})["output"])
