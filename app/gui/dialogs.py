# app/gui/dialogs.py

import dearpygui.dearpygui as dpg

def center_window(tag: str, width: int, height: int, offset_x: int = 200, offset_y: int = 100):
    """
    Centra la finestra indicata dal tag e poi applica un offset in px.
    offset_x: quanto spostarla verso destra dopo il centraggio
    offset_y: quanto spostarla verso il basso dopo il centraggio
    """
    if not dpg.does_item_exist(tag):
        return

    # Dimensioni del viewport (area client)
    viewport_w = dpg.get_viewport_client_width()
    viewport_h = dpg.get_viewport_client_height()

    # Calcolo posizione centrale
    x = (viewport_w - width) // 2 + offset_x
    y = (viewport_h - height) // 2 + offset_y

    dpg.set_item_pos(tag, [x, y])


def show_splash(on_submit):
    tag = "Splash"
    width, height = 800, 650

    if dpg.does_item_exist(tag):
        dpg.delete_item(tag)

    with dpg.window(label="Welcome",
                    tag=tag,
                    modal=True,
                    no_title_bar=True,
                    no_resize=True,
                    width=width,
                    height=height,
                    pos=[200, 100]):  # oppure pos=[0, 0] e poi center_window()
        
        dpg.add_spacer(height=20)
        dpg.add_text("Welcome to Secure Notes", bullet=True, wrap=350)
        dpg.add_spacer(height=10)
        dpg.add_text("Enter your name:", color=[200, 200, 200])
        dpg.add_input_text(tag="splash_username", width=width-100)
        dpg.add_spacer(height=10)
        dpg.add_text("Enter your master key:", color=[200, 200, 200])
        dpg.add_input_text(tag="splash_master_key", password=True, width=width-100)
        dpg.add_spacer(height=20)

        # Pulsanti
        with dpg.group(horizontal=True):
            dpg.add_button(label="Submit", width=100,
                callback=lambda: on_submit(
                    dpg.get_value("splash_username"),
                    dpg.get_value("splash_master_key")
                ))
            dpg.add_button(label="Exit", width=100,
                callback=lambda: dpg.stop_dearpygui())
        

    # 🔥 Handler per i tasti
    with dpg.handler_registry():
        dpg.add_key_press_handler(dpg.mvKey_Return, callback=lambda: on_submit(
            dpg.get_value("splash_username"),
            dpg.get_value("splash_master_key")
        ))
        dpg.add_key_press_handler(dpg.mvKey_Escape, callback=lambda: dpg.stop_dearpygui())

    dpg.set_value("splash_username", "")
    dpg.set_value("splash_master_key", "")
    center_window(tag, width, height, offset_x=200, offset_y=50)
    dpg.show_item(tag)

    return tag


def show_new_note_dialog(on_note_created):
    tag = "NewNote"
    width, height = 500, 450

    if dpg.does_item_exist(tag):
        dpg.delete_item(tag)

    with dpg.window(label="New Note",
                    tag=tag,
                    modal=True,
                    no_title_bar=True,
                    no_resize=True,
                    width=width,
                    height=height,
                    pos=[0, 0]):
        dpg.add_text("Create a New Note", bullet=True)
        dpg.add_separator()
        dpg.add_input_text(label="Title", tag="newnote_title")
        dpg.add_input_text(label="Content", multiline=True, height=150, tag="newnote_content")
        dpg.add_spacer(height=10)
        with dpg.group(horizontal=True):
            dpg.add_button(label="Create", callback=lambda: on_note_created(
                dpg.get_value("newnote_title"),
                dpg.get_value("newnote_content")
            ))
            dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item(tag))
        dpg.add_spacer(height=10)
        dpg.add_button(label="← Back to Menu", callback=lambda: (
            dpg.delete_item(tag),
            dpg.show_item("Main Window")
        ))
    center_window(tag, width, height, offset_x=100, offset_y=50)
    dpg.set_value("newnote_title", "")
    dpg.set_value("newnote_content", "")
    dpg.show_item(tag)
    return tag


def show_settings_dialog(on_settings_saved):
    tag = "Settings"
    width, height = 500, 400

    if dpg.does_item_exist(tag):
        dpg.delete_item(tag)

    with dpg.window(label="Settings",
                    tag=tag,
                    modal=True,
                    no_title_bar=True,
                    no_resize=True,
                    width=width,
                    height=height,
                    pos=[0, 0]):
        dpg.add_text("Application Settings", bullet=True)
        dpg.add_separator()
        dpg.add_combo(label="Theme", items=["Dark", "Light"], default_value="Dark", tag="settings_theme")
        dpg.add_spacer(height=10)
        with dpg.group(horizontal=True):
            dpg.add_button(label="Save", callback=lambda: on_settings_saved(dpg.get_value("settings_theme")))
            dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item(tag))
        dpg.add_spacer(height=10)
        dpg.add_button(label="← Back to Menu", callback=lambda: (
            dpg.delete_item(tag),
            dpg.show_item("Main Window")
        ))
    center_window(tag, width, height, offset_x=100, offset_y=50)
    dpg.set_value("settings_theme", "Dark")
    dpg.show_item(tag)
    return tag


def show_error_dialog(message: str):
    tag = "Error"
    width, height = 500, 300

    if dpg.does_item_exist(tag):
        dpg.delete_item(tag)

    with dpg.window(label="Error",
                    tag=tag,
                    modal=True,
                    no_title_bar=True,
                    no_resize=True,
                    width=width,
                    height=height,
                    pos=[0, 0]):
        dpg.add_text(f"Error: {message}", bullet=True, wrap=350)
        dpg.add_spacer(height=20)
        dpg.add_button(label="OK", callback=lambda: dpg.delete_item(tag))
    center_window(tag, width, height, offset_x=100, offset_y=50)
    dpg.show_item(tag)
    return tag


