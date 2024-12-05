from flask import Flask, jsonify
from config import get_delay, get_error
import time
import os
import random

app = Flask(__name__)


app.config['DELAY'] = get_delay() # Default: Uniform [15.0s, 30.0s]
app.config['ERROR'] = get_error() # Default: p(error) = 0

app.config['START_TIME'] = time.time()

@app.route('/status', methods=['GET'])
def status():
    # Simulate error
    if app.config['ERROR']:
        result = 'error'
    else:
        elapsed_time = time.time() - app.config['START_TIME']
        if elapsed_time < app.config['DELAY']:
            result = 'pending'
        else:
            result = 'completed'
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
