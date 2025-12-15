import customtkinter as ctk
from PIL import Image, ImageTk
from ui.notes_section import NotesSection
from ui.todo_section import TodoSection
from utils.database import create_tables

class NotesApp:

    def __init__(self, root):
        self.root = root
        self.root.title("MindList")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.notes_section = NotesSection(root)
        self.todo_section = TodoSection(root)

if __name__ == "__main__":
    create_tables()

    root = ctk.CTk()

    root.iconbitmap("assets/icons/mind.ico")

    app = NotesApp(root)
    root.geometry("900x750")
    root.minsize(800, 600)
    root.maxsize(800, 600)
    root.mainloop()