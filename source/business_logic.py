import pygame
import time
import json
import os
import sys
import random
import main
from tkinter import filedialog
import ui_components as ui
import tkinter as tk

# スクリプトのディレクトリをカレントディレクトリに設定
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# exeを実行している作業ディレクトリを読み込みbase_pathに格納
base_path = os.path.dirname(os.path.abspath(sys.argv[0]))

preset_file = os.path.join(base_path, 'last_preset.json')   

# グローバル変数
# デフォルトのサウンドファイルリスト
sound_files = []
current_sound_index = 0
last_key_time = time.time()
mode = "Default"
volume = 1.0

def play_sound():
    global current_sound_index, last_key_time, mode, volume
    if not sound_files:
        return
    current_time = time.time()

    # モードに応じたサウンドの選択
    if mode == "Default":
        # 1秒以内に連続してキーが押されたか判定
        if current_time - last_key_time <= 1.0:
            current_sound_index = min(current_sound_index + 1, len(sound_files) - 1)
        else:
            current_sound_index = 0

        sound = pygame.mixer.Sound(sound_files[current_sound_index])
    elif mode == "Random":
        sound = pygame.mixer.Sound(random.choice(sound_files))
    elif mode == "Loop":
        sound = pygame.mixer.Sound(sound_files[current_sound_index])
        current_sound_index = (current_sound_index + 1) % len(sound_files)

    last_key_time = current_time
    sound.set_volume(volume)
    sound.play()

def play_sound_override(key_name):
    if(ui.entry_override_key_file[key_name].get() == None):
        return
    sound = pygame.mixer.Sound(ui.entry_override_key_file[key_name].get())
    sound.set_volume(volume)
    sound.play()

def play_sound_override_mouse(key):
    sound = pygame.mixer.Sound(ui.entry_override_preset_mouse_button[key].get())
    sound.set_volume(volume)
    sound.play()

def update_listbox():
    ui.file_list_box.delete(0, tk.END)
    for file in sound_files:
        ui.file_list_box.insert(tk.END, file)

def save_last_preset():
    with open(preset_file, 'w') as file:
        json.dump(sound_files, file)

def load_last_preset():
    if os.path.exists(preset_file):
        with open(preset_file, 'r') as file:
            loaded_files = json.load(file)
            sound_files.clear()
            sound_files.extend(loaded_files)
            update_listbox()

def change_mode(new_mode):
    global mode
    mode = new_mode

def change_volume(val):
    global volume
    volume = float(val) / 100