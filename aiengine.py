# ai_engine.py - FilmBot Yapay Zeka Öneri Motoru
import sqlite3
from collections import Counter

def kullanici_profili_olustur(kullanici_id):
    """Kullanıcının puanladığı filmlere bakarak tür tercihlerini analiz eder."""
    conn = sqlite3.connect("filmbot.db")
    cursor = conn.cursor()

    # Kullanıcının yüksek puan verdiği filmlerin türlerini bul (JOIN!)
    cursor.execute("""
        SELECT f.tur, p.puan
        FROM puanlar p
        INNER JOIN filmler f ON p.film_id = f.film_id
        WHERE p.kullanici_id = ? AND p.puan >= 4
    """, (kullanici_id,))

    sonuclar = cursor.fetchall()
    conn.close()

    if not sonuclar:
        return {}

    # Tür sıklığını hesapla (basit AI: en çok beğenilen türler)
    tur_sayac = Counter([row[0] for row in sonuclar])
    toplam = sum(tur_sayac.values())
    profil = {tur: round(sayi/toplam, 2) for tur, sayi in tur_sayac.most_common()}
    return profil


def film_oner(kullanici_id, limit=5):
    """Kullanıcının profiline göre henüz izlemediği filmleri önerir."""
    conn = sqlite3.connect("filmbot.db")
    cursor = conn.cursor()

    # Kullanıcının zaten puanladığı filmleri bul
    cursor.execute("SELECT film_id FROM puanlar WHERE kullanici_id = ?", (kullanici_id,))
    puanlanan_filmler = [row[0] for row in cursor.fetchall()]

    # Kullanıcı profilini oluştur
    profil = kullanici_profili_olustur(kullanici_id)

    if not profil:
        # Profil yoksa en yüksek puanlı filmleri öner
        cursor.execute("""
            SELECT film_id, baslik, tur, yil, puan FROM filmler
            ORDER BY puan DESC LIMIT ?
        """, (limit,))
        oneriler = cursor.fetchall()
        conn.close()
        return oneriler

    # Tüm filmleri getir
    cursor.execute("SELECT film_id, baslik, tur, yil, puan FROM filmler")
    tum_filmler = cursor.fetchall()
    conn.close()

    # Öneri skoru hesapla: tür uyumu * film puanı
    skorlar = []
    for film in tum_filmler:
        if film[0] not in puanlanan_filmler:  # Zaten puanlanmamış filmler
            tur_skoru = profil.get(film[2], 0.1)  # Tür uyumu
            toplam_skor = tur_skoru * film[4]     # tür uyumu * imdb puanı
            skorlar.append((film, round(toplam_skor, 2)))

    # Skora göre sırala ve en iyi N filmi döndür
    skorlar.sort(key=lambda x: x[1], reverse=True)
    return [(s[0], s[1]) for s in skorlar[:limit]]


def istatistikler():
    """Veritabanı istatistiklerini gösterir (GROUP BY, COUNT, AVG kullanarak)."""
    conn = sqlite3.connect("filmbot.db")
    cursor = conn.cursor()

    # Türe göre film sayısı ve ortalama puan
    cursor.execute("""
        SELECT tur, COUNT(*) as sayi, ROUND(AVG(puan), 1) as ort_puan
        FROM filmler
        GROUP BY tur
        ORDER BY sayi DESC
    """)
    return cursor.fetchall()


if __name__ == '__main__':
    print('📊 Film İstatistikleri:')
    for stat in istatistikler():
        print(f'  {stat[0]:<15} | {stat[1]} film | Ort: ★ {stat[2]}')