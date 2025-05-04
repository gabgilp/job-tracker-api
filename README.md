# Job Tracker API

A FastAPI-based backend for tracking job applications.

---

## 🚀 Getting Started on Linux (Raspbian OS)

This guide assumes you're using a Linux environment (developed and tested on Raspbian OS).

### 📦 Prerequisites

- **PostgreSQL** must be installed on your local machine.
- Python environment (recommended: Python 3.11+)
- Required Python dependencies installed (see `requirements.txt`)

---

### ⚙️ Initial Setup (Recommended for Smooth Automation)

To enable automatic PostgreSQL startup/shutdown with the API:

#### 1. ✅ Auto-login to PostgreSQL (Skip Password Prompt)

- Create a `.pgpass` file in your home directory:
  ```bash
  nano ~/.pgpass
  ```
  Add the following line (replace with your actual credentials):

  ```
  localhost:5432:*:your_db_user:your_password
  ```

- Set secure permissions:
  ```bash
  chmod 600 ~/.pgpass
  ```

> 💡 If you skip this step, the API will still work — but you’ll be prompted to enter your PostgreSQL password manually each time.

---

#### 2. 🔒 Auto-stop PostgreSQL on API Shutdown

To allow FastAPI to stop PostgreSQL automatically when shutting down:

- Open the sudoers file:
  ```bash
  sudo visudo
  ```

- Add this line at the end (replace `yourusername` with your actual username):
  ```
  yourusername ALL=NOPASSWD: /path/to/systemctl stop postgresql
  ```

- Find the correct systemctl path with:
  ```bash
  which systemctl
  ```

> ⚠️ **Warning:** If you're using PostgreSQL for other services, it's recommended to remove or comment out this line in `tracker/main.py`:
>
> ```python
> subprocess.run(["sudo", "systemctl", "stop", "postgresql"])
> ```
> Otherwise, shutting down the API will stop PostgreSQL globally.

---

### ▶️ Running the API

After completing the setup steps above, start the API using:

```bash
./run_api.sh
```

This will:
- Start PostgreSQL (if not already running)
- Connect the FastAPI app to your database
- Run the application on `http://localhost:8000`

---

## 📝 Notes

- Database settings are stored in `.env`. Ensure this file is properly configured and not committed to version control.
- `.venv`, `.env`, and other sensitive files should be listed in `.gitignore`.

---

## 📂 Project Structure

```
job-tracker-api/
│
├── run_api.sh
├── .env
├── .gitignore
├── README.md
└── tracker/
    ├── main.py
    ├── db.py
    ├── models/
    ├── routers/
    └── ...
```

---

## 📬 Contact

If you have questions or run into issues, feel free to open an issue or start a discussion.

---
