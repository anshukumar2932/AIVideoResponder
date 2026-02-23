#!/usr/bin/env python3
"""
Simple web viewer for SQLite Customer Support Database
Run: python3 view_database.py
Then open: http://localhost:8000
"""

import sqlite3
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

DB_FILE = 'customer_support.db'

class DatabaseViewer(BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/':
            self.serve_html()
        elif path == '/api/tickets':
            self.serve_tickets()
        elif path == '/api/conversations':
            query = parse_qs(parsed_path.query)
            ticket_id = query.get('ticket_id', [None])[0]
            self.serve_conversations(ticket_id)
        elif path == '/api/stats':
            self.serve_stats()
        else:
            self.send_error(404)
    
    def serve_html(self):
        html = """
<!DOCTYPE html>
<html>
<head>
    <title>Customer Support Database Viewer</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        h1 { color: #333; }
        .container { max-width: 1200px; margin: 0 auto; }
        .stats { display: flex; gap: 20px; margin: 20px 0; }
        .stat-card { background: white; padding: 20px; border-radius: 8px; flex: 1; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .stat-card h3 { margin: 0 0 10px 0; color: #666; font-size: 14px; }
        .stat-card .value { font-size: 32px; font-weight: bold; color: #2196F3; }
        table { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        th { background: #2196F3; color: white; padding: 12px; text-align: left; }
        td { padding: 12px; border-bottom: 1px solid #ddd; }
        tr:hover { background: #f5f5f5; }
        .badge { padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
        .badge-resolved { background: #4CAF50; color: white; }
        .badge-open { background: #FF9800; color: white; }
        .badge-escalated { background: #F44336; color: white; }
        .badge-progress { background: #2196F3; color: white; }
        .confidence { font-weight: bold; }
        .confidence-high { color: #4CAF50; }
        .confidence-medium { color: #FF9800; }
        .confidence-low { color: #F44336; }
        .conversation { background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .message { margin: 10px 0; padding: 10px; border-radius: 4px; }
        .message-customer { background: #E3F2FD; }
        .message-chatbot { background: #F1F8E9; }
        .message-agent { background: #FFF3E0; }
        .sender { font-weight: bold; margin-bottom: 5px; }
        .intent { font-size: 12px; color: #666; font-style: italic; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Customer Support Database Viewer</h1>
        
        <div class="stats" id="stats"></div>
        
        <h2>Support Tickets</h2>
        <table id="tickets">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Customer</th>
                    <th>Subject</th>
                    <th>Category</th>
                    <th>Status</th>
                    <th>Confidence</th>
                    <th>Bot Handled</th>
                </tr>
            </thead>
            <tbody></tbody>
        </table>
        
        <div id="conversations"></div>
    </div>
    
    <script>
        // Load stats
        fetch('/api/stats')
            .then(r => r.json())
            .then(data => {
                document.getElementById('stats').innerHTML = `
                    <div class="stat-card">
                        <h3>Total Tickets</h3>
                        <div class="value">${data.total_tickets}</div>
                    </div>
                    <div class="stat-card">
                        <h3>Bot Resolved</h3>
                        <div class="value">${data.bot_resolved}</div>
                    </div>
                    <div class="stat-card">
                        <h3>Success Rate</h3>
                        <div class="value">${data.success_rate}%</div>
                    </div>
                    <div class="stat-card">
                        <h3>Avg Confidence</h3>
                        <div class="value">${data.avg_confidence}%</div>
                    </div>
                `;
            });
        
        // Load tickets
        fetch('/api/tickets')
            .then(r => r.json())
            .then(tickets => {
                const tbody = document.querySelector('#tickets tbody');
                tbody.innerHTML = tickets.map(t => {
                    const statusClass = t.status.toLowerCase().replace(' ', '-');
                    const confClass = t.confidence >= 80 ? 'high' : t.confidence >= 60 ? 'medium' : 'low';
                    return `
                        <tr onclick="loadConversation(${t.ticket_id})" style="cursor: pointer;">
                            <td>${t.ticket_id}</td>
                            <td>${t.customer}</td>
                            <td>${t.subject}</td>
                            <td>${t.category}</td>
                            <td><span class="badge badge-${statusClass}">${t.status}</span></td>
                            <td><span class="confidence confidence-${confClass}">${t.confidence}%</span></td>
                            <td>${t.bot_handled ? '✓' : '✗'}</td>
                        </tr>
                    `;
                }).join('');
            });
        
        function loadConversation(ticketId) {
            fetch('/api/conversations?ticket_id=' + ticketId)
                .then(r => r.json())
                .then(messages => {
                    if (messages.length === 0) {
                        document.getElementById('conversations').innerHTML = '<p>No conversation found for this ticket.</p>';
                        return;
                    }
                    document.getElementById('conversations').innerHTML = `
                        <h2>Conversation for Ticket #${ticketId}</h2>
                        <div class="conversation">
                            ${messages.map(m => `
                                <div class="message message-${m.sender.toLowerCase()}">
                                    <div class="sender">${m.sender}</div>
                                    <div>${m.message}</div>
                                    ${m.intent ? `<div class="intent">Intent: ${m.intent} (${m.confidence}%)</div>` : ''}
                                </div>
                            `).join('')}
                        </div>
                    `;
                });
        }
    </script>
</body>
</html>
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_tickets(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.ticket_id, c.full_name, t.subject, t.issue_category, 
                   t.status, t.chatbot_confidence_score, t.chatbot_handled
            FROM customer_support_tickets t
            JOIN customers c ON t.customer_id = c.customer_id
            ORDER BY t.ticket_id
        """)
        tickets = [{
            'ticket_id': row[0],
            'customer': row[1],
            'subject': row[2],
            'category': row[3],
            'status': row[4],
            'confidence': round(row[5] or 0, 1),
            'bot_handled': bool(row[6])
        } for row in cursor.fetchall()]
        conn.close()
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(tickets).encode())
    
    def serve_conversations(self, ticket_id):
        if not ticket_id:
            self.send_error(400)
            return
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sender_type, message_text, intent_detected, confidence_score
            FROM chatbot_conversations
            WHERE ticket_id = ?
            ORDER BY message_id
        """, (ticket_id,))
        messages = [{
            'sender': row[0],
            'message': row[1],
            'intent': row[2],
            'confidence': round(row[3] or 0, 1)
        } for row in cursor.fetchall()]
        conn.close()
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(messages).encode())
    
    def serve_stats(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(chatbot_handled) as resolved,
                ROUND(AVG(chatbot_confidence_score), 1) as avg_conf,
                ROUND(100.0 * SUM(chatbot_handled) / COUNT(*), 1) as success_rate
            FROM customer_support_tickets
        """)
        row = cursor.fetchone()
        stats = {
            'total_tickets': row[0],
            'bot_resolved': row[1],
            'avg_confidence': row[2],
            'success_rate': row[3]
        }
        conn.close()
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(stats).encode())
    
    def log_message(self, format, *args):
        pass  # Suppress log messages

if __name__ == '__main__':
    PORT = 8000
    server = HTTPServer(('localhost', PORT), DatabaseViewer)
    print(f"🚀 Database viewer running at http://localhost:{PORT}")
    print(f"📊 Viewing: {DB_FILE}")
    print("Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ Server stopped")
