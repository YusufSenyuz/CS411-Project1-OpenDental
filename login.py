import sqlite3
from tkinter import *
from tkinter import messagebox
from two_factor_auth import open_2fa_page

def attempt_login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    conn = sqlite3.connect('open_dental_users.db')
    cursor = conn.cursor()

    try:
        # Fetch user details from the database
        cursor.execute("SELECT username, email, role FROM users WHERE username = ? AND password = ?", (username, password))
        user_data = cursor.fetchone()

        if user_data:
            user = {
                'username': user_data[0],
                'email': user_data[1],
                'role': user_data[2],
            }
            messagebox.showinfo("Login Successful", f"Welcome, {user['username']}!")
            login_window.destroy()  # Close the login window
            open_2fa_page(user)  # Open the 2FA verification page
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
    finally:
        conn.close()

# GUI for Login Page
login_window = Tk()
login_window.title("Hospital Management System - Login")
login_window.geometry("400x300")
login_window.configure(bg="#f0f0f0")
login_window.resizable(False, False)

# Title Label
Label(login_window, text="Login", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=20)

# Username Field
Label(login_window, text="Username:", font=("Arial", 12), bg="#f0f0f0").pack(anchor=W, padx=50, pady=5)
username_entry = Entry(login_window, width=30, font=("Arial", 12))
username_entry.pack(pady=5)

# Password Field
Label(login_window, text="Password:", font=("Arial", 12), bg="#f0f0f0").pack(anchor=W, padx=50, pady=5)
password_entry = Entry(login_window, width=30, font=("Arial", 12), show="*")
password_entry.pack(pady=5)

# Login Button
Button(login_window, text="Login", font=("Arial", 12), bg="#4CAF50", fg="white", width=15, command=attempt_login).pack(pady=20)

# Run the Application
login_window.mainloop()