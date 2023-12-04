from pathlib import Path


data_path = Path(__file__).with_name("test.txt")
file_text = data_path.read_text()

