import sqlite3
import subprocess
from tkinter import *
from tkinter.ttk import Treeview
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def open_dashboard(user):
    print(f"Debug: Entering manager_dashboard with user: {user}")

    if not isinstance(user, dict) or 'uid' not in user:
        raise ValueError("Invalid user object passed to manager_dashboard.")

    manager_uid = user['uid']
    print(f"Debug: Manager UID is {manager_uid}")

    # Hardcoded hospital details for single-hospital system
    hospital_name = "Central Hospital"
    hospital_address = "123 Main St, Cityville"

    # Connect to the database
    conn = sqlite3.connect('open_dental_users.db')
    cursor = conn.cursor()

    try:
        # Fetch statistics
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

    except Exception as e:
        print(f"Error fetching statistics data: {e}")
        messagebox.showerror("Database Error", f"Error: {e}")
        return
    finally:
        conn.close()

    # Create the Manager Dashboard window
    dashboard = Tk()
    dashboard.title(f"{hospital_name} - Manager Dashboard")
    dashboard.geometry("900x700")
    dashboard.configure(bg="#f0f4f8")

    # Define a function to switch pages
    def show_page(page_name):
        for frame in pages.values():
            frame.pack_forget()
        pages[page_name].pack(fill=BOTH, expand=True)

        # Define a function to open floors_rooms.py
    def open_floors_rooms():
        try:
            subprocess.Popen(["python", "floors_rooms.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open floors_rooms.py: {e}")

    # Header Section
    header = Frame(dashboard, bg="#4CAF50", height=80)
    header.pack(fill=X)
    Label(header, text=f"Manager Dashboard - {hospital_name}", font=("Arial", 20), bg="#4CAF50", fg="white").pack()

    # Hospital Info Section
    # Buttons Section
    menu_frame = Frame(dashboard, bg="white", padx=10, pady=10)
    menu_frame.pack(fill=X, pady=10)

    Button(menu_frame, text="Home", font=("Arial", 12), bg="#4CAF50", command=lambda: show_page("Home")).pack(side=LEFT,
                                                                                                              padx=10)
    Button(menu_frame, text="All Doctors", font=("Arial", 12), bg="#6AA84F", command=lambda: show_page("Doctors")).pack(
        side=LEFT, padx=10)
    Button(menu_frame, text="All Patients", font=("Arial", 12), bg="#6AA84F",
           command=lambda: show_page("Patients")).pack(side=LEFT, padx=10)
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
    fig, axs = plt.subplots(2, 1, figsize=(6, 8), dpi=100)
    fig.subplots_adjust(hspace=0.5)
    # Gender Distribution Pie Chart
    if gender_distribution:
        genders, counts = zip(*gender_distribution)
        axs[0].pie(counts, labels=genders, autopct='%1.1f%%', startangle=140, colors=['skyblue', 'lightcoral'])
        axs[0].set_title("Gender Distribution of Patients")
    else:
        axs[0].text(0.5, 0.5, "No Data", ha='center', va='center', fontsize=14)

    # Age Distribution Bar Chart
    if age_distribution:
        ages, age_counts = zip(*age_distribution)
        axs[1].bar(ages, age_counts, color='orange')
        axs[1].set_title("Age Distribution of Patients")
        axs[1].set_xlabel("Age")
        axs[1].set_ylabel("Number of Patients")
    else:
        axs[1].text(0.5, 0.5, "No Data", ha='center', va='center', fontsize=14)

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

    # Footer Section
    footer = Frame(dashboard, bg="#f0f4f8", height=50)
    footer.pack(fill=X, side=BOTTOM, pady=10)
    Button(footer, text="Log Out", font=("Arial", 12), bg="#dc3545", fg="black", width=15,
           command=dashboard.destroy).pack(pady=10)

    dashboard.mainloop()