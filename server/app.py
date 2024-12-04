from flask import Flask, jsonify
import time
import os
import random

app = Flask(__name__)

# Configuration from environment variables
app.config['DELAY'] = float(os.environ.get('DELAY', '10.0'))  # Delay in seconds before status becomes 'completed'
app.config['ERROR_RATE'] = float(os.environ.get('ERROR_RATE', '0.0'))  # Probability of returning 'error'

# Record the start time
app.config['START_TIME'] = time.time()

@app.route('/status', methods=['GET'])
def status():
    # Simulate error based on ERROR_RATE
    if random.random() < app.config['ERROR_RATE']:
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
