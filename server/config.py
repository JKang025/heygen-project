import random

DELAY_CONFIG = {
    'model': 'uniform',  # Choose between 'fixed', 'uniform', or 'gaussian'
    'params': {
        'delay': 20.0,  # Used for 'fixed'
        'min_delay': 15.0,  # Used for 'uniform'
        'max_delay': 30.0,  # Used for 'uniform'
        'mean_delay': 10.0,  # Used for 'gaussian'
        'stddev_delay': 2.0,  # Used for 'gaussian'
    }
}

def get_delay():
    """Compute delay based on the configured model and parameters."""
    delay_model = DELAY_CONFIG.get('model', 'fixed')
    params = DELAY_CONFIG.get('params', {})

    if delay_model == 'fixed':
        delay = params.get('delay', 10.0)
        return delay

    elif delay_model == 'uniform':
        min_delay = params.get('min_delay', 5.0)
        max_delay = params.get('max_delay', 15.0)
        return random.uniform(min_delay, max_delay) 

    elif delay_model == 'gaussian':
        mean_delay = params.get('mean_delay', 10.0)
        stddev_delay = params.get('stddev_delay', 2.0)
        return max(0, random.gauss(mean_delay, stddev_delay)) 

    else:
        raise ValueError(f"Unknown DELAY_MODEL: {delay_model}")



ERROR_CONFIG = {
    'model': 'fixed',  # Choose between 'fixed', 'uniform', or 'gaussian'
    'params': {
        'probability': 0.0,  # Used for 'fixed'
        'min_probability': 0.05,  # Used for 'uniform'
        'max_probability': 0.15,  # Used for 'uniform'
        'mean_probability': 0.1,  # Used for 'gaussian'
        'stddev_probability': 0.02,  # Used for 'gaussian'
    }
}

def get_error():
    """Compute the probability of error based on the configured model and parameters."""
    error_model = ERROR_CONFIG.get('model', 'fixed')
    params = ERROR_CONFIG.get('params', {})

    if error_model == 'fixed':
        probability = params.get('probability', 0.1)
        return random.random() < probability  #

    elif error_model == 'uniform':
        min_probability = params.get('min_probability', 0.05)
        max_probability = params.get('max_probability', 0.15)
        probability = random.uniform(min_probability, max_probability) 
        return random.random() < probability

    elif error_model == 'gaussian':
        mean_probability = params.get('mean_probability', 0.1)
        stddev_probability = params.get('stddev_probability', 0.02)
        probability = max(0, min(1, random.gauss(mean_probability, stddev_probability))) 
        return random.random() < probability

    else:
        raise ValueError(f"Unknown ERROR_MODEL: {error_model}")