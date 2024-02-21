import os
from typing import List

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from salesgpt.agents import SalesGPT
from salesgpt.salesgptapi import SalesGPTAPI

app = FastAPI()

GPT_MODEL = "gpt-3.5-turbo-0613"
# GPT_MODEL_16K = "gpt-3.5-turbo-16k-0613"

# LangSmith settings section, set TRACING_V2 to "true" to enable it
# or leave it as it is, if you don't need tracing (more info in README)
os.environ["LANGCHAIN_TRACING_V2"] = "True"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "ls__08a83a8794fa4314a301155bb79a0d15"
os.environ["LANGCHAIN_PROJECT"] = "default"  # insert you project name here

USE_TOOLS = True

@app.get("/")
async def get_index():
    return FileResponse("static/index.html")


class MessageList(BaseModel):
    conversation_history: List[str]
    human_say: str


@app.post("/chat")
async def chat_with_sales_agent(req: MessageList):
    sales_api = SalesGPTAPI(
        config_path="examples/example_agent_perfil.json", verbose=True
    )
    name, reply = sales_api.do(req.conversation_history, req.human_say)
    res = {"name": name, "say": reply}
    return res


def _set_env():
    with open(".env", "r") as f:
        env_file = f.readlines()
    envs_dict = {
        key.strip("'"): value.strip("\n")
        for key, value in [(i.split("=")) for i in env_file]
    }
    os.environ["OPENAI_API_KEY"] = "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"


if __name__ == "__main__":
    _set_env()
    uvicorn.run(app, host="127.0.0.1", port=8000)