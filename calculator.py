import tkinter as tk
from tkinter import ttk, messagebox
import math

class SmartCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Calculator")
        self.geometry("460x580")
        self.minsize(420, 520)
        self.configure(bg="#1e1e2e")

        self.expression = ""
        self.memory = 0.0
        self.history = []

        self._create_styles()
        self._build_ui()
        self._bind_keys()

    def _create_styles(self):
        self.colors = {
            "bg": "#1e1e2e",
            "display_bg": "#181825",
            "display_fg": "#cdd6f4",
            "subtext": "#a6adc8",
            "btn_num": "#313244",
            "btn_op": "#45475a",
            "btn_action": "#89b4fa",
            "btn_danger": "#f38ba8",
            "btn_hover": "#585b70",
            "text": "#cdd6f4",
        }

    def _build_ui(self):
        
        display_frame = tk.Frame(self, bg=self.colors["display_bg"], pady=12, padx=16)
        display_frame.pack(fill="x", padx=12, pady=(12, 6))

        
        self.sub_display = tk.Label(
            display_frame,
            text="",
            anchor="e",
            font=("Segoe UI", 11),
            bg=self.colors["display_bg"],
            fg=self.colors["subtext"],
        )
        self.sub_display.pack(fill="x")

    
        self.main_display = tk.Entry(
            display_frame,
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["display_bg"],
            fg=self.colors["display_fg"],
            bd=0,
            justify="right",
            insertbackground=self.colors["text"],
        )
        self.main_display.pack(fill="x", pady=(4, 0))
        self.main_display.insert(0, "0")
        self.main_display.config(state="readonly")

    
        btn_frame = tk.Frame(self, bg=self.colors["bg"])
        btn_frame.pack(fill="both", expand=True, padx=12, pady=6)

        buttons = [
            ("MC", self._mem_clear, "op"), ("MR", self._mem_recall, "op"), ("M+", self._mem_add, "op"), ("Hist", self._toggle_history, "op"), ("C", self._clear_all, "danger"),
            ("sin", lambda: self._add_func("math.sin"), "op"), ("cos", lambda: self._add_func("math.cos"), "op"), ("tan", lambda: self._add_func("math.tan"), "op"), ("√", lambda: self._add_func("math.sqrt"), "op"), ("⌫", self._backspace, "danger"),
            ("ln", lambda: self._add_func("math.log"), "op"), ("log", lambda: self._add_func("math.log10"), "op"), ("^", lambda: self._append("**"), "op"), ("(", lambda: self._append("("), "op"), (")", lambda: self._append(")"), "op"),
            ("7", lambda: self._append("7"), "num"), ("8", lambda: self._append("8"), "num"), ("9", lambda: self._append("9"), "num"), ("÷", lambda: self._append("/"), "op"), ("π", lambda: self._append(str(math.pi)), "op"),
            ("4", lambda: self._append("4"), "num"), ("5", lambda: self._append("5"), "num"), ("6", lambda: self._append("6"), "num"), ("×", lambda: self._append("*"), "op"), ("e", lambda: self._append(str(math.e)), "op"),
            ("1", lambda: self._append("1"), "num"), ("2", lambda: self._append("2"), "num"), ("3", lambda: self._append("3"), "num"), ("-", lambda: self._append("-"), "op"), ("%", lambda: self._append("/100"), "op"),
            ("0", lambda: self._append("0"), "num"), (".", lambda: self._append("."), "num"), ("±", self._toggle_sign, "num"), ("+", lambda: self._append("+"), "op"), ("=", self._calculate, "action")
        ]

        
        for r in range(7):
            btn_frame.rowconfigure(r, weight=1)
        for c in range(5):
            btn_frame.columnconfigure(c, weight=1)

        idx = 0
        for label, cmd, b_type in buttons:
            r = idx // 5
            c = idx % 5
            color = self.colors["btn_num"]
            fg = self.colors["text"]

            if b_type == "op":
                color = self.colors["btn_op"]
            elif b_type == "danger":
                color = self.colors["btn_danger"]
                fg = "#11111b"
            elif b_type == "action":
                color = self.colors["btn_action"]
                fg = "#11111b"

            btn = tk.Button(
                btn_frame,
                text=label,
                font=("Segoe UI", 12, "bold" if b_type in ["action", "danger"] else "normal"),
                bg=color,
                fg=fg,
                activebackground=self.colors["btn_hover"],
                activeforeground=self.colors["text"],
                relief="flat",
                bd=0,
                command=cmd,
                cursor="hand2",
            )
            btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")
            idx += 1

    def _bind_keys(self):
        self.bind("<Key>", self._on_key_press)
        self.bind("<Return>", lambda e: self._calculate())
        self.bind("<BackSpace>", lambda e: self._backspace())
        self.bind("<Escape>", lambda e: self._clear_all())

    def _on_key_press(self, event):
        allowed = "0123456789+-*/.()"
        if event.char in allowed:
            self._append(event.char)

    def _update_display(self, text):
        self.main_display.config(state="normal")
        self.main_display.delete(0, tk.END)
        self.main_display.insert(0, text if text else "0")
        self.main_display.config(state="readonly")

    def _append(self, char):
        self.expression += str(char)
        self._update_display(self.expression)

    def _add_func(self, func_name):
        self.expression += f"{func_name}("
        self._update_display(self.expression)

    def _clear_all(self):
        self.expression = ""
        self.sub_display.config(text="")
        self._update_display("0")

    def _backspace(self):
        self.expression = self.expression[:-1]
        self._update_display(self.expression)

    def _toggle_sign(self):
        if not self.expression:
            return
        if self.expression.startswith("-"):
            self.expression = self.expression[1:]
        else:
            self.expression = "-" + self.expression
        self._update_display(self.expression)

    def _calculate(self):
        if not self.expression:
            return

        try:
            
            safe_dict = {
                "math": math,
                "abs": abs,
                "round": round,
                "__builtins__": None,
            }
            result = eval(self.expression, safe_dict)

            
            if isinstance(result, float):
                result = round(result, 8)
                if result.is_integer():
                    result = int(result)

            self.sub_display.config(text=f"{self.expression} =")
            self.history.append(f"{self.expression} = {result}")
            self.expression = str(result)
            self._update_display(self.expression)

        except ZeroDivisionError:
            self._update_display("Cannot divide by 0")
            self.expression = ""
        except Exception:
            self._update_display("Error")
            self.expression = ""

    
    def _mem_clear(self):
        self.memory = 0.0

    def _mem_recall(self):
        self.expression += str(self.memory)
        self._update_display(self.expression)

    def _mem_add(self):
        try:
            self.memory += float(self.main_display.get())
        except ValueError:
            pass

    
    def _toggle_history(self):
        h_win = tk.Toplevel(self)
        h_win.title("Calculation History")
        h_win.geometry("300x400")
        h_win.configure(bg=self.colors["bg"])

        lbl = tk.Label(
            h_win,
            text="Recent History",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"],
            pady=10,
        )
        lbl.pack()

        listbox = tk.Listbox(
            h_win,
            bg=self.colors["display_bg"],
            fg=self.colors["text"],
            font=("Consolas", 10),
            bd=0,
            highlightthickness=0,
        )
        listbox.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        for entry in reversed(self.history):
            listbox.insert(tk.END, entry)


if __name__ == "__main__":
    app = SmartCalculator()
    app.mainloop()