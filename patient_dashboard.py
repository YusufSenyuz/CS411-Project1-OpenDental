import sqlite3
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

def open_dashboard(user):
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
            raise Exception("No patient data found for this user UID.")
    except Exception as e:
        messagebox.showerror("Database Error", f"Error fetching patient data: {e}")
        return
    finally:
        conn.close()

    patient_name, age, gender, email, assigned_doctor, room_number = patient_data

    # Create the main window
    dashboard = Tk()
    dashboard.title("Patient Dashboard")
    dashboard.geometry("600x800")
    dashboard.configure(bg="#f0f4f8")
    dashboard.resizable(False, False)

    # Header Section
    header = Frame(dashboard, bg="#4CAF50", height=80)
    header.pack(fill=X)
    Label(header, text="Patient Profile", font=("Arial", 24, "bold"), bg="#4CAF50", fg="white").pack(pady=20)

    # Profile Picture Section
    profile_frame = Frame(dashboard, bg="white", padx=20, pady=20, relief=RAISED, bd=2)
    profile_frame.pack(pady=20, padx=20)

    try:
        img = Image.open("images/profile.png")
        img = img.resize((150, 150), Image.Resampling.LANCZOS)  # Use LANCZOS for high-quality resampling
        profile_pic = ImageTk.PhotoImage(img)
        profile_label = Label(profile_frame, image=profile_pic, bg="white")
        profile_label.image = profile_pic
        profile_label.pack(pady=10)
    except Exception as e:
        messagebox.showwarning("Image Error", f"Unable to load profile picture: {e}")

    # Patient Information Section
    info_frame = Frame(profile_frame, bg="white", padx=20, pady=10)
    info_frame.pack(pady=10, fill=X)

    Label(info_frame, text=f"Name: {patient_name}", font=("Arial", 14), bg="white").pack(anchor=W, pady=5)
    Label(info_frame, text=f"Age: {age}", font=("Arial", 14), bg="white").pack(anchor=W, pady=5)
    Label(info_frame, text=f"Gender: {gender}", font=("Arial", 14), bg="white").pack(anchor=W, pady=5)
    Label(info_frame, text=f"Email: {email}", font=("Arial", 14), bg="white").pack(anchor=W, pady=5)
    Label(info_frame, text=f"Assigned Doctor: {assigned_doctor}", font=("Arial", 14), bg="white").pack(anchor=W, pady=5)
    Label(info_frame, text=f"Room Number: {room_number}", font=("Arial", 14), bg="white").pack(anchor=W, pady=5)

    # Footer Section
    footer = Frame(dashboard, bg="#f0f4f8", height=50)
    footer.pack(fill=X, side=BOTTOM, pady=10)
    Button(footer, text="Log Out", font=("Arial", 12), bg="#dc3545", fg="black", width=15, command=dashboard.destroy).pack(pady=10)

    dashboard.mainloop()