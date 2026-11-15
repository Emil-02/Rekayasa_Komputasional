# Kamus Konjo — Algoritma Genetika

Kamus bahasa daerah **Konjo** (Sulawesi Selatan) berbasis CLI yang memakai **Algoritma Genetika** untuk "menemukan" kata target di kamus. Semua tahapan GA diimplementasikan dari nol dengan Python murni, tanpa library eksternal, dan setiap langkah ditampilkan agar mudah dipelajari. Proyek ini dibuat untuk mata kuliah Rekayasa Komputasional.

## Fitur

- **Kamus Konjo–Indonesia**: tampilkan seluruh kamus atau cari berdasarkan kata daerah maupun artinya.
- **Populasi awal**: dibangkitkan acak atau diinput manual, panjang individu mengikuti kata target.
- **Fungsi fitness**: jumlah huruf yang cocok pada posisi yang sama ÷ panjang kata target.
- **Seleksi roulette wheel**: probabilitas dan interval kumulatif tiap individu ditampilkan.
- **One-point crossover**: probabilitas crossover (default 0,80) dan titik potong bisa diatur.
- **Mutasi gen**: probabilitas mutasi (default 0,25); posisi dan huruf baru dipilih acak.
- **Generasi baru**: populasi baru bisa dipakai untuk iterasi berikutnya.
- **Mode langkah demi langkah** (menu 3) atau jalankan tiap tahap secara terpisah (menu 4–9).
- Bilangan acak bisa diisi **manual** untuk mencocokkan perhitungan di kertas.

## Cara Menjalankan

Butuh Python 3.8 atau lebih baru.

```bash
git clone https://github.com/Emil-02/Rekayasa_Komputasional.git
cd Rekayasa_Komputasional
python kamus_konjo.py
```

## Contoh Penggunaan

```text
=== Kamus Bahasa Daerah (KONJO) - Algoritma Genetika ===
1. Tampilkan Kamus
2. Cari Kata
3. Jalankan Algoritma Genetika
4. Tampilkan Populasi
5. Hasil Fitness
6. Seleksi Roulette
7. Cross Over
8. Mutasi
9. Generasi Baru
10. Keluar
Pilih menu (1-10): 2
Masukkan kata daerah / arti yang dicari: rumah
Ditemukan 1 hasil:
  - BOLA  =>  Rumah
```

## Alur Algoritma Genetika

```text
Populasi awal → Hitung fitness → Seleksi roulette → Crossover → Mutasi → Generasi baru
      ↑                                                                      │
      └──────────────────────────── ulangi ──────────────────────────────────┘
```

## Isi Kamus

| Konjo | Indonesia | Konjo | Indonesia |
| --- | --- | --- | --- |
| BAKKA | Besar | ANTAMA | Masuk |
| KASSA | Kuat | BARRASA | Menyapu |
| BOLA | Rumah | KUMBALA | Nakal |
| PANRA | Rusak | GAMMARA | Ganteng/Cantik |
| TANRA | Tanda | LUSSA | Kusut |

## Lisensi

Dirilis di bawah lisensi MIT. Lihat [LICENSE](LICENSE).
