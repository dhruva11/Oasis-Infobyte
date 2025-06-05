import tkinter as tk
from tkinter import messagebox, scrolledtext
import speech_recognition as sr
import pyttsx3
import threading
from datetime import datetime
import pyaudio

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Flag to control listening state and command history
listening = False
command_history = []

def get_microphone_list():
    """Return a list of available microphone device names."""
    p = pyaudio.PyAudio()
    mics = []
    try:
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            if device_info.get('maxInputChannels') > 0:  # Only input devices
                mics.append(device_info.get('name', f"Microphone {i}"))
    finally:
        p.terminate()
    return mics if mics else ["Default Microphone"]

def listen(mic_index=None):
    global listening
    try:
        with sr.Microphone(device_index=mic_index if mic_index is not None else None) as source:
            output_text.insert(tk.END, "Listening...\n")
            output_text.see(tk.END)
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            output_text.insert(tk.END, f"You said: {text}\n")
            output_text.see(tk.END)
            command_history.append(text)
            return text.lower()
    except sr.UnknownValueError:
        output_text.insert(tk.END, "Could not understand audio.\n")
        output_text.see(tk.END)
        return ""
    except sr.RequestError:
        output_text.insert(tk.END, "Could not connect to recognition service.\n")
        output_text.see(tk.END)
        return ""
    except sr.WaitTimeoutError:
        output_text.insert(tk.END, "No audio input detected.\n")
        output_text.see(tk.END)
        return ""
    except Exception as e:
        output_text.insert(tk.END, f"Error with microphone: {str(e)}\n")
        output_text.see(tk.END)
        return ""

def speak(text):
    engine.say(text)
    engine.runAndWait()
    output_text.insert(tk.END, f"Assistant: {text}\n")
    output_text.see(tk.END)

def process_command():
    global listening
    mic_index = mic_var.get()
    mic_index = mic_list.index(mic_index) if mic_index != "Default Microphone" else None
    while listening:
        command = listen(mic_index)
        if not listening:  # Check if stop was pressed during listening
            break
        if command:
            if "hello" in command:
                speak("Hi there!")
            elif "exit" in command:
                speak("Goodbye!")
                listening = False
                toggle_button.config(text="Start Listening", bg="#4CAF50", activebackground="#45a049")
                status_canvas.itemconfig(status_circle, fill="red")
            elif "time" in command:
                current_time = datetime.now().strftime("%I:%M %p")
                speak(f"The current time is {current_time}.")
            elif "date" in command:
                current_date = datetime.now().strftime("%B %d, %Y")
                speak(f"Today is {current_date}.")
            else:
                speak("I didn't understand that command.")

def toggle_listening():
    global listening
    if not listening:
        listening = True
        toggle_button.config(text="Stop Listening", bg="#f44336", activebackground="#d32f2f")
        status_canvas.itemconfig(status_circle, fill="green")
        output_text.insert(tk.END, "Started listening...\n")
        output_text.see(tk.END)
        # Run listening in a separate thread to avoid freezing GUI
        threading.Thread(target=process_command, daemon=True).start()
    else:
        listening = False
        toggle_button.config(text="Start Listening", bg="#4CAF50", activebackground="#45a049")
        status_canvas.itemconfig(status_circle, fill="red")
        output_text.insert(tk.END, "Stopped listening.\n")
        output_text.see(tk.END)

def clear_text():
    output_text.delete(1.0, tk.END)

def show_history():
    if not command_history:
        messagebox.showinfo("Command History", "No commands in history.")
    else:
        history_text = "\n".join(command_history)
        messagebox.showinfo("Command History", f"Recent Commands:\n{history_text}")

def main():
    global root, output_text, toggle_button, status_canvas, status_circle, mic_var, mic_list
    root = tk.Tk()
    root.title("Voice Assistant")
    root.geometry("400x450")
    root.configure(bg="#f0f0f0")

    # Create main frame
    frame = tk.Frame(root, bg="#f0f0f0")
    frame.pack(pady=20, padx=20, expand=True)

    # Title
    tk.Label(frame, text="Voice Assistant", font=("Helvetica", 16, "bold"), bg="#f0f0f0").pack(pady=10)

    # Microphone selection
    tk.Label(frame, text="Select Microphone:", font=("Helvetica", 12), bg="#f0f0f0").pack()
    mic_list = get_microphone_list()
    mic_var = tk.StringVar(value=mic_list[0])
    mic_dropdown = tk.OptionMenu(frame, mic_var, *mic_list)
    mic_dropdown.config(font=("Helvetica", 10), bg="#ffffff")
    mic_dropdown.pack(pady=5)

    # Status indicator
    status_canvas = tk.Canvas(frame, width=20, height=20, bg="#f0f0f0", highlightthickness=0)
    status_canvas.pack(pady=5)
    status_circle = status_canvas.create_oval(5, 5, 15, 15, fill="red")

    # Output text area
    output_text = scrolledtext.ScrolledText(frame, font=("Helvetica", 10), height=10, width=40, wrap=tk.WORD)
    output_text.pack(pady=10)

    # Button frame
    button_frame = tk.Frame(frame, bg="#f0f0f0")
    button_frame.pack(pady=10)
    toggle_button = tk.Button(button_frame, text="Start Listening", font=("Helvetica", 10), bg="#4CAF50", fg="white",
                             activebackground="#45a049", command=toggle_listening)
    toggle_button.pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Clear", font=("Helvetica", 10), bg="#2196F3", fg="white",
              activebackground="#1976D2", command=clear_text).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Show History", font=("Helvetica", 10), bg="#FFC107", fg="black",
              activebackground="#FFB300", command=show_history).pack(side=tk.LEFT, padx=5)

    # Initial greeting
    speak("Hello! Select a microphone and click 'Start Listening' to begin.")
    output_text.insert(tk.END, "Assistant: Hello! Select a microphone and click 'Start Listening' to begin.\n")

    root.mainloop()

if __name__ == "__main__":
    main()