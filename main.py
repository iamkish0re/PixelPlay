from pathlib import Path

import PySimpleGUI as sg
from PIL import Image

def is_path_valid(path):
    if path and Path(path).exists():
        True
    sg.popup_error("Please check the File Paths!")
    False

def view_img(src_file):
    image = sg.Image(src_file)
    sg.popup_no_titlebar(image)

def convert_png_to_jpg(src_file, trg_folder):
    src_img = Image.open(src_file)
    
    file_name = Path(src_file).stem
    output_file = Path(trg_folder) / f"{file_name}.jpg"
    #The image object is used to save the image in jpg format
    rgb = src.convert('RGB')
    rgb.save(output_file)
    sg.popup_no_titlebar("File Converted!")


layout = [
    # [sg.Image("C:/Users/kisho/Desktop/convert.jpg")],
    [sg.Text("Source File     :"), sg.Input(key="-IN-"), sg.FileBrowse(file_types=(("Image Files", "*.*"),))],
    [sg.Text("Target Folder  :"), sg.Input(key="-OUT-"), sg.FolderBrowse()],
    [sg.Exit(), 
    # sg.Button("View Image"), 
    sg.Button("Convert Image")]
]

window = sg.Window("PixelPlay", layout)

while True:
    event, values = window.read()
    print(event, values)
    if event in (sg.WINDOW_CLOSED, "Exit"):
        break
    if event == "View Image":
        if is_path_valid(values["-IN-"]):
            view_img(values["-IN-"])
    if event == "Convert Image":
        if is_path_valid(values["-IN-"]) and is_path_valid(values["-OUT-"]):
            convert_png_to_jpg(src=values["-IN-"], trg=values["-OUT-"])
    
    
window.close()