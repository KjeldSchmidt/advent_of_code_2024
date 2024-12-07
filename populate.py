import requests
from datetime import datetime
from pathlib import Path

day_of_month = datetime.now().day

personal_input = requests.get(
    f'https://adventofcode.com/2024/day/{day_of_month}/input',
    headers = {
        'Cookie': Path('.session_cookie').read_text(),
    }
)

input_file = Path(f"day_{day_of_month}/input.txt")
input_file.write_text(personal_input.text)

scaffold = Path("scaffold.py")
main_file = Path(f"day_{day_of_month}/main.py")
main_file.write_text(scaffold.read_text())
