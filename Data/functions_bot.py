import json
import time

# Function to load the data from the data.json file
def load_data():
    try:
        with open("./data.json", "r") as data_file:
            return json.load(data_file)
    except FileNotFoundError:
        return {}
    
# Function to save the data to the data.json file
def save_data(data):
    with open("./data.json", "w") as file:
        json.dump(data, file)

# Function to load the command history from the data.json file
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

# Function to add points to users
def add_points(user_id, points):
    data = load_data()
    user_id_str = str(user_id)
    current_time = int(time.time())

    if user_id_str not in data:
        data[user_id_str] = {"points": points, "last_claimed": current_time}
    else:
        data[user_id_str]["points"] += points
        data[user_id_str]["last_claimed"] = current_time

    save_data(data)