import os
import json 
import uuid
from datetime import datetime


# load faqs
FAQ_PATH = "knowledge/faqs.json"
def load_faqs():
    with open(FAQ_PATH, "r") as f:
        faqs = json.load(f)
    return faqs

FAQs = load_faqs()

# ticket manager
TICKETS_PATH = "tickets/tickets.json"
def load_tickets():
    if not os.path.exists(TICKETS_PATH):
        return []
    with open(TICKETS_PATH, "r") as f:
        tickets = json.load(f)
    return tickets

def save_tickets(tickets):
    with open(TICKETS_PATH, "w") as f:
        json.dump(tickets, f, indent=2)

def create_ticket(user_name, issue): 
    tickets = load_tickets()
    ticket = {
        "id": str(uuid.uuid4())[:8].upper(),
        "user_name": user_name,
        "issue": issue,
        "status": "open",
        "created_at": datetime.now().isoformat()
    }
    tickets.append(ticket)
    save_tickets(tickets)
    return ticket

def find_ticket(ticket_id):
    tickets = load_tickets()
    for ticket in tickets:
        if(ticket['id'] == ticket_id):
            return ticket
        return None

# escalataion manager

SUPPORT_EMAIL = "support@saas.com"
SUPPORT_HOURS = "Monday-Friday 9AM - 6PM UTC"

def escalate():
    return (
        f"I'm connecting you with a human agent...\n"
        f"Email us at: {SUPPORT_EMAIL}\n"
        f"Support hours: {SUPPORT_HOURS}\n"
        f"Or raise a ticket and we'll get back to you within 24 hours."
    )
