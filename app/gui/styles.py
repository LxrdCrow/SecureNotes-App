import dearpygui.dearpygui as dpg

dark_theme = None
light_theme = None

def init_themes():
    global dark_theme, light_theme

    # 🌙 Tema scuro – Blu Notte
    dark_theme = dpg.add_theme()
    # Applichiamo il tema a **tutti** gli elementi…
    with dpg.theme_component(dpg.mvAll, parent=dark_theme):
        # …ma aggiungiamo colori specifici per la Menu Bar
        dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (20, 30, 45), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (50, 75, 105), category=dpg.mvThemeCat_Core)

        # Sfondo principale, finestre, popup
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (13, 27, 42), category=dpg.mvThemeCat_Core)        # #0D1B2A
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (27, 38, 59), category=dpg.mvThemeCat_Core)         # #1B263B
        dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (27, 38, 59), category=dpg.mvThemeCat_Core)

        # Testi
        dpg.add_theme_color(dpg.mvThemeCol_Text, (240, 248, 255), category=dpg.mvThemeCat_Core)         # AliceBlue

        # Bottoni
        dpg.add_theme_color(dpg.mvThemeCol_Button, (27, 38, 59), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (41, 54, 74), category=dpg.mvThemeCat_Core)

        # Frame (input/textarea)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (20, 30, 45), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (30, 45, 65), category=dpg.mvThemeCat_Core)

        # Header (espansioni, collapser)
        dpg.add_theme_color(dpg.mvThemeCol_Header, (30, 45, 65), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (40, 60, 85), category=dpg.mvThemeCat_Core)

        # Scrollbar
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (20, 30, 45), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (40, 60, 85), category=dpg.mvThemeCat_Core)

        # Bordi
        dpg.add_theme_color(dpg.mvThemeCol_Border, (50, 75, 105), category=dpg.mvThemeCat_Core)


        # ☀️ Tema chiaro – Beige elegante
    light_theme = dpg.add_theme()
    with dpg.theme_component(dpg.mvAll, parent=light_theme):
        # Sfondo principale e popup
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (245, 245, 220), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg,  (255, 250, 240), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_PopupBg,  (255, 250, 240), category=dpg.mvThemeCat_Core)
        # – RIMOSSO mvThemeCol_ModalWindowDarkening
        # – RIMOSSO mvThemeCol_MenuBg

        # Barra dei menu
        dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (245, 235, 220), category=dpg.mvThemeCat_Core)

        # Titoli finestre
        dpg.add_theme_color(dpg.mvThemeCol_TitleBg,       (230, 220, 205), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (210, 200, 185), category=dpg.mvThemeCat_Core)

        # Testi e bottoni
        dpg.add_theme_color(dpg.mvThemeCol_Text,            (40, 40, 40), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button,          (220, 210, 190), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,   (200, 190, 170), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,    (180, 170, 150), category=dpg.mvThemeCat_Core)

        # Frame e header
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg,         (245, 235, 220), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Header,          (230, 220, 205), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered,   (210, 200, 185), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_HeaderActive,    (190, 180, 165), category=dpg.mvThemeCat_Core)

        # Scrollbar
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg,        (230, 220, 205), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab,      (190, 180, 165), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered,
                                                        (170, 160, 145), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive,
                                                        (150, 140, 125), category=dpg.mvThemeCat_Core)

        # Bordo generale
        dpg.add_theme_color(dpg.mvThemeCol_Border,            (160, 150, 135), category=dpg.mvThemeCat_Core)





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
    current = dpg.get_theme()
    if current == dark_theme:
        apply_light_theme()
    else:
        apply_dark_theme()


