import tkinter as tk, sys
from tkinter import messagebox

if sys.platform == "win32":
    try:
        import ctypes
        cw = ctypes.windll.kernel32.GetConsoleWindow()
        if cw: ctypes.windll.user32.ShowWindow(cw, 0)
    except: pass

def mult(x): return 1.0 if x <= 0 else max(.5, min(1.0, 4/9 + 500/(9*x)))
def maxsize(m): return max(0, 2000 - m*100)
def fmt(n): return f"{round(n):,}"

def calc():
    try:
        a, b = float(e1.get()), float(e2.get())
        if a < 0 or b < 0: raise ValueError
        mt = em.get().strip()
        mb = float(mt) if mt else 0.0
        if mb < 0: raise ValueError
        lo, hi = min(a, b), max(a, b)
        m = mult(lo)
        comb = hi + lo*m
        ma = mb + 1
        cap = maxsize(ma)
        fin = min(comb, cap)
        rl.config(text=fmt(fin))
        note = "  (capped)" if comb > cap else ""
        pl.config(text=f"{m*100:.1f}% of smaller turret added  •  Merge #{fmt(ma)}  •  Max {fmt(cap)}{note}")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers (0 or higher) in both turret boxes, and 0 or higher in the merge box if used.")

def clr():
    for w in (e1, e2, em): w.delete(0, tk.END)
    rl.config(text="—"); pl.config(text="—"); e1.focus()

THEMES = {
    "Dark":  dict(bg="#202020", slot="#555555", sb="#777777", inp="#333333", btn="#444444", bh="#555555", txt="#FFFFFF", mut="#AAAAAA", ac="#66CC66"),
    "Light": dict(bg="#E8E8E8", slot="#D0D0D0", sb="#A0A0A0", inp="#FFFFFF", btn="#C8C8C8", bh="#B5B5B5", txt="#202020", mut="#555555", ac="#198754"),
    "Blue":  dict(bg="#101A2A", slot="#24466F", sb="#3971A8", inp="#18304F", btn="#285B91", bh="#3473B4", txt="#FFFFFF", mut="#B7C9DF", ac="#62B0FF"),
}
theme = "Dark"

def apply(name):
    global theme; theme = name; c = THEMES[name]
    root.configure(bg=c["bg"]); cv.configure(bg=c["bg"])
    for w in (t1, rt, l1, l2): w.configure(bg=c["bg"], fg=c["txt"])
    pl.configure(bg=c["bg"], fg=c["ac"])
    infol.configure(bg=c["bg"], fg=c["mut"])
    ml.configure(bg=c["bg"], fg=c["mut"])
    plusl.configure(bg=c["bg"], fg=c["txt"])
    for w in (e1, e2, em): w.configure(bg=c["inp"], fg=c["txt"], insertbackground=c["txt"])
    rl.configure(bg=c["slot"], fg=c["txt"])
    for w in (calcb, clrb): w.configure(bg=c["btn"], fg=c["txt"], activebackground=c["bh"], activeforeground=c["txt"])
    tm.configure(bg=c["btn"], fg=c["txt"], activebackground=c["bh"], activeforeground=c["txt"], highlightbackground=c["btn"])
    draw()

def draw():
    c = THEMES[theme]; cv.delete("s")
    for x, y, w, h in ((145,145,150,78), (465,145,150,78), (340,225,80,46), (285,295,190,78)):
        cv.create_rectangle(x, y, x+w, y+h, fill=c["bg"], outline=c["bg"], tags="s")
        cv.create_rectangle(x+2, y+2, x+w-2, y+h-2, fill=c["slot"], outline=c["sb"], width=2, tags="s")

root = tk.Tk()
root.title("Turret Size Calculator")
root.geometry("760x560")
root.resizable(False, False)

cv = tk.Canvas(root, width=760, height=560, highlightthickness=0)
cv.pack(fill="both", expand=True)

t1 = tk.Label(root, text="TURRET SIZE CALCULATOR", font=("Arial", 20, "bold")); t1.place(x=0, y=18, width=760, height=35)

tv = tk.StringVar(value="Dark")
tm = tk.OptionMenu(root, tv, *THEMES.keys(), command=apply)
tm.config(font=("Arial", 10, "bold"), width=8, relief="flat", bd=0)
tm.place(x=620, y=15, width=110, height=32)

e1 = tk.Entry(root, justify="center", relief="flat", bd=0, font=("Arial", 18, "bold")); e1.place(x=175, y=181, width=90, height=32)
e2 = tk.Entry(root, justify="center", relief="flat", bd=0, font=("Arial", 18, "bold")); e2.place(x=495, y=181, width=90, height=32)

l1 = tk.Label(root, text="TURRET A", font=("Arial", 10, "bold")); l1.place(x=145, y=155, width=150, height=22)
l2 = tk.Label(root, text="TURRET B", font=("Arial", 10, "bold")); l2.place(x=465, y=155, width=150, height=22)

plusl = tk.Label(root, text="+", font=("Arial", 18, "bold")); plusl.place(x=360, y=176, width=40, height=30)

ml = tk.Label(root, text="MERGES (OPTIONAL)", font=("Arial", 8, "bold")); ml.place(x=310, y=213, width=140, height=14)
em = tk.Entry(root, justify="center", relief="flat", bd=0, font=("Arial", 12, "bold")); em.place(x=350, y=232, width=60, height=28)

rt = tk.Label(root, text="COMBINED SIZE", font=("Arial", 13, "bold")); rt.place(x=0, y=276, width=760, height=25)
rl = tk.Label(root, text="—", font=("Arial", 25, "bold")); rl.place(x=305, y=312, width=150, height=45)

calcb = tk.Button(root, text="CALCULATE", command=calc, relief="raised", bd=3, font=("Arial", 13, "bold"), cursor="hand2")
calcb.place(x=285, y=395, width=190, height=48)
clrb = tk.Button(root, text="CLEAR", command=clr, relief="raised", bd=3, font=("Arial", 10, "bold"), cursor="hand2")
clrb.place(x=325, y=450, width=110, height=35)

pl = tk.Label(root, text="—", font=("Arial", 10, "bold")); pl.place(x=0, y=496, width=760, height=22)

infol = tk.Label(root, text="Smaller value auto-becomes the efficiency turret (4/9 + 500/9x, 50-100%).\nEach merge lowers the max cap by 100, starting at 2000.", font=("Arial", 9), justify="center")
infol.place(x=0, y=524, width=760, height=32)

apply("Dark")
e1.focus()
root.bind("<Return>", lambda e: calc())
root.bind("<Escape>", lambda e: clr())
root.mainloop()
