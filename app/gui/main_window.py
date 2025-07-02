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

MAX_READS = 5
DATA_FILE = "notes_data.json"

def run_app():
    dpg.create_context()
    dpg.create_viewport(title="Secure Notes", width=900, height=700)
    dpg.setup_dearpygui()
    init_themes()

    app_state = {
        "username": None,
        "master_key": None,
        "notes": []  # ogni nota: {"title": str, "content_encrypted": str, "read_count": int}
    }

    # --- STORAGE ---
    def save_notes():
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(app_state["notes"], f)
        except Exception as e:
            print(f"Errore salvataggio note: {e}")

    def load_notes():
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    app_state["notes"] = json.load(f)
            except Exception:
                app_state["notes"] = []
        else:
            app_state["notes"] = []

    # --- UI LOGICA ---
    def update_note_list():
        if not dpg.does_item_exist("note_list"):
            return
        key = generate_key_from_password(app_state["master_key"])
        titles = []
        for note in app_state["notes"]:
            try:
                titles.append(decrypt_note(note["title"], key))
            except Exception:
                titles.append("<errore>")
        dpg.configure_item("note_list", items=titles)

    def find_note_by_title(title: str):
        key = generate_key_from_password(app_state["master_key"])
        for note in app_state["notes"]:
            try:
                if decrypt_note(note["title"], key) == title:
                    return note
            except Exception:
                continue
        return None

    def on_note_selected(_, title):
        if not title:
            return
        note = find_note_by_title(title)
        if not note:
            dpg.set_value("note_display", "Errore: nota non trovata.")
            return

        # incremento letture e controllo auto-eliminazione
        note["read_count"] = note.get("read_count", 0) + 1
        if note["read_count"] > MAX_READS:
            app_state["notes"].remove(note)
            update_note_list()
            dpg.set_value("note_display", f"Nota eliminata dopo {MAX_READS} letture.")
            save_notes()
            return

        # decrittazione del contenuto
        try:
            content = decrypt_note(
                note["content_encrypted"],
                generate_key_from_password(app_state["master_key"])
            )
        except Exception:
            content = "<errore decrittazione>"
        dpg.set_value("note_display", f"Titolo: {title}\n\n{content}")
        save_notes()

    def on_note_created(title: str, content: str):
        key = generate_key_from_password(app_state["master_key"])
        # verifica duplicati
        for note in app_state["notes"]:
            try:
                if decrypt_note(note["title"], key) == title:
                    show_error_dialog("Titolo già esistente.")
                    return
            except Exception:
                pass

        # cifro titolo e contenuto
        enc_title   = encrypt_note(title, key)
        enc_content = encrypt_note(content, key)

        app_state["notes"].append({
            "title":             enc_title,
            "content_encrypted": enc_content,
            "read_count":        0
        })

        if dpg.does_item_exist("NewNote"):
            dpg.delete_item("NewNote")
        update_note_list()
        save_notes()

    def delete_note():
        title = dpg.get_value("note_list")
        if not title:
            show_error_dialog("Seleziona una nota.")
            return
        note = find_note_by_title(title)
        if not note:
            show_error_dialog("Nota non trovata.")
            return
        app_state["notes"].remove(note)
        update_note_list()
        dpg.set_value("note_display", "Nota eliminata.")
        save_notes()

    def on_settings_saved(theme: str):
        if theme == "Dark":
            apply_dark_theme()
        else:
            apply_light_theme()
        if dpg.does_item_exist("Settings"):
            dpg.delete_item("Settings")

    def create_main_window(user: str):
        if dpg.does_item_exist("Main Window"):
            dpg.delete_item("Main Window")

        with dpg.window(
            tag="Main Window",
            width=900,
            height=700,
            no_title_bar=False,
            show=True
        ):
            with dpg.menu_bar():
                with dpg.menu(label="File"):
                    dpg.add_menu_item(label="New Note",
                                      callback=lambda: show_new_note_dialog(on_note_created))
                    dpg.add_menu_item(label="Settings",
                                      callback=lambda: show_settings_dialog(on_settings_saved))
                    dpg.add_menu_item(label="Exit",
                                      callback=lambda: (save_notes(), dpg.stop_dearpygui()))

            dpg.add_text(f"Benvenuto, {user}!", color=[200, 200, 100])
            dpg.add_separator()

            with dpg.group(horizontal=True):
                with dpg.child_window(tag="Sidebar", width=250, height=-1):
                    dpg.add_text("Le tue Note:")
                    dpg.add_listbox(
                        tag="note_list",
                        items=[],
                        width=230,
                        num_items=15,
                        callback=on_note_selected
                    )
                    dpg.add_button(label="Delete Note", callback=delete_note, width=230)

                with dpg.child_window(tag="MainPanel", width=-1, height=-1):
                    dpg.add_text("Nota selezionata:")
                    dpg.add_input_text(
                        tag="note_display",
                        multiline=True,
                        readonly=True,
                        width=-1,
                        height=500
                    )

        dpg.set_primary_window("Main Window", True)
        dpg.split_frame(delay=1)
        dpg.focus_item("Main Window")

    def on_splash_done(user: str, mk: str):
        app_state["username"]   = user
        app_state["master_key"] = mk

        load_notes()
        if dpg.does_item_exist("Splash"):
            dpg.delete_item("Splash")

        create_main_window(user)  # crea la finestra e il widget note_list
        update_note_list()        # quindi popola la listbox

    # mostra la splash e parte tutto
    dpg.set_frame_callback(1, lambda: show_splash(on_splash_done))
    dpg.show_viewport()
    dpg.start_dearpygui()
    save_notes()
    dpg.destroy_context()





