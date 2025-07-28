# app/gui/main_window.py

import dearpygui.dearpygui as dpg
import json
import os

from .styles import init_themes, apply_dark_theme, apply_light_theme
from .dialogs import (
    show_splash,
    show_new_note_dialog,
    show_settings_dialog,
    show_error_dialog
)
from .crypto_utils import encrypt_note, decrypt_note, generate_key_from_password

DATA_FILE = "notes_data.json"
SETTINGS_FILE = "settings.json"

def run_app():
    
    dpg.create_context()
    dpg.create_viewport(title="Secure Notes", width=900, height=700)
    dpg.setup_dearpygui()
    init_themes()

    
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            settings = json.load(f)
    else:
        settings = {
            "theme": "Dark",
            "auto_delete_enabled": True,
            "max_reads": 5
        }

    
    if settings["theme"] == "Dark":
        apply_dark_theme()
    else:
        apply_light_theme()

    
    app_state = {
        "username": None,
        "master_key": None,   
        "notes": [],     
        "auto_delete_enabled": settings["auto_delete_enabled"],
        "max_reads": settings["max_reads"]
    }

    
    def save_notes():
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(app_state["notes"], f, ensure_ascii=False, indent=2)


    def load_notes():
        if not os.path.exists(DATA_FILE):
            app_state["notes"] = []
            return

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                contents = f.read().strip()
                if contents:
                    app_state["notes"] = json.loads(contents)
                else:
                    app_state["notes"] = []
        except (json.JSONDecodeError, IOError):
            app_state["notes"] = []


    def save_settings():
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "theme": settings["theme"],
                "auto_delete_enabled": app_state["auto_delete_enabled"],
                "max_reads": app_state["max_reads"]
            }, f, ensure_ascii=False, indent=2)

    def update_note_list():
        if not dpg.does_item_exist("note_list"):
            return
        if not app_state["master_key"]:
            return

        items = []
        key = generate_key_from_password(app_state["master_key"])
        for note in app_state["notes"]:
            try:
                items.append(decrypt_note(note["title"], key))
            except:
                items.append("<errore>")
        dpg.configure_item("note_list", items=items)

    def on_note_selected(_, title):
        if not title:
            return

        key = generate_key_from_password(app_state["master_key"])
        for note in app_state["notes"]:
            try:
                if decrypt_note(note["title"], key) == title:
                    break
            except:
                continue
        else:
            dpg.set_value("note_display", "Error: note not found.")
            return

        limit = note.get("max_reads", app_state["max_reads"])
        if app_state["auto_delete_enabled"]:
            note["read_count"] = note.get("read_count", 0) + 1
            if note["read_count"] > limit:
                app_state["notes"].remove(note)
                save_notes()
                update_note_list()
                dpg.set_value("note_display", f"Note deleted after {limit} reads.")
                return

        try:
            body = decrypt_note(note["content_encrypted"], key)
        except:
            body = "<error decrypting content>"
        dpg.set_value("note_display", f"Title: {title}\n\n{body}")
        save_notes()

    def on_note_created(title, content, per_note_reads):
        if not app_state["master_key"]:
            show_error_dialog("You must enter a Master Key to continue.")
            return

        key = generate_key_from_password(app_state["master_key"])

        for note in app_state["notes"]:
            try:
                if decrypt_note(note["title"], key) == title:
                    show_error_dialog("Title already exists.")
                    return
            except:
                continue

        enc_t = encrypt_note(title, key)
        enc_c = encrypt_note(content, key)
        app_state["notes"].append({
            "title": enc_t,
            "content_encrypted": enc_c,
            "read_count": 0,
            "max_reads": per_note_reads or app_state["max_reads"]
        })
        save_notes()
        if dpg.does_item_exist("NewNote"):
            dpg.delete_item("NewNote")
        update_note_list()

    def delete_note():
        title = dpg.get_value("note_list") or ""
        if not title:
            show_error_dialog("Select a note to delete.")
            return

        key = generate_key_from_password(app_state["master_key"])
        for note in app_state["notes"]:
            try:
                if decrypt_note(note["title"], key) == title:
                    app_state["notes"].remove(note)
                    save_notes()
                    update_note_list()
                    dpg.set_value("note_display", "Note deleted.")
                    return
            except:
                continue

        show_error_dialog("Note not found.")

    def on_settings_saved(theme, auto_del, max_reads, _):
        settings["theme"] = theme
        if theme == "Dark":
            apply_dark_theme()
        else:
            apply_light_theme()
        app_state["auto_delete_enabled"] = auto_del
        if max_reads >= 1:
            app_state["max_reads"] = max_reads
        save_settings()

    def create_main_window(user):
        load_notes()
        if dpg.does_item_exist("Main Window"):
            dpg.delete_item("Main Window")

        with dpg.window(tag="Main Window", width=900, height=700, show=True):
            with dpg.menu_bar():
                with dpg.menu(label="File"):
                    dpg.add_menu_item(
                        label="New Note",
                        callback=lambda: show_new_note_dialog(
                            on_note_created,
                            app_state["max_reads"]
                        )
                    )
                    dpg.add_menu_item(
                        label="Settings",
                        callback=lambda: show_settings_dialog(
                            on_settings_saved,
                            settings["theme"],
                            app_state["auto_delete_enabled"],
                            app_state["max_reads"]
                        )
                    )
                    dpg.add_menu_item(
                        label="Exit",
                        callback=lambda: (save_notes(), dpg.stop_dearpygui())
                    )

            dpg.add_text(f"Welcome, {user}!", color=[200, 200, 100])
            dpg.add_separator()

            with dpg.group(horizontal=True):
                with dpg.child_window(tag="Sidebar", width=250, height=-1):
                    dpg.add_text("Your Notes:")
                    dpg.add_listbox(
                        tag="note_list",
                        items=[],
                        width=230, num_items=15,
                        callback=on_note_selected
                    )
                    dpg.add_button(
                        label="Delete Note",
                        callback=delete_note,
                        width=230
                    )

                with dpg.child_window(tag="MainPanel", width=-1, height=-1):
                    dpg.add_text("Note Content:")
                    dpg.add_input_text(
                        tag="note_display",
                        multiline=True,
                        readonly=True,
                        width=-1,
                        height=500
                    )

        dpg.set_primary_window("Main Window", True)
        update_note_list()

    def on_splash_done(user, mk):
        app_state["username"] = user
        app_state["master_key"] = mk
        dpg.delete_item("Splash")
        create_main_window(user)

    show_splash(on_splash_done)
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()



