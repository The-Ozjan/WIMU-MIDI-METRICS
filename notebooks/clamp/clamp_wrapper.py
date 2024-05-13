import subprocess

def clamp_output(query_modal: str, key_modal:str, top_n:int = 1, model:str = "sander-wood/clamp-small-512", cwd: str = "notebooks/clamp/model/"):
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
            music_name = data_lines[i+1].strip().split('inference/music_keys/')[1]  # Extract music file name
            music_data.append((music_name, prob, sim))
            i += 2  # Skip the next line since it's the music file name
        else:
            i += 1

    return music_data

def change_clamp_txt_query(query:str, path:str="notebooks/clamp/model/inference/"):
    with open(path + "text_query.txt", 'w') as file:
        file.write(query)