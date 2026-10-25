"""Sort Race: Sorting Algorithm Battle Arena (tkinter)

Run with:  python sort_race_tk.py

Bubble, Insertion, Merge and Quick sort race on the same data. Every lane
advances one operation (a comparison or a write) per tick, so the algorithm
that needs fewer operations finishes first.
"""
import math
import random
import re
import tkinter as tk
from tkinter import ttk


# ---------------------------------------------------------------- algorithms
# Each algorithm is a generator: it updates the lane's counters and highlighted
# bar indices (L.hl), then yields once per operation so the race can interleave.

def bubble(L):
    a = L.a
    n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            L.cmp += 1
            L.hl = [j, j + 1]
            yield
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                L.wr += 2
                yield
                swapped = True
        if not swapped:
            break


def insertion(L):
    a = L.a
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0:
            L.cmp += 1
            L.hl = [j, j + 1]
            yield
            if a[j] > key:
                a[j + 1] = a[j]
                L.wr += 1
                yield
                j -= 1
            else:
                break
        a[j + 1] = key
        L.wr += 1
        L.hl = [j + 1]
        yield


def merge_sort(L, lo=0, hi=None):
    a = L.a
    if hi is None:
        hi = len(a)
    if hi - lo < 2:
        return
    mid = (lo + hi) // 2
    yield from merge_sort(L, lo, mid)
    yield from merge_sort(L, mid, hi)
    left, right = a[lo:mid], a[mid:hi]
    i = j = 0
    k = lo
    while i < len(left) and j < len(right):
        L.cmp += 1
        L.hl = [lo + i, mid + j]
        yield
        if left[i] <= right[j]:
            a[k] = left[i]
            i += 1
        else:
            a[k] = right[j]
            j += 1
        L.wr += 1
        L.hl = [k]
        yield
        k += 1
    for v in left[i:] + right[j:]:
        a[k] = v
        L.wr += 1
        L.hl = [k]
        yield
        k += 1


def quick_sort(L, lo=0, hi=None):
    a = L.a
    if hi is None:
        hi = len(a) - 1
    if lo >= hi:
        return
    m = (lo + hi) // 2                      # middle pivot avoids the worst case
    a[m], a[hi] = a[hi], a[m]
    L.wr += 2
    pivot = a[hi]
    i = lo
    for j in range(lo, hi):
        L.cmp += 1
        L.hl = [j, hi]
        yield
        if a[j] < pivot:
            a[i], a[j] = a[j], a[i]
            L.wr += 2
            L.hl = [i, j]
            i += 1
            yield
    a[i], a[hi] = a[hi], a[i]
    L.wr += 2
    L.hl = [i, hi]
    yield
    yield from quick_sort(L, lo, i - 1)
    yield from quick_sort(L, i + 1, hi)


ALGOS = [
    ("Bubble sort", "O(n²)", "#E4572E", bubble),
    ("Insertion sort", "O(n²)", "#E8A317", insertion),
    ("Merge sort", "O(n log n)", "#5B6CF0", merge_sort),
    ("Quick sort", "O(n log n) average", "#14A098", quick_sort),
]
ORD = ["1st", "2nd", "3rd", "4th"]


class Lane:
    def __init__(self, name, complexity, colour, algo, data):
        self.name, self.complexity, self.colour, self.algo = name, complexity, colour, algo
        self.a = list(data)
        self.cmp = self.wr = self.steps = self.rank = 0
        self.hl = []
        self.done = False
        self.it = algo(self)


# ---------------------------------------------------------------------- data
KINDS = ["Random", "Nearly sorted", "Reversed", "Few unique values", "My own numbers"]
MINE = "My own numbers"


def make_data(kind, n, custom):
    if kind == MINE:
        return list(custom)
    if kind == "Few unique values":
        step = -(-n // 5)
        return [random.randint(1, 5) * step for _ in range(n)]
    a = list(range(1, n + 1))
    if kind == "Reversed":
        a.reverse()
    elif kind == "Nearly sorted":
        for _ in range(max(2, n // 10)):
            i, j = random.randrange(n), random.randrange(n)
            a[i], a[j] = a[j], a[i]
    else:
        random.shuffle(a)
    return a


def parse_numbers(text):
    """Return (numbers, error_message). Accepts commas, spaces or semicolons."""
    nums = []
    for p in re.split(r"[\s,;]+", text):
        if not p:
            continue
        try:
            v = float(p)
        except ValueError:
            return None, f'"{p}" is not a number.'
        if not math.isfinite(v):
            return None, f'"{p}" is not a finite number.'
        nums.append(int(v) if v.is_integer() else v)
    if len(nums) < 2:
        return None, "Enter at least 2 numbers."
    if len(nums) > 100:
        return None, f"Use at most 100 numbers. You entered {len(nums)}."
    return nums, None


# ------------------------------------------------------------------- drawing
BG = "#ffffff"
FG = "#111827"
MUTED = "#6b7280"
BORDER = "#d1d5db"
HOT = "#1f2937"
HOT_OUTLINE = "#e5e7eb"
FONT = ("Segoe UI", 10)
FONT_B = ("Segoe UI", 10, "bold")
FONT_H = ("Segoe UI", 13, "bold")
FONT_S = ("Segoe UI", 8, "bold")


def draw_lane(c, L, mn, mx):
    """Redraw one lane on its canvas."""
    c.delete("all")
    w = max(c.winfo_width(), 200)
    h = max(c.winfo_height(), 150)
    pad = 12
    top, bottom = 44, h - 30

    # card border and coloured top edge
    c.create_rectangle(1, 1, w - 2, h - 2, outline=BORDER, fill=BG)
    c.create_rectangle(1, 1, w - 2, 6, outline=L.colour, fill=L.colour)

    # header
    c.create_text(pad, 24, text=L.name, anchor="w", font=FONT_H, fill=FG)
    nx = pad + 10 + len(L.name) * 9
    c.create_text(nx, 25, text=L.complexity, anchor="w", font=FONT, fill=MUTED)
    if L.done:
        c.create_oval(w - pad - 50, 12, w - pad, 36, outline=L.colour, width=2)
        c.create_text(w - pad - 25, 24, text=ORD[L.rank - 1], font=FONT_B, fill=FG)

    # bars
    n = len(L.a)
    labels = n <= 25
    plot_top = top + (14 if labels else 0)
    span = mx - mn
    avail = bottom - plot_top
    bw = (w - 2 * pad) / n
    hot = set() if L.done else set(L.hl)
    for i, v in enumerate(L.a):
        t = (v - mn) / span if span else 0.6
        bh = 3 + t * (avail - 3)
        x0 = pad + i * bw
        x1 = x0 + max(bw - 1, 1)
        y0 = bottom - bh
        if i in hot:
            c.create_rectangle(x0, y0, x1, bottom, fill=HOT, outline=HOT_OUTLINE)
        else:
            c.create_rectangle(x0, y0, x1, bottom, fill=L.colour, outline="")
        if labels:
            c.create_text((x0 + x1) / 2, y0 - 2, text=f"{v:g}", anchor="s", font=FONT_S, fill=FG)

    # stats
    c.create_text(pad, h - 14, anchor="w", font=FONT, fill=FG,
                  text=f"Comparisons {L.cmp}     Writes {L.wr}     Steps {L.steps}")


# ------------------------------------------------------------------------ UI
class App:
    def __init__(self, root):
        self.root = root
        root.title("Sort Race")
        root.geometry("1150x720")
        root.minsize(900, 600)

        self.data = []
        self.lanes = []
        self.canvases = []
        self.after_id = None
        self.running = False
        self.mn = self.mx = 0

        self.kind = tk.StringVar(value=KINDS[0])
        self.size = tk.IntVar(value=30)
        self.speed = tk.IntVar(value=26)
        self.text = tk.StringVar(value="38, 12, 77, 5, 91, 24, 60, 3, 49, 15")
        self.error = tk.StringVar()
        self.verdict = tk.StringVar()

        self.build_ui()
        self.new_data()

    # -- layout
    def build_ui(self):
        side = ttk.Frame(self.root, padding=12)
        side.pack(side="left", fill="y")

        ttk.Label(side, text="Sort race", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(
            side, wraplength=220, justify="left",
            text="Four algorithms sort the same numbers. Each lane runs one operation "
                 "per tick, so the algorithm that needs fewer comparisons and writes "
                 "crosses the line first.",
        ).pack(anchor="w", pady=(2, 14))

        ttk.Label(side, text="Data").pack(anchor="w")
        box = ttk.Combobox(side, textvariable=self.kind, values=KINDS, state="readonly")
        box.pack(fill="x", pady=(0, 10))
        box.bind("<<ComboboxSelected>>", lambda e: self.on_kind_change())

        self.size_label = ttk.Label(side, text="Size: 30")
        self.size_label.pack(anchor="w")
        self.size_scale = ttk.Scale(side, from_=10, to=100, orient="horizontal",
                                    command=self.on_size_drag)
        self.size_scale.set(30)
        self.size_scale.pack(fill="x", pady=(0, 10))
        self.size_scale.bind("<ButtonRelease-1>", lambda e: self.new_data())

        self.custom_label = ttk.Label(side, text="Your numbers (2 to 100)")
        self.custom_entry = ttk.Entry(side, textvariable=self.text)
        self.custom_entry.bind("<Return>", lambda e: self.new_data())
        self.err_label = ttk.Label(side, textvariable=self.error, foreground="#b91c1c",
                                   wraplength=220, justify="left")

        self.speed_label = ttk.Label(side, text="Speed: 26")
        self.speed_label.pack(anchor="w")
        self.speed_scale = ttk.Scale(side, from_=1, to=40, orient="horizontal",
                                     command=self.on_speed_drag)
        self.speed_scale.set(26)
        self.speed_scale.pack(fill="x", pady=(0, 14))

        self.new_btn = ttk.Button(side, text="New data", command=lambda: self.new_data(reshuffle=True))
        self.new_btn.pack(fill="x", pady=(0, 6))
        self.start_btn = ttk.Button(side, text="Start race", command=self.start)
        self.start_btn.pack(fill="x")

        ttk.Label(side, textvariable=self.verdict, wraplength=220, justify="left",
                  font=FONT_B).pack(anchor="w", pady=(16, 0))

        ttk.Label(side, wraplength=220, justify="left", foreground=MUTED,
                  text="A step is one comparison or one write. Dark bars are the "
                       "values being touched right now.").pack(side="bottom", anchor="w")

        self.side = side

        arena = ttk.Frame(self.root, padding=(0, 12, 12, 12))
        arena.pack(side="left", fill="both", expand=True)
        for r in range(2):
            arena.rowconfigure(r, weight=1, uniform="r")
            arena.columnconfigure(r, weight=1, uniform="c")
        for i in range(len(ALGOS)):
            c = tk.Canvas(arena, bg=BG, highlightthickness=0, width=420, height=300)
            c.grid(row=i // 2, column=i % 2, sticky="nsew", padx=5, pady=5)
            c.bind("<Configure>", lambda e, i=i: self.paint(i))
            self.canvases.append(c)

        self.update_custom_visibility()

    # -- controls
    def update_custom_visibility(self):
        mine = self.kind.get() == MINE
        if mine:
            self.size_scale.state(["disabled"])
            self.custom_label.pack(anchor="w", before=self.speed_label)
            self.custom_entry.pack(fill="x", before=self.speed_label)
            self.err_label.pack(anchor="w", before=self.speed_label, pady=(0, 10))
        else:
            self.size_scale.state(["!disabled"])
            self.custom_label.pack_forget()
            self.custom_entry.pack_forget()
            self.err_label.pack_forget()
            self.error.set("")

    def on_kind_change(self):
        self.update_custom_visibility()
        self.new_data()

    def on_size_drag(self, v):
        self.size_label.config(text=f"Size: {int(float(v))}")

    def on_speed_drag(self, v):
        n = int(float(v))
        self.speed.set(n)
        self.speed_label.config(text=f"Speed: {n}")

    # -- data / lanes
    def new_data(self, reshuffle=False):
        self.stop()
        kind = self.kind.get()
        custom = None
        if kind == MINE:
            custom, err = parse_numbers(self.text.get())
            self.error.set(err or "")
            if err:
                return False
        size = int(float(self.size_scale.get()))
        self.data = make_data(kind, size, custom)
        if kind == MINE and reshuffle:
            random.shuffle(self.data)        # "New data" reshuffles your own list
        self.reset_lanes()
        self.verdict.set("Press Start race to begin.")
        return True

    def reset_lanes(self):
        self.lanes = [Lane(*spec, self.data) for spec in ALGOS]
        self.mn, self.mx = min(self.data), max(self.data)
        for i in range(len(self.lanes)):
            self.paint(i)

    def paint(self, i):
        if i < len(self.lanes):
            draw_lane(self.canvases[i], self.lanes[i], self.mn, self.mx)

    # -- race
    def stop(self):
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.running = False

    def start(self):
        if self.kind.get() == MINE:
            if not self.new_data():
                return
        else:
            self.stop()
            self.reset_lanes()               # rerun on the same data
        self.running = True
        self.acc = 0.0
        self.finished = 0
        self.verdict.set("Racing...")
        self.tick()

    def tick(self):
        if not self.running:
            return
        self.acc += 0.15 * 1.15 ** self.speed.get()   # operations per frame
        k = int(self.acc)
        self.acc -= k
        touched = set()
        for _ in range(k):
            for i, L in enumerate(self.lanes):
                if L.done:
                    continue
                touched.add(i)
                try:
                    next(L.it)
                    L.steps += 1
                except StopIteration:
                    L.done, L.hl = True, []
                    self.finished += 1
                    L.rank = self.finished
        for i in touched:
            self.paint(i)

        if self.finished >= len(self.lanes):
            self.running = False
            self.after_id = None
            first = min(self.lanes, key=lambda L: L.rank)
            last = max(self.lanes, key=lambda L: L.rank)
            self.verdict.set(
                f"{first.name} finished first in {first.steps} steps. "
                f"{last.name} needed {last.steps}, about {last.steps / first.steps:.1f} times as many."
            )
            return
        self.after_id = self.root.after(30, self.tick)


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
