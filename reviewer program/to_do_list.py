import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os
import random

group_colors = ["#e0f7fa", "#ffeb3b", "#c8e6c9", "#ffccbc", "#f48fb1", "#bbdefb", "#d1c4e9", "#b2dfdb"]
groups = {}

# Default autosave file (next to this script)
DEFAULT_SAVE_PATH = os.path.join(os.path.dirname(__file__), "todo_data.json")


def show_todo_mode(parent):
    # --- Variables ---
    global task_entry, group_entry, selected_group, group_dropdown, task_area

    # --- Helper: persist/load data ---
    def get_serializable_data():
        data = {}
        for gname, ginfo in groups.items():
            tasks = []
            for task_label, task_var in ginfo['tasks']:
                tasks.append({
                    "text": task_label.cget("text"),
                    "done": bool(task_var.get())
                })
            data[gname] = tasks
        return data

    def save_default():
        try:
            data = get_serializable_data()
            with open(DEFAULT_SAVE_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            # keep silent for autosave; show debug on explicit save if needed
            print("Auto-save error:", e)

    def save_as_dialog():
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Save To-Do List As"
            )
            if not file_path:
                return
            data = get_serializable_data()
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Saved", f"To-do list saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error Saving", f"Could not save to file:\n{e}")

    def load_from_path(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Clear existing groups
            clear_tasks(silent=True)
            for gname, tasks in data.items():
                create_group(gname)
                for t in tasks:
                    text = t.get("text", "")
                    done = bool(t.get("done", False))
                    task_var = tk.IntVar(value=1 if done else 0)
                    task_label = tk.Checkbutton(
                        groups[gname]['frame'],
                        text=text,
                        variable=task_var,
                        font=("Arial", 12),
                        command=lambda tl=None, tv=task_var: toggle_task(tl, tv)
                    )
                    # Fix callback closure by configuring after creation
                    # set the command properly referencing the created widget
                    task_label.config(command=lambda tl=task_label, tv=task_var: toggle_task(tl, tv))
                    task_label.pack(anchor="w", padx=10, pady=2)
                    groups[gname]['tasks'].append((task_label, task_var))
                    # apply visual state
                    if done:
                        task_label.config(font=("Arial", 12, "bold", "overstrike"), fg="gray")
            update_group_dropdown()
            save_default()  # autosave loaded state to default path
        except Exception as e:
            messagebox.showerror("Load Error", f"Could not load file:\n{e}")

    def load_dialog():
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if not file_path:
            return
        load_from_path(file_path)

    def load_default_if_exists():
        if os.path.exists(DEFAULT_SAVE_PATH):
            load_from_path(DEFAULT_SAVE_PATH)

    # --- Functions (UI actions) ---
    def add_task():
        task = task_entry.get().strip()
        group = selected_group.get()
        if not task:
            messagebox.showwarning("Warning", "Please enter a task.")
            return
        if group == "Select a group":
            messagebox.showwarning("Warning", "Please select or add a group first.")
            return
        task_var = tk.IntVar()
        task_label = tk.Checkbutton(
            groups[group]['frame'],
            text=task,
            variable=task_var,
            font=("Arial", 12),
        )
        # set command with closure
        task_label.config(command=lambda tl=task_label, tv=task_var: toggle_task(tl, tv))
        task_label.pack(anchor="w", padx=10, pady=2)
        groups[group]['tasks'].append((task_label, task_var))
        task_entry.delete(0, tk.END)
        save_default()  # autosave

    def delete_group(group):
        if group in groups:
            groups[group]['frame'].destroy()
            del groups[group]
            update_group_dropdown()
            save_default()  # autosave

    def delete_task():
        changed = False
        for gname, group in list(groups.items()):
            to_remove = [pair for pair in group['tasks'] if pair[1].get() == 1]
            for task_label, task_var in to_remove:
                task_label.destroy()
                group['tasks'].remove((task_label, task_var))
                changed = True
        if changed:
            save_default()  # autosave

    def clear_tasks(silent=False):
        # remove all group frames
        for gname in list(groups.keys()):
            groups[gname]['frame'].destroy()
            del groups[gname]
        update_group_dropdown()
        if not silent:
            save_default()  # autosave

    def toggle_task(task_label, task_var):
        if task_label is None:
            return
        if task_var.get() == 1:
            task_label.config(font=("Arial", 12, "bold", "overstrike"), fg="gray")
        else:
            task_label.config(font=("Arial", 12), fg="black")
        save_default()  # autosave

    def create_group(group_name):
        if group_name in groups:
            return
        # pick color deterministically or random
        available = [c for c in group_colors if c not in [groups[g]['frame'].cget('bg') for g in groups]]
        color = random.choice(available) if available else random.choice(group_colors)
        group_frame = tk.LabelFrame(task_area, text=group_name, bg=color, font=("Arial", 12, "bold"))
        group_frame.pack(fill="x", padx=10, pady=5)
        del_group_btn = tk.Button(
            group_frame, text="Delete Group", command=lambda gn=group_name: delete_group(gn),
            bg="#f44336", fg="white", font=("Arial", 10)
        )
        del_group_btn.pack(anchor="e", padx=5, pady=2)
        groups[group_name] = {'frame': group_frame, 'tasks': []}
        update_group_dropdown()
        save_default()  # autosave

    def update_group_dropdown():
        menu = group_dropdown["menu"]
        menu.delete(0, "end")
        for group in groups.keys():
            menu.add_command(label=group, command=tk._setit(selected_group, group))
        if groups:
            # set to first existing group if current selection not valid
            current = selected_group.get()
            if current not in groups:
                selected_group.set(next(iter(groups.keys())))
        else:
            selected_group.set("Select a group")

    def add_group():
        group_name = group_entry.get().strip()
        if not group_name:
            messagebox.showwarning("Warning", "Please enter a group name.")
            return
        if group_name in groups:
            messagebox.showwarning("Warning", "Group already exists.")
            return
        create_group(group_name)
        group_entry.delete(0, tk.END)

    # explicit save button uses Save As dialog
    def save_lists():
        save_as_dialog()

    # --- UI ---
    todo_frame = tk.Frame(parent, bg="#f5f5f5")
    todo_frame.pack(fill="both", expand=True)

    # Task Entry
    frame = tk.Frame(todo_frame, bg="#f5f5f5")
    frame.pack(pady=10)

    tk.Label(frame, text="Task:", bg="#f5f5f5", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
    task_entry = tk.Entry(frame, width=25, font=("Arial", 12))
    task_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame, text="Group:", bg="#f5f5f5", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
    group_entry = tk.Entry(frame, width=25, font=("Arial", 12))
    group_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame, text="Select Group:", bg="#f5f5f5", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5)
    selected_group = tk.StringVar(value="Select a group")
    group_dropdown = tk.OptionMenu(frame, selected_group, "Select a group")
    group_dropdown.config(width=22, font=("Arial", 12))
    group_dropdown.grid(row=2, column=1, padx=5, pady=5)

    # Buttons
    btn_frame = tk.Frame(todo_frame, bg="#f5f5f5")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Add Task", command=add_task, width=15, bg="#4CAF50", fg="white", font=("Arial", 10)).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Add Group", command=add_group, width=15, bg="#2196F3", fg="white", font=("Arial", 10)).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Delete Selected Tasks", command=delete_task, width=15, bg="#f44336", fg="white", font=("Arial", 10)).grid(row=1, column=0, padx=5)
    tk.Button(btn_frame, text="Clear All", command=clear_tasks, width=15, bg="#2196F3", fg="white", font=("Arial", 10)).grid(row=1, column=1, padx=5)

    # Save/Load controls
    tk.Button(btn_frame, text="Save As...", command=save_lists, width=15, bg="#6a5acd", fg="white", font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=6)
    tk.Button(btn_frame, text="Load...", command=load_dialog, width=15, bg="#6a5acd", fg="white", font=("Arial", 10)).grid(row=2, column=1, padx=5, pady=6)

    # Task List Area
    task_area = tk.Frame(todo_frame, bg="#f5f5f5")
    task_area.pack(padx=10, pady=10, fill="both", expand=True)

    # Load saved data if present
    load_default_if_exists()

    # Return the frame so you can manage it (show/hide) in main.py
    return todo_frame
