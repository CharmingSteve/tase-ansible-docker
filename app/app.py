from flask import Flask, render_template
import redis
import os
import socket

app = Flask(__name__)

# Connect to Redis using environment variables
redis_host = os.environ.get('REDIS_HOST', 'redis')
redis_port = int(os.environ.get('REDIS_PORT', 6379))
redis_client = redis.Redis(host=redis_host, port=redis_port)

@app.route('/')
def hello():
    # Increment visit counter
    visits = redis_client.incr('hits')
    
    # Get hostname for container identification
    hostname = socket.gethostname()
    
    return render_template('index.html', 
                          visits=visits, 
                          hostname=hostname)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
