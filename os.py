import tkinter as tk
from tkinter import messagebox, filedialog
import os
import cv2
from PIL import Image, ImageTk

# Function to open an enhanced text editor window
def open_text_editor():
    def save_file():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(text_area.get("1.0", tk.END))
            messagebox.showinfo("Save File", f"File saved: {file_path}")

    def open_file():
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                text_area.delete("1.0", tk.END)
                text_area.insert(tk.END, file.read())
            messagebox.showinfo("Open File", f"File opened: {file_path}")

    text_editor = tk.Toplevel()
    text_editor.title("Text Editor")
    text_editor.geometry("600x400")

    menu_bar = tk.Menu(text_editor)
    text_editor.config(menu=menu_bar)

    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Open", command=open_file)
    file_menu.add_command(label="Save", command=save_file)
    menu_bar.add_cascade(label="File", menu=file_menu)

    text_area = tk.Text(text_editor, wrap='word')
    text_area.pack(expand=1, fill='both')

# Function to open an enhanced calculator window
def open_calculator():
    def click(button):
        current = entry.get()
        if button == "=":
            try:
                result = str(eval(current))
                entry.delete(0, tk.END)
                entry.insert(tk.END, result)
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {e}")
                entry.delete(0, tk.END)
        elif button == "C":
            entry.delete(0, tk.END)
        else:
            entry.insert(tk.END, button)

    calculator = tk.Toplevel()
    calculator.title("Enhanced Calculator")
    calculator.geometry("300x400")

    entry = tk.Entry(calculator, font=("Arial", 18))
    entry.grid(row=0, column=0, columnspan=4)

    buttons = [
        '7', '8', '9', '/',
        '4', '5', '6', '*',
        '1', '2', '3', '-',
        '0', 'C', '=', '+'
    ]

    row = 1
    col = 0
    for button in buttons:
        btn = tk.Button(calculator, text=button, font=("Arial", 18), command=lambda b=button: click(b))
        btn.grid(row=row, column=col, sticky="nsew")
        col += 1
        if col > 3:
            col = 0
            row += 1

    for i in range(4):
        calculator.grid_columnconfigure(i, weight=1)
        calculator.grid_rowconfigure(i + 1, weight=1)

# Function to open a camera app window
def open_camera():
    def take_photo():
        ret, frame = cap.read()
        if ret:
            save_dir = "saved"
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            file_path = os.path.join(save_dir, f"photo_{len(os.listdir(save_dir)) + 1}.png")
            cv2.imwrite(file_path, frame)
            messagebox.showinfo("Photo Saved", f"Photo saved: {file_path}")
            add_file_to_desktop(file_path)

    def update_frame():
        ret, frame = cap.read()
        if ret:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(img)
            camera_label.config(image=img)
            camera_label.image = img
        camera_label.after(10, update_frame)

    camera_app = tk.Toplevel()
    camera_app.title("Camera App")
    camera_app.geometry("800x600")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Failed to open the webcam.")
        return

    camera_label = tk.Label(camera_app)
    camera_label.pack()

    take_photo_button = tk.Button(camera_app, text="Take Photo", command=take_photo)
    take_photo_button.pack()

    update_frame()

    camera_app.protocol("WM_DELETE_WINDOW", lambda: on_closing(cap, camera_app))

def add_file_to_desktop(file_path):
    file_name = os.path.basename(file_path)
    img = Image.open(file_path)
    img.thumbnail((100, 100))
    img = ImageTk.PhotoImage(img)
    desktop_area.create_image(50 + (len(os.listdir("saved")) * 110) % 800, 50 + (len(os.listdir("saved")) * 110) // 800 * 110, image=img, anchor='nw', tags="file")
    desktop_area.image = img

def on_closing(cap, window):
    cap.release()
    window.destroy()

# Function to shut down the application
def shutdown():
    root.destroy()

# Main application window
root = tk.Tk()
root.title("MaxosOS")
root.geometry("800x600")

# Menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Text Editor", command=open_text_editor)
file_menu.add_command(label="Calculator", command=open_calculator)
file_menu.add_command(label="Camera App", command=open_camera)
menu_bar.add_cascade(label="Applications", menu=file_menu)

# Desktop area
desktop_area = tk.Canvas(root, bg="lightblue")
desktop_area.pack(expand=1, fill='both')

# Taskbar
taskbar = tk.Frame(root, bg="grey")
taskbar.pack(side='bottom', fill='x')

# Taskbar buttons
text_editor_button = tk.Button(taskbar, text="Text Editor", command=open_text_editor)
text_editor_button.pack(side='left', padx=5, pady=5)

calculator_button = tk.Button(taskbar, text="Calculator", command=open_calculator)
calculator_button.pack(side='left', padx=5, pady=5)

camera_button = tk.Button(taskbar, text="Camera App", command=open_camera)
camera_button.pack(side='left', padx=5, pady=5)

shutdown_button = tk.Button(taskbar, text="Shutdown", command=shutdown)
shutdown_button.pack(side='right', padx=5, pady=5)

root.mainloop()
