import dearpygui.dearpygui as dpg

# Variabili globali per i temi
dark_theme = None
light_theme = None

def init_themes():
    """Inizializza i temi una volta sola all'avvio dell'applicazione"""
    global dark_theme, light_theme
    
    # Crea tema scuro
    dark_theme = dpg.add_theme()
    with dpg.theme_component(dpg.mvAll, parent=dark_theme):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (30, 30, 30), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button, (50, 50, 50), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (70, 70, 70), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (90, 90, 90), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (40, 40, 40), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (60, 60, 60), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Header, (70, 70, 70), category=dpg.mvThemeCat_Core)
    
    # Crea tema chiaro
    light_theme = dpg.add_theme()
    with dpg.theme_component(dpg.mvAll, parent=light_theme):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (245, 245, 245), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text, (10, 10, 10), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button, (200, 200, 200), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (220, 220, 220), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (180, 180, 180), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (230, 230, 230), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (200, 200, 200), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Header, (210, 210, 210), category=dpg.mvThemeCat_Core)
    
    # Imposta il tema scuro come default
    dpg.bind_theme(dark_theme)

def apply_dark_theme():
    """Applica il tema scuro"""
    if dark_theme is None:
        init_themes()
    dpg.bind_theme(dark_theme)

def apply_light_theme():
    """Applica il tema chiaro"""
    if light_theme is None:
        init_themes()
    dpg.bind_theme(light_theme)

def toggle_theme():
    """Alterna tra tema scuro e chiaro"""
    current_theme = dpg.get_theme()
    
    if current_theme == dark_theme:
        apply_light_theme()
    else:
        apply_dark_theme()



