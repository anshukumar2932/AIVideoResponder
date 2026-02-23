# Customer Support Chatbot Database Documentation

## Overview

This database schema is designed for testing and managing customer support chatbot systems, similar to Amazon-style support platforms. It tracks customer tickets, chatbot interactions, performance metrics, and escalation workflows.

## Database Structure

### Core Tables

#### 1. `customer_support_tickets`
Main table for tracking all support tickets.

**Key Fields:**
- `ticket_id`: Unique identifier for each ticket
- `customer_id`: Reference to the customer
- `order_id`: Optional reference to related order
- `issue_category`: Main category (Payment, Delivery, Refund, Account, Product)
- `issue_subcategory`: Specific issue type
- `chatbot_handled`: Boolean indicating if chatbot resolved the issue
- `chatbot_confidence_score`: AI confidence level (0-100)
- `status`: Current ticket status (Open, In Progress, Resolved, Escalated, Closed)
- `priority`: Urgency level (Low, Medium, High, Urgent)
- `customer_sentiment`: Detected sentiment (Positive, Neutral, Negative)

#### 2. `chatbot_conversations`
Logs all messages exchanged during ticket resolution.

**Key Fields:**
- `message_id`: Unique message identifier
- `ticket_id`: Reference to parent ticket
- `sender_type`: Who sent the message (Customer, Chatbot, Agent)
- `message_text`: Actual message content
- `intent_detected`: Detected user intent (track_order, request_refund, etc.)
- `confidence_score`: Intent detection confidence

#### 3. `customers`
Customer information table.

**Key Fields:**
- `customer_id`: Unique customer identifier
- `email`: Customer email (unique)
- `full_name`: Customer name
- `account_status`: Account state (Active, Suspended, Closed)

#### 4. `orders`
Order tracking table.

**Key Fields:**
- `order_id`: Unique order identifier
- `order_number`: Human-readable order number
- `order_status`: Current order state
- `total_amount`: Order value

#### 5. `support_agents`
Human support agents who handle escalated tickets.

**Key Fields:**
- `agent_id`: Unique agent identifier
- `specialization`: Agent expertise area
- `is_available`: Current availability status

#### 6. `chatbot_metrics`
Daily performance metrics for analytics.

**Key Fields:**
- `total_tickets`: Total tickets received
- `chatbot_resolved`: Tickets resolved by chatbot
- `escalated_to_human`: Tickets requiring human intervention
- `avg_confidence_score`: Average AI confidence
- `customer_satisfaction_score`: CSAT score (1-5)

## Database Compatibility

### SQLite (Recommended for Testing)
Use `customer_support.db` - ready-to-use database file included!

```bash
# Database is already created! Just use it:
sqlite3 database/customer_support.db

# Or recreate from scratch:
sqlite3 database/customer_support.db < database/sqlite_schema.sql

# Run test queries:
python3 database/test_database.py
```

### PostgreSQL
Use `schema.sql` - includes `GENERATED ALWAYS AS IDENTITY` for auto-increment.

```sql
-- Create database
CREATE DATABASE customer_support_db;

-- Connect and run schema
\c customer_support_db
\i schema.sql
\i sample_data.sql
```

### MySQL
Use `mysql_schema.sql` - uses `AUTO_INCREMENT` instead.

```sql
-- Create database
CREATE DATABASE customer_support_db;

-- Use database and run schema
USE customer_support_db;
SOURCE mysql_schema.sql;
SOURCE sample_data.sql;
```

## Setup Instructions

### SQLite (Quickstart - Recommended)

The database is already created! Just start using it:

```bash
# Open the database
sqlite3 database/customer_support.db

# Run some queries
sqlite3 database/customer_support.db "SELECT * FROM customers;"

# Or use the Python test script
cd database
python3 test_database.py
```

To recreate from scratch:
```bash
sqlite3 database/customer_support.db < database/sqlite_schema.sql
```

### PostgreSQL

**1. Create Database:**
```bash
psql -U postgres
CREATE DATABASE customer_support_db;
\q
```

**2. Run Schema:**
```bash
psql -U postgres -d customer_support_db -f schema.sql
```

**3. Load Sample Data:**
```bash
psql -U postgres -d customer_support_db -f sample_data.sql
```

### MySQL

**1. Create Database:**
```bash
mysql -u root -p
CREATE DATABASE customer_support_db;
exit;
```

**2. Run Schema:**
```bash
mysql -u root -p customer_support_db < mysql_schema.sql
```

**3. Load Sample Data:**
```bash
mysql -u root -p customer_support_db < sample_data.sql
```

## Common Use Cases

### 1. Track Chatbot Performance

```sql
SELECT 
    COUNT(*) as total_tickets,
    SUM(CASE WHEN chatbot_handled = TRUE THEN 1 ELSE 0 END) as resolved_by_bot,
    ROUND(100.0 * SUM(CASE WHEN chatbot_handled = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) as success_rate
FROM customer_support_tickets;
```

### 2. Find Low Confidence Tickets

```sql
SELECT ticket_id, subject, chatbot_confidence_score, status
FROM customer_support_tickets
WHERE chatbot_confidence_score < 70
ORDER BY chatbot_confidence_score ASC;
```

### 3. View Conversation History

```sql
SELECT sender_type, message_text, intent_detected, confidence_score
FROM chatbot_conversations
WHERE ticket_id = 1
ORDER BY created_at ASC;
```

### 4. Analyze Customer Sentiment

```sql
SELECT 
    customer_sentiment,
    COUNT(*) as count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) as percentage
FROM customer_support_tickets
WHERE customer_sentiment IS NOT NULL
GROUP BY customer_sentiment;
```

## Chatbot Testing Scenarios

### Scenario 1: Order Tracking
```sql
-- Customer asks: "Where is my order?"
INSERT INTO customer_support_tickets 
(customer_id, order_id, issue_category, subject, description, chatbot_handled, chatbot_confidence_score, status)
VALUES (1, 1, 'Delivery', 'Track order', 'Where is my order?', TRUE, 95.0, 'Resolved');
```

### Scenario 2: Refund Request
```sql
-- Customer asks: "I want a refund"
INSERT INTO customer_support_tickets 
(customer_id, order_id, issue_category, subject, description, chatbot_handled, chatbot_confidence_score, status)
VALUES (2, 2, 'Refund', 'Request refund', 'I want to return this item', FALSE, 65.0, 'Escalated');
```

### Scenario 3: Account Issue
```sql
-- Customer asks: "Can't login"
INSERT INTO customer_support_tickets 
(customer_id, issue_category, subject, description, chatbot_handled, chatbot_confidence_score, status)
VALUES (3, 'Account', 'Login problem', 'Forgot password', TRUE, 92.0, 'Resolved');
```

## Performance Optimization

### Recommended Indexes
Already included in schema:
- `idx_tickets_customer`: Fast customer lookup
- `idx_tickets_status`: Filter by status
- `idx_tickets_created`: Time-based queries
- `idx_conversations_ticket`: Conversation retrieval
- `idx_orders_customer`: Order lookup

### Additional Indexes (Optional)
```sql
CREATE INDEX idx_tickets_category ON customer_support_tickets(issue_category);
CREATE INDEX idx_tickets_priority ON customer_support_tickets(priority);
CREATE INDEX idx_conversations_intent ON chatbot_conversations(intent_detected);
```

## Analytics Queries

See `queries.sql` for 15+ pre-built analytical queries including:
- Chatbot performance metrics
- Resolution time analysis
- Intent detection frequency
- Agent workload distribution
- Customer sentiment trends

## Integration Points

### Chatbot Integration
1. Create ticket when conversation starts
2. Log each message to `chatbot_conversations`
3. Update `chatbot_confidence_score` based on intent detection
4. Set `chatbot_handled = TRUE` if resolved
5. Escalate to human if confidence < threshold

### Example Python Integration

**SQLite:**
```python
import sqlite3

# Connect to database
conn = sqlite3.connect('customer_support.db')
cursor = conn.cursor()

# Create new ticket
def create_ticket(customer_id, subject, description, category):
    cursor.execute("""
        INSERT INTO customer_support_tickets 
        (customer_id, issue_category, subject, description)
        VALUES (?, ?, ?, ?)
    """, (customer_id, category, subject, description))
    ticket_id = cursor.lastrowid
    conn.commit()
    return ticket_id

# Log conversation
def log_message(ticket_id, sender, message, intent, confidence):
    cursor.execute("""
        INSERT INTO chatbot_conversations 
        (ticket_id, sender_type, message_text, intent_detected, confidence_score)
        VALUES (?, ?, ?, ?, ?)
    """, (ticket_id, sender, message, intent, confidence))
    conn.commit()

# Use the functions
ticket_id = create_ticket(1, "Need help", "I have a question", "General")
log_message(ticket_id, "Customer", "Hello", "greeting", 95.0)
```

**PostgreSQL:**
```python
import psycopg2

# Create new ticket
def create_ticket(customer_id, subject, description, category):
    conn = psycopg2.connect("dbname=customer_support_db")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO customer_support_tickets 
        (customer_id, issue_category, subject, description)
        VALUES (%s, %s, %s, %s)
        RETURNING ticket_id
    """, (customer_id, category, subject, description))
    ticket_id = cur.fetchone()[0]
    conn.commit()
    return ticket_id

# Log conversation
def log_message(ticket_id, sender, message, intent, confidence):
    conn = psycopg2.connect("dbname=customer_support_db")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO chatbot_conversations 
        (ticket_id, sender_type, message_text, intent_detected, confidence_score)
        VALUES (%s, %s, %s, %s, %s)
    """, (ticket_id, sender, message, intent, confidence))
    conn.commit()
```

## Maintenance

### Regular Tasks
1. Archive old resolved tickets (>90 days)
2. Update daily metrics in `chatbot_metrics`
3. Clean up orphaned conversations
4. Analyze low-confidence patterns

### Backup

**SQLite:**
```bash
# Simple file copy
cp customer_support.db customer_support_backup.db

# Or export to SQL
sqlite3 customer_support.db .dump > backup.sql
```

**PostgreSQL:**
```bash
pg_dump customer_support_db > backup.sql
```

**MySQL:**
```bash
mysqldump customer_support_db > backup.sql
```

## Extending the Schema

### Add Custom Fields
```sql
ALTER TABLE customer_support_tickets 
ADD COLUMN custom_field VARCHAR(255);
```

### Add New Intent Types
Just insert new values - no schema change needed:
```sql
INSERT INTO chatbot_conversations 
(ticket_id, sender_type, message_text, intent_detected)
VALUES (1, 'Customer', 'Message', 'new_intent_type');
```

## Troubleshooting

### Issue: Foreign Key Constraint Errors
**Solution:** Ensure parent records exist before inserting child records.
```sql
-- Insert customer first, then ticket
INSERT INTO customers (...) VALUES (...);
INSERT INTO customer_support_tickets (...) VALUES (...);
```

### Issue: Check Constraint Violations
**Solution:** Use only allowed values for status, priority, sentiment fields.

### Issue: Timestamp Issues in MySQL
**Solution:** Use `NOW()` instead of `CURRENT_TIMESTAMP` in queries.

## License

This schema is provided as-is for educational and commercial use.

## Support

For questions or issues, refer to:
- PostgreSQL docs: https://www.postgresql.org/docs/
- MySQL docs: https://dev.mysql.com/doc/

---

**Version:** 1.0  
**Last Updated:** February 2026  
**Compatible With:** SQLite 3+, PostgreSQL 12+, MySQL 5.7+, MariaDB 10.2+

## Quick Start

```bash
# The SQLite database is ready to use!
cd database
python3 test_database.py

# Or query directly
sqlite3 customer_support.db "SELECT * FROM customer_support_tickets;"
```
