from fastapi import FastAPI, Depends, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# FastAPI-App 
app = FastAPI()

# CORS aktivieren (damit React-Frontend auf Port 5173 zugreifen darf)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", "http://127.0.0.1:5173",
        "http://localhost:8080", "http://127.0.0.1:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Datenmodell für Chat-Eingaben


class UserMessage(BaseModel):
    text: str

# Auth-Stub (prüft nur, ob irgendein Token im Header mitkommt)


def require_auth(authorization: str | None = Header(default=None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

# Health-Check (für Monitoring)


@app.get("/health")
def health():
    return {"status": "ok"}

# Version-Info


@app.get("/version")
def version():
    return {"app": "genai-demo", "version": "0.1.0", "mode": "fallback"}

# Chat-Endpoint (einfacher Echo-/Demo-Handler)


@app.post("/chat", dependencies=[Depends(require_auth)])
def chat(msg: UserMessage):
    user_text = msg.text.strip()
    if not user_text:
        raise HTTPException(status_code=400, detail="Empty message")
    # Demo-Antwort – hier könnte ein LLM-Aufruf erfolgen
    assistant_reply = f"Echo: {user_text}"
    return {"reply": assistant_reply}
