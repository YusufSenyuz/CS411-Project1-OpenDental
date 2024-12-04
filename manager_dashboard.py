from tkinter import *

def open_dashboard(username):
    dashboard = Tk()
    dashboard.title(f"Open Dental - Dashboard ({username})")
    dashboard.geometry("1000x600")
    dashboard.configure(bg="#f0f0f0")

    menu_bar = Menu(dashboard)

    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="New", command=None)
    file_menu.add_command(label="Open", command=None)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=dashboard.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)

    patients_menu = Menu(menu_bar, tearoff=0)
    patients_menu.add_command(label="New Patient", command=None)
    patients_menu.add_command(label="Search Patient", command=None)
    menu_bar.add_cascade(label="Patients", menu=patients_menu)

    appointments_menu = Menu(menu_bar, tearoff=0)
    appointments_menu.add_command(label="Schedule Appointment", command=None)
    appointments_menu.add_command(label="View Appointments", command=None)
    menu_bar.add_cascade(label="Appointments", menu=appointments_menu)

    reports_menu = Menu(menu_bar, tearoff=0)
    reports_menu.add_command(label="Generate Report", command=None)
    menu_bar.add_cascade(label="Reports", menu=reports_menu)

    dashboard.config(menu=menu_bar)

    left_frame = Frame(dashboard, bg="#D9EAD3", width=200, height=600, relief=RAISED, bd=2)
    left_frame.pack(side=LEFT, fill=Y)

    main_frame = Frame(dashboard, bg="#ffffff", relief=RAISED, bd=2)
    main_frame.pack(fill=BOTH, expand=True)

    Label(left_frame, text="Quick Actions", bg="#D9EAD3", font=("Arial", 14)).pack(pady=10)


    Button(left_frame, text="Patients Registered To My Hospital", font=("Arial", 12), width=15, bg="#6AA84F").pack(pady=5)
    Button(left_frame, text="Doctors In My Hospital", font=("Arial", 12), width=15, bg="#6AA84F").pack(pady=5)
    Button(left_frame, text="All Rooms", font=("Arial", 12), width=15, bg="#6AA84F").pack(pady=5)

    Label(main_frame, text=f"Welcome to Open Dental, {username}", font=("Arial", 20), bg="#ffffff").pack(pady=20)

    status_label = Label(main_frame, text=f"Status: Logged in as {username}", font=("Arial", 12), bg="#ffffff")
    status_label.pack(pady=5)

    dashboard.mainloop()
