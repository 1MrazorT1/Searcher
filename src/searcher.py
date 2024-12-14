#!/usr/bin/env python3

import tkinter as tk
import searcherFrame
import utils

app = tk.Tk()
app.title("Searcher")
app.geometry("800x600")
app.resizable(False, False)

main_frame = create_main_frame(app)

load_algorithms(main_frame)

app.mainloop()