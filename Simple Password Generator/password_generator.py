import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip


def generate_password(length, use_letters, use_numbers, use_symbols):
    characters = ""
    if use_letters:
        characters += string.ascii_letters
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation
    if not characters:
        return "Error: At least one character type must be selected."
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def validate_numeric_input(text):
    if text == "":
        return True
    try:
        int(text)
        return True
    except ValueError:
        return False


def generate_and_display():
    length_valid = validate_numeric_input(length_entry.get())
    length_entry.config(highlightbackground="red" if not length_valid else "SystemButtonFace")

    if not length_valid:
        messagebox.showerror("Error", "Please enter a valid number for length.")
        return

    length = int(length_entry.get())
    if length <= 0:
        messagebox.showerror("Error", "Length must be positive.")
        return

    use_letters = letters_var.get()
    use_numbers = numbers_var.get()
    use_symbols = symbols_var.get()
    password = generate_password(length, use_letters, use_numbers, use_symbols)
    if password.startswith("Error"):
        messagebox.showerror("Error", password)
        return
    password_label.config(text=f"Password: {password}")


def copy_to_clipboard():
    password_text = password_label.cget("text").replace("Password: ", "")
    if password_text and not password_text.startswith("Error"):
        pyperclip.copy(password_text)
        messagebox.showinfo("Success", "Password copied to clipboard!")
    else:
        messagebox.showerror("Error", "No password to copy.")


def main():
    root = tk.Tk()
    root.title("Password Generator")
    root.geometry("350x350")
    root.configure(bg="#f0f0f0")

    # Register validation command
    validate_cmd = root.register(validate_numeric_input)

    # Create main frame
    frame = tk.Frame(root, bg="#f0f0f0")
    frame.pack(pady=20, padx=20, expand=True)

    # Title
    tk.Label(frame, text="Password Generator", font=("Helvetica", 16, "bold"), bg="#f0f0f0").pack(pady=10)

    # Length input
    tk.Label(frame, text="Password Length:", font=("Helvetica", 12), bg="#f0f0f0").pack()
    global length_entry
    length_entry = tk.Entry(frame, font=("Helvetica", 12), width=15, validate="key",
                            validatecommand=(validate_cmd, "%P"))
    length_entry.pack(pady=5)

    # Checkboxes
    global letters_var, numbers_var, symbols_var
    letters_var = tk.BooleanVar(value=True)
    numbers_var = tk.BooleanVar(value=True)
    symbols_var = tk.BooleanVar()
    tk.Checkbutton(frame, text="Include Letters", variable=letters_var, font=("Helvetica", 10), bg="#f0f0f0").pack(
        anchor="w")
    tk.Checkbutton(frame, text="Include Numbers", variable=numbers_var, font=("Helvetica", 10), bg="#f0f0f0").pack(
        anchor="w")
    tk.Checkbutton(frame, text="Include Symbols", variable=symbols_var, font=("Helvetica", 10), bg="#f0f0f0").pack(
        anchor="w")

    # Buttons
    button_frame = tk.Frame(frame, bg="#f0f0f0")
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Generate Password", font=("Helvetica", 10), bg="#4CAF50", fg="white",
              activebackground="#45a049", command=generate_and_display).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Copy to Clipboard", font=("Helvetica", 10), bg="#2196F3", fg="white",
              activebackground="#1976D2", command=copy_to_clipboard).pack(side=tk.LEFT, padx=5)

    # Password label
    global password_label
    password_label = tk.Label(frame, text="Password: ", font=("Helvetica", 12), bg="#f0f0f0")
    password_label.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()