import subprocess
from typing import Dict, List, Tuple
import shutil

def clamp_output(query_modal: str, key_modal:str, top_n:int = 1, model:str = "sander-wood/clamp-small-512", cwd: str = "notebooks/clamp/model/") -> List[Tuple[str, float, float]]:
    if top_n <= 0:
        return []
    command = ["python", "clamp_ori.py", "-clamp_model_name", model,
            "-query_modal", query_modal, "-key_modal", key_modal, "-top_n", str(top_n)]
    res = subprocess.run(command,stdout=subprocess.PIPE, cwd = cwd)
    data_lines = res.stdout.decode('utf-8').strip().split('\n')
    music_data = []
    i = 0
    while i < len(data_lines):
        line = data_lines[i]
        if line.startswith("Prob"):
            prob = float(line.split(':')[1].split('%')[0]) / 100  # Extract probability
            sim = float(line.split('- Sim:')[1].split(':')[0])  # Extract similarity
            music_name = data_lines[i+1].strip().split('/')[-1]  # Extract music file name
            music_data.append((music_name, prob, sim))
            i += 2  # Skip the next line since it's the music file name
        else:
            i += 1

    return music_data

def change_clamp_txt_query(query:str, path:str="notebooks/clamp/model/inference/") -> None:
    with open(path + "text_query.txt", 'w') as file:
        file.write(query)

def get_output_change_txt_query(query:str, path:str="notebooks/clamp/model/inference/", top_n:int = 1, model:str = "sander-wood/clamp-small-512", cwd: str = "notebooks/clamp/model/") -> List[Tuple[str, float, float]]:
    change_clamp_txt_query(query, path)
    return clamp_output("text", "music",top_n=top_n, model=model, cwd=cwd)

def change_clamp_music_query(original_query_path:str, clamp_reading_path:str="notebooks/clamp/model/inference/") -> None:
    shutil.copy2(original_query_path, clamp_reading_path + "music_query.mxl")

def change_clamp_txt_keys(keys:List[str], path:str="notebooks/clamp/model/inference/") -> None:
    with open(path + "text_keys.txt", 'w') as file:
        for key in keys:
            file.write(key+"\n")

def get_output_change_music_query(music_query_path:str, path:str="notebooks/clamp/model/inference/", top_n:int = 1, model:str = "sander-wood/clamp-small-512", cwd: str = "notebooks/clamp/model/")-> List[Tuple[str, float, float]]:
    change_clamp_music_query(music_query_path, path)
    return clamp_output("music", "text", top_n=top_n, model=model, cwd=cwd)