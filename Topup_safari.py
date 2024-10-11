import tkinter as tk
import pyautogui
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
import re
import subprocess
import time

class ResizableTransparentBox(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure the window
        self.overrideredirect(True)
        self.attributes('-alpha', 0.5)  # Set transparency (0.0 to 1.0)
        self.geometry('200x200+100+100')  # Set initial size and position

        # Create a label as the transparent box
        self.label = tk.Label(self, text="", bg='black')
        self.label.pack(fill='both', expand=True)

        # Bind mouse events for dragging and resizing
        self.label.bind('<ButtonPress-1>', self.start_drag)
        self.label.bind('<B1-Motion>', self.dragging)
        self.label.bind('<ButtonPress-3>', self.start_resize)
        self.label.bind('<B3-Motion>', self.resizing)
        self.label.bind('<ButtonRelease-3>', self.read_numbers)

    def start_drag(self, event):
        self._x = event.x
        self._y = event.y

    def dragging(self, event):
        x, y = self.winfo_x() + event.x - self._x, self.winfo_y() + event.y - self._y
        self.geometry(f'+{x}+{y}')

    def start_resize(self, event):
        self._start_x = self.winfo_width()
        self._start_y = self.winfo_height()
        self._x = event.x_root
        self._y = event.y_root

    def resizing(self, event):
        new_width = max(self._start_x + (event.x_root - self._x), 50)
        new_height = max(self._start_y + (event.y_root - self._y), 50)
        self.geometry(f'{new_width}x{new_height}+{self.winfo_x()}+{self.winfo_y()}')

    def read_numbers(self, event):
        geometry_str = self.geometry()
        width, height, x, y = map(int, geometry_str.replace('x', '+').split('+'))
        # Capture the region covered by the box
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        # Use pytesseract to perform OCR on the captured image
        numbers_text = pytesseract.image_to_string(screenshot)
        # Use regex to retrive only numbers (0-9) from the captured image
        numbers_text = re.findall("\d", numbers_text)
        # print("Numbers within the box:", numbers_text)
        for i in range(0, len(numbers_text), 16):
            card_num = numbers_text[i:i+16]
            card="".join(card_num)
            print(card)
            if len(card)==16:
                # makes dial-able and %23 == "#"
                dial= "*705*" + card +"%23"
                # Construct the ADB command to start a call with the specified phone number
                adb_command = 'adb shell am start -a android.intent.action.CALL -d tel:{}'.format(dial)
                # Run the ADB command using subprocess
                subprocess.run(adb_command, shell=True)
                time.sleep(0.2)
            else:
                pass

if __name__ == "__main__":
    app = ResizableTransparentBox()
    app.mainloop()