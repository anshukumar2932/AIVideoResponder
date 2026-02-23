# SQLite Database - Complete Guide

## 📦 What's Included

Your SQLite database is **ready to use** with:

- ✅ **customer_support.db** (72KB) - Fully populated database
- ✅ 5 customers with realistic profiles
- ✅ 5 orders in various states
- ✅ 5 support tickets (3 bot-resolved, 2 escalated)
- ✅ 15+ conversation messages with intent detection
- ✅ Performance metrics and analytics

## 🚀 Quick Start (3 Ways)

### 1. Command Line (Instant)

```bash
# View all tickets
sqlite3 database/customer_support.db "SELECT * FROM customer_support_tickets;"

# Check chatbot performance
sqlite3 database/customer_support.db "SELECT COUNT(*) as total, SUM(chatbot_handled) as bot_resolved FROM customer_support_tickets;"

# View customers
sqlite3 database/customer_support.db "SELECT * FROM customers;"
```

### 2. Python Script (Analytics)

```bash
cd database
python3 test_database.py
```

**Output includes:**
- All support tickets with status
- Chatbot performance summary
- Tickets by category
- Customer sentiment analysis
- Sample conversations
- Low confidence tickets

### 3. Web Viewer (Visual)

```bash
cd database
python3 view_database.py
```

Then open: **http://localhost:8000**

**Features:**
- Interactive ticket browser
- Real-time statistics dashboard
- Click tickets to view conversations
- Color-coded status and confidence levels

## 📊 Database Schema

### Tables Overview

| Table | Records | Purpose |
|-------|---------|---------|
| customer_support_tickets | 5 | Main ticket tracking |
| chatbot_conversations | 15 | Message logs with intents |
| customers | 5 | Customer profiles |
| orders | 5 | Order tracking |
| support_agents | 3 | Human agents |
| chatbot_metrics | 2 | Daily performance stats |

### Key Fields Explained

**customer_support_tickets:**
- `chatbot_handled` - 1 = bot resolved, 0 = needs human
- `chatbot_confidence_score` - AI confidence (0-100)
- `status` - Open, In Progress, Resolved, Escalated, Closed
- `priority` - Low, Medium, High, Urgent
- `customer_sentiment` - Positive, Neutral, Negative

**chatbot_conversations:**
- `sender_type` - Customer, Chatbot, or Agent
- `intent_detected` - track_order, password_reset, etc.
- `confidence_score` - Intent detection confidence

## 💡 Common Use Cases

### 1. Find All Open Tickets

```sql
SELECT ticket_id, subject, priority, created_at
FROM customer_support_tickets
WHERE status = 'Open'
ORDER BY priority DESC;
```

### 2. Chatbot Performance Report

```sql
SELECT 
    COUNT(*) as total_tickets,
    SUM(chatbot_handled) as resolved_by_bot,
    ROUND(100.0 * SUM(chatbot_handled) / COUNT(*), 2) as success_rate,
    ROUND(AVG(chatbot_confidence_score), 2) as avg_confidence
FROM customer_support_tickets;
```

### 3. Low Confidence Tickets (Need Review)

```sql
SELECT ticket_id, subject, chatbot_confidence_score, status
FROM customer_support_tickets
WHERE chatbot_confidence_score < 70
ORDER BY chatbot_confidence_score ASC;
```

### 4. View Full Conversation

```sql
SELECT 
    sender_type,
    message_text,
    intent_detected,
    confidence_score
FROM chatbot_conversations
WHERE ticket_id = 1
ORDER BY message_id;
```

### 5. Customer Ticket History

```sql
SELECT 
    t.ticket_id,
    t.subject,
    t.status,
    t.chatbot_handled,
    t.created_at
FROM customer_support_tickets t
JOIN customers c ON t.customer_id = c.customer_id
WHERE c.email = 'john.doe@email.com'
ORDER BY t.created_at DESC;
```

### 6. Most Common Intents

```sql
SELECT 
    intent_detected,
    COUNT(*) as frequency,
    ROUND(AVG(confidence_score), 2) as avg_confidence
FROM chatbot_conversations
WHERE intent_detected IS NOT NULL
GROUP BY intent_detected
ORDER BY frequency DESC;
```

### 7. Tickets by Category

```sql
SELECT 
    issue_category,
    COUNT(*) as count,
    SUM(chatbot_handled) as bot_resolved,
    ROUND(AVG(chatbot_confidence_score), 2) as avg_confidence
FROM customer_support_tickets
GROUP BY issue_category
ORDER BY count DESC;
```

### 8. Sentiment Analysis

```sql
SELECT 
    customer_sentiment,
    COUNT(*) as count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM customer_support_tickets), 2) as percentage
FROM customer_support_tickets
WHERE customer_sentiment IS NOT NULL
GROUP BY customer_sentiment;
```

## 🐍 Python Integration

### Basic Connection

```python
import sqlite3

# Connect to database
conn = sqlite3.connect('customer_support.db')
cursor = conn.cursor()

# Execute query
cursor.execute("SELECT * FROM customers")
customers = cursor.fetchall()

for customer in customers:
    print(customer)

conn.close()
```

### Create New Ticket

```python
def create_ticket(customer_id, category, subject, description):
    conn = sqlite3.connect('customer_support.db')
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

# Usage
new_ticket = create_ticket(1, 'Product', 'Question about item', 'What is the warranty?')
print(f"Created ticket #{new_ticket}")
```

### Log Conversation Message

```python
def log_message(ticket_id, sender, message, intent=None, confidence=None):
    conn = sqlite3.connect('customer_support.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO chatbot_conversations 
        (ticket_id, sender_type, message_text, intent_detected, confidence_score)
        VALUES (?, ?, ?, ?, ?)
    """, (ticket_id, sender, message, intent, confidence))
    
    conn.commit()
    conn.close()

# Usage
log_message(1, 'Customer', 'Hello, I need help', 'greeting', 95.0)
log_message(1, 'Chatbot', 'How can I assist you?', 'offer_help', 98.0)
```

### Update Ticket Status

```python
def resolve_ticket(ticket_id, resolution_notes):
    conn = sqlite3.connect('customer_support.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE customer_support_tickets 
        SET status = 'Resolved',
            resolved_at = datetime('now'),
            resolution_notes = ?
        WHERE ticket_id = ?
    """, (resolution_notes, ticket_id))
    
    conn.commit()
    conn.close()

# Usage
resolve_ticket(1, 'Issue resolved by chatbot')
```

### Escalate to Human

```python
def escalate_ticket(ticket_id, agent_id, priority='High'):
    conn = sqlite3.connect('customer_support.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE customer_support_tickets 
        SET status = 'Escalated',
            assigned_agent_id = ?,
            priority = ?
        WHERE ticket_id = ?
    """, (agent_id, priority, ticket_id))
    
    conn.commit()
    conn.close()

# Usage
escalate_ticket(2, agent_id=1, priority='Urgent')
```

## 🔧 Maintenance

### Backup Database

```bash
# Simple copy
cp customer_support.db backup_$(date +%Y%m%d).db

# Export to SQL
sqlite3 customer_support.db .dump > backup.sql
```

### Reset Database

```bash
rm customer_support.db
sqlite3 customer_support.db < sqlite_schema.sql
```

### Vacuum (Optimize)

```bash
sqlite3 customer_support.db "VACUUM;"
```

### Check Database Size

```bash
ls -lh customer_support.db
```

## 📈 Testing Scenarios

### Scenario 1: High Confidence - Bot Resolves

```sql
INSERT INTO customer_support_tickets 
(customer_id, issue_category, subject, description, chatbot_handled, chatbot_confidence_score, status)
VALUES (1, 'Delivery', 'Track my order', 'Where is order ORD-123?', 1, 95.0, 'Resolved');
```

### Scenario 2: Low Confidence - Escalate

```sql
INSERT INTO customer_support_tickets 
(customer_id, issue_category, subject, description, chatbot_handled, chatbot_confidence_score, status, assigned_agent_id)
VALUES (2, 'Refund', 'Complex refund issue', 'Multiple items, partial refund needed', 0, 45.0, 'Escalated', 1);
```

### Scenario 3: Medium Confidence - In Progress

```sql
INSERT INTO customer_support_tickets 
(customer_id, issue_category, subject, description, chatbot_handled, chatbot_confidence_score, status)
VALUES (3, 'Product', 'Product question', 'Is this compatible with X?', 0, 65.0, 'In Progress');
```

## 🛠️ Useful Commands

### Interactive Mode

```bash
sqlite3 customer_support.db
```

Then inside SQLite:
```sql
.tables                    -- List all tables
.schema customer_support_tickets  -- Show table structure
.mode column              -- Better formatting
.headers on               -- Show column names
SELECT * FROM customers;  -- Run queries
.quit                     -- Exit
```

### Export to CSV

```bash
sqlite3 customer_support.db -header -csv "SELECT * FROM customer_support_tickets;" > tickets.csv
```

### Import from CSV

```bash
sqlite3 customer_support.db
.mode csv
.import data.csv customer_support_tickets
```

## 📁 File Structure

```
database/
├── customer_support.db       # ← SQLite database (ready to use!)
├── sqlite_schema.sql          # Schema + sample data
├── test_database.py           # Python analytics script
├── view_database.py           # Web viewer
├── queries.sql                # Useful SQL queries
├── README.md                  # Full documentation
├── QUICKSTART.md             # Quick reference
└── SQLITE_GUIDE.md           # This file
```

## 🎯 Next Steps

1. ✅ **Test the database** - Run `python3 test_database.py`
2. 🌐 **View in browser** - Run `python3 view_database.py`
3. 🔍 **Explore queries** - Check `queries.sql` for more examples
4. 🤖 **Integrate with chatbot** - Use Python examples above
5. 📊 **Add test data** - Create more tickets for testing

## 💬 Sample Data Included

**Customers:**
- John Doe (john.doe@email.com)
- Jane Smith (jane.smith@email.com)
- Bob Wilson (bob.wilson@email.com)
- Alice Brown (alice.brown@email.com)
- Charlie Davis (charlie.davis@email.com)

**Ticket Types:**
- ✅ Late delivery (resolved by bot)
- ❌ Payment issue (escalated)
- ⏳ Wrong product (in progress)
- ✅ Login issue (resolved by bot)
- ✅ Order tracking (resolved by bot)

**Intents Detected:**
- track_order
- password_reset
- provide_order_number
- request_refund
- express_gratitude

## 🔗 Resources

- SQLite Documentation: https://www.sqlite.org/docs.html
- Python sqlite3 module: https://docs.python.org/3/library/sqlite3.html
- SQL Tutorial: https://www.sqlitetutorial.net/

---

**Database Version:** 1.0  
**Created:** February 2026  
**Size:** 72KB  
**Records:** 35 total across all tables

Happy testing! 🚀
