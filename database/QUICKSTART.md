# SQLite Database Quick Start Guide

## What You Have

✅ **customer_support.db** - A ready-to-use SQLite database (72KB)  
✅ Pre-loaded with 5 customers, 5 orders, 5 tickets, and conversation logs  
✅ Fully indexed and optimized for chatbot testing

## Instant Usage

### 1. Open the Database
```bash
sqlite3 database/customer_support.db
```

### 2. Run Basic Queries

**View all tickets:**
```sql
SELECT * FROM customer_support_tickets;
```

**View customers:**
```sql
SELECT * FROM customers;
```

**Check chatbot performance:**
```sql
SELECT 
    COUNT(*) as total,
    SUM(chatbot_handled) as resolved_by_bot,
    ROUND(AVG(chatbot_confidence_score), 2) as avg_confidence
FROM customer_support_tickets;
```

**View conversation for a ticket:**
```sql
SELECT sender_type, message_text, intent_detected 
FROM chatbot_conversations 
WHERE ticket_id = 1;
```

### 3. Use Python Test Script

```bash
cd database
python3 test_database.py
```

This will show:
- All support tickets
- Chatbot performance metrics
- Tickets by category
- Customer sentiment analysis
- Sample conversations
- Low confidence tickets

## Database Schema

### Tables:
1. **customer_support_tickets** - Main ticket tracking
2. **chatbot_conversations** - Message logs
3. **customers** - Customer information
4. **orders** - Order tracking
5. **support_agents** - Human agents
6. **chatbot_metrics** - Performance metrics

### Key Fields:
- `chatbot_handled` - 1 if bot resolved, 0 if human needed
- `chatbot_confidence_score` - AI confidence (0-100)
- `status` - Open, In Progress, Resolved, Escalated, Closed
- `priority` - Low, Medium, High, Urgent
- `customer_sentiment` - Positive, Neutral, Negative

## Common Queries

### Find tickets needing escalation:
```sql
SELECT ticket_id, subject, chatbot_confidence_score 
FROM customer_support_tickets 
WHERE chatbot_confidence_score < 70;
```

### Get tickets by status:
```sql
SELECT status, COUNT(*) 
FROM customer_support_tickets 
GROUP BY status;
```

### View customer ticket history:
```sql
SELECT t.ticket_id, t.subject, t.status, t.created_at
FROM customer_support_tickets t
JOIN customers c ON t.customer_id = c.customer_id
WHERE c.email = 'john.doe@email.com'
ORDER BY t.created_at DESC;
```

### Most common intents:
```sql
SELECT intent_detected, COUNT(*) as frequency
FROM chatbot_conversations
WHERE intent_detected IS NOT NULL
GROUP BY intent_detected
ORDER BY frequency DESC;
```

## Python Integration

```python
import sqlite3

# Connect
conn = sqlite3.connect('customer_support.db')
cursor = conn.cursor()

# Create ticket
cursor.execute("""
    INSERT INTO customer_support_tickets 
    (customer_id, issue_category, subject, description)
    VALUES (?, ?, ?, ?)
""", (1, 'General', 'Test ticket', 'This is a test'))
conn.commit()

# Query tickets
cursor.execute("SELECT * FROM customer_support_tickets")
tickets = cursor.fetchall()
for ticket in tickets:
    print(ticket)

conn.close()
```

## Testing Scenarios

### Scenario 1: Track Order (High Confidence)
```sql
INSERT INTO customer_support_tickets 
(customer_id, issue_category, subject, description, chatbot_handled, chatbot_confidence_score, status)
VALUES (1, 'Delivery', 'Where is my order?', 'I want to track my order', 1, 95.0, 'Resolved');
```

### Scenario 2: Refund Request (Low Confidence - Escalate)
```sql
INSERT INTO customer_support_tickets 
(customer_id, issue_category, subject, description, chatbot_handled, chatbot_confidence_score, status)
VALUES (2, 'Refund', 'Need refund', 'Product damaged, need refund', 0, 55.0, 'Escalated');
```

### Scenario 3: Account Issue (Medium Confidence)
```sql
INSERT INTO customer_support_tickets 
(customer_id, issue_category, subject, description, chatbot_handled, chatbot_confidence_score, status)
VALUES (3, 'Account', 'Password reset', 'Cannot reset my password', 1, 88.0, 'Resolved');
```

## Useful Commands

**List all tables:**
```bash
sqlite3 customer_support.db ".tables"
```

**Show table schema:**
```bash
sqlite3 customer_support.db ".schema customer_support_tickets"
```

**Export to CSV:**
```bash
sqlite3 customer_support.db -header -csv "SELECT * FROM customer_support_tickets;" > tickets.csv
```

**Backup database:**
```bash
cp customer_support.db backup_$(date +%Y%m%d).db
```

**Reset database:**
```bash
rm customer_support.db
sqlite3 customer_support.db < sqlite_schema.sql
```

## Next Steps

1. ✅ Database is ready - start querying!
2. 📊 Run `test_database.py` to see analytics
3. 🔧 Modify schema if needed (see `sqlite_schema.sql`)
4. 🤖 Integrate with your chatbot application
5. 📈 Add more test data for comprehensive testing

## File Structure

```
database/
├── customer_support.db      # ← The SQLite database (ready to use!)
├── sqlite_schema.sql         # Schema + sample data
├── test_database.py          # Python test script
├── queries.sql               # Useful SQL queries
├── README.md                 # Full documentation
└── QUICKSTART.md            # This file
```

## Support

For more details, see `README.md` in the database folder.

Happy testing! 🚀
