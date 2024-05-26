# To install All The packages just type

# "pip install -r requirements.txt"

# in the terminal of vscode or whichever IDE you are Using

import tkinter as tk
from tkinter import ttk, messagebox
import re
import requests

class SOSManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Study Management")
        self.root.geometry("800x600")

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
        self.search_button = ttk.Button(self.root, text="Search", command=self.search_items)

        # Create tree view
        self.tree = ttk.Treeview(self.root, columns=("Course", "Instructor", "Credits", "Schedule"))
        self.tree.heading("#1", text="Course")
        self.tree.heading("#2", text="Instructor")
        self.tree.heading("#3", text="Credits")
        self.tree.heading("#4", text="Schedule")
        self.tree["show"] = "headings"

        # Create drop-down menu
        options = [f"Semester {i}" for i in range(1, 9)]
        self.variable = tk.StringVar(self.root)
        self.variable.set(options[0])
        self.dropdown = ttk.OptionMenu(self.root, self.variable, *options)

        # Create search entry
        self.search_entry = ttk.Entry(self.root)

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
        self.search_entry.grid(row=10, column=0, padx=10, pady=5)
        self.search_button.grid(row=10, column=1, pady=5)

        self.tree.grid(row=0, column=2, rowspan=11, padx=10, pady=5, sticky="nsew")
        self.dropdown.grid(row=11, column=0, columnspan=2, pady=10)

        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(10, weight=1)

        self.root.mainloop()

    def validate_input(self, course_name, instructor, credits, schedule):
        if not course_name or not instructor or not credits or not schedule:
            messagebox.showerror("Input Error", "All fields must be filled out.")
            return False

        if not credits.isdigit():
            messagebox.showerror("Input Error", "Credits must be a number.")
            return False

        if not re.match(r"\w+", course_name):
            messagebox.showerror("Input Error", "Invalid course name.")
            return False

        return True

    def add_item(self):
        course_name = self.entry1.get()
        instructor = self.entry2.get()
        credits = self.entry3.get()
        schedule = self.entry4.get()

        if self.validate_input(course_name, instructor, credits, schedule):
            selected_semester = self.variable.get()
            course_info = (course_name, instructor, credits, schedule)

            data = {
                'course_name': course_name,
                'instructor': instructor,
                'credits': credits,
                'schedule': schedule,
                'semester': selected_semester
            }

            response = requests.post('http://127.0.0.1:5000/sos', json=data)
            if response.status_code == 201:
                self.tree.insert("", "end", values=course_info)
            else:
                messagebox.showerror("Server Error", f"Error adding item: {response.json().get('error')}")

            self.save_sos()
        self.clear_entry_fields()

    def remove_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            self.tree.delete(selected_item)

            response = requests.delete('http://127.0.0.1:5000/sos', params={
                'semester': self.variable.get(),
                'course_name': item_values[0],
                'instructor': item_values[1]
            })

            if response.status_code != 200:
                messagebox.showerror("Server Error", f"Error removing item: {response.json().get('error')}")

    def load_subjects(self):
        selected_semester = self.variable.get()
        response = requests.get('http://127.0.0.1:5000/sos', params={'semester': selected_semester})
        if response.status_code == 200:
            self.tree.delete(*self.tree.get_children())
            for course in response.json().get('courses', []):
                self.tree.insert("", "end", values=(course['course_name'], course['instructor'], course['credits'], course['schedule']))
        else:
            messagebox.showerror("Server Error", f"Error loading items: {response.json().get('error')}")

    def search_items(self):
        query = self.search_entry.get()
        for child in self.tree.get_children():
            values = self.tree.item(child, "values")
            if query.lower() in " ".join(values).lower():
                self.tree.selection_set(child)
                self.tree.focus(child)
                return
        messagebox.showinfo("Search Result", "No matching course found.")

    def clear_entry_fields(self):
        self.entry1.delete(0, tk.END)
        self.entry2.delete(0, tk.END)
        self.entry3.delete(0, tk.END)
        self.entry4.delete(0, tk.END)

    def edit_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            self.entry1.insert(0, item_values[0])
            self.entry2.insert(0, item_values[1])
            self.entry3.insert(0, item_values[2])
            self.entry4.insert(0, item_values[3])
            self.tree.delete(selected_item)

    def save_sos(self):
        with open("sos.txt", "w") as f:
            for child in self.tree.get_children():
                f.write(",".join(self.tree.item(child, "values")) + "\n")

    def sort_items(self):
        items = [(self.tree.item(child, "values"), child) for child in self.tree.get_children()]
        sorted_items = sorted(items, key=lambda x: x[0][0])
        for idx, item in enumerate(sorted_items):
            self.tree.move(item[1], "", idx)

    def select_teacher(self, teacher_number):
        self.tree.delete(*self.tree.get_children())
        teacher_data = {
            1: {"Semester 1": [("Subject1", "Description1", "Code1", "Sir Nauman")],
                "Semester 2": [("Subject2", "Description2", "Code2", "Sir Nauman")]},
            2: {"Semester 1": [("Subject3", "Description3", "Code3", "Sir Rafaqat Kazmi")],
                "Semester 2": [("Subject4", "Description4", "Code4", "Sir Rafaqat Kazmi")]},
            3: {"Semester 1": [("Subject5", "Description5", "Code5", "Ma'am Sunnia")],
                "Semester 2": [("Subject6", "Description6", "Code6", "Ma'am Sunnia")]}
        }

        self.semesters = teacher_data.get(teacher_number, {})
        self.update_sos_listbox()

    def update_sos_listbox(self):
        self.tree.delete(*self.tree.get_children())
        selected_semester = self.variable.get()
        courses = self.semesters.get(selected_semester, [])
        for course in courses:
            self.tree.insert("", "end", values=course)


if __name__ == "__main__":
    sos_manager = SOSManager()
