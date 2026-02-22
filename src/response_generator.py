import random

RESPONSES = {

    # 1️⃣ CANCEL ORDER
    "cancel_order": [
        "No worries — your order has been successfully canceled.",
        "I've taken care of that. The order is now canceled.",
        "Your cancellation request has been processed.",
        "Done! The order has been canceled as requested.",
        "The order is officially canceled.",
        "That’s been handled — your order is no longer active.",
        "Cancellation confirmed. You’ll receive a notification shortly.",
        "Everything’s sorted. The order has been successfully canceled."
    ],

    # 2️⃣ TRACK ORDER
    "track_order": [
        "You can track your order using the link sent to your email.",
        "Your order is currently in transit.",
        "I’ve located your shipment — it’s on the way.",
        "Your package is moving through the delivery network.",
        "Tracking details have been shared with you.",
        "Your order is actively being delivered.",
        "Everything looks good — your shipment is progressing.",
        "You can monitor delivery anytime using your tracking number."
    ],

    # 3️⃣ REFUND REQUEST
    "refund_request": [
        "Your refund request has been received and is being processed.",
        "I’ve initiated the refund process for you.",
        "The refund has been approved.",
        "Your request is under review.",
        "The refund has been logged in our system.",
        "Everything is in motion — you’ll see it reflected soon.",
        "Your refund request is successfully recorded.",
        "We’re processing your refund right away."
    ],

    # 4️⃣ CHANGE ORDER
    "change_order": [
        "Sure, let’s update your order details.",
        "I can help you modify the order.",
        "Your order can still be adjusted.",
        "No problem — we can make changes before it ships.",
        "Let’s get those updates applied.",
        "I’m ready to help you modify the order.",
        "We can update your order right away.",
        "Tell me the changes and I’ll handle it."
    ],

    # 5️⃣ GREETING
    "greeting": [
        "Hello! How can I assist you today?",
        "Hi there! What can I help you with?",
        "Welcome! How may I support you?",
        "Hey! I’m here to help.",
        "Good to hear from you.",
        "Hi! Let’s get this sorted out.",
        "Greetings! How can I make things easier?",
        "Hello! What can I do for you?"
    ],

    # 6️⃣ CHECK ORDER STATUS
    "check_order_status": [
        "Let me check the status of your order.",
        "Your order is currently being processed.",
        "I’ve pulled up your order details.",
        "Your order is progressing as expected.",
        "Everything looks on track.",
        "Your order is active and being handled.",
        "I can confirm your order is in progress.",
        "Your order status has been updated."
    ],

    # 7️⃣ DELIVERY ISSUE
    "delivery_issue": [
        "I’m sorry to hear about the delivery issue.",
        "I’ll investigate the shipment problem.",
        "Let’s resolve this quickly.",
        "I’m checking what happened with your delivery.",
        "We’ll get this sorted out immediately.",
        "I’m escalating this concern.",
        "Thanks for your patience.",
        "I’m reviewing the delivery status now."
    ],

    # 8️⃣ PAYMENT ISSUE
    "payment_issue": [
        "Let’s take care of the payment issue.",
        "Your payment didn’t go through properly.",
        "Let’s review the transaction details.",
        "I’m checking what went wrong.",
        "There was a payment processing error.",
        "We’ll resolve this quickly.",
        "I’ll guide you through the fix.",
        "Let me verify the transaction."
    ],

    # 9️⃣ ACCOUNT ISSUE
    "account_issue": [
        "I’m here to help with your account.",
        "Let’s review your account details.",
        "I understand you're facing an account issue.",
        "I’ll assist you right away.",
        "Let’s get your account back on track.",
        "I’m checking your account settings.",
        "We’ll sort this out immediately.",
        "Thanks for reaching out about your account."
    ],

    # 1️⃣0️⃣ SHIPPING COST
    "shipping_cost": [
        "Shipping costs depend on your location and order size.",
        "Let me check the shipping fee for you.",
        "Shipping charges are calculated at checkout.",
        "I can provide details on shipping rates.",
        "The shipping cost varies by delivery speed.",
        "Standard shipping fees apply to your order.",
        "Shipping rates are based on your address.",
        "I’ll help you understand the shipping charges."
    ],

    # 1️⃣1️⃣ SHIPPING ADDRESS
    "change_shipping_address": [
        "We can update your shipping address.",
        "Let me modify the delivery address.",
        "Your address can still be changed.",
        "I’ll update your shipping details.",
        "Let’s correct the address right away.",
        "Address update request received.",
        "We’ll make sure it goes to the right place.",
        "I’m updating your shipping information."
    ],

    # 1️⃣2️⃣ ORDER CONFIRMATION
    "order_confirmation": [
        "Your order has been successfully confirmed.",
        "Confirmation email has been sent.",
        "Your order is officially placed.",
        "Everything looks good — your order is confirmed.",
        "We’ve received your order.",
        "Order confirmation completed.",
        "Your purchase has been successfully recorded.",
        "You’ll receive confirmation shortly."
    ],

    # 1️⃣3️⃣ RETURN ITEM
    "return_item": [
        "I’ll guide you through the return process.",
        "You can return the item within the policy period.",
        "Let’s initiate your return request.",
        "Return instructions will be sent to you.",
        "We’ll process your return smoothly.",
        "I’m creating a return request now.",
        "Your return has been successfully logged.",
        "Please follow the return steps provided."
    ],

    # 1️⃣4️⃣ WARRANTY CLAIM
    "warranty_claim": [
        "Let’s review your warranty claim.",
        "I’ll check if your product is under warranty.",
        "Warranty request received.",
        "We’ll verify your warranty eligibility.",
        "I’m processing your warranty claim.",
        "Let’s initiate the warranty procedure.",
        "Warranty validation in progress.",
        "Your warranty request is being reviewed."
    ],

    # 1️⃣5️⃣ TECHNICAL SUPPORT
    "technical_support": [
        "I’m here to assist with the technical issue.",
        "Let’s troubleshoot this step by step.",
        "I’ll help resolve the technical problem.",
        "Thanks for reporting this issue.",
        "Let’s fix the technical glitch.",
        "I’m reviewing your technical concern.",
        "We’ll get this working properly.",
        "Technical assistance is underway."
    ],

    # 1️⃣6️⃣ PASSWORD RESET
    "password_reset": [
        "I’ll help you reset your password.",
        "Password reset instructions have been sent.",
        "Let’s recover your account access.",
        "You can reset your password securely.",
        "I’m initiating the password reset process.",
        "Follow the steps in your email to reset it.",
        "Your password reset request is confirmed.",
        "Access recovery instructions are on the way."
    ],

    # 1️⃣7️⃣ SUBSCRIPTION CANCEL
    "cancel_subscription": [
        "Your subscription has been successfully canceled.",
        "I’ve processed your subscription cancellation.",
        "Your plan is now inactive.",
        "Subscription termination confirmed.",
        "You won’t be charged further.",
        "The cancellation is complete.",
        "Subscription has been ended.",
        "Everything is finalized regarding your subscription."
    ],

    # 1️⃣8️⃣ SUBSCRIPTION UPGRADE
    "upgrade_subscription": [
        "Let’s upgrade your subscription plan.",
        "Your plan can be upgraded instantly.",
        "I’ll help you switch to a higher tier.",
        "Upgrade request received.",
        "Your subscription upgrade is in progress.",
        "Let’s enhance your plan benefits.",
        "You’re eligible for an upgrade.",
        "Upgrade completed successfully."
    ],

    # 1️⃣9️⃣ DISCOUNT INQUIRY
    "discount_inquiry": [
        "Let me check available discounts for you.",
        "We currently have promotional offers available.",
        "I’ll verify if you’re eligible for discounts.",
        "Special deals may apply to your order.",
        "Discount information is available at checkout.",
        "We frequently run limited-time offers.",
        "Let’s explore current promotions.",
        "I’ll share any applicable discounts."
    ],

    # 2️⃣0️⃣ PRODUCT INQUIRY
    "product_inquiry": [
        "I’ll provide details about the product.",
        "Let me share more information about that item.",
        "Here’s what you need to know about the product.",
        "I’m pulling up product specifications.",
        "Product details are available now.",
        "Let’s review the product features.",
        "I can help you compare options.",
        "Here’s more information about the item."
    ],

    # 2️⃣1️⃣ OUT OF STOCK
    "out_of_stock": [
        "The item is currently out of stock.",
        "This product is temporarily unavailable.",
        "We’re expecting new inventory soon.",
        "Stock levels are currently depleted.",
        "Please check back later for availability.",
        "Restocking is in progress.",
        "We’ll notify you once it’s back.",
        "The item will be restocked shortly."
    ],

    # 2️⃣2️⃣ LATE DELIVERY
    "late_delivery": [
        "I apologize for the delivery delay.",
        "Your shipment is slightly delayed.",
        "We’re working to deliver it soon.",
        "Unexpected delays occurred.",
        "Thank you for your patience.",
        "We’re monitoring the delayed shipment.",
        "Delivery will be completed shortly.",
        "We’re expediting the process."
    ],

    # 2️⃣3️⃣ DAMAGED ITEM
    "damaged_item": [
        "I’m sorry the item arrived damaged.",
        "Let’s arrange a replacement.",
        "We’ll resolve this immediately.",
        "Please share details about the damage.",
        "Replacement process has started.",
        "I’m logging the damage report.",
        "We’ll fix this quickly.",
        "Thank you for reporting the issue."
    ],

    # 2️⃣4️⃣ WRONG ITEM
    "wrong_item": [
        "It seems you received the wrong item.",
        "Let’s correct this mistake.",
        "I’ll arrange the correct shipment.",
        "We’ll fix the mix-up immediately.",
        "Return instructions will be sent.",
        "Replacement is being processed.",
        "Thanks for notifying us.",
        "We’ll ensure you get the right product."
    ],

    # 2️⃣5️⃣ CONTACT SUPPORT
    "contact_support": [
        "You can reach our support team anytime.",
        "Our support team is available 24/7.",
        "I’ll connect you with a representative.",
        "Support contact details are available.",
        "We’re here to help further.",
        "You can escalate this to our team.",
        "Our experts will assist you.",
        "Let me provide support options."
    ],

    # 2️⃣6️⃣ FEEDBACK
    "feedback": [
        "We appreciate your feedback.",
        "Thank you for sharing your thoughts.",
        "Your feedback helps us improve.",
        "We value your input.",
        "Thanks for taking the time to respond.",
        "Your suggestions are important to us.",
        "We’re grateful for your feedback.",
        "We’ll use your feedback to improve."
    ],

    # 2️⃣7️⃣ GOODBYE
    "goodbye": [
        "Thank you for contacting us.",
        "Have a wonderful day!",
        "We appreciate your time.",
        "Feel free to reach out anytime.",
        "Goodbye and take care!",
        "Thanks for choosing us.",
        "We’re always here to help.",
        "Have a great day ahead!"
    ],
}


def generate_response(intent: str) -> str:
    if intent not in RESPONSES:
        return "I’m not fully certain about your request yet. Could you clarify?"
    return random.choice(RESPONSES[intent])


if __name__ == "__main__":
    while True:
        user_intent = input("Enter intent: ")
        print(generate_response(user_intent))