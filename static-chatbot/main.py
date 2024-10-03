import openai
import os
from fastapi import FastAPI, Form, Request
from typing import Annotated
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


load_dotenv()
OPENAI_KEY = os.getenv("OPEN_API_KEY")

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

chat_log = [{"role": "system",
             "content": "You are a Pytorch tutor AI, completely dedicated to teach users how \
                to learn Pytorch from scratch. Please provide clear instructions on Pytorch \
                concepts, best practices and syntax. Help create a path of leaning for \
                users to be able to create real life, production ready Pytorch applications"}]

chat_responses = []

@app.post("/", response_class=HTMLResponse)
async def chat(request: Request, user_input: Annotated[str, Form()]):

    chat_log.append({"role": "user", "content": user_input})
    chat_responses.append(user_input)

    openai.api_key = OPENAI_KEY
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = chat_log,
        temperature = 0.6,
    )

    bot_response = response.choices[0].message.content
    chat_log.append({"role": "assistant", "content": bot_response})
    chat_responses.append(bot_response)

    return templates.TemplateResponse("home.html", {"request": request, "chat_responses": chat_responses})