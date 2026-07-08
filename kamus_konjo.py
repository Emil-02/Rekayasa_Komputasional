import random
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

kamus = [
    {"kata": "BAKKA",   "arti": "Besar"},
    {"kata": "KASSA",   "arti": "Kuat"},
    {"kata": "BOLA",    "arti": "Rumah"},
    {"kata": "PANRA",   "arti": "Rusak"},
    {"kata": "TANRA",   "arti": "Tanda"},
    {"kata": "ANTAMA",  "arti": "Masuk"},
    {"kata": "BARRASA", "arti": "Menyapu"},
    {"kata": "KUMBALA", "arti": "Nakal"},
    {"kata": "GAMMARA", "arti": "Ganteng/Cantik"},
    {"kata": "LUSSA",   "arti": "Kusut"},
]

class GAState:
    def __init__(self):
        self.target = None          
        self.populasi = []          
        self.fitness = []           
        self.jumlah_cocok = []      
        self.probabilitas = []      
        self.interval = []          
        self.parent1 = None
        self.parent2 = None
        self.child1 = None
        self.child2 = None
        self.child1_mutasi = None
        self.child2_mutasi = None
        self.generasi_ke = 0

    def reset_setelah_generasi_baru(self):
        self.fitness = []
        self.jumlah_cocok = []
        self.probabilitas = []
        self.interval = []
        self.parent1 = None
        self.parent2 = None
        self.child1 = None
        self.child2 = None
        self.child1_mutasi = None
        self.child2_mutasi = None


state = GAState()

def hitung_fitness(individu, target):
    """Fitness = jumlah huruf yang cocok pada posisi sama / panjang target"""
    individu = individu.upper()
    target = target.upper()
    panjang = min(len(individu), len(target))
    cocok = sum(1 for i in range(panjang) if individu[i] == target[i])
    fitness = cocok / len(target)
    return cocok, fitness


def ambil_float(prompt, default=None):
    """Input angka float dengan opsi default (Enter = pakai default)."""
    teks = input(prompt).strip()
    if teks == "" and default is not None:
        return default
    try:
        return float(teks)
    except ValueError:
        print(f"  Input tidak valid, memakai nilai default {default}.")
        return default


def cetak_garis(karakter="-", panjang=70):
    print(karakter * panjang)


# =====================================================================
# MENU 1. TAMPILKAN KAMUS
# =====================================================================
def menu_tampilkan_kamus():
    cetak_garis("=")
    print("DAFTAR KAMUS BAHASA DAERAH")
    cetak_garis("=")
    print(f"{'No':<4}{'Kata Daerah':<15}{'Arti (Indonesia)':<20}")
    cetak_garis()
    for i, entri in enumerate(kamus, start=1):
        print(f"{i:<4}{entri['kata']:<15}{entri['arti']:<20}")
    cetak_garis()
    print(f"Total kata dalam kamus : {len(kamus)}")

# =====================================================================
# MENU 2. CARI KATA
# =====================================================================
def menu_cari_kata():
    cetak_garis("=")
    print("CARI KATA DALAM KAMUS")
    cetak_garis("=")
    kunci = input("Masukkan kata daerah / arti yang dicari: ").strip().lower()
    hasil = [e for e in kamus if kunci in e["kata"].lower() or kunci in e["arti"].lower()]
    if hasil:
        print(f"\nDitemukan {len(hasil)} hasil:")
        for e in hasil:
            print(f"  - {e['kata']}  =>  {e['arti']}")
    else:
        print("\nKata tidak ditemukan dalam kamus.")


# =====================================================================
# MENU 4. TAMPILKAN POPULASI (sekaligus inisialisasi target & populasi awal)
# =====================================================================
def menu_tampilkan_populasi(otomatis=False, target_input=None, jumlah_default=4):
    cetak_garis("=")
    print("INISIALISASI / TAMPILKAN POPULASI AWAL")
    cetak_garis("=")

    # ---- pilih kata target ----
    if target_input is None:
        menu_tampilkan_kamus()
        target_input = input("\nMasukkan KATA TARGET (harus ada di kamus): ").strip().upper()

    entri_target = next((e for e in kamus if e["kata"].upper() == target_input), None)
    if entri_target is None:
        print("Kata target tidak ditemukan di kamus. Proses dibatalkan.")
        return
    target = entri_target["kata"].upper()

    # ---- cari kandidat sepanjang target sebagai populasi awal ----
    kandidat = [e["kata"].upper() for e in kamus
                if len(e["kata"]) == len(target) and e["kata"].upper() != target]

    if len(kandidat) < 2:
        print(f"Kata dengan panjang {len(target)} huruf di kamus tidak cukup (min. 2).")
        print("Masukkan individu populasi awal secara manual.")
        populasi = []
        jumlah = int(ambil_float(f"Jumlah individu populasi (default {jumlah_default}): ",
                                  jumlah_default))
        for i in range(jumlah):
            kata = input(f"  Individu {i+1} ({len(target)} huruf): ").strip().upper()
            populasi.append(kata)
    else:
        if otomatis:
            jumlah = min(jumlah_default, len(kandidat))
            populasi = random.sample(kandidat, jumlah)
        else:
            print(f"\nKandidat kata sepanjang {len(target)} huruf yang tersedia di kamus:")
            for i, k in enumerate(kandidat, start=1):
                print(f"  {i}. {k}")
            jumlah = int(ambil_float(
                f"\nBerapa individu diambil sebagai populasi awal? (default {min(jumlah_default, len(kandidat))}): ",
                min(jumlah_default, len(kandidat))))
            jumlah = max(2, min(jumlah, len(kandidat)))
            pilih_manual = input("Pilih manual dari daftar (m) atau acak (a)? [a]: ").strip().lower()
            if pilih_manual == "m":
                populasi = []
                sisa = kandidat.copy()
                for n in range(jumlah):
                    for i, k in enumerate(sisa, start=1):
                        print(f"    {i}. {k}")
                    idx = int(ambil_float(f"  Pilih individu ke-{n+1} (nomor): ", 1)) - 1
                    idx = max(0, min(idx, len(sisa) - 1))
                    populasi.append(sisa.pop(idx))
            else:
                populasi = random.sample(kandidat, jumlah)

    state.target = target
    state.populasi = populasi
    state.reset_setelah_generasi_baru()
    state.generasi_ke = 0

    print(f"\nTarget kata      : {target}  (panjang = {len(target)})")
    print("Populasi awal    :")
    for i, ind in enumerate(populasi, start=1):
        print(f"  Individu {i} = {ind}")


# =====================================================================
# MENU 5. HASIL FITNESS
# =====================================================================
def menu_hasil_fitness():
    if not state.populasi:
        print("Populasi belum dibuat. Jalankan menu 4 (Tampilkan Populasi) dahulu.")
        return None

    cetak_garis("=")
    print("PERHITUNGAN FITNESS")
    cetak_garis("=")
    print(f"Target = {'  '.join(state.target)}   (Panjang = {len(state.target)})\n")

    print(f"{'Individu':<10}{'Kromosom':<12}{'Cocok':<8}{'Fitness':<10}")
    cetak_garis()

    fitness_list = []
    cocok_list = []
    for i, ind in enumerate(state.populasi, start=1):
        cocok, fit = hitung_fitness(ind, state.target)
        fitness_list.append(fit)
        cocok_list.append(cocok)
        print(f"I{i:<9}{ind:<12}{cocok:<8}{cocok}/{len(state.target)} = {fit:.2f}")

    total_fitness = sum(fitness_list)
    cetak_garis()
    print(f"Total Fitness = {' + '.join(f'{f:.2f}' for f in fitness_list)} = {total_fitness:.2f}")

    state.fitness = fitness_list
    state.jumlah_cocok = cocok_list
    return total_fitness


# =====================================================================
# MENU 6. SELEKSI ROULETTE
# =====================================================================
def menu_seleksi_roulette():
    if not state.fitness:
        print("Fitness belum dihitung. Jalankan menu 5 (Hasil Fitness) dahulu.")
        return

    cetak_garis("=")
    print("SELEKSI ROULETTE WHEEL")
    cetak_garis("=")

    total_fitness = sum(state.fitness)
    if total_fitness == 0:
        print("Total fitness = 0, seleksi roulette tidak dapat dilakukan (semua individu buruk).")
        return

    probabilitas = [f / total_fitness for f in state.fitness]

    # bangun interval kumulatif
    interval = []
    kumulatif = 0.0
    for p in probabilitas:
        bawah = kumulatif
        kumulatif += p
        interval.append((bawah, kumulatif))

    state.probabilitas = probabilitas
    state.interval = interval

    print(f"{'Individu':<10}{'Fitness':<10}{'Probabilitas':<15}{'Interval'}")
    cetak_garis()
    for i, ind in enumerate(state.populasi, start=1):
        p_bawah, p_atas = interval[i - 1]
        print(f"I{i:<9}{state.fitness[i-1]:<10.2f}{probabilitas[i-1]:<15.3f}"
              f"{p_bawah:.3f} - {p_atas:.3f}")

    # ---- proses pemilihan parent ----
    print("\nProses Pemilihan Parent (Roulette Wheel):")
    parents = []
    for ke in (1, 2):
        pakai_manual = input(f"  Masukkan bilangan acak r{ke} manual? (y/n) [n]: ").strip().lower()
        if pakai_manual == "y":
            r = ambil_float(f"  r{ke} (0-1): ", random.random())
        else:
            r = random.random()
            print(f"  r{ke} dibangkitkan otomatis = {r:.3f}")

        terpilih_idx = 0
        for i, (bawah, atas) in enumerate(interval):
            if bawah <= r < atas or (i == len(interval) - 1 and r == 1.0):
                terpilih_idx = i
                break
        terpilih = state.populasi[terpilih_idx]
        print(f"  Karena {interval[terpilih_idx][0]:.3f} <= {r:.3f} < "
              f"{interval[terpilih_idx][1]:.3f}, maka terpilih Individu {terpilih_idx+1} "
              f"({terpilih}) sebagai Parent {ke}.\n")
        parents.append(terpilih)

    state.parent1, state.parent2 = parents[0], parents[1]
    print(f"Parent 1 = {state.parent1}")
    print(f"Parent 2 = {state.parent2}")


# =====================================================================
# MENU 7. CROSS OVER (One-Point Crossover)
# =====================================================================
def menu_cross_over():
    if state.parent1 is None or state.parent2 is None:
        print("Parent belum dipilih. Jalankan menu 6 (Seleksi Roulette) dahulu.")
        return

    cetak_garis("=")
    print("CROSSOVER (ONE-POINT CROSSOVER)")
    cetak_garis("=")

    p1, p2 = state.parent1, state.parent2
    panjang = min(len(p1), len(p2))

    prob_co = ambil_float("Probabilitas crossover (default 0.80): ", 0.80)
    pakai_manual = input("Masukkan bilangan acak crossover manual? (y/n) [n]: ").strip().lower()
    if pakai_manual == "y":
        r = ambil_float("Bilangan acak (0-1): ", random.random())
    else:
        r = random.random()
        print(f"Bilangan acak dibangkitkan otomatis = {r:.3f}")

    if r < prob_co:
        titik_default = panjang // 2 if panjang > 2 else 1
        titik = int(ambil_float(
            f"Titik potong (1..{panjang-1}, default {titik_default}): ", titik_default))
        titik = max(1, min(titik, panjang - 1))

        child1 = p1[:titik] + p2[titik:]
        child2 = p2[:titik] + p1[titik:]

        print(f"\nCrossover DILAKUKAN karena r={r:.3f} < probabilitas={prob_co:.2f}")
        print(f"  Parent 1: {p1[:titik]} | {p1[titik:]}")
        print(f"  Parent 2: {p2[:titik]} | {p2[titik:]}")
        print(f"  Child 1 = {p1[:titik]} + {p2[titik:]} = {child1}")
        print(f"  Child 2 = {p2[:titik]} + {p1[titik:]} = {child2}")
    else:
        child1, child2 = p1, p2
        print(f"\nCrossover TIDAK dilakukan karena r={r:.3f} >= probabilitas={prob_co:.2f}")
        print(f"  Child 1 = Parent 1 = {child1}")
        print(f"  Child 2 = Parent 2 = {child2}")

    state.child1, state.child2 = child1, child2


# =====================================================================
# MENU 8. MUTASI
# =====================================================================
def menu_mutasi():
    if state.child1 is None or state.child2 is None:
        print("Belum ada child hasil crossover. Jalankan menu 7 (Cross Over) dahulu.")
        return

    cetak_garis("=")
    print("MUTASI GEN")
    cetak_garis("=")

    prob_mut = ambil_float("Probabilitas mutasi (default 0.25): ", 0.25)

    hasil = []
    for label, child in (("Child 1", state.child1), ("Child 2", state.child2)):
        print(f"\n{label} ({child}):")
        pakai_manual = input("  Masukkan bilangan acak mutasi manual? (y/n) [n]: ").strip().lower()
        if pakai_manual == "y":
            r = ambil_float("  Bilangan acak (0-1): ", random.random())
        else:
            r = random.random()
            print(f"  Bilangan acak dibangkitkan otomatis = {r:.3f}")

        if r < prob_mut:
            posisi = random.randrange(len(child))
            huruf_baru = random.choice(ALPHABET)
            baru = child[:posisi] + huruf_baru + child[posisi + 1:]
            print(f"  Mutasi DILAKUKAN karena r={r:.3f} < probabilitas={prob_mut:.2f}")
            print(f"  Posisi gen ke-{posisi+1} ('{child[posisi]}') diubah menjadi '{huruf_baru}'")
            print(f"  Hasil mutasi {label}: {baru}")
            hasil.append(baru)
        else:
            print(f"  Mutasi TIDAK dilakukan karena r={r:.3f} >= probabilitas={prob_mut:.2f}")
            print(f"  {label} tetap: {child}")
            hasil.append(child)

    state.child1_mutasi, state.child2_mutasi = hasil[0], hasil[1]


# =====================================================================
# MENU 9. GENERASI BARU
# =====================================================================
def menu_generasi_baru():
    if state.child1_mutasi is None or state.child2_mutasi is None:
        print("Belum ada hasil mutasi. Jalankan menu 8 (Mutasi) dahulu.")
        return

    state.generasi_ke += 1
    cetak_garis("=")
    print(f"HASIL GENERASI KE-{state.generasi_ke}")
    cetak_garis("=")

    anak = [state.child1_mutasi, state.child2_mutasi]
    print(f"{'Keturunan':<12}{'Kromosom':<12}{'Cocok':<8}{'Fitness'}")
    cetak_garis()
    fitness_baru = []
    for i, ind in enumerate(anak, start=1):
        cocok, fit = hitung_fitness(ind, state.target)
        fitness_baru.append(fit)
        print(f"Child {i:<6}{ind:<12}{cocok:<8}{cocok}/{len(state.target)} = {fit:.2f}")

    terbaik_idx = fitness_baru.index(max(fitness_baru))
    print(f"\nFitness tertinggi generasi ke-{state.generasi_ke}: "
          f"{max(fitness_baru):.2f} melalui {anak[terbaik_idx]}")

    if max(fitness_baru) >= 1.0:
        print(f">>> Target '{state.target}' TERCAPAI! Solusi optimal ditemukan: {anak[terbaik_idx]}")
    else:
        print(">>> Solusi optimal (fitness = 1.0) belum tercapai.")

    lanjut = input("\nGunakan populasi baru ini untuk generasi berikutnya? (y/n) [n]: ").strip().lower()
    if lanjut == "y":
        # Populasi baru minimal berisi 2 individu (anak); individu lama tetap
        # bisa dipertahankan agar ukuran populasi konsisten jika diperlukan.
        state.populasi = anak
        state.reset_setelah_generasi_baru()
        print("Populasi telah diperbarui dengan hasil generasi ini.")
    else:
        print("Populasi tidak diperbarui. Anda bisa mengulang seleksi/crossover/mutasi (menu 6-9).")


# =====================================================================
# MENU 3. JALANKAN ALGORITMA GENETIKA (otomatis, 1 generasi penuh)
# =====================================================================
def menu_jalankan_ga():
    cetak_garis("#")
    print("MENJALANKAN ALGORITMA GENETIKA (1 GENERASI PENUH)")
    cetak_garis("#")

    menu_tampilkan_populasi()
    if not state.populasi:
        return

    input("\nTekan ENTER untuk melanjutkan ke perhitungan fitness...")
    menu_hasil_fitness()

    input("\nTekan ENTER untuk melanjutkan ke seleksi roulette...")
    menu_seleksi_roulette()

    input("\nTekan ENTER untuk melanjutkan ke crossover...")
    menu_cross_over()

    input("\nTekan ENTER untuk melanjutkan ke mutasi...")
    menu_mutasi()

    input("\nTekan ENTER untuk melihat hasil generasi baru...")
    menu_generasi_baru()


# =====================================================================
# MENU UTAMA
# =====================================================================
def tampilkan_menu():
    print()
    cetak_garis("=")
    print("=== Kamus Bahasa Daerah (KONJO) - Algoritma Genetika ===")
    cetak_garis("=")
    print("1. Tampilkan Kamus")
    print("2. Cari Kata")
    print("3. Jalankan Algoritma Genetika")
    print("4. Tampilkan Populasi")
    print("5. Hasil Fitness")
    print("6. Seleksi Roulette")
    print("7. Cross Over")
    print("8. Mutasi")
    print("9. Generasi Baru")
    print("10. Keluar")
    cetak_garis("=")


def main():
    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu (1-10): ").strip()

        if pilihan == "1":
            menu_tampilkan_kamus()
        elif pilihan == "2":
            menu_cari_kata()
        elif pilihan == "3":
            menu_jalankan_ga()
        elif pilihan == "4":
            menu_tampilkan_populasi()
        elif pilihan == "5":
            menu_hasil_fitness()
        elif pilihan == "6":
            menu_seleksi_roulette()
        elif pilihan == "7":
            menu_cross_over()
        elif pilihan == "8":
            menu_mutasi()
        elif pilihan == "9":
            menu_generasi_baru()
        elif pilihan == "10":
            print("Terima kasih. Program selesai.")
            break
        else:
            print("Pilihan tidak valid, silakan pilih 1-10.")
if __name__ == "__main__":
    main()