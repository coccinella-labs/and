from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = FastAPI()

# Load the model and tokenizer
model = AutoModelForCausalLM.from_pretrained("bniladridas/conversational-ai-fine-tuned")
tokenizer = AutoTokenizer.from_pretrained("bniladridas/conversational-ai-fine-tuned")


class ChatRequest(BaseModel):
    input_text: str


@app.post("/chat")
async def generate_response(chat_request: ChatRequest):
    try:
        # Tokenize input
        inputs = tokenizer(chat_request.input_text, return_tensors="pt")

        # Generate response
        outputs = model.generate(**inputs)

        # Decode and return the response
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status")
async def status():
    return {"status": "API is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
