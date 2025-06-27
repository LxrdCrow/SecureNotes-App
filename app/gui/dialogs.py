# app/gui/dialogs.py

import dearpygui.dearpygui as dpg

def show_splash(on_submit):
    with dpg.window(label="Welcome", tag="Splash", modal=True, no_title_bar=True, width=400, height=300):
        username_input = dpg.add_input_text(label="Enter your name", tag="username_input")
        dpg.add_button(label="Submit", callback=lambda: on_submit(dpg.get_value("username_input")))


def show_login(on_login_success):
    with dpg.window(label="Login", modal=True, no_title_bar=True, width=400, height=300):
        dpg.add_text("🔑 Login to Secure Notes", bullet=True)
        username_var = dpg.add_input_text(label="Username")
        password_var = dpg.add_input_text(label="Password", password=True)
        dpg.add_button(label="Login", callback=lambda: on_login_success(dpg.get_value(username_var)))

        dpg.add_same_line()
        dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item("Login"))

def show_new_note_dialog(on_note_created):
    with dpg.window(label="New Note", modal=True, no_title_bar=True, width=400, height=300):
        dpg.add_text("📝 Create a New Note", bullet=True)
        title_var = dpg.add_input_text(label="Title")
        content_var = dpg.add_input_text(label="Content", multiline=True)
        dpg.add_button(label="Create", callback=lambda: on_note_created(dpg.get_value(title_var), dpg.get_value(content_var)))

        dpg.add_same_line()
        dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item("New Note"))


def show_settings_dialog(on_settings_saved):
    with dpg.window(label="Settings", modal=True, no_title_bar=True, width=400, height=300):
        dpg.add_text("⚙️ Settings", bullet=True)
        theme_var = dpg.add_combo(label="Theme", items=["Dark", "Light"], default_value="Dark")
        dpg.add_button(label="Save", callback=lambda: on_settings_saved(dpg.get_value(theme_var)))

        dpg.add_same_line()
        dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item("Settings"))
        
def show_error_dialog(message):
    with dpg.window(label="Error", modal=True, no_title_bar=True, width=400, height=200):
        dpg.add_text(f"❗ Error: {message}", bullet=True)
        dpg.add_button(label="OK", callback=lambda: dpg.delete_item("Error"))