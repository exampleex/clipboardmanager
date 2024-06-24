import tkinter as tk
from tkinter import messagebox
import pyperclip
from datetime import datetime

class ClipboardManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Clipboard Manager")

        self.clipboard_history = []

        self.create_widgets()
        self.check_clipboard()

    def create_widgets(self):
        self.history_listbox = tk.Listbox(self.root, width=50, height=20)
        self.history_listbox.pack(pady=10)

        self.copy_button = tk.Button(self.root, text="Copy Selected", command=self.copy_selected)
        self.copy_button.pack(pady=5)

        self.clear_button = tk.Button(self.root, text="Clear History", command=self.clear_history)
        self.clear_button.pack(pady=5)

    def check_clipboard(self):
        try:
            current_clipboard = pyperclip.paste()
            if not self.clipboard_history or current_clipboard != self.clipboard_history[-1]:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                entry = f"{timestamp}: {current_clipboard}"
                self.clipboard_history.append(current_clipboard)
                self.history_listbox.insert(tk.END, entry)
        except pyperclip.PyperclipException:
            messagebox.showerror("Clipboard Error", "Failed to access the clipboard")

        self.root.after(1000, self.check_clipboard)

    def copy_selected(self):
        try:
            selected_index = self.history_listbox.curselection()
            if selected_index:
                selected_text = self.clipboard_history[selected_index[0]]
                pyperclip.copy(selected_text)
                messagebox.showinfo("Clipboard Manager", "Text copied to clipboard")
            else:
                messagebox.showwarning("Clipboard Manager", "No item selected")
        except pyperclip.PyperclipException:
            messagebox.showerror("Clipboard Error", "Failed to copy to the clipboard")

    def clear_history(self):
        self.clipboard_history.clear()
        self.history_listbox.delete(0, tk.END)
        messagebox.showinfo("Clipboard Manager", "Clipboard history cleared")

if __name__ == "__main__":
    root = tk.Tk()
    app = ClipboardManager(root)
    root.mainloop()
