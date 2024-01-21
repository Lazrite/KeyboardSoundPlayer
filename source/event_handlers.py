# event_handlers.py

import tkinter as tk
import customtkinter as ctk
import threading
import business_logic as logic
from pynput import keyboard
from PIL import Image, ImageTk
import pystray
from pystray import MenuItem as item
from tkinter import filedialog
import ui_components as ui
import json
from pynput import mouse
import icon as ic
import base64
from io import BytesIO

root = None

def inithialize(root_param):
    global root
    root = root_param

def show_main_content():
    # メインコンテンツを表示する関数
    # 既存のコンテンツを全て削除
    for widget in ui.content_frame.winfo_children():
        widget.destroy()

    # メインコンテンツを表示（例としてラベルを表示）
    ui.create_main_content()

def show_second_content():
    # セカンドコンテンツを表示する関数
    # 既存のコンテンツを全て削除
    for widget in ui.content_frame.winfo_children():
        widget.destroy()

    # セカンドコンテンツを表示（例として中央にボタンを配置）
    ui.create_second_content()

def show_third_content():
    # セカンドコンテンツを表示する関数
    # 既存のコンテンツを全て削除
    for widget in ui.content_frame.winfo_children():
        widget.destroy()

    # セカンドコンテンツを表示（例として中央にボタンを配置）
    ui.create_third_content()


def on_press(key):
    if(ui.check_loud_key.get()):
        try:
            print('press: {}'.format(key.char))
            if format(key.char).capitalize() in ui.entry_key_overrideflags and ui.entry_key_overrideflags[format(key.char).capitalize()]:
                threading.Thread(target=lambda:logic.play_sound_override(format(key.char).capitalize())).start()
            else:
                threading.Thread(target=logic.play_sound).start()
        except AttributeError:
            print('spkey press: {}'.format(key.name))
            if format(key.name).capitalize() in ui.entry_key_overrideflags and ui.entry_key_overrideflags[format(key.name).capitalize()]:
                threading.Thread(target=lambda:logic.play_sound_override(format(key.name).capitalize())).start()
            else:
                threading.Thread(target=logic.play_sound).start()

def on_click(x, y, button, pressed):
    if pressed and ui.check_loud_click.get():
        if button == mouse.Button.left:
            if 'leftclick' in ui.entry_override_preset_mouse_button:
                threading.Thread(target=lambda:logic.play_sound_override_mouse('leftclick')).start()
            else:
                threading.Thread(target=logic.play_sound).start()
        elif button == mouse.Button.right:
            if 'rightclick' in ui.entry_override_preset_mouse_button:
                threading.Thread(target=lambda:logic.play_sound_override_mouse('rightclick')).start()
            else:
                threading.Thread(target=logic.play_sound).start()
        elif button == mouse.Button.middle and 'middleclick' in ui.entry_override_preset_mouse_button:
            if 'middleclick' in ui.entry_override_preset_mouse_button:
                threading.Thread(target=lambda:logic.play_sound_override_mouse('middleclick')).start()
            else:
                threading.Thread(target=logic.play_sound).start()

def on_scroll(x, y, dx, dy):
    if ui.check_loud_scroll.get():
        if('mousescroll' in ui.entry_override_preset_mouse_button):
            threading.Thread(target=lambda:logic.play_sound_override_mouse('mousescroll')).start()
        else:
            threading.Thread(target=logic.play_sound).start()

def add_sound_file():
    filename = filedialog.askopenfilename(filetypes=[("SE File","*.wav;*.mp3;*.ogg"), ("All Files", "*")])
    if filename:
        logic.sound_files.append(filename)
        ui.file_list_box.insert(tk.END, filename)

def remove_sound_file():
    if ui.file_list_box.curselection() >= 0:
        logic.sound_files.pop(ui.file_list_box.curselection())
        ui.file_list_box.delete(ui.file_list_box.curselection())

def move_up():
    selected_indices = ui.file_list_box.curselection()
    ui.file_list_box.move_up(selected_indices)

def move_down():
    selected_indices = ui.file_list_box.curselection()
    ui.file_list_box.move_down(selected_indices)

def create_image():
    # ここでタスクトレイアイコンの画像を作成します
    # Base64でエンコードされた画像データ
    encoded_image = ic.icon_data

    # Base64データをバイナリデータにデコードし、PIL Imageに変換
    icon_image = Image.open(BytesIO(base64.b64decode(encoded_image)))
    return icon_image

def show_window(icon, item):
    icon.stop()
    root.after(0, root.deiconify)

def hide_window():
    root.withdraw()
    image = create_image()
    menu = (item('ウィンドウを表示', show_window), item('終了', exit_app))
    icon = pystray.Icon("name", image, "タイトル", menu)
    icon.run()

def exit_app(icon, item):
    icon.stop()
    root.destroy()

def save_preset():
    filename = filedialog.asksaveasfilename(defaultextension=".json",
                                            filetypes=[("JSON Files", "*.json"), ("All Files", "*")])
    if filename:
        with open(filename, 'w') as file:
            json.dump(logic.sound_files, file)

def load_preset():
    filename = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json"), ("All Files", "*")])
    if filename:
        with open(filename, 'r') as file:
            loaded_files = json.load(file)
            logic.sound_files.clear()
            logic.sound_files.extend(loaded_files)
            update_listbox()

def update_listbox():
    ui.file_list_box.delete(0, tk.END)
    for file in logic.sound_files:
        ui.file_list_box.insert(tk.END, file)

def on_closing():
    logic.save_last_preset()
    root.destroy()

def on_click_keyboard(key):
    ui.current_select_key = key
    ui.label_current_key.configure(text="選択中：" + ui.current_select_key)
    if ui.current_select_key in ui.entry_override_key_file:
        ui.entry_overlide_key.configure(textvariable=ui.entry_override_key_file[ui.current_select_key])
    else:
        ui.entry_overlide_key.configure(textvariable=ctk.StringVar()) 

def on_load_keyboard_override_preset():
    # JSONファイルから読み込み
    filename = filedialog.askopenfilename(defaultextension=".json",
                                            filetypes=[("JSON Files", "*.json")])
    if filename:
        with open(filename, 'r') as f:
            data = json.load(f)
    loaded_data = data['file']
    ui.entry_key_overrideflags = data['keyoverride']

    # 読み込んだデータからctk.StringVarの辞書を作成
    new_ctk_string_vars = {k: ctk.StringVar(value=v) for k, v in loaded_data.items()}

    ui.entry_override_key_file = new_ctk_string_vars

    # forで回す
    for key in ui.entry_key_overrideflags:
        if(key == ''):
            continue

        ui.entry_key_overrideflags[key] = True
        ui.entry_key[key].configure(fg_color="red")


def on_save_keyboard_override_preset():
    # ctk.StringVarから通常の文字列を取得し、新しい辞書に格納
    normal_strings = {k: v.get() for k, v in ui.entry_override_key_file.items()}


    data = {
    'file': normal_strings,
    'keyoverride': ui.entry_key_overrideflags
    }

    filename = filedialog.asksaveasfilename(defaultextension=".json",
                                            filetypes=[("JSON Files", "*.json"), ("All Files", "*")])
    if filename:
        # JSONファイルに書き込み
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

def on_load_mouse_override_preset():
# JSONファイルから読み込み
    filename = filedialog.askopenfilename(defaultextension=".json",
                                            filetypes=[("JSON Files", "*.json"), ("All Files", "*")])
    if filename:
        with open(filename, 'r') as f:
            data = json.load(f)
    loaded_data = data['file']
    ui.entry_mouse_overrideflags = data['keyoverride']

    # 読み込んだデータからctk.StringVarの辞書を作成
    new_ctk_string_vars = {k: ctk.StringVar(value=v) for k, v in loaded_data.items()}

    ui.entry_override_preset_mouse_button = new_ctk_string_vars

    if('rightclick' in ui.entry_mouse_overrideflags):
        ui.entry_override_mouse_right.configure(textvariable=ui.entry_override_preset_mouse_button['rightclick']) 
    if('leftclick' in ui.entry_mouse_overrideflags):
        ui.entry_override_mouse_left.configure(textvariable=ui.entry_override_preset_mouse_button['leftclick']) 
    if('middleclick' in ui.entry_mouse_overrideflags):
        ui.entry_override_mouse_middle.configure(textvariable=ui.entry_override_preset_mouse_button['middleclick']) 
    if('mousescroll' in ui.entry_mouse_overrideflags):
        ui.entry_override_mouse_scroll.configure(textvariable=ui.entry_override_preset_mouse_button['mousescroll']) 
    return

def on_save_mouse_override_preset():
    # ctk.StringVarから通常の文字列を取得し、新しい辞書に格納
    normal_strings = {k: v.get() for k, v in ui.entry_override_preset_mouse_button.items()}


    data = {
    'file': normal_strings,
    'keyoverride': ui.entry_mouse_overrideflags
    }

    filename = filedialog.asksaveasfilename(defaultextension=".json",
                                            filetypes=[("JSON Files", "*.json")])
    if filename:
        # JSONファイルに書き込み
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    return

def on_load_mouse_override(key):
    filepath = filedialog.askopenfilename(filetypes=[("SE File","*.wav;*.mp3;*.ogg"), ("All Files", "*")])
    if filepath and ui.current_select_key != None:
        ui.entry_override_preset_mouse_button[key] = ctk.StringVar()
        ui.entry_override_preset_mouse_button[key].set(filepath)
        if(key == 'rightclick'):
            ui.entry_override_mouse_right.configure(textvariable=ui.entry_override_preset_mouse_button[key]) 
        elif(key == 'leftclick'):
            ui.entry_override_mouse_left.configure(textvariable=ui.entry_override_preset_mouse_button[key]) 
        elif(key == 'middleclick'):
            ui.entry_override_mouse_middle.configure(textvariable=ui.entry_override_preset_mouse_button[key]) 
        elif(key == 'mousescroll'):
            ui.entry_override_mouse_scroll.configure(textvariable=ui.entry_override_preset_mouse_button[key]) 

        ui.entry_mouse_overrideflags[key] = True

def on_reset_mouse_override(key):

    del ui.entry_override_preset_mouse_button[key]

    if(key == 'rightclick'):
        ui.entry_override_mouse_right.configure(textvariable=ctk.StringVar()) 
    elif(key == 'leftclick'):
        ui.entry_override_mouse_left.configure(textvariable=ctk.StringVar()) 
    elif(key == 'middleclick'):
        ui.entry_override_mouse_middle.configure(textvariable=ctk.StringVar()) 
    elif(key == 'mousescroll'):
        ui.entry_override_mouse_scroll.configure(textvariable=ctk.StringVar()) 

    del ui.entry_mouse_overrideflags[key]

def on_load_key_override():
    filepath = filedialog.askopenfilename(filetypes=[("SE File","*.wav;*.mp3;*.ogg"), ("All Files", "*")])
    if filepath and ui.current_select_key != None:
        ui.entry_override_key_file[ui.current_select_key] = ctk.StringVar()
        ui.entry_override_key_file[ui.current_select_key].set(filepath)
        ui.entry_overlide_key.configure(textvariable=ui.entry_override_key_file[ui.current_select_key]) 
        ui.entry_key_overrideflags[ui.current_select_key] = True
        ui.entry_key[ui.current_select_key].configure(fg_color="red")

def on_reset_override_key():
    if ui.current_select_key != None:
        del ui.entry_override_key_file[ui.current_select_key]
        ui.entry_overlide_key.configure(textvariable=ctk.StringVar()) 
        del ui.entry_key_overrideflags[ui.current_select_key]
        ui.entry_key[ui.current_select_key].configure(fg_color="transparent")

def on_change_check_loud_key():
    ui.check_loud_key_buffer = ui.check_loud_key.get()

def on_change_check_loud_click():
    ui.check_loud_click_buffer = ui.check_loud_click.get()

def on_change_check_loud_scroll():
    ui.check_loud_scroll_buffer = ui.check_loud_scroll.get()