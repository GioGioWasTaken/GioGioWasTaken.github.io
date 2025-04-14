import os
import re

def process_md_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    filename = os.path.splitext(os.path.basename(filepath))[0].replace('_', ' ').title()
    content = ''.join(lines)

    # Check if file has TOML front matter (+ + +)
    if lines and lines[0].strip() == '+++':
        # Find end of front matter
        try:
            end_index = lines.index('+++\n', 1)
        except ValueError:
            print(f"[!] Malformed front matter in {filepath}")
            return

        header = ''.join(lines[1:end_index])
        body = ''.join(lines[end_index+1:])

        if 'title' not in header:
            header += f'title = "{filename}"\n'
            new_content = '+++\n' + header + '+++\n' + body
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"[+] Added title to front matter: {filepath}")
    else:
        # No front matter — add it
        body = content
        new_content = f'+++\ntitle = "{filename}"\n+++\n\n' + body
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"[+] Added new front matter: {filepath}")

def walk_and_process(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                full_path = os.path.join(root, file)
                process_md_file(full_path)

if __name__ == '__main__':
    walk_and_process('.')
