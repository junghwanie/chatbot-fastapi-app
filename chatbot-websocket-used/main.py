import openai
import os
from fastapi import FastAPI, Form, Request, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Annotated
from dotenv import load_dotenv


# https://1ar.io/p/how-to-understand-that-openai-api-streaming-response-is-done/
# https://github.com/codingwithroby/the-complete-chatbot-bootcamp


load_dotenv()

openai_key = os.getenv("OPEN_API_KEY")

app = FastAPI()
templates = Jinja2Templates(directory="templates")

chat_responses = []

@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse(
        "home.html", {"request": request, "chat_responses": chat_responses}
    )

chat_log = [{"role": "system",
             "content": "You are a Python tutor AI, completely dedicated to teach users how \
                to learn Python from scratch. Please provide clear instructions on Python \
                concepts, best practices and syntax. Help create a path of leaning for \
                users to be able to create real life, production ready Python applications"}]


@app.websocket("/ws")
async def chat(websocket: WebSocket):

    await websocket.accept()

    while True:
        user_input = await websocket.receive_text()
        chat_log.append({"role": "user", "content": user_input})
        chat_responses.append(user_input)

        openai.api_key = openai_key
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=chat_log,
            temperature=0.6,
            stream=True,
        )

        ai_response = ""

        for chunk in response:
            # Error: content <- chunk.choices[0].delta.content is not None?
            if chunk.choices[0].finish_reason is None:
                ai_response += chunk.choices[0].delta.content
                await websocket.send_text(chunk.choices[0].delta.content)
        chat_responses.append(ai_response)


@app.post("/", response_class=HTMLResponse)
async def chat(request: Request, user_input: Annotated[str, Form()]):

    chat_log.append({"role": "user", "content": user_input})
    chat_responses.append(user_input)

    openai.api_key = openai_key
    response = openai.ChatCompletion.create(
        model="gpt-4", messages=chat_log, temperature=0.6
    )

    bot_response = response.choices[0].message.content
    chat_log.append({"role": "assistant", "content": bot_response})
    chat_responses.append(bot_response)

    return templates.TemplateResponse(
        "home.html", {"request": request, "chat_responses": chat_responses}
    )