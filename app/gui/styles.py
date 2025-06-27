import dearpygui.dearpygui as dpg

dark_theme = None
light_theme = None
current_theme = None

def apply_dark_theme():
    global dark_theme, current_theme
    if not dark_theme:
        dark_theme = dpg.theme()
        with dark_theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (50, 50, 50), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (70, 70, 70), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (90, 90, 90), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255), category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
            with dpg.theme_component(dpg.mvText):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (200, 200, 200), category=dpg.mvThemeCat_Core)
    dpg.bind_theme(dark_theme)
    current_theme = dark_theme

def apply_light_theme():
    global light_theme, current_theme
    if not light_theme:
        light_theme = dpg.theme()
        with light_theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (200, 200, 200), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (220, 220, 220), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (180, 180, 180), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_Text, (10, 10, 10), category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
            with dpg.theme_component(dpg.mvText):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (20, 20, 20), category=dpg.mvThemeCat_Core)
    dpg.bind_theme(light_theme)
    current_theme = light_theme

def toggle_theme():
    if current_theme == dark_theme:
        apply_light_theme()
    else:
        apply_dark_theme()


