from fastapi import FastAPI
from pydantic import BaseModel
import os
from openai import OpenAI
from knowledge_base import carregar_base

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="WEG Soft-Starter Chatbot")

base_weg = carregar_base()

class Pergunta(BaseModel):
    pergunta: str

@app.post("/chat")
def chat(pergunta: Pergunta):

    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Você é um assistente técnico especialista em Soft-Starter WEG SSW-07. "
                    "Use SOMENTE as informações da base técnica abaixo.\n\n"
                    f"{base_weg}"
                )
            },
            {
                "role": "user",
                "content": pergunta.pergunta
            }
        ]
    )

    return {"resposta": resposta.choices[0].message.content}

