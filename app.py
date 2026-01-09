from fastapi import FastAPI
from pydantic import BaseModel
import os
from openai import OpenAI
from knowledge_base import carregar_base

client = openai(api_key=os.getenv("OPENAI_API_KEY"))

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
from fastapi import Request
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse

@app.post("/whatsapp")
async def whatsapp(request: Request):
    form = await request.form()
    mensagem = form.get("Body")

    resposta_ai = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Você é um assistente técnico especialista em Soft-Starter WEG SSW-07. "
                    "Use SOMENTE a base técnica fornecida."
                )
            },
            {
                "role": "user",
                "content": mensagem
            }
        ]
    )

    resp = MessagingResponse()
    resp.message(resposta_ai.choices[0].message.content)

    return PlainTextResponse(str(resp))
    

