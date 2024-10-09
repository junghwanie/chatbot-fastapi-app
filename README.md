## Chatbot Implementations with FastAPI and WebSockets


This repository provides chatbot application designed using FastAPI and WebSockets and serves OpenAI's gpt-3.5-turbo.

### Technology used
Here are a few methods of chatbot implementations:

-  **Static Chatbot** \
  Interactive conversations are possible through a chatbot using LLM built with FastAPI.

-  **Context aware chatbot** \
  A chatbot that remembers previous conversations and provides responses accordingly.</br>
  Enables appropriate conversation through system prompt.

-  **Chatbot with templates** \
  Jinja's include allows us to import another HTML from on HTML.

-  **Chat with Websockets** \
  Real-time streaming capabilities using WebSockets.


### Websockets used
Future developed.


### Running locally
To run a static chatbot:
```shell
cd static-chatbot
pip install -r requirements.txt
```

```shell
# Run directly with uvicorn module
uvicorn main:app --reload
```


### Contributing
Planning to add more chatbot examples over time. PRs are welcome.