"""A script to organize files scatterd in many directories."""

import os


base_path = "/home/alex/django/mosh/Code With Mosh - The Ultimate Django Series Part 1"

for dir in sorted(os.listdir(base_path)):
    full_path = os.path.join(base_path, dir)
    for path, dirs, files in os.walk(full_path):
        for file in files:
            required_files = [".mp4", ".pdf", ".zip"]
            file_ext = file[-4:]
            if file_ext in required_files:
                file_path = os.path.join(path, file)
                print(f"Moving {file} to {full_path}...")
                os.rename(file_path, os.path.join(full_path, file))
                for d in dirs:
                    os.rmdir(d)
    print("-" * 50)
