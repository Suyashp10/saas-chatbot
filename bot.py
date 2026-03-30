from data import FAQs, create_ticket, find_ticket, escalate

# intent keywords

# INTENT_KEYWORDS = {
#     "greeting": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "howdy", "yo"],
#     "create_ticket":  ["raise ticket", "create ticket", "open ticket", "submit ticket", "new ticket", "log issue"],
#     "track_ticket":   ["track ticket", "ticket status", "my ticket", "check ticket", "ticket id"],
#     "escalate":       ["human", "agent", "real person", "talk to someone", "live support", "speak to"],
#     "goodbye":        ["bye", "goodbye", "exit", "quit", "thanks bye", "see you"],
# }

INTENT_KEYWORDS = {
    "greeting":      ["hi", "hello", "hey", "howdy", "greetings", "sup",
                      "good morning", "good evening", "good afternoon",
                      "what's up", "hiya"],

    "create_ticket": ["raise", "create", "open", "submit", "log", "file",
                      "report", "register", "new", "start"],

    "track_ticket":  ["track", "status", "check", "find", "lookup", "where",
                      "follow", "update", "progress", "see"],

    "escalate":      ["human", "agent", "person", "representative", "staff",
                      "manager", "supervisor", "operator"],

    "goodbye":       ["bye", "goodbye", "exit", "quit", "cya", "later",
                      "done", "that's all", "all done", "no more"],
}

INTENT_CONTEXT = {
    "create_ticket": ["ticket", "issue", "problem", "bug", "error", "case",
                      "complaint", "request", "incident", "support", "help"],

    "track_ticket":  ["ticket", "issue", "case", "request", "id", "number",
                      "reference", "complaint"],

    "escalate":      ["speak", "talk", "chat", "call", "contact", "reach",
                      "connect", "need", "want", "transfer"],
}

PHRASE_INTENTS = {
    "create_ticket": ["i have a bug", "something is broken", "app crashed",
                      "not working", "having an issue", "facing a problem",
                      "need help with", "i found a bug"],

    "escalate":      ["i'm frustrated", "im frustrated", "this is urgent",
                      "nobody is helping", "need to speak to someone",
                      "let me talk to", "connect me to", "transfer me"],

    "goodbye":       ["thanks bye", "see you", "that'll be all",
                      "have a good", "talk later", "no more questions"],
}

def detect_intent(message):
    msg = message.lower().strip()
    tokens = set(msg.split())

    for intent, phrases in PHRASE_INTENTS.items():
        for phrase in phrases:
            if phrase in msg:
                return intent

    for intent, keywords in INTENT_KEYWORDS.items():
        keyword_hit = any(kw in tokens for kw in keywords)

        if keyword_hit:
            if intent in INTENT_CONTEXT:
                context_hit = any(ctx in tokens for ctx in INTENT_CONTEXT[intent])
                if context_hit:
                    return intent
            else:
                return intent

    return "faq"

def match_faq(message):
    message = message.lower().strip()
    best_match = None
    best_score = 0

    for faq in FAQs:
        score = 0
        for keyword in faq["keywords"]:
            if keyword in message:
                score += 1
        if score > best_score:
            best_score = score
            best_match = faq
    if best_match and best_score > 0:
        return best_match["answer"]
    
    return None

#session state

sessions = {}
def get_session(session_id):
    if session_id not in sessions:
        sessions[session_id] = {
            "state": None,
            "user_name": None,
            "issue": None
        }
    return sessions[session_id]

def clear_session(session_id):
    if session_id in sessions:
        sessions[session_id] = {
            "state": None,
            "user_name": None,
            "issue": None
        }

#response handler
def get_response(session_id, message):
    session = get_session(session_id)
    msg = message.strip()

    if session["state"] == "awaiting_name":
        session["user_name"] = msg
        session["state"] = "awaiting_issue"
        return f"Thanks {session['user_name']}! Can you please describe the issue you're facing?"
    
    if session["state"] == "awaiting_issue":
        session["issue"] = msg
        ticket = create_ticket(session["user_name"], session["issue"])
        clear_session(session_id)
        return (
            f"Ticket created successfully!\n"
            f"Ticket ID: {ticket['id']}\n"
            f"We'll get back to you shortly. Is there anything else I can help you with?"
        )

    intent = detect_intent(msg)

    if intent == "greeting":
        return (
            "Hello! I'm SaaS Support Bot.\n"
            "I can help you with FAQs, raise a support ticket, "
            "track an existing ticket, or connect you with a human agent.\n"
            "How can I help you today?"
        )
    
    if intent == "create_ticket":
        session["state"] = "awaiting_name"
        return "Sure, I can help you with that. What is your name?"

    if intent == "track_ticket":
        return "Please provide your ticket ID to check the status."

    if intent == "escalate":
        return escalate()

    if intent == "goodbye":
        return "Goodbye! If you have any more questions in the future, feel free to ask. Have a great day!"

    if intent == "faq":
        words = msg.upper().split()  # uppercase the whole message first
    for word in words:
        if len(word) == 8 and word.isalnum() and any(c.isdigit() for c in word):
            ticket = find_ticket(word)
            if ticket:
                return (
                    f"Ticket Found!\n"
                    f"ID: {ticket['id']}\n"
                    f"Issue: {ticket['issue']}\n"
                    f"Status: {ticket['status'].upper()}\n"
                    f"Raised by: {ticket['user_name']}\n"
                    f"Created: {ticket['created_at']}"
                )
            else:
                return f"No ticket found with ID '{word}'. Please check and try again."
            answer = match_faq(msg)
            if answer:
                return answer
        
        return (
            "I'm not sure I understood that.\n"
            "I can help you with:\n"
            "• FAQs (billing, account, technical issues)\n"
            "• Raise a support ticket\n"
            "• Track an existing ticket\n"
            "• Connect you with a human agent"
        )