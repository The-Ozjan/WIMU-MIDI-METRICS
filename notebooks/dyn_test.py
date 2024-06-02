from pathlib import Path
# from .clamp.model.clamp import main as create_embeddings
import numpy as np
from .clamp.statistics import load_json_as_ndarray, normalize_embeddings
import matplotlib.pyplot as plt



if __name__ == '__main__':
    # create_embeddings(Path('aaa'), Path('aaa/emb'), 64)

    # dodawać do wektora kolejno ciche, głośne i dziwne
    embeddings_dir = Path('aaa/emb')
    embedding_files = list(embeddings_dir.glob('**/*.json'))
    names = list(f'{f.stem}.midi' for f in embedding_files)
    embeddings = np.stack(list(load_json_as_ndarray(f) for f in embedding_files))
    embeddings = normalize_embeddings(embeddings)
    dist_matrix = np.zeros((embeddings.shape[0], embeddings.shape[0]))

    # for i in range(embeddings.shape[0]):
    #     for j in range(embeddings.shape[0]):
    #         dist_matrix[i, j] = np.linalg.norm(embeddings[i] - embeddings[j])

    # plt.imshow(dist_matrix)
    # plt.show()
    # wyświetlić wektor 2D w matplotlib
    # Inicjalizacja wynikowych macierzy
    min_wyniki = np.zeros((16, 16, 2), dtype=float)
    max_wyniki = np.zeros((16, 16, 2), dtype=float)

    # Iteracja przez wszystkie pary punktów
    for i in range(16):
        for j in range(16):
            if i != j:  # Unikanie porównywania tego samego punktu z samym sobą
                # Obliczenie różnic w każdej współrzędnej
                roznice = np.abs(embeddings[i] - embeddings[j])
                # Znalezienie współrzędnej, w której różnią się najmniej i najbardziej
                min_indeks = np.argmin(roznice)
                max_indeks = np.argmax(roznice)
                # Zapisanie wyników
                min_wyniki[i, j] = [min_indeks, roznice[min_indeks]]
                max_wyniki[i, j] = [max_indeks, roznice[max_indeks]]

    print(min_wyniki)
    print(max_wyniki)

    plt.subplot(1, 2, 1)
    plt.imshow(min_wyniki[:,:,0], cmap='viridis', interpolation='nearest')
    plt.colorbar()
    plt.title('Indeks najmniejszej różnicy')

    plt.subplot(1, 2, 2)
    plt.imshow(max_wyniki[:,:,0], cmap='viridis', interpolation='nearest')
    plt.colorbar()
    plt.title('Indeks największej różnicy')

    plt.tight_layout()
    plt.show()
