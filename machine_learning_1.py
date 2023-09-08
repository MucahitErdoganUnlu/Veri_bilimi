# Bu kod unlicensed (lisanssız) olarak yayınlanmıştır ve herkes tarafından serbestçe kullanılabilir ve değiştirilebilir.

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def collaborative_filter(input_director):
    # IMDb verilerini içeren CSV dosyasını oku
    star_ratings = pd.read_csv("imdb_top_1000.csv")

    # Yönetmen-Oyuncu matrisini oluştur, burada satırlar yönetmenleri, sütunlar oyuncuları ve değerler ise imdb puanlarını temsil eder
    director_star_ratings = star_ratings.pivot_table(index='Director', columns='Star1', values='IMDB_Rating', aggfunc='mean')

    # NaN (boş) değerleri 0 ile doldur (eksik puanları 0 olarak kabul ediyoruz)
    director_star_ratings = director_star_ratings.fillna(0)

    # Yönetmenler arasındaki benzerliği hesapla (kosinüs benzerliği kullanılır)
    director_similarity = cosine_similarity(director_star_ratings)

    # Benzerlik puanlarını saklamak için bir DataFrame oluştur
    director_similarity_df = pd.DataFrame(director_similarity, index=director_star_ratings.index, columns=director_star_ratings.index)

    # Verilen bir yönetmen için oyuncu önerileri yapmak için bir işlev tanımla
    def get_similar_directors(Director, num_recommendations=5):
        # Kullanıcının puanlarını al
        director_ratings = director_star_ratings.loc[Director]

        # Yönetmen benzerliğini kullanarak yönetmenin puanlarının ağırlıklı ortalamasını hesapla
        similar_directors = director_similarity_df[Director].sort_values(ascending=False)[1:]  # Kullanıcıyı dışarıda bırak
        recommendations = director_star_ratings.mul(similar_directors, axis=0).sum(axis=1) / (similar_directors.sum())
        
        # Önerileri tahmini puanlara göre sırala
        recommended_stars = recommendations.sort_values(ascending=False)
        
        # En iyi N öneriyi al
        top_recommendations = recommended_stars.head(num_recommendations)
        
        return top_recommendations

    # Belirli bir yönetmen için benzerliği yüksek yönetmenleri al
    recommendations = get_similar_directors(input_director)

    # Önerilen oyuncuları saklamak için benzersiz bir liste oluştur
    unique_list = []

    for director, point in recommendations.items():
        if(point != 0.0):
            # Benzerliği yüksek yönetmenlerin çalıştığı oyuncu listesini al
            list_of_stars = star_ratings.loc[star_ratings['Director'] == director, 'Star1'].to_list()
            for star in list_of_stars:
                if star not in unique_list:
                    unique_list.append(star)

    # Oyuncuları döndür
    return unique_list

if __name__ == "__main__":
    # Örnek olarak "Alfred Hitchcock" için film önerilerini al
    unique_list = collaborative_filter("Alfred Hitchcock")
    
    # Önerilen oyuncuları ekrana yazdır
    for star in unique_list:
        print(star)
