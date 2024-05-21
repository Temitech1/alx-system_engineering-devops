#!/usr/bin/python3
"""
Using a REST API, for a given employee ID,
returns information about their TODO list progress
and exports their tasks to a CSV file.
"""
import csv
import requests
from sys import argv


def get_user_name(users, user_id):
    """
    Retrieve the user name from the users list based on the user ID.
    """
    for user in users:
        if user["id"] == int(user_id):
            return user["name"]
    return "Unknown"


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
    user_name = get_user_name(users, user_id)

    todos_response = requests.get(todos_url)
    if todos_response.status_code != 200:
        print("Failed to fetch user TODO list.")
        exit(1)

    todos = todos_response.json()
    total_tasks = len(todos)
    completed_tasks = sum(task["completed"] for task in todos)

    print(f"Employee {user_name} is done with tasks"
          f"({completed_tasks}/{total_tasks}):")

    for task in todos:
        if task["completed"]:
            print(f"\t {task['title']}")

    # Export tasks to CSV
    csv_filename = f"{user_id}.csv"
    with open(csv_filename, "w", newline="") as csvfile:
        fieldnames = ["USER_ID", "USERNAME", "TASK_COMPLETED_STATUS", "TASK_TITLE"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for task in todos:
            writer.writerow({
                "USER_ID": user_id,
                "USERNAME": user_name,
                "TASK_COMPLETED_STATUS": "True" if task["completed"] else "False",
                "TASK_TITLE": task["title"]
            })

    print(f"Task data exported to {csv_filename}")
