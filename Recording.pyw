import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import cv2
import numpy as np
import pyautogui
from screeninfo import get_monitors

class ScreenRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Recorder")

        self.is_recording = False
        self.output = None
        self.save_path = ""
        self.selected_fps = tk.StringVar(value="30")  # Default FPS
        self.selected_resolution = tk.StringVar(value="Auto")  # Default resolution

        self.root.geometry("350x250")  # Set the window size

        style = ttk.Style()
        style.theme_use("clam")  # Choose a theme (e.g., "clam", "arc", "alt", etc.)

        self.start_button = ttk.Button(root, text="Start Recording", command=self.start_recording, width=20)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED, width=20)
        self.stop_button.pack(pady=10)

        self.select_path_button = ttk.Button(root, text="Select Save Path", command=self.select_save_path, width=20)
        self.select_path_button.pack(pady=10)

        self.resolution_label = ttk.Label(root, text="Select Resolution:")
        self.resolution_label.pack()

        self.resolution_options = ["Auto", "1080p", "720p", "480p"]
        self.resolution_menu = ttk.Combobox(root, textvariable=self.selected_resolution, values=self.resolution_options)
        self.resolution_menu.pack()

        self.fps_label = ttk.Label(root, text="Select FPS:")
        self.fps_label.pack()

        self.fps_options = [str(i) for i in range(10, 101, 10)]  # 10, 20, ..., 100
        self.fps_menu = ttk.Combobox(root, textvariable=self.selected_fps, values=self.fps_options)
        self.fps_menu.pack()

    def select_save_path(self):
        self.save_path = filedialog.asksaveasfilename(defaultextension=".avi", filetypes=[("AVI files", "*.avi")])

    def get_screen_resolution(self):
        monitor = get_monitors()[0]  # Get the primary monitor
        return monitor.width, monitor.height

    def start_recording(self):
        if not self.save_path:
            messagebox.showerror("Error", "Please select a save path first!")
            return

        self.is_recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.select_path_button.config(state=tk.DISABLED)
        self.resolution_menu.config(state=tk.DISABLED)
        self.fps_menu.config(state=tk.DISABLED)

        selected_resolution = self.selected_resolution.get()
        if selected_resolution == "Auto":
            screen_width, screen_height = self.get_screen_resolution()
        else:
            resolution_mapping = {
                "1080p": (1920, 1080),
                "720p": (1280, 720),
                "480p": (858, 480)  # Adjusted for aspect ratio
            }
            resolution = resolution_mapping[selected_resolution]
            screen_width, screen_height = resolution

        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        fps = int(self.selected_fps.get())
        self.output = cv2.VideoWriter(self.save_path, fourcc, fps, (screen_width, screen_height))

        self.recording_thread = threading.Thread(target=self.record_screen)
        self.recording_thread.start()

    def stop_recording(self):
        self.is_recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.select_path_button.config(state=tk.NORMAL)
        self.resolution_menu.config(state=tk.NORMAL)
        self.fps_menu.config(state=tk.NORMAL)

    def record_screen(self):
        while self.is_recording:
            screenshot = pyautogui.screenshot()
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            self.output.write(frame)

        self.output.release()

def main():
    root = tk.Tk()
    app = ScreenRecorderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
