import tkinter as tk
from tkinter import messagebox

import sys
if sys.platform == "win32":
    try:
        import ctypes
        console_window = ctypes.windll.kernel32.GetConsoleWindow()
        if console_window:
            ctypes.windll.user32.ShowWindow(console_window, 0)
    except Exception:
        pass


def get_multiplier(second_turret):
    if second_turret <= 0:
        return 1.0
    multiplier = (4 / 9) + (500 / (9 * second_turret))
    return max(0.5, min(1.0, multiplier))


def get_max_size(merge_count):
    return max(0, 2000 - (merge_count * 100))


def format_number(number):
    return f"{round(number):,}"


def calculate():
    try:
        first = float(first_entry.get())
        second = float(second_entry.get())

        if first < 0 or second < 0:
            raise ValueError

        merge_text = merge_entry.get().strip()
        merges_before = float(merge_text) if merge_text else 0.0

        if merges_before < 0:
            raise ValueError

        larger = max(first, second)
        smaller = min(first, second)

        multiplier = get_multiplier(smaller)
        combined = larger + (smaller * multiplier)

        merges_after = merges_before + 1
        max_size = get_max_size(merges_after)

        final_size = min(combined, max_size)

        result_label.config(text=format_number(final_size))

        capped_note = "  (capped)" if combined > max_size else ""
        percent_label.config(
            text=(
                f"{multiplier * 100:.1f}% of smaller turret added  •  "
                f"Merge #{format_number(merges_after)}  •  "
                f"Max {format_number(max_size)}{capped_note}"
            )
        )

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter valid numbers (0 or higher) in both turret boxes, "
            "and 0 or higher in the merge box if used."
        )


def clear():
    first_entry.delete(0, tk.END)
    second_entry.delete(0, tk.END)
    merge_entry.delete(0, tk.END)
    result_label.config(text="—")
    percent_label.config(text="—")
    first_entry.focus()


THEMES = {
    "Dark": {
        "bg": "#202020",
        "panel": "#292929",
        "slot": "#555555",
        "slot_border": "#777777",
        "input": "#333333",
        "button": "#444444",
        "button_hover": "#555555",
        "text": "#FFFFFF",
        "muted": "#AAAAAA",
        "accent": "#66CC66",
    },
    "Light": {
        "bg": "#E8E8E8",
        "panel": "#F5F5F5",
        "slot": "#D0D0D0",
        "slot_border": "#A0A0A0",
        "input": "#FFFFFF",
        "button": "#C8C8C8",
        "button_hover": "#B5B5B5",
        "text": "#202020",
        "muted": "#555555",
        "accent": "#198754",
    },
    "Blue": {
        "bg": "#101A2A",
        "panel": "#16243A",
        "slot": "#24466F",
        "slot_border": "#3971A8",
        "input": "#18304F",
        "button": "#285B91",
        "button_hover": "#3473B4",
        "text": "#FFFFFF",
        "muted": "#B7C9DF",
        "accent": "#62B0FF",
    },
}

current_theme = "Dark"


def apply_theme(name):
    global current_theme
    current_theme = name
    colors = THEMES[name]

    root.configure(bg=colors["bg"])
    canvas.configure(bg=colors["bg"])

    title_label.configure(bg=colors["bg"], fg=colors["text"])
    result_title.configure(bg=colors["bg"], fg=colors["text"])
    percent_label.configure(bg=colors["bg"], fg=colors["accent"])
    info_label.configure(bg=colors["bg"], fg=colors["muted"])
    merge_label.configure(bg=colors["bg"], fg=colors["muted"])
    first_label.configure(bg=colors["bg"], fg=colors["muted"])
    second_label.configure(bg=colors["bg"], fg=colors["muted"])
    plus_label.configure(bg=colors["bg"], fg=colors["text"])

    first_entry.configure(
        bg=colors["input"],
        fg=colors["text"],
        insertbackground=colors["text"]
    )
    second_entry.configure(
        bg=colors["input"],
        fg=colors["text"],
        insertbackground=colors["text"]
    )
    merge_entry.configure(
        bg=colors["input"],
        fg=colors["text"],
        insertbackground=colors["text"]
    )

    result_label.configure(
        bg=colors["slot"],
        fg=colors["text"]
    )

    calculate_button.configure(
        bg=colors["button"],
        fg=colors["text"],
        activebackground=colors["button_hover"],
        activeforeground=colors["text"]
    )
    clear_button.configure(
        bg=colors["button"],
        fg=colors["text"],
        activebackground=colors["button_hover"],
        activeforeground=colors["text"]
    )

    theme_menu.configure(
        bg=colors["button"],
        fg=colors["text"],
        activebackground=colors["button_hover"],
        activeforeground=colors["text"],
        highlightbackground=colors["button"]
    )

    redraw_slots()


def redraw_slots():
    colors = THEMES[current_theme]

    canvas.delete("slot")

    draw_slot(145, 145, 150, 78, tag="slot", color=colors["slot"])
    draw_slot(465, 145, 150, 78, tag="slot", color=colors["slot"])
    draw_slot(340, 225, 80, 46, tag="slot", color=colors["slot"])
    draw_slot(285, 295, 190, 78, tag="slot", color=colors["slot"])


def draw_slot(x, y, width, height, tag="slot", color=None):
    colors = THEMES[current_theme]

    if color is None:
        color = colors["slot"]

    canvas.create_rectangle(
        x, y, x + width, y + height,
        fill=colors["bg"],
        outline=colors["bg"],
        tags=tag
    )
    canvas.create_rectangle(
        x + 2, y + 2,
        x + width - 2, y + height - 2,
        fill=color,
        outline=colors["slot_border"],
        width=2,
        tags=tag
    )


root = tk.Tk()
root.title("Turret Size Calculator")
root.geometry("760x560")
root.resizable(False, False)

canvas = tk.Canvas(
    root,
    width=760,
    height=560,
    highlightthickness=0
)
canvas.pack(fill="both", expand=True)

title_label = tk.Label(
    root,
    text="TURRET SIZE CALCULATOR",
    font=("Arial", 20, "bold")
)
title_label.place(x=0, y=18, width=760, height=35)

theme_var = tk.StringVar(value="Dark")

theme_menu = tk.OptionMenu(
    root,
    theme_var,
    *THEMES.keys(),
    command=apply_theme
)
theme_menu.config(
    font=("Arial", 10, "bold"),
    width=8,
    relief="flat",
    bd=0
)
theme_menu.place(x=620, y=15, width=110, height=32)

first_entry = tk.Entry(
    root,
    justify="center",
    relief="flat",
    bd=0,
    font=("Arial", 18, "bold")
)
first_entry.place(x=175, y=181, width=90, height=32)

second_entry = tk.Entry(
    root,
    justify="center",
    relief="flat",
    bd=0,
    font=("Arial", 18, "bold")
)
second_entry.place(x=495, y=181, width=90, height=32)

first_label = tk.Label(
    root,
    text="TURRET A",
    font=("Arial", 10, "bold")
)
first_label.place(x=145, y=155, width=150, height=22)

second_label = tk.Label(
    root,
    text="TURRET B",
    font=("Arial", 10, "bold")
)
second_label.place(x=465, y=155, width=150, height=22)

plus_label = tk.Label(
    root,
    text="+",
    font=("Arial", 18, "bold")
)
plus_label.place(x=360, y=176, width=40, height=30)

merge_label = tk.Label(
    root,
    text="MERGES (OPTIONAL)",
    font=("Arial", 8, "bold")
)
merge_label.place(x=310, y=213, width=140, height=14)

merge_entry = tk.Entry(
    root,
    justify="center",
    relief="flat",
    bd=0,
    font=("Arial", 12, "bold")
)
merge_entry.place(x=350, y=232, width=60, height=28)

result_title = tk.Label(
    root,
    text="COMBINED SIZE",
    font=("Arial", 13, "bold")
)
result_title.place(x=0, y=276, width=760, height=25)

result_label = tk.Label(
    root,
    text="—",
    font=("Arial", 25, "bold")
)
result_label.place(x=305, y=312, width=150, height=45)

calculate_button = tk.Button(
    root,
    text="CALCULATE",
    command=calculate,
    relief="raised",
    bd=3,
    font=("Arial", 13, "bold"),
    cursor="hand2"
)
calculate_button.place(x=285, y=395, width=190, height=48)

clear_button = tk.Button(
    root,
    text="CLEAR",
    command=clear,
    relief="raised",
    bd=3,
    font=("Arial", 10, "bold"),
    cursor="hand2"
)
clear_button.place(x=325, y=450, width=110, height=35)

percent_label = tk.Label(
    root,
    text="—",
    font=("Arial", 10, "bold")
)
percent_label.place(x=0, y=496, width=760, height=22)

info_label = tk.Label(
    root,
    text=(
        "Smaller value auto-becomes the efficiency turret (4/9 + 500/9x, 50-100%).\n"
        "Each merge lowers the max cap by 100, starting at 2000."
    ),
    font=("Arial", 9),
    justify="center"
)
info_label.place(x=0, y=524, width=760, height=32)

apply_theme("Dark")

first_entry.focus()
root.bind("<Return>", lambda event: calculate())
root.bind("<Escape>", lambda event: clear())

root.mainloop()
