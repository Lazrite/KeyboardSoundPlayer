import tkinter as tk
import customtkinter as ctk
import CTkListbox
import business_logic as logic
import event_handlers as ev

# グローバル

# コンテンツフレーム
content_frame = None
# 音量スライダー
volume_slider = None
# 音量表示ラベル
volume_var = None
# 長押し時間スライダー
pressed_time_slider = None
# 長押し時間ラベル
pressed_time_var = None
# サウンドファイル一覧リストボックス
file_list_box = None
# ルートウィンドウ
root = None
# キーボードオーバーライドプリセット
entry_override_preset = None
# キーボードオーバーライドファイル
entry_override_key_file = {}
# エントリされているキー
entry_key = {}
# エントリキーオーバーライドフラグ
entry_key_overrideflags = {}
# オーバーライドされているキー
entry_overlide_key = None
# 現在選択中のキーのラベル
label_current_key = None
# 現在選択中のキー
current_select_key = ""
# マウスオーバーライドプリセット
entry_override_preset_mouse = None
# マウスオーバーライドボタン
entry_override_preset_mouse_button = {}
# 右クリックエントリ
entry_override_mouse_right = None
# 左クリックエントリ
entry_override_mouse_left = None
# 中クリックエントリ
entry_override_mouse_middle = None
# スクロールエントリ
entry_override_mouse_scroll = None
# キーボードを鳴らすかフラグ
check_loud_key = None
# 情報保存バッファ
check_loud_key_buffer = None
# クリックを鳴らすかフラグ
check_loud_click = None
# 情報保存バッファ
check_loud_click_buffer = None
# スクロールを鳴らすかフラグ
check_loud_scroll = None
# 情報保存バッファ
check_loud_scroll_buffer = None
# マウスオーバーライドフラグ
entry_mouse_overrideflags = {}
# ボタン長押しを許容するか
check_pressed_key = None
# 情報保存バッファ
check_pressed_key_buffer = None

# 特殊キーを含むキーボードのレイアウト
key_rows = [
    ["Esc"] + [f"F{i}" for i in range(1, 13)],
    ["~", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "Backspace"],
    ["Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "@", "[", "]", "\\"],
    ["CapsLock", "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "Enter"],
    ["Shift", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "Shift_r", "Up"],
    ["Ctrl_l", "Cmd", "Alt_l", "Space", "Alt_r", "Fn", "Menu", "Ctrl_r", "Left", "Down", "Right"],
]

# 初期化処理
def inithialize(root_param):
    global root
    global check_loud_key_buffer
    global check_loud_click_buffer
    global check_loud_scroll_buffer
    global check_pressed_key_buffer

    root = root_param
    check_loud_key_buffer = 1
    check_loud_click_buffer = 1
    check_loud_scroll_buffer = 1
    check_pressed_key_buffer = 0

# サイドバー作成
def create_sidebar():
    # サイドバーメニュー用のフレームを作成
    sidebar = ctk.CTkFrame(root, width=200, corner_radius=0)
    sidebar.pack(side="left", fill="y")

    # サイドバーメニューの項目（ボタン）を追加
    btn1 = ctk.CTkButton(sidebar, text="全体設定", command=ev.show_main_content)
    btn1.pack(pady=10, padx=10)
    # キーボードオーバーライドボタン
    btn2 = ctk.CTkButton(sidebar, text="キーボード\nオーバーライド", command=ev.show_second_content)
    btn2.pack(pady=10, padx=10)
    # マウスオーバーライドボタン
    btn3 = ctk.CTkButton(sidebar, text="マウス\nオーバーライド", command=ev.show_third_content)
    btn3.pack(pady=10, padx=10)

    #最小化ボタン
    minimize_button = ctk.CTkButton(sidebar, text="バックグラウンドで実行する", command=lambda:ev.hide_window())
    minimize_button.pack(side="bottom", pady=10, padx=10)

# コンテンツエリア作成
def create_content_area():
    global content_frame  # グローバル変数を使用することを明示
    # コンテンツ表示エリア
    content_frame = ctk.CTkFrame(root)
    content_frame.pack(side="right", fill="both", expand=True)
    return content_frame

# メインコンテンツ作成
def create_main_content():
    root.geometry("800x600")

    # モード選択とボタン用のフレーム
    control_frame = ctk.CTkFrame(content_frame)
    control_frame.pack(padx = 10, pady=10, fill="x")

    # モード切替ラベル
    mode_label = ctk.CTkLabel(control_frame, text="モード切替")
    mode_label.pack(side="left", padx=10)

    # ラジオボタン
    mode_var = ctk.StringVar(value="Default")
    modes = [("Default", "Default"), ("Random", "Random"), ("Loop", "Loop")]
    for text, mode in modes:
        ctk.CTkRadioButton(control_frame, text=text, variable=mode_var, value=mode, command=lambda: logic.change_mode(mode_var.get())).pack(side="left")
    mode = "Default"

    # 音量調整スライダー用のフレーム
    volume_frame = ctk.CTkFrame(content_frame)
    volume_frame.pack(side="left", pady=10, padx=10, fill="y")

    volume_label = ctk.CTkLabel(volume_frame, text="音量調整")
    volume_label.pack(pady=5, padx=5)

    global volume_slider
    volume_slider = ctk.CTkSlider(volume_frame, from_=0, to=100, orientation='Vertical', command=logic.change_volume)
    volume_slider.set(100)
    volume_slider.pack()

    global volume_var
    volume_var = ctk.CTkLabel(volume_frame, text=volume_slider.get())
    volume_var.pack()

    # 長押し時間指定スライダー用のフレーム
    pressed_time_frame = ctk.CTkFrame(content_frame)
    pressed_time_frame.pack(side="left", pady=10, padx=10, fill="y")

    pressed_time_label = ctk.CTkLabel(pressed_time_frame, text="リピート\n時間")
    pressed_time_label.pack(pady=5, padx=5)

    global pressed_time_slider
    pressed_time_slider = ctk.CTkSlider(pressed_time_frame, from_=0, to=1, orientation='Vertical', command=logic.change_repeat)
    pressed_time_slider.set(1.0)
    pressed_time_slider.pack()

    global pressed_time_var
    pressed_time_var = ctk.CTkLabel(pressed_time_frame, text=pressed_time_slider.get())
    pressed_time_var.pack()

    # ボタンフレーム
    btn_frame = ctk.CTkFrame(content_frame)
    btn_frame.pack(fill='both', pady=10, padx=10)

    # サウンドファイル操作ボタン
    btn_add = ctk.CTkButton(btn_frame, text="ファイル追加", command=ev.add_sound_file)
    btn_add.grid(row=0, column=0, padx=5, pady=5, sticky='we')

    btn_remove = ctk.CTkButton(btn_frame, text="ファイル削除", command=ev.remove_sound_file)
    btn_remove.grid(row=1, column=0, padx=5, pady=5, sticky='we')

    btn_move_up = ctk.CTkButton(btn_frame, text="上に移動", command=ev.move_up)
    btn_move_up.grid(row=2, column=0, padx=5, pady=5, sticky='we')

    btn_move_down = ctk.CTkButton(btn_frame, text="下に移動", command=ev.move_down)
    btn_move_down.grid(row=3, column=0, padx=5, pady=5, sticky='we')

    # GUIでプリセット保存・読み込みボタンを追加
    btn_save_preset = ctk.CTkButton(btn_frame, text="プリセット保存", command=ev.save_preset)
    btn_save_preset.grid(row=4, column=0, padx=5, pady=5, sticky='we')

    btn_load_preset = ctk.CTkButton(btn_frame, text="プリセット読み込み", command=ev.load_preset)
    btn_load_preset.grid(row=5, column=0, padx=5, pady=5, sticky='we')

    global check_loud_key
    check_loud_key = check_loud_key_buffer
    check_loud_key = ctk.CTkCheckBox(btn_frame, text="キーボードを鳴らす", variable=ctk.IntVar(value=check_loud_key), command=ev.on_change_check_loud_key)
    check_loud_key.grid(row=0, column=1, padx=5, pady=5, sticky='we')

    global check_loud_click
    check_loud_click = check_loud_click_buffer
    check_loud_click = ctk.CTkCheckBox(btn_frame, text="マウスクリックを鳴らす", variable=ctk.IntVar(value=check_loud_click), command=ev.on_change_check_loud_click)
    check_loud_click.grid(row=1, column=1, padx=5, pady=5, sticky='we')

    global check_loud_scroll
    check_loud_scroll = check_loud_scroll_buffer
    check_loud_scroll = ctk.CTkCheckBox(btn_frame, text="マウススクロールを鳴らす", variable=ctk.IntVar(value=check_loud_scroll), command=ev.on_change_check_loud_scroll)
    check_loud_scroll.grid(row=2, column=1, padx=5, pady=5, sticky='we')

    global check_pressed_key
    check_pressed_key = check_pressed_key_buffer
    check_pressed_key = ctk.CTkCheckBox(btn_frame, text="長押しでリピートする", variable=ctk.IntVar(value=check_pressed_key), command=ev.on_change_check_pressed_key)
    check_pressed_key.grid(row=3, column=1, padx=5, pady=5, sticky='we')

    # サウンドファイル一覧CTkListbox
    global file_list_box
    file_list_box = CTkListbox.CTkListbox(content_frame)
    for file in logic.sound_files:
        file_list_box.insert(tk.END, file)
    file_list_box.pack(fill="both", expand=True, pady=10, padx=10)

def create_second_content():
    root.geometry("1200x600")

    keyboard_override_preset = ctk.CTkFrame(content_frame)
    keyboard_override_preset.pack(fill=tk.X, padx=10, pady=10)

    #プリセット
    preset_lavel = ctk.CTkLabel(keyboard_override_preset, text="オーバーライドプリセット")
    preset_lavel.pack()

    # ファイルパス表示用のエントリー（読み取り専用）
    global entry_override_preset
    entry_override_preset = ctk.StringVar()
    entry = ctk.CTkEntry(keyboard_override_preset, textvariable=entry_override_preset, state="readonly")
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)

    # オーバーライドプリセット選択ボタン
    button = ctk.CTkButton(keyboard_override_preset, text="プリセット保存", command=ev.on_save_keyboard_override_preset)
    button.pack(side=tk.RIGHT, padx=10, pady=10)

    # オーバーライドプリセット保存ボタン
    button = ctk.CTkButton(keyboard_override_preset, text="プリセット読み込み", command=ev.on_load_keyboard_override_preset)
    button.pack(side=tk.RIGHT, padx=10, pady=10)

    # 事前告知
    warn_label = ctk.CTkLabel(content_frame, text="お使いのキーボードでは動かないキーもあります")
    warn_label.pack()

    # キーボードのGUI表示
    global entry_key
    for row in key_rows:
        frame = ctk.CTkFrame(content_frame)
        frame.pack(pady=5)
        for key in row:
            if key == "":
                continue  # 空のキーはスキップ
            if key in ["Backspace", "Tab", "CapsLock", "Enter", "Shift", "Space"]:
                button_width = 80
            else:
                button_width = 40
            button = ctk.CTkButton(frame, border_width=2, fg_color="transparent", text=key, command=lambda k=key: ev.on_click_keyboard(k), width=button_width, height=40)
            button.pack(side=tk.LEFT, padx=5, pady=5)
            entry_key[key] = button

    keyboard_override_menu = ctk.CTkFrame(content_frame)
    keyboard_override_menu.pack(fill=tk.X, padx=10, pady=10)

    #オーバーライドメニューの表示

    #キーオーバーライドラベル
    global label_current_key
    label_current_key = ctk.CTkLabel(keyboard_override_menu, text="選択中：" + current_select_key)
    label_current_key.pack()

    # ファイルパス表示用のエントリー（読み取り専用）
    global entry_override_key_file
    global entry_overlide_key
    entry_override_key_file[current_select_key] = ctk.StringVar()
    entry_overlide_key = ctk.CTkEntry(keyboard_override_menu, textvariable=entry_override_key_file[current_select_key], state="readonly")
    entry_overlide_key.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)

    # オーバーライド解除ボタン
    button = ctk.CTkButton(keyboard_override_menu, text="オーバーライド解除", border_width=2, fg_color="transparent", command=ev.on_reset_override_key)
    button.pack(side=tk.RIGHT, padx=10, pady=10)

    # ファイル選択ボタン
    button = ctk.CTkButton(keyboard_override_menu, text="オーバーライドファイル選択", command=ev.on_load_key_override)
    button.pack(side=tk.RIGHT, padx=10, pady=10)

def create_third_content():
    root.geometry("1200x600")

    global entry_override_mouse_right
    global entry_override_mouse_left
    global entry_override_mouse_middle
    global entry_override_mouse_scroll

    mouse_override_preset = ctk.CTkFrame(content_frame)
    mouse_override_preset.pack(fill=tk.X, padx=10, pady=10)

    #プリセット
    preset_lavel = ctk.CTkLabel(mouse_override_preset, text="オーバーライドプリセット")
    preset_lavel.pack()

    #プリセット
    # ファイルパス表示用のエントリー（読み取り専用）
    global entry_override_preset_mouse
    entry_override_preset_mouse = ctk.StringVar()
    entry = ctk.CTkEntry(mouse_override_preset, textvariable=entry_override_preset_mouse, state="readonly")
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)

    # オーバーライドプリセット選択ボタン
    button = ctk.CTkButton(mouse_override_preset, text="プリセット選択", command=ev.on_load_mouse_override_preset)
    button.pack(side=tk.RIGHT, padx=10, pady=10)

    # オーバーライドプリセット保存ボタン
    button2 = ctk.CTkButton(mouse_override_preset, text="プリセット保存", command=ev.on_save_mouse_override_preset)
    button2.pack(side=tk.RIGHT, padx=10, pady=10)

    mouse_override = ctk.CTkFrame(content_frame)
    mouse_override.pack(fill=tk.X, padx=10, pady=10)
    mouse_override.grid_columnconfigure((0), weight=1)

    

    #プリセット
    # ファイルパス表示用のエントリー（読み取り専用）
    entry_override_mouse_right = ctk.CTkEntry(mouse_override, textvariable=ctk.StringVar(), state="readonly")
    
    entry_override_mouse_right.grid(row=0, column=0, padx=10, pady=10, columnspan=10, sticky='we')
    
    #右クリック
    mouse_lavel = ctk.CTkLabel(mouse_override, text="右クリック")
    mouse_lavel.grid(row=0, column=11, padx=10, pady=10, sticky='e')

    # オーバーライドプリセット選択ボタン
    button = ctk.CTkButton(mouse_override, text="オーバーライドファイル選択", command=lambda:ev.on_load_mouse_override('rightclick'))
    button.grid(row=0, column=12, padx=10, pady=10, sticky='e')

    # オーバーライド解除ボタン
    button = ctk.CTkButton(mouse_override, text="オーバーライド解除", command=lambda:ev.on_reset_mouse_override('rightclick'))
    button.grid(row=0, column=13, padx=10, pady=10, sticky='e')

    #プリセット
    # ファイルパス表示用のエントリー（読み取り専用）
    entry_override_mouse_left = ctk.CTkEntry(mouse_override, textvariable=ctk.StringVar(), state="readonly")
    
    entry_override_mouse_left.grid(row=1, column=0, padx=10, pady=10, columnspan=10, sticky='we')
    
    #左クリック
    mouse_lavel = ctk.CTkLabel(mouse_override, text="左クリック")
    mouse_lavel.grid(row=1, column=11, padx=10, pady=10, sticky='e')

    # オーバーライドプリセット選択ボタン
    button = ctk.CTkButton(mouse_override, text="オーバーライドファイル選択", command=lambda:ev.on_load_mouse_override('leftclick'))
    button.grid(row=1, column=12, padx=10, pady=10, sticky='e')

    # オーバーライド解除ボタン
    button = ctk.CTkButton(mouse_override, text="オーバーライド解除", command=lambda:ev.on_reset_mouse_override('leftclick'))
    button.grid(row=1, column=13, padx=10, pady=10, sticky='e')

    #プリセット
    # ファイルパス表示用のエントリー（読み取り専用）
    entry_override_mouse_middle = ctk.CTkEntry(mouse_override, textvariable=ctk.StringVar(), state="readonly")
    
    entry_override_mouse_middle.grid(row=2, column=0, padx=10, pady=10, columnspan=10, sticky='we')
    
    #中クリック
    mouse_lavel = ctk.CTkLabel(mouse_override, text="中クリック")
    mouse_lavel.grid(row=2, column=11, padx=10, pady=10, sticky='e')

    # オーバーライドプリセット選択ボタン
    button = ctk.CTkButton(mouse_override, text="オーバーライドファイル選択", command=lambda:ev.on_load_mouse_override('middleclick'))
    button.grid(row=2, column=12, padx=10, pady=10, sticky='e')

    # オーバーライド解除ボタン
    button = ctk.CTkButton(mouse_override, text="オーバーライド解除", command=lambda:ev.on_reset_mouse_override('middleclick'))
    button.grid(row=2, column=13, padx=10, pady=10, sticky='e')

    #プリセット
    # ファイルパス表示用のエントリー（読み取り専用）
    entry_override_mouse_scroll = ctk.CTkEntry(mouse_override, textvariable=ctk.StringVar(), state="readonly")
    
    entry_override_mouse_scroll.grid(row=3, column=0, padx=10, pady=10, columnspan=10, sticky='we')
    
    #スクロール
    mouse_lavel = ctk.CTkLabel(mouse_override, text="マウススクロール")
    mouse_lavel.grid(row=3, column=11, padx=10, pady=10, sticky='e')

    # オーバーライドプリセット選択ボタン
    button = ctk.CTkButton(mouse_override, text="オーバーライドファイル選択", command=lambda:ev.on_load_mouse_override('mousescroll'))
    button.grid(row=3, column=12, padx=10, pady=10, sticky='e')

    # オーバーライド解除ボタン
    button = ctk.CTkButton(mouse_override, text="オーバーライド解除", command=lambda:ev.on_reset_mouse_override('mousescroll'))
    button.grid(row=3, column=13, padx=10, pady=10, sticky='e')
    

