
import tkinter as tk
import secrets
import string

# Dark glossy theme
BG = "#090D18"
CARD = "#151D2E"
CARD_LIGHT = "#1D2940"
CYAN = "#00E5FF"
CYAN_HOVER = "#00BFD4"
PURPLE = "#9D4EDD"
PURPLE_HOVER = "#8138C4"
SILVER = "#DCE6F2"
MUTED = "#8D9BB5"
BORDER = "#2A3A55"
GREEN = "#36E6A0"
AMBER = "#FFC857"
RED = "#FF6685"

AMBIGUOUS = "0O1lI"
history = []


def show_status(message, color=MUTED):
    status_var.set(message)
    status_label.config(fg=color)


def generate_password():
    try:
        length = int(length_var.get())
    except ValueError:
        show_status("Enter a valid password length.", RED)
        return

    if not 8 <= length <= 128:
        show_status("Length must be between 8 and 128.", RED)
        return

    groups = []

    if upper_var.get():
        groups.append(string.ascii_uppercase)
    if lower_var.get():
        groups.append(string.ascii_lowercase)
    if digits_var.get():
        groups.append(string.digits)
    if symbols_var.get():
        groups.append("!@#$%^&*()-_=+[]{};:,.?/")

    if len(groups) < 2:
        show_status("Select at least two character types.", RED)
        return

    if exclude_var.get():
        groups = [
            "".join(char for char in group if char not in AMBIGUOUS)
            for group in groups
        ]

    if any(not group for group in groups):
        show_status("Change your character selections.", RED)
        return

    if length < len(groups):
        show_status("Length is too short for your selections.", RED)
        return

    # Guarantee one character from every selected group.
    chars = [secrets.choice(group) for group in groups]
    all_chars = "".join(groups)

    for _ in range(length - len(chars)):
        chars.append(secrets.choice(all_chars))

    # Shuffle securely to avoid a predictable character order.
    for i in range(len(chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        chars[i], chars[j] = chars[j], chars[i]

    password = "".join(chars)
    password_var.set(password)
    update_strength(password)

    history.insert(0, password)
    del history[5:]
    update_history()

    show_status("Password generated successfully.", GREEN)


def update_strength(password):
    variety = sum([
        any(c.islower() for c in password),
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(c in "!@#$%^&*()-_=+[]{};:,.?/" for c in password),
    ])

    if len(password) >= 16 and variety >= 3:
        strength_var.set("STRONG")
        strength_label.config(fg=GREEN)
    elif len(password) >= 12 and variety >= 2:
        strength_var.set("MODERATE")
        strength_label.config(fg=AMBER)
    else:
        strength_var.set("BASIC")
        strength_label.config(fg=RED)


def copy_password():
    password = password_var.get()

    if not password:
        show_status("Generate a password first.", RED)
        return

    try:
        root.clipboard_clear()
        root.clipboard_append(password)
        root.update()
        show_status("Password copied to clipboard.", GREEN)
    except tk.TclError:
        show_status("Could not access the clipboard.", RED)


def clear_password():
    password_var.set("")
    strength_var.set("NOT GENERATED")
    strength_label.config(fg=MUTED)
    show_status("Ready to generate a password.")


def update_history():
    history_box.config(state="normal")
    history_box.delete("1.0", tk.END)

    if history:
        for number, password in enumerate(history, start=1):
            history_box.insert(tk.END, f"{number}. {password}\n")
    else:
        history_box.insert(
            tk.END, "Your recently generated passwords will appear here."
        )

    history_box.config(state="disabled")


def make_button(parent, text, command, bg, fg, hover_bg):
    button = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        activebackground=hover_bg,
        activeforeground=fg,
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=12,
        pady=11,
    )

    button.bind("<Enter>", lambda event: button.config(bg=hover_bg))
    button.bind("<Leave>", lambda event: button.config(bg=bg))
    return button


def make_checkbox(parent, text, variable):
    return tk.Checkbutton(
        parent,
        text=text,
        variable=variable,
        bg=CARD,
        fg=SILVER,
        activebackground=CARD,
        activeforeground=CYAN,
        selectcolor=BG,
        font=("Segoe UI", 10),
        cursor="hand2",
        padx=4,
        pady=5,
    )


# ---------------- Main window ----------------

root = tk.Tk()
root.title("Password Studio | Secure Generator")
root.geometry("640x820")
root.minsize(570, 720)
root.configure(bg=BG)

length_var = tk.StringVar(value="16")
password_var = tk.StringVar()
strength_var = tk.StringVar(value="NOT GENERATED")
status_var = tk.StringVar(value="Ready to generate a secure password.")

upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)
exclude_var = tk.BooleanVar(value=False)

# Header
header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=28, pady=(22, 16))

tk.Label(
    header,
    text="P A S S W O R D   S T U D I O",
    bg=BG,
    fg=CYAN,
    font=("Segoe UI", 10, "bold"),
).pack(anchor="w")

tk.Label(
    header,
    text="Security starts with a strong password.",
    bg=BG,
    fg=SILVER,
    font=("Segoe UI", 21, "bold"),
).pack(anchor="w", pady=(9, 4))

tk.Label(
    header,
    text="Secure randomness  •  Custom controls  •  Instant copy",
    bg=BG,
    fg=MUTED,
    font=("Segoe UI", 9),
).pack(anchor="w")

# Main content card
card = tk.Frame(
    root,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1,
)
card.pack(fill="both", expand=True, padx=24, pady=(0, 16))

# Length setting
tk.Label(
    card,
    text="01  /  PASSWORD LENGTH",
    bg=CARD,
    fg=CYAN,
    font=("Segoe UI", 10, "bold"),
).pack(anchor="w", padx=22, pady=(22, 9))

length_frame = tk.Frame(card, bg=CARD)
length_frame.pack(fill="x", padx=22)

tk.Entry(
    length_frame,
    textvariable=length_var,
    bg=BG,
    fg=CYAN,
    insertbackground=CYAN,
    font=("Consolas", 13, "bold"),
    relief="flat",
    justify="center",
    width=8,
    highlightthickness=1,
    highlightbackground=BORDER,
    highlightcolor=CYAN,
).pack(side="left", ipady=9)

tk.Label(
    length_frame,
    text="Characters  |  Minimum 8, maximum 128",
    bg=CARD,
    fg=MUTED,
    font=("Segoe UI", 9),
).pack(side="left", padx=12)

# Character options
tk.Label(
    card,
    text="02  /  CHARACTER OPTIONS",
    bg=CARD,
    fg=CYAN,
    font=("Segoe UI", 10, "bold"),
).pack(anchor="w", padx=22, pady=(22, 8))

options_frame = tk.Frame(card, bg=CARD)
options_frame.pack(fill="x", padx=18)

make_checkbox(
    options_frame, "Uppercase (A–Z)", upper_var
).grid(row=0, column=0, sticky="w", padx=4)

make_checkbox(
    options_frame, "Lowercase (a–z)", lower_var
).grid(row=0, column=1, sticky="w", padx=4)

make_checkbox(
    options_frame, "Numbers (0–9)", digits_var
).grid(row=1, column=0, sticky="w", padx=4)

make_checkbox(
    options_frame, "Symbols (!@#...)", symbols_var
).grid(row=1, column=1, sticky="w", padx=4)

make_checkbox(
    card,
    "Exclude ambiguous characters (0, O, 1, l, I)",
    exclude_var,
).pack(anchor="w", padx=22, pady=(8, 12))

# Generate password button
make_button(
    card,
    "GENERATE SECURE PASSWORD",
    generate_password,
    PURPLE,
    "#FFFFFF",
    PURPLE_HOVER,
).pack(fill="x", padx=22, pady=(0, 20))

# Generated password display
tk.Label(
    card,
    text="03  /  YOUR PASSWORD",
    bg=CARD,
    fg=CYAN,
    font=("Segoe UI", 10, "bold"),
).pack(anchor="w", padx=22, pady=(0, 8))

tk.Entry(
    card,
    textvariable=password_var,
    bg=BG,
    fg=CYAN,
    insertbackground=CYAN,
    font=("Consolas", 13),
    relief="flat",
    justify="center",
    highlightthickness=1,
    highlightbackground=BORDER,
    highlightcolor=CYAN,
).pack(fill="x", padx=22, ipady=13)

# Strength indicator
strength_frame = tk.Frame(card, bg=CARD)
strength_frame.pack(fill="x", padx=22, pady=(12, 14))

tk.Label(
    strength_frame,
    text="PASSWORD STRENGTH",
    bg=CARD,
    fg=MUTED,
    font=("Segoe UI", 9, "bold"),
).pack(side="left")

strength_label = tk.Label(
    strength_frame,
    textvariable=strength_var,
    bg=CARD,
    fg=MUTED,
    font=("Segoe UI", 10, "bold"),
)
strength_label.pack(side="right")

# Copy and clear buttons
button_frame = tk.Frame(card, bg=CARD)
button_frame.pack(fill="x", padx=22, pady=(0, 19))

make_button(
    button_frame,
    "COPY PASSWORD",
    copy_password,
    CYAN,
    BG,
    CYAN_HOVER,
).pack(side="left", fill="x", expand=True, padx=(0, 6))

make_button(
    button_frame,
    "CLEAR",
    clear_password,
    CARD_LIGHT,
    SILVER,
    BORDER,
).pack(side="left", fill="x", expand=True, padx=(6, 0))

# Recent password history
tk.Label(
    card,
    text="04  /  RECENT PASSWORDS",
    bg=CARD,
    fg=CYAN,
    font=("Segoe UI", 10, "bold"),
).pack(anchor="w", padx=22, pady=(0, 8))

history_box = tk.Text(
    card,
    height=4,
    bg=BG,
    fg=SILVER,
    font=("Consolas", 9),
    relief="flat",
    wrap="word",
    padx=12,
    pady=8,
    highlightthickness=1,
    highlightbackground=BORDER,
    state="disabled",
)
history_box.pack(fill="x", padx=22)

# Status message
status_label = tk.Label(
    card,
    textvariable=status_var,
    bg=CARD,
    fg=MUTED,
    font=("Segoe UI", 9),
    wraplength=520,
)
status_label.pack(anchor="w", padx=22, pady=(12, 18))

# Footer
tk.Label(
    root,
    text="Session-only history  |  Passwords are not saved to a file",
    bg=BG,
    fg=MUTED,
    font=("Segoe UI", 8),
).pack(pady=(0, 12))

update_history()
root.mainloop()
