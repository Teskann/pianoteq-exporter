import os
import argparse
import subprocess
from pathlib import Path

import requests

pianoteq_path = os.path.expanduser("~/Applications/Pianoteq 8/x86-64bit/Pianoteq 8")
pianoteq_presets_path = os.path.expanduser("~/.local/share/Modartt/Pianoteq/Presets")
pianoteq_saved_midi_path = os.path.expanduser("~/.local/share/Modartt/Pianoteq/Archive")
exported_wav_folder = os.path.expanduser("~/pianoteq-exports")
index_of_midi_to_export = 1
remote_server = 'localhost:8081'

def most_recent(path, index=1):
    return os.path.join(path, sorted(os.listdir(path))[-index])

def latest_played_midi():
    return most_recent(most_recent(most_recent(pianoteq_saved_midi_path)), index_of_midi_to_export)

def save_current_preset():
    rpc("savePreset", {"name": "current_preset_for_export", "bank": "temp"})

def fxp_path():
    return os.path.join(pianoteq_presets_path, "temp", "current_preset_for_export.fxp")

def export_midi(midi_path, exported_wav_folder):
    wav_path = os.path.join(exported_wav_folder, Path(midi_path).stem + '.wav')
    subprocess.run([pianoteq_path, "--fxp", fxp_path(), "--midi", midi_path, "--wav", wav_path, "--normalize"])


def rpc(method, params=None, id_=0):
    if params is None:
        params=[]
    url = f'http://{remote_server}/jsonrpc'
    payload = {
        "method": method,
        "params": params,
        "jsonrpc": "2.0",
        "id": id_}

    try:
        result=requests.post(url, json=payload)
    except requests.exceptions.ConnectionError:
        print('Connection error..')
        return None

    return result.json()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--server", metavar='IP:PORT', help='specify the Pianoteq server address (default: ' + remote_server + ')')
    parser.add_argument("--ptq-path", help=f'Pianoteq executable Path (default: {pianoteq_path})', default=pianoteq_path)
    parser.add_argument("--ptq-presets-path", help=f'Pianoteq presets Path (default: {pianoteq_presets_path})', default=pianoteq_presets_path)
    parser.add_argument("--ptq-midi-files-path", help=f'Pianoteq saved midi files Path (default: {pianoteq_saved_midi_path})', default=pianoteq_saved_midi_path)
    parser.add_argument("--exported-wav-folder", help=f'Folder path of exported wav (default: {exported_wav_folder})', default=exported_wav_folder)
    parser.add_argument("--index-of-midi-to-export", help=f'Index of the midi file to export. 1 is the latest, 2 is the file before and so on (default: 1)', default=1)

    args = parser.parse_args()
    if args.server:
        remote_server = args.server
    if args.ptq_path:
        pianoteq_path = args.ptq_path
    if args.ptq_presets_path:
        pianoteq_presets_path = args.ptq_presets_path
    if args.ptq_midi_files_path:
        pianoteq_saved_midi_path = args.ptq_midi_files_path
    if args.exported_wav_folder:
        exported_wav_folder = args.exported_wav_folder
    if args.index_of_midi_to_export:
        index_of_midi_to_export = int(args.index_of_midi_to_export)

    save_current_preset()
    midi_path = latest_played_midi()
    export_midi(midi_path, exported_wav_folder)