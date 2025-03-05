from docx import Document
import tkinter as tk
from tkinter import filedialog, scrolledtext

def extract_performance_requirements(file):
    doc = Document(file)
    content = []
    capture = False
    for para in doc.paragraphs:
        if "performance requirements" in para.text.lower():
            capture = True
            content.append(f'{para.text}')
        elif capture:
            if para.text.strip() == "":
                capture = False
            else:
                content.append(f'{para.text}')
        elif "performance requirements" in para.text.lower():
            content.append(f'{para.text}')
    return content

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Word Documents", "*.docx")])
    if file_path:
        with open(file_path, 'rb') as file:
            requirements = extract_performance_requirements(file)
            display_requirements(requirements)

def display_requirements(requirements):
    result_text.delete(1.0, tk.END)

    if len(requirements) == 0:
        result_text.insert(tk.END, "No requirements found")
        return
    for req in requirements:
        result_text.insert(tk.END, req + "\n")

def show_performance_qualification():
    clear_content_frame()
    browse_button = tk.Button(content_frame, text="Choose File", command=browse_file)
    browse_button.pack(pady=10)
    global result_text
    result_text = scrolledtext.ScrolledText(content_frame, wrap=tk.WORD, width=100, height=100)
    result_text.pack(pady=10)

def show_installation_qualification():
    clear_content_frame()
    tk.Label(content_frame, text="Installation Qualification functionality goes here").pack(pady=10)

def show_operational_qualification():
    clear_content_frame()
    tk.Label(content_frame, text="Operational Qualification functionality goes here").pack(pady=10)

def clear_content_frame():
    for widget in content_frame.winfo_children():
        widget.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Qualification Extractor")

    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=1)

    side_nav = tk.Frame(main_frame, width=200, bg='lightgrey')
    side_nav.pack(side=tk.LEFT, fill=tk.Y)

    content_frame = tk.Frame(main_frame)
    content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

    tk.Button(side_nav, text="Performance Qualification", command=show_performance_qualification).pack(fill=tk.X)
    tk.Button(side_nav, text="Installation Qualification", command=show_installation_qualification).pack(fill=tk.X)
    tk.Button(side_nav, text="Operational Qualification", command=show_operational_qualification).pack(fill=tk.X)

    root.mainloop()
