from pathlib import Path
import io
import PySimpleGUI as sg
from PIL import Image

def is_path_valid(path):
    if path and Path(path).exists():
        return True
    return False

def view_img(src_file):
    src_img = Image.open(src_file)
    src_img.thumbnail((800, 800))

    bio = io.BytesIO()
    src_img.save(bio, format="PNG")

    img_layout = [
        [sg.Image(data=bio.getvalue(), key="-IMG-")],
    ]
    img_title = src_file
    img_window = sg.Window(img_title, img_layout, use_custom_titlebar = True)

    while True:
        event, values = img_window.read()
        print(event, values)
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break        
        
    img_window.close()
    # sg.popup_no_titlebar(bio.getvalue())

def convert_image(src_file, trg_folder, type):
    src_img = Image.open(src_file)
    trg_dir = Path()
    if trg_folder == None:
        trg_dir = Path(src_img).parent
    else:
        trg_dir = Path(trg_folder)
    file_name = Path(src_file).stem

    output_file = trg_dir / f"{file_name}.jpg"
    
    # PNG TO JPG
    rgb = src_img.convert('RGB')
    rgb.save(output_file)
    sg.popup_no_titlebar("File Converted!")

def main_window():
    menu_def = [["File", ["Setting", "Theme", "---", "Exit"]],
                ["Help", ["About"]]]
    layout = [
        [sg.MenubarCustom(menu_def, tearoff=False)],
        [sg.Text("Convert to "), sg.Combo(['PNG', 'JPG', "PDF"], key="-TYPE-")],
        [
            sg.Text("Source File :", s=16, justification='right'), 
            sg.Input(key="-IN-"), 
            sg.FileBrowse(file_types=(("Image Files", "*.*"),))],
        [
            sg.Text("Target Folder :", s=16, justification='right'), 
            sg.Input(key="-OUT-"), 
            sg.FolderBrowse()],
        [
            sg.Button("View Image"), 
            sg.Button("Convert Image")],
        [sg.HorizontalSeparator()],
        [
            sg.Text("", key="-STATUS-"),
        ]
    ]
    title = settings["GUI"]["title"]
    window = sg.Window(title, layout, use_custom_titlebar = True)

    while True:
        event, values = window.read()
        print(event, values)
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break
        if event == "About":
            sg.popup(title, "Version 1.0", "Image Converter", grab_anywhere=True)
        if event == "View Image":
            window['-STATUS-'].update("")
            if is_path_valid(values["-IN-"]):
                view_img(values["-IN-"])
            else:
                window['-STATUS-'].update("Path/File doesnt exist")
        if event == "Convert Image":
            window['-STATUS-'].update("")
            if is_path_valid(values["-IN-"]):
                convert_image(src_file=values["-IN-"], trg_folder=values["-OUT-"], type=values["-TYPE-"])
            else:
                window['-STATUS-'].update("Path/File doesnt exist")
    window.close()

if __name__ == "__main__":
    CONFIG_PATH = Path.cwd()
    print(CONFIG_PATH)
    settings = sg.UserSettings(
        path = CONFIG_PATH, filename = 'config.ini', use_config_file = True, convert_bools_and_none = True
    )
    font_family = settings["GUI"]["font_family"]
    font_size = int(settings["GUI"]["font_size"])

    sg.set_options(font=(font_family, font_size))
    main_window()