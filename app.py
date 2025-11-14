from flask import Flask, render_template
import sqlite3
import re
from datetime import datetime
import socket

app = Flask(__name__)

def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect("ecom.db")
    conn.row_factory = sqlite3.Row
    return conn

def execute_query(query):
    """Execute a SQL query and return results"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query)
    columns = [description[0] for description in cur.description] if cur.description else []
    rows = cur.fetchall()
    conn.close()
    return columns, rows

def get_local_ip():
    """Get the local IP address for network access"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/user-spending')
def user_spending():
    """Get user spending with distinct brands"""
    query = """
    SELECT u.user_id, u.name, u.email,
           COUNT(DISTINCT pr.brand) AS distinct_brands,
           SUM(p.amount) AS total_spent
    FROM users u
    JOIN orders o ON u.user_id = o.user_id
    JOIN payments p ON o.order_id = p.order_id AND p.status = 'paid'
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products pr ON oi.product_id = pr.product_id
    GROUP BY u.user_id
    ORDER BY total_spent DESC
    LIMIT 50;
    """
    columns, rows = execute_query(query)
    return {
        'columns': columns,
        'rows': [dict(row) for row in rows]
    }

@app.route('/api/rfm-analysis')
def rfm_analysis():
    """Get RFM analysis"""
    query = """
    WITH last_order AS (
      SELECT user_id, MAX(order_date) AS last_order_date
      FROM orders
      GROUP BY user_id
    ),
    freq AS (
      SELECT user_id, COUNT(*) AS order_count
      FROM orders
      GROUP BY user_id
    ),
    monetary AS (
      SELECT o.user_id, SUM(p.amount) AS total_spent
      FROM orders o
      JOIN payments p ON o.order_id = p.order_id
      WHERE p.status = 'paid'
      GROUP BY o.user_id
    )
    SELECT 
      u.user_id,
      u.name,
      u.email,
      ROUND(julianday('now') - julianday(last_order.last_order_date), 1) AS recency_days,
      freq.order_count,
      ROUND(COALESCE(monetary.total_spent,0), 2) AS total_spent
    FROM users u
    LEFT JOIN last_order ON u.user_id = last_order.user_id
    LEFT JOIN freq ON u.user_id = freq.user_id
    LEFT JOIN monetary ON u.user_id = monetary.user_id
    ORDER BY total_spent DESC
    LIMIT 20;
    """
    columns, rows = execute_query(query)
    return {
        'columns': columns,
        'rows': [dict(row) for row in rows]
    }

@app.route('/api/sustainability')
def sustainability():
    """Get sustainability revenue share"""
    query = """
    SELECT 
      ROUND(SUM(p.amount), 2) AS total_paid,
      ROUND(SUM(p.amount * (pr.sustainability_score >= 0.7)), 2) AS high_sustainability_revenue,
      ROUND(100.0 * SUM(p.amount * (pr.sustainability_score >= 0.7)) / SUM(p.amount), 2) AS pct_high_sustainability
    FROM payments p
    JOIN orders o ON p.order_id = o.order_id
    JOIN order_items oi ON oi.order_id = o.order_id
    JOIN products pr ON pr.product_id = oi.product_id
    WHERE p.status = 'paid';
    """
    columns, rows = execute_query(query)
    return {
        'columns': columns,
        'rows': [dict(row) for row in rows]
    }

@app.route('/api/cohort')
def cohort():
    """Get cohort analysis"""
    query = """
    WITH user_cohort AS (
      SELECT user_id, substr(first_order_date,1,7) AS cohort_month
      FROM users
      WHERE first_order_date IS NOT NULL
    ),
    orders_month AS (
      SELECT user_id, substr(order_date,1,7) AS order_month, SUM(order_value - COALESCE(discount_amount,0)) AS revenue
      FROM orders
      GROUP BY user_id, order_month
    )
    SELECT c.cohort_month, o.order_month, COUNT(DISTINCT o.user_id) AS active_users, ROUND(SUM(o.revenue), 2) AS revenue
    FROM user_cohort c
    JOIN orders_month o ON c.user_id = o.user_id
    GROUP BY c.cohort_month, o.order_month
    ORDER BY c.cohort_month, o.order_month
    LIMIT 50;
    """
    columns, rows = execute_query(query)
    return {
        'columns': columns,
        'rows': [dict(row) for row in rows]
    }

@app.route('/api/stats')
def stats():
    """Get overall statistics"""
    stats = {}
    
    # Total users
    _, rows = execute_query("SELECT COUNT(*) as count FROM users")
    stats['total_users'] = rows[0][0]
    
    # Total orders
    _, rows = execute_query("SELECT COUNT(*) as count FROM orders")
    stats['total_orders'] = rows[0][0]
    
    # Total revenue
    _, rows = execute_query("SELECT ROUND(SUM(amount), 2) as total FROM payments WHERE status = 'paid'")
    stats['total_revenue'] = rows[0][0] or 0
    
    # Total products
    _, rows = execute_query("SELECT COUNT(*) as count FROM products")
    stats['total_products'] = rows[0][0]
    
    return stats

if __name__ == '__main__':
    local_ip = get_local_ip()
    port = 8080
    print(f"\n{'='*60}")
    print(f"🚀 E-commerce Analytics Dashboard is running!")
    print(f"{'='*60}")
    print(f"📱 Access from other devices:")
    print(f"   http://{local_ip}:{port}")
    print(f"   http://localhost:{port}")
    print(f"{'='*60}\n")
    app.run(host='0.0.0.0', port=port, debug=True)

