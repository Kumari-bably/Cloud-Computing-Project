
from flask import Flask
import redis
import os

app = Flask(__name__)

# Connect to Redis
redis_host = os.environ.get("REDIS_HOST", "localhost")

r = redis.Redis(
    host=redis_host,
    port=6379,
    decode_responses=True
)

@app.route("/")
def home():
    try:
        visitors = r.incr("visitor_count")

        return f"""
        <html>
        <head>
            <title>Visitor Counter App</title>
            <style>
                body {{
                    font-family: Arial;
                    text-align: center;
                    background: #f0f4f8;
                    padding: 80px;
                }}
                .card {{
                    background: white;
                    padding: 40px;
                    border-radius: 15px;
                    display: inline-block;
                    box-shadow: 0 4px 15px #cccccc;
                }}
                h1 {{ color: #2563eb; }}
                h2 {{ color: #16a34a; font-size: 45px; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h1>Welcome to Visitor Counter</h1>
                <p>Total Visitors</p>
                <h2>{visitors}</h2>
                <p>Powered by Flask and Redis</p>
            </div>
        </body>
        </html>
        """
    except redis.RedisError:
        return "Redis connection failed", 503

@app.route("/health")
def health():
    try:
        r.ping()
        return "Application is healthy!", 200
    except redis.RedisError:
        return "Redis is unavailable", 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
