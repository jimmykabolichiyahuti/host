from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import stripe
load_dotenv()
stripe.api_key = os.getenv("stripe_secretkey")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://whitecapsclo.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():
    return {"status": "ok"}
class PaymentRequest(BaseModel):
    amount:int
@app.post("/create-payment-intent")
def create_payment_intent(gg: PaymentRequest):
    try:
        intent = stripe.PaymentIntent.create(
            amount=gg.amount,
            currency="usd",
            automatic_payment_methods={"enabled": True},
        )
        return {"client_secret": intent.client_secret}
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))
