# IMDb Verileri ve Makine Öğrenimi ile Yönetmen Analizi

Bu projede, IMDb verilerini kullanarak farklı yönetmenlerin filmlerinin analizini yapmak için makine öğrenimi teknikleri kullanılmıştır. Proje, Python programlama dili ile geliştirilmiştir ve aşağıda verilen adımları içerir:

1. **Veri Okuma ve Temizleme:**
   - "imdb_top_1000.csv" adlı CSV dosyası okunur.
   - Yönetmen sütunundaki yinelenen değerler kaldırılır ve yinelenenlerin sayısı hesaplanır.
   - Gereksiz sütunlar kaldırılır ve sadece "Yönetmen", "Yinelenenler" ve "IMDB Puanı" sütunları tutulur.

2. **Makine Öğrenimi ile Ortak Önerilerin Hesaplanması:**
   - Her yönetmen için ortak oyuncu önerileri hesaplanır.
   - `collaborative_filter` ve `kNN` fonksiyonları kullanılır.
   - İki öneri listesindeki ortak oyuncu sayısı hesaplanır ve saklanır.

3. **Grafiksel Analiz:**
   - İki farklı grafik çizilir:
     - İlk grafik, yönetmenlerin filmlerinin sayısı ve ortak öneri sayısı arasındaki ilişkiyi gösterir.
     - İkinci grafik, yönetmenlerin en yüksek IMDb puanları ile ortak öneri sayısı arasındaki ilişkiyi gösterir.

4. **Kod Lisansı:**
   - Bu kod, herhangi bir lisans altında serbest bırakılmıştır ve herkes tarafından serbestçe kullanılabilir ve değiştirilebilir.

## Kullanım

- Ana kod dosyası 'driver.py', veriyi okur, analiz yapar ve grafikler oluşturur. Çalıştırmak için Windows'ta 'python driver.py' komutunu çalıştırmalısınız.

## Lisans

Bu kodun herhangi bir lisans altında serbest bırakıldığına dair herhangi bir kısıtlama yoktur. İstediğiniz gibi kullanabilir, değiştirebilir ve dağıtabilirsiniz.

