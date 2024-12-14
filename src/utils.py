import tkinter as tk

def load_algorithms(parent_widget):
    scrollbar = tk.Scrollbar(parent_widget, orient = tk.VERTICAL)
    scrollbar.pack(side=tk.RIGHT, fill = tk.Y)

    listbox = tk.Listbox(parent_widget, yscrollcommand = scrollbar.set)
    listbox.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)

    scrollbar.config(command = listbox.yview)

    algorithms = ["A1", "A2", "A3"]
    for algorithm in algorithms:
        listbox.insert(tk.END, algorithm)
    
    listbox.bind("<<ListboxSelect>>", lambda event: select_algorithm(event, listbox))


def select_algorithm(event, listbox):
    selected = listbox.get(listbox.curselection())
    print(f"Selected Algorithm: {selected}")