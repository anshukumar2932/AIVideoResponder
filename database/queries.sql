-- ============================================================================
-- Useful Queries for Chatbot Testing & Analytics
-- ============================================================================

-- 1. Get all open tickets
SELECT 
    t.ticket_id,
    c.full_name,
    t.subject,
    t.issue_category,
    t.priority,
    t.created_at
FROM customer_support_tickets t
JOIN customers c ON t.customer_id = c.customer_id
WHERE t.status = 'Open'
ORDER BY t.priority DESC, t.created_at ASC;

-- 2. Chatbot performance summary
SELECT 
    COUNT(*) as total_tickets,
    SUM(CASE WHEN chatbot_handled = TRUE THEN 1 ELSE 0 END) as chatbot_resolved,
    SUM(CASE WHEN status = 'Escalated' THEN 1 ELSE 0 END) as escalated,
    ROUND(AVG(chatbot_confidence_score), 2) as avg_confidence,
    ROUND(100.0 * SUM(CASE WHEN chatbot_handled = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) as resolution_rate
FROM customer_support_tickets
WHERE created_at >= CURRENT_DATE - INTERVAL '7 days';

-- 3. Tickets by category and status
SELECT 
    issue_category,
    status,
    COUNT(*) as ticket_count,
    AVG(chatbot_confidence_score) as avg_confidence
FROM customer_support_tickets
GROUP BY issue_category, status
ORDER BY issue_category, ticket_count DESC;

-- 4. Customer sentiment analysis
SELECT 
    customer_sentiment,
    COUNT(*) as count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) as percentage
FROM customer_support_tickets
WHERE customer_sentiment IS NOT NULL
GROUP BY customer_sentiment;

-- 5. Average resolution time by category
SELECT 
    issue_category,
    COUNT(*) as total_tickets,
    ROUND(AVG(EXTRACT(EPOCH FROM (resolved_at - created_at))/60), 2) as avg_resolution_minutes
FROM customer_support_tickets
WHERE resolved_at IS NOT NULL
GROUP BY issue_category
ORDER BY avg_resolution_minutes DESC;

-- 6. Chatbot conversation history for a ticket
SELECT 
    c.message_id,
    c.sender_type,
    c.message_text,
    c.intent_detected,
    c.confidence_score,
    c.created_at
FROM chatbot_conversations c
WHERE c.ticket_id = 1
ORDER BY c.created_at ASC;

-- 7. Most common intents detected
SELECT 
    intent_detected,
    COUNT(*) as frequency,
    ROUND(AVG(confidence_score), 2) as avg_confidence
FROM chatbot_conversations
WHERE intent_detected IS NOT NULL
GROUP BY intent_detected
ORDER BY frequency DESC
LIMIT 10;

-- 8. Tickets requiring human escalation
SELECT 
    t.ticket_id,
    c.full_name,
    t.subject,
    t.issue_category,
    t.chatbot_confidence_score,
    t.created_at,
    a.agent_name
FROM customer_support_tickets t
JOIN customers c ON t.customer_id = c.customer_id
LEFT JOIN support_agents a ON t.assigned_agent_id = a.agent_id
WHERE t.status = 'Escalated'
ORDER BY t.priority DESC, t.created_at ASC;

-- 9. Customer ticket history
SELECT 
    t.ticket_id,
    t.subject,
    t.issue_category,
    t.status,
    t.chatbot_handled,
    t.created_at,
    t.resolved_at
FROM customer_support_tickets t
WHERE t.customer_id = 1
ORDER BY t.created_at DESC;

-- 10. Daily chatbot metrics
SELECT 
    DATE(created_at) as date,
    COUNT(*) as total_tickets,
    SUM(CASE WHEN chatbot_handled = TRUE THEN 1 ELSE 0 END) as resolved_by_bot,
    ROUND(AVG(chatbot_confidence_score), 2) as avg_confidence,
    COUNT(DISTINCT customer_id) as unique_customers
FROM customer_support_tickets
WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- 11. Low confidence tickets (may need review)
SELECT 
    t.ticket_id,
    c.full_name,
    t.subject,
    t.chatbot_confidence_score,
    t.status,
    t.created_at
FROM customer_support_tickets t
JOIN customers c ON t.customer_id = c.customer_id
WHERE t.chatbot_confidence_score < 70
ORDER BY t.chatbot_confidence_score ASC;

-- 12. Agent workload
SELECT 
    a.agent_name,
    a.specialization,
    COUNT(t.ticket_id) as assigned_tickets,
    SUM(CASE WHEN t.status = 'Resolved' THEN 1 ELSE 0 END) as resolved_tickets
FROM support_agents a
LEFT JOIN customer_support_tickets t ON a.agent_id = t.assigned_agent_id
GROUP BY a.agent_id, a.agent_name, a.specialization
ORDER BY assigned_tickets DESC;

-- 13. Tickets with orders
SELECT 
    t.ticket_id,
    c.full_name,
    o.order_number,
    o.order_status,
    t.issue_category,
    t.subject,
    t.status
FROM customer_support_tickets t
JOIN customers c ON t.customer_id = c.customer_id
JOIN orders o ON t.order_id = o.order_id
WHERE t.order_id IS NOT NULL
ORDER BY t.created_at DESC;

-- 14. Update ticket status
-- UPDATE customer_support_tickets 
-- SET status = 'Resolved', 
--     resolved_at = CURRENT_TIMESTAMP,
--     resolution_notes = 'Issue resolved by chatbot'
-- WHERE ticket_id = 1;

-- 15. Escalate ticket to human agent
-- UPDATE customer_support_tickets 
-- SET status = 'Escalated',
--     assigned_agent_id = 1,
--     priority = 'High'
-- WHERE ticket_id = 2;
