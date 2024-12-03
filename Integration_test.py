from unittest.mock import patch
import pytest
import tkinter as tk
from gui import BugFinderGUI

@pytest.fixture
def setup_gui():
    root = tk.Tk()
    gui = BugFinderGUI(root)
    yield gui
    root.destroy()

@patch("tkinter.filedialog.askopenfilename", return_value="code.txt")
@patch("tkinter.filedialog.askdirectory", return_value="Source code")
def test_file_selection(mock_file, mock_dir, setup_gui):
    gui = setup_gui
    gui.browse_report_file()
    assert gui.entry_report_file.get() == "code.txt"
    gui.browse_source_directory()
    assert gui.entry_source_dir.get() == "Source code"

@patch("tkinter.filedialog.askopenfilename", return_value="code.txt")
@patch("tkinter.filedialog.askdirectory", return_value="Source code")
def test_analyze_report(mock_file, mock_dir, setup_gui):
    gui = setup_gui
    gui.entry_report_file.insert(0, "code.txt")
    gui.entry_source_dir.insert(0, "Source code")
    gui.analyze_report()
    assert "Similarity Scores" in gui.results_text.get("1.0", "end")