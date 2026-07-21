"""
Simple Flask To-Do List App (v1)
Features: add a task, view all tasks, delete a task.
"""
from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

# In-memory storage: list of dicts {"id": int, "text": str}
tasks = []
next_id = 1

PAGE = """
<!doctype html>
<html>
<head>
    <title>To-Do List</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 500px; margin: 40px auto; }
        h1 { color: #333; }
        li { margin-bottom: 8px; }
        form { margin-bottom: 20px; }
        input[type=text] { padding: 6px; width: 70%; }
        button { padding: 6px 12px; }
        .del { color: red; text-decoration: none; margin-left: 10px; }
    </style>
</head>
<body>
    <h1>My To-Do List</h1>
    <form method="POST" action="/add">
        <input type="text" name="task" placeholder="New task..." required>
        <button type="submit">Add</button>
    </form>
    <ul>
        {% for t in tasks %}
            <li>{{ t.text }} <a class="del" href="/delete/{{ t.id }}">[delete]</a></li>
        {% else %}
            <li>No tasks yet. Add one above!</li>
        {% endfor %}
    </ul>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(PAGE, tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    global next_id
    text = request.form.get("task", "").strip()
    if text:
        tasks.append({"id": next_id, "text": text})
        next_id += 1
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
