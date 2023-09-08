# Bu kod unlicensed (lisanssız) olarak yayınlanmıştır ve herkes tarafından serbestçe kullanılabilir ve değiştirilebilir.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def kNN(input_director):
    # IMDb verilerini içeren "imdb_top_1000.csv" dosyasını okuyun
    data = pd.read_csv("imdb_top_1000.csv")
    
    # Yönetmen, oyuncu ve IMDb puanlarını içeren bir veri çerçevesi oluşturun
    ratings = data[["Director", "Star1", "IMDB_Rating"]]
    ratings = ratings.groupby(['Director', 'Star1'])['IMDB_Rating'].mean().reset_index()

    # Bayesian ortalama ile oyuncu istatistiklerini hesaplayın
    director_stats = ratings.groupby('Star1')[['IMDB_Rating']].agg(['count', 'mean'])
    director_stats.columns = director_stats.columns.droplevel()

    # Oyuncu-yönetmen matrisini oluşturun
    from scipy.sparse import csr_matrix

    def create_matrix(df):
        """
		Veri çerçevesi kullanarak bir oyuncu-yönetmen matrisi oluşturur.

		Argümanlar:
		df (pandas.DataFrame): Yönetmen, oyuncu ve IMDb puanlarını içeren veri çerçevesi.

		Döndürdüğü Değerler:
		X (scipy.sparse.csr_matrix): Oyuncu-yönetmen matrisi.
		star_mapper (dict): Oyuncu adlarını indekslere eşleyen bir sözlük.
		director_mapper (dict): Yönetmen adlarını indekslere eşleyen bir sözlük.
		star_inv_mapper (dict): İndeksleri oyuncu adlarına eşleyen bir sözlük.
		director_inv_mapper (dict): İndeksleri yönetmen adlarına eşleyen bir sözlük.
		"""
        N = len(df['Star1'].unique())
        M = len(df['Director'].unique())
        star_mapper = dict(zip(np.unique(df["Star1"]), list(range(N))))
        director_mapper = dict(zip(np.unique(df["Director"]), list(range(M))))
        star_inv_mapper = dict(zip(list(range(N)), np.unique(df["Star1"])))
        director_inv_mapper = dict(zip(list(range(M)), np.unique(df["Director"])))
        star_index = [star_mapper[i] for i in df['Star1']]
        director_index = [director_mapper[i] for i in df['Director']]
        X = csr_matrix((df["IMDB_Rating"], (director_index, star_index)), shape=(M, N))
        return X, star_mapper, director_mapper, star_inv_mapper, director_inv_mapper

    X, _, director_mapper, _, director_inv_mapper = create_matrix(ratings)

    from sklearn.neighbors import NearestNeighbors

    # Benzer yönetmenleri bulan bir işlev tanımlayın
    def find_similar_directors(director_name, X, k, metric='cosine', show_distance=False):
        """
		Belirli bir oyuncuya benzer yönetmenleri bulur.

		Argümanlar:
		director_name (str): Benzer yönetmenlerini aradığınız yönetmenin adı.
		X (scipy.sparse.csr_matrix): Oyuncu-yönetmen matrisi.
		k (int): Benzer yönetmenlerin sayısı.
		metric (str, optional): Benzerlik metriği (varsayılan 'cosine').
		show_distance (bool, optional): Benzerlik mesafesini gösterme (varsayılan False).

		Döndürdüğü Değerler:
		neighbour_ids (list): Benzer yönetmenlerin adlarını içeren bir liste.
		"""
        neighbour_ids = []
        director_ind = director_mapper[director_name]
        director_vec = X[director_ind]
        k += 1
        kNN = NearestNeighbors(n_neighbors=k, algorithm="brute", metric=metric)
        kNN.fit(X)
        director_vec = director_vec.reshape(1, -1)
        neighbour = kNN.kneighbors(director_vec, return_distance=show_distance)
        for i in range(0, k):
            n = neighbour.item(i)
            neighbour_ids.append(director_inv_mapper[n])
        neighbour_ids.pop(0)
        return neighbour_ids

    director_stars = dict(zip(ratings['Director'], ratings['Star1']))

    # Benzer yönetmenlerin çalıştığı oyuncuları bulun
    similar_ids = find_similar_directors(input_director, X, k=10)

    unique_list = []
    for i in similar_ids:
        if director_stars[i] not in unique_list:
            unique_list.append(director_stars[i])

    return unique_list

if __name__ == "__main__":
    # "Alfred Hitchcock" için benzer yönetmenleri bulun
    unique_list = kNN("Alfred Hitchcock")
    print("Benzer Yönetmenler:")
    for i in unique_list:
        print(i)
