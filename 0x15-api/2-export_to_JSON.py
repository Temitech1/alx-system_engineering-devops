#!/usr/bin/python3
"""
Using a REST API, for a given employee ID,
returns information about their TODO list progress
and exports all their tasks to a JSON file.
"""
import json
import requests
from sys import argv


def get_user_data(users, user_id):
    """
    Retrieve the user's name and username from the users list.
    """
    for user in users:
        if user["id"] == int(user_id):
            return user["name"], user["username"]
    return "Unknown", "Unknown"


if __name__ == "__main__":
    if len(argv) != 2:
        print("Usage: ./todo.py <user_id>")
        exit(1)

    user_id = argv[1]
    users_url = "https://jsonplaceholder.typicode.com/users"
    todos_url = f"https://jsonplaceholder.typicode.com/users/{user_id}/todos"

    users_response = requests.get(users_url)
    if users_response.status_code != 200:
        print("Failed to fetch users.")
        exit(1)

    users = users_response.json()
    user_name, user_username = get_user_data(users, user_id)

    todos_response = requests.get(todos_url)
    if todos_response.status_code != 200:
        print("Failed to fetch user TODO list.")
        exit(1)

    todos = todos_response.json()
    total_tasks = len(todos)
    completed_tasks = sum(task["completed"] for task in todos)

    print(f"Employee {user_name} is done with tasks ({completed_tasks}/{total_tasks}):")

    # Export all tasks to JSON
    json_filename = f"{user_id}.json"
    task_data = [
        {
            "task": task["title"],
            "completed": task["completed"],
            "username": user_username
        }
        for task in todos
    ]
    json_data = {
        "USER_ID": user_id,
        "tasks": task_data
    }

    with open(json_filename, "w") as jsonfile:
        json.dump(json_data, jsonfile, indent=4)

    print(f"\nTask data exported to {json_filename}")
