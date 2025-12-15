import customtkinter as ctk
from tkinter import messagebox
from customtkinter import CTkImage
from PIL import Image
from utils.database import add_todo, get_todos, update_todo_done, delete_todo

BG_PRIMARY = "#97AAFF"
BG_SECONDARY = "#A9B7FF"
BG_TERTIARY = "#D3DBFF"

BTN_PRIMARY = "#6A85FF"
BTN_PRIMARY_HOVER = "#6B6EDB"

BTN_DANGER = "#FF6237"
BTN_DANGER_HOVER = "#E0552E"

SCROLL_BG = "#A9B7FF"
SCROLL_THUMB = "#6C87FF"
SCROLL_THUMB_HOVER = "#5A73E0"

TEXT_DARK = "black"
TEXT_LIGHT = "white"
TEXT_MUTED = "gray"

class TodoSection:
    def __init__(self, root):
        self.root = root
        self.trash_icon = CTkImage(Image.open("assets/icons/trash.png"), size=(20, 20))
        self.todos = get_todos()
        self.create_todo_section()

    def create_todo_section(self):
        frame_todo = ctk.CTkFrame(self.root, fg_color=BG_PRIMARY, corner_radius=15)
        frame_todo.pack(fill="both", expand=True, padx=20, pady=10)

        todo_container = ctk.CTkFrame(
            frame_todo,
            fg_color=BG_SECONDARY,
            corner_radius=20
        )
        todo_container.pack(fill="both", expand=True, padx=15, pady=15)

        self.todo_frame = ctk.CTkScrollableFrame(
            todo_container,
            fg_color=BG_SECONDARY,
            corner_radius=0,
            scrollbar_fg_color=SCROLL_BG,
            scrollbar_button_color=SCROLL_THUMB,
            scrollbar_button_hover_color=SCROLL_THUMB_HOVER
        )
        self.todo_frame.pack(side="left", fill="both", expand=True, padx=(10, 6), pady=10)

        add_container = ctk.CTkFrame(
            todo_container,
            fg_color=BG_PRIMARY,
            corner_radius=20,
            width=260
        )
        add_container.pack(side="right", fill="y", padx=(6, 10), pady=10)
        add_container.pack_propagate(False)

        self.entry_add = ctk.CTkEntry(
            add_container,
            placeholder_text="Digite sua tarefa aqui...",
            height=60,
            font=("Arial", 14),
            corner_radius=12,
            fg_color=BG_TERTIARY,
            text_color=TEXT_DARK,
            border_width=0
        )
        self.entry_add.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkButton(
            add_container,
            text="Salvar",
            height=60,
            corner_radius=15,
            fg_color=BTN_PRIMARY,
            hover_color=BTN_PRIMARY_HOVER,
            font=("Arial", 18, "bold"),
            text_color=TEXT_LIGHT,
            command=self.save_todo
        ).pack(fill="x", padx=20, pady=(0, 20))

        self.render_todos()

    def save_todo(self):
        task = self.entry_add.get().strip()
        if not task:
            messagebox.showwarning("Aviso", "Digite uma tarefa.")
            return

        add_todo(task)
        self.entry_add.delete(0, "end")
        self.todos = get_todos()
        self.render_todos()

    def toggle_todo(self, idx):
        todo = self.todos[idx]
        update_todo_done(todo["id"], not todo["done"])
        self.todos = get_todos()
        self.render_todos()

    def render_todos(self):
        for widget in self.todo_frame.winfo_children():
            widget.destroy()

        if not self.todos:
            ctk.CTkLabel(
                self.todo_frame,
                text="Nenhuma tarefa",
                font=("Arial", 16, "bold"),
                text_color=TEXT_MUTED
            ).pack(expand=True)
            return

        for i, todo in enumerate(self.todos):
            card = ctk.CTkFrame(
                self.todo_frame,
                fg_color=BG_PRIMARY,
                corner_radius=15,
                height=55
            )
            card.pack(fill="x", pady=6, padx=8)
            card.pack_propagate(False)

            chk = ctk.CTkCheckBox(
                card,
                text=todo["text"],
                variable=ctk.BooleanVar(value=todo["done"]),
                command=lambda idx=i: self.toggle_todo(idx),
                font=("Arial", 14, "bold"),
                text_color=TEXT_LIGHT,
                fg_color=BTN_PRIMARY,
                hover_color=BTN_PRIMARY_HOVER
            )
            chk.pack(side="left", padx=15, expand=True, anchor="w")

            ctk.CTkButton(
                card,
                image=self.trash_icon,
                width=36,
                height=36,
                corner_radius=10,
                fg_color=BTN_DANGER,
                hover_color=BTN_DANGER_HOVER,
                text="",
                command=lambda idx=i: self.delete_todo(idx)
            ).pack(side="right", padx=10)

    def delete_todo(self, idx):
        delete_todo(self.todos[idx]["id"])
        self.todos = get_todos()
        self.render_todos()