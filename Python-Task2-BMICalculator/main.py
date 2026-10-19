
import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

DB_NAME = "bmi_history.db"

# Pastel color palette
PINK = "#F7DCE5"
BABY_PINK = "#FCE8EF"
WHITE = "#FFFFFF"
BABY_BLUE = "#A9D6F5"
BLUE_HOVER = "#83BDE8"
DARK_TEXT = "#45566B"
MUTED_TEXT = "#7B899B"
BORDER = "#E8C1D0"


def create_database():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL,
                recorded_at TEXT NOT NULL
            )
        """)


def calculate_bmi():
    name = name_entry.get().strip()
    weight_text = weight_entry.get().strip()
    height_text = height_entry.get().strip()

    if not name or not weight_text or not height_text:
        messagebox.showerror(
            "Missing Information",
            "Please fill in all fields."
        )
        return

    try:
        weight = float(weight_text)
        height_cm = float(height_text)
    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Weight and height must be numbers."
        )
        return

    if weight <= 0 or height_cm <= 0:
        messagebox.showerror(
            "Invalid Input",
            "Weight and height must be greater than zero."
        )
        return

    if weight > 500 or height_cm > 300:
        messagebox.showerror(
            "Invalid Input",
            "Please check your weight and height values."
        )
        return

    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)

    if bmi < 18.5:
        category = "Underweight"
        result_color = "#729BC2"
    elif bmi < 25:
        category = "Normal weight"
        result_color = "#579C83"
    elif bmi < 30:
        category = "Overweight"
        result_color = "#D39A52"
    else:
        category = "Obesity"
        result_color = "#C96F88"

    result_label.config(
        text=f"BMI: {bmi:.2f}\nCategory: {category}",
        fg=result_color
    )

    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute(
                """
                INSERT INTO bmi_records
                (name, weight, height, bmi, category, recorded_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    weight,
                    height_cm,
                    bmi,
                    category,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
            )

        messagebox.showinfo(
            "Saved",
            "Your result has been saved to history."
        )

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not save the result:\n{error}"
        )


def show_history():
    try:
        with sqlite3.connect(DB_NAME) as conn:
            records = conn.execute("""
                SELECT name, weight, height, bmi, category, recorded_at
                FROM bmi_records
                ORDER BY id DESC
                LIMIT 20
            """).fetchall()

    except sqlite3.Error as error:
        messagebox.showerror("Database Error", str(error))
        return

    history_window = tk.Toplevel(root)
    history_window.title("BMI History")
    history_window.geometry("850x420")
    history_window.configure(bg=BABY_PINK)

    tk.Label(
        history_window,
        text="Your BMI History",
        font=("Segoe UI", 20, "bold"),
        fg=DARK_TEXT,
        bg=BABY_PINK
    ).pack(pady=15)

    table_frame = tk.Frame(history_window, bg=WHITE)
    table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    scrollbar = tk.Scrollbar(table_frame)
    scrollbar.pack(side="right", fill="y")

    table = tk.Text(
        table_frame,
        bg=WHITE,
        fg=DARK_TEXT,
        font=("Consolas", 10),
        wrap="none",
        yscrollcommand=scrollbar.set,
        relief="flat",
        padx=10,
        pady=10
    )
    table.pack(fill="both", expand=True)
    scrollbar.config(command=table.yview)

    table.insert(
        "end",
        f"{'Name':<16}{'Weight':<10}{'Height':<10}"
        f"{'BMI':<9}{'Category':<16}Date\n"
    )
    table.insert("end", "-" * 100 + "\n")

    for record in records:
        name, weight, height, bmi, category, recorded_at = record
        table.insert(
            "end",
            f"{name[:15]:<16}{weight:<10.1f}{height:<10.1f}"
            f"{bmi:<9.2f}{category:<16}{recorded_at}\n"
        )

    if not records:
        table.insert("end", "\nNo BMI records saved yet.")

    table.configure(state="disabled")


def add_field(label_text):
    tk.Label(
        form_frame,
        text=label_text,
        font=("Segoe UI", 11, "bold"),
        fg=DARK_TEXT,
        bg=WHITE
    ).pack(anchor="w", pady=(10, 4))

    entry = tk.Entry(
        form_frame,
        font=("Segoe UI", 12),
        bg="#FAFCFF",
        fg=DARK_TEXT,
        insertbackground=DARK_TEXT,
        relief="flat",
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=BLUE_HOVER
    )
    entry.pack(fill="x", ipady=8)
    return entry


create_database()

root = tk.Tk()
root.title("BMI Calculator | Pastel Edition")
root.geometry("540x720")
root.minsize(500, 680)
root.configure(bg=BABY_PINK)

# Header
header = tk.Frame(root, bg=BABY_PINK)
header.pack(fill="x", pady=(25, 15))

tk.Label(
    header,
    text="BMI CALCULATOR",
    font=("Segoe UI", 26, "bold"),
    fg=DARK_TEXT,
    bg=BABY_PINK
).pack()

tk.Label(
    header,
    text="A simple way to calculate and track your BMI",
    font=("Segoe UI", 11),
    fg=MUTED_TEXT,
    bg=BABY_PINK
).pack(pady=(6, 0))

# Main white card
card = tk.Frame(
    root,
    bg=WHITE,
    highlightthickness=1,
    highlightbackground=BORDER
)
card.pack(fill="both", expand=True, padx=28, pady=(5, 20))

form_frame = tk.Frame(card, bg=WHITE)
form_frame.pack(fill="x", padx=28, pady=(20, 5))

name_entry = add_field("Your name")
weight_entry = add_field("Weight (kg)")
height_entry = add_field("Height (cm)")

# Calculate button
calculate_button = tk.Button(
    card,
    text="Calculate BMI",
    command=calculate_bmi,
    font=("Segoe UI", 12, "bold"),
    bg=BABY_BLUE,
    fg=DARK_TEXT,
    activebackground=BLUE_HOVER,
    activeforeground=DARK_TEXT,
    relief="flat",
    cursor="hand2",
    bd=0
)
calculate_button.pack(fill="x", padx=28, pady=(18, 12), ipady=10)

# Result panel
result_frame = tk.Frame(card, bg=BABY_PINK)
result_frame.pack(fill="x", padx=28, pady=5)

result_label = tk.Label(
    result_frame,
    text="Your result will appear here",
    font=("Segoe UI", 15, "bold"),
    fg=MUTED_TEXT,
    bg=BABY_PINK,
    justify="center",
    pady=15
)
result_label.pack(fill="x")

# History button
history_button = tk.Button(
    card,
    text="View BMI History",
    command=show_history,
    font=("Segoe UI", 11, "bold"),
    bg=PINK,
    fg=DARK_TEXT,
    activebackground=BORDER,
    activeforeground=DARK_TEXT,
    relief="flat",
    cursor="hand2",
    bd=0
)
history_button.pack(fill="x", padx=28, pady=(12, 10), ipady=8)

# Disclaimer
tk.Label(
    card,
    text="BMI is a screening measure, not a medical diagnosis.",
    font=("Segoe UI", 9),
    fg=MUTED_TEXT,
    bg=WHITE,
    wraplength=400
).pack(pady=(8, 18))

root.mainloop()
