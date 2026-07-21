"""
Simple Flask To-Do List App (v2)
New in this version:
  - Mark tasks as complete/incomplete
  - Assign a priority (Low / Medium / High) to each task
  - Completed tasks are visually struck through
  - Tasks are sorted so High priority shows first
"""
from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

# In-memory storage: list of dicts {"id", "text", "done", "priority"}
tasks = []
next_id = 1

PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}

PAGE = """
<!doctype html>
<html>
<head>
    <title>To-Do List</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 550px; margin: 40px auto; }
        h1 { color: #333; }
        li { margin-bottom: 10px; list-style: none; }
        form.add-form { margin-bottom: 20px; }
        input[type=text] { padding: 6px; width: 50%; }
        select { padding: 6px; }
        button { padding: 6px 12px; }
        .done { text-decoration: line-through; color: #888; }
        .priority-High { border-left: 4px solid #d9534f; padding-left: 8px; }
        .priority-Medium { border-left: 4px solid #f0ad4e; padding-left: 8px; }
        .priority-Low { border-left: 4px solid #5bc0de; padding-left: 8px; }
        .actions a { margin-left: 8px; text-decoration: none; }
        .del { color: red; }
        .toggle { color: green; }
    </style>
</head>
<body>
    <h1>My To-Do List</h1>
    <form class="add-form" method="POST" action="/add">
        <input type="text" name="task" placeholder="New task..." required>
        <select name="priority">
            <option value="Low">Low</option>
            <option value="Medium" selected>Medium</option>
            <option value="High">High</option>
        </select>
        <button type="submit">Add</button>
    </form>
    <ul>
        {% for t in tasks %}
            <li class="priority-{{ t.priority }}">
                <span class="{{ 'done' if t.done else '' }}">
                    [{{ t.priority }}] {{ t.text }}
                </span>
                <span class="actions">
                    <a class="toggle" href="/toggle/{{ t.id }}">
                        [{{ 'undo' if t.done else 'complete' }}]
                    </a>
                    <a class="del" href="/delete/{{ t.id }}">[delete]</a>
                </span>
            </li>
        {% else %}
            <li>No tasks yet. Add one above!</li>
        {% endfor %}
    </ul>
</body>
</html>
"""


def sorted_tasks():
    return sorted(tasks, key=lambda t: (t["done"], PRIORITY_ORDER.get(t["priority"], 3)))


@app.route("/")
def index():
    return render_template_string(PAGE, tasks=sorted_tasks())


@app.route("/add", methods=["POST"])
def add_task():
    global next_id
    text = request.form.get("task", "").strip()
    priority = request.form.get("priority", "Medium")
    if priority not in PRIORITY_ORDER:
        priority = "Medium"
    if text:
        tasks.append({"id": next_id, "text": text, "done": False, "priority": priority})
        next_id += 1
    return redirect(url_for("index"))


@app.route("/toggle/<int:task_id>")
def toggle_task(task_id):
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = not t["done"]
            break
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
