import os
import stripe
from flask import Blueprint, request, jsonify

from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

stripe_bp = Blueprint("stripe", __name__)


@stripe_bp.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")
    print("Request received:", payload)
    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=sig_header, secret=endpoint_secret
        )
    except ValueError:
        print("Invalid payload")
        return jsonify({"error": "Invalid payload"}), 400
    except stripe.error.SignatureVerificationError:
        print("Invalid signature")
        return jsonify({"error": "Invalid signature"}), 400

    # Handle specific event types
    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        # Example: update payment status in DB
        order_id = intent["metadata"].get("order_id")
        print("PaymentIntent succeeded for order:", order_id)
        print("PaymentIntent succeeded:", intent["id"])

    elif event["type"] == "payment_link.created":
        session = event["data"]["object"]
        print("Checkout session created:", session["id"])
        print("Checkout URL:", session.get("url", "N/A"))
    elif event["type"] == "payment_intent.payment_failed":
        intent = event["data"]["object"]
        print("PaymentIntent failed:", intent["id"])
    elif event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        print("Checkout session completed:", session["id"])
    else:
        print("Unhandled event type", event["type"])

    return jsonify({"status": "received"}), 200
