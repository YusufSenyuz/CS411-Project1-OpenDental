import sqlite3
from tkinter import *
from tkinter import messagebox
from two_factor_auth import open_2fa_page

conn = sqlite3.connect('open_dental_users.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT, password TEXT, email TEXT, role TEXT)''')

conn.commit()

root = Tk()
root.title("Open Dental - Login")
root.geometry("550x370")
root.configure(bg="#e0e0e0")
root.resizable(False, False)

def open_2fa(username, email):
    root.destroy()
    open_2fa_page(username, email)

def check_login():
    username = username_entry.get()
    password = password_entry.get()
    selected_role = role_filter.get()

    c.execute("SELECT username FROM users WHERE role=?", (selected_role,))
    expected_user = c.fetchone()

    if expected_user and expected_user[0] != username:
        messagebox.showerror("Error", "Role and username do not match.")
        return

    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()

    if user:
        open_2fa(username, user[2])
    else:
        messagebox.showerror("Error", "Invalid username or password.")

def autofill_username(event):
    role = role_filter.get()

    c.execute("SELECT username FROM users WHERE role=?", (role,))
    user = c.fetchone()

    if user:
        username_entry.delete(0, END)
        username_entry.insert(0, user[0])

def get_roles():
    c.execute("SELECT DISTINCT role FROM users")
    roles = c.fetchall()
    return [role[0] for role in roles]

Label(root, text="Log On", font=("Arial", 20), bg="#e0e0e0", fg="black").place(x=80, y=30)

Label(root, text="Select Role", bg="#e0e0e0", font=("Arial", 12)).place(x=80, y=100)
role_filter = StringVar(root)
role_filter.set("Select Role")

user_roles = get_roles()

role_menu = OptionMenu(root, role_filter, *user_roles, command=autofill_username)
role_menu.place(x=180, y=100, width=150)

Label(root, text="Username", bg="#e0e0e0", font=("Arial", 12)).place(x=80, y=160)
username_entry = Entry(root, width=30)
username_entry.place(x=180, y=160)

Label(root, text="Password", bg="#e0e0e0", font=("Arial", 12)).place(x=80, y=220)
password_entry = Entry(root, show="*", width=30)
password_entry.place(x=180, y=220)

Button(root, text="Login", command=check_login, width=15, bg="#4CAF50", fg="black", font=("Arial", 12)).place(x=250, y=270)

root.mainloop()

conn.close()
