# GUI purpose
from tkinter import *
import tkinter.ttk as ttk
from PIL import ImageTk, Image

# utilities purpose
import sqlite3
import datetime
import time

# email purpose
import smtplib
# libraries for email texting
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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

    def printlist(self, frame):

        data_lowongan = self.retrievedata("pekerjaan")

        no = Label(frame, text="No", font=("Helvetica", 10))
        nama_pekerjaan = Label(frame, text="Nama Pekerjaan", font=("Helvetica", 10))
        deskripsi_pekerjaan = Label(frame, text="Deskripsi Pekerjaan",
                                    font=("Helvetica", 10))
        status_pekerjaan = Label(frame, text="Status Pekerjaan", font=("Helvetica", 10))

        no.grid(row=0, column=0, padx=(0, 20))
        nama_pekerjaan.grid(row=0, column=1, padx=(0, 20))
        deskripsi_pekerjaan.grid(row=0, column=2, padx=(0, 20))
        status_pekerjaan.grid(row=0, column=3, padx=(0, 20))

        return data_lowongan


class MenuPelamar(Utility):

    def __init__(self):
        self.__no_pekerjaan_pelamar = int()

    def printlist(self, frame):

        data_lowongan = super().printlist(frame)

        counter = 1
        for lowongan in data_lowongan:

            for i in range(0, len(lowongan)):
                if i < 4:
                    Label(window.menu_utama_pelamar_kerja_frame, text=lowongan[i]).grid(
                        row=counter, column=i, padx=(0, 20))

            counter += 1

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

    def __submit_pilihan_user(self, value):
        self.__no_pekerjaan_pelamar = int(value[0])

    def menu_utama(self, header_frame, frame, footer_frame):
        self.printlist(frame)
        label_menu_utama_pelamar_kerja = Label(frame, text="Pilih Pekerjaan yang diinginkan")
        label_menu_utama_pelamar_kerja.grid(row=50, column=0, columnspan=2, pady=(20, 30), padx=(0, 10))

        data = super().retrievedata("pekerjaan")
        data_option = list()
        for i in range(0, len(data)):
            data_option.append(str(i+1) + ".   " + data[i][1])

        pilihan_user = StringVar()
        pilihan_user.set(data_option[0])

        dropdown_data = OptionMenu(frame, pilihan_user, *data_option)
        dropdown_data.grid(row=50, column=2, pady=(20, 30), padx=(0, 10), sticky=EW)

        submit_pilihan_pelamar_btn = Button(frame, text="Submit",
                                            command=lambda: [self.__submit_pilihan_user(pilihan_user.get()),
                                                             window.remove_current_frame(header_frame),
                                                             window.remove_current_frame(frame),
                                                             window.remove_current_frame(footer_frame),
                                                             window.menu_isi_data_diri_pelamar_kerja(
                                                                 Pelamar(self.get_all_soal()))])
        submit_pilihan_pelamar_btn.grid(row=50, column=3, pady=(20, 30), ipadx=10, ipady=10)

    def get_all_soal(self):

        no_pekerjaan = self.__no_pekerjaan_pelamar-1

        return [self.__get_id_pekerjaan(no_pekerjaan), self.__get_nama_pekerjaan(no_pekerjaan),
                self.__get_soal_kerja(no_pekerjaan), self.__get_soal_psikologi()]


class Pelamar:

    def __init__(self, data):

        self.__data = data

        self.__id_pekerjaan = data[0]
        self.__status_kelulusan = "-"

        self.__nama_lengkap = ""
        self.__email = ""
        self.__no_hp = ""
        self.__jenis_kelamin = "(L : Laki - Laki | P : Perempuan)"
        self.__pendidikan_terakhir = ""
        self.__lama_pengalaman_kerja = "(dalam tahun ex : 5)"
        self.__tanggal_applied = datetime.datetime.now().strftime("%d/%m/%Y")

        self.__tuple_jawaban_kerja = list()
        for i in range(0, len(data[2])):
            self.__tuple_jawaban_kerja.append(IntVar())

        self.__tuple_jawaban_psikologi = list()
        for i in range(0, len(data[3])):
            self.__tuple_jawaban_psikologi.append(IntVar())

        self.__tuple_jawaban_gabungan = ""
        self.__tupleData_send_to_database = ""

    def isi_data_diri(self, frame):
        # data diri

        Label(frame, text="Isi Data Diri", font=("Helvetica", 10)).grid(row=0, column=0, pady=(0, 10), sticky=W)

        Label(frame, text="Nama Lengkap", font=("Helvetica", 10)).grid(row=1, column=0, sticky=W, pady=(0, 10))
        if self.__nama_lengkap == "":
            self.__nama_lengkap = Entry(frame, width=40)
        else:
            temp = self.__nama_lengkap.get()
            self.__nama_lengkap = Entry(frame, width=40)
            self.__nama_lengkap.insert(0, temp)
        self.__nama_lengkap.grid(row=1, column=1, columnspan=2, padx=(10, 0), pady=(0, 10))

        Label(frame, text="Email", font=("Helvetica", 10)).grid(row=2, column=0, sticky=W, pady=(0, 10))
        if self.__email == "":
            self.__email = Entry(frame, width=40)
        else:
            temp = self.__email.get()
            self.__email = Entry(frame, width=40)
            self.__email.insert(0, temp)
        self.__email.grid(row=2, column=1, columnspan=2, padx=(10, 0), pady=(0, 10))

        Label(frame, text="No HP", font=("Helvetica", 10)).grid(row=3, column=0, sticky=W, pady=(0, 10))
        if self.__no_hp == "":
            self.__no_hp = Entry(frame, width=40)
        else:
            temp = self.__no_hp.get()
            self.__no_hp = Entry(frame, width=40)
            self.__no_hp.insert(0, temp)
        self.__no_hp.grid(row=3, column=1, columnspan=2, padx=(10, 0), pady=(0, 10))

        Label(frame, text="Jenis Kelamin ", font=("Helvetica", 10)).grid(row=4, column=0, sticky=W, pady=(0, 10))
        if self.__jenis_kelamin == "(L : Laki - Laki | P : Perempuan)":
            self.__jenis_kelamin = Entry(frame, width=40)
            self.__jenis_kelamin.insert(0, "(L : Laki - Laki | P : Perempuan)")
            self.__jenis_kelamin.bind("<Button-1>", lambda event: window.clear_entry(self.__jenis_kelamin))
        else:
            temp = self.__jenis_kelamin.get()
            self.__jenis_kelamin = Entry(frame, width=40)
            self.__jenis_kelamin.insert(0, temp)
        self.__jenis_kelamin.grid(row=4, column=1, columnspan=2, padx=(10, 0), pady=(0, 10))

        Label(frame, text="Pendidikan terakhir", font=("Helvetica", 10)).grid(row=5, column=0, sticky=W, pady=(0, 10))
        if self.__pendidikan_terakhir == "":
            self.__pendidikan_terakhir = Entry(frame, width=40)
        else:
            temp = self.__pendidikan_terakhir.get()
            self.__pendidikan_terakhir = Entry(frame, width=40)
            self.__pendidikan_terakhir.insert(0, temp)
        self.__pendidikan_terakhir.grid(row=5, column=1, columnspan=2, padx=(10, 0), pady=(0, 10))

        Label(frame, text="Pengalaman Kerja di bidang " + self.__data[1],
              font=("Helvetica", 10)).grid(row=6, column=0, sticky=W, pady=(0, 10))
        if self.__lama_pengalaman_kerja == "(dalam tahun ex : 5)":
            self.__lama_pengalaman_kerja = Entry(frame, width=40)
            self.__lama_pengalaman_kerja.insert(0, "(dalam tahun ex : 5)")
            self.__lama_pengalaman_kerja.bind("<Button-1>",
                                              lambda event: window.clear_entry(self.__lama_pengalaman_kerja))
        else:
            temp = self.__lama_pengalaman_kerja.get()
            self.__lama_pengalaman_kerja = Entry(frame, width=40)
            self.__lama_pengalaman_kerja.insert(0, temp)
        self.__lama_pengalaman_kerja.grid(row=6, column=1, columnspan=2, padx=(10, 0), pady=(0, 10))

    def isi_data_pertanyaan(self, frame):
        radio_button_options = [
            ("5", 5),
            ("4", 4),
            ("3", 3),
            ("2", 2),
            ("1", 1)
        ]

        # soal pekerjaan

        Label(frame, text="Pertanyaan mengenai Lowongan Pekerjaan " + self.__data[1],
              font=("Helvetica", 10)).grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky=W)

        Label(frame, text="5 : Sangat Bisa | 4 : Cukup Bisa | 3 : Bisa | 2 : Kurang Bisa | 1 : Tidak Bisa",
              font=("Helvetica", 10)).grid(row=1, column=0, columnspan=3, pady=(0, 10), sticky=W)

        for i in range(0, len(self.__data[2])):
            Label(frame, text=self.__data[2][i], font=("Helvetica", 10)).grid(
                row=(2 + i), column=0, padx=(10, 10), pady=(0, 10), sticky=W)

            # radio button option frame for pertanyaan kerja
            options_frame_kerja = LabelFrame(frame, bd=0, highlightthickness=0)
            options_frame_kerja.grid(row=(2 + i), column=1, columnspan=2, sticky=W+E)

            for j in range(0, len(radio_button_options)):
                Radiobutton(options_frame_kerja, text=radio_button_options[j][0],
                            variable=self.__tuple_jawaban_kerja[i],
                            value=radio_button_options[j][1]).grid(
                    row=0, column=j, pady=(0, 10))

        # tes psikologi

        Label(frame).grid(row=30, column=0, columnspan=3, pady=(0, 10), sticky=W)
        Label(frame, text="Test Psikologi",
              font=("Helvetica", 10)).grid(row=31, column=0, columnspan=3, pady=(0, 10), sticky=W)
        Label(frame, text="5 : Sangat Setuju | 4 : Cukup Setuju | 3 : Setuju | 2 : Kurang Setuju | 1 : Tidak Setuju",
              font=("Helvetica", 10)).grid(row=32, column=0, columnspan=3, pady=(0, 10), sticky=W)

        for i in range(0, len(self.__data[3])):
            Label(frame, text=self.__data[3][i], font=("Helvetica", 10)).grid(
                row=(33 + i), column=0, padx=(10, 10), pady=(0, 10), sticky=W)

            # radio button option frame for pertanyaan kerja
            options_frame_psikologi = LabelFrame(frame, bd=0, highlightthickness=0)
            options_frame_psikologi.grid(row=(33 + i), column=1, columnspan=2, sticky=W+E)

            for j in range(0, len(radio_button_options)):
                Radiobutton(options_frame_psikologi, text=radio_button_options[j][0],
                            variable=self.__tuple_jawaban_psikologi[i],
                            value=radio_button_options[j][1]).grid(
                    row=0, column=j, pady=(0, 10))

    def get_data(self):
        # data diri
        self.__nama_lengkap = self.__nama_lengkap.get()
        self.__email = self.__email.get()
        self.__no_hp = self.__no_hp.get()
        self.__jenis_kelamin = self.__jenis_kelamin.get()
        self.__pendidikan_terakhir = self.__pendidikan_terakhir.get()
        self.__lama_pengalaman_kerja = self.__lama_pengalaman_kerja.get()

        # data jawaban pekerjaan
        for i in range(0, len(self.__data[2])):
            self.__tuple_jawaban_kerja[i] = self.__tuple_jawaban_kerja[i].get()

        # data jawaban psikologi
        for i in range(0, len(self.__data[3])):
            self.__tuple_jawaban_psikologi[i] = self.__tuple_jawaban_psikologi[i].get()

        self.__tuple_jawaban_kerja = tuple(self.__tuple_jawaban_kerja)
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

    @staticmethod
    def analisa_kelulusan(data):

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

    def send_ke_email_pelamar(self):
        data = self.retrievedata()

        # header : from, to, subject

        from_email = "ianindratama2@gmail.com"
        to_email = data[0][4]
        subject = "Pemberitahuan Hasil Lamaran Kerja di PT XYZ"

        msg = MIMEMultipart()
        # header
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        # body
        body = "<h1>Halo <b>" + str(data[0][3]) + "</b>,</h1>"

        if data[0][2] == "Tidak Lulus":
            body += "<br>Mohon maaf anda belum lolos tahap 1 lamaran kerja perusahan PT XYZ sebagai " + str(data[1][1])
        elif data[0][2] == "Lulus":
            body += "<br>Selamat anda lolos tahap 1 lamaran kerja perusahan PT XYZ sebagai " + str(data[1][1])

            # konversi dari tanggal di database ke string
            date_str = data[0][9]
            date_obj = datetime.datetime.strptime(date_str, "%d/%m/%Y")

            # pertemuan tahap ke dua akan dilangsungkan 3 hari setelah pelamar melakukan tahap satu
            date = date_obj.date()
            date += datetime.timedelta(days=3)

            # mengecek apakah hari nya itu sabtu atau minggu kalau iya pindahin ke minggu
            day = date.strftime("%A")

            if day == "Saturday":
                day = "Monday"
                date += datetime.timedelta(days=2)
            elif day == "Sunday":
                day = "Monday"
                date += datetime.timedelta(days=1)

            body += ".<br>Silahkan Datang ke kantor pada hari " + day + " jam 9 WIB pada tanggal " + str(date)

        body += ".<br><br>Dari HRD PT XYZ<br><b>Joko Syamsudin</b>"

        # explaining to NIME what is the type of the message (plain, html, xml, etc)
        msg.attach(MIMEText(body, 'html'))

        # send the message to pelamar email
        message = msg.as_string()

        server = smtplib.SMTP("smtp.gmail.com", 587)  # server host, port
        server.starttls()  # secure server
        server.login(from_email, "zhnuybzhqweipuaq")

        server.sendmail(from_email, to_email, message)

        server.quit()


class Admin(Utility):

    def __init__(self):
        pass

    # lowongan kerja panel

    def printlist(self, frame):

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


class Window:
    def __init__(self):
        self.root = Tk()
        self.root.rowconfigure(3, weight=1)
        self.program_geometry = "500x300+525+200"
        self.date_time_label = Label(self.root, text="", fg="Red", font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.root, text="Menu Sebelumnya", state=DISABLED)
        self.menu_utama_button = Button(self.root, text="Menu Utama", state=DISABLED)

        # image in program
        self.__program_logo_image = ImageTk.PhotoImage((Image.open("logo1.png")).resize((75, 75)))
        self.__harap_tunggu_image = ImageTk.PhotoImage((Image.open("harap_tunggu.png")).resize((150, 100)))
        self.__sukses_image = ImageTk.PhotoImage((Image.open("sukses.png")).resize((150, 100)))

        # frame menu utama
        self.menu_utama_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_utama_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_utama_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu pelamar kerja
        self.menu_utama_pelamar_kerja_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_utama_pelamar_kerja_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_utama_pelamar_kerja_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu isi data diri pelamar kerja
        self.menu_isi_data_diri_pelamar_kerja_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_isi_data_diri_pelamar_kerja_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_isi_data_diri_pelamar_kerja_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu isi pertanyaan pelamar kerja
        self.menu_isi_pertanyaan_pelamar_kerja_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_isi_pertanyaan_pelamar_kerja_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_isi_pertanyaan_pelamar_kerja_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu proses pelamar kerja
        self.menu_proses_pelamar_kerja_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_proses_pelamar_kerja_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_proses_pelamar_kerja_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu akhir pelamar kerja
        self.menu_akhir_pelamar_kerja_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_akhir_pelamar_kerja_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_akhir_pelamar_kerja_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu login admin
        self.menu_login_admin_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_login_admin_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_login_admin_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu utama admin
        self.menu_utama_admin_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_utama_admin_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_utama_admin_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)


        self.root.title("Program Seleksi Kerja PT XYZ")
        self.root.iconbitmap('icon.ico')

    @staticmethod
    def remove_current_frame(current_frame):
        current_frame.grid_remove()

    @staticmethod
    def clear_entry(entry):
        entry.delete(0, END)

    def header(self, frame):
        # program name label
        program_name_label = Label(frame, text="Program Seleksi Kerja\nPT XYZ", font=("Helvetica", 20))
        program_name_label.grid(row=0, rowspan=2, column=0, columnspan=2, padx=(20, 10))

        # program logo image
        program_logo_image_label = Label(frame, image=self.__program_logo_image)
        program_logo_image_label.grid(row=0, rowspan=2, column=2, pady=(10, 10), sticky=E)

    def footer(self, frame):
        # date time label
        now = datetime.datetime.now().strftime("%A, %d %B %Y %H:%M:%S")
        self.date_time_label.configure(text=now)
        self.date_time_label.grid(row=0, column=0, sticky=W, padx=(10, 10), pady=(0, 10))

        # menu sebelumnya
        self.menu_sebelumnya_button.grid(row=0, column=1, padx=(30, 30), pady=(0, 10))

        # menu utama
        self.menu_utama_button.grid(row=0, column=2, pady=(0, 10), sticky=E)

        frame.after(1000, lambda: self.footer(frame))

    def menu_utama(self):
        self.program_geometry = "500x300+525+200"
        self.root.geometry(self.program_geometry)

        self.menu_utama_header_frame.grid(row=0, rowspan=2, column=0, columnspan=2)
        self.menu_utama_frame.grid(row=2, column=0, columnspan=2)
        self.menu_utama_footer_frame.grid(row=3, column=0, columnspan=2)

        # header section
        self.header(self.menu_utama_header_frame)

        # container section
        btn_pelamar_kerja = Button(self.menu_utama_frame, text="Pelamar Kerja",
                                   command=lambda: [self.remove_current_frame(self.menu_utama_header_frame),
                                                    self.remove_current_frame(self.menu_utama_frame),
                                                    self.remove_current_frame(self.menu_utama_footer_frame),
                                                    self.menu_utama_pelamar_kerja()])

        btn_admin = Button(self.menu_utama_frame, text="Admin",
                           command=lambda: [self.remove_current_frame(self.menu_utama_header_frame),
                                            self.remove_current_frame(self.menu_utama_frame),
                                            self.remove_current_frame(self.menu_utama_footer_frame),
                                            self.menu_login_admin("true")])

        btn_pelamar_kerja.grid(row=2, column=0, padx=(15, 50), pady=(35, 50), ipadx=15, ipady=25)
        btn_admin.grid(row=2, column=1, pady=(35, 50), ipadx=30, ipady=25)

        # footer section
        self.date_time_label = Label(self.menu_utama_footer_frame, text="", fg="Red", font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_utama_footer_frame, text="Menu Sebelumnya", state=DISABLED)
        self.menu_utama_button = Button(self.menu_utama_footer_frame, text="Menu Utama", state=DISABLED)
        self.footer(self.menu_utama_footer_frame)

    def menu_utama_pelamar_kerja(self):
        self.program_geometry = "550x300+525+200"
        self.root.geometry(self.program_geometry)

        self.menu_utama_pelamar_kerja_header_frame.grid(row=0, rowspan=2, column=0, columnspan=3, sticky="WE",
                                                        padx=(25, 0))
        self.menu_utama_pelamar_kerja_frame.grid(row=2, column=0, columnspan=3, sticky="WE", padx=(25, 0))
        self.menu_utama_pelamar_kerja_footer_frame.grid(row=3, column=0, columnspan=3, sticky="WE", padx=(25, 0))

        # instantiate menu pelamar
        menu_pelamar = MenuPelamar()

        # header section
        self.header(self.menu_utama_pelamar_kerja_header_frame)

        # container section
        menu_pelamar.menu_utama(self.menu_utama_pelamar_kerja_header_frame, self.menu_utama_pelamar_kerja_frame,
                                self.menu_utama_pelamar_kerja_footer_frame)

        # footer section
        self.date_time_label = Label(self.menu_utama_pelamar_kerja_footer_frame, text="", fg="Red",
                                     font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_utama_pelamar_kerja_footer_frame, text="Menu Sebelumnya",
                                             state=ACTIVE,
                                             command=lambda: [
                                                 self.remove_current_frame(self.menu_utama_pelamar_kerja_header_frame),
                                                 self.remove_current_frame(self.menu_utama_pelamar_kerja_frame),
                                                 self.remove_current_frame(self.menu_utama_pelamar_kerja_footer_frame),
                                                 self.menu_utama()])
        self.menu_utama_button = Button(self.menu_utama_pelamar_kerja_footer_frame, text="Menu Utama", state=ACTIVE,
                                        command=lambda: [
                                            self.remove_current_frame(self.menu_utama_pelamar_kerja_header_frame),
                                            self.remove_current_frame(self.menu_utama_pelamar_kerja_frame),
                                            self.remove_current_frame(
                                                self.menu_utama_pelamar_kerja_footer_frame),
                                            self.menu_utama()])
        self.footer(self.menu_utama_pelamar_kerja_footer_frame)

    def menu_isi_data_diri_pelamar_kerja(self, pelamar):
        self.program_geometry = "550x450+525+150"
        self.root.geometry(self.program_geometry)

        self.menu_isi_data_diri_pelamar_kerja_header_frame.grid(row=0, rowspan=2, column=0, columnspan=3, sticky="WE",
                                                                padx=(25, 0))
        self.menu_isi_data_diri_pelamar_kerja_frame.grid(row=2, column=0, columnspan=3, sticky="WE", padx=(25, 0))
        self.menu_isi_data_diri_pelamar_kerja_footer_frame.grid(row=3, column=0, columnspan=3, sticky="WE",
                                                                padx=(25, 0))

        # header section
        self.header(self.menu_isi_data_diri_pelamar_kerja_header_frame)

        # container section
        pelamar.isi_data_diri(self.menu_isi_data_diri_pelamar_kerja_frame)

        submit_btn = Button(self.menu_isi_data_diri_pelamar_kerja_frame, text="Submit",
                            command=lambda: [
                                self.remove_current_frame(self.menu_isi_data_diri_pelamar_kerja_header_frame),
                                self.remove_current_frame(self.menu_isi_data_diri_pelamar_kerja_frame),
                                self.remove_current_frame(
                                    self.menu_isi_data_diri_pelamar_kerja_footer_frame),
                                self.menu_isi_pertanyaan_pelamar_kerja(pelamar)])
        submit_btn.grid(row=7, column=2, pady=(20, 40), ipadx=10, sticky=W + E)

        # footer section
        self.date_time_label = Label(self.menu_isi_data_diri_pelamar_kerja_footer_frame, text="", fg="Red",
                                     font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_isi_data_diri_pelamar_kerja_footer_frame, text="Menu Sebelumnya",
                                             state=ACTIVE,
                                             command=lambda: [
                                                 self.remove_current_frame(
                                                     self.menu_isi_data_diri_pelamar_kerja_header_frame),
                                                 self.remove_current_frame(self.menu_isi_data_diri_pelamar_kerja_frame),
                                                 self.remove_current_frame(
                                                     self.menu_isi_data_diri_pelamar_kerja_footer_frame),
                                                 self.menu_utama_pelamar_kerja()])
        self.menu_utama_button = Button(self.menu_isi_data_diri_pelamar_kerja_footer_frame, text="Menu Utama",
                                        state=ACTIVE,
                                        command=lambda: [
                                            self.remove_current_frame(
                                                self.menu_isi_data_diri_pelamar_kerja_header_frame),
                                            self.remove_current_frame(
                                                self.menu_isi_data_diri_pelamar_kerja_frame),
                                            self.remove_current_frame(
                                                self.menu_isi_data_diri_pelamar_kerja_footer_frame),
                                            self.menu_utama()])
        self.footer(self.menu_isi_data_diri_pelamar_kerja_footer_frame)

    def menu_isi_pertanyaan_pelamar_kerja(self, pelamar):
        self.program_geometry = "900x710+300+50"
        self.root.geometry(self.program_geometry)

        self.menu_isi_pertanyaan_pelamar_kerja_header_frame.grid(row=0, rowspan=2, column=0, columnspan=3, sticky="WE",
                                                                 padx=(25, 0))
        self.menu_isi_pertanyaan_pelamar_kerja_frame.grid(row=2, column=0, columnspan=3, sticky="WE", padx=(25, 0))
        self.menu_isi_pertanyaan_pelamar_kerja_footer_frame.grid(row=3, column=0, columnspan=3,
                                                                 sticky="WE", padx=(25, 0))

        # header section
        self.header(self.menu_isi_pertanyaan_pelamar_kerja_header_frame)

        # container section
        pelamar.isi_data_pertanyaan(self.menu_isi_pertanyaan_pelamar_kerja_frame)

        submit_btn = Button(self.menu_isi_pertanyaan_pelamar_kerja_frame, text="Submit", width=20,
                            command=lambda: [
                                self.remove_current_frame(self.menu_isi_pertanyaan_pelamar_kerja_header_frame),
                                self.remove_current_frame(self.menu_isi_pertanyaan_pelamar_kerja_frame),
                                self.remove_current_frame(
                                    self.menu_isi_pertanyaan_pelamar_kerja_footer_frame),
                                self.menu_proses_pelamar_kerja(pelamar)])
        submit_btn.grid(row=80, column=0, columnspan=3, pady=(20, 20), ipadx=10, sticky=E)

        # footer section
        self.date_time_label = Label(self.menu_isi_pertanyaan_pelamar_kerja_footer_frame, text="", fg="Red",
                                     font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_isi_pertanyaan_pelamar_kerja_footer_frame,
                                             text="Menu Sebelumnya", state=ACTIVE,
                                             command=lambda: [
                                                 self.remove_current_frame(
                                                     self.menu_isi_pertanyaan_pelamar_kerja_header_frame),
                                                 self.remove_current_frame(
                                                     self.menu_isi_pertanyaan_pelamar_kerja_frame),
                                                 self.remove_current_frame(
                                                     self.menu_isi_pertanyaan_pelamar_kerja_footer_frame),
                                                 self.menu_isi_data_diri_pelamar_kerja(pelamar)])
        self.menu_utama_button = Button(self.menu_isi_pertanyaan_pelamar_kerja_footer_frame, text="Menu Utama",
                                        state=ACTIVE,
                                        command=lambda: [
                                            self.remove_current_frame(
                                                self.menu_isi_pertanyaan_pelamar_kerja_header_frame),
                                            self.remove_current_frame(
                                                self.menu_isi_pertanyaan_pelamar_kerja_frame),
                                            self.remove_current_frame(
                                                self.menu_isi_pertanyaan_pelamar_kerja_footer_frame),
                                            self.menu_utama()])
        self.footer(self.menu_isi_pertanyaan_pelamar_kerja_footer_frame)

    def menu_proses_pelamar_kerja(self, pelamar):
        self.program_geometry = "600x350+550+200"
        self.root.geometry(self.program_geometry)

        self.menu_proses_pelamar_kerja_header_frame.grid(row=0, rowspan=2, column=0, columnspan=3, sticky="WE",
                                                         padx=(25, 0))
        self.menu_proses_pelamar_kerja_frame.grid(row=2, column=0, columnspan=3, sticky="WE", padx=(25, 0))
        self.menu_proses_pelamar_kerja_footer_frame.grid(row=3, column=0, columnspan=3, sticky="WE", padx=(25, 0))

        # header section
        self.header(self.menu_proses_pelamar_kerja_header_frame)

        # container section
        harap_tunggu_image = Label(self.menu_proses_pelamar_kerja_frame, image=self.__harap_tunggu_image)
        harap_tunggu_image.grid(row=0, rowspan=2, column=0, columnspan=3, pady=(10, 10))

        # label progressbar
        progress = ttk.Progressbar(self.menu_proses_pelamar_kerja_frame, orient=HORIZONTAL, length=300,
                                   mode='determinate')
        progress.grid(row=2, rowspan=2, column=0, columnspan=3, pady=(10, 10))

        # label peringatan
        Label(self.menu_proses_pelamar_kerja_frame,
              text="Harap tunggu, sedang memproses pelamaran anda, mohon jangan menutup program",
              font=("Helvetica", 10, "bold")).grid(row=4, column=0, columnspan=3, pady=(10, 10))

        # footer section
        self.date_time_label = Label(self.menu_proses_pelamar_kerja_footer_frame, text="", fg="Red",
                                     font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_proses_pelamar_kerja_footer_frame,
                                             text="Menu Sebelumnya", state=DISABLED)
        self.menu_utama_button = Button(self.menu_proses_pelamar_kerja_footer_frame, text="Menu Utama", state=DISABLED)
        self.footer(self.menu_proses_pelamar_kerja_footer_frame)

        # progressbar progress
        progress['value'] = 20
        pelamar.get_data()
        self.menu_proses_pelamar_kerja_frame.update()
        time.sleep(1)

        progress['value'] = 50
        proses = Evaluate(pelamar.send_to_database())
        self.menu_proses_pelamar_kerja_frame.update()
        time.sleep(1)

        progress['value'] = 100
        proses.analisa_kelulusan(proses.retrievedata())
        self.menu_proses_pelamar_kerja_frame.update()
        time.sleep(1)

        progress['value'] = 200
        proses.send_ke_email_pelamar()
        self.menu_proses_pelamar_kerja_frame.update()
        time.sleep(1)

        progress['value'] = 300
        self.remove_current_frame(self.menu_proses_pelamar_kerja_header_frame)
        self.remove_current_frame(self.menu_proses_pelamar_kerja_frame)
        self.remove_current_frame(self.menu_proses_pelamar_kerja_footer_frame)
        self.menu_akhir_pelamar_kerja()

    def menu_akhir_pelamar_kerja(self):
        self.program_geometry = "610x350+550+200"
        self.root.geometry(self.program_geometry)

        self.menu_akhir_pelamar_kerja_header_frame.grid(row=0, rowspan=2, column=0, columnspan=3, sticky="WE",
                                                        padx=(25, 0))
        self.menu_akhir_pelamar_kerja_frame.grid(row=2, column=0, columnspan=3, sticky="WE", padx=(25, 0))
        self.menu_akhir_pelamar_kerja_footer_frame.grid(row=3, column=0, columnspan=3, sticky="WE", padx=(25, 0))

        # header section
        self.header(self.menu_akhir_pelamar_kerja_header_frame)

        # container section
        sukses_image = Label(self.menu_akhir_pelamar_kerja_frame, image=self.__sukses_image)
        sukses_image.grid(row=0, rowspan=2, column=0, columnspan=3, pady=(10, 10))

        Label(self.menu_akhir_pelamar_kerja_frame,
              text="Sukses melamar pekerjaan, silahkan buka email anda untuk pemberitahuan selanjutnya",
              font=("Helvetica", 10, "bold")).grid(row=2, column=0, columnspan=3, pady=(10, 10))

        # footer section
        self.date_time_label = Label(self.menu_akhir_pelamar_kerja_footer_frame, text="", fg="Red",
                                     font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_akhir_pelamar_kerja_footer_frame,
                                             text="Menu Sebelumnya", state=DISABLED)
        self.menu_utama_button = Button(self.menu_akhir_pelamar_kerja_footer_frame, text="Menu Utama", state=ACTIVE,
                                        command=lambda: [
                                            self.remove_current_frame(self.menu_akhir_pelamar_kerja_header_frame),
                                            self.remove_current_frame(self.menu_akhir_pelamar_kerja_frame),
                                            self.remove_current_frame(self.menu_akhir_pelamar_kerja_footer_frame),
                                            self.menu_utama()
                                        ])
        self.footer(self.menu_akhir_pelamar_kerja_footer_frame)

    def admin_verification(self, header_frame, frame, footer_frame, username, password):
        username = username.get()
        password = password.get()

        if username == "admin" and password == "admin":
            self.remove_current_frame(header_frame)
            self.remove_current_frame(frame)
            self.remove_current_frame(footer_frame)
            self.menu_utama_admin()
        else:
            self.menu_login_admin("false")

    def menu_login_admin(self, check):
        self.program_geometry = "500x310+525+200"
        self.root.geometry(self.program_geometry)

        self.menu_login_admin_header_frame.grid(row=0, rowspan=2, column=0, columnspan=2)
        self.menu_login_admin_frame.grid(row=2, column=0, columnspan=2)
        self.menu_login_admin_footer_frame.grid(row=3, column=0, columnspan=2)

        # header section
        self.header(self.menu_login_admin_header_frame)

        # container section
        Label(self.menu_login_admin_frame, text="Username", font=("Helvetica", 10)).grid(row=0, column=0, columnspan=2,
                                                                                         padx=(0, 25),
                                                                                         pady=(15, 15))
        Label(self.menu_login_admin_frame, text="Password", font=("Helvetica", 10)).grid(row=1, column=0, columnspan=2,
                                                                                         padx=(0, 30),
                                                                                         pady=(0, 20))

        username_input = Entry(self.menu_login_admin_frame)
        username_input.grid(row=0, column=2, pady=(20, 20))

        password_input = Entry(self.menu_login_admin_frame)
        password_input.grid(row=1, column=2, pady=(0, 20))

        submit_btn = Button(self.menu_login_admin_frame, text="Submit", font=("Helvetica", 10),
                            command=lambda: self.admin_verification(self.menu_login_admin_header_frame,
                                                                    self.menu_login_admin_frame,
                                                                    self.menu_login_admin_footer_frame,
                                                                    username_input, password_input))
        submit_btn.grid(row=2, column=2, pady=(0, 10))

        label_check = Label(self.menu_login_admin_frame, text="Username atau Password anda salah, silahkan coba lagi",
                            font=("Helvetica", "10", "bold"), fg=self.menu_login_admin_frame.cget('bg'))
        label_check.grid(row=3, column=0, columnspan=3, pady=(0, 10))

        if check != "true":
            label_check.configure(fg="red")

        # footer section
        self.date_time_label = Label(self.menu_login_admin_footer_frame, text="", fg="Red",
                                     font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_login_admin_footer_frame, text="Menu Sebelumnya",
                                             command=lambda: [
                                                 self.remove_current_frame(self.menu_login_admin_header_frame),
                                                 self.remove_current_frame(self.menu_login_admin_frame),
                                                 self.remove_current_frame(self.menu_login_admin_footer_frame),
                                                 self.menu_utama()])
        self.menu_utama_button = Button(self.menu_login_admin_footer_frame, text="Menu Utama",
                                        command=lambda: [
                                            self.remove_current_frame(self.menu_login_admin_header_frame),
                                            self.remove_current_frame(self.menu_login_admin_frame),
                                            self.remove_current_frame(self.menu_login_admin_footer_frame),
                                            self.menu_utama()])
        self.footer(self.menu_login_admin_footer_frame)

    def menu_utama_admin(self):
        self.program_geometry = "500x310+525+200"
        self.root.geometry(self.program_geometry)

        self.menu_utama_admin_header_frame.grid(row=0, rowspan=2, column=0, columnspan=2)
        self.menu_utama_admin_frame.grid(row=2, column=0, columnspan=2)
        self.menu_utama_admin_footer_frame.grid(row=3, column=0, columnspan=2)

        # header section
        self.header(self.menu_utama_admin_header_frame)

        # container section
        btn_panel_kerja = Button(self.menu_utama_admin_frame, text="Panel Lowongan Kerja",
                                 command=lambda: [self.remove_current_frame(self.menu_utama_admin_header_frame),
                                                  self.remove_current_frame(self.menu_utama_admin_frame),
                                                  self.remove_current_frame(self.menu_utama_admin_footer_frame)])

        btn_panel_psikologi = Button(self.menu_utama_admin_frame, text="Panel Test Psikologi",
                                     command=lambda: [self.remove_current_frame(self.menu_utama_admin_header_frame),
                                                      self.remove_current_frame(self.menu_utama_admin_frame),
                                                      self.remove_current_frame(self.menu_utama_admin_footer_frame)])

        btn_panel_kerja.grid(row=2, column=0, padx=(15, 50), pady=(35, 50), ipadx=15, ipady=25)
        btn_panel_psikologi.grid(row=2, column=1, pady=(35, 50), ipadx=30, ipady=25)

        # footer section
        self.date_time_label = Label(self.menu_utama_admin_footer_frame, text="", fg="Red",
                                     font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_utama_admin_footer_frame, text="Menu Sebelumnya",
                                             state=DISABLED)
        self.menu_utama_button = Button(self.menu_utama_admin_footer_frame, text="Menu Utama",
                                        command=lambda: [
                                            self.remove_current_frame(self.menu_utama_admin_header_frame),
                                            self.remove_current_frame(self.menu_utama_admin_frame),
                                            self.remove_current_frame(self.menu_utama_admin_footer_frame),
                                            self.menu_utama()])
        self.footer(self.menu_utama_admin_footer_frame)

    def keep_program_alive(self):
        self.root.mainloop()


# menu utama


#     elif pil_menu == "2":
#
#         admin = Admin()
#
#         username = input("Username : ")
#         password = input("Password : ")
#
#         if username == "admin" and password == "admin":
#             admin.menu_utama()
#         else:
#             print("Username / Passowrd anda salah")
#             print("1. Daftar Kerja\t\t2.Admin\t\t3.Keluar Program")
#

# menu utama

window = Window()
window.menu_utama()
window.keep_program_alive()
