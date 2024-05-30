from itertools import groupby
import tkinter as tk
from tkinter import messagebox, simpledialog

# Initialize tasks dictionary
tasks = {}

def load_tasks_from_file():
    global tasks
    try:
        with open('tasks.txt', 'r') as f:
            for line in f:
                stripped_line = line.strip()
                print(f"Processing line: {stripped_line}")  # Debugging: Print each line
                if ':' in stripped_line:
                    task_name, *progress = stripped_line.split(': ', 1)
                    if progress:
                        tasks[task_name] = list(progress[0])
                    else:
                        tasks[task_name] = []  # Default to empty list if progress is missing
                else:
                    print(f"Skipping line due to missing ': ' delimiter: {stripped_line}")
    except FileNotFoundError:
        print("File not found. Starting with an empty tasks dictionary.")
        tasks = {}


def save_tasks_to_file():
    with open('tasks.txt', 'w') as f:
        for task, progress in tasks.items():
            f.write(f"{task}: {' '.join(progress)}\n")

def add_task():
    task_name = simpledialog.askstring("Input", "Enter the task name:", parent=root)
    if task_name:
        tasks[task_name] = ['']
        save_tasks_to_file()
        update_ui()
        messagebox.showinfo("Success", "Task added successfully.")

def del_task():
    task_name = simpledialog.askstring("Input", "Enter the task name:", parent=root)
    if task_name in tasks:
        del tasks[task_name]
        save_tasks_to_file()
        update_ui()
        messagebox.showinfo("Success", "Task deleted successfully.")
    else:
        messagebox.showerror("Error", "Task not found.")

def mark_as_done(task_name):
    if task_name in tasks:
        tasks[task_name].append('O')
        save_tasks_to_file()
        update_ui()
        messagebox.showinfo("Success", "Task marked as done.")
    else:
        messagebox.showerror("Error", "Task not found.")

def mark_as_not_done(task_name):
    if task_name in tasks:
        tasks[task_name].append('X')
        save_tasks_to_file()
        update_ui()
        messagebox.showinfo("Success", "Task marked as not done.")
    else:
        messagebox.showerror("Error", "Task not found.")

def view_status():
    status_text = "\n".join([f"{task}: {' '.join(progress)}" for task, progress in tasks.items()])
    messagebox.showinfo("Status", status_text)

def count_last_continuous_os():
    last_sequence_counts = []
    for progress in tasks.values():
        # Find the index of the last 'X'
        last_x_index = next((i for i, x in enumerate(reversed(progress)) if x == 'X'), -1)
        
        # If 'X' is not found, consider the entire list as 'O's
        if last_x_index == -1:
            last_sequence_counts.append(len(progress))
        else:
            # Calculate the count of 'O's before the last 'X'
            last_sequence_counts.append(last_x_index)
    
    status_text = "Last Continuous Streak:\n" + "\n".join([f"{task}: {count}" for task, count in zip(tasks.keys(), last_sequence_counts)])
    messagebox.showinfo("Continuous Streak", status_text)

def update_ui():
    frame = tk.Frame(root)
    frame.pack(padx=20, pady=20)
    row_index = 0
    for task, progress in tasks.items():
        task_label = tk.Label(frame, text=task)
        task_label.grid(row=row_index, column=0, padx=10, sticky=tk.W)

        done_button = tk.Checkbutton(frame, text="Done", command=lambda t=task: mark_as_done(t))
        done_button.grid(row=row_index, column=1, padx=10, sticky=tk.W)

        not_done_button = tk.Checkbutton(frame, text="Not Done", command=lambda t=task: mark_as_not_done(t))
        not_done_button.grid(row=row_index, column=2, padx=10, sticky=tk.W)

        row_index += 1

root = tk.Tk()
root.title('Productivity Tracker App')
root.geometry('800x600')  # Adjusted window size for better visibility

load_tasks_from_file()

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

update_ui()  # Initial UI setup

add_button = tk.Button(root, text='Add Task', command=add_task)
add_button.pack(pady=10)

delete_button = tk.Button(root, text='Delete Task', command=del_task)
delete_button.pack(pady=10)

continuous_os_button = tk.Button(root, text='Streak', command=count_last_continuous_os)
continuous_os_button.pack(pady=10)


exit_button = tk.Button(root, text='Exit', command=root.quit)
exit_button.pack(pady=10)

root.mainloop()

