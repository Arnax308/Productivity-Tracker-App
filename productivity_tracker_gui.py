from itertools import groupby
import tkinter as tk
from tkinter import messagebox, simpledialog

# Initialize tasks dictionary with an additional 'buttons_shown' flag
tasks = {}

def load_tasks_from_file():
    global tasks
    try:
        with open('tasks.txt', 'r') as f:
            for line in f:
                stripped_line = line.strip()
                if ':' in stripped_line:
                    task_name, *progress = stripped_line.split(': ', 1)
                    if progress:
                        tasks[task_name] = {'progress': list(progress[0]), 'buttons_shown': False}
                    else:
                        tasks[task_name] = {'progress': [], 'buttons_shown': False}  # Default to empty list if progress is missing
                else:
                    print(f"Skipping line due to missing ': ' delimiter: {stripped_line}")
    except FileNotFoundError:
        print("File not found. Starting with an empty tasks dictionary.")
        tasks = {}

def save_tasks_to_file():
    with open('tasks.txt', 'w') as f:
        for task, info in tasks.items():
            f.write(f"{task}: {' '.join(info['progress'])}\n")

def add_task():
    task_name = simpledialog.askstring("Input", "Enter the task name:", parent=root)
    if task_name:
        tasks[task_name] = {'progress': [''], 'buttons_shown': False}
        save_tasks_to_file()
        update_ui()
        messagebox.showinfo("Success", "Task added successfully.")

def del_task():
    task_name = simpledialog.askstring("Input", "Enter the task name:", parent=root)
    if task_name in tasks:
        # Remove the task from the tasks dictionary
        del tasks[task_name]
        # Save the updated tasks to file
        save_tasks_to_file()
        
        # Destroy the existing frame
        if hasattr(root, 'frame'):
            root.frame.destroy()
        
        # Create a new frame
        root.frame = tk.Frame(root)
        root.frame.pack(padx=20, pady=20)
        
        # Repopulate the frame with the current tasks
        update_ui()
        
        messagebox.showinfo("Success", "Task deleted successfully.")
    else:
        messagebox.showerror("Error", "Task not found.")



def mark_as_done(task_name):
    if task_name in tasks:
        tasks[task_name]['progress'].append('O')
        save_tasks_to_file()
        update_ui()
        messagebox.showinfo("Success", "Task marked as done.")
    else:
        messagebox.showerror("Error", "Task not found.")

def mark_as_not_done(task_name):
    if task_name in tasks:
        tasks[task_name]['progress'].append('X')
        save_tasks_to_file()
        update_ui()
        messagebox.showinfo("Success", "Task marked as not done.")
    else:
        messagebox.showerror("Error", "Task not found.")

def view_status():
    status_text = "\n".join([f"{task}: {' '.join(progress)}" for task, info in tasks.items() for progress in (info['progress'],)])
    messagebox.showinfo("Status", status_text)

def count_last_continuous_os():
    last_sequence_counts = []
    for info in tasks.values():
        progress = info['progress']
        last_x_index = next((i for i, x in enumerate(reversed(progress)) if x == 'X'), -1)
        if last_x_index == -1:
            last_sequence_counts.append(len(progress))
        else:
            last_sequence_counts.append(last_x_index)
    
    status_text = "Last Continuous Streak:\n" + "\n".join([f"{task}: {count-1}" for task, count in zip(tasks.keys(), last_sequence_counts)])
    messagebox.showinfo("Continuous Streak", status_text)

def update_ui():
    frame = tk.Frame(root)
    frame.pack(padx=20, pady=20)
    for task in tasks.keys():
        if task in tasks:
            task_label = tk.Label(frame, text=task)
            task_label.pack(side=tk.TOP, fill=tk.X)
            
            done_button = tk.Checkbutton(frame, text="Done", command=lambda t=task: mark_as_done(t))
            done_button.pack(side=tk.LEFT, padx=10)
            
            not_done_button = tk.Checkbutton(frame, text="Not Done", command=lambda t=task: mark_as_not_done(t))
            not_done_button.pack(side=tk.LEFT, padx=10)




root = tk.Tk()
root.frame = tk.Frame(root)
root.frame.pack(padx=20, pady=20)

root.title('Productivity Tracker App')
root.geometry('800x600')

load_tasks_from_file()

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

update_ui()

add_button = tk.Button(root, text='Add Task', command=add_task)
add_button.pack(pady=10)

delete_button = tk.Button(root, text='Delete Task', command=del_task)
delete_button.pack(pady=10)

continuous_os_button = tk.Button(root, text='Streak', command=count_last_continuous_os)
continuous_os_button.pack(pady=10)

exit_button = tk.Button(root, text='Exit', command=root.quit)
exit_button.pack(pady=10)

root.mainloop()


