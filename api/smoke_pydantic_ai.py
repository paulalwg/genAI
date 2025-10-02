from pydantic import BaseModel

class Answer(BaseModel):
    answer: str

try:
    # Mit Key/Quota: echte strukturierte Antwort
    from pydantic_ai import Agent, Model
    agent = Agent(Model("gpt-4o-mini"), output_model=Answer)
    result = agent.run("Antworte als JSON-Feld 'answer' mit 'Hallo Welt'.")
    print("Pydantic-AI:", result.answer)
except Exception as e:
    # Fallback: wir validieren lokale Daten gegen das Schema
    raw = {"answer": "Hallo Welt (Fallback)"}
    obj = Answer(**raw)
    print("Pydantic-AI Fallback:", obj.answer, f"[Grund: {type(e).__name__}]")
