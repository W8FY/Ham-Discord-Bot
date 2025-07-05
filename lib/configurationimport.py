import yaml

# Load in config from config.yml
def load_config_params(filepath):
    with open(str(filepath), 'r') as file:
        config_params = yaml.safe_load(file)
    return config_params