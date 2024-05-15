import matplotlib.pyplot as plt
from notebooks.clamp import clamp_wrapper as cw
import numpy as np 
import matplotlib.pyplot as plt 
from typing import Dict, List, Tuple

def test(query:str):
    cw.change_clamp_txt_query(query)
    return cw.clamp_output("text", "music", top_n=24)

def save_plot(smaller:List[Tuple[str, int, int]], bigger:List[Tuple[str, int, int]], query:str) ->None:
    barWidth = 0.25
    fig = plt.subplots(figsize =(12, 8)) 
    br1 = np.arange(len(smaller)) 
    br2 = [x + barWidth for x in br1] 
    smaller.sort()
    bigger.sort()
    plt.bar(br1, [tup[1] for tup in smaller], color ='r', width = barWidth, 
            edgecolor ='grey', label ='clamp-small-512') 
    plt.bar(br2, [tup[1] for tup in bigger], color ='g', width = barWidth, 
            edgecolor ='grey', label ='clamp-small-1024') 
    plt.xlabel('Music name', fontweight ='bold', fontsize = 15) 
    plt.ylabel('Probability', fontweight ='bold', fontsize = 15) 
    plt.xticks([r + barWidth for r in range(len(smaller))], 
            [tup[0] for tup in smaller], rotation=90)
    plt.legend()
    plt.tight_layout()
    plt.savefig(query+'.png')

def save_plot_clamp_models_txt_query(query:str, top_n:int=24) -> None:
    smaller = cw.get_output_change_txt_query(query, top_n=top_n)
    bigger = cw.clamp_output("text", "music", top_n=24, model="sander-wood/clamp-small-1024")
    save_plot(smaller, bigger, query)

def save_plot_clamp_models_music_query(query:str, top_n:int = 24) -> None:
    smaller = cw.get_output_change_music_query(query, top_n=top_n)
    bigger = cw.clamp_output("music", "text", top_n=24, model="sander-wood/clamp-small-1024")
    save_plot(smaller, bigger, query.split('/')[-1])


def main():
    cw.change_clamp_txt_keys(["It is funny.", "It is sad.", "It is about love", "It is composed for movie", "Clint Eastwood played in fil with this music."])
    save_plot_clamp_models_txt_query("Love song.")
    save_plot_clamp_models_music_query("notebooks/clamp/model/inference/music_keys/Gran Torino.mxl")
    save_plot_clamp_models_txt_query("This song genre is Jazz")
    save_plot_clamp_models_txt_query("This song genre is Dance")
    save_plot_clamp_models_txt_query("This song genre is Rock")
    save_plot_clamp_models_txt_query("This song genre is Country")
    save_plot_clamp_models_txt_query("This song is Happy")
    save_plot_clamp_models_txt_query("This song is from movie")



if __name__ == "__main__":
    main()
