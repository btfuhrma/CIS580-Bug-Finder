import os
import pytest
from vectorizer import Vectorizor

@pytest.fixture
def setup_test_files():
    # Create test report and source code files
    report_file = "code.txt"
    source_dir = "Source code"
    os.makedirs(source_dir, exist_ok=True)

    with open(report_file, "w") as f:
        f.write("This is a test bug report.")

    with open(os.path.join(source_dir, "file1.py"), "w") as f:
        f.write("This is a test source code file.")

    with open(os.path.join(source_dir, "file2.py"), "w") as f:
        f.write("Another test source code file.")

    yield report_file, source_dir

    # Cleanup
    os.remove(report_file)
    for file in os.listdir(source_dir):
        os.remove(os.path.join(source_dir, file))
    os.rmdir(source_dir)

def test_load_report(setup_test_files):
    report_file, source_dir = setup_test_files
    vectorizor = Vectorizor(report_file, source_dir)
    assert vectorizor.load_report() == "This is a test bug report."

def test_load_source_code_files(setup_test_files):
    report_file, source_dir = setup_test_files
    vectorizor = Vectorizor(report_file, source_dir)
    assert sorted(vectorizor.load_source_code_files()) == sorted(["file1.py", "file2.py"])

def test_get_closest_file(setup_test_files):
    report_file, source_dir = setup_test_files
    vectorizor = Vectorizor(report_file, source_dir)
    closest_file, closest_score = vectorizor.getClosestFile()
    assert closest_file in ["file1.py", "file2.py"]
    assert 0 <= closest_score <= 1