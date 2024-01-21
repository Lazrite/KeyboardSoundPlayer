
import tkinter as tk
import customtkinter as ctk
import ui_components as ui
import event_handlers as ev
import business_logic as logic
from pynput import keyboard
from pynput import mouse
import pygame
import os
import sys
import icon


def main():
    # メインウィンドウの設定
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("green")
    # ルートメイン
    root = ctk.CTk()
    # タイトル初期化
    root.title("キーボードサウンドプレイヤー")
    root.geometry("800x600")

    # アイコンの設定
    ic = tk.PhotoImage(data=icon.icon_data)  # PhotoImageオブジェクトの作成
    root.wm_iconbitmap()
    root.iconphoto(False, ic)

    #イベントハンドラ、コンポーネント初期化
    ev.inithialize(root)
    ui.inithialize(root)

    # UIコンテンツ作成
    ui.create_sidebar()
    ui.create_content_area()
    ui.create_main_content()

    #pygameのサウンド初期化
    pygame.mixer.init()

    # キーボードリスナー
    listener = keyboard.Listener(on_press=ev.on_press)
    listener.start()

    # マウスリスナー
    listener_mouse = mouse.Listener(on_click=ev.on_click, on_scroll=ev.on_scroll)
    listener_mouse.start()

    # アプリケーション起動時に最後のプリセットを読み込む
    logic.load_last_preset()  

    # アプリ終了時にイベントをバインド
    root.protocol("WM_DELETE_WINDOW", ev.on_closing)

    # メインループ開始
    root.mainloop()

if __name__ == "__main__":
    main()
