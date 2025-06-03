import tkinter as tk
from tkinter import messagebox, TclError


def calculate_bmi(weight, height_cm):
    # Convert height from cm to meters
    height_m = height_cm / 100
    # Calculate BMI: weight (kg) / (height (m) ^ 2)
    bmi = weight / (height_m ** 2)
    return bmi


def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def validate_numeric_input(text):
    if text == "":
        return True
    try:
        float(text)
        return True
    except ValueError:
        return False


def calculate_and_display():
    weight_valid = validate_numeric_input(weight_entry.get())
    height_valid = validate_numeric_input(height_entry.get())

    weight_entry.config(highlightbackground="red" if not weight_valid else "SystemButtonFace")
    height_entry.config(highlightbackground="red" if not height_valid else "SystemButtonFace")

    if not weight_valid or not height_valid:
        messagebox.showerror("Error", "Please enter valid numerical values.")
        return

    weight = float(weight_entry.get())
    height_cm = float(height_entry.get())
    if weight <= 0 or height_cm <= 0:
        messagebox.showerror("Error", "Weight and height must be positive numbers.")
        return

    bmi = calculate_bmi(weight, height_cm)
    category = get_bmi_category(bmi)
    result_label.config(text=f"BMI: {bmi:.2f}\nCategory: {category}")


def clear_inputs():
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    result_label.config(text="BMI: \nCategory: ")
    weight_entry.config(highlightbackground="SystemButtonFace")
    height_entry.config(highlightbackground="SystemButtonFace")


def main():
    root = tk.Tk()
    root.title("BMI Calculator")
    root.geometry("350x300")
    root.configure(bg="#f0f0f0")

    # Register validation command
    validate_cmd = root.register(validate_numeric_input)

    # Create main frame
    frame = tk.Frame(root, bg="#f0f0f0")
    frame.pack(pady=20, padx=20, expand=True)

    # Title
    tk.Label(frame, text="BMI Calculator", font=("Helvetica", 16, "bold"), bg="#f0f0f0").pack(pady=10)

    # Weight input
    tk.Label(frame, text="Weight (kg):", font=("Helvetica", 12), bg="#f0f0f0").pack()
    global weight_entry
    weight_entry = tk.Entry(frame, font=("Helvetica", 12), width=15, validate="key",
                            validatecommand=(validate_cmd, "%P"))
    weight_entry.pack(pady=5)

    # Height input
    tk.Label(frame, text="Height (cm):", font=("Helvetica", 12), bg="#f0f0f0").pack()
    global height_entry
    height_entry = tk.Entry(frame, font=("Helvetica", 12), width=15, validate="key",
                            validatecommand=(validate_cmd, "%P"))
    height_entry.pack(pady=5)

    # Buttons
    button_frame = tk.Frame(frame, bg="#f0f0f0")
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Calculate BMI", font=("Helvetica", 10), bg="#4CAF50", fg="white",
              activebackground="#45a049", command=calculate_and_display).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Clear", font=("Helvetica", 10), bg="#f44336", fg="white",
              activebackground="#d32f2f", command=clear_inputs).pack(side=tk.LEFT, padx=5)

    # Result label
    global result_label
    result_label = tk.Label(frame, text="BMI: \nCategory: ", font=("Helvetica", 12), bg="#f0f0f0")
    result_label.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()