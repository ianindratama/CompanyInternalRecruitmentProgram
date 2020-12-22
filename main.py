import sqlite3
import datetime


class Utility:

    @staticmethod
    def retrievedata(identity):
        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()

        c.execute("SELECT rowid, * FROM " + identity)
        conn.commit()

        data = list(c.fetchall())

        conn.close()
        return data

    def printlist(self):

        data_lowongan = self.retrievedata("pekerjaan")

        print("No \t Nama Pekerjaan \t Deskripsi Pekerjaan \t Status Pekerjaan", end="")

        return data_lowongan


class MenuPelamar(Utility):

    def printlist(self):

        data_lowongan = super().printlist()
        print()

        counter = 1
        for lowongan in data_lowongan:
            print("{} \t\t".format(counter), end="")
            counter += 1
            for i in range(0, len(lowongan)):

                if i != 0 and i < 4:
                    print(lowongan[i], "\t\t", end="")

            print()

    def __get_id_pekerjaan(self, no):
        data = super(MenuPelamar, self).retrievedata("pekerjaan")
        return data[no][0]

    def __get_nama_pekerjaan(self, no):
        data = super(MenuPelamar, self).retrievedata("pekerjaan")
        return data[no][1]

    def __get_soal_kerja(self, no):

        data = super(MenuPelamar, self).retrievedata("pekerjaan")

        soal = list()

        for i in range(6, 11):
            soal.append(str(data[no][i]).replace("P", "", 1))

        return soal

    def __get_soal_psikologi(self):

        data = super(MenuPelamar, self).retrievedata("test_psikologi")

        soal = list()

        for i in range(0, 5):
            soal.append(data[i][1])

        return soal

    def menu_utama(self):
        print("Selamat datang Pelamar Kerja")
        self.printlist()

    def get_all_soal(self):

        user_input = int(input("Input No pekerjaan yang diinginkan : "))

        no_pekerjaan = user_input-1

        return [self.__get_id_pekerjaan(no_pekerjaan), self.__get_nama_pekerjaan(no_pekerjaan),
                self.__get_soal_kerja(no_pekerjaan), self.__get_soal_psikologi()]


class Pelamar(MenuPelamar):

    def __init__(self, data):

        self.__id_pekerjaan = data[0]
        self.__status_kelulusan = "-"

        print("Isi Data Diri")
        self.__nama_lengkap = input("Nama Lengkap : ")
        self.__email = input("Email : ")
        self.__no_hp = input("No HP : ")
        self.__jenis_kelamin = input("Jenis Kelamin (L : Laki - Laki | P : Perempuan) : ")
        self.__pendidikan_terakhir = input("Pendidikan terakhir : ")
        self.__lama_pengalaman_kerja = input("Pengalaman Kerja (dalam tahun ex : 5) : ")

        x = datetime.datetime.now()
        self.__tanggal_applied = x.strftime("%d/%m/%Y")

        print("Pertanyaan mengenai Lowongan Pekerjaan " + data[1])
        print("5 : Sangat Bisa | 4 : Cukup Bisa | 3 : Bisa | 2 : Kurang Bisa | 1 : Tidak Bisa")

        self.__tuple_jawaban_kerja = list()

        for s in data[2]:
            self.__tuple_jawaban_kerja.append(input("" + s + " : "))

        self.__tuple_jawaban_kerja = tuple(self.__tuple_jawaban_kerja)

        print("Test Psikologi")
        print("5 : Sangat Setuju | 4 : Cukup Setuju | 3 : Setuju | 2 : Kurang Setuju | 1 : Tidak Setuju")

        self.__tuple_jawaban_psikologi = list()

        for s in data[3]:
            self.__tuple_jawaban_psikologi.append(input("" + s + " : "))

        self.__tuple_jawaban_psikologi = tuple(self.__tuple_jawaban_psikologi)

        self.__tuple_jawaban_gabungan = self.__tuple_jawaban_kerja + self.__tuple_jawaban_psikologi

        self.__tupleData_send_to_database = (self.__id_pekerjaan, self.__status_kelulusan, self.__nama_lengkap,
                                             self.__email, self.__no_hp, self.__jenis_kelamin,
                                             self.__pendidikan_terakhir, self.__lama_pengalaman_kerja,
                                             self.__tanggal_applied)

        self.__tupleData_send_to_database = self.__tupleData_send_to_database + self.__tuple_jawaban_gabungan

    def send_to_database(self):
        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()

        c.execute("INSERT INTO pelamar VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  self.__tupleData_send_to_database)
        conn.commit()

        c.execute("SELECT last_insert_rowid()")

        id_pelamar = c.lastrowid

        conn.close()

        return id_pelamar


class Evaluate(Utility):

    def __init__(self, id_pelamar):
        self.__id_pelamar = id_pelamar

    def retrievedata(self):

        # retrive data pelamar
        data = super(Evaluate, self).retrievedata("pelamar")

        data_pelamar = list()

        for d in data:
            if self.__id_pelamar == d[0]:
                data_pelamar = d

        # retrieve data pekerjaan
        data = super(Evaluate, self).retrievedata("pekerjaan")

        data_pekerjaan = list()

        for d in data:
            if data_pelamar[1] == str(d[0]):
                data_pekerjaan = d

        # retrieve data soal kerja
        data_soal_kerja = list()

        for i in range(0, len(data_pekerjaan)):
            if i > 5:
                data_soal_kerja.append(data_pekerjaan[i])

        # retrieve data jawaban kerja
        data_jawaban_kerja = list()
        data_jawaban_psikologi = list()

        for i in range(0, len(data_pelamar)):
            if 9 < i < 15:
                data_jawaban_kerja.append(data_pelamar[i])
            elif i >= 15:
                data_jawaban_psikologi.append(data_pelamar[i])

        data_jawaban_gabungan = [data_jawaban_kerja, data_jawaban_psikologi]

        # retrieve data nilai minimum kelulusan untuk setiap test_psikologi
        data = super(Evaluate, self).retrievedata("test_psikologi")
        data_nilai_minimum_kelulusan_psikologi = list()
        data_nilai_maximum_kelulusan_psikologi = list()

        for d in data:
            data_nilai_minimum_kelulusan_psikologi.append(int(d[2]))
            data_nilai_maximum_kelulusan_psikologi.append(int(d[3]))

        data_nilai_kelulusan_psikologi = [data_nilai_minimum_kelulusan_psikologi,
                                          data_nilai_maximum_kelulusan_psikologi]

        return [data_pelamar, data_pekerjaan, data_soal_kerja,
                data_jawaban_gabungan, data_nilai_kelulusan_psikologi]

    def analisa_kelulusan(self, data):

        # analisa jawaban kerja

        nilai_kerja = 0

        for i in range(0, len(data[2])):
            if data[2][i][0] == "P":
                if int(data[3][0][i]) >= 4:
                    nilai_kerja += int(data[3][0][i])
                else:
                    nilai_kerja = 0
                    break
            else:
                nilai_kerja += int(data[3][0][i])

        # analisa jawaban psikologi

        counter_kelulusan_psikologi = 0

        for j in range(0, len(data[3][1])):
            if int(data[4][0][j]) <= int(data[3][1][j]) <= int(data[4][1][j]):
                counter_kelulusan_psikologi += 1

        # analisa kelulusan dan modify status kelulusan di database

        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()

        if nilai_kerja >= int(data[1][5]) and counter_kelulusan_psikologi >= 3:
            c.execute("UPDATE pelamar SET status_kelulusan = ? WHERE rowid = ?", ("Lulus", data[0][0]))
            conn.commit()
        else:
            c.execute("UPDATE pelamar SET status_kelulusan = ? WHERE rowid = ?", ("Tidak Lulus", data[0][0]))
            conn.commit()

        conn.close()


class Admin(Utility):

    def __init__(self):
        pass

    # lowongan kerja panel

    def printlist(self):

        data_lowongan = super().printlist()

        print(" \t Nilai Kelulusan Pertanyaan Kerja \t Pertanyaan 1 \t Pertanyaan 2 \t Pertanyaan 3", end="")
        print(" \t Kategori Pekerjaan \t Pertanyaan 4 \t Pertanyaan 5")

        for lowongan in data_lowongan:
            for i in range(0, len(lowongan)):

                if i < 5:
                    print(lowongan[i], "\t\t", end="")
                else:
                    print(lowongan[i], "\t", end="")

            print()

    @staticmethod
    def __check_priority_question(pertanyaan):
        check_priority_pertanyaan = input(
            'Apakah pertanyaan "' + pertanyaan + '" merupakan pertanyaan prioritas (1. Ya | 2. Tidak): ')

        if check_priority_pertanyaan == "1":
            pertanyaan = "P" + pertanyaan

        return pertanyaan

    def __tambah_lowongan_pekerjaan(self):
        n = int(input("Jumlah lowongan pekerjaan yang akan ditambahkan : "))

        for i in range(0, n):
            list_tambah = []
            nama_pekerjaan = input("Nama Pekerjaan : ")
            list_tambah.append(nama_pekerjaan)
            deskripsi_pekerjaan = input("Deskripsi Pekerjaan : ")
            list_tambah.append(deskripsi_pekerjaan)
            status_pekerjaan = input("Status Pekerjaan (Tetap / Intern) : ")
            list_tambah.append(status_pekerjaan)
            kategori_pekerjaan = input("Kategori Pekerjaan (IT : 1 \tBisnis : 2\tETC : 3): ")
            list_tambah.append(kategori_pekerjaan)
            nilai_lulus = input("Nilai Lulus : ")
            list_tambah.append(nilai_lulus)

            for j in range(0, 5):
                list_tambah.append(self.__check_priority_question(
                    input('Pertanyaan ' + str(j + 1) + ' mengenai pekerjaan : '))
                )

            conn = sqlite3.connect("jobs.db")
            c = conn.cursor()

            c.execute("INSERT INTO pekerjaan VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", tuple(list_tambah))
            conn.commit()

            conn.close()

            print("Berhasil memasukkan data")

    def __modify_lowongan_pekerjaan(self):

        id_pekerjaan = input("Masukkan id lowongan pekerjaan yang ingin dimodifikasi : ")

        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()

        c.execute("SELECT * FROM pekerjaan WHERE rowid=(?)", id_pekerjaan)
        conn.commit()

        get_data = c.fetchone()

        print("note : jika tidak ingin diubah maka tulis 'pass'")

        list_modify = list()

        list_modify.append(input("Nama pekerjaan : "))
        list_modify.append(input("Deskripsi pekerjaan : "))
        list_modify.append(input("Status pekerjaan : "))
        list_modify.append(input("Kategori pekerjaan : "))
        list_modify.append(input("Nilai Lulus : "))

        for j in range(0, 5):

            pertanyaan = input('Pertanyaan ' + str(j + 1) + ' : ')
            if pertanyaan != "pass":
                list_modify.append(self.__check_priority_question(pertanyaan))
            else:
                list_modify.append(pertanyaan)

        for i in range(0, len(list_modify)):
            if list_modify[i] == "pass":
                list_modify[i] = get_data[i]

        c.execute(""" UPDATE pekerjaan SET nama_pekerjaan = ?, deskripsi_pekerjaan = ?, status_pekerjaan = ?,
                        kategori_pekerjaan = ?, nilai_lulus = ?, pertanyaan1 = ?,
                        pertanyaan2 = ?, pertanyaan3 = ?, pertanyaan4 = ?, pertanyaan5 = ?
                        WHERE rowid = ?
            """, (str(list_modify[0]), str(list_modify[1]), str(list_modify[2]), str(list_modify[3]),
                  str(list_modify[4]), str(list_modify[5]), str(list_modify[6]), str(list_modify[7]),
                  str(list_modify[8]), str(list_modify[9]), str(id_pekerjaan)))

        conn.commit()

        print("Sukses memodifikasi data")

        conn.close()

    @staticmethod
    def __delete_lowongan_pekerjaan():
        id_pekerjaan = input("Masukkan id lowongan pekerjaan yang ingin dihapus : ")

        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()

        c.execute("DELETE FROM pekerjaan WHERE rowid = ? ", id_pekerjaan)
        conn.commit()

        c.execute("DELETE FROM pelamar WHERE id_pekerjaan = ? ", id_pekerjaan)
        conn.commit()

        print("Berhasil dihapus")

        conn.close()

    def __list_pelamar_kerja(self):
        data = super(Admin, self).retrievedata("pelamar")
        for d in data:
            print(d)

    # test psikologi panel

    @staticmethod
    def __count_soal_psikologi():
        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()

        c.execute("SELECT rowid, * FROM test_psikologi")
        conn.commit()

        list_soal = c.fetchall()
        return len(list_soal)

    @staticmethod
    def __list_test_psikologi():
        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()

        c.execute("SELECT rowid, * FROM test_psikologi")
        conn.commit()

        list_soal = c.fetchall()

        for soal in list_soal:
            print(soal)

        conn.close()

    @staticmethod
    def __tambah_test_psikologi(jumlah_soal):

        if jumlah_soal < 5:

            n = int(input("Jumlah pertanyaan psikologi yang akan ditambahkan : "))

            if jumlah_soal + n <= 5:

                for i in range(0, n):
                    soal = input("Masukkan pertanyaan psikologi : ")
                    nilai_minimum_kelulusan = input("""Masukkan Nilai Minimum Kelulusan untuk pertanyaan "{}" : """.
                                                    format(soal))
                    nilai_maximum_kelulusan = input("""Masukkan Nilai Maximum Kelulusan untuk pertanyaan "{}" : """.
                                                    format(soal))
                    tuple_soal = [soal, nilai_minimum_kelulusan, nilai_maximum_kelulusan]
                    tuple_soal = tuple(tuple_soal)

                    conn = sqlite3.connect("jobs.db")
                    c = conn.cursor()

                    c.execute("INSERT INTO test_psikologi VALUES (?, ?, ?)", tuple_soal)
                    conn.commit()

                    conn.close()

                    print("Berhasil memasukkan data")
            else:
                print("Tidak bisa menambahkan {} pertanyaan karena melampaui limit jumlah pertanyaan".format(n))

        else:
            print("Anda sudah mengisi 5 Pertanyaan Test Psikologi")

    def __modify_test_psikologi(self):

        data = super(Admin, self).retrievedata("test_psikologi")

        id_soal = int(input("Masukkan ID soal psikologi yang ingin diedit : "))

        for d in data:
            if d[0] == id_soal:
                data = d

        print('Isi dengan "pass" jika tidak ingin mengubah data')
        soal_modify = input("Masukkan pertanyaan baru : ")

        if soal_modify == "pass":
            soal_modify = data[1]

        nilai_minimum_kelulusan_modify = input("""Masukkan Nilai Minimum Kelulusan untuk pertanyaan "{}" : """.
                                               format(soal_modify))

        if nilai_minimum_kelulusan_modify == "pass":
            nilai_minimum_kelulusan_modify = data[2]

        nilai_maximum_kelulusan_modify = input("""Masukkan Nilai Maximum Kelulusan untuk pertanyaan "{}" : """.
                                               format(soal_modify))

        if nilai_maximum_kelulusan_modify == "pass":
            nilai_maximum_kelulusan_modify = data[2]

        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()

        c.execute("UPDATE test_psikologi SET soal = ?, nilai_minimum_kelulusan = ?, nilai_maximum_kelulusan = ?"
                  "WHERE rowid = ?",
                  (soal_modify, nilai_minimum_kelulusan_modify, nilai_maximum_kelulusan_modify, id_soal))
        conn.commit()

        conn.close()

        print("Berhasil mengubah soal")

    @staticmethod
    def __hapus_test_psikologi():
        id_soal = input("Masukkan ID soal psikologi yang ingin dihapus : ")
        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()

        c.execute("DELETE FROM test_psikologi WHERE rowid = ? ", str(id_soal))
        conn.commit()

        print("Berhasil menghapus soal")

        conn.close()

    def __menu_psikologi(self):

        jumlah_soal = self.__count_soal_psikologi()

        if jumlah_soal != 5:
            print("Peringatan : Hanya ada {} dari 5 Pertanyaan Test Psikologi! "
                  "Harap tambahkan {} Pertanyaan !".format(jumlah_soal, 5-jumlah_soal))

        print("1. List Test Psikologi")
        print("2. Input Test Psikologi")
        print("3. Modifikasi Test Psikologi")
        print("4. Hapus Test Psikologi")

        pilihan_menu = input("Pilih menu : ")

        if pilihan_menu == "1":
            self.__list_test_psikologi()
        elif pilihan_menu == "2":
            self.__tambah_test_psikologi(jumlah_soal)
        elif pilihan_menu == "3":
            self.__modify_test_psikologi()
        elif pilihan_menu == "4":
            self.__hapus_test_psikologi()

    def __menu_lowongan(self):
        print("1. List Lowongan Pekerja")
        print("2. Input Lowongan Pekerja")
        print("3. Modifikasi Lowongan Pekerja")
        print("4. Hapus Lowongan Pekerja")
        print("5. Lihat Pelamar Kerja")

        pilihan_menu = input("Pilih menu : ")

        if pilihan_menu == "1":
            self.printlist()
        elif pilihan_menu == "2":
            self.__tambah_lowongan_pekerjaan()
        elif pilihan_menu == "3":
            self.printlist()
            self.__modify_lowongan_pekerjaan()
        elif pilihan_menu == "4":
            self.printlist()
            self.__delete_lowongan_pekerjaan()
        elif pilihan_menu == "5":
            self.__list_pelamar_kerja()

    def menu_utama(self):
        print("Selamat datang di menu Admin")

        i = 0
        while i == 0:

            print("1. Lowongan Kerja")
            print("2. Pertanyaan Test Psikologi")
            print("3. Keluar")

            pilihan_menu = input("Pilih menu : ")

            if pilihan_menu == "1":
                self.__menu_lowongan()  # lowongan pekerjaan
            elif pilihan_menu == "2":
                self.__menu_psikologi()  # test psikologi
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
        menu_pelamar = MenuPelamar()
        menu_pelamar.menu_utama()
        pelamar = Pelamar(menu_pelamar.get_all_soal())
        proses = Evaluate(pelamar.send_to_database())
        proses.analisa_kelulusan(proses.retrievedata())
        print("Sukses melamar, silahkan buka email anda untuk pemberitahuan selanjutnya")
    elif pil_menu == "2":

        admin = Admin()

        username = input("Username : ")
        password = input("Password : ")

        if username == "admin" and password == "admin":
            admin.menu_utama()
        else:
            print("Username / Passowrd anda salah")
            print("1. Daftar Kerja\t\t2.Admin\t\t3.Keluar Program")

    elif pil_menu == "3":
        print("Terima kasih sampai jumpa kembali")
    else:
        print("Pilihan anda salah silahkan ulangi lagi")

