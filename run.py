import os
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

class RunnerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Runner")
        self.root.geometry("1000x600")
        self.root.resizable(True, True)

        # ===== Top frame =====
        top_frame = tk.Frame(root)
        top_frame.pack(fill=tk.X, pady=5)

        self.folder_label = tk.Label(top_frame, text="Folder: None", anchor="w")
        self.folder_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.select_btn = tk.Button(top_frame, text="Select Folder", command=self.select_folder)
        self.select_btn.pack(side=tk.LEFT, padx=5)

        self.run_btn = tk.Button(top_frame, text="Run Selected Files", command=self.run_selected)
        self.run_btn.pack(side=tk.RIGHT, padx=5)

        # ===== Select/Deselect all checkbox =====
        self.select_all_var = tk.IntVar(value=1)
        self.select_all_cb = tk.Checkbutton(root, text="Select All", variable=self.select_all_var, command=self.toggle_select_all)
        self.select_all_cb.pack(anchor="w", padx=5)

        # ===== Treeview =====
        self.tree = ttk.Treeview(root, columns=("Select", "File", "Path", "Status"), show='headings', selectmode='none')
        self.tree.heading("Select", text="Select")
        self.tree.heading("File", text="File Name")
        self.tree.heading("Path", text="Full Path")
        self.tree.heading("Status", text="Status")
        self.tree.column("Select", width=60, anchor="center")
        self.tree.column("File", width=300)
        self.tree.column("Path", width=500)
        self.tree.column("Status", width=120)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # ===== Progress bar =====
        self.progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=700, mode='determinate')
        self.progress.pack(pady=5)

        # ===== Data =====
        self.files = []  # list of dict: {path, selected_var, item}

    # ===== Folder selection =====
    def select_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return
        self.folder_label.config(text=f"Folder: {folder}")

        # Reset treeview
        self.tree.delete(*self.tree.get_children())
        self.files.clear()

        # Walk folder recursively
        for dirpath, dirnames, filenames in os.walk(folder):
            for file in filenames:
                ext = os.path.splitext(file)[1].lower()
                if ext in [".exe", ".ps1", ".bat"]:
                    full_path = os.path.join(dirpath, file)
                    selected_var = tk.IntVar(value=1)
                    item = self.tree.insert("", tk.END, values=("☑", file, full_path, "PENDING"))
                    self.files.append({"path": full_path, "selected_var": selected_var, "item": item})

        # Bind click on first column to toggle checkbox
        self.tree.bind("<Button-1>", self.toggle_checkbox)

    # ===== Toggle checkbox =====
    def toggle_checkbox(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            col = self.tree.identify_column(event.x)
            row = self.tree.identify_row(event.y)
            if col == "#1":  # Select column
                for f in self.files:
                    if f["item"] == row:
                        if f["selected_var"].get() == 1:
                            f["selected_var"].set(0)
                            self.tree.set(row, "Select", "☐")
                        else:
                            f["selected_var"].set(1)
                            self.tree.set(row, "Select", "☑")
                        break

    # ===== Select / Deselect all =====
    def toggle_select_all(self):
        value = self.select_all_var.get()
        for f in self.files:
            f["selected_var"].set(value)
            self.tree.set(f["item"], "Select", "☑" if value else "☐")

    # ===== Run selected files =====
    def run_selected(self):
        selected = [f for f in self.files if f["selected_var"].get()==1]
        if not selected:
            messagebox.showwarning("Warning", "No files selected!")
            return
        self.run_btn.config(state=tk.DISABLED)
        threading.Thread(target=self._run_thread, args=(selected,)).start()

    # ===== Thread run =====
    def _run_thread(self, selected_list):
        total = len(selected_list)
        self.progress['maximum'] = total

        for i, f in enumerate(selected_list, 1):
            file_path = f["path"]
            ext = os.path.splitext(file_path)[1].lower()
            item = f["item"]
            try:
                if ext == ".exe" or ext == ".bat":
                    cmd = [file_path] if ext == ".exe" else ["cmd", "/c", file_path]
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                elif ext == ".ps1":
                    result = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", file_path],
                                             capture_output=True, text=True, timeout=300)
                else:
                    result = None
                status = "SUCCESS" if result and result.returncode == 0 else f"FAIL ({result.returncode})" if result else "SKIPPED"
            except subprocess.TimeoutExpired:
                status = "TIMEOUT"
            except Exception as e:
                status = f"ERROR ({e})"

            # Update treeview
            self.tree.set(item, "Status", status)
            self._color_status(item, status)
            self.progress['value'] = i

        messagebox.showinfo("Done", "Selected files processed.")
        self.run_btn.config(state=tk.NORMAL)

    # ===== Color status =====
    def _color_status(self, item, status):
        if "SUCCESS" in status:
            self.tree.item(item, tags=("success",))
        elif "FAIL" in status:
            self.tree.item(item, tags=("fail",))
        elif "TIMEOUT" in status:
            self.tree.item(item, tags=("timeout",))
        else:
            self.tree.item(item, tags=("error",))

        self.tree.tag_configure("success", background="#d4edda")
        self.tree.tag_configure("fail", background="#f8d7da")
        self.tree.tag_configure("timeout", background="#fff3cd")
        self.tree.tag_configure("error", background="#f5c6cb")


if __name__ == "__main__":
    root = tk.Tk()
    app = RunnerGUI(root)
    root.mainloop()
