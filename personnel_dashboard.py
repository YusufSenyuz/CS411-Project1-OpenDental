import sqlite3
from tkinter import *
from tkinter.ttk import Treeview, Style
from tkinter import messagebox
import subprocess


from patient_dashboard import open_dashboard


def personnel_dashboard(user):
    print(f"Debug: Entering personnel_dashboard with user: {user}")

    if not isinstance(user, dict) or 'uid' not in user:
        raise ValueError("Invalid user object passed to personnel_dashboard.")

    personnel_uid = user['uid']
    print(f"Debug: Personnel UID is {personnel_uid}")

    # Connect to the database
    conn = sqlite3.connect('open_dental_users.db')
    cursor = conn.cursor()

    try:
        # Fetch personnel details
        cursor.execute("""
            SELECT name, age, gender, email, role, hospital_name
            FROM personnel
            WHERE per_id = ?
        """, (personnel_uid,))
        personnel_data = cursor.fetchone()

        if not personnel_data:
            raise Exception(f"No personnel data found for UID {personnel_uid}")

        name, age, gender, email, role, hospital_name = personnel_data

        # Fetch assigned patients
        cursor.execute("""
            SELECT p.pid, p.name, p.age, p.gender, p.room_number
            FROM patients p
            INNER JOIN patient_assignments pa ON p.pid = pa.patient_pid
            WHERE pa.personnel_pid = ?
        """, (personnel_uid,))
        assigned_patients = cursor.fetchall()
        print(f"Debug: Found assigned patients: {assigned_patients}")

    except Exception as e:
        print(f"Error fetching personnel or patient data: {e}")
        messagebox.showerror("Database Error", f"Error: {e}")
        return
    finally:
        conn.close()

    # GUI Setup for Personnel Dashboard
    dashboard = Toplevel()  # Open as a separate window
    dashboard.title(f"{name}'s Dashboard")
    dashboard.geometry("900x700")
    dashboard.configure(bg="#f0f4f8")

    # Header Section
    header = Frame(dashboard, bg="#4CAF50", height=80)
    header.pack(fill=X)
    Label(header, text=f"{name}'s Dashboard", font=("Arial", 20), bg="#4CAF50", fg="white").pack()

    # Personnel Information Section
    info_frame = Frame(dashboard, bg="white", padx=10, pady=10, relief=RAISED, bd=2)
    info_frame.pack(padx=10, pady=10, fill=X)

    Label(info_frame, text=f"Name: {name}", font=("Arial", 14)).pack(anchor=W)
    Label(info_frame, text=f"Email: {email}", font=("Arial", 14)).pack(anchor=W)
    Label(info_frame, text=f"Role: {role}", font=("Arial", 14)).pack(anchor=W)
    Label(info_frame, text=f"Hospital: {hospital_name}", font=("Arial", 14)).pack(anchor=W)

    # Buttons Section
    menu_frame = Frame(dashboard, bg="white", padx=10, pady=10)
    menu_frame.pack(fill=X, pady=10)

    # implement the show all doctors button
    # GUI for All Doctors
    # Configure styles
    style = Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background="#F9F9F9",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#F9F9F9")
    style.map('Treeview',
              background=[('selected', '#0078D4')],
              foreground=[('selected', 'white')])

    style.configure("Treeview.Heading",
                    font=("Helvetica", 10, "bold"),
                    background="#4CAF50",
                    foreground="white")

    style.configure("TLabelFrame",
                    background="#F3F3F3",
                    font=("Helvetica", 10, "bold"))

    style.configure("TButton",
                    font=("Helvetica", 10),
                    padding=5)
    def show_all_doctors():
        """Function to display all doctors."""
        conn = sqlite3.connect('open_dental_users.db')
        cursor = conn.cursor()

        try:
            cursor.execute("""
                   SELECT p.per_id, p.name, p.email, p.age
                   FROM personnel p 
                   WHERE p.role = 'Doctor'
               """)
            doctors = cursor.fetchall()
            print(f"Debug: Found doctors: {doctors}")
        except Exception as e:
            print(f"Error fetching doctors: {e}")
            messagebox.showearor("Database Error", f"Error: {e}")
            return
        finally:
            conn.close()

        # GUI for All Doctors
        doctors_window = Toplevel()
        doctors_window.title("All Doctors")
        doctors_window.geometry("800x600")
        doctors_window.configure(bg="#e9f5e9")

        Label(doctors_window, text="All Doctors", font=("Arial", 20, "bold"), bg="#e9f5e9", fg="#4CAF50").pack(pady=10)

        # Treeview for displaying doctors
        tree = Treeview(
            doctors_window,
            columns=("ID", "Name", "Email", "Age"),
            show="headings",
            height=15
        )
        tree.pack(fill=BOTH, expand=True, pady=10)

        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Email", text="Email")
        tree.heading("Age", text="Age")

        tree.tag_configure("oddrow", background="#D6EEEE")
        tree.tag_configure("evenrow", background="#ffffff")

        # Populate the table
        for index, doctor in enumerate(doctors):
            tag = "oddrow" if index % 2 == 0 else "evenrow"
            tree.insert("", END, values=doctor, tags=(tag,))

        # Scrollbar for Treeview
        scrollbar = Scrollbar(doctors_window, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

    # GUI for All Patients
    def show_all_patients():
        """Function to display all patients."""
        conn = sqlite3.connect('open_dental_users.db')
        cursor = conn.cursor()

        try:
            cursor.execute("""
                   SELECT p.pid, p.name, p.age, p.assigned_doctor, p.room_number
                   FROM patients p
               """)
            patients = cursor.fetchall()
            print(f"Debug: Found patients: {patients}")
        except Exception as e:
            print(f"Error fetching patients: {e}")
            messagebox.showerror("Database Error", f"Error: {e}")
            return
        finally:
            conn.close()

        # GUI for All Patients
        patients_window = Toplevel()
        patients_window.title("All Patients")
        patients_window.geometry("800x600")
        patients_window.configure(bg="#f9f9f9")

        Label(patients_window, text="All Patients", font=("Arial", 20, "bold"), bg="#f9f9f9", fg="#4CAF50").pack(
            pady=10)

        # Treeview for displaying patients
        tree = Treeview(
            patients_window,
            columns=("ID", "Name", "Age", "Assigned Doctor", "Room Number"),
            show="headings",
            height=15
        )
        tree.pack(fill=BOTH, expand=True, pady=10)

        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Age", text="Age")
        tree.heading("Assigned Doctor", text="Assigned Doctor")
        tree.heading("Room Number", text="Room Number")

        tree.tag_configure("oddrow", background="#D6EEEE")
        tree.tag_configure("evenrow", background="#ffffff")

        # Populate the table
        for index, patient in enumerate(patients):
            patient = list(patient)  # Convert to list to allow modification
            if patient[4] is None:  # Room Number is at index 4
                patient[4] = "Not Assigned"
            tag = "oddrow" if index % 2 == 0 else "evenrow"
            tree.insert("", END, values=patient, tags=(tag,))

        # Scrollbar for Treeview
        scrollbar = Scrollbar(patients_window, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)


    # Update Buttons in the personnel_dashboard function
    Button(menu_frame, text="All Doctors", font=("Arial", 12), bg="#6AA84F", command=show_all_doctors).pack(side=LEFT, padx=10)
    Button(menu_frame, text="All Patients", font=("Arial", 12), bg="#6AA84F", command=show_all_patients).pack(side=LEFT, padx=10)
    Button(menu_frame, text="Add Patient", font=("Arial", 12), bg="#6AA84F", command=lambda: print("Add Patient clicked")).pack(side=LEFT, padx=10)

    # Patient Table Section
    table_frame = Frame(dashboard, bg="white")
    table_frame.pack(padx=10, pady=10, fill=BOTH, expand=True)

    Label(table_frame, text="My Patients", font=("Arial", 16)).pack()

    tree = Treeview(
        table_frame,
        columns=("ID", "Name", "Age", "Gender", "Room"),
        show="headings",
        height=8
    )
    tree.pack(fill=BOTH, expand=True)

    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Age", text="Age")
    tree.heading("Gender", text="Gender")
    tree.heading("Room", text="Room")

    # Populate table with assigned patients
    for patient in assigned_patients:
        tree.insert("", END, values=patient)

    def open_login_page():
        try:
            subprocess.Popen(["python", "login.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open login.py: {e}")
    # Add double-click functionality to open patient dashboard
    def on_double_click(event):
        selected_item = tree.selection()
        if selected_item:
            patient_pid = int(tree.item(selected_item, "values")[0])
            print(f"Debug: Double-click detected on patient PID: {patient_pid}")
            open_dashboard({'uid': patient_pid}, parent=dashboard)

    tree.bind("<Double-1>", on_double_click)

    def terminate_session():
        """Terminate the session and show the login page."""
        dashboard.withdraw()  # Hide the current window
        open_login_page()  # Open the login page

    # Log Out Button
    footer = Frame(dashboard, bg="#f0f4f8", height=50)
    footer.pack(fill=X, side=BOTTOM, pady=10)
    Button(footer, text="Log Out", font=("Arial", 12), bg="#dc3545", fg="black", width=15, command=terminate_session).pack(pady=10)

    dashboard.mainloop()