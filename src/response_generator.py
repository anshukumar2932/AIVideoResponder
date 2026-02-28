import random

RESPONSES = {

    #  CANCEL ORDER
    "cancel_order": [
        "Your order has been successfully canceled.",
        "I've processed the cancellation for you.",
        "The order is now canceled.",
        "Cancellation confirmed. You’ll receive an email shortly."
    ],

    #  CHANGE ORDER
    "change_order": [
        "Sure, I can help modify your order.",
        "Let’s update your order details.",
        "Your order can still be adjusted.",
        "Tell me what changes you'd like to make."
    ],

    #  CHANGE SHIPPING ADDRESS
    "change_shipping_address": [
        "I can help update your shipping address.",
        "Let’s modify the delivery address.",
        "Your shipping address can be updated.",
        "Please provide the new address details."
    ],

    #  CHECK CANCELLATION FEE
    "check_cancellation_fee": [
        "Let me check if any cancellation fee applies.",
        "I’ll verify the cancellation charges for you.",
        "Cancellation fees depend on the order status.",
        "I’m reviewing the fee details now."
    ],

    #  CHECK INVOICE
    "check_invoice": [
        "Let me check your invoice details.",
        "I’ll retrieve the invoice information.",
        "Your invoice details are being reviewed.",
        "I’m checking your billing information."
    ],

    #  CHECK PAYMENT METHODS
    "check_payment_methods": [
        "We accept multiple payment methods including card and online banking.",
        "Let me share the available payment options.",
        "You can pay using credit, debit, or supported digital methods.",
        "Here are the supported payment methods."
    ],

    #  CHECK REFUND POLICY
    "check_refund_policy": [
        "Let me explain our refund policy.",
        "Refunds are processed based on our policy terms.",
        "I’ll provide details about the refund guidelines.",
        "Here’s how our refund policy works."
    ],

    #  COMPLAINT
    "complaint": [
        "I’m sorry to hear about your experience.",
        "Let me help resolve your concern.",
        "I understand your frustration.",
        "I’ll escalate this issue immediately."
    ],

    #  CONTACT CUSTOMER SERVICE
    "contact_customer_service": [
        "You can reach our customer service team anytime.",
        "I’ll provide the contact details for support.",
        "Our support team is available 24/7.",
        "Let me guide you to customer service."
    ],

    # CONTACT HUMAN AGENT
    "contact_human_agent": [
        "I’ll connect you with a human representative.",
        "Please hold while I transfer you to an agent.",
        "A live agent will assist you shortly.",
        "Let me escalate this to a human support agent."
    ],

    #  CREATE ACCOUNT
    "create_account": [
        "I can help you create a new account.",
        "Let’s get your account set up.",
        "I’ll guide you through the registration process.",
        "Creating an account is quick and simple."
    ],

    #  DELETE ACCOUNT
    "delete_account": [
        "I can assist with deleting your account.",
        "Let me help you close your account.",
        "Account deletion request received.",
        "I’ll guide you through the account removal process."
    ],

    #  DELIVERY OPTIONS
    "delivery_options": [
        "We offer multiple delivery options.",
        "Let me explain the available shipping methods.",
        "You can choose from standard or express delivery.",
        "Here are the delivery options available."
    ],

    #  DELIVERY PERIOD
    "delivery_period": [
        "Delivery time depends on your location.",
        "Standard delivery usually takes a few business days.",
        "Let me check the estimated delivery time.",
        "Your shipment timeline is being reviewed."
    ],

    #  EDIT ACCOUNT
    "edit_account": [
        "I can help update your account details.",
        "Let’s modify your account information.",
        "Your account settings can be updated.",
        "Tell me what you'd like to change."
    ],

    #  GET INVOICE
    "get_invoice": [
        "I’ll retrieve your invoice.",
        "Your invoice is being prepared.",
        "Let me generate the invoice for you.",
        "Invoice details are on the way."
    ],

    #  GET REFUND
    "get_refund": [
        "I’ll initiate your refund request.",
        "Your refund is being processed.",
        "Refund request received.",
        "Let me help you with the refund procedure."
    ],

    #  NEWSLETTER SUBSCRIPTION
    "newsletter_subscription": [
        "Your newsletter subscription has been updated.",
        "I’ve processed your subscription request.",
        "Newsletter preferences have been changed.",
        "Your subscription status has been updated."
    ],

    #  PAYMENT ISSUE
    "payment_issue": [
        "I’m checking the payment issue.",
        "There seems to be a payment processing error.",
        "Let me review the transaction details.",
        "I’ll help resolve the payment problem."
    ],

    #  PLACE ORDER
    "place_order": [
        "I can help you place a new order.",
        "Let’s proceed with your purchase.",
        "Your order is being created.",
        "I’ll guide you through placing the order."
    ],

    #  RECOVER PASSWORD
    "recover_password": [
        "I’ll help you recover your password.",
        "Password recovery instructions have been sent.",
        "Let’s reset your password securely.",
        "Follow the steps in your email to recover access."
    ],

    #  REGISTRATION PROBLEMS
    "registration_problems": [
        "I’m sorry you’re facing registration issues.",
        "Let me help fix the sign-up problem.",
        "I’ll guide you through resolving this.",
        "Let’s troubleshoot the registration issue."
    ],

    #  TRACK REFUND
    "track_refund": [
        "Let me check the status of your refund.",
        "Your refund is currently being processed.",
        "I’m tracking your refund progress.",
        "Here’s the latest update on your refund."
    ],
    # TRACK ORDER
    "track_order": [
        "Let me check the current status of your order for you.",
        "Your order is currently in transit and on its way.",
        "I’ve located your shipment — it’s progressing through the delivery process.",
        "Your package has been dispatched and is moving toward its destination.",
        "Here’s the latest update: your order is actively being processed for delivery.",
        "Your shipment is on schedule and moving through our logistics network.",
        "I’m tracking your order now — it’s currently en route.",
        "Everything looks good — your order is advancing toward delivery."
    ],

    # 🔹 UNCERTAIN (confidence fallback)
    "uncertain": [
        "I’m not fully certain about your request yet. Could you clarify?",
        "Could you please rephrase that?",
        "I want to make sure I understand correctly — can you clarify?"
    ]
}


def generate_response(intent: str) -> str:
    if intent not in RESPONSES:
        print(f"[WARNING] Missing response key for intent: {intent}")
        return random.choice(RESPONSES["uncertain"])
    return random.choice(RESPONSES[intent])


if __name__ == "__main__":
    while True:
        user_intent = input("Enter intent: ")
        print(generate_response(user_intent))