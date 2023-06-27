import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar
from HCR2Reader import process_images
from HCR2Reader import process_images, get_score_mapping
import pandas as pd

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(padx=10, pady=10)
        self.create_widgets()

    def create_widgets(self):
        self.select_button = tk.Button(self, text="Select Images", command=self.select_images)
        self.select_button.grid(row=0, column=0, pady=5)

        self.save_button = tk.Button(self, text="Save CSV", state=tk.DISABLED, command=self.save_csv)
        self.save_button.grid(row=1, column=0, pady=5)

        # Create a progress bar
        self.progress_var = tk.IntVar()
        self.progress_bar = Progressbar(self, length=500, variable=self.progress_var)
        self.progress_bar.grid(row=2, column=0, pady=5)

        # Create a label to display text about progress
        self.progress_text = tk.StringVar()
        self.progress_label = tk.Label(self, textvariable=self.progress_text)
        self.progress_label.grid(row=3, column=0, pady=5)

    def select_images(self):
        image_files = filedialog.askopenfilenames(title='Choose images', filetypes=[('Image Files', '*.png')])
        self.progress_var.set(0)
        self.progress_bar["maximum"] = len(image_files)
        
        self.df = pd.DataFrame()
        
        for image_file in image_files:
            # Update progress bar and text
            self.progress_var.set(image_files.index(image_file) + 1)
            self.progress_text.set(f"Processing: {image_file.split('/')[-1]}")
            self.progress_bar.update()

            processed_df = process_images(image_file)
            self.df = pd.concat([self.df, processed_df], ignore_index=True)
        
        self.df = self.df.sort_values(by=['points'], ascending=False)
        self.df['position'] = range(1, len(self.df) + 1)
        score_mapping = get_score_mapping()
        self.df['score'] = self.df['position'].map(score_mapping).fillna(0)

        self.progress_text.set("Done processing images!")
        self.save_button["state"] = tk.NORMAL

    def save_csv(self):
        if self.df is not None:
            csv_file = filedialog.asksaveasfilename(defaultextension=".csv")
            self.df.to_csv(csv_file, index=False)

root = tk.Tk()
root.title('HCR2 Reader') # Set the title of the window
app = Application(master=root)
app.mainloop()
