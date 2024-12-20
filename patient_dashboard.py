import sqlite3
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess


def open_dashboard(user, parent=None):
    print(f"Debug: User passed to open_dashboard: {user}")
    if not isinstance(user, dict) or 'uid' not in user:
        raise Exception(f"Invalid user object: {user}")

    conn = sqlite3.connect('open_dental_users.db')
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT name, age, gender, email, assigned_doctor, room_number
            FROM patients
            WHERE pid = ?
        """, (user['uid'],))
        patient_data = cursor.fetchone()

        if not patient_data:
            raise Exception("No patient data found for the given patient UID.")
    except Exception as e:
        messagebox.showerror("Database Error", f"Error fetching patient data: {e}")
        return
    finally:
        conn.close()

    patient_name, age, gender, email, assigned_doctor, room_number = patient_data

    dashboard = Toplevel(parent)
    dashboard.title("Patient Dashboard")
    dashboard.geometry("600x800")
    dashboard.configure(bg="#f0f4f8")
    dashboard.resizable(False, False)

    header = Frame(dashboard, bg="#4CAF50", height=80)
    header.pack(fill=X)
    Label(header, text="Patient Profile", font=("Arial", 24, "bold"), bg="#4CAF50", fg="white").pack(pady=20)

    info_frame = Frame(dashboard, bg="white", padx=20, pady=10)
    info_frame.pack(pady=10, fill=X)

    Label(info_frame, text=f"Name: {patient_name}", font=("Arial", 14), bg="white").pack(anchor=W, pady=5)
    Label(info_frame, text=f"Age: {age}", font=("Arial", 14), bg="white").pack(anchor=W, pady=5)
    Label(info_frame, text=f"Gender: {gender}", font=("Arial", 14), bg="white").pack(anchor=W, pady=5)
    Label(info_frame, text=f"Email: {email}", font=("Arial", 14), bg="white").pack(anchor=W, pady=5)
    Label(info_frame, text=f"Assigned Doctor: {assigned_doctor}", font=("Arial", 14), bg="white").pack(anchor=W, pady=5)
    Label(info_frame, text=f"Room Number: {room_number}", font=("Arial", 14), bg="white").pack(anchor=W, pady=5)

    def open_login_page():
        try:
            subprocess.Popen(["python3", "login.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open login.py: {e}")
    def terminate_session():
        """Terminate the session and show the login page."""
        dashboard.withdraw()
        open_login_page()

    footer = Frame(dashboard, bg="#f0f4f8", height=50)
    footer.pack(fill=X, side=BOTTOM, pady=10)
    Button(footer, text="Log Out", font=("Arial", 12), bg="#dc3545", fg="black", width=15, command=terminate_session).pack(pady=10)