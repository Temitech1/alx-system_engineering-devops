#!/usr/bin/python3
"""
Using a REST API, exports all tasks from all employees to a JSON file.
"""
import json
import requests


def get_user_data(users, user_id):
    """
    Retrieve the user's name and username from the users list.
    """
    for user in users:
        if user["id"] == user_id:
            return user["name"], user["username"]
    return "Unknown", "Unknown"


if __name__ == "__main__":
    users_url = "https://jsonplaceholder.typicode.com/users"
    todos_url = "https://jsonplaceholder.typicode.com/todos"

    users_response = requests.get(users_url)
    if users_response.status_code != 200:
        print("Failed to fetch users.")
        exit(1)

    users = users_response.json()

    todos_response = requests.get(todos_url)
    if todos_response.status_code != 200:
        print("Failed to fetch TODO list.")
        exit(1)

    todos = todos_response.json()

    # Organize tasks by user ID
    tasks_by_user = {}
    for todo in todos:
        user_id = todo["userId"]
        user_name, user_username = get_user_data(users, user_id)
        task_data = {
            "username": user_username,
            "task": todo["title"],
            "completed": todo["completed"]
        }

        if user_id not in tasks_by_user:
            tasks_by_user[user_id] = []

        tasks_by_user[user_id].append(task_data)

    # Export all tasks to JSON
    json_filename = "todo_all_employees.json"
    with open(json_filename, "w") as jsonfile:
        json.dump(tasks_by_user, jsonfile, indent=4)

    print(f"Task data exported to {json_filename}")
