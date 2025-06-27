import dearpygui.dearpygui as dpg
from .styles import apply_dark_theme, toggle_theme
from .dialogs import show_splash, show_login, show_new_note_dialog, show_settings_dialog

def run_app(master_key):
    dpg.create_context()
    dpg.create_viewport(title='Secure Notes', width=800, height=600)
    dpg.setup_dearpygui()
    apply_dark_theme()

    def on_login_success(username):
        print(f"✅ on_login_success called with: {username}")
        dpg.delete_item("Login")

        with dpg.window(tag="Main Window", width=800, height=600):
            dpg.add_text(f"Hello, {username}!", color=[200, 200, 100])
            dpg.add_separator()

            with dpg.group(horizontal=True):
                with dpg.child_window(tag="Sidebar", width=200, height=-1):
                    dpg.add_text("Your Notes:")
                    dpg.add_listbox(tag="##note_list", items=[], width=180, num_items=15)

                with dpg.child_window(tag="MainPanel", width=-1, height=-1):
                    dpg.add_text("Select a note or create a new one from the File menu.")

        # Menu bar
        with dpg.viewport_menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="New Note", callback=show_new_note_dialog)
                dpg.add_menu_item(label="Settings", callback=show_settings_dialog)
                dpg.add_menu_item(label="Exit", callback=lambda: dpg.stop_dearpygui())
            with dpg.menu(label="View"):
                dpg.add_menu_item(label="Toggle Theme", callback=toggle_theme)

        dpg.set_primary_window("Main Window", True)

    def on_splash_done(username):
        print("🎬 Splash submitted")
        dpg.delete_item("Splash")
        on_login_success(username)

    show_splash(on_splash_done)
    print("🎬 Splash shown")

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


