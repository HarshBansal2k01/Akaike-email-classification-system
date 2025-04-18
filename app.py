# app.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
from utils import mask_pii
from api import predict_category

app = FastAPI()

class EmailRequest(BaseModel):
    input_email_body: str

@app.post("/classify/")
def classify_email(req: EmailRequest):
    original_text = req.input_email_body
    masked_text, entities = mask_pii(original_text)
    predicted_category = predict_category(masked_text)

    return {
        "input_email_body": original_text,
        "list_of_masked_entities": entities,
        "masked_email": masked_text,
        "category_of_the_email": predicted_category
    }
