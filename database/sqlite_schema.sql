-- ============================================================================
-- Customer Support Chatbot Database Schema - SQLite Version
-- ============================================================================

-- Main Customer Support Tickets Table
CREATE TABLE customer_support_tickets (
    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    order_id INTEGER NULL,
    
    -- Issue Classification
    issue_category TEXT NOT NULL,
    issue_subcategory TEXT NULL,
    
    -- Ticket Details
    subject TEXT NOT NULL,
    description TEXT NOT NULL,
    
    -- Chatbot Metrics
    chatbot_handled INTEGER DEFAULT 0,  -- 0=False, 1=True
    chatbot_confidence_score REAL,
    
    -- Status Tracking
    status TEXT DEFAULT 'Open' CHECK(status IN ('Open', 'In Progress', 'Resolved', 'Escalated', 'Closed')),
    priority TEXT DEFAULT 'Medium' CHECK(priority IN ('Low', 'Medium', 'High', 'Urgent')),
    
    -- Assignment
    assigned_agent_id INTEGER NULL,
    
    -- Sentiment Analysis
    customer_sentiment TEXT CHECK(customer_sentiment IN ('Positive', 'Neutral', 'Negative')),
    
    -- Timestamps
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    resolved_at TEXT NULL,
    
    -- Resolution
    resolution_notes TEXT
);

-- Chatbot Conversation Log Table
CREATE TABLE chatbot_conversations (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id INTEGER NOT NULL,
    sender_type TEXT NOT NULL CHECK(sender_type IN ('Customer', 'Chatbot', 'Agent')),
    message_text TEXT NOT NULL,
    intent_detected TEXT,
    confidence_score REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (ticket_id) REFERENCES customer_support_tickets(ticket_id) ON DELETE CASCADE
);

-- Customers Table
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    phone TEXT,
    account_status TEXT DEFAULT 'Active' CHECK(account_status IN ('Active', 'Suspended', 'Closed')),
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Orders Table
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    order_number TEXT UNIQUE NOT NULL,
    order_status TEXT DEFAULT 'Pending' CHECK(order_status IN ('Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled', 'Returned')),
    total_amount REAL NOT NULL,
    order_date TEXT DEFAULT CURRENT_TIMESTAMP,
    delivery_date TEXT NULL,
    
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);

-- Support Agents Table
CREATE TABLE support_agents (
    agent_id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    specialization TEXT,
    is_available INTEGER DEFAULT 1,  -- 0=False, 1=True
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Chatbot Performance Metrics Table
CREATE TABLE chatbot_metrics (
    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    total_tickets INTEGER DEFAULT 0,
    chatbot_resolved INTEGER DEFAULT 0,
    escalated_to_human INTEGER DEFAULT 0,
    avg_confidence_score REAL,
    avg_resolution_time_minutes INTEGER,
    customer_satisfaction_score REAL CHECK(customer_satisfaction_score BETWEEN 1 AND 5)
);

-- Indexes for Performance
CREATE INDEX idx_tickets_customer ON customer_support_tickets(customer_id);
CREATE INDEX idx_tickets_status ON customer_support_tickets(status);
CREATE INDEX idx_tickets_created ON customer_support_tickets(created_at);
CREATE INDEX idx_conversations_ticket ON chatbot_conversations(ticket_id);
CREATE INDEX idx_orders_customer ON orders(customer_id);

-- Insert Sample Customers
INSERT INTO customers (email, full_name, phone, account_status) VALUES
('john.doe@email.com', 'John Doe', '+1-555-0101', 'Active'),
('jane.smith@email.com', 'Jane Smith', '+1-555-0102', 'Active'),
('bob.wilson@email.com', 'Bob Wilson', '+1-555-0103', 'Active'),
('alice.brown@email.com', 'Alice Brown', '+1-555-0104', 'Active'),
('charlie.davis@email.com', 'Charlie Davis', '+1-555-0105', 'Active');

-- Insert Sample Orders
INSERT INTO orders (customer_id, order_number, order_status, total_amount, order_date) VALUES
(1, 'ORD-2024-001', 'Delivered', 299.99, datetime('now', '-5 days')),
(1, 'ORD-2024-002', 'Shipped', 149.50, datetime('now', '-2 days')),
(2, 'ORD-2024-003', 'Processing', 89.99, datetime('now', '-1 day')),
(3, 'ORD-2024-004', 'Delivered', 499.99, datetime('now', '-10 days')),
(4, 'ORD-2024-005', 'Cancelled', 199.99, datetime('now', '-3 days'));

-- Insert Support Agents
INSERT INTO support_agents (agent_name, email, specialization, is_available) VALUES
('Sarah Johnson', 'sarah.j@support.com', 'Refunds', 1),
('Mike Chen', 'mike.c@support.com', 'Technical', 1),
('Emily Rodriguez', 'emily.r@support.com', 'Billing', 1);

-- Insert Sample Support Tickets
INSERT INTO customer_support_tickets 
(customer_id, order_id, issue_category, issue_subcategory, subject, description, 
 chatbot_handled, chatbot_confidence_score, status, priority, customer_sentiment) 
VALUES
(1, 1, 'Delivery', 'Late Delivery', 'Order not received on time', 
 'My order was supposed to arrive yesterday but I still haven''t received it.', 
 1, 85.50, 'Resolved', 'Medium', 'Neutral'),

(2, 3, 'Payment', 'Payment Failed', 'Payment declined but amount deducted', 
 'My payment was declined but the amount was deducted from my account.', 
 0, 45.20, 'Escalated', 'High', 'Negative'),

(3, 4, 'Product', 'Wrong Item', 'Received wrong product', 
 'I ordered a blue shirt but received a red one instead.', 
 0, 60.00, 'In Progress', 'Medium', 'Negative'),

(4, NULL, 'Account', 'Login Issue', 'Cannot login to my account', 
 'I forgot my password and the reset link is not working.', 
 1, 92.30, 'Resolved', 'Low', 'Neutral'),

(1, 2, 'Delivery', 'Track Order', 'Where is my order?', 
 'Can you tell me the current status of my order ORD-2024-002?', 
 1, 95.80, 'Resolved', 'Low', 'Positive');

-- Insert Chatbot Conversations
-- Ticket 1: Late Delivery (Resolved by Chatbot)
INSERT INTO chatbot_conversations (ticket_id, sender_type, message_text, intent_detected, confidence_score) VALUES
(1, 'Customer', 'My order was supposed to arrive yesterday but I still haven''t received it.', 'track_order', 88.50),
(1, 'Chatbot', 'I understand your concern. Let me check the status of your order. Can you provide your order number?', 'request_order_number', 90.00),
(1, 'Customer', 'ORD-2024-001', 'provide_order_number', 95.00),
(1, 'Chatbot', 'Thank you! I see your order is currently in transit and will be delivered by tomorrow evening. Would you like me to send you tracking updates?', 'provide_tracking_info', 92.00),
(1, 'Customer', 'Yes please', 'confirm_action', 98.00),
(1, 'Chatbot', 'Great! I''ve enabled tracking notifications for your order. You''ll receive SMS updates. Is there anything else I can help with?', 'confirm_resolution', 95.00);

-- Ticket 4: Login Issue (Resolved by Chatbot)
INSERT INTO chatbot_conversations (ticket_id, sender_type, message_text, intent_detected, confidence_score) VALUES
(4, 'Customer', 'I forgot my password and the reset link is not working.', 'password_reset', 90.00),
(4, 'Chatbot', 'I can help you reset your password. Let me send you a new reset link to your registered email. Is alice.brown@email.com correct?', 'verify_email', 92.00),
(4, 'Customer', 'Yes that''s correct', 'confirm_email', 96.00),
(4, 'Chatbot', 'Perfect! I''ve sent a new password reset link to your email. Please check your inbox and spam folder. The link will expire in 24 hours.', 'send_reset_link', 94.00),
(4, 'Customer', 'Got it, thanks!', 'express_gratitude', 98.00);

-- Ticket 5: Track Order (Resolved by Chatbot)
INSERT INTO chatbot_conversations (ticket_id, sender_type, message_text, intent_detected, confidence_score) VALUES
(5, 'Customer', 'Where is my order?', 'track_order', 95.00),
(5, 'Chatbot', 'I''d be happy to help you track your order. Could you please provide your order number?', 'request_order_number', 96.00),
(5, 'Customer', 'ORD-2024-002', 'provide_order_number', 98.00),
(5, 'Chatbot', 'Your order ORD-2024-002 is currently shipped and expected to arrive on Feb 25, 2026. Tracking number: TRK123456789', 'provide_tracking_info', 97.00);

-- Insert Performance Metrics
INSERT INTO chatbot_metrics (date, total_tickets, chatbot_resolved, escalated_to_human, 
                             avg_confidence_score, avg_resolution_time_minutes, customer_satisfaction_score) 
VALUES
(date('now', '-1 day'), 15, 12, 3, 87.50, 8, 4.2),
(date('now'), 5, 3, 2, 85.20, 10, 4.0);
