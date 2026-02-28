#!/usr/bin/env python3
"""
Test script for SQLite Customer Support Database
"""

import sqlite3
from datetime import datetime

def connect_db():
    """Connect to the SQLite database"""
    return sqlite3.connect('customer_support.db')

def test_queries():
    """Run test queries on the database"""
    conn = connect_db()
    cursor = conn.cursor()
    
    print("=" * 70)
    print("CUSTOMER SUPPORT CHATBOT DATABASE - TEST QUERIES")
    print("=" * 70)
    
    # Query 1: All tickets
    print("\n1. ALL SUPPORT TICKETS:")
    print("-" * 70)
    cursor.execute("""
        SELECT t.ticket_id, c.full_name, t.subject, t.status, t.chatbot_handled
        FROM customer_support_tickets t
        JOIN customers c ON t.customer_id = c.customer_id
        ORDER BY t.ticket_id
    """)
    for row in cursor.fetchall():
        handled = "✓ Bot" if row[4] else "✗ Human"
        print(f"#{row[0]} | {row[1]:15} | {row[2]:30} | {row[3]:12} | {handled}")
    
    # Query 2: Chatbot performance
    print("\n2. CHATBOT PERFORMANCE SUMMARY:")
    print("-" * 70)
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(chatbot_handled) as resolved_by_bot,
            ROUND(AVG(chatbot_confidence_score), 2) as avg_confidence,
            ROUND(100.0 * SUM(chatbot_handled) / COUNT(*), 2) as success_rate
        FROM customer_support_tickets
    """)
    row = cursor.fetchall()[0]
    print(f"Total Tickets:        {row[0]}")
    print(f"Resolved by Chatbot:  {row[1]}")
    print(f"Avg Confidence:       {row[2]}%")
    print(f"Success Rate:         {row[3]}%")
    
    # Query 3: Tickets by category
    print("\n3. TICKETS BY CATEGORY:")
    print("-" * 70)
    cursor.execute("""
        SELECT issue_category, COUNT(*) as count, 
               ROUND(AVG(chatbot_confidence_score), 2) as avg_conf
        FROM customer_support_tickets
        GROUP BY issue_category
        ORDER BY count DESC
    """)
    for row in cursor.fetchall():
        print(f"{row[0]:15} | Count: {row[1]} | Avg Confidence: {row[2]}%")
    
    # Query 4: Customer sentiment
    print("\n4. CUSTOMER SENTIMENT ANALYSIS:")
    print("-" * 70)
    cursor.execute("""
        SELECT customer_sentiment, COUNT(*) as count,
               ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM customer_support_tickets), 2) as percentage
        FROM customer_support_tickets
        WHERE customer_sentiment IS NOT NULL
        GROUP BY customer_sentiment
    """)
    for row in cursor.fetchall():
        print(f"{row[0]:10} | Count: {row[1]} | Percentage: {row[2]}%")
    
    # Query 5: Conversation sample
    print("\n5. SAMPLE CONVERSATION (Ticket #1):")
    print("-" * 70)
    cursor.execute("""
        SELECT sender_type, message_text, intent_detected, confidence_score
        FROM chatbot_conversations
        WHERE ticket_id = 1
        ORDER BY message_id
    """)
    for row in cursor.fetchall():
        sender = f"[{row[0]}]"
        intent = f"({row[2]})" if row[2] else ""
        print(f"{sender:12} {row[1][:50]}... {intent}")
    
    # Query 6: Low confidence tickets
    print("\n6. LOW CONFIDENCE TICKETS (< 70%):")
    print("-" * 70)
    cursor.execute("""
        SELECT ticket_id, subject, chatbot_confidence_score, status
        FROM customer_support_tickets
        WHERE chatbot_confidence_score < 70
        ORDER BY chatbot_confidence_score ASC
    """)
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(f"#{row[0]} | {row[1]:35} | Confidence: {row[2]}% | {row[3]}")
    else:
        print("No low confidence tickets found.")
    
    conn.close()
    print("\n" + "=" * 70)

def create_new_ticket(customer_id, subject, description, category):
    """Example: Create a new support ticket"""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO customer_support_tickets 
        (customer_id, issue_category, subject, description, status, priority)
        VALUES (?, ?, ?, ?, 'Open', 'Medium')
    """, (customer_id, category, subject, description))
    
    ticket_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return ticket_id

def log_conversation(ticket_id, sender, message, intent=None, confidence=None):
    """Example: Log a conversation message"""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO chatbot_conversations 
        (ticket_id, sender_type, message_text, intent_detected, confidence_score)
        VALUES (?, ?, ?, ?, ?)
    """, (ticket_id, sender, message, intent, confidence))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    test_queries()
    
    # Example: Create a new ticket
    print("\nEXAMPLE: Creating a new ticket...")
    new_ticket_id = create_new_ticket(
        customer_id=1,
        subject="Product inquiry",
        description="What are the dimensions of product XYZ?",
        category="Product"
    )
    print(f"✓ Created ticket #{new_ticket_id}")
    
    # Example: Log a conversation
    log_conversation(
        ticket_id=new_ticket_id,
        sender="Customer",
        message="What are the dimensions of product XYZ?",
        intent="product_inquiry",
        confidence=88.5
    )
    print(f"✓ Logged conversation for ticket #{new_ticket_id}")
