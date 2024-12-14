import tkinter as tk

def create_main_frame(app):
    main_frame = tk.Frame(app)
    main_frame.pack(fill=tk.BOTH, expand = True)

    return main_frame