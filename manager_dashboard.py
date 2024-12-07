import sqlite3
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

    # Header Section
    header = Frame(dashboard, bg="#4CAF50", height=80)
    header.pack(fill=X)
    Label(header, text=f"Manager Dashboard - {hospital_name}", font=("Arial", 20), bg="#4CAF50", fg="white").pack()

    # Hospital Info Section
    info_frame = Frame(dashboard, bg="white", padx=10, pady=10, relief=RAISED, bd=2)
    info_frame.pack(padx=10, pady=10, fill=X)

    Label(info_frame, text=f"Hospital Name: {hospital_name}", font=("Arial", 14)).pack(anchor=W)
    Label(info_frame, text=f"Address: {hospital_address}", font=("Arial", 14)).pack(anchor=W)

    # Buttons Section
    menu_frame = Frame(dashboard, bg="white", padx=10, pady=10)
    menu_frame.pack(fill=X, pady=10)

    Button(menu_frame, text="All Doctors", font=("Arial", 12), bg="#6AA84F", command=lambda: print("All Doctors clicked")).pack(side=LEFT, padx=10)
    Button(menu_frame, text="All Patients", font=("Arial", 12), bg="#6AA84F", command=lambda: print("All Patients clicked")).pack(side=LEFT, padx=10)
    Button(menu_frame, text="All Rooms", font=("Arial", 12), bg="#6AA84F", command=lambda: print("All Rooms clicked")).pack(side=LEFT, padx=10)

    # Visual Statistics Section
    stats_frame = Frame(dashboard, bg="white", padx=10, pady=10)
    stats_frame.pack(fill=BOTH, expand=True)

    Label(stats_frame, text="Hospital Statistics", font=("Arial", 16)).pack()

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
    canvas = FigureCanvasTkAgg(fig, master=stats_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    # Footer Section
    footer = Frame(dashboard, bg="#f0f4f8", height=50)
    footer.pack(fill=X, side=BOTTOM, pady=10)
    Button(footer, text="Log Out", font=("Arial", 12), bg="#dc3545", fg="black", width=15, command=dashboard.destroy).pack(pady=10)

    dashboard.mainloop()