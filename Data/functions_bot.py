import json

def load_command_history():
    try:
        with open("./data.json", "r") as data_history:
            return json.load(data_history)
    except FileNotFoundError:
        return {}

# Function to save command history to the data.json file
def save_command_history(data_history):
    with open("./data.json", "w") as file:
        json.dump(data_history, file)