import tkinter as tk
import re
import string
import secrets


# =====================================================
# PASSWORD LAB - VERSION 5.5
# =====================================================

root = tk.Tk()
root.title("Password Lab - Password Strength Analyzer")
root.geometry("900x780")
root.minsize(650, 500)


# =====================================================
# THEMES
# =====================================================

current_theme = "dark"

themes = {
    "light": {
        "root": "#F3F4FA",
        "card": "#FFFFFF",
        "input": "#F1F3F9",
        "text": "#20243A",
        "muted": "#747B91",
        "border": "#DDE1EC",
        "accent": "#7057E8",
        "accent_hover": "#5D43D0",
        "success": "#16A36A",
        "warning": "#E99B24",
        "danger": "#E34F64",
        "check_bg": "#F5F6FB",
        "tip_bg": "#F0EDFF",
        "crack_bg": "#EAF7F0",
        "progress_bg": "#E4E6EF",
        "button_text": "#FFFFFF"
    },

    "dark": {
        "root": "#101522",
        "card": "#1B2435",
        "input": "#252F43",
        "text": "#F1F3FA",
        "muted": "#A5AEC1",
        "border": "#303C52",
        "accent": "#927BFF",
        "accent_hover": "#A795FF",
        "success": "#39D98A",
        "warning": "#FFC15A",
        "danger": "#FF7185",
        "check_bg": "#222D40",
        "tip_bg": "#292545",
        "crack_bg": "#203A34",
        "progress_bg": "#303C52",
        "button_text": "#FFFFFF"
    }
}

colors = themes[current_theme]


# =====================================================
# SCROLLABLE WINDOW
# =====================================================

outer_frame = tk.Frame(root, bg=colors["root"])
outer_frame.pack(fill="both", expand=True)

main_canvas = tk.Canvas(
    outer_frame,
    bg=colors["root"],
    highlightthickness=0
)

scrollbar = tk.Scrollbar(
    outer_frame,
    orient="vertical",
    command=main_canvas.yview
)

main_canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
main_canvas.pack(side="left", fill="both", expand=True)

main_frame = tk.Frame(main_canvas, bg=colors["root"])

canvas_window = main_canvas.create_window(
    (0, 0),
    window=main_frame,
    anchor="nw"
)


def update_scroll_region(event=None):
    main_canvas.configure(scrollregion=main_canvas.bbox("all"))


def resize_content(event):
    main_canvas.itemconfigure(canvas_window, width=event.width)


main_frame.bind("<Configure>", update_scroll_region)
main_canvas.bind("<Configure>", resize_content)


def mouse_scroll(event):
    main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


root.bind_all("<MouseWheel>", mouse_scroll)


# =====================================================
# THEME REGISTRATION
# =====================================================

theme_widgets = []


def register(widget, role):
    theme_widgets.append((widget, role))
    return widget


# =====================================================
# PASSWORD REQUIREMENTS
# =====================================================

checklist_text = {
    "length8": "At least 8 characters",
    "length12": "At least 12 characters",
    "lowercase": "One lowercase letter",
    "uppercase": "One uppercase letter",
    "number": "One number",
    "special": "One special character"
}

criteria = {key: False for key in checklist_text}
check_labels = {}


# =====================================================
# COMMON PASSWORDS
# =====================================================

common_passwords = [
    "password",
    "password123",
    "12345678",
    "123456789",
    "qwerty123",
    "admin123",
    "iloveyou",
    "welcome123"
]


# =====================================================
# CRACK TIME ESTIMATION
# =====================================================

def estimate_crack_time(password):

    if not password:
        return "Not available"

    charset = 0

    if re.search(r"[a-z]", password):
        charset += 26

    if re.search(r"[A-Z]", password):
        charset += 26

    if re.search(r"[0-9]", password):
        charset += 10

    if re.search(r"[^a-zA-Z0-9]", password):
        charset += 32

    if charset == 0:
        return "Not available"

    combinations = charset ** len(password)
    guesses_per_second = 1_000_000_000
    seconds = combinations / (2 * guesses_per_second)

    if seconds < 1:
        return "Less than a second"
    elif seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        return f"{int(seconds / 60)} minutes"
    elif seconds < 86400:
        return f"{int(seconds / 3600)} hours"
    elif seconds < 31536000:
        return f"{int(seconds / 86400)} days"

    years = seconds / 31536000

    if years < 1000:
        return f"{int(years)} years"
    elif years < 1_000_000:
        return f"{int(years / 1000)} thousand years"
    elif years < 1_000_000_000:
        return f"{int(years / 1_000_000)} million years"

    return "Billions of years or more"


# =====================================================
# UPDATE CHECKLIST
# =====================================================

def update_checklist():

    for key, label in check_labels.items():

        if criteria[key]:
            label.configure(
                text="✓  " + checklist_text[key],
                fg=colors["success"]
            )
        else:
            label.configure(
                text="○  " + checklist_text[key],
                fg=colors["muted"]
            )


# =====================================================
# PROGRESS BAR
# =====================================================

current_score = 0


def update_score_bar(value=None):

    global current_score

    if value is not None:
        current_score = value

    strength_canvas.delete("all")

    width = strength_canvas.winfo_width()

    if width <= 1:
        width = 500

    height = 12

    strength_canvas.create_rectangle(
        0, 0, width, height,
        fill=colors["progress_bg"],
        outline=""
    )

    if current_score > 0:

        if current_score <= 33:
            bar_color = colors["danger"]
        elif current_score <= 66:
            bar_color = colors["warning"]
        else:
            bar_color = colors["success"]

        strength_canvas.create_rectangle(
            0, 0,
            width * current_score / 100,
            height,
            fill=bar_color,
            outline=""
        )


# =====================================================
# SECURITY TIPS
# =====================================================

def update_tips(password):

    tips = []

    if len(password) < 12:
        tips.append("Use at least 12 characters.")

    if not re.search(r"[A-Z]", password):
        tips.append("Add an uppercase letter.")

    if not re.search(r"[a-z]", password):
        tips.append("Add a lowercase letter.")

    if not re.search(r"[0-9]", password):
        tips.append("Include a number.")

    if not re.search(r"[^a-zA-Z0-9]", password):
        tips.append("Include a special character.")

    if password.lower() in common_passwords:
        tips.append("Avoid commonly used passwords.")

    if not tips:
        tips.append("Great! Your password meets all six checks.")

    tip_label.configure(
        text="\n".join("• " + tip for tip in tips[:5])
    )


# =====================================================
# PASSWORD ANALYSIS
# =====================================================

strength_status = "empty"


def analyze_password(event=None):

    global strength_status

    password = password_entry.get()

    criteria["length8"] = len(password) >= 8
    criteria["length12"] = len(password) >= 12
    criteria["lowercase"] = bool(re.search(r"[a-z]", password))
    criteria["uppercase"] = bool(re.search(r"[A-Z]", password))
    criteria["number"] = bool(re.search(r"[0-9]", password))
    criteria["special"] = bool(re.search(r"[^a-zA-Z0-9]", password))

    update_checklist()

    if not password:

        strength_status = "empty"

        strength_label.configure(
            text="Enter a password",
            bg=colors["card"],
            fg=colors["muted"]
        )

        score_label.configure(text="0%")
        crack_label.configure(text="Not available")
        tip_label.configure(
            text="Enter a password to receive security tips."
        )

        update_score_bar(0)
        return

    score = sum(criteria.values())
    percentage = int((score / 6) * 100)

    if password.lower() in common_passwords:
        strength = "WEAK"
        strength_status = "weak"
        percentage = min(percentage, 25)

    elif percentage <= 33:
        strength = "WEAK"
        strength_status = "weak"

    elif percentage <= 66:
        strength = "MEDIUM"
        strength_status = "medium"

    else:
        strength = "STRONG"
        strength_status = "strong"

    strength_colors = {
        "weak": colors["danger"],
        "medium": colors["warning"],
        "strong": colors["success"]
    }

    strength_label.configure(
        text=f"Password Strength: {strength}",
        bg=colors["card"],
        fg=strength_colors[strength_status]
    )

    score_label.configure(text=f"{percentage}%")

    crack_label.configure(
        text=estimate_crack_time(password)
    )

    update_score_bar(percentage)
    update_tips(password)


# =====================================================
# PASSWORD GENERATOR
# =====================================================

def generate_password():

    characters = (
        string.ascii_letters
        + string.digits
        + "!@#$%^&*()-_=+"
    )

    password = "".join(
        secrets.choice(characters)
        for _ in range(16)
    )

    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

    analyze_password()


# =====================================================
# COPY PASSWORD
# =====================================================

def copy_password():

    password = password_entry.get()

    if password:

        root.clipboard_clear()
        root.clipboard_append(password)
        root.update()

        copy_button.configure(text="Copied!")

        root.after(
            1500,
            lambda: copy_button.configure(text="Copy")
        )


# =====================================================
# CLEAR PASSWORD
# =====================================================

def clear_password():

    password_entry.delete(0, tk.END)

    for key in criteria:
        criteria[key] = False

    analyze_password()


# =====================================================
# SHOW / HIDE PASSWORD
# =====================================================

password_visible = False


def toggle_password_visibility():

    global password_visible

    password_visible = not password_visible

    if password_visible:
        password_entry.configure(show="")
        show_button.configure(text="Hide")
    else:
        password_entry.configure(show="*")
        show_button.configure(text="Show")


# =====================================================
# APPLY THEME - FIXED
# =====================================================

def apply_theme():

    global colors

    colors = themes[current_theme]

    root.configure(bg=colors["root"])
    outer_frame.configure(bg=colors["root"])
    main_canvas.configure(bg=colors["root"])
    main_frame.configure(bg=colors["root"])

    scrollbar.configure(
        bg=colors["card"],
        troughcolor=colors["root"],
        activebackground=colors["accent"]
    )

    for widget, role in theme_widgets:

        try:

            if role == "root":
                widget.configure(bg=colors["root"])

            elif role == "card":
                widget.configure(
                    bg=colors["card"],
                    highlightbackground=colors["border"]
                )

            elif role == "text":
                widget.configure(
                    bg=colors["card"],
                    fg=colors["text"]
                )

            elif role == "muted":
                widget.configure(
                    bg=colors["card"],
                    fg=colors["muted"]
                )

            elif role == "header":
                widget.configure(
                    bg=colors["root"],
                    fg=colors["text"]
                )

            elif role == "header_muted":
                widget.configure(
                    bg=colors["root"],
                    fg=colors["muted"]
                )

            elif role == "input":
                widget.configure(
                    bg=colors["input"],
                    fg=colors["text"],
                    insertbackground=colors["text"],
                    highlightbackground=colors["border"]
                )

            elif role == "button":
                widget.configure(
                    bg=colors["accent"],
                    fg=colors["button_text"],
                    activebackground=colors["accent_hover"],
                    activeforeground=colors["button_text"]
                )

            elif role == "secondary_button":
                widget.configure(
                    bg=colors["input"],
                    fg=colors["text"],
                    activebackground=colors["border"],
                    activeforeground=colors["text"]
                )

            elif role == "checklist":
                widget.configure(bg=colors["check_bg"])

            elif role == "check_item":
                widget.configure(bg=colors["check_bg"])

            elif role == "tip":
                widget.configure(bg=colors["tip_bg"])

            elif role == "tip_text":
                widget.configure(
                    bg=colors["tip_bg"],
                    fg=colors["text"]
                )

            elif role == "crack":
                widget.configure(bg=colors["crack_bg"])

            elif role == "crack_text":
                widget.configure(
                    bg=colors["crack_bg"],
                    fg=colors["text"]
                )

            elif role == "crack_value":
                widget.configure(
                    bg=colors["crack_bg"],
                    fg=colors["success"]
                )

            elif role == "strength":
                status_colors = {
                    "empty": colors["muted"],
                    "weak": colors["danger"],
                    "medium": colors["warning"],
                    "strong": colors["success"]
                }

                widget.configure(
                    bg=colors["card"],
                    fg=status_colors[strength_status]
                )

        except tk.TclError:
            pass

    theme_button.configure(
        text="☀ Light Mode" if current_theme == "dark" else "☾ Dark Mode",
        bg=colors["input"],
        fg=colors["text"],
        activebackground=colors["border"],
        activeforeground=colors["text"]
    )

    strength_canvas.configure(bg=colors["card"])

    update_checklist()
    update_score_bar()


def toggle_theme():

    global current_theme

    current_theme = (
        "light" if current_theme == "dark" else "dark"
    )

    apply_theme()


# =====================================================
# HEADER
# =====================================================

header_frame = register(
    tk.Frame(main_frame, bg=colors["root"]),
    "root"
)

header_frame.pack(
    fill="x",
    padx=35,
    pady=(25, 20)
)

header_left = register(
    tk.Frame(header_frame, bg=colors["root"]),
    "root"
)

header_left.pack(side="left")

title_label = register(
    tk.Label(
        header_left,
        text="Password Lab",
        font=("Segoe UI", 27, "bold"),
        bg=colors["root"],
        fg=colors["text"]
    ),
    "header"
)

title_label.pack(anchor="w")

subtitle_label = register(
    tk.Label(
        header_left,
        text="Check how secure your password really is.",
        font=("Segoe UI", 10),
        bg=colors["root"],
        fg=colors["muted"]
    ),
    "header_muted"
)

subtitle_label.pack(anchor="w", pady=(5, 0))


theme_button = tk.Button(
    header_frame,
    text="☀ Light Mode",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    bd=0,
    padx=15,
    pady=10,
    cursor="hand2",
    command=toggle_theme
)

theme_button.pack(side="right", anchor="n")


# =====================================================
# PASSWORD INPUT CARD
# =====================================================

input_card = register(
    tk.Frame(
        main_frame,
        bg=colors["card"],
        highlightthickness=1,
        highlightbackground=colors["border"]
    ),
    "card"
)

input_card.pack(fill="x", padx=35, pady=(0, 15))

input_inner = register(
    tk.Frame(input_card, bg=colors["card"]),
    "card"
)

input_inner.pack(fill="x", padx=22, pady=20)

input_title = register(
    tk.Label(
        input_inner,
        text="Enter Your Password",
        font=("Segoe UI", 12, "bold"),
        bg=colors["card"],
        fg=colors["text"]
    ),
    "text"
)

input_title.pack(anchor="w", pady=(0, 12))


entry_frame = register(
    tk.Frame(input_inner, bg=colors["card"]),
    "card"
)

entry_frame.pack(fill="x")

password_entry = register(
    tk.Entry(
        entry_frame,
        font=("Segoe UI", 13),
        show="*",
        relief="flat",
        bd=0,
        bg=colors["input"],
        fg=colors["text"],
        insertbackground=colors["text"],
        highlightthickness=1,
        highlightbackground=colors["border"]
    ),
    "input"
)

password_entry.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=13,
    padx=(0, 10)
)

password_entry.bind("<KeyRelease>", analyze_password)


show_button = register(
    tk.Button(
        entry_frame,
        text="Show",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        bd=0,
        padx=18,
        pady=12,
        cursor="hand2",
        command=toggle_password_visibility
    ),
    "secondary_button"
)

show_button.pack(side="right")


# =====================================================
# ACTION BUTTONS
# =====================================================

button_frame = register(
    tk.Frame(input_inner, bg=colors["card"]),
    "card"
)

button_frame.pack(fill="x", pady=(15, 0))


generate_button = register(
    tk.Button(
        button_frame,
        text="Generate Password",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        bd=0,
        padx=16,
        pady=11,
        cursor="hand2",
        command=generate_password
    ),
    "button"
)

generate_button.pack(side="left", padx=(0, 10))


copy_button = register(
    tk.Button(
        button_frame,
        text="Copy",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        bd=0,
        padx=20,
        pady=11,
        cursor="hand2",
        command=copy_password
    ),
    "secondary_button"
)

copy_button.pack(side="left", padx=(0, 10))


clear_button = register(
    tk.Button(
        button_frame,
        text="Clear",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        bd=0,
        padx=20,
        pady=11,
        cursor="hand2",
        command=clear_password
    ),
    "secondary_button"
)

clear_button.pack(side="left")


# =====================================================
# PASSWORD ANALYSIS CARD
# =====================================================

result_card = register(
    tk.Frame(
        main_frame,
        bg=colors["card"],
        highlightthickness=1,
        highlightbackground=colors["border"]
    ),
    "card"
)

result_card.pack(fill="x", padx=35, pady=(0, 15))

result_inner = register(
    tk.Frame(result_card, bg=colors["card"]),
    "card"
)

result_inner.pack(fill="x", padx=22, pady=20)


result_title = register(
    tk.Label(
        result_inner,
        text="Password Analysis",
        font=("Segoe UI", 12, "bold"),
        bg=colors["card"],
        fg=colors["text"]
    ),
    "text"
)

result_title.pack(anchor="w", pady=(0, 12))


strength_label = register(
    tk.Label(
        result_inner,
        text="Enter a password",
        font=("Segoe UI", 14, "bold"),
        bg=colors["card"],
        fg=colors["muted"]
    ),
    "strength"
)

strength_label.pack(anchor="w")


score_frame = register(
    tk.Frame(result_inner, bg=colors["card"]),
    "card"
)

score_frame.pack(fill="x", pady=(15, 5))


score_text = register(
    tk.Label(
        score_frame,
        text="Security Score",
        font=("Segoe UI", 10),
        bg=colors["card"],
        fg=colors["muted"]
    ),
    "muted"
)

score_text.pack(side="left")


score_label = register(
    tk.Label(
        score_frame,
        text="0%",
        font=("Segoe UI", 11, "bold"),
        bg=colors["card"],
        fg=colors["text"]
    ),
    "text"
)

score_label.pack(side="right")


strength_canvas = tk.Canvas(
    result_inner,
    height=12,
    bg=colors["card"],
    highlightthickness=0
)

strength_canvas.pack(fill="x", pady=(5, 15))

strength_canvas.bind(
    "<Configure>",
    lambda event: update_score_bar()
)


# =====================================================
# CRACK TIME
# =====================================================

crack_frame = register(
    tk.Frame(result_inner, bg=colors["crack_bg"]),
    "crack"
)

crack_frame.pack(fill="x", pady=(5, 0))

crack_inner = register(
    tk.Frame(crack_frame, bg=colors["crack_bg"]),
    "crack"
)

crack_inner.pack(fill="x", padx=15, pady=14)


crack_title = register(
    tk.Label(
        crack_inner,
        text="Estimated time to crack",
        font=("Segoe UI", 10),
        bg=colors["crack_bg"],
        fg=colors["text"]
    ),
    "crack_text"
)

crack_title.pack(side="left")


crack_label = register(
    tk.Label(
        crack_inner,
        text="Not available",
        font=("Segoe UI", 10, "bold"),
        bg=colors["crack_bg"],
        fg=colors["success"]
    ),
    "crack_value"
)

crack_label.pack(side="right")


# =====================================================
# PASSWORD REQUIREMENTS
# =====================================================

check_card = register(
    tk.Frame(
        main_frame,
        bg=colors["card"],
        highlightthickness=1,
        highlightbackground=colors["border"]
    ),
    "card"
)

check_card.pack(fill="x", padx=35, pady=(0, 15))

check_inner = register(
    tk.Frame(check_card, bg=colors["card"]),
    "card"
)

check_inner.pack(fill="x", padx=22, pady=20)


check_title = register(
    tk.Label(
        check_inner,
        text="Password Requirements",
        font=("Segoe UI", 12, "bold"),
        bg=colors["card"],
        fg=colors["text"]
    ),
    "text"
)

check_title.pack(anchor="w", pady=(0, 12))


checklist_frame = register(
    tk.Frame(check_inner, bg=colors["check_bg"]),
    "checklist"
)

checklist_frame.pack(fill="x")


for key, description in checklist_text.items():

    label = register(
        tk.Label(
            checklist_frame,
            text="○  " + description,
            font=("Segoe UI", 10),
            bg=colors["check_bg"],
            fg=colors["muted"],
            anchor="w"
        ),
        "check_item"
    )

    label.pack(fill="x", padx=15, pady=7)

    check_labels[key] = label


# =====================================================
# SMART SECURITY TIPS
# =====================================================

tips_card = register(
    tk.Frame(
        main_frame,
        bg=colors["card"],
        highlightthickness=1,
        highlightbackground=colors["border"]
    ),
    "card"
)

tips_card.pack(fill="x", padx=35, pady=(0, 15))

tips_inner = register(
    tk.Frame(tips_card, bg=colors["card"]),
    "card"
)

tips_inner.pack(fill="x", padx=22, pady=20)


tips_title = register(
    tk.Label(
        tips_inner,
        text="Smart Security Tips",
        font=("Segoe UI", 12, "bold"),
        bg=colors["card"],
        fg=colors["text"]
    ),
    "text"
)

tips_title.pack(anchor="w", pady=(0, 12))


tip_box = register(
    tk.Frame(tips_inner, bg=colors["tip_bg"]),
    "tip"
)

tip_box.pack(fill="x")


tip_label = register(
    tk.Label(
        tip_box,
        text="Enter a password to receive security tips.",
        font=("Segoe UI", 10),
        bg=colors["tip_bg"],
        fg=colors["text"],
        justify="left",
        anchor="w",
        wraplength=700
    ),
    "tip_text"
)

tip_label.pack(fill="x", padx=15, pady=15)


# =====================================================
# FOOTER
# =====================================================

footer_label = register(
    tk.Label(
        main_frame,
        text="Password Lab  |  Stay Safe. Stay Secure.",
        font=("Segoe UI", 9),
        bg=colors["root"],
        fg=colors["muted"]
    ),
    "header_muted"
)

footer_label.pack(pady=(5, 25))


# =====================================================
# RUN APPLICATION
# =====================================================

apply_theme()

root.after(100, update_scroll_region)

root.mainloop()