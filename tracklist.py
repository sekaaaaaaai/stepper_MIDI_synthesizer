import mido
import sys

# コマンドライン引数からMIDIファイル名を取得
if len(sys.argv) < 2:
    print("使用方法: python script.py <MIDIファイル>")
    sys.exit(1)

midi_file = sys.argv[1]  # コマンドライン引数からMIDIファイル名を取得
mid = mido.MidiFile(midi_file)

# トラック情報を表示
for i, track in enumerate(mid.tracks):
    print(f"Track {i}: {track.name}")

