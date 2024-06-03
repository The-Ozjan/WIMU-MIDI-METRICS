import subprocess
from typing import Dict, List, Tuple
import shutil
import notebooks.clamp.model.clamp_ori as clamp
from torch import Tensor
from unidecode import unidecode
from transformers import AutoTokenizer
from notebooks.clamp.model.utils import *


def clamp_output(
    query_modal: str,
    key_modal: str,
    top_n: int = 1,
    model: str = 'sander-wood/clamp-small-512',
    cwd: str = 'notebooks/clamp/model/',
) -> List[Tuple[str, float, float]]:
    """
    Function for getting output from clamp model using different queries
    Returns list of tupples with music name, probability and similarity

    query_modal: name of query. It could be text or music
    key_modal: nameof key: It could be text or music
    top_n: size of output files
    model: clamp model. It could be clamp-small-512 or clamp-small-1024
    """
    if top_n <= 0:
        return []
    command = [
        'python',
        'clamp_ori.py',
        '-clamp_model_name',
        model,
        '-query_modal',
        query_modal,
        '-key_modal',
        key_modal,
        '-top_n',
        str(top_n),
    ]
    res = subprocess.run(command, stdout=subprocess.PIPE, cwd=cwd)
    data_lines = res.stdout.decode('utf-8').strip().split('\n')
    music_data = []
    i = 0
    while i < len(data_lines):
        line = data_lines[i]
        if line.startswith('Prob'):
            prob = float(line.split(':')[1].split('%')[0]) / 100  # Extract probability
            sim = float(line.split('- Sim:')[1].split(':')[0])  # Extract similarity
            music_name = data_lines[i + 1].strip().split('/')[-1]  # Extract music file name
            music_data.append((music_name, prob, sim))
            i += 2  # Skip the next line since it's the music file name
        else:
            i += 1

    return music_data


def change_clamp_txt_query(query: str, path: str = 'notebooks/clamp/model/inference/') -> None:
    """
    Function for clamp text query changing

    query: new string query
    path: path to query file to save
    """
    with open(path + 'text_query.txt', 'w') as file:
        file.write(query)


def get_output_change_txt_query(
    query: str,
    path: str = 'notebooks/clamp/model/inference/',
    top_n: int = 1,
    model: str = 'sander-wood/clamp-small-512',
    cwd: str = 'notebooks/clamp/model/',
) -> List[Tuple[str, float, float]]:
    """
    Function for getting text query clamp output.
    Returns clamp model output for text guery

    query_modal: name of query. It could be text or music
    path: path to query file to save
    top_n: size of output files
    model: clamp model. It could be clamp-small-512 or clamp-small-1024
    cwd: working directory for prosess
    """
    change_clamp_txt_query(query, path)
    return clamp_output('text', 'music', top_n=top_n, model=model, cwd=cwd)


def change_clamp_music_query(original_query_path: str, clamp_reading_path: str = 'notebooks/clamp/model/inference/') -> None:
    """
    Function for changing music query.

    original_query_path: original music query
    clamp_reading_path: path to clmp
    """
    shutil.copy2(original_query_path, clamp_reading_path + 'music_query.mxl')


def change_clamp_txt_keys(keys: List[str], path: str = 'notebooks/clamp/model/inference/') -> None:
    """
    Function for clamp text keys changing.

    keys: list with string keys
    path: path to clamp
    """
    with open(path + 'text_keys.txt', 'w') as file:
        for key in keys:
            file.write(key + '\n')


def get_output_change_music_query(
    music_query_path: str,
    path: str = 'notebooks/clamp/model/inference/',
    top_n: int = 1,
    model: str = 'sander-wood/clamp-small-512',
    cwd: str = 'notebooks/clamp/model/',
) -> List[Tuple[str, float, float]]:
    """
    Function for getting output for clamp model and music query changing

    music_query_path: name of music query.
    path: path to query file to save
    top_n: size of output files
    model: clamp model. It could be clamp-small-512 or clamp-small-1024
    cwd: working directory for prosess
    """
    change_clamp_music_query(music_query_path, path)
    return clamp_output('music', 'text', top_n=top_n, model=model, cwd=cwd)


def get_output_music_to_music_change_music_query(
    music_query_path: str,
    path: str = 'notebooks/clamp/model/inference/',
    top_n: int = 1,
    model: str = 'sander-wood/clamp-small-512',
    cwd: str = 'notebooks/clamp/model/',
) -> List[Tuple[str, float, float]]:
    """
    Function for getting output for clamp model and music query changing for music to music comparsion.

    music_query_path: name of music query.
    path: path to query file to save
    top_n: size of output files
    model: clamp model. It could be clamp-small-512 or clamp-small-1024
    cwd: working directory for prosess
    """
    change_clamp_music_query(music_query_path, path)
    return clamp_output('music', 'music', top_n=top_n, model=model, cwd=cwd)

def compute_str_query_embeding(query:str) -> Tensor:
    if torch.cuda.is_available():    
        device = torch.device("cuda")
        print('There are %d GPU(s) available.' % torch.cuda.device_count())
        print('We will use the GPU:', torch.cuda.get_device_name(0))

    else:
        device = torch.device("cpu")
    TEXT_MODEL_NAME = 'distilroberta-base'
    # initialize patchilizer, tokenizer, and softmax
    patchilizer = MusicPatchilizer()
    tokenizer = AutoTokenizer.from_pretrained(TEXT_MODEL_NAME)
    softmax = torch.nn.Softmax(dim=1)
    query_decode = unidecode(query)
    query_ids = clamp.encoding_data([query_decode], "text")
    query_feature = clamp.get_features(query_ids, "text")
    return query_feature