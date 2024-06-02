from .clamp import midi_to_abc as ma


from pathlib import Path  # noqa: E402




musics = []
out = []


# Choose a file from the dataset by putting its index here
# The index should be the zero-based index of a file converted by MusPy when setting up the dataset
# file_index: int = 199
file_names = [
    #p/mp
    'Beethoven/2451_qt06_2.mid',
    'Bach/2201_prelude16.mid',
    'Bach/2209_fugue4.mid',
    'Bach/2210_prelude4.mid',
    'Bach/2212_prelude12.mid',
    'Bach/2229_fugue20.mid',
    'Schubert/1727_schubert_op114_2.mid',
    #mf/f
    'Beethoven/2423_ps01_02.mid',
    'Bach/2217_cs3-1pre.mid',
    'Bach/2219_cs3-3cou.mid',
    'Bach/2222_cs3-6gig.mid',
    'Beethoven/2590_ps12_03.mid',
    #high dynamic range / ambiguous
    'Beethoven/2480_qt05_1.mid',
    'Beethoven/2586_vcs4_2.mid',
    'Beethoven/2572_bevs7c.mid',
    'Beethoven/2571_bevs7b.mid',
]

# Alternatively you can put a full (relative or absolute) path to a MIDI file to be processed here
# Leave empty to use the file_index field
full_file_path: str = './data/raw/musicnet/musicnet_midis/'
abc_path = './data/raw/musicnet/abcs'
cnt = ma.Counter(len(musics))


full_path_used = full_file_path != ''
i = 0
for file_name in file_names:
    i += 1
    if full_path_used:
        path = Path(full_file_path + file_name)
    #     music = mp.read_midi(path)

    ma.try_midi_to_abc(path, Path('./aaa/' + file_name + '.abc'), cnt)

# ma.try_midi_to_abc(Path('D:/1727_schubert_op114_2.mid'), Path('./notebooks/midis/1727_schubert_op114_2.abc'), cnt)
