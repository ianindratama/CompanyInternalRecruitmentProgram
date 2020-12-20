import sqlite3


class Utility:

    def printlist(self):
        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()

        c.execute("SELECT rowid, * FROM pekerjaan")
        conn.commit()

        data_lowongan = list(c.fetchall())

        print("No \t Nama Pekerjaan \t Deskripsi Pekerjaan \t Status Pekerjaan \t Kategori Pekerjaan", end="")

        conn.close()
        return data_lowongan


class Pelamar(Utility):

    def __init__(self):
        pass

    def printlist(self):

        data_lowongan = super().printlist()
        print()

        for lowongan in data_lowongan:
            for i in range(0, len(lowongan)):

                print("{} \t\t".format(i + 1), end="")

                if i < 5:
                    print(lowongan[i], "\t\t", end="")

            print()

    def menu_utama(self):
        print("Selamat datang Pelamar Kerja")
        # list_lowongan_pekerjaan_pelamar()
        # user_input = input("Input ID pekerjaan yang diinginkan : ")
        # input_lowongan_pekerjaan(user_input)


class Admin(Utility):

    def __init__(self):
        pass

    # lowongan kerja panel

    def printlist(self):

        data_lowongan = super().printlist()

        print(" \t Nilai Kelulusan Pertanyaan Kerja \t Pertanyaan 1 \t Pertanyaan 2 \t Pertanyaan 3", end="")
        print(" \t Pertanyaan 4 \t Pertanyaan 5")

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

        print("Berhasil dihapus")

        conn.close()

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

                    tuple_soal = [soal]
                    tuple_soal = tuple(tuple_soal)

                    conn = sqlite3.connect("jobs.db")
                    c = conn.cursor()

                    c.execute("INSERT INTO test_psikologi VALUES (?)", tuple_soal)
                    conn.commit()

                    conn.close()

                    print("Berhasil memasukkan data")
            else:
                print("Tidak bisa menambahkan {} pertanyaan karena melampaui limit jumlah pertanyaan".format(n))

        else:
            print("Anda sudah mengisi 5 Pertanyaan Test Psikologi")

    @staticmethod
    def __modify_test_psikologi():
        id_soal = input("Masukkan ID soal psikologi yang ingin diedit : ")
        soal_modify = input("Masukkan pertanyaan baru : ")

        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()

        c.execute("UPDATE test_psikologi SET soal = ? WHERE rowid = ?", (soal_modify, id_soal))
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
            print("still working")

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
        pelamar = Pelamar()
        pelamar.menu_utama()
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



