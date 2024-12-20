import sqlite3
import time
import tkinter as tk
from tkinter import ttk, messagebox

conn = sqlite3.connect('open_dental_users.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY,
    floor INTEGER,
    room_number INTEGER,
    beds INTEGER,
    available_beds INTEGER
)''')

# Mock data
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

        # Frame for patient management
        patient_frame = ttk.LabelFrame(parent, text="Patient Management")
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
        room_frame = ttk.LabelFrame(parent, text="Room Management")
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
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(button_frame, text="Assign Room", command=self.assign_room).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Discharge Patient", command=self.discharge_patient).pack(side="left", padx=5)

        self.load_patients()
        self.load_floors()

    def load_patients(self):
        for row in self.patient_list.get_children():
            self.patient_list.delete(row)
        patients = cursor.execute('''
            SELECT pid, name, status, room_number, COALESCE(bed, 'N/A') AS bed
            FROM patients
        ''').fetchall()
        for index, patient in enumerate(patients):
            tag = 'oddrow' if index % 2 == 0 else 'evenrow'
            self.patient_list.insert("", "end", values=patient, tags=(tag,))

        self.patient_list.tag_configure('oddrow', background="#f0f8ff")
        self.patient_list.tag_configure('evenrow', background="#e6e6fa")

    def load_floors(self):
        floors = cursor.execute("SELECT DISTINCT floor FROM rooms").fetchall()
        floor_values = [floor[0] for floor in floors]

        # If no floors exist in the database, set the default floor to 1
        if floor_values:
            self.floor_select["values"] = floor_values
            self.floor_var.set(floor_values[0])  # Set the first floor as default
        else:
            self.floor_select["values"] = [1]
            self.floor_var.set(1)  # Set default floor to 1

        # Trigger room loading for the initial floor
        self.load_rooms()

    def load_rooms(self, event=None):
        for row in self.room_list.get_children():
            self.room_list.delete(row)
        selected_floor = self.floor_var.get()
        rooms = cursor.execute("SELECT id, room_number, beds, available_beds FROM rooms WHERE floor = ?",
                               (selected_floor,)).fetchall()
        for index, room in enumerate(rooms):
            tag = 'oddrow' if index % 2 == 0 else 'evenrow'
            self.room_list.insert("", "end", values=room, tags=(tag,))

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
        start_time = time.time()

        # Update the room and patient tables
        cursor.execute("UPDATE rooms SET available_beds = available_beds - 1 WHERE id = ?", (room_id,))
        cursor.execute("UPDATE patients SET room_number = ?, status = 'admitted' WHERE pid = ?",
                       (self.selected_room[1], patient_id))
        conn.commit()

        duration = time.time() - start_time
        print(f"Time taken to assign room: {duration:.2f} seconds")
        self.load_patients()
        self.load_rooms()
        messagebox.showinfo("Success", f"Patient {name} assigned to Room {self.selected_room[1]}.")

    def discharge_patient(self):
        if not self.selected_patient:
            messagebox.showerror("Error", "Select a patient.")
            return
        patient_id, name, status, room_number, bed = self.selected_patient
        if status != "admitted":
            messagebox.showerror("Error", f"Patient {name} is not admitted.")
            return
        cursor.execute("UPDATE rooms SET available_beds = available_beds + 1 WHERE room_number = ?", (room_number,))
        cursor.execute("UPDATE patients SET status = 'waiting', room_number = 'N/A', bed = NULL WHERE pid = ?",
                       (patient_id,))
        conn.commit()
        self.load_patients()
        self.load_rooms()
        messagebox.showinfo("Success", f"Patient {name} discharged.")

root = tk.Tk()
app = HIMSApp(root)
root.mainloop()