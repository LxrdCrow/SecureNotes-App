import dearpygui.dearpygui as dpg
from .styles import init_themes, apply_dark_theme, apply_light_theme, toggle_theme
from .dialogs import (
    show_splash,
    show_new_note_dialog,
    show_settings_dialog,
    show_error_dialog
)

def run_app():
    """Avvia l'applicazione senza bisogno di master key esterna"""
    dpg.create_context()
    
    # Configura il viewport
    dpg.create_viewport(title='Secure Notes', width=900, height=700)
    dpg.setup_dearpygui()
    
    # Inizializza i temi
    init_themes()
    
    # Variabile per memorizzare i dati utente
    app_state = {
        "username": None,
        "master_key": None
    }

    # Funzione per gestire la creazione di una nuova nota
    def on_note_created(title, content):
        print(f"Nota creata: Titolo='{title}', Contenuto='{content}'")
        if dpg.does_item_exist("NewNote"):
            dpg.delete_item("NewNote")

    # Funzione per gestire salvataggio impostazioni
    def on_settings_saved(theme):
        print(f"🎨 Tema selezionato: {theme}")
        if theme == "Dark":
            apply_dark_theme()
        else:
            apply_light_theme()
        if dpg.does_item_exist("Settings"):
            dpg.delete_item("Settings")

    # Funzione per creare la finestra principale
    def create_main_window(username):
        # Elimina eventuale finestra principale esistente
        if dpg.does_item_exist("Main Window"):
            dpg.delete_item("Main Window")
        
        # Crea la finestra principale
        with dpg.window(tag="Main Window", width=900, height=700, no_title_bar=False, show=True):
            dpg.add_text(f"Benvenuto, {username}!", tag="username_text", color=[200, 200, 100])
            dpg.add_separator()

            with dpg.group(horizontal=True):
                with dpg.child_window(tag="Sidebar", width=250, height=-1):
                    dpg.add_text("Le tue Note:")
                    dpg.add_listbox(tag="note_list", items=[], width=230, num_items=15)

                with dpg.child_window(tag="MainPanel", width=-1, height=-1):
                    dpg.add_text("Seleziona una nota o crea una nuova dal menu File.")

        # Barra menu con funzioni
        with dpg.viewport_menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="New Note", callback=lambda: show_new_note_dialog(on_note_created))
                dpg.add_menu_item(label="Settings", callback=lambda: show_settings_dialog(on_settings_saved))
                dpg.add_menu_item(label="Exit", callback=lambda: dpg.stop_dearpygui())
            with dpg.menu(label="View"):
                dpg.add_menu_item(label="Toggle Theme", callback=toggle_theme)

        dpg.set_primary_window("Main Window", True)
        dpg.split_frame(delay=2)  # Forza un refresh
        dpg.focus_item("Main Window")
        print(f"Finestra principale creata per {username}")

    # Callback dopo splash (ora riceve sia username che master key)
    def on_splash_done(username, master_key):
        print(f"🎬 Login completato: username={username}")
        print(f"🔑 Master key inserita: {master_key}")
        
        # QUI VA LA TUA LOGICA DI VERIFICA MASTER KEY
        # Esempio: se la master key è "Morsmordre"
        if master_key == "Morsmordre":
            print("✅ Master key verificata con successo")
            app_state["username"] = username
            app_state["master_key"] = master_key
            
            # Chiudi la splash screen
            if dpg.does_item_exist("Splash"):
                dpg.delete_item("Splash")
            
            # Aspetta un frame prima di creare la finestra principale
            dpg.split_frame(delay=1)
            create_main_window(username)
        else:
            print("❌ Master key non valida")
            show_error_dialog("Master key non valida. Riprova.")
            # Non chiudere la finestra, permette di riprovare
            # Reimposta i campi per un nuovo tentativo
            dpg.set_value("splash_username", "")
            dpg.set_value("splash_master_key", "")

    # Mostra la splash screen con un piccolo ritardo
    def show_initial_screen():
        show_splash(on_splash_done)
    
    dpg.set_frame_callback(1, show_initial_screen)
    
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()