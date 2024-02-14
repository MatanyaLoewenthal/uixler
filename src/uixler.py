from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import requests
import uvicorn
import httpx

# import openai
# from groqcloud import Groqcloud

# import groq
from groq.cloud.core import ChatCompletion

app = FastAPI()


@app.get("/{path:path}", response_class=HTMLResponse)
async def generate_site(
    base_site: str = "https://news.ycombinator.com/",
    prompt: str = "make the site top bar green and the text size 30",
    path: str = "",
):
    with httpx.Client() as client:
        proxy = client.get(f"{base_site}{path}")
        html_content = proxy.text
    try:

        with ChatCompletion("mixtral-8x7b-32768") as chat:
            full_prompt = f"""
            [INST] You are a helpful website enhancing assistant. Your task is to generate valid HTML that enhances the website according to the prompt. If any part of the website_html is unclear or is not relevant to the prompt, return that html as is:
            prompt: {prompt}
            website_html: {html_content}
            Just generate the entire website HTML with the enhancements, without explanations:
            [/INST]
            """
            response, _, _ = chat.send_chat(full_prompt)

        # print(response)
        return response
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


def start():
    uvicorn.run("uixler:app", host="0.0.0.0", port=8000, reload=True)
