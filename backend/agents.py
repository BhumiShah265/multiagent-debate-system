from sqlalchemy.orm import Mapped
import os
from dotenv import load_dotenv
import json
from openai import OpenAI
load_dotenv()
AVAILABLE_MODELS = {
    "gpt-5.5-pro": "openai/gpt-5.5-pro",
    "claude-5-sonnet": "anthropic/claude-fable-5",
    "gemini-pro-latest": "google/gemini-pro-latest",
    "deepseek-v4-pro": "deepseek/deepseek-v4-pro",
    "grok-4.20": "x-ai/grok-4.20-multi-agent",
    "qwen-3.7-plus": "qwen/qwen3.7-plus",
    "gemini-3.1-flash-lite": "google/gemini-3.1-flash-lite-image",
    "llama-nemotron-free": "nvidia/llama-nemotron-rerank-vl-1b-v2:free"
}
BASE_URL = "https://openrouter.ai/models"
RETRIEVE = os.get_env("OPENROUTER_API_KEY")

client = OpenAI(BASE_URL,RETRIEVE)

def call_llm(model_id, system_prompt, user_prompt, response_format=None):
    full_model_name = AVAILABLE_MODELS.get(model_id,model_id)
    messages = [
        {"role":"system","content":"system_prompt"},
        {"role":"user","content":"user_prompt"}
    ]
    try:
        extra_headers = {
            "HTTP-Referer":os.getenv("HTTP-Referer"),
            "X-Title":"Multi-Agent Debate System"
        }
        kwargs ={
            "model":full_model_name,
            "messages":messages,
            "extra_headers":extra_headers
        }
        if response_format:
            kwargs["response_format"] = response_format
        response = client.chat.completions.create(**kwargs)
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling model {full_model_name}: {e}")
        return f"Error: Failed to generate response from {model_id}."
    
def parse_referee_json(raw_text: str) -> dict:
    try:
        # Clean up any potential markdown formatting
        cleaned_text = raw_text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text.split("```json")[1].split("```")[0].strip()
        elif cleaned_text.startswith("```"):
            cleaned_text = cleaned_text.split("```")[1].split("```")[0].strip()
            
        return json.loads(cleaned_text)
    except Exception as e:
        print(f"Failed to parse JSON from referee: {e}\nRaw output was: {raw_text}")
        # Return a fallback structure so the system doesn't crash
        return {
            "scores": {
                "optimist": {"quality": 5.0, "persuasiveness": 5.0, "consensus": 0.0},
                "skeptic": {"quality": 5.0, "persuasiveness": 5.0, "consensus": 0.0},
                "realist": {"quality": 5.0, "persuasiveness": 5.0, "consensus": 0.0}
            },
            "consensus_score": 50.0,
            "summary": "Failed to parse referee scores. Default values applied."
        }