import serial
import time
import mido
import sys

# 🎵 MIDIノート番号を周波数（Hz）に変換
def midi_to_freq(note):
    return 440.0 * (2 ** ((note - 69) / 12.0))

# コマンドライン引数からMIDIファイル名を取得
if len(sys.argv) < 2:
    print("使用方法: python script.py <MIDIファイル> <TrackNo.>")
    sys.exit(1)

midi_file = sys.argv[1]  # コマンドライン引数からMIDIファイル名を取得
track_number = int(sys.argv[2]) if len(sys.argv) > 2 else 0  # トラック番号（デフォルト: 0）

# 🎹 MIDIファイルを読み取る
mid = mido.MidiFile(midi_file)

# トラック番号が範囲外の場合のエラーハンドリング
if track_number < 0 or track_number >= len(mid.tracks):
    print(f"エラー: 指定されたトラック番号 {track_number} は存在しません。0 〜 {len(mid.tracks)-1} の範囲で指定してください。")
    sys.exit(1)

# 🎼 MIDIのテンポを取得（デフォルト: 120BPM = 500000μs）
tempo = 500000  # 初期値（マイクロ秒単位）
for track in mid.tracks:
    for msg in track:
        if msg.type == 'set_tempo':
            tempo = msg.tempo  # MIDI内のテンポを取得
            break

# ティックを秒に変換する関数
def ticks_to_seconds(ticks):
    return (ticks / mid.ticks_per_beat) * (tempo / 1_000_000.0)

# Arduinoと接続（ポートは環境に合わせて変更）
ser = serial.Serial('/dev/cu.usbserial-10', 9600)  # Windowsなら'COMx', Mac/Linuxなら'/dev/ttyUSBx'
time.sleep(2)  # 接続待ち

# 🎶 トラック0のMIDIイベントを解析＆送信
track = mid.tracks[2.3]  # トラック0のみ取得
active_notes = []  # 現在鳴っているノートを記録

for msg in track:
    time.sleep(ticks_to_seconds(msg.time))  # 適切な速度に調整

    if msg.type == 'note_on' and msg.velocity > 0:  # ノートON
        active_notes.append(msg.note)  # ノートをリストに追加
        active_notes.sort(reverse=True)  # 高い音を優先するためソート
        highest_note = active_notes[0]  # 一番高い音を取得
        freq = midi_to_freq(highest_note)
        print(f"Sending: {freq:.2f} Hz")
        ser.write(f"{freq:.2f}\n".encode())  # 送信

    elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):  # ノートOFF
        if msg.note in active_notes:
            active_notes.remove(msg.note)  # ノートをリストから削除
        
        if active_notes:  # まだ鳴っている音があれば一番高い音を送信
            highest_note = active_notes[0]
            freq = midi_to_freq(highest_note)
            print(f"Sending: {freq:.2f} Hz")
            ser.write(f"{freq:.2f}\n".encode())  # 送信
        else:
            ser.write("0.00\n".encode())  # 全部消えたら停止信号を送信

# 最後に停止信号を送る
ser.write("0.00\n".encode())  # 全部消えたら停止信号を送信

ser.close()

# # 🎶 MIDI イベントを解析＆送信
# active_notes = []  # 現在鳴っているノートを記録
# for msg in mid.play():  # play()を使うとタイミングを保持
#     if msg.type == 'note_on' and msg.velocity > 0:  # ノートON
#         active_notes.append(msg.note)  # ノートをリストに追加
#         active_notes.sort(reverse=True)  # 高い音を優先するためソート
#         highest_note = active_notes[0]  # 一番高い音を取得
#         freq = midi_to_freq(highest_note)
#         print(f"Sending: {freq:.2f} Hz")
#         ser.write(f"{freq:.2f}\n".encode())  # 送信

#     elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):  # ノートOFF
#         if msg.note in active_notes:
#             active_notes.remove(msg.note)  # ノートをリストから削除
        
#         if active_notes:  # まだ鳴っている音があれば一番高い音を送信
#             highest_note = active_notes[0]
#             freq = midi_to_freq(highest_note)
#             print(f"Sending: {freq:.2f} Hz")
#             ser.write(f"{freq:.2f}\n".encode())  # 送信
#         else:
#             ser.write("0.00\n".encode())  # 全部消えたら停止信号を送信

# ser.close()