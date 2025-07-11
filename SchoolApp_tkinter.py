import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
from datetime import datetime
import json

try:
    import sv_ttk
except ImportError:
    sv_ttk = None
from advanced_linked_list import SchoolSystem
from fee_manager import FeeStack
from school_map import find_shortest_path, get_locations, school_map

class Teacher:
    def _init_(self, name, emp_id, subject, department, email):
        self.name = name
        self.emp_id = emp_id
        self.subject = subject
        self.department = department
        self.email = email
        self.entry_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            'type': 'Teacher',
            'name': self.name,
            'emp_id': self.emp_id,
            'subject': self.subject,
            'department': self.department,
            'email': self.email,
            'entry_date': self.entry_date
        }

class SchoolApp:
    def _init_(self, root):
        self.root = root
        self.root.title("School Management System")
        self.root.geometry("800x600")

        self.school_system = SchoolSystem()
        self.fee_stack = FeeStack()
        self.record_queue = deque()
        self.load_records()

        if sv_ttk:
            sv_ttk.set_theme("light")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, padx=10, fill="both", expand=True)

        self.create_student_tab()
        self.create_fee_tab()
        self.create_navigation_tab()
        self.create_teacher_tab()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    # Helper Functions
    def add_labeled_entry(self, tab, row, label_text):
        ttk.Label(tab, text=label_text).grid(row=row, column=0, padx=5, pady=5, sticky="e")
        entry = ttk.Entry(tab)
        entry.grid(row=row, column=1, padx=5, pady=5)
        return entry

    def add_labeled_combobox(self, tab, row, label_text, values):
        ttk.Label(tab, text=label_text).grid(row=row, column=0, padx=5, pady=5, sticky="e")
        combo = ttk.Combobox(tab, values=values)
        combo.grid(row=row, column=1, padx=5, pady=5)
        return combo

    def add_button(self, tab, row, text, command):
        ttk.Button(tab, text=text, command=command).grid(row=row, column=0, columnspan=2, pady=5)

    def add_output_text(self, tab, row):
        output = tk.Text(tab, height=10, width=60)
        output.grid(row=row, column=0, columnspan=2, padx=5, pady=10)
        output.config(state="disabled")
        return output

    def update_output(self, output_widget, text):
        output_widget.config(state="normal")
        output_widget.delete(1.0, tk.END)
        output_widget.insert(tk.END, text)
        output_widget.config(state="disabled")

    def get_int_entry(self, entry_widget, error_message):
        try:
            return int(entry_widget.get())
        except ValueError:
            messagebox.showerror("Error", error_message)
            return None

    def get_float_entry(self, entry_widget, error_message):
        try:
            return float(entry_widget.get())
        except ValueError:
            messagebox.showerror("Error", error_message)
            return None

    # Tab Creation
    def create_student_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Student Management")

        self.student_id_entry = self.add_labeled_entry(tab, 0, "Student ID:")
        self.student_name_entry = self.add_labeled_entry(tab, 1, "Name:")
        self.student_grade_entry = self.add_labeled_entry(tab, 2, "Grade:")

        self.add_button(tab, 3, "Add Student", self.add_student)
        self.add_button(tab, 4, "Transfer Student", self.transfer_student)
        self.add_button(tab, 5, "Remove Student", self.remove_student)
        self.add_button(tab, 6, "View Students", self.view_students)

        self.student_output = self.add_output_text(tab, 7)

    def create_fee_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Fee Management")

        self.fee_student_id_entry = self.add_labeled_entry(tab, 0, "Student ID:")
        self.fee_amount_entry = self.add_labeled_entry(tab, 1, "Amount ($):")

        self.add_button(tab, 2, "Add Payment", self.add_payment)
        self.add_button(tab, 3, "Check Latest Payment", self.check_latest_payment)
        self.add_button(tab, 4, "Remove Latest Payment", self.remove_latest_payment)
        self.add_button(tab, 5, "View Balance", self.view_balance)
        self.add_button(tab, 6, "View Payment History", self.view_payment_history)

        self.fee_output = self.add_output_text(tab, 7)

    def create_navigation_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="School Navigation")

        locations = get_locations()
        self.start_location = self.add_labeled_combobox(tab, 0, "Start Location:", locations)
        self.start_location.set("Main Gate")
        self.end_location = self.add_labeled_combobox(tab, 1, "End Location:", locations)
        self.end_location.set("Lab")

        self.add_button(tab, 2, "Find Shortest Path", self.find_path)

        self.nav_output = self.add_output_text(tab, 3)

    def create_teacher_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Teacher Management")

        self.teacher_name_entry = self.add_labeled_entry(tab, 0, "Teacher Name:")
        self.teacher_id_entry = self.add_labeled_entry(tab, 1, "Teacher ID:")
        self.teacher_subject_entry = self.add_labeled_entry(tab, 2, "Subject:")
        self.teacher_dept_entry = self.add_labeled_entry(tab, 3, "Department:")
        self.teacher_email_entry = self.add_labeled_entry(tab, 4, "Email:")

        self.add_button(tab, 5, "Add Teacher", self.add_teacher)
        self.add_button(tab, 6, "View Records", self.view_all_records)
        self.add_button(tab, 7, "Save Records", self.save_records)

        self.teacher_output = self.add_output_text(tab, 8)

    # Student Methods
    def add_student(self):
        student_id = self.get_int_entry(self.student_id_entry, "Invalid student ID")
        if student_id is None or student_id < 0:
            return
        name = self.student_name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Name cannot be empty")
            return
        grade = self.get_int_entry(self.student_grade_entry, "Invalid grade")
        if grade is None or grade < 0:
            return
        self.school_system.add_student(student_id, name, grade)
        messagebox.showinfo("Success", f"Student {name} added!")
        self.student_id_entry.delete(0, tk.END)
        self.student_name_entry.delete(0, tk.END)
        self.student_grade_entry.delete(0, tk.END)

    def transfer_student(self):
        student_id = self.get_int_entry(self.student_id_entry, "Invalid student ID")
        if student_id is None:
            return
        to_grade = self.get_int_entry(self.student_grade_entry, "Invalid grade")
        if to_grade is None:
            return
        if self.school_system.transfer_student(student_id, to_grade):
            messagebox.showinfo("Success", f"Student ID {student_id} transferred to grade {to_grade}.")
        else:
            messagebox.showerror("Error", "Student not found.")
        self.student_id_entry.delete(0, tk.END)
        self.student_grade_entry.delete(0, tk.END)

    def remove_student(self):
        student_id = self.get_int_entry(self.student_id_entry, "Invalid student ID")
        if student_id is None:
            return
        if self.school_system.students.remove('id', student_id):
            messagebox.showinfo("Success", f"Student ID {student_id} removed.")
        else:
            messagebox.showerror("Error", "Student not found.")
        self.student_id_entry.delete(0, tk.END)

    def view_students(self):
        current = self.school_system.students.head
        output = "Students:\n"
        while current:
            data = current.data
            output += f"ID: {data['id']}, Name: {data['name']}, Grade: {data['grade']}\n"
            current = current.next
        self.update_output(self.student_output, output)

    # Fee Methods
    def add_payment(self):
        student_id = self.fee_student_id_entry.get().strip()
        if not student_id:
            messagebox.showerror("Error", "Student ID cannot be empty")
            return
        amount = self.get_float_entry(self.fee_amount_entry, "Invalid amount")
        if amount is None or amount <= 0:
            messagebox.showerror("Error", "Amount must be positive")
            return
        self.fee_stack.push(student_id, amount)
        messagebox.showinfo("Success", f"Payment of ${amount:.2f} added for {student_id}.")
        self.fee_student_id_entry.delete(0, tk.END)
        self.fee_amount_entry.delete(0, tk.END)

    def check_latest_payment(self):
        latest_payment = self.fee_stack.peek()
        if latest_payment:
            output = (
                f"Latest Payment:\n"
                f"Student ID: {latest_payment['student_id']}\n"
                f"Amount: ${latest_payment['amount']:.2f}\n"
                f"Time: {latest_payment['timestamp']}\n"
            )
            self.update_output(self.fee_output, output)
        else:
            self.update_output(self.fee_output, "No payments recorded.")

    def remove_latest_payment(self):
        removed_payment = self.fee_stack.pop()
        if removed_payment:
            output = (
                f"Removed Payment:\n"
                f"Student ID: {removed_payment['student_id']}\n"
                f"Amount: ${removed_payment['amount']:.2f}\n"
                f"Time: {removed_payment['timestamp']}\n"
                f"New Balance: ${self.fee_stack.get_balance():.2f}\n"
            )
            messagebox.showinfo("Success", f"Payment of ${removed_payment['amount']:.2f} removed for {removed_payment['student_id']}.")
            self.update_output(self.fee_output, output)
        else:
            messagebox.showerror("Error", "No payments to remove.")
            self.update_output(self.fee_output, "No payments recorded.")

    def view_balance(self):
        balance = self.fee_stack.get_balance()
        self.update_output(self.fee_output, f"Current Balance: ${balance:.2f}\n")

    def view_payment_history(self):
        payments = self.fee_stack.get_all_payments()
        output = "Payment History (Newest First):\n"
        for payment in payments:
            output += f"ID: {payment['student_id']}, Amount: ${payment['amount']:.2f}, Time: {payment['timestamp']}\n"
        self.update_output(self.fee_output, output)

    # Navigation Methods
    def find_path(self):
        start = self.start_location.get()
        end = self.end_location.get()
        result = find_shortest_path(school_map, start, end)
        if result["status"] == "success":
            path = " -> ".join(result["path"])
            output = f"Shortest Path: {path}\nDistance: {result['distance']} units"
        else:
            output = "No path found or invalid locations."
        self.update_output(self.nav_output, output)
    # Teacher Methods
    def add_teacher(self):
        name = self.teacher_name_entry.get().strip()
        emp_id = self.teacher_id_entry.get().strip()
        subject = self.teacher_subject_entry.get().strip()
        department = self.teacher_dept_entry.get().strip()
        email = self.teacher_email_entry.get().strip()
        if not all([name, emp_id, subject, department, email]):
            messagebox.showerror("Error", "All teacher fields must be filled")
            return
        teacher = Teacher(name, emp_id, subject, department, email)
        self.record_queue.append(teacher)
        messagebox.showinfo("Success", f"Teacher {name} added to records.")
        self.teacher_name_entry.delete(0, tk.END)
        self.teacher_id_entry.delete(0, tk.END)
        self.teacher_subject_entry.delete(0, tk.END)
        self.teacher_dept_entry.delete(0, tk.END)
        self.teacher_email_entry.delete(0, tk.END)

    def view_all_records(self):
        if not self.record_queue:
            output = "No teacher records found.\n"
        else:
            output = "Teacher Records:\n"
            for i, teacher in enumerate(self.record_queue, 1):
                data = teacher.to_dict()
                output += f"{i}. {data['name']} - ID: {data['emp_id']} - {data['subject']} - {data['department']} - {data['email']} - {data['entry_date']}\n"
        self.update_output(self.teacher_output, output)

    def save_records(self):
        try:
            with open("teacher_records.json", "w") as f:
                json.dump([teacher.to_dict() for teacher in self.record_queue], f, indent=4)
            messagebox.showinfo("Success", "Records saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save records: {e}")

    def load_records(self):
        try:
            with open("teacher_records.json", "r") as f:
                data = json.load(f)
                self.record_queue.clear()
                for item in data:
                    if item['type'] == 'Teacher':
                        teacher = Teacher(item['name'], item['emp_id'], item['subject'], item['department'], item['email'])
                        teacher.entry_date = item['entry_date']
                        self.record_queue.append(teacher)
        except FileNotFoundError:
            self.record_queue.clear()

    def on_closing(self):
        self.save_records()
        self.root.destroy()

if _name_ == "_main_":
    root = tk.Tk()
    app = SchoolApp(root)
    root.mainloop()
