import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def input_process_data():
    num_processes = int(entry_processes.get())
    processes = []
    for i in range(num_processes):
        arrival_label = tk.Label(window, text=f"Arrival time for Process {i+1}:")
        arrival_label.grid(row=i+2, column=0, padx=5, pady=5, sticky="e")
        arrival_entry = tk.Entry(window)
        arrival_entry.grid(row=i+2, column=1, padx=5, pady=5)
        burst_label = tk.Label(window, text=f"Burst time for Process {i+1}:")
        burst_label.grid(row=i+2, column=2, padx=5, pady=5, sticky="e")
        burst_entry = tk.Entry(window)
        burst_entry.grid(row=i+2, column=3, padx=5, pady=5)
        processes.append((i+1, arrival_entry, burst_entry))
    return processes

def calculate_times():
    try:
        processes = []
        for i in range(int(entry_processes.get())):
            arrival_time = int(processes_entries[i][1].get())
            burst_time = int(processes_entries[i][2].get())
            processes.append((i + 1, arrival_time, burst_time))

        # Sort processes by arrival time
        processes.sort(key=lambda x: x[1])

        start_time = 0
        total_waiting_time = 0
        total_turnaround_time = 0
        total_response_time = 0

        gantt_chart = []

        while processes:
            # Filter processes that have arrived
            available_processes = [p for p in processes if p[1] <= start_time]
            if not available_processes:  # If no process is available at start_time
                start_time = processes[0][1]  # Jump in time to the next process arrival
                continue

            # Select process with shortest burst time
            available_processes.sort(key=lambda x: x[2])  # Sort by burst time
            current_process = available_processes[0]

            # Calculate times
            waiting_time = start_time - current_process[1]
            turnaround_time = waiting_time + current_process[2]
            response_time = waiting_time  # In non-preemptive, waiting time equals response time

            # Update totals
            total_waiting_time += waiting_time
            total_turnaround_time += turnaround_time
            total_response_time += response_time

            # Record Gantt chart
            gantt_chart.append((current_process[0], start_time, start_time + current_process[2]))

            # Move time forward
            start_time += current_process[2]

            # Mark process as completed
            processes.remove(current_process)

        num_processes = len(gantt_chart)
        avg_waiting_time = total_waiting_time / num_processes
        avg_turnaround_time = total_turnaround_time / num_processes
        avg_response_time = total_response_time / num_processes

        result_label.config(text=f"Average Waiting Time: {avg_waiting_time:.2f}\nAverage Turnaround Time: {avg_turnaround_time:.2f}\nAverage Response Time: {avg_response_time:.2f}")

        plot_gantt_chart(gantt_chart)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for arrival and burst times.")

def clear_entries():
    for entry in processes_entries:
        entry[1].delete(0, tk.END)
        entry[2].delete(0, tk.END)
    result_label.config(text="")
    if hasattr(window, 'canvas'):
        window.canvas.get_tk_widget().destroy()  # Clear previous Gantt chart canvas


def plot_gantt_chart(gantt_chart):
    fig = Figure(figsize=(10, 4), dpi=100)
    ax = fig.add_subplot(111)

    # Sort the Gantt chart based on the start time
    gantt_chart.sort(key=lambda x: x[1])

    for i, (process_id, start_time, end_time) in enumerate(gantt_chart):
        ax.barh(y=i, width=end_time - start_time, left=start_time, height=0.5, align='center',
                label=f'Process {process_id}')
    ax.set_xlabel('Time')
    ax.set_ylabel('Processes')
    ax.set_title('Gantt Chart')
    ax.set_yticks(range(len(gantt_chart)))
    ax.set_yticklabels(
        [f'P{process_id}' for process_id, _, _ in gantt_chart])  # Use process IDs from the sorted gantt_chart
    ax.grid(axis='x')
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=10, columnspan=4, padx=5, pady=5)
    window.canvas = canvas


window = tk.Tk()
window.title("Process Scheduling")

label_processes = tk.Label(window, text="Enter the number of processes:")
label_processes.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_processes = tk.Entry(window)
entry_processes.grid(row=0, column=1, padx=5, pady=5)

processes_entries = []

result_label = tk.Label(window, text="")
result_label.grid(row=1, columnspan=4, padx=5, pady=5)

calculate_button = tk.Button(window, text="Calculate", command=calculate_times)
calculate_button.grid(row=1, column=2, padx=5, pady=5)

clear_button = tk.Button(window, text="Clear", command=clear_entries)
clear_button.grid(row=1, column=1, padx=5, pady=5)

def update_processes_entries():
    global processes_entries
    processes_entries = input_process_data()

update_button = tk.Button(window, text="Update", command=update_processes_entries)
update_button.grid(row=0, column=2, padx=5, pady=5)

window.mainloop()