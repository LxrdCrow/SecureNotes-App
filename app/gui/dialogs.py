# app/gui/dialogs.py

import dearpygui.dearpygui as dpg

def center_window(tag: str, width: int, height: int, offset_x: int = 200, offset_y: int = 100):
    if not dpg.does_item_exist(tag):
        return
    vw = dpg.get_viewport_client_width()
    vh = dpg.get_viewport_client_height()
    x = (vw - width) // 2 + offset_x
    y = (vh - height) // 2 + offset_y
    dpg.set_item_pos(tag, [x, y])

def show_splash(on_submit):
    tag, w, h = "Splash", 700, 600
    if dpg.does_item_exist(tag):
        dpg.delete_item(tag)

    def _submit():
        username = dpg.get_value("splash_username") or ""
        master_key = dpg.get_value("splash_master_key") or ""
        if not master_key.strip():
            show_error_dialog("You must enter a Master Key to continue.")
            return
        on_submit(username, master_key)

    with dpg.window(label="Welcome", tag=tag, modal=True, no_title_bar=True,
                    no_resize=True, width=w, height=h, pos=[200,100]):
        dpg.add_spacer(height=20)
        dpg.add_text("Welcome to Secure Notes", bullet=True, wrap=350)
        dpg.add_spacer(height=10)
        dpg.add_text("Enter your name:", color=[200,200,200])
        dpg.add_input_text(tag="splash_username", width=w-100)
        dpg.add_spacer(height=10)
        dpg.add_text("Enter your Master Key:", color=[200,200,200])
        dpg.add_input_text(tag="splash_master_key", password=True, width=w-100)
        dpg.add_spacer(height=20)
        dpg.add_text("This key is used to encrypt your notes.", color=[200,200,200])
        dpg.add_text("Make sure to remember it!", color=[200,200,200])
        dpg.add_spacer(height=10)
        dpg.add_text("Note: If you lose your Master Key, you will not be able to access your notes.", color=[255,0,0])
        dpg.add_spacer(height=20)
        with dpg.group(horizontal=True):
            dpg.add_button(label="Submit", width=100, callback=_submit)
            dpg.add_button(label="Exit",   width=100, callback=lambda: dpg.stop_dearpygui())

    if not dpg.does_item_exist("splash_enter_handler"):
        with dpg.handler_registry(tag="splash_enter_handler"):
            dpg.add_key_press_handler(dpg.mvKey_Return, callback=lambda: _submit())
            dpg.add_key_press_handler(dpg.mvKey_Escape, callback=lambda: dpg.stop_dearpygui())

    dpg.set_value("splash_username", "")
    dpg.set_value("splash_master_key", "")
    center_window(tag, w, h, offset_x=200, offset_y=50)
    dpg.show_item(tag)
    return tag


def show_new_note_dialog(on_note_created, default_max_reads: int):
    tag, w, h = "NewNote", 900, 900
    if dpg.does_item_exist(tag):
        dpg.delete_item(tag)

    def _submit():
        if not dpg.does_item_exist(tag) or not dpg.is_item_shown(tag):
            return
        on_note_created(
            dpg.get_value("newnote_title"),
            dpg.get_value("newnote_content"),
            dpg.get_value("newnote_max_reads") or None
        )

    with dpg.window(label="New Note", tag=tag, modal=True, no_title_bar=True,
                    no_resize=True, width=w, height=h, pos=[0,0]):
        dpg.add_text("Create a New Note", bullet=True)
        dpg.add_separator()
        dpg.add_spacer(height=10)

        dpg.add_input_text(label="Title", tag="newnote_title", width=w-80)
        dpg.add_spacer(height=10)
        dpg.add_input_text(label="Content", tag="newnote_content",
                           multiline=True, height=320, width=w-80)
        dpg.add_spacer(height=10)
        dpg.add_input_int(label="Max Reads", tag="newnote_max_reads",
                          default_value=default_max_reads,
                          min_value=1, max_value=100,
                          width=160)
        dpg.add_spacer(height=20)

        with dpg.group(horizontal=True):
            dpg.add_button(label="Create", width=160, callback=_submit)
            dpg.add_button(label="Cancel", width=160,
                           callback=lambda: dpg.delete_item(tag))

        dpg.add_spacer(height=10)
        dpg.add_button(label="Back to Menu", width=160,
                       callback=lambda: (dpg.delete_item(tag), dpg.show_item("Main Window")))

        dpg.focus_item("newnote_title")

    if not dpg.does_item_exist("newnote_enter_handler"):
        with dpg.handler_registry(tag="newnote_enter_handler"):
            dpg.add_key_press_handler(dpg.mvKey_Return, callback=lambda: _submit())
            dpg.add_key_press_handler(dpg.mvKey_Escape, callback=lambda: dpg.delete_item(tag))

    dpg.set_value("newnote_title", "")
    dpg.set_value("newnote_content", "")
    dpg.set_value("newnote_max_reads", default_max_reads)

    center_window(tag, w, h, offset_x=100, offset_y=50)
    dpg.show_item(tag)
    return tag


def show_settings_dialog(on_save, current_theme: str, auto_delete: bool, max_reads: int):
    tag, w, h = "Settings", 500, 350
    if dpg.does_item_exist(tag):
        dpg.delete_item(tag)

    with dpg.window(label="Settings", tag=tag, modal=True, no_title_bar=True,
                    no_resize=True, width=w, height=h, pos=[0,0]):
        dpg.add_text("Application Settings", bullet=True)
        dpg.add_separator()
        dpg.add_spacer(height=10)

        dpg.add_combo(label="Theme", items=["Dark","Light"],
                      default_value=current_theme, tag="settings_theme")
        dpg.add_spacer(height=10)

        dpg.add_checkbox(label="Enable Auto-Delete",
                         tag="settings_auto_delete",
                         default_value=auto_delete)
        dpg.add_spacer(height=10)

        dpg.add_text("Default Max Reads Before Deletion:")
        dpg.add_input_int(label="", tag="settings_max_reads",
                          default_value=max_reads, min_value=1, max_value=100)
        dpg.add_spacer(height=20)

        with dpg.group(horizontal=True):
            dpg.add_button(label="Save", width=100,
                callback=lambda: (
                    on_save(
                        dpg.get_value("settings_theme"),
                        dpg.get_value("settings_auto_delete"),
                        dpg.get_value("settings_max_reads"),
                        None
                    ),
                    dpg.delete_item(tag)
                ))
            dpg.add_button(label="Cancel", width=100,
                           callback=lambda: dpg.delete_item(tag))

    center_window(tag, w, h, offset_x=100, offset_y=50)
    dpg.show_item(tag)
    return tag


def show_error_dialog(message: str = "An error has occurred.."):
    tag, w, h = "ErrorDialog", 400, 150
    if dpg.does_item_exist(tag):
        dpg.delete_item(tag)

    with dpg.window(label="Errore", tag=tag, modal=True,
                    no_title_bar=True, no_resize=True,
                    width=w, height=h):
        dpg.add_text("Error:", color=[255,0,0])
        dpg.add_text(message, wrap=350)
        dpg.add_spacer(height=20)
        dpg.add_button(label="OK", width=100, callback=lambda: dpg.delete_item(tag))

    center_window(tag, w, h, offset_x=150, offset_y=60)
    dpg.show_item(tag)
    return tag

