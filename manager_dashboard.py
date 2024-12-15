import sqlite3
import subprocess
import time
from tkinter import *
from tkinter.ttk import Treeview, Style
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def open_dashboard(user):
    print(f"Debug: Entering manager_dashboard with user: {user}")

    if not isinstance(user, dict) or 'uid' not in user:
        raise ValueError("Invalid user object passed to manager_dashboard.")

    manager_uid = user['uid']
    print(f"Debug: Manager UID is {manager_uid}")

    hospital_name = "Central Hospital"
    hospital_address = "123 Main St, Cityville"

    conn = sqlite3.connect('open_dental_users.db')
    cursor = conn.cursor()

    try:
        start_time = time.time()
        cursor.execute("SELECT COUNT(*) FROM patients")
        total_patients = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM personnel WHERE role = 'Doctor'")
        total_doctors = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM rooms")
        total_rooms = cursor.fetchone()[0]

        cursor.execute("SELECT gender, COUNT(*) FROM patients GROUP BY gender")
        gender_distribution = cursor.fetchall()

        cursor.execute("SELECT age, COUNT(*) FROM patients GROUP BY age")
        age_distribution = cursor.fetchall()

        cursor.execute("SELECT race, COUNT(*) FROM patients GROUP BY race")
        race_distribution = cursor.fetchall()

        cursor.execute("SELECT education_level, COUNT(*) FROM patients GROUP BY education_level")
        education_level_distribution = cursor.fetchall()
        duration = time.time() - start_time
        print(f"Time taken to fetch hospital statistics: {duration:.2f} seconds")

    except Exception as e:
        print(f"Error fetching statistics data: {e}")
        messagebox.showerror("Database Error", f"Error: {e}")
        return
    finally:
        conn.close()

    dashboard = Tk()
    dashboard.title(f"{hospital_name} - Manager Dashboard")
    dashboard.geometry("900x700")
    dashboard.configure(bg="#f0f4f8")

    def show_page(page_name):
        for frame in pages.values():
            frame.pack_forget()
        pages[page_name].pack(fill=BOTH, expand=True)

    def open_login_page():
        try:
            subprocess.Popen(["python3", "login.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open login.py: {e}")

    def open_floors_rooms():
        try:
            subprocess.Popen(["python3", "floors_rooms.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open floors_rooms.py: {e}")

    header = Frame(dashboard, bg="#4CAF50", height=80)
    header.pack(fill=X)
    Label(header, text=f"Manager Dashboard - {hospital_name}", font=("Arial", 20), bg="#4CAF50", fg="white").pack()

    menu_frame = Frame(dashboard, bg="white", padx=10, pady=10)
    menu_frame.pack(fill=X, pady=10)
    # implement the show all doctors button
    # GUI for All Doctors
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
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Email", text="Email")
        tree.heading("Age", text="Age")

        tree.tag_configure("oddrow", background="#f0f8ff")
        tree.tag_configure("evenrow", background="#e6e6fa")

        # Populate the table
        for index, doctor in enumerate(doctors):
            tag = "oddrow" if index % 2 == 0 else "evenrow"
            tree.insert("", END, values=doctor, tags=(tag,))

        # Scrollbar for Treeview
        scrollbar = Scrollbar(doctors_window, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

    def show_all_patients():
        """Function to display all patients."""
        conn = sqlite3.connect('open_dental_users.db')
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT p.pid, p.name, p.age, p.status, p.room_number
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
            columns=("ID", "Name", "Age", "Status", "Room Number"),
            show="headings",
            height=15
        )
        tree.pack(fill=BOTH, expand=True, pady=10)

        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Age", text="Age")
        tree.heading("Status", text="Status")
        tree.heading("Room Number", text="Room Number")

        tree.tag_configure("oddrow", background="#f0f8ff")
        tree.tag_configure("evenrow", background="#e6e6fa")

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

        # Handle double-click event
        def on_patient_double_click(event):
            selected_item = tree.selection()
            if not selected_item:
                return

            # Fetch patient details
            patient = tree.item(selected_item)["values"]
            patient_id = patient[0]
            patient_name = patient[1]
            patient_status = patient[3]

            if patient_status == "waiting":
                # Open room assignment dialog
                assign_room_dialog(patient_id, patient_name)
            elif patient_status == "admitted":
                # Ask to discharge the patient
                discharge_patient_dialog(patient_id, patient_name)

        tree.bind("<Double-1>", on_patient_double_click)

        patients_window.mainloop()

    def discharge_patient_dialog(patient_id, patient_name):
        """Ask if the patient should be discharged."""
        response = messagebox.askyesno(
            "Discharge Patient",
            f"Do you want to discharge {patient_name}?"
        )

        if response:  # If user clicks "Yes"
            conn = sqlite3.connect('open_dental_users.db')
            cursor = conn.cursor()

            try:
                # Fetch the current room number for the patient
                cursor.execute("SELECT room_number FROM patients WHERE pid = ?", (patient_id,))
                room_number = cursor.fetchone()[0]

                # Update the database to discharge the patient
                if room_number:
                    cursor.execute("UPDATE rooms SET available_beds = available_beds + 1 WHERE room_number = ?",
                                   (room_number,))
                cursor.execute("UPDATE patients SET status = 'waiting', room_number = NULL, bed = NULL WHERE pid = ?",
                               (patient_id,))
                conn.commit()
                messagebox.showinfo("Success", f"{patient_name} has been discharged.")
            except Exception as e:
                print(f"Error discharging patient: {e}")
                messagebox.showerror("Error", f"Could not discharge {patient_name}: {e}")
            finally:
                conn.close()

    def assign_room_dialog(patient_id, patient_name):
        """Dialog to assign a room to a patient."""
        conn = sqlite3.connect('open_dental_users.db')
        cursor = conn.cursor()

        # Fetch available rooms
        cursor.execute("SELECT id, floor, room_number, beds, available_beds FROM rooms WHERE available_beds > 0")
        rooms = cursor.fetchall()

        if not rooms:
            messagebox.showinfo("No Rooms Available", "There are no rooms with available beds.")
            return

        # Create the dialog window
        dialog = Toplevel()
        dialog.title(f"Assign Room to {patient_name}")
        dialog.geometry("600x400")

        Label(dialog, text=f"Assign Room to {patient_name}", font=("Arial", 16), pady=10).pack()

        # Treeview for displaying rooms
        room_tree = Treeview(
            dialog,
            columns=("Room ID", "Floor", "Room Number", "Beds", "Available Beds"),
            show="headings",
            height=15
        )
        room_tree.pack(fill=BOTH, expand=True, pady=10)

        room_tree.heading("Room ID", text="Room ID")
        room_tree.heading("Floor", text="Floor")
        room_tree.heading("Room Number", text="Room Number")
        room_tree.heading("Beds", text="Beds")
        room_tree.heading("Available Beds", text="Available Beds")

        room_tree.tag_configure("oddrow", background="#f0f8ff")
        room_tree.tag_configure("evenrow", background="#e6e6fa")

        # Populate the table
        for index, room in enumerate(rooms):
            tag = "oddrow" if index % 2 == 0 else "evenrow"
            room_tree.insert("", END, values=room, tags=(tag,))

        # Scrollbar for Treeview
        scrollbar = Scrollbar(dialog, orient=VERTICAL, command=room_tree.yview)
        room_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Assign room to the patient
        def assign_room():
            selected_item = room_tree.selection()
            if not selected_item:
                messagebox.showwarning("No Selection", "Please select a room.")
                return

            # Fetch selected room details
            room = room_tree.item(selected_item)["values"]
            room_id = room[0]
            room_number = room[2]

            try:
                # Update the database
                cursor.execute("UPDATE rooms SET available_beds = available_beds - 1 WHERE id = ?", (room_id,))
                cursor.execute("UPDATE patients SET room_number = ?, status = 'admitted' WHERE pid = ?",
                               (room_number, patient_id))
                conn.commit()
                messagebox.showinfo("Success", f"{patient_name} has been assigned to Room {room_number}.")
                dialog.destroy()
            except Exception as e:
                print(f"Error assigning room: {e}")
                messagebox.showerror("Error", f"Could not assign room: {e}")
            finally:
                conn.close()

        Button(dialog, text="Assign Room", command=assign_room).pack(pady=10)

        dialog.mainloop()

    # Update Buttons in the personnel_dashboard function
    Button(menu_frame, text="Home", font=("Arial", 12), bg="#4CAF50", command=lambda: show_page("Home")).pack(side=LEFT,
                                                                                                              padx=10)
    Button(menu_frame, text="All Doctors", font=("Arial", 12), bg="#6AA84F", command=show_all_doctors).pack(side=LEFT,
                                                                                                            padx=10)
    Button(menu_frame, text="All Patients", font=("Arial", 12), bg="#6AA84F", command=show_all_patients).pack(side=LEFT,
                                                                                                              padx=10)

    Button(menu_frame, text="All Rooms", font=("Arial", 12), bg="#6AA84F", command=open_floors_rooms).pack(
        side=LEFT, padx=10)

    # Page Frames
    pages = {}

    # Home Page
    home_page = Frame(dashboard, bg="white", padx=10, pady=10)
    pages["Home"] = home_page
    home_page.pack(fill=BOTH, expand=True)

    Label(home_page, text="Hospital Statistics", font=("Arial", 16)).pack()

    # Create Visualizations using Matplotlib
    fig, axs = plt.subplots(4, 1, figsize=(6, 8), dpi=100)
    fig.subplots_adjust(hspace=0.5)
    # Gender Distribution Pie Chart
    if gender_distribution:
        genders, counts = zip(*gender_distribution)
        axs[0].pie(counts, labels=genders, autopct='%1.1f%%', startangle=140, colors=['skyblue', 'lightcoral'])
        axs[0].set_title("Gender Distribution of Patients")
    else:
        axs[0].text(0.5, 0.5, "No Data", ha='center', va='center', fontsize=14)
    # Race Distribution Pie Chart
    if race_distribution:
        races, counts = zip(*race_distribution)
        axs[1].pie(counts, labels=races, autopct='%1.1f%%', startangle=140,
                   colors=['gold', 'green', 'purple', 'orange', 'pink'])
        axs[1].set_title("Race Distribution of Patients")
    else:
        axs[1].text(0.5, 0.5, "No Data", ha='center', va='center', fontsize=14)

    # Education Level Distribution Pie Chart
    if education_level_distribution:
        education_levels, counts = zip(*education_level_distribution)
        axs[2].pie(counts, labels=education_levels, autopct='%1.1f%%', startangle=140,
                   colors=['brown', 'cyan', 'lime', 'magenta', 'grey'])
        axs[2].set_title("Education Level Distribution of Patients")
    else:
        axs[2].text(0.5, 0.5, "No Data", ha='center', va='center', fontsize=14)
    # Age Distribution Bar Chart
    if age_distribution:
        ages, age_counts = zip(*age_distribution)
        axs[3].bar(ages, age_counts, color='orange')
        axs[3].set_title("Age Distribution of Patients")
        axs[3].set_xlabel("Age")
        axs[3].set_ylabel("Number of Patients")
    else:
        axs[3].text(0.5, 0.5, "No Data", ha='center', va='center', fontsize=14)

    # Embed Matplotlib figure in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=home_page)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    # Foo Pages (Doctors, Patients, Rooms)
    for name in ["Doctors", "Patients", "Rooms"]:
        page = Frame(dashboard, bg="white", padx=10, pady=10)
        pages[name] = page
        Label(page, text=f"{name} Page (Placeholder)", font=("Arial", 16)).pack()

    # Show Home Page by default
    show_page("Home")

    def terminate_session():
        """Terminate the session and show the login page."""
        dashboard.withdraw()  # Hide the current window
        open_login_page()  # Open the login page

    # Footer Section
    footer = Frame(dashboard, bg="#f0f4f8", height=50)
    footer.pack(fill=X, side=BOTTOM, pady=10)
    Button(footer, text="Log Out", font=("Arial", 12), bg="#dc3545", fg="black", width=15,
           command=terminate_session).pack(pady=10)

    dashboard.mainloop()