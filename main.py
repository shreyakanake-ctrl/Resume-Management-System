import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

window = tk.Tk()
window.title("Resume Management System")
window.geometry("400x300")

title = tk.Label(window, text="RESUME MANAGEMENT SYSTEM")
title.pack(pady=30)

username_label = tk.Label(window, text="Username")
username_label.pack()

username_entry = tk.Entry(window)
username_entry.pack()

password_label = tk.Label(window, text="Password")
password_label.pack()

password_entry = tk.Entry(window, show="*")
password_entry.pack()

def save_update(resume_id, name_entry, email_entry,
                phone_entry, skills_entry, update):

    name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    skills = skills_entry.get()

    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password= MYSQL_PASSWORD,
        database="resume_management"
    )

    cursor = conn.cursor()

    query = """
    UPDATE resumes
    SET full_name=%s, email=%s, phone=%s, skills=%s
    WHERE resume_id=%s
    """

    values = (name, email, phone, skills, resume_id)

    cursor.execute(query, values)
    conn.commit()

    messagebox.showinfo("Success", "Resume updated successfully!")

    cursor.close()
    conn.close()
    update.destroy()

def update_resume(tree):
    selected = tree.focus()

    if not selected:
        messagebox.showwarning("Warning", "Please select a resume first")
        return

    record = tree.item(selected)["values"]

    update = tk.Toplevel(window)
    update.title("Update Resume")
    update.geometry("500x600")

    tk.Label(update, text="Update Resume",
             font=("Arial", 18, "bold")).pack(pady=15)

    tk.Label(update, text="Name").pack()
    name_entry = tk.Entry(update, width=40)
    name_entry.pack()
    name_entry.insert(0, record[1])

    tk.Label(update, text="Email").pack()
    email_entry = tk.Entry(update, width=40)
    email_entry.pack()
    email_entry.insert(0, record[2])

    tk.Label(update, text="Phone").pack()
    phone_entry = tk.Entry(update, width=40)
    phone_entry.pack()
    phone_entry.insert(0, record[3])

    tk.Label(update, text="Skills").pack()
    skills_entry = tk.Entry(update, width=40)
    skills_entry.pack()
    skills_entry.insert(0, record[9])

    tk.Button(
    update,
    text="UPDATE",
    width=20,
    command=lambda: save_update(
        record[0],
        name_entry,
        email_entry,
        phone_entry,
        skills_entry,
        update
    )
).pack(pady=20)


def save_resume(name_entry, email_entry, phone_entry, address_entry,
                qualification_entry, college_entry, year_entry,
                percentage_entry, skills_entry, experience_entry,
                projects_entry):

    name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    address = address_entry.get()
    qualification = qualification_entry.get()
    college = college_entry.get()
    year = year_entry.get()
    percentage = percentage_entry.get()
    skills = skills_entry.get()
    experience = experience_entry.get()
    projects = projects_entry.get()

    if name == "" or email == "" or phone == "":
        messagebox.showwarning(
            "Warning",
            "Please fill Name, Email and Phone"
        )
        return

    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password=MYSQL_PASSWORD,
        database="resume_management"
    )

    cursor = conn.cursor()

    query = """
    INSERT INTO resumes
    (full_name, email, phone, address, qualification, college,
     passing_year, percentage, skills, experience, projects)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        name, email, phone, address, qualification, college,
        year, percentage, skills, experience, projects
    )

    cursor.execute(query, values)
    conn.commit()

    messagebox.showinfo("Success", "Resume saved successfully!")

    cursor.close()
    conn.close()

def delete_resume(tree):
    selected = tree.focus()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a resume first"
        )
        return

    record = tree.item(selected)["values"]
    resume_id = record[0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this resume?"
    )

    if not confirm:
        return

    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password=MYSQL_PASSWORD,
        database="resume_management"
    )

    cursor = conn.cursor()

    query = "DELETE FROM resumes WHERE resume_id=%s"
    cursor.execute(query, (resume_id,))
    conn.commit()

    cursor.close()
    conn.close()

    tree.delete(selected)

    messagebox.showinfo(
        "Success",
        "Resume deleted successfully!"
    )



def view_resumes():
    view = tk.Toplevel(window)
    view.title("View Resumes")
    view.geometry("1000x500")

    tk.Label(
        view,
        text="ALL RESUMES",
        font=("Arial", 18, "bold")
    ).pack(pady=15)

    columns = (
        "ID", "Name", "Email", "Phone", "Address",
        "Qualification", "College", "Year", "Percentage",
        "Skills", "Experience", "Projects"
    )

    tree = ttk.Treeview(view, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    tree.pack(fill="both", expand=True)
    tk.Button(
    view,
    text="UPDATE SELECTED",
    width=20,
    command=lambda: update_resume(tree)
).pack(pady=10)

    tk.Button(
    view,
    text="DELETE SELECTED",
    width=20,
    command=lambda: delete_resume(tree)
).pack(pady=5)

    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password=MYSQL_PASSWORD,
        database="resume_management"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM resumes")

    records = cursor.fetchall()

    for record in records:
        tree.insert("", tk.END, values=record)

    cursor.close()
    conn.close()



def add_resume():
    add = tk.Toplevel(window)
    add.title("Add Resume")
    add.geometry("500x700")

    tk.Label(add, text="ADD RESUME",
             font=("Arial", 18, "bold")).pack(pady=20)

    tk.Label(add, text="Full Name").pack()
    name_entry = tk.Entry(add)
    name_entry.pack()

    tk.Label(add, text="Email").pack()
    email_entry = tk.Entry(add)
    email_entry.pack()

    tk.Label(add, text="Phone").pack()
    phone_entry = tk.Entry(add)
    phone_entry.pack()

    tk.Label(add, text="Address").pack()
    address_entry = tk.Entry(add)
    address_entry.pack()

    tk.Label(add, text="Qualification").pack()
    qualification_entry = tk.Entry(add)
    qualification_entry.pack()

    tk.Label(add, text="College").pack()
    college_entry = tk.Entry(add)
    college_entry.pack()

    tk.Label(add, text="Passing Year").pack()
    year_entry = tk.Entry(add)
    year_entry.pack()

    tk.Label(add, text="Percentage").pack()
    percentage_entry = tk.Entry(add)
    percentage_entry.pack()

    tk.Label(add, text="Skills").pack()
    skills_entry = tk.Entry(add)
    skills_entry.pack()

    tk.Label(add, text="Experience").pack()
    experience_entry = tk.Entry(add)
    experience_entry.pack()

    tk.Label(add, text="Projects").pack()
    projects_entry = tk.Entry(add)
    projects_entry.pack()

    
    tk.Button(
    add,
    text="SAVE",
    command=lambda: save_resume(
        name_entry,
        email_entry,
        phone_entry,
        address_entry,
        qualification_entry,
        college_entry,
        year_entry,
        percentage_entry,
        skills_entry,
        experience_entry,
        projects_entry
    )
).pack(pady=20)

    tk.Button(
    add,
    text="CLEAR",
    width=20,
    command=lambda: clear_form(
        name_entry,
        email_entry,
        phone_entry,
        address_entry,
        qualification_entry,
        college_entry,
        year_entry,
        percentage_entry,
        skills_entry,
        experience_entry,
        projects_entry
    )
).pack(pady=5)

def clear_form(
    name_entry,
    email_entry,
    phone_entry,
    address_entry,
    qualification_entry,
    college_entry,
    year_entry,
    percentage_entry,
    skills_entry,
    experience_entry,
    projects_entry
):

    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    qualification_entry.delete(0, tk.END)
    college_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    percentage_entry.delete(0, tk.END)
    skills_entry.delete(0, tk.END)
    experience_entry.delete(0, tk.END)
    projects_entry.delete(0, tk.END)



def search_resume():

    search = tk.Toplevel(window)
    search.title("Search Resume")
    search.geometry("800x500")

    tk.Label(
        search,
        text="SEARCH RESUME",
        font=("Arial", 18, "bold")
    ).pack(pady=15)

    tk.Label(search, text="Enter Name").pack()

    search_entry = tk.Entry(search, width=40)
    search_entry.pack(pady=10)

    columns = ("ID", "Name", "Email", "Phone", "Skills")

    tree = ttk.Treeview(
        search,
        columns=columns,
        show="headings"
    )

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=140)

    tree.pack(fill="both", expand=True, pady=10)

    def search_data():

        for item in tree.get_children():
            tree.delete(item)

        name = search_entry.get()

        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password=MYSQL_PASSWORD,
            database="resume_management"
        )

        cursor = conn.cursor()

        query = """
        SELECT resume_id, full_name, email, phone, skills
        FROM resumes
        WHERE full_name LIKE %s
        """

        cursor.execute(query, ("%" + name + "%",))

        records = cursor.fetchall()

        for record in records:
            tree.insert("", tk.END, values=record)

        cursor.close()
        conn.close()

    tk.Button(
        search,
        text="SEARCH",
        width=20,
        command=search_data
    ).pack(pady=10)

def dashboard():
    dash = tk.Toplevel(window)
    dash.title("Dashboard")
    dash.geometry("500x400")

    title = tk.Label(
        dash,
        text="RESUME MANAGEMENT SYSTEM",
        font=("Arial", 18, "bold")
    )
    title.pack(pady=30)

    tk.Button(dash, text="Add Resume", width=20, command=add_resume).pack(pady=10)
    tk.Button(
        dash,
        text="View Resumes",
        width=20,
        command=view_resumes
    ).pack(pady=10)
    tk.Button(
    dash,
    text="Search Resume",
    width=20,
    command=search_resume
).pack(pady=10)
    tk.Button(
    dash,
    text="Logout",
    width=20,
    command=dash.destroy
).pack(pady=10)

def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "Admin" and password == "Admin123":
        messagebox.showinfo("Login", "Login Successful")
        dashboard()
    else:
        messagebox.showerror("Login", "Invalid Username or Password")

login_button = tk.Button(window, text="LOGIN", command=login)
login_button.pack(pady=20)

window.mainloop()