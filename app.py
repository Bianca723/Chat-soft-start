from fastapi import FastAPI
from pydantic import BaseModel
import os
from openai import OpenAI

# Inicializa a API da OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="WEG Soft-Starter Chatbot")

# Modelo de entrada
class Pergunta(BaseModel):
    pergunta: str

# Rota principal
@app.post("/chat")
def chat(pergunta: Pergunta):

    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Você é um assistente técnico especialista em Soft-Starter WEG SSW-07. "
                    "Responda de forma clara, técnica e objetiva. "
                    "Explique parâmetros, erros, alarmes e procedimentos de programação. "
                    "Sempre que possível, cite os parâmetros (ex: P102, P110)."
                )
            },
            {
                "role": "user",
                "content": pergunta.pergunta
            }
        ]
    )

    return {
        "resposta": resposta.choices[0].message.content
    }

# Rota de teste (opcional)
@app.get("/")
def root():
    return {"status": "Chatbot WEG Soft-Starter rodando com sucesso"}
