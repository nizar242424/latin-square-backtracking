import tkinter as tk
from tkinter import ttk, messagebox
import time
import json
import os
from tkinter import filedialog

class ModernTheme:
    BACKGROUND = "#f5f5f7"
    DARK_BG = "#282c34"
    PRIMARY = "#007aff"
    SECONDARY = "#5856d6"
    SUCCESS = "#34c759"
    WARNING = "#ff9500"
    DANGER = "#ff3b30"
    LIGHT_GRAY = "#e5e5ea"
    DARK_GRAY = "#8e8e93"
    TEXT_PRIMARY = "#000000"
    TEXT_SECONDARY = "#ffffff"
    
    @staticmethod
    def configure_styles():
        style = ttk.Style()
        
        style.configure("TFrame", background=ModernTheme.BACKGROUND)
        style.configure("Dark.TFrame", background=ModernTheme.DARK_BG)
        
        style.configure("TLabel", 
                       background=ModernTheme.BACKGROUND, 
                       foreground=ModernTheme.TEXT_PRIMARY, 
                       font=("Helvetica", 10))
        
        style.configure("Header.TLabel", 
                       background=ModernTheme.BACKGROUND, 
                       foreground=ModernTheme.TEXT_PRIMARY, 
                       font=("Helvetica", 16, "bold"))
        
        style.configure("Title.TLabel", 
                       background=ModernTheme.BACKGROUND, 
                       foreground=ModernTheme.TEXT_PRIMARY, 
                       font=("Helvetica", 12, "bold"))
        
        style.configure("Dark.TLabel", 
                       background=ModernTheme.DARK_BG, 
                       foreground=ModernTheme.TEXT_SECONDARY, 
                       font=("Helvetica", 10))
        
        style.configure("TButton", 
                       background=ModernTheme.PRIMARY, 
                       foreground=ModernTheme.TEXT_SECONDARY, 
                       font=("Helvetica", 10, "bold"),
                       borderwidth=0,
                       focusthickness=0,
                       padding=6)
        
        style.map("TButton",
                 background=[("active", ModernTheme.SECONDARY), 
                            ("disabled", ModernTheme.LIGHT_GRAY)],
                 foreground=[("disabled", ModernTheme.DARK_GRAY)])
        
        style.configure("Success.TButton", background=ModernTheme.SUCCESS)
        style.map("Success.TButton", background=[("active", "#2eb150")])
        
        style.configure("Danger.TButton", background=ModernTheme.DANGER)
        style.map("Danger.TButton", background=[("active", "#d93228")])
        
        style.configure("TEntry", 
                       fieldbackground=ModernTheme.LIGHT_GRAY,
                       foreground=ModernTheme.TEXT_PRIMARY,
                       borderwidth=0,
                       font=("Helvetica", 10))
        
        style.configure("TProgressbar", 
                       background=ModernTheme.PRIMARY,
                       troughcolor=ModernTheme.LIGHT_GRAY,
                       borderwidth=0)
        
        style.configure("TLabelframe", 
                       background=ModernTheme.BACKGROUND,
                       borderwidth=1,
                       relief="solid")
        
        style.configure("TLabelframe.Label", 
                       background=ModernTheme.BACKGROUND,
                       foreground=ModernTheme.TEXT_PRIMARY,
                       font=("Helvetica", 10, "bold"))
        
        style.configure("TScrollbar", 
                       background=ModernTheme.LIGHT_GRAY,
                       troughcolor=ModernTheme.BACKGROUND,
                       borderwidth=0,
                       arrowsize=12)

class LatinSquareGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Latin Square Generator")
        ModernTheme.configure_styles()
        self.setup_ui()
        self.solving = False
        self.stop_flag = False
        self.stop_message_shown = False  # Track if stop message has been shown

    def setup_ui(self):
        self.root.geometry("900x750")
        self.root.resizable(True, True)
        self.root.configure(bg=ModernTheme.BACKGROUND)
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        app_title = ttk.Label(header_frame, text="Latin Square Generator", style="Header.TLabel")
        app_title.pack(side=tk.LEFT)
        
        control_panel = ttk.LabelFrame(main_frame, text="Controls")
        control_panel.pack(fill=tk.X, pady=(0, 15))
        
        input_frame = ttk.Frame(control_panel)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        size_label = ttk.Label(input_frame, text="Size:")
        size_label.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="e")
        
        self.n_var = tk.StringVar(value="4")
        size_entry = ttk.Entry(input_frame, textvariable=self.n_var, width=5)
        size_entry.grid(row=0, column=1, padx=(0, 10), pady=5, sticky="w")
        
        delay_label = ttk.Label(input_frame, text="Delay (s):")
        delay_label.grid(row=0, column=2, padx=(10, 5), pady=5, sticky="e")
        
        self.delay_var = tk.DoubleVar(value=0.1)
        delay_entry = ttk.Entry(input_frame, textvariable=self.delay_var, width=5)
        delay_entry.grid(row=0, column=3, padx=(0, 10), pady=5, sticky="w")
        
        buttons_frame = ttk.Frame(input_frame)
        buttons_frame.grid(row=0, column=4, padx=10, pady=5)
        
        self.generate_btn = ttk.Button(buttons_frame, text="Generate", style="Success.TButton", command=self.generate_latin_square)
        self.generate_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(buttons_frame, text="Stop", style="Danger.TButton", command=self.stop_generation, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_btn = ttk.Button(buttons_frame, text="Save", command=self.save_square, state=tk.DISABLED)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        progress_frame = ttk.Frame(control_panel)
        progress_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        stats_frame = ttk.Frame(progress_frame)
        stats_frame.pack(fill=tk.X)
        
        self.time_label = ttk.Label(stats_frame, text="Time: 0.00s")
        self.time_label.pack(side=tk.LEFT, padx=(0, 15))
        
        self.steps_label = ttk.Label(stats_frame, text="Steps: 0")
        self.steps_label.pack(side=tk.LEFT)
        
        display_frame = ttk.LabelFrame(main_frame, text="Latin Square")
        display_frame.pack(fill=tk.BOTH, expand=True)
        
        self.table_container = ttk.Frame(display_frame)
        self.table_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.table_canvas = tk.Canvas(self.table_container, bg=ModernTheme.BACKGROUND, 
                                    highlightthickness=0)
        self.table_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar_y = ttk.Scrollbar(self.table_container, orient="vertical", 
                                  command=self.table_canvas.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill="y")
        
        scrollbar_x = ttk.Scrollbar(display_frame, orient="horizontal", 
                                  command=self.table_canvas.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill="x")
        
        self.table_canvas.configure(yscrollcommand=scrollbar_y.set, 
                                  xscrollcommand=scrollbar_x.set)
        self.table_canvas.bind('<Configure>', self.on_canvas_configure)
        
        self.table_frame = ttk.Frame(self.table_canvas, style="TFrame")
        self.canvas_window = self.table_canvas.create_window((0, 0), window=self.table_frame, 
                                                          anchor="center")

    def on_canvas_configure(self, event):
        self.table_canvas.update_idletasks()
        self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))
        
        canvas_width = self.table_canvas.winfo_width()
        canvas_height = self.table_canvas.winfo_height()
        
        if hasattr(self, 'table_frame'):
            frame_width = self.table_frame.winfo_reqwidth()
            frame_height = self.table_frame.winfo_reqheight()
            
            x = max(0, (canvas_width - frame_width) // 2)
            y = max(0, (canvas_height - frame_height) // 2)
            
            self.table_canvas.coords(self.canvas_window, x, y)

    def generate_latin_square(self):
        try:
            n = int(self.n_var.get())
            if n < 2:
                messagebox.showerror("Error", "Size must be at least 2.")
                return
            elif n > 15:
                response = messagebox.askquestion("Warning", 
                                             "Large sizes may take a long time to generate.\nDo you want to continue?")
                if response != "yes":
                    return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer for size.")
            return
        
        try:
            delay = float(self.delay_var.get())
            if delay < 0:
                messagebox.showerror("Error", "Delay cannot be negative.")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for delay.")
            return
        
        self.solving = True
        self.stop_flag = False
        self.stop_message_shown = False  # Reset the flag when starting new generation
        self.generate_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.save_btn.config(state=tk.DISABLED)
        
        self.latin_square = [[0] * n for _ in range(n)]
        self.start_time = time.time()
        self.steps = 0
        
        self.update_progress(0)
        self.update_stats()
        
        self.root.after(100, lambda: self.solve(0, 0, n))

    def solve(self, row, col, n):
        # Check for stop flag at the beginning of each recursive call
        if self.stop_flag:
            self.reset_controls()
            return False

        # Process UI events to ensure the stop button works
        self.root.update_idletasks()
        self.root.update()
        
        if col == n:
            self.finish_generation()
            return True

        if row == n - 1 and col == n - 1:
            for num in range(1, n + 1):
                # Check for stop again
                if self.stop_flag:
                    self.reset_controls()
                    return False
                    
                if self.is_safe(row, col, num, n):
                    self.latin_square[row][col] = num
                    self.update_display(n)
                    self.steps += 1
                    self.update_stats()
                    self.finish_generation()
                    return True
            return False

        for num in range(1, n + 1):
            # Check for stop flag before each iteration
            if self.stop_flag:
                self.reset_controls()
                return False
                
            if self.is_safe(row, col, num, n):
                self.latin_square[row][col] = num
                self.update_display(n)
                self.steps += 1
                self.update_stats()
                self.update_progress((row * n + col) / (n * n) * 100)
                
                self.root.update()
                time.sleep(self.delay_var.get())
                
                # Check for stop flag after delay
                if self.stop_flag:
                    self.reset_controls()
                    return False
                
                if col == n - 1:
                    if self.solve(row + 1, 0, n):
                        return True
                else:
                    if self.solve(row, col + 1, n):
                        return True

                # Check for stop flag before backtracking
                if self.stop_flag:
                    self.reset_controls()
                    return False
                    
                self.latin_square[row][col] = 0
                self.update_display(n)
                self.steps += 1
                self.update_stats()
                
                self.root.update()
                time.sleep(self.delay_var.get())

        return False

    def is_safe(self, row, col, num, n):
        for i in range(n):
            if self.latin_square[row][i] == num or self.latin_square[i][col] == num:
                return False
        return True

    def update_display(self, n):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        cell_size = min(50, max(30, 400 // n))
        padding = 2 if n <= 10 else 1
        font_size = max(8, min(16, int(22 - n * 0.8)))
        
        for i in range(n):
            for j in range(n):
                value = self.latin_square[i][j]
                
                if value == 0:
                    bg_color = ModernTheme.LIGHT_GRAY
                    fg_color = ModernTheme.LIGHT_GRAY
                    text = ""
                else:
                    if (i + j) % 2 == 0:
                        bg_color = ModernTheme.PRIMARY
                        fg_color = ModernTheme.TEXT_SECONDARY
                    else:
                        bg_color = ModernTheme.SECONDARY
                        fg_color = ModernTheme.TEXT_SECONDARY
                    text = str(value)
                
                frame = tk.Frame(
                    self.table_frame,
                    width=cell_size,
                    height=cell_size,
                    bg=bg_color,
                    highlightbackground="#000000",
                    highlightthickness=1
                )
                frame.grid(row=i, column=j, padx=padding, pady=padding)
                frame.grid_propagate(False)
                
                label = tk.Label(
                    frame,
                    text=text,
                    bg=bg_color,
                    fg=fg_color,
                    font=("Helvetica", font_size, "bold")
                )
                label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.table_frame.update_idletasks()
        self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))
        
        canvas_width = self.table_canvas.winfo_width()
        canvas_height = self.table_canvas.winfo_height()
        frame_width = self.table_frame.winfo_reqwidth()
        frame_height = self.table_frame.winfo_reqheight()
        
        x = max(0, (canvas_width - frame_width) // 2)
        y = max(0, (canvas_height - frame_height) // 2)
        
        self.table_canvas.coords(self.canvas_window, x, y)

    def update_progress(self, value):
        self.progress_var.set(value)
        self.progress_bar.update()

    def update_stats(self):
        elapsed_time = time.time() - self.start_time
        self.time_label.config(text=f"Time: {elapsed_time:.2f}s")
        self.steps_label.config(text=f"Steps: {self.steps}")

    def stop_generation(self):
        if not self.stop_flag:  # Only set the flag if it's not already set
            self.stop_flag = True
            self.stop_btn.config(state=tk.DISABLED)  # Disable stop button immediately

    def finish_generation(self):
        self.update_progress(100)
        self.generate_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.NORMAL)
        self.solving = False
        
        elapsed_time = time.time() - self.start_time
        messagebox.showinfo("Complete", f"Latin Square generated!\nTime: {elapsed_time:.2f}s\nSteps: {self.steps}")

    def reset_controls(self):
        if not self.stop_message_shown:  # Only show message once
            self.stop_message_shown = True
            self.generate_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.solving = False
            
            # Show message only when explicitly stopped by user (not when algorithm naturally completes)
            if self.stop_flag:
                messagebox.showinfo("Stopped", "Generation stopped by user.")

    def save_square(self):
        if not hasattr(self, 'latin_square') or not self.latin_square:
            messagebox.showerror("Error", "No Latin Square to save")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Latin Square"
        )
        
        if file_path:
            try:
                data = {
                    "size": len(self.latin_square),
                    "square": self.latin_square,
                    "time": time.time() - self.start_time,
                    "steps": self.steps
                }
                
                if file_path.endswith('.json'):
                    with open(file_path, 'w') as f:
                        json.dump(data, f, indent=2)
                else:
                    with open(file_path, 'w') as f:
                        f.write(f"Latin Square (n={len(self.latin_square)}):\n")
                        for row in self.latin_square:
                            f.write(" ".join(map(str, row)) + "\n")
                        f.write(f"\nGenerated in {data['time']:.2f} seconds")
                        f.write(f"\nTotal steps: {data['steps']}")
                
                messagebox.showinfo("Success", "Latin Square saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LatinSquareGenerator(root)
    root.mainloop()