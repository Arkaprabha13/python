import csv
import tkinter as tk
from tkinter import ttk

class Student:
    def __init__(self, name, roll, age):
        self.name = name
        self.rollNumber = roll
        self.age = age

    def display(self):
        return f"Name: {self.name}\nRoll Number: {self.rollNumber}\nAge: {self.age}"

    def update_information(self, new_name, new_age):
        self.name = new_name
        self.age = new_age

    def get_details_as_list(self):
        return [self.name, self.rollNumber, self.age]

class StudentManagementSystem:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def search_student(self, roll_number):
        for student in self.students:
            if student.rollNumber == roll_number:
                return student
        return None

    def update_student_information(self, roll_number, new_name, new_age):
        student = self.search_student(roll_number)
        if student:
            student.update_information(new_name, new_age)
            return "Student information updated successfully."
        else:
            return "Student not found."

    def get_all_students(self):
        return [student.display() for student in self.students]

    def export_to_csv(self):
        with open("StudentDetails.csv", mode="w", newline='') as file:
            writer = csv.writer(file)

            # Add headers
            writer.writerow(["Name", "Roll Number", "Age"])

            # Add student details
            for student in self.students:
                writer.writerow(student.get_details_as_list())

        return "Student details exported to CSV successfully."

def is_valid_name(name):
    return name.isalpha()

def is_valid_age(age):
    return age.isdigit() and 0 < int(age) <= 150  # Assuming a reasonable age range

class StudentManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")

        self.sms = StudentManagementSystem()

        self.create_widgets()

    def create_widgets(self):
        # Label
        ttk.Label(self.root, text="Student Management System", font=("Helvetica", 16)).grid(row=0, column=1, pady=10)

        # Notebook
        notebook = ttk.Notebook(self.root)
        notebook.grid(row=1, column=1, pady=10)

        # Add Student Tab
        add_student_frame = ttk.Frame(notebook)
        notebook.add(add_student_frame, text="Add Student")

        ttk.Label(add_student_frame, text="Name:").grid(row=0, column=0, pady=5)
        self.name_entry = ttk.Entry(add_student_frame)
        self.name_entry.grid(row=0, column=1, pady=5)

        ttk.Label(add_student_frame, text="Roll Number:").grid(row=1, column=0, pady=5)
        self.roll_entry = ttk.Entry(add_student_frame)
        self.roll_entry.grid(row=1, column=1, pady=5)

        ttk.Label(add_student_frame, text="Age:").grid(row=2, column=0, pady=5)
        self.age_entry = ttk.Entry(add_student_frame)
        self.age_entry.grid(row=2, column=1, pady=5)

        ttk.Button(add_student_frame, text="Add Student", command=self.add_student).grid(row=3, column=1, pady=10)

        # Display Students Tab
        display_students_frame = ttk.Frame(notebook)
        notebook.add(display_students_frame, text="Display Students")

        self.display_text = tk.Text(display_students_frame, height=10, width=40)
        self.display_text.grid(row=0, column=0, pady=10)
        ttk.Button(display_students_frame, text="Refresh", command=self.display_all_students).grid(row=1, column=0, pady=10)

        # Export to CSV Tab
        export_to_csv_frame = ttk.Frame(notebook)
        notebook.add(export_to_csv_frame, text="Export to CSV")

        ttk.Button(export_to_csv_frame, text="Export to CSV", command=self.export_to_csv).grid(row=0, column=0, pady=10)

    def add_student(self):
        name = self.name_entry.get()
        roll = self.roll_entry.get()
        age = self.age_entry.get()

        if is_valid_name(name) and is_valid_age(age):
            roll = int(roll)
            age = int(age)
            student = Student(name, roll, age)
            self.sms.add_student(student)
            self.clear_entries()
            self.display_all_students()
        else:
            tk.messagebox.showerror("Error", "Invalid name or age. Please enter valid values.")

    def display_all_students(self):
        students = self.sms.get_all_students()
        self.display_text.delete("1.0", tk.END)
        for student in students:
            self.display_text.insert(tk.END, student + "\n\n")

    def export_to_csv(self):
        message = self.sms.export_to_csv()
        tk.messagebox.showinfo("Export to CSV", message)



    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.roll_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementGUI(root)
    root.mainloop()
