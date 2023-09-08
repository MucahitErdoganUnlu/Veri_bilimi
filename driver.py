# Bu kod unlicensed (lisanssız) olarak yayınlanmıştır ve herkes tarafından serbestçe kullanılabilir ve değiştirilebilir.
# Bu dosya ana kod dosyasıdır. Projeyi kullanmak için bu dosyayı çalıştırın.
 
from machine_learning_1 import collaborative_filter  # collaborative_filter fonksiyonunu içe aktar
from machine_learning_2 import kNN  # kNN fonksiyonunu içe aktar
import pandas as pd  # pandas kütüphanesini içe aktar
import matplotlib.pyplot as plt  # matplotlib kütüphanesini içe aktar

# IMDb verilerini içeren CSV dosyasını oku
df = pd.read_csv("imdb_top_1000.csv")

# Yönetmen sütunundaki yinelenen değerleri kaldır ve yinelenen sayısını hesapla
df_no_duplicates = df.drop_duplicates(subset='Director', keep='first')
df_no_duplicates['Repetitions'] = df.groupby('Director')['Director'].transform('count')

# Gereksiz sütunları kaldır ve sadece 'Director', 'Repetitions' ve 'IMDB_Rating' sütunlarını tut
df_no_duplicates = df_no_duplicates[["Director", "Repetitions", "IMDB_Rating"]]

# Tekrarlanmayan yönetmenleri bir listeye al
nonrepeating_director_list = df['Director'].drop_duplicates().tolist()

# Her yönetmen için ortak önerilerin sayısını hesapla ve sakla
list_mutual_recomm = []

# Performans ölçümü için doğru önerilen oyuncu sayılarını tut
list_performans_coll_filter = []
list_performans_kNN = []
for director in nonrepeating_director_list:
    list_coll = collaborative_filter(director)
    list_kNN = kNN(director)

    # İki öneri sistemini kıyaslama
    n_mutual = 0
    for star in list_coll:
        if star in list_kNN:
            n_mutual += 1

    list_mutual_recomm.append(n_mutual)

    # collaborative_filter için performans ölçümü
    performans_director_star = df[df['Director'] == director]["Star1"].tolist()
    performans_coll_filter = 0
    performans_kNN = 0

    for star_performans in performans_director_star:
        if star_performans in list_coll:
            performans_coll_filter += 1
        if star_performans in list_kNN:
            performans_kNN += 1
    list_performans_coll_filter.append(performans_coll_filter)
    list_performans_kNN.append(performans_kNN)

# Performansları yeni sütunlara yazdır
df_no_duplicates["Performans_Coll_Filter"] = list_performans_coll_filter
df_no_duplicates["Performans_kNN"] = list_performans_kNN

# IMDB puanına göre artan şekilde veri çerçevesini sırala
df_for_performans = df_no_duplicates.sort_values(by="IMDB_Rating", ascending=True)

# İlk grafik: IMDB puanı ve Collaborative Filtering'in Doğru Öneri Sayısı
plt.scatter(x=df_for_performans["IMDB_Rating"], y=df_for_performans["Performans_Coll_Filter"], alpha=0.1)

# Eksen etiketlerini ve başlığı ekleyin
plt.xlabel('Yönetmenin en yüksek IMDB puanına sahip filminin puanı')
plt.ylabel('Collabortive Filtering Algoritmasının Doğru Önerdiği Oyuncu Sayısı')
plt.title('Collabortive Filtering için IMDB Puanına Bağlı Performans Ölçümü (alpha=0.1)')
plt.show()

# İkinci grafik: IMDB puanı ve kNN'in Doğru Öneri Sayısı
plt.scatter(x=df_for_performans["IMDB_Rating"], y=df_for_performans["Performans_kNN"], alpha=0.1)

# Eksen etiketlerini ve başlığı ekleyin
plt.xlabel('Yönetmenin en yüksek IMDB puanına sahip filminin puanı')
plt.ylabel('kNN Algoritmasının Doğru Önerdiği Oyuncu Sayısı')
plt.title('kNN için IMDB Puanına Bağlı Performans Ölçümü (alpha=0.1)')
plt.show()

# Yönetmen verilerine ortak öneri sayılarını ekleyin ve sıralayın
df_no_duplicates["Mutual_Star_Count"] = list_mutual_recomm
df_no_duplicates = df_no_duplicates.sort_values(by="Mutual_Star_Count", ascending=True)

# Üçüncü grafik: Ortak öneri sayısı ve yönetmenin film sayısı arasındaki ilişki
plt.scatter(x=df_no_duplicates["Mutual_Star_Count"], y=df_no_duplicates["Repetitions"], alpha=0.1)

# Eksen etiketlerini ve başlığı ekleyin
plt.xlabel('İki makine öğrenmesinin ortak önerilerinin bir yönetmen için toplam sayısı')
plt.ylabel('Bir yönetmenin ilk 1000\'deki film sayısı')
plt.title('Ortak önerilerin yönetmenin film sayısıyla karşılaştırılması (alpha=0.1)')
plt.show()

# Dördüncü grafik: Ortak öneri sayısı ve yönetmenin en yüksek IMDb puanı arasındaki ilişki
plt.scatter(x=df_no_duplicates["Mutual_Star_Count"], y=df_no_duplicates["IMDB_Rating"], alpha=0.1)
plt.ylim(7, None)
plt.xlabel('İki makine öğrenmesinin ortak önerilerinin bir yönetmen için toplam sayısı')
plt.ylabel('Yönetmenin en yüksek IMDB puanına sahip filminin puanı')
plt.title('Ortak önerilerin sayısının yönetmenin filmlerinin IMDB puanıyla karşılaştırılması (alpha=0.1)')
plt.show()
