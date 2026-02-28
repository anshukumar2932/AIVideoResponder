-- ============================================================================
-- Customer Support Chatbot Database Schema
-- ============================================================================
-- Compatible with: PostgreSQL (primary), MySQL (with minor modifications)
-- Purpose: Track customer support tickets and chatbot interactions
-- ============================================================================

-- Main Customer Support Tickets Table
CREATE TABLE customer_support_tickets (
    ticket_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    customer_id BIGINT NOT NULL,
    order_id BIGINT NULL,
    
    -- Issue Classification
    issue_category VARCHAR(100) NOT NULL,      -- Payment, Delivery, Refund, Account, Product
    issue_subcategory VARCHAR(100) NULL,       -- Late Delivery, Wrong Item, Damaged Product
    
    -- Ticket Details
    subject VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    
    -- Chatbot Metrics
    chatbot_handled BOOLEAN DEFAULT FALSE,     -- Did chatbot resolve it?
    chatbot_confidence_score DECIMAL(5,2),     -- Confidence level (0-100)
    
    -- Status Tracking
    status VARCHAR(50) DEFAULT 'Open',         -- Open, In Progress, Resolved, Escalated, Closed
    priority VARCHAR(20) DEFAULT 'Medium',     -- Low, Medium, High, Urgent
    
    -- Assignment
    assigned_agent_id BIGINT NULL,             -- Human agent if escalated
    
    -- Sentiment Analysis
    customer_sentiment VARCHAR(20),            -- Positive, Neutral, Negative
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL,
    
    -- Resolution
    resolution_notes TEXT,
    
    -- Constraints
    CONSTRAINT chk_status CHECK (status IN ('Open', 'In Progress', 'Resolved', 'Escalated', 'Closed')),
    CONSTRAINT chk_priority CHECK (priority IN ('Low', 'Medium', 'High', 'Urgent')),
    CONSTRAINT chk_sentiment CHECK (customer_sentiment IN ('Positive', 'Neutral', 'Negative'))
);

-- Chatbot Conversation Log Table
CREATE TABLE chatbot_conversations (
    message_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    ticket_id BIGINT NOT NULL,
    sender_type VARCHAR(20) NOT NULL,          -- Customer, Chatbot, Agent
    message_text TEXT NOT NULL,
    intent_detected VARCHAR(100),              -- track_order, request_refund, etc.
    confidence_score DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_ticket
        FOREIGN KEY (ticket_id)
        REFERENCES customer_support_tickets(ticket_id)
        ON DELETE CASCADE,
    CONSTRAINT chk_sender CHECK (sender_type IN ('Customer', 'Chatbot', 'Agent'))
);

-- Customers Table (Supporting)
CREATE TABLE customers (
    customer_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    account_status VARCHAR(20) DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_account_status CHECK (account_status IN ('Active', 'Suspended', 'Closed'))
);

-- Orders Table (Supporting)
CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    customer_id BIGINT NOT NULL,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    order_status VARCHAR(50) DEFAULT 'Pending',
    total_amount DECIMAL(10,2) NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivery_date TIMESTAMP NULL,
    
    CONSTRAINT fk_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
        ON DELETE CASCADE,
    CONSTRAINT chk_order_status CHECK (order_status IN ('Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled', 'Returned'))
);

-- Support Agents Table
CREATE TABLE support_agents (
    agent_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    agent_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    specialization VARCHAR(100),               -- Refunds, Technical, Billing
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chatbot Performance Metrics Table
CREATE TABLE chatbot_metrics (
    metric_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    date DATE NOT NULL,
    total_tickets INT DEFAULT 0,
    chatbot_resolved INT DEFAULT 0,
    escalated_to_human INT DEFAULT 0,
    avg_confidence_score DECIMAL(5,2),
    avg_resolution_time_minutes INT,
    customer_satisfaction_score DECIMAL(3,2),  -- 1-5 scale
    
    CONSTRAINT chk_satisfaction CHECK (customer_satisfaction_score BETWEEN 1 AND 5)
);

-- Indexes for Performance
CREATE INDEX idx_tickets_customer ON customer_support_tickets(customer_id);
CREATE INDEX idx_tickets_status ON customer_support_tickets(status);
CREATE INDEX idx_tickets_created ON customer_support_tickets(created_at);
CREATE INDEX idx_conversations_ticket ON chatbot_conversations(ticket_id);
CREATE INDEX idx_orders_customer ON orders(customer_id);

-- ============================================================================
-- MySQL Compatibility Notes:
-- Replace "GENERATED ALWAYS AS IDENTITY" with "AUTO_INCREMENT"
-- Example: ticket_id BIGINT PRIMARY KEY AUTO_INCREMENT
-- ============================================================================
