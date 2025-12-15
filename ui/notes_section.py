import customtkinter as ctk
from tkinter import messagebox
from customtkinter import CTkImage
from PIL import Image
from utils.database import add_note, get_notes, delete_note

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

class NotesSection:
    def __init__(self, root):
        self.root = root
        self.trash_icon = CTkImage(Image.open("assets/icons/trash.png"), size=(20, 20))
        self.notes = get_notes()
        self.create_notes_section()

    def create_notes_section(self):
        frame_notes = ctk.CTkFrame(self.root, fg_color=BG_PRIMARY, corner_radius=15)
        frame_notes.pack(fill="x", padx=10, pady=8)

        notes_container = ctk.CTkFrame(frame_notes, fg_color=BG_SECONDARY, corner_radius=20)
        notes_container.pack(fill="x", padx=12, pady=10)

        header = ctk.CTkFrame(notes_container, fg_color=BG_SECONDARY)
        header.pack(pady=(6, 4), padx=10, fill="x")

        self.note_title = ctk.CTkEntry(
            header,
            placeholder_text="Digite o título da anotação...",
            height=40,
            corner_radius=10,
            fg_color=BG_TERTIARY,
            text_color=TEXT_DARK,
            border_width=0,
            font=("Arial", 18, "bold")
        )
        self.note_title.pack(side="left", padx=6, fill="x", expand=True)

        ctk.CTkButton(
            header,
            text="Salvar",
            width=90,
            height=40,
            corner_radius=10,
            fg_color=BTN_PRIMARY,
            hover_color=BTN_PRIMARY_HOVER,
            text_color=TEXT_LIGHT,
            font=("Arial", 18, "bold"),
            command=self.save_note
        ).pack(side="left", padx=6)

        self.note_text = ctk.CTkTextbox(
            notes_container,
            height=80,
            corner_radius=20,
            fg_color=BG_TERTIARY,
            text_color=TEXT_MUTED,
            font=("Arial", 14)
        )
        self.note_text.pack(pady=(6, 8), padx=12, fill="x")

        self.placeholder_text = "Digite aqui sua anotação..."
        self.note_text.insert("1.0", self.placeholder_text)
        self.note_text.bind("<FocusIn>", self.clear_placeholder)
        self.note_text.bind("<FocusOut>", self.restore_placeholder)

        list_outer = ctk.CTkFrame(frame_notes, fg_color=BG_SECONDARY, corner_radius=20, height=160)
        list_outer.pack(fill="x", padx=12, pady=8)
        list_outer.pack_propagate(False)

        list_inner = ctk.CTkFrame(list_outer, fg_color=BG_SECONDARY, corner_radius=20)
        list_inner.pack(fill="both", expand=True, padx=6, pady=6)

        self.notes_list_frame = ctk.CTkScrollableFrame(
            list_inner,
            fg_color=BG_SECONDARY,
            corner_radius=0,
            scrollbar_fg_color=SCROLL_BG,
            scrollbar_button_color=SCROLL_THUMB,
            scrollbar_button_hover_color=SCROLL_THUMB_HOVER
        )
        self.notes_list_frame.pack(fill="both", expand=True)

        self.update_notes_list()

    def clear_placeholder(self, _):
        if self.note_text.get("1.0", "end-1c") == self.placeholder_text:
            self.note_text.delete("1.0", "end")
            self.note_text.configure(text_color=TEXT_DARK)

    def restore_placeholder(self, _):
        if not self.note_text.get("1.0", "end-1c").strip():
            self.note_text.insert("1.0", self.placeholder_text)
            self.note_text.configure(text_color=TEXT_MUTED)

    def save_note(self):
        title = self.note_title.get().strip()
        content = self.note_text.get("1.0", "end").strip()

        if not title or not content or content == self.placeholder_text:
            messagebox.showwarning("Aviso", "Digite um título e um conteúdo.")
            return

        add_note(title, content)
        self.notes = get_notes()
        self.note_title.delete(0, "end")
        self.note_text.delete("1.0", "end")
        self.restore_placeholder(None)
        self.update_notes_list()

    def update_notes_list(self):
        for widget in self.notes_list_frame.winfo_children():
            widget.destroy()

        if not self.notes:
            ctk.CTkLabel(
                self.notes_list_frame,
                text="Nenhuma nota",
                font=("Arial", 16, "bold"),
                text_color=TEXT_MUTED
            ).pack(expand=True)
            return

        for title in self.notes:
            card = ctk.CTkFrame(self.notes_list_frame, fg_color=BG_PRIMARY, corner_radius=15, height=55)
            card.pack(fill="x", pady=6, padx=8)
            card.pack_propagate(False)

            inner = ctk.CTkFrame(card, fg_color=BG_PRIMARY)
            inner.pack(fill="both", expand=True, padx=12)

            ctk.CTkLabel(
                inner,
                text=title,
                font=("Arial", 14, "bold"),
                text_color=TEXT_LIGHT
            ).pack(side="left")

            ctk.CTkButton(
                inner,
                image=self.trash_icon,
                width=34,
                height=34,
                corner_radius=8,
                fg_color=BTN_DANGER,
                hover_color=BTN_DANGER_HOVER,
                text="",
                command=lambda t=title: self.delete_note(t)
            ).pack(side="right", padx=5)

            ctk.CTkButton(
                inner,
                text="Abrir",
                width=70,
                height=34,
                corner_radius=8,
                fg_color=BTN_PRIMARY,
                hover_color=BTN_PRIMARY_HOVER,
                text_color=TEXT_LIGHT,
                command=lambda t=title: self.open_note(t)
            ).pack(side="right", padx=5)

    def open_note(self, title):
        popup = ctk.CTkToplevel(self.root)
        popup.title(title)
        popup.geometry("420x300")
        popup.resizable(False, False)
        popup.grab_set()

        frame = ctk.CTkFrame(popup, fg_color=BG_PRIMARY, corner_radius=15)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            frame,
            text=title,
            font=("Arial", 18, "bold"),
            text_color=TEXT_LIGHT
        ).pack(pady=(10, 5))

        box = ctk.CTkTextbox(
            frame,
            height=160,
            corner_radius=10,
            fg_color=BG_SECONDARY,
            text_color=TEXT_DARK,
            font=("Arial", 14)
        )
        box.insert("1.0", self.notes[title])
        box.configure(state="disabled")
        box.pack(padx=10, pady=8, fill="x")

        ctk.CTkButton(
            frame,
            text="FECHAR",
            height=40,
            corner_radius=10,
            fg_color=BTN_DANGER,
            hover_color=BTN_DANGER_HOVER,
            font=("Arial", 14, "bold"),
            command=popup.destroy
        ).pack(padx=10, pady=10, fill="x")

    def delete_note(self, title):
        delete_note(title)
        self.notes = get_notes()
        self.update_notes_list()