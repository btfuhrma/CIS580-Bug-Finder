import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from vectorizer import Vectorizor  # Ensure this is the correct path to your vectorizer module

class BugFinderGUI:
    def __init__(self, master):
        self.master = master
        master.title("Bug Finder Tool")

        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface components."""
        # Bug Report Section
        ttk.Label(self.master, text="Bug Report File:").grid(row=0, column=0, sticky="e")
        self.entry_report_file = ttk.Entry(self.master, width=40)
        self.entry_report_file.grid(row=0, column=1)

        ttk.Button(self.master, text="Browse", command=self.browse_report_file).grid(row=0, column=2)

        # Source Code Directory Section
        ttk.Label(self.master, text="Source Code Directory:").grid(row=1, column=0, sticky="e")
        self.entry_source_dir = ttk.Entry(self.master, width=40)
        self.entry_source_dir.grid(row=1, column=1)

        ttk.Button(self.master, text="Browse", command=self.browse_source_directory).grid(row=1, column=2)

        # Analyze Button
        ttk.Button(self.master, text="Analyze", command=self.analyze_report).grid(row=2, column=1)

    def browse_report_file(self):
        """Open a file dialog to select a bug report file."""
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            self.entry_report_file.delete(0, tk.END)
            self.entry_report_file.insert(0, filename)

    def browse_source_directory(self):
        """Open a directory dialog to select the source code directory."""
        directory = filedialog.askdirectory()
        if directory:
            self.entry_source_dir.delete(0, tk.END)
            self.entry_source_dir.insert(0, directory)

    def analyze_report(self):
        """Analyze the selected bug report against source code files."""
        report_file = self.entry_report_file.get()
        source_dir = self.entry_source_dir.get()

        # Validate report file input
        if not report_file or not os.path.isfile(report_file):
            messagebox.showerror("Error", "Please select a valid bug report file.")
            return

        # Validate source directory input
        if not source_dir or not os.path.isdir(source_dir):
            messagebox.showerror("Error", "Please select a valid source code directory.")
            return

        # Create an instance of the Vectorizor class and perform analysis
        vectorizor = Vectorizor(report_file, source_dir)
        
        try:
            similarities, files = vectorizor.get_all_similarities()
            closest_file, closest_score = vectorizor.getClosestFile()

            # Prepare results for display
            result_message = "Similarity Scores:\n"
            for file_name, score in zip(files, similarities):
                result_message += f"File: {file_name}, Similarity Score: {score:.4f}\n"

            result_message += f"\nClosest file: {closest_file}, Similarity score: {closest_score:.4f}"
            messagebox.showinfo("Analysis Results", result_message)


        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during analysis: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    bug_finder_gui = BugFinderGUI(root)
    root.mainloop()