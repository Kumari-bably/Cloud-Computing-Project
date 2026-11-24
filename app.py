
from flask import Flask
import redis
import os

app = Flask(__name__)

# Redis connection
redis_url = os.environ.get("REDIS_URL")

if redis_url:
    # Render Redis / Valkey connection
    r = redis.from_url(
        redis_url,
        decode_responses=True
    )
else:
    # Local Docker Compose connection
    redis_host = os.environ.get("REDIS_HOST", "localhost")

    r = redis.Redis(
        host=redis_host,
        port=6379,
        decode_responses=True
    )


# Home Page
@app.route("/")
def home():
    try:
        visitors = r.incr("visitor_count")

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Visitor Counter App</title>

            <meta name="viewport"
                  content="width=device-width, initial-scale=1.0">

            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: #f0f4f8;
                    text-align: center;
                    padding: 50px 15px;
                }}

                .container {{
                    background: white;
                    max-width: 500px;
                    margin: auto;
                    padding: 35px 20px;
                    border-radius: 15px;
                    box-shadow: 0 4px 15px
                                rgba(0,0,0,0.1);
                }}

                h1 {{
                    color: #2563eb;
                }}

                .count {{
                    font-size: 55px;
                    font-weight: bold;
                    color: #16a34a;
                    margin: 20px;
                }}

                p {{
                    color: #555;
                    font-size: 18px;
                }}

                .footer {{
                    font-size: 14px;
                    margin-top: 25px;
                    color: #888;
                }}
            </style>
        </head>

        <body>
            <div class="container">

                <h1>Visitor Counter App</h1>

                <p>Total Visitors</p>

                <div class="count">
                    {visitors}
                </div>

                <p>Welcome to our Cloud Computing Project!</p>

                <div class="footer">
                    Powered by Flask and Redis
                </div>

            </div>
        </body>
        </html>
        """

    except redis.RedisError:
        return "Redis connection failed", 503


# Health Check API
@app.route("/health")
def health():
    try:
        r.ping()
        return "Application is healthy!", 200

    except redis.RedisError:
        return "Redis is unavailable", 503


# Run Application
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
