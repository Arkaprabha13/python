import csv

class Student:
    def __init__(self, name, roll, age):
        self.name = name
        self.rollNumber = roll
        self.age = age

    def display(self):
        print(f"Name: {self.name}\nRoll Number: {self.rollNumber}\nAge: {self.age}")

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

    def display_all_students(self):
        print("=== All Students ===")
        for student in self.students:
            student.display()
            print("---------------------")

    def search_student(self, roll_number):
        for student in self.students:
            if student.rollNumber == roll_number:
                return student
        return None

    def update_student_information(self, roll_number, new_name, new_age):
        student = self.search_student(roll_number)
        if student:
            student.update_information(new_name, new_age)
            print("Student information updated successfully.")
        else:
            print("Student not found.")

    def export_to_csv(self):
        with open("StudentDetails.csv", mode="w", newline='') as file:
            writer = csv.writer(file)
            
            # Add headers
            writer.writerow(["Name", "Roll Number", "Age"])

            # Add student details
            for student in self.students:
                writer.writerow(student.get_details_as_list())

        print("Student details exported to CSV successfully.")

def is_valid_name(name):
    return name.isalpha()

def is_valid_age(age):
    return age.isdigit() and 0 < int(age) <= 150  # Assuming a reasonable age range

def display_menu():
    print("\n===== Student Management System =====")
    print("1. Add Student")
    print("2. Display All Students")
    print("3. Search Student")
    print("4. Update Student Information")
    print("5. Export to CSV")
    print("6. Exit")

def main():
    sms = StudentManagementSystem()

    while True:
        display_menu()

        choice = int(input("Enter your choice: "))

        if choice == 1:
            name = input("Enter student name: ")
            age = input("Enter age: ")

            if is_valid_name(name) and is_valid_age(age):
                roll = int(input("Enter roll number: "))
                sms.add_student(Student(name, roll, int(age)))
                print("Student added successfully.")
            else:
                print("Invalid name or age. Please enter valid values.")
        elif choice == 2:
            sms.display_all_students()
        elif choice == 3:
            roll_number = int(input("Enter roll number to search: "))
            found_student = sms.search_student(roll_number)
            if found_student:
                print("Student found:")
                found_student.display()
            else:
                print("Student not found.")
        elif choice == 4:
            roll_number = int(input("Enter roll number to update: "))
            new_name = input("Enter new name: ")
            new_age = input("Enter new age: ")

            if is_valid_name(new_name) and is_valid_age(new_age):
                sms.update_student_information(roll_number, new_name, int(new_age))
            else:
                print("Invalid name or age. Please enter valid values.")
        elif choice == 5:
            sms.export_to_csv()
        elif choice == 6:
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
