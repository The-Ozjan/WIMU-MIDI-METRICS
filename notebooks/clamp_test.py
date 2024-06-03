import matplotlib.pyplot as plt
from notebooks.clamp import clamp_wrapper as cw
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
from notebooks.clamp.statistics import *
import torch
from torch import Tensor


def calc_avg_dist(query_emb, embed):
    sims = torch.cosine_similarity(query_emb, embed)
    return sims.mean()

def print_table(
    info: pd.DataFrame, embeddings: ArrayLike, author_names_and_occurences: List[Tuple[str, int]], name_to_idx: dict[str, int], query_emb: Tensor
):
    """
    Calculates and displays minimum and maximum variance in the embeddings for all music and for music of each author separately.
    """
    print('|                  Group or author                   | Songs | Avg similar  |')
    print('|----------------------------------------------------|-------|--------------|')
    dist = calc_avg_dist(query_emb, torch.from_numpy(embeddings))
    print(f'| {"Everyone": ^50} | {embeddings.shape[0]: >5} | {dist.item(): 12.9f} |')

    # Variance of embeddings for individual authors
    authors_with_more_than_five_songs = list([name, occ] for [name, occ] in author_names_and_occurences if occ >= 5)
    for [author, _] in authors_with_more_than_five_songs[::-1]:
        single_author_info = info[info[MaestroHeaders.CANONICAL_COMPOSER] == author]
        single_author_idxs = list(name_to_idx[name] for name in single_author_info[MaestroHeaders.MIDI_FILENAME].str[5:])
        single_author_selector = np.array(single_author_idxs, dtype=np.int32)
        single_author_embeddings = embeddings[single_author_selector]
        dist = calc_avg_dist(query_emb, torch.from_numpy(single_author_embeddings))
        print(
            f'| {author: ^50} | {single_author_embeddings.shape[0]: >5} | {dist.item(): 12.9f} |'
        )

def save_plot(smaller: List[Tuple[str, int, int]], bigger: List[Tuple[str, int, int]], query: str) -> None:
    barWidth = 0.25
    fig = plt.subplots(figsize=(12, 8))
    br1 = np.arange(len(smaller))
    br2 = [x + barWidth for x in br1]
    smaller.sort()
    bigger.sort()
    plt.bar(br1, [tup[1] for tup in smaller], color='r', width=barWidth, edgecolor='grey', label='clamp-small-512')
    plt.bar(br2, [tup[1] for tup in bigger], color='g', width=barWidth, edgecolor='grey', label='clamp-small-1024')
    plt.xlabel('Music name', fontweight='bold', fontsize=15)
    plt.ylabel('Probability', fontweight='bold', fontsize=15)
    plt.xticks([r + barWidth for r in range(len(smaller))], [tup[0] for tup in smaller], rotation=90)
    plt.legend()
    plt.tight_layout()
    plt.savefig(query + '.png')


def save_plot_clamp_models_txt_query(query: str, top_n: int = 24) -> None:
    smaller = cw.get_output_change_txt_query(query, top_n=top_n)
    bigger = cw.clamp_output('text', 'music', top_n=24, model='sander-wood/clamp-small-1024')
    save_plot(smaller, bigger, query)


def save_plot_clamp_models_music_query(query: str, top_n: int = 24) -> None:
    smaller = cw.get_output_change_music_query(query, top_n=top_n)
    bigger = cw.clamp_output('music', 'text', top_n=24, model='sander-wood/clamp-small-1024')
    save_plot(smaller, bigger, query.split('/')[-1])


def save_plot_clamp_models_music_query_music_keys(query: str, top_n: int = 24) -> None:
    smaller = cw.get_output_music_to_music_change_music_query(query, top_n=top_n)
    bigger = cw.clamp_output('music', 'music', top_n=24, model='sander-wood/clamp-small-1024')
    save_plot(smaller, bigger, 'm2m' + query.split('/')[-1])


def heatmap_avg_distance_query(query_embed_list: List[str], info: pd.DataFrame, embeddings: ArrayLike, author_names_and_occurences: List[Tuple[str, int]], name_to_idx: dict[str, int]):
    arr = []
    authors_with_more_than_five_songs = list([name, occ] for [name, occ] in author_names_and_occurences if occ >= 5)
    labels = [author for [author, _] in authors_with_more_than_five_songs[::-1]]
    for query in query_embed_list:
        query_emb = cw.compute_str_query_embeding(query)
        row = []
        for [author, _] in authors_with_more_than_five_songs[::-1]:
            single_author_info = info[info[MaestroHeaders.CANONICAL_COMPOSER] == author]
            single_author_idxs = list(name_to_idx[name] for name in single_author_info[MaestroHeaders.MIDI_FILENAME].str[5:])
            single_author_selector = np.array(single_author_idxs, dtype=np.int32)
            single_author_embeddings = embeddings[single_author_selector]
            dist = calc_avg_dist(query_emb, torch.from_numpy(single_author_embeddings))
            row.append(dist.item())
        arr.append(row)

    fig, ax = plt.subplots(nrows=1, ncols=1)

    # Plot Heatmap for keys in track matrix
    matrix = np.array(arr)
    im = ax.imshow(matrix)
    ax.figure.colorbar(im, ax=ax)
    ax.set_xticks(np.arange(len(labels)), labels=labels)
    ax.set_yticks(np.arange(len(query_embed_list)), labels=query_embed_list)
    plt.setp(ax.get_xticklabels(), rotation=90, ha='right', rotation_mode='anchor')
    ax.invert_yaxis()
    ax.set_title('Keys in tracks heatmap')
    plt.tight_layout()
    plt.savefig("query_author_name_test" + '.png')

def main():
    save_plot_clamp_models_txt_query("Love song.")
    save_plot_clamp_models_txt_query("This song genre is Jazz")
    save_plot_clamp_models_txt_query("This song genre is Dance")
    save_plot_clamp_models_txt_query("This song genre is Rock")
    save_plot_clamp_models_txt_query("This song genre is Country")
    save_plot_clamp_models_txt_query("This song is Happy")
    save_plot_clamp_models_txt_query("This song is from movie")

    cw.change_clamp_txt_keys(
        [
            'It is funny.',
            'It is sad.',
            'It is about love.',
            'It is composed for movie.',
            'Clint Eastwood played in film with this music.',
            'Genre of this music is Jazz',
            'Genre of this music is Reggae.',
            'Genre of this music is Rock.',
            'Genre of this music is Classic.',
            'This music could be in mafia movie.',
        ]
    )
    save_plot_clamp_models_music_query("notebooks/clamp/model/inference/music_keys/Gran Torino.mxl")
    save_plot_clamp_models_music_query("notebooks/clamp/model/inference/music_keys/Don't Worry, Be Happy.mxl")
    save_plot_clamp_models_music_query("notebooks/clamp/model/inference/music_keys/Flight of the Bumblebee.mxl")
    save_plot_clamp_models_music_query("notebooks/clamp/model/inference/music_keys/Call Me Maybe.mxl")
    save_plot_clamp_models_music_query("notebooks/clamp/model/inference/music_keys/The Godfather Theme.mxl")
    save_plot_clamp_models_music_query("notebooks/clamp/model/inference/music_keys/Eye of the Tiger.mxl")

    save_plot_clamp_models_music_query_music_keys('notebooks/clamp/model/inference/music_keys/Gran Torino.mxl')
    save_plot_clamp_models_music_query_music_keys("notebooks/clamp/model/inference/music_keys/Don't Worry, Be Happy.mxl")
    save_plot_clamp_models_music_query_music_keys('notebooks/clamp/model/inference/music_keys/Flight of the Bumblebee.mxl')
    save_plot_clamp_models_music_query_music_keys('notebooks/clamp/model/inference/music_keys/Call Me Maybe.mxl')
    save_plot_clamp_models_music_query_music_keys('notebooks/clamp/model/inference/music_keys/The Godfather Theme.mxl')
    save_plot_clamp_models_music_query_music_keys('notebooks/clamp/model/inference/music_keys/Eye of the Tiger.mxl')
    queryEm = cw.compute_str_query_embeding("It is composed by Johannes Brahms")
    info = load_maestro_info()
    (names, embeddings) = load_maestro_clamp_embeddings()
    author_names_and_occurences = list(dict(Counter(info[MaestroHeaders.CANONICAL_COMPOSER].iloc)).items())
    author_names_and_occurences.sort(key=lambda x: x[1])
    name_to_idx = {name: i for i, name in enumerate(names)}
    print_table(info, embeddings, author_names_and_occurences, name_to_idx, queryEm)
    heatmap_avg_distance_query(["It is composed by Johannes Brahms", "It is composed by Frédéric Chopin", "Franz Liszt", "Ludwig van Beethoven", "Robert Schumann"], info, embeddings, author_names_and_occurences, name_to_idx)



if __name__ == '__main__':
    main()
