import matplotlib.pyplot as plt
from notebooks.clamp import clamp_wrapper as cw
import numpy as np
from typing import List, Tuple
import os

CLAMP_OUTPUT = List[Tuple[str, float, float]]



def save_plot(smaller: CLAMP_OUTPUT, bigger: CLAMP_OUTPUT, query: str, out_type: str = 'similarity', target_dir: str = 'results/clamp/') -> None:
    tp = 1 if out_type == 'probability' else 2
    barWidth = 0.25
    plt.subplots(figsize=(12, 8))
    br1 = np.arange(len(smaller))
    br2 = [x + barWidth for x in br1]
    smaller.sort()
    bigger.sort()
    plt.bar(br1, [tup[tp] for tup in smaller], color='r', width=barWidth, edgecolor='grey', label='clamp-small-512')
    plt.bar(br2, [tup[tp] for tup in bigger], color='g', width=barWidth, edgecolor='grey', label='clamp-small-1024')
    plt.xlabel('Music name', fontweight='bold', fontsize=15)
    plt.ylabel(out_type, fontweight='bold', fontsize=15)
    plt.xticks([r + barWidth for r in range(len(smaller))], [tup[0] for tup in smaller], rotation=90)
    plt.legend()
    plt.tight_layout()

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    plt.savefig(target_dir + query + '.png')


def save_plot_clamp_models_txt_query(query: str, top_n: int = 24) -> None:
    smaller = cw.get_output_change_txt_query(query, top_n=top_n)
    bigger = cw.clamp_output('text', 'music', top_n=top_n, model='sander-wood/clamp-small-1024')
    save_plot(smaller, bigger, query)


def save_plot_clamp_models_music_query(query: str, top_n: int = 24) -> None:
    smaller = cw.get_output_change_music_query(query, top_n=top_n)
    bigger = cw.clamp_output('music', 'text', top_n=top_n, model='sander-wood/clamp-small-1024')
    save_plot(smaller, bigger, query.split('/')[-1])


def save_plot_clamp_models_music_query_music_keys(query: str, top_n: int = 24) -> None:
    smaller = cw.get_output_music_to_music_change_music_query(query, top_n=top_n)
    bigger = cw.clamp_output('music', 'music', top_n=top_n, model='sander-wood/clamp-small-1024')
    save_plot(smaller, bigger, 'm2m' + query.split('/')[-1])


def main():

    cw.change_clamp_txt_keys(
        [
            "this song is loud",
            "this song is quiet",
            "this song is not loud nor quiet",
        ]
    )
    save_plot_clamp_models_music_query("notebooks/clamp/model/inference/music_keys/Gran Torino.mxl")
    save_plot_clamp_models_music_query("notebooks/clamp/model/inference/music_keys/Don't Worry, Be Happy.mxl")
    save_plot_clamp_models_music_query("notebooks/clamp/model/inference/music_keys/Flight of the Bumblebee.mxl")
    save_plot_clamp_models_music_query("notebooks/clamp/model/inference/music_keys/Call Me Maybe.mxl")
    save_plot_clamp_models_music_query("notebooks/clamp/model/inference/music_keys/The Godfather Theme.mxl")
    save_plot_clamp_models_music_query("notebooks/clamp/model/inference/music_keys/Eye of the Tiger.mxl")


if __name__ == '__main__':
    main()
