from pathlib import Path
import io
import PySimpleGUI as sg
from PIL import Image
import configparser

"""
Formats: JPG, PNG, GIF, SVG, BMP, EPS, PSD, TIFF and WEBP
Current: JPG, PNG
"""
# Function definitions for conversions

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
    img_window = sg.Window(img_title, img_layout, use_custom_titlebar=True)

    while True:
        event, values = img_window.read()
        print(event, values)
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break

    img_window.close()
    # sg.popup_no_titlebar(bio.getvalue())


def is_same_format(src_file, type):
    format_extensions = {
        "JPG": '.jpg',
        "PNG": '.png',
        "BMP": '.bmp',
        "TIFF": '.tiff',
        "WEBP": '.webp',
        "ICO": '.ico'
    }

    src_ext = Path(src_file).suffix
    print(src_ext, type, format_extensions[type], src_ext == format_extensions[type])
    return src_ext == format_extensions[type]


def convert_image(src_file, trg_folder, type):

    src_img = Image.open(src_file)
    trg_dir = Path()

    # If the target folder is not specified, save in source folder
    if trg_folder == None:
        trg_dir = Path(src_img).parent
    else:
        trg_dir = Path(trg_folder)

    file_name = Path(src_file).stem

    src_format = Path(src_file).suffix
    # JPG
    if src_format == ".png":
        if type == "JPG":
            rgb = src_img.convert('RGB')
            rgb.save(trg_dir / f"{file_name}.jpg")
            sg.popup_no_titlebar("File Converted!\n" + "Saved as " +  str(trg_dir) + "/" + file_name + ".jpg")
        elif type == "BMP":
            rgb = src_img.convert('RGB')
            rgb.save(trg_dir / f"{file_name}.bmp")
            sg.popup_no_titlebar("File Converted!\n" + "Saved as " +  str(trg_dir) + "/" + file_name + ".bmp")
        elif type == "TIFF":
            src_img.save(trg_dir / f"{file_name}.tiff", compression = "lzw")
            sg.popup_no_titlebar("File Converted!\n" + "Saved as " +  str(trg_dir) + "/" + file_name + ".tiff")
        else:
            sg.popup_no_titlebar("Under Development!")
    elif src_format in (".jpg", ".jpeg"):
        if type == "PNG":
            rgb.save(trg_dir / f"{file_name}.png")
            sg.popup_no_titlebar("File Converted!")
        elif type == "BMP":
            rgb = src_img.convert('RGB')
            rgb.save(trg_dir / f"{file_name}.bmp")
            sg.popup_no_titlebar("File Converted!\n" + "Saved as " +  str(trg_dir) + "/" + file_name + ".bmp")
        elif type == "TIFF":
            src_img.save(trg_dir / f"{file_name}.tiff")
            sg.popup_no_titlebar("File Converted!\n" + "Saved as " +  str(trg_dir) + "/" + file_name + ".tiff")
        else:
            sg.popup_no_titlebar("Under Development!")


# MAIN GUI WINDOW
def main_window():
    # img_types = (".png", ".jpg", "jpeg", ".tiff", ".tif", ".bmp") 
    img_types = (".png", ".jpg", "jpeg") 
    menu_def = [["File", ["Setting", "Theme", "---", "Exit"]],
                ["Help", ["About"]]]
    layout = [
        [sg.MenubarCustom(menu_def, tearoff=False)],
        [
            sg.Text("Convert to "), sg.Combo(['PNG', 'JPG', "BMP", "TIFF"], key="-TYPE-", readonly=True)],
        [
            sg.Text("Source File :", s=16, justification='right'),
            sg.Input(key="-IN-"),
            sg.FilesBrowse(file_types=(("Image Files " + str(img_types), img_types),))],
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
    window = sg.Window(title, layout, use_custom_titlebar=True)
    

    while True:
        event, values = window.read()
        print(event, values)
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break
        if event == "About":
            sg.popup(title, "Version 1.0",
                     "Image Converter", grab_anywhere=True)
        # View image
        if event == "View Image":
            window['-STATUS-'].update("")
            if is_path_valid(values["-IN-"]):
                view_img(values["-IN-"])
            else:
                window['-STATUS-'].update("Path/File doesnt exist")
        # Convert event
        if event == "Convert Image":
            window['-STATUS-'].update("")
            # Checks if the source is a valid path and the file exists
            if is_path_valid(values["-IN-"]):
                # Checks if the file and conversion format is same
                if not is_same_format(src_file=values["-IN-"], type=values["-TYPE-"]):
                    print("HERE")
                    convert_image(
                        src_file=values["-IN-"], trg_folder=values["-OUT-"], type=values["-TYPE-"])
                # TODO: Create a modal that promts the formats are same and if the user clicks yes convert else PASS
                else:
                    # convert_image(src_file=values["-IN-"], trg_folder=values["-OUT-"], type=values["-TYPE-"])
                    window['-STATUS-'].update("Same format Detected!")
            else:
                window['-STATUS-'].update("Path/File doesnt exist")
    window.close()

if __name__ == "__main__":
    CONFIG_PATH = Path.cwd()
    config = configparser.ConfigParser()
    # CHECKS IF CONFIG.INI IS PRESENT, IF NOT CREATES IT WITH DEFAULT SETTINGS!
    if not Path(CONFIG_PATH / 'config.ini').exists():
        config['GUI'] = {'title': 'PixelPlay', 'font_size': 10, 'font_family': 'consolas'}
        config.write(open('config.ini', 'w'))
    print(CONFIG_PATH)
    settings = sg.UserSettings(
        path=CONFIG_PATH, filename='config.ini', use_config_file=True, convert_bools_and_none=True
    )
    font_family = settings["GUI"]["font_family"]
    font_size = int(settings["GUI"]["font_size"])

    sg.set_options(font=(font_family, font_size))
    sg.theme("DarkGrey13")
    main_window()
