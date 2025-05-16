
# 🧠 Django Quiz Game

A simple quiz game built with Django where users answer multiple-choice questions and earn points.

---

## 🎯 Purpose

To demonstrate core Django concepts:

* Views, Templates, URLs
* Forms & Sessions
* Basic game logic using Python lists

---

## 🛠️ Tech Stack

* Python 3 🐍
* Django 5.x 🌐

---

## ⚙️ How to Run

```bash
git clone [YOUR_REPO_URL]
cd django_quiz_project

python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Visit 👉 `http://127.0.0.1:8000/quiz/start/`

---

## 🧩 How It Works

* Questions stored in a Python list (`views.py`)
* Player selects answers via forms
* Score tracked in Django sessions
* Result page shows score & accuracy
* Replay option available

---

## 📁 Key Files

* `views.py` – quiz logic
* `urls.py` – routing
* `templates/` – HTML pages
* `settings.py` – config
![IMAGE 2025-05-16 11:00:51](https://github.com/user-attachments/assets/b4c04945-d0e8-4316-b3f9-2d49085640ea)
![IMAGE 2025-05-16 11:00:59](https://github.com/user-attachments/assets/fa31704b-7660-4cf0-9ed1-d09d173bb4a7)


