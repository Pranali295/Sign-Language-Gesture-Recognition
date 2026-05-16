import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import hashlib
import subprocess
import time
import shutil

# --------------------------
# Global
# --------------------------
attempts = 3

# --------------------------
# Load/Save Users
# --------------------------
def load_users():
    with open("users.json", "r") as f:
        return json.load(f)

def save_users(data):
    with open("users.json", "w") as f:
        json.dump(data, f, indent=4)

# --------------------------
# Main Window
# --------------------------
root = tk.Tk()
root.title("AI Sign Language System")
root.geometry("500x450")
root.configure(bg="#1e1e2f")

# --------------------------
# Utility Functions
# --------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def log_activity(user):
    with open("log.txt", "a") as f:
        f.write(f"{user} logged in at {time.ctime()}\n")

# --------------------------
# LOGIN FUNCTION
# --------------------------
def login():
    global attempts
    users = load_users()

    username = entry_user.get()
    password = hash_password(entry_pass.get())

    if username in users and users[username]["password"] == password:
        role = users[username]["role"]

        log_activity(username)

        messagebox.showinfo("Success", f"Welcome {username} ({role})")
        open_dashboard(username, role)

    else:
        attempts -= 1
        messagebox.showerror("Error", f"Invalid Credentials\nAttempts left: {attempts}")

        if attempts == 0:
            messagebox.showerror("Blocked", "Too many attempts!")
            root.destroy()

# --------------------------
# DASHBOARD
# --------------------------
def open_dashboard(user, role):
    dashboard = tk.Toplevel(root)
    dashboard.title("Dashboard")
    dashboard.geometry("500x500")
    dashboard.configure(bg="#282a36")

    tk.Label(dashboard, text=f"Welcome {user}", fg="white", bg="#282a36",
             font=("Arial", 18)).pack(pady=15)

    tk.Label(dashboard, text=f"Role: {role}", fg="lightgreen", bg="#282a36").pack()

    # 🔥 Real-time Clock
    def update_time():
        current = time.strftime("%H:%M:%S")
        clock_label.config(text=f"Time: {current}")
        dashboard.after(1000, update_time)

    clock_label = tk.Label(dashboard, fg="white", bg="#282a36")
    clock_label.pack()
    update_time()

    # 🔥 Status Label
    status_label = tk.Label(dashboard, text="Status: Idle",
                            fg="orange", bg="#282a36")
    status_label.pack(pady=5)

    # Start Model
    def start_model():
        status_label.config(text="Status: Running", fg="green")
        subprocess.run(["python", "hand_gesture_recognition.py"])
        status_label.config(text="Status: Stopped", fg="red")

    tk.Button(dashboard, text="▶ Start Detection",
              command=start_model,
              bg="#50fa7b", fg="black", width=20).pack(pady=10)

    tk.Button(dashboard, text="❌ Exit",
              command=dashboard.destroy,
              bg="#ff5555", fg="white", width=20).pack(pady=10)

    # --------------------------
    # ADMIN FEATURES
    # --------------------------
    if role == "admin":

        tk.Label(dashboard, text="Admin Dashboard",
                 fg="yellow", bg="#282a36",
                 font=("Arial", 14)).pack(pady=10)

        users_data = load_users()
        tk.Label(dashboard, text=f"Total Users: {len(users_data)}",
                 fg="cyan", bg="#282a36").pack()

        btn_frame = tk.Frame(dashboard, bg="#282a36")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="👥 Manage Users",
                  command=manage_users_window,
                  width=18, bg="#bd93f9").grid(row=0, column=0, padx=10)

        tk.Button(btn_frame, text="📊 View Logs",
                  command=view_logs,
                  width=18, bg="#8be9fd").grid(row=0, column=1, padx=10)

        tk.Button(btn_frame, text="⬇ Export Logs",
                  command=export_logs,
                  width=18, bg="#f1fa8c").grid(row=1, column=0, columnspan=2, pady=10)

# --------------------------
# LOGS
# --------------------------
def view_logs():
    try:
        with open("log.txt", "r") as f:
            logs = f.read()
    except:
        logs = "No logs found."

    log_window = tk.Toplevel(root)
    log_window.title("Logs")

    text = tk.Text(log_window, width=60, height=20)
    text.pack()
    text.insert(tk.END, logs)

def export_logs():
    try:
        shutil.copy("log.txt", "backup_logs.txt")
        messagebox.showinfo("Success", "Logs exported!")
    except:
        messagebox.showerror("Error", "No logs to export!")

# --------------------------
# USER MANAGEMENT
# --------------------------
def manage_users_window():
    win = tk.Toplevel(root)
    win.title("Manage Users")
    win.geometry("400x400")

    tk.Label(win, text="User Management", font=("Arial", 14)).pack(pady=10)

    listbox = tk.Listbox(win, width=30)
    listbox.pack(pady=10)

    def load_list():
        listbox.delete(0, tk.END)
        data = load_users()
        for user in data:
            listbox.insert(tk.END, user)

    load_list()

    def delete_user():
        selected = listbox.get(tk.ACTIVE)

        if selected == "admin":
            messagebox.showerror("Error", "Cannot delete admin!")
            return

        data = load_users()
        del data[selected]
        save_users(data)

        load_list()
        messagebox.showinfo("Deleted", "User removed!")

    def change_password():
        selected = listbox.get(tk.ACTIVE)

        new_pass = simpledialog.askstring("Password", "Enter new password:", show='*')
        if not new_pass:
            return

        data = load_users()
        data[selected]["password"] = hash_password(new_pass)
        save_users(data)

        messagebox.showinfo("Success", "Password updated!")

    tk.Button(win, text="Delete User", command=delete_user, bg="#ff5555").pack(pady=5)
    tk.Button(win, text="Change Password", command=change_password, bg="#50fa7b").pack(pady=5)

# --------------------------
# LOGIN UI
# --------------------------
tk.Label(root, text="🔐 Secure Login", fg="white", bg="#1e1e2f",
         font=("Arial", 20)).pack(pady=20)

frame = tk.Frame(root, bg="#1e1e2f")
frame.pack(pady=10)

tk.Label(frame, text="Username", fg="white", bg="#1e1e2f").grid(row=0, column=0, pady=5)
entry_user = tk.Entry(frame)
entry_user.grid(row=0, column=1)

tk.Label(frame, text="Password", fg="white", bg="#1e1e2f").grid(row=1, column=0, pady=5)
entry_pass = tk.Entry(frame, show="*")
entry_pass.grid(row=1, column=1)

# 🔥 Show Password
show_var = tk.BooleanVar()

def toggle_password():
    entry_pass.config(show="" if show_var.get() else "*")

tk.Checkbutton(root, text="Show Password",
               variable=show_var,
               command=toggle_password,
               bg="#1e1e2f", fg="white").pack()

tk.Button(root, text="Login", command=login,
          bg="#6272a4", fg="white", width=15).pack(pady=20)

tk.Label(root, text="⚠ Authorized Users Only", fg="red", bg="#1e1e2f").pack()

root.mainloop()