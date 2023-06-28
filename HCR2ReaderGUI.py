import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar
from tkinter import messagebox
from tkinter import simpledialog
from HCR2Reader import process_images, get_score_mapping
import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(padx=10, pady=10)
        self.create_widgets()

    def create_widgets(self):
        self.select_button = tk.Button(self, text="Select Images", command=self.select_images)
        self.select_button.grid(row=0, column=0, pady=5)

        self.save_button = tk.Button(self, text="Save Data", state=tk.DISABLED, command=self.save_data)
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

    def save_data(self):
        if self.df is not None:
            # Count the number of each kind of record
            color_counts = len(self.df['color'])
            position_counts = len(self.df['position'])
            player_counts = len(self.df['player'])
            score_counts = len(self.df['score'])
            points_counts = len(self.df['points'])

            # Check if the counts match
            counts_match = all(counts == len(self.df) for counts in [color_counts, position_counts, player_counts, score_counts, points_counts])

            # Create a message to display to the user
            message = ""
            if not counts_match:
                message += "There may be an issue with the data. Some counts do not match.\n\n"
                message += "Record Counts:\n"
                message += f"Colors: {color_counts}\n"
                message += f"Positions: {position_counts}\n"
                message += f"Players: {player_counts}\n"
                message += f"Scores: {score_counts}\n"
                message += f"Points: {points_counts}\n"
            else:
                message += f"Number of complete records: {len(self.df)}"

            # Show a custom dialog box with the record counts or the number of complete records
            dialog = FormatDialog(self.master, "Save Data", message)
            format_choice = dialog.result

            # Save the data in the chosen format
            if format_choice is not None:
                file_path = filedialog.asksaveasfilename(defaultextension=f".{format_choice}")
                if file_path:
                    if format_choice == "csv":
                        self.df.to_csv(file_path, index=False)
                    elif format_choice == "xml":
                        self.df.to_xml(file_path, root_name='data', row_name='record')
                    elif format_choice == "json":
                        self.df.to_json(file_path, orient='records')
                    elif format_choice == "html":
                        styled_table = self.df.style.applymap(lambda color: f"background-color: {color}", subset=['color'])
                        modified_html = self.modify_html_table(styled_table)
                        with open(file_path, 'w') as f:
                            f.write(modified_html)

                        messagebox.showinfo("Save Successful", f"Data saved as {format_choice.upper()} format.")

    def modify_html_table(self, styled_table):
        # Convert styled table to HTML string
        html = styled_table.set_table_attributes('class="styled-table"')._repr_html_()

        # Use BeautifulSoup to parse the HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Find the table
        table = soup.find('table')

        # Find the index of the "color" column
        color_column_index = styled_table.columns.get_loc("color")

        # Colors dictionary
        color_dict = {"blue": "#B5CEFF", "yellow": "#FFFFC8"}

        # Iterate over each row in the table
        for row in table.find_all('tr'):
            # Get all cells in the row
            cells = row.find_all('td')
            # If this row has a cell in the "color" column
            if len(cells) > color_column_index:
                # Get the "color" cell
                color_cell = cells[color_column_index]
                # Get the color value (strip any existing styles to avoid confusion)
                color_value = color_cell.get_text(strip=True)
                # Check if the color value exists in our color dictionary
                if color_value in color_dict:
                    # Replace the color value with the corresponding color in the dictionary
                    color_value = color_dict[color_value]
                # Set the background color of the row
                row['style'] = f'background-color: {color_value};'

        # Convert the modified BeautifulSoup object back to a string
        modified_html = str(soup)

        return modified_html

class FormatDialog(simpledialog.Dialog):
    def __init__(self, parent, title, message):
        self.result = None
        self.text = message
        super().__init__(parent, title=title)

    def body(self, master):
        tk.Label(master, text=self.text).pack()

        format_choices = ["csv", "xml", "json", "html"]
        self.var = tk.StringVar(master)
        self.var.set(format_choices[0])

        format_option = tk.OptionMenu(master, self.var, *format_choices)
        format_option.pack()

    def apply(self):
        self.result = self.var.get()

root = tk.Tk()
root.title('HCR2 Reader') # Set the title of the window
app = Application(master=root)
app.mainloop()