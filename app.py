import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import datetime

# Faculty Names
faculty_names = [
    "Pammidi Krathi Kumari", "Sugunasri Singidi", "Nakka Sindhuri", "Dandamudi Vijendra",
    "Tetla Sridhar Reddy", "Kanumuri Vinod Kumar", "Kottuthundiyil Cherian Jose"
]

# Feedback Questions
questions = [
    "Does the teacher present the lessons clearly and orderly?",
    "Does the teacher come prepared on lessons?",
    "Is the teacher capable of keeping the class under discipline and control?",
    "Does the teacher possess depth of knowledge in subject?",
    "Does the teacher speak with voice clarity and effective body language?",
    "Do you find in the teacher, a true friendly support with elderly affection?",
    "Do you find the teacher inspiring in the class as well as outside?",
    "Do you find the teacher impartial and honest in paper valuation and personal remark making?",
    "Do you find the teacher patient and considerate?",
    "Do you find the teacher unbiased and open-minded in judgment?",
    "Does the teacher remind you about your responsibility to the institution?",
    "Does the teacher insist on keeping the records up to date and neat?",
    "Does the teacher come well dressed?",
    "Is the teacher regular and punctual?",
    "Does the teacher use the blackboard/whiteboard effectively?",
    "Does the teacher help the students to clear doubts and guide them for the successful completion of the practical program?",
    "Does the teacher show readiness to give assignments to improve the studies?",
    "Does the teacher command students’ attention and give responses to students’ doubts and questions?"
]

# Feedback Options
options = ["Poor", "Improve", "Average", "Good", "Excellent"]

# Store submitted feedback to check completion
submitted_feedback = set()

# Database Setup
def initialize_database():
    conn = sqlite3.connect("feedback.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        faculty_name TEXT,
        question TEXT,
        response TEXT
    )
    """)
    conn.commit()
    conn.close()

# Check if all faculty feedback is submitted
def check_feedback_completion():
    if len(submitted_feedback) == len(faculty_names):
        messagebox.showinfo("Thank You", "Thank you for your feedback!")

# Store feedback in database
def submit_feedback(faculty_name):
    feedback_results = {question: var.get() for question, var in feedback_vars.items()}

    if all(feedback_results.values()):  # Ensure all questions are answered
        conn = sqlite3.connect("feedback.db")
        cursor = conn.cursor()

        for question, response in feedback_results.items():
            cursor.execute("INSERT INTO feedback (faculty_name, question, response) VALUES (?, ?, ?)",
                           (faculty_name, question, response))

        conn.commit()
        conn.close()

        submitted_feedback.add(faculty_name)
        messagebox.showinfo("Feedback Submitted", f"Thank you for your feedback on {faculty_name}!")
        feedback_window.destroy()
        check_feedback_completion()
    else:
        messagebox.showwarning("Incomplete Feedback", "Please select an option for each question.")

# Open feedback form
def open_feedback_form(faculty_name):
    global feedback_window, feedback_vars
    feedback_window = tk.Toplevel(root)
    feedback_window.title(f"Feedback - {faculty_name}")
    feedback_window.geometry("600x600")
    feedback_window.configure(bg="#f8f9fa")
    
    tk.Label(feedback_window, text=f"Feedback for {faculty_name}", font=("Arial", 14, "bold"), bg="#f8f9fa").pack(pady=10)
    
    canvas = tk.Canvas(feedback_window)
    scroll_frame = tk.Frame(canvas)
    scrollbar = ttk.Scrollbar(feedback_window, orient="vertical", command=canvas.yview)
    
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    
    feedback_vars = {}
    for question in questions:
        tk.Label(scroll_frame, text=question, font=("Arial", 10), wraplength=550, justify="left", bg="#f8f9fa").pack(pady=5)
        var = tk.StringVar()
        feedback_vars[question] = var
        for option in options:
            tk.Radiobutton(scroll_frame, text=option, variable=var, value=option, font=("Arial", 9), bg="#f8f9fa").pack(anchor="w")
    
    tk.Button(scroll_frame, text="Submit", command=lambda: submit_feedback(faculty_name), font=("Arial", 12), bg="#007bff", fg="white").pack(pady=20)
    
    scroll_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# Open faculty list for feedback
def open_faculty_list():
    faculty_window = tk.Toplevel(root)
    faculty_window.title("Select Faculty")
    faculty_window.geometry("400x500")
    faculty_window.configure(bg="#ffffff")
    
    tk.Label(faculty_window, text="Select Faculty for Feedback", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=10)
    
    for faculty in faculty_names:
        tk.Button(faculty_window, text=faculty, font=("Arial", 12), bg="#f0f0f0", fg="black", width=40, 
                  command=lambda f=faculty: open_feedback_form(f)).pack(pady=5)

# Retrieve and display stored feedback
def show_feedback():
    feedback_window = tk.Toplevel(root)
    feedback_window.title("Stored Feedback")
    feedback_window.geometry("600x400")

    conn = sqlite3.connect("feedback.db")
    cursor = conn.cursor()

    cursor.execute("SELECT faculty_name, question, response FROM feedback")
    rows = cursor.fetchall()
    conn.close()

    text_area = tk.Text(feedback_window, wrap="word", font=("Arial", 10))
    text_area.pack(expand=True, fill="both", padx=10, pady=10)

    for faculty_name, question, response in rows:
        text_area.insert("end", f"Faculty: {faculty_name}\nQuestion: {question}\nResponse: {response}\n\n")

    text_area.config(state="disabled")  # Make text read-only

# Initialize database
initialize_database()

# Main Dashboard
root = tk.Tk()
root.title("GGU FEEDBACK")
root.geometry("600x700")
root.configure(bg="#f8f9fa")

# Header Box
title_frame = tk.Frame(root, bg="#007bff", bd=5, relief="raised")
title_frame.pack(pady=10, padx=20, fill="x")
tk.Label(title_frame, text="GGU FEEDBACK", font=("Arial", 18, "bold"), fg="white", bg="#007bff").pack(pady=10)

# Display Date & Time
date_str = datetime.datetime.now().strftime("%A, %B %d, %Y")
tk.Label(root, text=date_str, font=("Arial", 14), fg="black", bg="#f8f9fa").pack(pady=5)

# Faculty Feedback Box
feedback_frame = tk.Frame(root, bg="#28a745", bd=5, relief="raised")
feedback_frame.pack(pady=20, padx=20, fill="x")
tk.Label(feedback_frame, text="Faculty Feedback", font=("Arial", 14, "bold"), fg="white", bg="#28a745").pack(pady=10)

# Give Feedback Button
tk.Button(root, text="Give Feedback", font=("Arial", 14, "bold"), bg="#dc3545", fg="white", 
          width=20, height=2, command=open_faculty_list).pack(pady=10)

# View Feedback Button
tk.Button(root, text="View Feedback", font=("Arial", 14, "bold"), bg="#17a2b8", fg="white", 
          width=20, height=2, command=show_feedback).pack(pady=10)

# Run Application
root.mainloop()
