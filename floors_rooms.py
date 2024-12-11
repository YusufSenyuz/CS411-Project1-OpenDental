import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Database setup
conn = sqlite3.connect('open_dental_users.db')
cursor = conn.cursor()

# Tables
#cursor.execute('''ALTER TABLE users ADD COLUMN status TEXT DEFAULT 'waiting' ''')

cursor.execute('''CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY,
    floor INTEGER,
    room_number INTEGER,
    beds INTEGER,
    available_beds INTEGER
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS assignments (
    patient_id INTEGER,
    room_id INTEGER,
    bed INTEGER,
    FOREIGN KEY(patient_id) REFERENCES users(uid),
    FOREIGN KEY(room_id) REFERENCES rooms(id)
)''')

# Mock data
cursor.executemany('INSERT OR IGNORE INTO users (uid, username, status) VALUES (?, ?, ?)',
                   [(1, 'Alice', 'waiting'),
                    (2, 'Bob', 'waiting'),
                    (3, 'Charlie', 'waiting')])

cursor.executemany('INSERT OR IGNORE INTO rooms (id, floor, room_number, beds, available_beds) VALUES (?, ?, ?, ?, ?)',
                   [(1, 1, 101, 2, 2),
                    (2, 1, 102, 1, 1),
                    (3, 2, 201, 2, 2)])

conn.commit()


# Tkinter Application
class HIMSApp:
    def __init__(self, parent):
        self.parent = parent
        self.selected_patient = None
        self.selected_room = None

        self.selected_patient = None
        self.selected_room = None
        # Configure styles
        style = ttk.Style()
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

        # Frame for patient management
        patient_frame = ttk.LabelFrame(root, text="Patient Management")
        patient_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.patient_list = ttk.Treeview(patient_frame, columns=("ID", "Name", "Status", "Room Number", "Bed"),
                                         show="headings")
        self.patient_list.heading("ID", text="ID")
        self.patient_list.heading("Name", text="Name")
        self.patient_list.heading("Status", text="Status")
        self.patient_list.heading("Room Number", text="Room Number")
        self.patient_list.heading("Bed", text="Bed")
        self.patient_list.pack(side="left", fill="both", expand=True)

        patient_scroll = ttk.Scrollbar(patient_frame, orient="vertical", command=self.patient_list.yview)
        self.patient_list.configure(yscroll=patient_scroll.set)
        patient_scroll.pack(side="right", fill="y")

        self.patient_list.bind("<<TreeviewSelect>>", self.select_patient)

        # Room management
        room_frame = ttk.LabelFrame(root, text="Room Management")
        room_frame.pack(fill="x", expand=True, padx=10, pady=10)

        ttk.Label(room_frame, text="Floor:").grid(row=0, column=0, padx=5, pady=5)
        self.floor_var = tk.IntVar()
        self.floor_select = ttk.Combobox(room_frame, textvariable=self.floor_var)
        self.floor_select.grid(row=0, column=1, padx=5, pady=5)
        self.floor_select.bind("<<ComboboxSelected>>", self.load_rooms)

        self.room_list = ttk.Treeview(room_frame, columns=("Room ID", "Room Number", "Beds", "Available Beds"),
                                      show="headings")
        self.room_list.heading("Room ID", text="Room ID")
        self.room_list.heading("Room Number", text="Room Number")
        self.room_list.heading("Beds", text="Beds")
        self.room_list.heading("Available Beds", text="Available Beds")
        self.room_list.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

        room_scroll = ttk.Scrollbar(room_frame, orient="vertical", command=self.room_list.yview)
        self.room_list.configure(yscroll=room_scroll.set)
        room_scroll.grid(row=1, column=3, sticky="ns")

        self.room_list.bind("<<TreeviewSelect>>", self.select_room)

        # Buttons
        button_frame = ttk.Frame(root)
        button_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(button_frame, text="Assign Room", command=self.assign_room).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Discharge Patient", command=self.discharge_patient).pack(side="left", padx=5)

        self.load_patients()
        self.load_floors()

    def load_patients(self):
        for row in self.patient_list.get_children():
            self.patient_list.delete(row)
        patients = cursor.execute('''
            SELECT users.uid, users.username, users.status,
                   COALESCE(rooms.room_number, 'N/A') AS room_number,
                   COALESCE(assignments.bed, 'N/A') AS bed
            FROM users
            LEFT JOIN assignments ON users.uid = assignments.patient_id
            LEFT JOIN rooms ON assignments.room_id = rooms.id
        ''').fetchall()
        # Insert data with alternating row colors
        for index, patient in enumerate(patients):
            tag = 'oddrow' if index % 2 == 0 else 'evenrow'
            self.patient_list.insert("", "end", values=patient, tags=(tag,))

        # Configure row styles
        self.patient_list.tag_configure('oddrow', background="#f0f8ff")
        self.patient_list.tag_configure('evenrow', background="#e6e6fa")

    def load_floors(self):
        floors = cursor.execute("SELECT DISTINCT floor FROM rooms").fetchall()
        self.floor_select["values"] = [floor[0] for floor in floors]

    def load_rooms(self, event=None):
        for row in self.room_list.get_children():
            self.room_list.delete(row)
        selected_floor = self.floor_var.get()
        rooms = cursor.execute("SELECT id, room_number, beds, available_beds FROM rooms WHERE floor = ?",
                               (selected_floor,)).fetchall()
        # Insert data with alternating row colors
        for index, room in enumerate(rooms):
            tag = 'oddrow' if index % 2 == 0 else 'evenrow'
            self.room_list.insert("", "end", values=room, tags=(tag,))

        # Configure row styles
        self.room_list.tag_configure('oddrow', background="#f0f8ff")
        self.room_list.tag_configure('evenrow', background="#e6e6fa")

    def select_patient(self, event):
        selected = self.patient_list.selection()
        if selected:
            self.selected_patient = self.patient_list.item(selected[0])["values"]

    def select_room(self, event):
        selected = self.room_list.selection()
        if selected:
            self.selected_room = self.room_list.item(selected[0])["values"]

    def assign_room(self):
        if not self.selected_patient or not self.selected_room:
            messagebox.showerror("Error", "Select a patient and a room.")
            return
        room_id, _, beds, available_beds = self.selected_room
        patient_id, name, status, _, _ = self.selected_patient
        if status != "waiting":
            messagebox.showerror("Error", f"Patient {name} is already assigned.")
            return
        if available_beds == 0:
            messagebox.showerror("Error", "No available beds in the selected room.")
            return
        cursor.execute("UPDATE rooms SET available_beds = available_beds - 1 WHERE id = ?", (room_id,))
        cursor.execute("INSERT INTO assignments (patient_id, room_id, bed) VALUES (?, ?, ?)",
                       (patient_id, room_id, beds - available_beds + 1))
        cursor.execute("UPDATE users SET status = 'admitted' WHERE uid = ?", (patient_id,))
        conn.commit()
        self.load_patients()
        self.load_rooms()
        messagebox.showinfo("Success", f"Patient {name} assigned to Room {self.selected_room[1]}.")

    def discharge_patient(self):
        if not self.selected_patient:
            messagebox.showerror("Error", "Select a patient.")
            return
        patient_id, name, status, _, _ = self.selected_patient
        if status != "admitted":
            messagebox.showerror("Error", f"Patient {name} is not admitted.")
            return
        room_id, bed = cursor.execute("SELECT room_id, bed FROM assignments WHERE patient_id = ?",
                                      (patient_id,)).fetchone()
        cursor.execute("DELETE FROM assignments WHERE patient_id = ?", (patient_id,))
        cursor.execute("UPDATE users SET status = 'waiting' WHERE uid = ?", (patient_id,))
        cursor.execute("UPDATE rooms SET available_beds = available_beds + 1 WHERE id = ?", (room_id,))
        conn.commit()
        self.load_patients()
        self.load_rooms()
        messagebox.showinfo("Success", f"Patient {name} discharged.")


# Main application
root = tk.Tk()
app = HIMSApp(root)
root.mainloop()