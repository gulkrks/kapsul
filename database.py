# database.py - FilmBot Veritabanı Modülü
import sqlite3

def veritabani_olustur():
    conn = sqlite3.connect("filmbot.db")
    cursor = conn.cursor()

    # Filmler tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS filmler (
            film_id INTEGER PRIMARY KEY AUTOINCREMENT,
            baslik VARCHAR(200) NOT NULL,
            tur VARCHAR(50),
            yil INTEGER,
            yonetmen VARCHAR(100),
            puan DECIMAL(3,1) DEFAULT 0.0
        )
    """)

    # Kullanicilar tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kullanicilar (
            kullanici_id INTEGER PRIMARY KEY AUTOINCREMENT,
            kullanici_adi VARCHAR(50) NOT NULL UNIQUE,
            kayit_tarihi DATE DEFAULT CURRENT_DATE
        )
    """)

    # Puanlar tablosu (FOREIGN KEY ile iliskisel)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS puanlar (
            puan_id INTEGER PRIMARY KEY AUTOINCREMENT,
            kullanici_id INTEGER,
            film_id INTEGER,
            puan INTEGER CHECK(puan BETWEEN 1 AND 5),
            yorum TEXT,
            FOREIGN KEY (kullanici_id) REFERENCES kullanicilar(kullanici_id),
            FOREIGN KEY (film_id) REFERENCES filmler(film_id)
        )
    """)

    conn.commit()
    conn.close()
    print("Veritabani olusturuldu!")


def ornek_filmler_ekle():
    conn = sqlite3.connect("filmbot.db")
    cursor = conn.cursor()

    filmler = [
        ('Esaretin Bedeli', 'Dram', 1994, 'Frank Darabont', 9.3),
        ('Baba', 'Suç', 1972, 'Francis Ford Coppola', 9.2),
        ('Yüzüklerin Efendisi', 'Fantastik', 2003, 'Peter Jackson', 9.0),
        ('Kara Şövalye', 'Aksiyon', 2008, 'Christopher Nolan', 9.0),
        ('Yıldızlararası', 'Bilim Kurgu', 2014, 'Christopher Nolan', 8.7),
        ('Forrest Gump', 'Dram', 1994, 'Robert Zemeckis', 8.8),
        ('Başlangıç', 'Bilim Kurgu', 2010, 'Christopher Nolan', 8.8),
        ('Matrix', 'Bilim Kurgu', 1999, 'Wachowski', 8.7),
        ('Yeşil Yol', 'Dram', 1999, 'Frank Darabont', 8.6),
        ('Terminatör 2', 'Aksiyon', 1991, 'James Cameron', 8.6),
        ('Gladyatör', 'Aksiyon', 2000, 'Ridley Scott', 8.5),
        ('Prestij', 'Gizem', 2006, 'Christopher Nolan', 8.5),
        ('Kumsal', 'Dram', 2023, 'Greta Gerwig', 7.0),
        ('Oppenheimer', 'Dram', 2023, 'Christopher Nolan', 8.5),
        ('Parazit', 'Gerilim', 2019, 'Bong Joon-ho', 8.5),
    ]

    cursor.executemany("INSERT OR IGNORE INTO filmler (baslik, tur, yil, yonetmen, puan) VALUES (?,?,?,?,?)", filmler)
    conn.commit()
    conn.close()
    print(f"{len(filmler)} film eklendi!")


def filmleri_listele():
    conn = sqlite3.connect("filmbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT film_id, baslik, tur, yil, puan FROM filmler ORDER BY puan DESC")
    filmler = cursor.fetchall()
    conn.close()
    return filmler


def ture_gore_filtrele(tur):
    conn = sqlite3.connect("filmbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT baslik, yil, puan FROM filmler WHERE tur = ? ORDER BY puan DESC", (tur,))
    filmler = cursor.fetchall()
    conn.close()
    return filmler


def film_puanla(kullanici_id, film_id, puan, yorum=''):
    conn = sqlite3.connect("filmbot.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO puanlar (kullanici_id, film_id, puan, yorum) VALUES (?,?,?,?)",
                   (kullanici_id, film_id, puan, yorum))
    conn.commit()
    conn.close()
    print("Puanınız kaydedildi!")


if __name__ == '__main__':
    veritabani_olustur()
    ornek_filmler_ekle()
    print('\nTüm filmler:')
    for f in filmleri_listele():
        print(f'  {f[0]}. {f[1]} ({f[3]}) - {f[2]} - ★ {f[4]}')