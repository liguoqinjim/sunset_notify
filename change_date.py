import json
from datetime import date

def change_since_date():
    filepath = "crawler/config.json"

    # Read the config file
    with open(filepath, 'r') as f:
        config = json.load(f)
    
    # Update the since_date field with today's date
    config['since_date'] = date.today().strftime('%Y-%m-%d')
    
    # Write the updated config file
    with open(filepath, 'w') as f:
        json.dump(config, f, indent=4)

if __name__ == "__main__":
    change_since_date()