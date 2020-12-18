import sqlite3

class Pelamar:
    def __init__(self, namalengkap, email, nohp, pendidikan_ter, pengalaman_ker, tgl_applied, list_test_psikologi):
        self.namalengkap = namalengkap
        self.email = email
        self.nohp = nohp
        self.pendidikan_ter = pendidikan_ter
        self.pengalaman_ker = pengalaman_ker
        self.tgl_applied = tgl_applied
        self.list_test_psikologi = list_test_psikologi


class PelamarBidangITBisnis(Pelamar):
    def __init__(self, namalengkap, email, nohp, pendidikan_ter, pengalaman_ker, tgl_applied, list_test_psikologi, list_test_kerja):
        super().__init__(namalengkap, email, nohp, pendidikan_ter, pengalaman_ker, tgl_applied, list_test_psikologi)
        self.list_test_kerja = list_test_kerja


# general utility

def printList(identity):
    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()

    c.execute("SELECT rowid, * FROM pekerjaan")
    conn.commit()

    data_lowongan = list(c.fetchall())

    print("No \t Nama Pekerjaan \t Deskripsi Pekerjaan \t Status Pekerjaan \t Kategori Pekerjaan", end="")
    if identity == "admin":
        print(" \t Nilai Kelulusan Pertanyaan Kerja \t Pertanyaan 1 \t Pertanyaan 2 \t Pertanyaan 3", end="")
        print(" \t Pertanyaan 4 \t Pertanyaan 5", end="")

    print()

    for lowongan in data_lowongan:
        for i in range(0, len(lowongan)):

            if i == 0 and identity == "admin":
                print("{} \t".format(lowongan[i]), end="")
            elif i == 0 and identity == "pelamar":
                print("{} \t\t".format(i+1), end="")

            if i > 0 and i < 5:
                print(lowongan[i], "\t\t", end="")

            if i > 4 and identity == "admin":
                print(lowongan[i], "\t", end="")
        print()

    conn.close()


# pelamar utility

def list_lowongan_pekerjaan_pelamar():
    printList("pelamar")

def input_lowongan_pekerjaan(id):
    print("working on progress")

# admin utility

def list_lowongan_pekerjaan_admin():
    printList("admin")


def list_pelamar_kerja():   # still error
    conn = sqlite3.connect("pelamarkerja.db")
    c = conn.cursor()

    c.execute("SELECT rowid, * FROM pelamar")
    conn.commit()

    list_pelamar = c.fetchall()

    for pelamar in list_pelamar:
        print(pelamar)

    conn.close()


def check_priority_question(list_tambah, pertanyaan):
    check_priority_pertanyaan = input('Apakah pertanyaan "' + pertanyaan + '" merupakan pertanyaan prioritas (1. Ya | 2. Tidak): ')

    if check_priority_pertanyaan == "1":
        pertanyaan = "P" + pertanyaan

    list_tambah.append(pertanyaan)


def tambah_lowongan_pekerjaan():

    n = int(input("Jumlah lowongan pekerjaan yang akan ditambahkan : "))

    for i in range(0, n):
        list_tambah = []
        nama_pekerjaan = input("Nama Pekerjaan : ")
        list_tambah.append(nama_pekerjaan)
        deskripsi_pekerjaan = input("Deskripsi Pekerjaan : ")
        list_tambah.append(deskripsi_pekerjaan)
        status_pekerjaan = input("Status Pekerjaan (Tetap / Intern) : ")
        list_tambah.append(status_pekerjaan)
        kategori_pekerjaan = input("Status Pekerjaan (IT : 1 \tBisnis : 2\tETC : 3): ")
        list_tambah.append(kategori_pekerjaan)
        nilai_lulus = input("Nilai Lulus : ")
        list_tambah.append(nilai_lulus)

        if kategori_pekerjaan != "3":

            for j in range(0, 5):
                pertanyaan = input('Pertanyaan ' + str(j+1) + ' mengenai pekerjaan (Jika tidak ada bisa diisi dengan "pass"): ')

                if pertanyaan != "pass":
                    check_priority_question(list_tambah, pertanyaan)

        i = len(list_tambah)
        while i < 10:
            list_tambah.append("pass")
            i += 1

        list_tambah = tuple(list_tambah)

        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()

        c.execute("INSERT INTO pekerjaan VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", list_tambah)
        conn.commit()

        conn.close()

        print("Berhasil memasukkan data")


def modify_lowongan_pekerjaan():

    id_pekerjaan = input("Masukkan id lowongan pekerjaan yang ingin dimodifikasi : ")

    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()

    c.execute("SELECT * FROM pekerjaan WHERE rowid=(?)", id_pekerjaan)
    conn.commit()

    get_data = c.fetchone()

    print("note : jika tidak ingin diubah maka tulis 'pass'")

    list_modify = []

    list_modify.append(input("Nama pekerjaan : "))
    list_modify.append(input("Deskripsi pekerjaan : "))
    list_modify.append(input("Status pekerjaan : "))
    list_modify.append("pass")
    list_modify.append(input("Nilai Lulus : "))

    for j in range(0, 5):

        if get_data[3] != "3":
            pertanyaan = input('Pertanyaan ' + str(j + 1) + ' : ')
            if pertanyaan != "pass":
                check_priority_question(list_modify, pertanyaan)
            else:
                list_modify.append(pertanyaan)
        else:
            list_modify.append("pass")

    for i in range(0, len(list_modify)):
        if list_modify[i] == "pass":
            list_modify[i] = get_data[i]

    for i in range(5, 9):
        if list_modify[i] == "pass" and list_modify[i+1] != "pass":
            list_modify[i], list_modify[i+1] = list_modify[i+1], list_modify[i]

    c.execute(""" UPDATE pekerjaan SET nama_pekerjaan = ?, deskripsi_pekerjaan = ?, status_pekerjaan = ?,
                kategori_pekerjaan = ?, nilai_lulus = ?, pertanyaan1 = ?,
                pertanyaan2 = ?, pertanyaan3 = ?, pertanyaan4 = ?, pertanyaan5 = ?
                WHERE rowid = ?
    """, (str(list_modify[0]), str(list_modify[1]), str(list_modify[2]), str(list_modify[3])
            ,str(list_modify[4]), str(list_modify[5]), str(list_modify[6]), str(list_modify[7])
            ,str(list_modify[8]), str(list_modify[9]), str(id_pekerjaan)))

    conn.commit()

    print("Sukses memodifikasi data")

    conn.close()


def delete_lowongan_pekerjaan():

    id_pekerjaan = input("Masukkan id lowongan pekerjaan yang ingin dihapus : ")

    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()

    c.execute("DELETE FROM pekerjaan WHERE rowid = ? ", id_pekerjaan)
    conn.commit()

    print("Berhasil dihapus")

    conn.close()


def list_test_psikologi():

    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()

    c.execute("SELECT rowid, * FROM test_psikologi")
    conn.commit()

    list_soal = c.fetchall()

    for soal in list_soal:
        print(soal)

    conn.close()


def tambah_test_psikologi():

    n = int(input("Jumlah pertanyaan psikologi yang akan ditambahkan : "))

    for i in range(0, n):

        soal = input("Masukkan pertanyaan psikologi : ")

        tuple_soal = [soal]
        tuple_soal = tuple(tuple_soal)

        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()

        c.execute("INSERT INTO test_psikologi VALUES (?)", tuple_soal)
        conn.commit()

        conn.close()

        print("Berhasil memasukkan data")


def modify_test_psikologi():

    id_soal = input("Masukkan ID soal psikologi yang ingin diedit : ")
    soal_modify = input("Masukkan pertanyaan baru : ")

    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()

    c.execute("UPDATE test_psikologi SET soal = ? WHERE rowid = ?", (soal_modify, id_soal))
    conn.commit()

    conn.close()

    print("Berhasil mengubah soal")


def hapus_test_psikologi():
    id_soal = input("Masukkan ID soal psikologi yang ingin dihapus : ")
    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()

    c.execute("DELETE FROM test_psikologi WHERE rowid = ? ", str(id_soal))
    conn.commit()

    conn.close()


def menu_psikologi():

    print("1. List Test Psikologi")
    print("2. Input Test Psikologi")
    print("3. Modifikasi Test Psikologi")
    print("4. Hapus Test Psikologi")

    pilihan_menu = input("Pilih menu : ")

    if pilihan_menu == "1":
        list_test_psikologi()
    elif pilihan_menu == "2":
        tambah_test_psikologi()
    elif pilihan_menu == "3":
        modify_test_psikologi()
    elif pilihan_menu == "4":
        hapus_test_psikologi()

# menu admin utility

def menu_utama_admin():

    print("1. List Lowongan Pekerja")
    print("2. Input Lowongan Pekerja")
    print("3. Modifikasi Lowongan Pekerja")
    print("4. Hapus Lowongan Pekerja")
    print("5. Lihat Pelamar Kerja")

    pilihan_menu = input("Pilih menu : ")

    if pilihan_menu == "1":
        list_lowongan_pekerjaan_admin()
    elif pilihan_menu == "2":
        tambah_lowongan_pekerjaan()
    elif pilihan_menu == "3":
        list_lowongan_pekerjaan_admin()
        modify_lowongan_pekerjaan()
    elif pilihan_menu == "4":
        list_lowongan_pekerjaan_admin()
        delete_lowongan_pekerjaan()
    elif pilihan_menu == "5":
        list_pelamar_kerja()

# menu pelamar dan admin

def menu_user():

    print("Selamat datang Pelamar Kerja")
    list_lowongan_pekerjaan_pelamar()
    user_input = input("Input ID pekerjaan yang diinginkan : ")
    input_lowongan_pekerjaan(user_input)


def menu_admin():

    print("Selamat datang di menu Admin")

    i = 0
    while i == 0:

        print("1. Lowongan Kerja")
        print("2. Pertanyaan Test Psikologi")
        print("3. Keluar")


        pilihan_menu = input("Pilih menu : ")

        if pilihan_menu == "1":
            menu_utama_admin()    # lowongan pekerjaan
        elif pilihan_menu == "2":
            menu_psikologi()  # test psikologi
        elif pilihan_menu == "3":
            i = 1
        else:
            print("Pilihan anda salah silahkan ulangi lagi")

# menu utama

print("Program Seleksi Pelamar Kerja")
print("1. Daftar Kerja\t\t2.Admin\t\t3.Keluar Program")

pil_menu = ""

while pil_menu != "3":

    pil_menu = input("Pilihan menu : ")

    if pil_menu == "1":
        menu_user()
    elif pil_menu == "2":

        username = input("Username : ")
        password = input("Password : ")

        if username == "admin" and password == "admin":
            menu_admin()
        else:
            print("Username / Passowrd anda salah")
            print("1. Daftar Kerja\t\t2.Admin\t\t3.Keluar Program")

    elif pil_menu == "3":
        print("Terima kasih sampai jumpa kembali")
    else:
        print("Pilihan anda salah silahkan ulangi lagi")



