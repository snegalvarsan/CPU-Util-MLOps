from flask import Flask, render_template_string
import os
import psycopg2
import psutil
from datetime import datetime

app = Flask(__name__)

# DB connection parameters
DB_NAME = os.environ.get("POSTGRES_DB")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_HOST = os.environ.get("POSTGRES_HOST")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>System Metrics Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding-top: 40px; }
        table { margin: 0 auto; border-collapse: collapse; }
        th, td { padding: 10px 20px; border: 1px solid #ccc; }
        h1 { margin-bottom: 20px; }
    </style>
</head>
<body>
    <h1>CPU & Memory Usage (Latest)</h1>
    <table>
        <tr><th>Timestamp</th><th>CPU (%)</th><th>Memory (%)</th></tr>
        {% for row in data %}
        <tr><td>{{ row[0] }}</td><td>{{ row[1] }}</td><td>{{ row[2] }}</td></tr>
        {% endfor %}
    </table>
</body>
</html>
"""

def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )

def create_table_if_not_exists():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS metrics (
                    id SERIAL PRIMARY KEY,
                    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    cpu FLOAT,
                    memory FLOAT
                );
            """)
        conn.commit()

@app.route('/')
def dashboard():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT time, cpu, memory FROM metrics ORDER BY time DESC LIMIT 5;")
            data = cur.fetchall()
    return render_template_string(HTML_TEMPLATE, data=data)

@app.route('/metrics')
def metrics():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO metrics (cpu, memory) VALUES (%s, %s);", (cpu, memory))
        conn.commit()

    return f"Metrics recorded: CPU={cpu}%, Memory={memory}%"

if __name__ == '__main__':
    create_table_if_not_exists()
    app.run(host='0.0.0.0', port=5000)
