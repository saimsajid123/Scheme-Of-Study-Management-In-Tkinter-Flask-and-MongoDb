# Sumbitted by:
# Muhammad Saim Sajid
# Rollno:
# F21BSEEN1E02025
# Semester:
# 5th
# Section:
# E1
# Sumbitted by:
# Huzaifa Qureshi
# Rollno:
# F21BSEEN1E02022
# Semester:
# 5th
# Section:
# E1
# Project:
# Scheme of Study Management In Tkinter
# Sumbitted To:
# Sir Nauman

# To install All The packages just type

# "pip install -r requirements.txt"

# in the terminal of vscode or whichever IDE you are Using

import tkinter as tk
from tkinter import ttk
import re
import requests

class SOSManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Study Management")

        self.semesters = {}

        # Create labels
        self.label1 = ttk.Label(self.root, text="Course Name:")
        self.label2 = ttk.Label(self.root, text="Instructor:")
        self.label3 = ttk.Label(self.root, text="Credits:")
        self.label4 = ttk.Label(self.root, text="Schedule:")

        # Create entry widgets
        self.entry1 = ttk.Entry(self.root)
        self.entry2 = ttk.Entry(self.root)
        self.entry3 = ttk.Entry(self.root)
        self.entry4 = ttk.Entry(self.root)

        # Create buttons
        self.add_button = ttk.Button(self.root, text="Add", command=self.add_item)
        self.delete_button = ttk.Button(self.root, text="Remove", command=self.remove_item)
        self.edit_button = ttk.Button(self.root, text="Edit", command=self.edit_item)
        self.save_button = ttk.Button(self.root, text="Save", command=self.save_sos)
        self.sort_button = ttk.Button(self.root, text="Sort", command=self.sort_items)
        self.load_button = ttk.Button(self.root, text="Load Subjects", command=self.load_subjects)

        # Create tree view
        self.tree = ttk.Treeview(self.root, columns=("Course", "Instructor", "Credits", "Schedule"))
        self.tree.heading("#1", text="Course")
        self.tree.heading("#2", text="Instructor")
        self.tree.heading("#3", text="Credits")
        self.tree.heading("#4", text="Schedule")

        # Create drop-down menu
        options = [f"Semester {i}" for i in range(1, 9)]
        self.variable = tk.StringVar(self.root)
        self.variable.set(options[0])
        self.dropdown = ttk.OptionMenu(self.root, self.variable, *options)

        # Create menu bar
        menubar = tk.Menu(self.root)
        teacher_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Teacher", menu=teacher_menu)
        teacher_menu.add_command(label="Sir Nauman", command=lambda: self.select_teacher(1))
        teacher_menu.add_command(label="Sir Rafaqat Kazmi", command=lambda: self.select_teacher(2))
        teacher_menu.add_command(label="Ma'am Sunnia", command=lambda: self.select_teacher(3))
        self.root.config(menu=menubar)

        # Grid layout
        self.label1.grid(row=0, column=0, padx=10, pady=5)
        self.entry1.grid(row=0, column=1, padx=10, pady=5)
        self.label2.grid(row=1, column=0, padx=10, pady=5)
        self.entry2.grid(row=1, column=1, padx=10, pady=5)
        self.label3.grid(row=2, column=0, padx=10, pady=5)
        self.entry3.grid(row=2, column=1, padx=10, pady=5)
        self.label4.grid(row=3, column=0, padx=10, pady=5)
        self.entry4.grid(row=3, column=1, padx=10, pady=5)

        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)
        self.delete_button.grid(row=5, column=0, columnspan=2, pady=10)
        self.edit_button.grid(row=6, column=0, columnspan=2, pady=10)
        self.save_button.grid(row=7, column=0, columnspan=2, pady=10)
        self.sort_button.grid(row=8, column=0, columnspan=2, pady=10)
        self.load_button.grid(row=9, column=0, columnspan=2, pady=10)

        self.tree.grid(row=0, column=2, rowspan=10, padx=10, pady=5)
        self.dropdown.grid(row=10, column=0, columnspan=2, pady=10)

        self.root.mainloop()

    def add_item(self):
        subject_name = self.entry1.get()
        description = self.entry2.get()
        course_code = self.entry3.get()
        teacher_name = self.entry4.get()

        if subject_name and description and course_code and teacher_name:
            selected_semester = self.variable.get()
            if selected_semester:
                course_info = f"{subject_name}: {description} ({course_code}, {teacher_name})"

                data = {
                    'subject_name': subject_name,
                    'description': description,
                    'course_code': course_code,
                    'teacher_name': teacher_name,
                    'selected_semester': selected_semester
                }
                response = requests.post('http://127.0.0.1:5000/sos', json=data)

                if response.status_code == 201:
                    self.update_sos_listbox()
                else:
                    print(f"Error adding item: {response.json().get('error')}")

                self.save_sos()  

        self.clear_entry_fields()

    def remove_item(self):
        selected_item = self.tree.get(tk.ANCHOR)
        if selected_item:
            self.tree.delete(tk.ANCHOR)

            response = requests.delete('http://127.0.0.1:5000/sos',
                                       params={'selected_semester': self.variable.get(),
                                               'selected_item': selected_item})

            if response.status_code != 200:
                print(f"Error removing item: {response.json().get('error')}")

    def load_subjects(self):
        selected_semester = self.variable.get()
        if selected_semester:
            response = requests.get('http://127.0.0.1:5000/sos', params={'selected_semester': selected_semester})

            if response.status_code == 200:
                self.tree.delete(0, tk.END)  
                for course in response.json().get('courses', []):
                    self.tree.insert(tk.END, course)
            else:
                print(f"Error loading items: {response.json().get('error')}")

    def clear_entry_fields(self):
        self.entry1.delete(0, tk.END)
        self.entry2.delete(0, tk.END)
        self.entry3.delete(0, tk.END)
        self.entry4.delete(0, tk.END)

    def edit_item(self):
        selected_item = self.tree.get(tk.ANCHOR)
        if selected_item:
            subject_name, description, rest_info = selected_item.split(": ", 2)
            course_code, teacher_name = re.search(r'\((.*?)\, (.*?)\)', rest_info).groups()

            self.entry1.insert(0, subject_name)
            self.entry2.insert(0, description)
            self.entry3.insert(0, course_code)
            self.entry4.insert(0, teacher_name)

            self.tree.delete(tk.ANCHOR)

    def save_sos(self):
        sos_items = self.tree.get(0, tk.END)
        with open("sos.txt", "w") as f:
            for item in sos_items:
                f.write(f"{item}\n")

    def sort_items(self):
        items = self.tree.get(0, tk.END)
        sorted_items = sorted(items)

        self.tree.delete(0, tk.END)
        for item in sorted_items:
            self.tree.insert(tk.END, item)

    def update_sos_listbox(self):
        self.tree.delete(0, tk.END)
        selected_semester = self.variable.get()
        if selected_semester:
            courses = self.semesters.get(selected_semester, [])
            for course in courses:
                self.tree.insert(tk.END, course)

    def select_teacher(self, teacher_number):
        self.tree.delete(0, tk.END)

        if teacher_number == 1:
            self.semesters = {"Semester 1": ["Subject1: Description1 (Code1, Sir Nauman)"],
                             "Semester 2": ["Subject2: Description2 (Code2, Sir Nauman)"]}
        elif teacher_number == 2:
            self.semesters = {"Semester 1": ["Subject3: Description3 (Code3, Sir Rafaqat Kazmi)"],
                             "Semester 2": ["Subject4: Description4 (Code4, Sir Rafaqat Kazmi)"]}
        elif teacher_number == 3:
            self.semesters = {"Semester 1": ["Subject5: Description5 (Code5, Ma'am Sunnia)"],
                             "Semester 2": ["Subject6: Description6 (Code6, Ma'am Sunnia)"]}

        self.update_sos_listbox()


if __name__ == "__main__":
    sos_manager = SOSManager()

