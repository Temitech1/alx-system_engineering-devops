#!/usr/bin/python3
"""
Using a REST API, for a given employee ID,
returns information about their TODO list progress.
"""

import requests
from sys import argv

if __name__ == "__main__":
    if len(argv) != 2:
        print("Usage: ./todo.py <employee_id>")
        exit(1)

    employee_id = argv[1]
    url = f"https://jsonplaceholder.typicode.com/users/{employee_id}/todos"

    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch employee TODO list.")
        exit(1)

    todos = response.json()
    employee_name = todos[0]["userId"]
    total_tasks = len(todos)
    completed_tasks = sum(task["completed"] for task in todos)

    print(f"Employee {employee_name} is done with tasks({completed_tasks}/{total_tasks}):")

    for task in todos:
        if task["completed"]:
            print(f"\t {task['title']}")
