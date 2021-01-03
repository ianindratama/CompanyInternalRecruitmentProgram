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

    @staticmethod
    def retrievedataspecific(identity, id_pekerjaan):
        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()

        c.execute("SELECT rowid, * FROM " + identity + " WHERE rowid=(?)", (str(id_pekerjaan),))
        conn.commit()

        data = c.fetchone()
        data = list(data)

        conn.close()
        return data

    def printlist(self, frame):

        data_lowongan = self.retrievedata("pekerjaan")

        Label(frame, text="No", font=("Helvetica", 10)).grid(row=0, column=0, padx=(0, 20))
        Label(frame, text="Nama Pekerjaan", font=("Helvetica", 10)).grid(row=0, column=1, padx=(0, 20))
        Label(frame, text="Deskripsi Pekerjaan", font=("Helvetica", 10)).grid(row=0, column=2, padx=(0, 20))
        Label(frame, text="Status Pekerjaan", font=("Helvetica", 10)).grid(row=0, column=3, padx=(0, 20))

        return data_lowongan

    @staticmethod
    def count_soal_psikologi():
        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()

        c.execute("SELECT rowid, * FROM test_psikologi")
        conn.commit()

        list_soal = c.fetchall()

        conn.close()

        return len(list_soal)


class MenuPelamar(Utility):

    def __init__(self):
        self.__no_pekerjaan_pelamar = int()

    def printlist(self, frame):

        data_lowongan = super().printlist(frame)

        counter = 1
        for lowongan in data_lowongan:

            for i in range(0, len(lowongan)):

                if i == 0:
                    Label(frame, text=str(counter)).grid(row=counter, column=i, padx=(0, 20))

                if 0 < i < 4:
                    Label(frame, text=lowongan[i]).grid(row=counter, column=i, padx=(0, 20))

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

        temp = ""

        for v in value:
            if v != ".":
                temp += v
            else:
                break

        self.__no_pekerjaan_pelamar = int(temp)

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
                                                             window.destroy_current_frame(frame),
                                                             window.remove_current_frame(footer_frame),
                                                             window.menu_isi_data_diri_pelamar_kerja(
                                                                 Pelamar(self.get_all_soal()),
                                                                 LabelFrame(window.root, bd=0,
                                                                            highlightthickness=0))])
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
        self.__pendidikan_terakhir = "(ex : S1 Teknik Komputer)"
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
            temp = self.__nama_lengkap
            self.__nama_lengkap = Entry(frame, width=40)
            self.__nama_lengkap.insert(0, temp)
        self.__nama_lengkap.grid(row=1, column=1, columnspan=2, padx=(10, 0), pady=(0, 10))

        Label(frame, text="Email", font=("Helvetica", 10)).grid(row=2, column=0, sticky=W, pady=(0, 10))
        if self.__email == "":
            self.__email = Entry(frame, width=40)
        else:
            temp = self.__email
            self.__email = Entry(frame, width=40)
            self.__email.insert(0, temp)
        self.__email.grid(row=2, column=1, columnspan=2, padx=(10, 0), pady=(0, 10))

        Label(frame, text="No HP", font=("Helvetica", 10)).grid(row=3, column=0, sticky=W, pady=(0, 10))
        if self.__no_hp == "":
            self.__no_hp = Entry(frame, width=40)
        else:
            temp = self.__no_hp
            self.__no_hp = Entry(frame, width=40)
            self.__no_hp.insert(0, temp)
        self.__no_hp.grid(row=3, column=1, columnspan=2, padx=(10, 0), pady=(0, 10))

        Label(frame, text="Jenis Kelamin ", font=("Helvetica", 10)).grid(row=4, column=0, sticky=W, pady=(0, 10))
        if self.__jenis_kelamin == "(L : Laki - Laki | P : Perempuan)":
            self.__jenis_kelamin = Entry(frame, width=40)
            self.__jenis_kelamin.insert(0, "(L : Laki - Laki | P : Perempuan)")
            self.__jenis_kelamin.bind("<Button-1>",
                                      lambda event: window.clear_entry_jenis_kelamin_once(self.__jenis_kelamin))
        else:
            temp = self.__jenis_kelamin
            self.__jenis_kelamin = Entry(frame, width=40)
            self.__jenis_kelamin.insert(0, temp)
        self.__jenis_kelamin.grid(row=4, column=1, columnspan=2, padx=(10, 0), pady=(0, 10))

        Label(frame, text="Pendidikan terakhir", font=("Helvetica", 10)).grid(row=5, column=0, sticky=W, pady=(0, 10))
        if self.__pendidikan_terakhir == "(ex : S1 Teknik Komputer)":
            self.__pendidikan_terakhir = Entry(frame, width=40)
            self.__pendidikan_terakhir.insert(0, "(ex : S1 Teknik Komputer)")
            self.__pendidikan_terakhir.bind("<Button-1>", lambda event: window.clear_entry_pendidikan_terakhir_once(
                self.__pendidikan_terakhir))
        else:
            temp = self.__pendidikan_terakhir
            self.__pendidikan_terakhir = Entry(frame, width=40)
            self.__pendidikan_terakhir.insert(0, temp)
        self.__pendidikan_terakhir.grid(row=5, column=1, columnspan=2, padx=(10, 0), pady=(0, 10))

        Label(frame, text="Pengalaman Kerja di bidang " + self.__data[1],
              font=("Helvetica", 10)).grid(row=6, column=0, sticky=W, pady=(0, 10))
        if self.__lama_pengalaman_kerja == "(dalam tahun ex : 5)":
            self.__lama_pengalaman_kerja = Entry(frame, width=40)
            self.__lama_pengalaman_kerja.insert(0, "(dalam tahun ex : 5)")
            self.__lama_pengalaman_kerja.bind("<Button-1>",
                                              lambda event: window.clear_entry_pengalaman_kerja_once(
                                                  self.__lama_pengalaman_kerja))
        else:
            temp = self.__lama_pengalaman_kerja
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
            Label(frame, text=self.__data[2][i], anchor=W, font=("Helvetica", 10)).grid(
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

    def get_data_diri(self):
        # data diri
        self.__nama_lengkap = self.__nama_lengkap.get()
        self.__email = self.__email.get()
        self.__no_hp = self.__no_hp.get()
        self.__jenis_kelamin = self.__jenis_kelamin.get()
        self.__pendidikan_terakhir = self.__pendidikan_terakhir.get()
        self.__lama_pengalaman_kerja = self.__lama_pengalaman_kerja.get()

    def get_data(self):

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
            c.execute("UPDATE pelamar SET status_kelulusan = ? WHERE rowid = ?", ("Lulus", data[0][0],))

            conn.commit()
        else:
            c.execute("UPDATE pelamar SET status_kelulusan = ? WHERE rowid = ?", ("Tidak Lulus", data[0][0],))
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

        # atribute lowongan kerja
        self.__nama_pekerjaan = ""
        self.__deskripsi_pekerjaan = ""
        self.__status_pekerjaan = "Tetap / Intern"
        self.__kategori_pekerjaan = "1 : IT   2 : Bisnis   3 : ETC"
        self.__nilai_lulus = ""
        self.__pertanyaan_kerja_1 = ""
        self.__pertanyaan_kerja_2 = ""
        self.__pertanyaan_kerja_3 = ""
        self.__pertanyaan_kerja_4 = ""
        self.__pertanyaan_kerja_5 = ""
        self.__prioritas_pertanyaan_kerja_1 = IntVar()
        self.__prioritas_pertanyaan_kerja_2 = IntVar()
        self.__prioritas_pertanyaan_kerja_3 = IntVar()
        self.__prioritas_pertanyaan_kerja_4 = IntVar()
        self.__prioritas_pertanyaan_kerja_5 = IntVar()

        # atribute no pekerjaan yang di input user untuk modify atau delete
        self.__no_pekerjaan_input_from_user = int()
        self.__id_pekerjaan_input_from_user = int()

        # atribute psikologi
        self.__soal_psikologi = ""
        self.__nilai_minimum_psikologi = ""
        self.__nilai_maximum_psikologi = ""

        # atribute no soal psikologi yang di input user untuk modify atau delete
        self.__no_psikologi_input_from_user = int()
        self.__id_psikologi_input_from_user = int()

    # lowongan kerja panel

    def printlist(self, frame):

        data_lowongan = super().printlist(frame)

        Label(frame, text="Kategori Pekerjaan", font=("Helvetica", 10)).grid(row=0, column=4, padx=(0, 20))
        Label(frame, text="Nilai Kelulusan", font=("Helvetica", 10)).grid(row=0, column=5, padx=(0, 20))

        counter = 1
        for lowongan in data_lowongan:
            for i in range(0, len(lowongan)):

                if i == 0:
                    Label(frame, text=str(counter)).grid(row=counter, column=i, padx=(0, 20))

                if 0 < i < 6:
                    Label(frame, text=lowongan[i]).grid(row=counter, column=i, padx=(0, 20))

            counter += 1

    def printlist_pelamar(self, frame):
        data_pelamar = super(Admin, self).retrievedata("pelamar")

        modified_data_pelamar = list()

        for i in range(0, len(data_pelamar)):
            data = list()
            data.append(data_pelamar[i][3])
            data.append(data_pelamar[i][4])
            # cari nama pekerjaan berdasarkan id pekerjaan
            data.append(super(Admin, self).retrievedataspecific("pekerjaan", data_pelamar[i][1])[1])
            data.append(data_pelamar[i][2])
            data.append(data_pelamar[i][9])
            modified_data_pelamar.append(data)

        Label(frame, text="No", font=("Helvetica", 10)).grid(row=0, column=0, padx=(0, 20))
        Label(frame, text="Nama", font=("Helvetica", 10)).grid(row=0, column=1, padx=(0, 20))
        Label(frame, text="Email", font=("Helvetica", 10)).grid(row=0, column=2, padx=(0, 20))
        Label(frame, text="Nama Pekerjaan", font=("Helvetica", 10)).grid(row=0, column=3, padx=(0, 20))
        Label(frame, text="Status Kelulusan", font=("Helvetica", 10)).grid(row=0, column=4, padx=(0, 20))
        Label(frame, text="Tanggal Applied", font=("Helvetica", 10)).grid(row=0, column=5, padx=(0, 20))

        counter = 1
        for pelamar in modified_data_pelamar:
            Label(frame, text=str(counter)).grid(row=counter, column=0, padx=(0, 20))
            for i in range(0, len(pelamar)):
                Label(frame, text=pelamar[i]).grid(row=counter, column=i+1, padx=(0, 20))
            counter += 1

    def printlist_psikologi(self, frame):
        data_psikologi = super(Admin, self).retrievedata("test_psikologi")

        Label(frame, text="No", font=("Helvetica", 10)).grid(row=0, column=0, padx=(0, 20))
        Label(frame, text="Soal", font=("Helvetica", 10)).grid(row=0, column=1, padx=(0, 20))
        Label(frame, text="Nilai Minimum Kelulusan", font=("Helvetica", 10)).grid(row=0, column=2, padx=(0, 20))
        Label(frame, text="Nilai Maximum Kelulusan", font=("Helvetica", 10)).grid(row=0, column=3, padx=(0, 20))

        counter = 1
        for data in data_psikologi:
            for i in range(0, len(data)):

                if i == 0:
                    Label(frame, text=str(counter)).grid(row=counter, column=i, padx=(0, 20))

                if 0 < i:
                    if i == 1:
                        Label(frame, text=data[i]).grid(row=counter, column=i, padx=(0, 20), sticky=W)
                    else:
                        Label(frame, text=data[i]).grid(row=counter, column=i, padx=(0, 20))

            counter += 1

    @staticmethod
    def __check_priority_question(pertanyaan, check):

        if check == 1:
            pertanyaan = "P" + pertanyaan

        return pertanyaan

    def tambah_lowongan_pekerjaan(self, frame_header, frame, frame_footer):

        Label(frame, text="Isi Data Lowongan Pekerjaan").grid(row=0, column=0, columnspan=2, sticky=W, padx=(20, 0),
                                                              pady=(0, 10))

        Label(frame, text="Nama Pekerjaan").grid(row=1, column=0, sticky=W, padx=(20, 10), pady=(0, 10))
        self.__nama_pekerjaan = Entry(frame, width=40)
        self.__nama_pekerjaan.grid(row=1, column=1, columnspan=2, sticky=W + E, padx=(0, 10), pady=(0, 10))

        Label(frame, text="Deskripsi Pekerjaan").grid(row=2, column=0, sticky=W, padx=(20, 10), pady=(0, 10))
        self.__deskripsi_pekerjaan = Entry(frame, width=40)
        self.__deskripsi_pekerjaan.grid(row=2, column=1, columnspan=2, sticky=W + E, padx=(0, 10), pady=(0, 10))

        Label(frame, text="Status Pekerjaan").grid(row=3, column=0, sticky=W, padx=(20, 10), pady=(0, 10))
        self.__status_pekerjaan = Entry(frame, width=40)
        self.__status_pekerjaan.insert(0, "Tetap / Intern")
        self.__status_pekerjaan.bind("<Button-1>",
                                     lambda event: window.clear_entry_status_once(self.__status_pekerjaan))
        self.__status_pekerjaan.grid(row=3, column=1, columnspan=2, sticky=W + E, padx=(0, 10), pady=(0, 10))

        Label(frame, text="Kategori Pekerjaan").grid(row=4, column=0, sticky=W, padx=(20, 10), pady=(0, 10))
        self.__kategori_pekerjaan = Entry(frame, width=40)
        self.__kategori_pekerjaan.insert(0, "1 : IT   2 : Bisnis   3 : ETC")
        self.__kategori_pekerjaan.bind("<Button-1>",
                                       lambda event: window.clear_entry_kategori_once(self.__kategori_pekerjaan))
        self.__kategori_pekerjaan.grid(row=4, column=1, columnspan=2, sticky=W + E, padx=(0, 10), pady=(0, 10))

        Label(frame, text="Nilai Lulus Pekerjaan").grid(row=5, column=0, sticky=W, padx=(20, 10), pady=(0, 20))
        self.__nilai_lulus = Entry(frame, width=40)
        self.__nilai_lulus.grid(row=5, column=1, columnspan=2, sticky=W + E, padx=(0, 10), pady=(0, 20))

        Label(frame, text="Pertanyaan mengenai Pekerjaan").grid(row=6, column=0, columnspan=2, sticky=W, padx=(20, 0))
        Label(frame, text="Klik tombol prioritas jika pertanyaan tersebut merupakan pertanyaan prioritas").grid(
            row=7, column=0, columnspan=4, sticky=W, padx=(20, 0), pady=(0, 10))

        Label(frame, text="Pertanyaan 1").grid(row=8, column=0, sticky=W, pady=(0, 10), padx=(20, 10))
        self.__pertanyaan_kerja_1 = Entry(frame, width=40)
        self.__pertanyaan_kerja_1.grid(row=8, column=1, columnspan=2, sticky=W + E, pady=(0, 10))
        Checkbutton(frame, text="Prioritas", variable=self.__prioritas_pertanyaan_kerja_1).grid(row=8, column=3,
                                                                                                padx=(20, 0),
                                                                                                pady=(0, 10))

        Label(frame, text="Pertanyaan 2").grid(row=9, column=0, sticky=W, pady=(0, 10), padx=(20, 10))
        self.__pertanyaan_kerja_2 = Entry(frame, width=40)
        self.__pertanyaan_kerja_2.grid(row=9, column=1, columnspan=2, sticky=W + E, pady=(0, 10))
        Checkbutton(frame, text="Prioritas", variable=self.__prioritas_pertanyaan_kerja_2).grid(row=9, column=3,
                                                                                                padx=(20, 0),
                                                                                                pady=(0, 10))

        Label(frame, text="Pertanyaan 3").grid(row=10, column=0, sticky=W, pady=(0, 10), padx=(20, 10))
        self.__pertanyaan_kerja_3 = Entry(frame, width=40)
        self.__pertanyaan_kerja_3.grid(row=10, column=1, columnspan=2, sticky=W + E, pady=(0, 10))
        Checkbutton(frame, text="Prioritas", variable=self.__prioritas_pertanyaan_kerja_3).grid(row=10, column=3,
                                                                                                padx=(20, 0),
                                                                                                pady=(0, 10))

        Label(frame, text="Pertanyaan 4").grid(row=11, column=0, sticky=W, pady=(0, 10), padx=(20, 10))
        self.__pertanyaan_kerja_4 = Entry(frame, width=40)
        self.__pertanyaan_kerja_4.grid(row=11, column=1, columnspan=2, sticky=W + E, pady=(0, 10))
        Checkbutton(frame, text="Prioritas", variable=self.__prioritas_pertanyaan_kerja_4).grid(row=11, column=3,
                                                                                                padx=(20, 0),
                                                                                                pady=(0, 10))

        Label(frame, text="Pertanyaan 5").grid(row=12, column=0, sticky=W, pady=(0, 10), padx=(20, 10))
        self.__pertanyaan_kerja_5 = Entry(frame, width=40)
        self.__pertanyaan_kerja_5.grid(row=12, column=1, columnspan=2, sticky=W + E, pady=(0, 10))
        Checkbutton(frame, text="Prioritas", variable=self.__prioritas_pertanyaan_kerja_5).grid(row=12, column=3,
                                                                                                padx=(20, 0),
                                                                                                pady=(0, 10))

        submit_btn = Button(frame, text="Submit",
                            command=lambda: self.__proses_tambah_lowogan_pekerjaan(frame_header, frame, frame_footer))
        submit_btn.grid(row=13, column=1, columnspan=2, pady=20, sticky=W + E)

    def __proses_tambah_lowogan_pekerjaan(self, frame_header, frame, frame_footer):
        list_data = list()
        list_data.append(self.__nama_pekerjaan.get())
        list_data.append(self.__deskripsi_pekerjaan.get())
        list_data.append(self.__status_pekerjaan.get())
        list_data.append(self.__kategori_pekerjaan.get())
        list_data.append(self.__nilai_lulus.get())
        list_data.append(
            self.__check_priority_question(self.__pertanyaan_kerja_1.get(), self.__prioritas_pertanyaan_kerja_1.get()))
        list_data.append(
            self.__check_priority_question(self.__pertanyaan_kerja_2.get(), self.__prioritas_pertanyaan_kerja_2.get()))
        list_data.append(
            self.__check_priority_question(self.__pertanyaan_kerja_3.get(), self.__prioritas_pertanyaan_kerja_3.get()))
        list_data.append(
            self.__check_priority_question(self.__pertanyaan_kerja_4.get(), self.__prioritas_pertanyaan_kerja_4.get()))
        list_data.append(
            self.__check_priority_question(self.__pertanyaan_kerja_5.get(), self.__prioritas_pertanyaan_kerja_5.get()))

        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()

        c.execute("INSERT INTO pekerjaan VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", tuple(list_data))
        conn.commit()

        conn.close()

        # clear semua data attribute di object setelah input data lowongan kerja ke db berhasil
        self.__nama_pekerjaan = ""
        self.__deskripsi_pekerjaan = ""
        self.__status_pekerjaan = "Tetap / Intern"
        self.__kategori_pekerjaan = "1 : IT   2 : Bisnis   3 : ETC"
        self.__nilai_lulus = ""
        self.__pertanyaan_kerja_1 = ""
        self.__pertanyaan_kerja_2 = ""
        self.__pertanyaan_kerja_3 = ""
        self.__pertanyaan_kerja_4 = ""
        self.__pertanyaan_kerja_5 = ""
        self.__prioritas_pertanyaan_kerja_1 = IntVar()
        self.__prioritas_pertanyaan_kerja_2 = IntVar()
        self.__prioritas_pertanyaan_kerja_3 = IntVar()
        self.__prioritas_pertanyaan_kerja_4 = IntVar()
        self.__prioritas_pertanyaan_kerja_5 = IntVar()

        window.remove_current_frame(frame_header)
        window.remove_current_frame(frame)
        window.remove_current_frame(frame_footer)

        window.menu_input_akhir_kerja_admin()

    def __submit_pekerjaan_pilihan_user(self, value):

        temp = ""

        for v in value:
            if v != ".":
                temp += v
            else:
                break

        self.__no_pekerjaan_input_from_user = int(temp)

    def menu_modify_lowongan_pekerjaan(self, frame_header, frame, frame_footer):

        label_menu_modify_kerja_admin = Label(frame,
                                              text="Pilih Lowongan Kerja yang ingin di edit")
        label_menu_modify_kerja_admin.grid(row=50, column=0, columnspan=2, pady=(20, 30), padx=(0, 10))

        data = super().retrievedata("pekerjaan")
        data_option = list()
        for i in range(0, len(data)):
            data_option.append(str(i + 1) + ".   " + data[i][1])

        pilihan_user = StringVar()
        pilihan_user.set(data_option[0])

        dropdown_data = OptionMenu(frame, pilihan_user, *data_option)
        dropdown_data.grid(row=50, column=2, columnspan=2, pady=(20, 30), sticky=EW)

        submit_pilihan_btn = Button(frame, text="Submit",
                                    command=lambda: [
                                        self.__submit_pekerjaan_pilihan_user(pilihan_user.get()),
                                        self.__get_data_modify_lowongan_pekerjaan(),
                                        window.remove_current_frame(frame_header),
                                        window.destroy_current_frame(frame),
                                        window.remove_current_frame(frame_footer),
                                        window.menu_input_modify_kerja_admin()
                                    ])
        submit_pilihan_btn.grid(row=50, column=4, pady=(20, 30), ipadx=10, ipady=10)

    def __get_data_modify_lowongan_pekerjaan(self):

        data = super(Admin, self).retrievedata("pekerjaan")

        # get id pekerjaan
        self.__id_pekerjaan_input_from_user = data[(self.__no_pekerjaan_input_from_user-1)][0]

        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()

        c.execute("SELECT rowid, * FROM pekerjaan WHERE rowid=(?)", (str(self.__id_pekerjaan_input_from_user),))
        conn.commit()

        data = c.fetchone()

        conn.close()

        # retrieve data pekerjaan from db and save to atribute lowongan kerja
        self.__nama_pekerjaan = data[1]
        self.__deskripsi_pekerjaan = data[2]
        self.__status_pekerjaan = data[3]
        self.__kategori_pekerjaan = data[4]
        self.__nilai_lulus = data[5]

        if data[6][0] == "P":
            self.__pertanyaan_kerja_1 = data[6][1:]
            self.__prioritas_pertanyaan_kerja_1.set(1)
        else:
            self.__pertanyaan_kerja_1 = data[6]
            self.__prioritas_pertanyaan_kerja_1.set(0)

        if data[7][0] == "P":
            self.__pertanyaan_kerja_2 = data[7][1:]
            self.__prioritas_pertanyaan_kerja_2.set(1)
        else:
            self.__pertanyaan_kerja_2 = data[7]
            self.__prioritas_pertanyaan_kerja_2.set(0)

        if data[8][0] == "P":
            self.__pertanyaan_kerja_3 = data[8][1:]
            self.__prioritas_pertanyaan_kerja_3.set(1)
        else:
            self.__pertanyaan_kerja_3 = data[8]
            self.__prioritas_pertanyaan_kerja_3.set(0)

        if data[9][0] == "P":
            self.__pertanyaan_kerja_4 = data[9][1:]
            self.__prioritas_pertanyaan_kerja_4.set(1)
        else:
            self.__pertanyaan_kerja_4 = data[9]
            self.__prioritas_pertanyaan_kerja_4.set(0)

        if data[10][0] == "P":
            self.__pertanyaan_kerja_5 = data[10][1:]
            self.__prioritas_pertanyaan_kerja_5.set(1)
        else:
            self.__pertanyaan_kerja_5 = data[10]
            self.__prioritas_pertanyaan_kerja_5.set(0)

    def input_modify_lowongan_pekerjaan(self, frame_header, frame, frame_footer):

        Label(frame, text="Modifikasi Data Lowongan Pekerjaan").grid(row=0, column=0, columnspan=2, sticky=W,
                                                                     padx=(20, 0), pady=(0, 10))

        Label(frame, text="Nama Pekerjaan").grid(row=1, column=0, sticky=W, padx=(20, 10), pady=(0, 10))
        temp_nama_pekerjaan = self.__nama_pekerjaan
        self.__nama_pekerjaan = Entry(frame, width=40)
        self.__nama_pekerjaan.insert(0, temp_nama_pekerjaan)
        self.__nama_pekerjaan.grid(row=1, column=1, columnspan=2, sticky=W + E, padx=(0, 10), pady=(0, 10))

        Label(frame, text="Deskripsi Pekerjaan").grid(row=2, column=0, sticky=W, padx=(20, 10), pady=(0, 10))
        temp_deskripsi_pekerjaan = self.__deskripsi_pekerjaan
        self.__deskripsi_pekerjaan = Entry(frame, width=40)
        self.__deskripsi_pekerjaan.insert(0, temp_deskripsi_pekerjaan)
        self.__deskripsi_pekerjaan.grid(row=2, column=1, columnspan=2, sticky=W + E, padx=(0, 10), pady=(0, 10))

        Label(frame, text="Status Pekerjaan").grid(row=3, column=0, sticky=W, padx=(20, 10), pady=(0, 10))
        temp_status_pekerjaan = self.__status_pekerjaan
        self.__status_pekerjaan = Entry(frame, width=40)
        self.__status_pekerjaan.insert(0, temp_status_pekerjaan)
        self.__status_pekerjaan.grid(row=3, column=1, columnspan=2, sticky=W + E, padx=(0, 10), pady=(0, 10))

        Label(frame, text="Kategori Pekerjaan").grid(row=4, column=0, sticky=W, padx=(20, 10), pady=(0, 10))
        temp_kategori_pekerjaan = self.__kategori_pekerjaan
        self.__kategori_pekerjaan = Entry(frame, width=40)
        self.__kategori_pekerjaan.insert(0, temp_kategori_pekerjaan)
        self.__kategori_pekerjaan.grid(row=4, column=1, columnspan=2, sticky=W + E, padx=(0, 10), pady=(0, 10))

        Label(frame, text="Nilai Lulus Pekerjaan").grid(row=5, column=0, sticky=W, padx=(20, 10), pady=(0, 20))
        temp_nilai_lulus_pekerjaan = self.__nilai_lulus
        self.__nilai_lulus = Entry(frame, width=40)
        self.__nilai_lulus.insert(0, temp_nilai_lulus_pekerjaan)
        self.__nilai_lulus.grid(row=5, column=1, columnspan=2, sticky=W + E, padx=(0, 10), pady=(0, 20))

        Label(frame, text="Pertanyaan mengenai Pekerjaan").grid(row=6, column=0, columnspan=2, sticky=W, padx=(20, 0))
        Label(frame, text="Klik tombol prioritas jika pertanyaan tersebut merupakan pertanyaan prioritas").grid(
            row=7, column=0, columnspan=4, sticky=W, padx=(20, 0), pady=(0, 10))

        Label(frame, text="Pertanyaan 1").grid(row=8, column=0, sticky=W, pady=(0, 10), padx=(20, 10))
        temp_pertanyaan_kerja_1 = self.__pertanyaan_kerja_1
        self.__pertanyaan_kerja_1 = Entry(frame, width=40)
        self.__pertanyaan_kerja_1.insert(0, temp_pertanyaan_kerja_1)
        self.__pertanyaan_kerja_1.grid(row=8, column=1, columnspan=2, sticky=W + E, pady=(0, 10))
        Checkbutton(frame, text="Prioritas", variable=self.__prioritas_pertanyaan_kerja_1).grid(row=8, column=3,
                                                                                                padx=(20, 0),
                                                                                                pady=(0, 10))

        Label(frame, text="Pertanyaan 2").grid(row=9, column=0, sticky=W, pady=(0, 10), padx=(20, 10))
        temp_pertanyaan_kerja_2 = self.__pertanyaan_kerja_2
        self.__pertanyaan_kerja_2 = Entry(frame, width=40)
        self.__pertanyaan_kerja_2.insert(0, temp_pertanyaan_kerja_2)
        self.__pertanyaan_kerja_2.grid(row=9, column=1, columnspan=2, sticky=W + E, pady=(0, 10))
        Checkbutton(frame, text="Prioritas", variable=self.__prioritas_pertanyaan_kerja_2).grid(row=9, column=3,
                                                                                                padx=(20, 0),
                                                                                                pady=(0, 10))

        Label(frame, text="Pertanyaan 3").grid(row=10, column=0, sticky=W, pady=(0, 10), padx=(20, 10))
        temp_pertanyaan_kerja_3 = self.__pertanyaan_kerja_3
        self.__pertanyaan_kerja_3 = Entry(frame, width=40)
        self.__pertanyaan_kerja_3.insert(0, temp_pertanyaan_kerja_3)
        self.__pertanyaan_kerja_3.grid(row=10, column=1, columnspan=2, sticky=W + E, pady=(0, 10))
        Checkbutton(frame, text="Prioritas", variable=self.__prioritas_pertanyaan_kerja_3).grid(row=10, column=3,
                                                                                                padx=(20, 0),
                                                                                                pady=(0, 10))

        Label(frame, text="Pertanyaan 4").grid(row=11, column=0, sticky=W, pady=(0, 10), padx=(20, 10))
        temp_pertanyaan_kerja_4 = self.__pertanyaan_kerja_4
        self.__pertanyaan_kerja_4 = Entry(frame, width=40)
        self.__pertanyaan_kerja_4.insert(0, temp_pertanyaan_kerja_4)
        self.__pertanyaan_kerja_4.grid(row=11, column=1, columnspan=2, sticky=W + E, pady=(0, 10))
        Checkbutton(frame, text="Prioritas", variable=self.__prioritas_pertanyaan_kerja_4).grid(row=11, column=3,
                                                                                                padx=(20, 0),
                                                                                                pady=(0, 10))

        Label(frame, text="Pertanyaan 5").grid(row=12, column=0, sticky=W, pady=(0, 10), padx=(20, 10))
        temp_pertanyaan_kerja_5 = self.__pertanyaan_kerja_5
        self.__pertanyaan_kerja_5 = Entry(frame, width=40)
        self.__pertanyaan_kerja_5.insert(0, temp_pertanyaan_kerja_5)
        self.__pertanyaan_kerja_5.grid(row=12, column=1, columnspan=2, sticky=W + E, pady=(0, 10))
        Checkbutton(frame, text="Prioritas", variable=self.__prioritas_pertanyaan_kerja_5).grid(row=12, column=3,
                                                                                                padx=(20, 0),
                                                                                                pady=(0, 10))

        submit_btn = Button(frame, text="Submit",
                            command=lambda: self.__proses_modify_lowogan_pekerjaan(frame_header, frame, frame_footer))
        submit_btn.grid(row=13, column=1, columnspan=2, pady=20, sticky=W + E)

    def __proses_modify_lowogan_pekerjaan(self, frame_header, frame, frame_footer):

        list_modify = list()
        list_modify.append(self.__nama_pekerjaan.get())
        list_modify.append(self.__deskripsi_pekerjaan.get())
        list_modify.append(self.__status_pekerjaan.get())
        list_modify.append(self.__kategori_pekerjaan.get())
        list_modify.append(self.__nilai_lulus.get())
        list_modify.append(
            self.__check_priority_question(self.__pertanyaan_kerja_1.get(), self.__prioritas_pertanyaan_kerja_1.get()))
        list_modify.append(
            self.__check_priority_question(self.__pertanyaan_kerja_2.get(), self.__prioritas_pertanyaan_kerja_2.get()))
        list_modify.append(
            self.__check_priority_question(self.__pertanyaan_kerja_3.get(), self.__prioritas_pertanyaan_kerja_3.get()))
        list_modify.append(
            self.__check_priority_question(self.__pertanyaan_kerja_4.get(), self.__prioritas_pertanyaan_kerja_4.get()))
        list_modify.append(
            self.__check_priority_question(self.__pertanyaan_kerja_5.get(), self.__prioritas_pertanyaan_kerja_5.get()))

        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()

        c.execute(""" UPDATE pekerjaan SET nama_pekerjaan = ?, deskripsi_pekerjaan = ?, status_pekerjaan = ?,
                                kategori_pekerjaan = ?, nilai_lulus = ?, pertanyaan1 = ?,
                                pertanyaan2 = ?, pertanyaan3 = ?, pertanyaan4 = ?, pertanyaan5 = ?
                                WHERE rowid = ?
                    """, (str(list_modify[0]), str(list_modify[1]), str(list_modify[2]), str(list_modify[3]),
                          str(list_modify[4]), str(list_modify[5]), str(list_modify[6]), str(list_modify[7]),
                          str(list_modify[8]), str(list_modify[9]), str(self.__id_pekerjaan_input_from_user)))

        conn.commit()

        conn.close()

        # clear semua data attribute di object setelah input data lowongan kerja ke db berhasil
        self.__nama_pekerjaan = ""
        self.__deskripsi_pekerjaan = ""
        self.__status_pekerjaan = "Tetap / Intern"
        self.__kategori_pekerjaan = "1 : IT   2 : Bisnis   3 : ETC"
        self.__nilai_lulus = ""
        self.__pertanyaan_kerja_1 = ""
        self.__pertanyaan_kerja_2 = ""
        self.__pertanyaan_kerja_3 = ""
        self.__pertanyaan_kerja_4 = ""
        self.__pertanyaan_kerja_5 = ""
        self.__prioritas_pertanyaan_kerja_1 = IntVar()
        self.__prioritas_pertanyaan_kerja_2 = IntVar()
        self.__prioritas_pertanyaan_kerja_3 = IntVar()
        self.__prioritas_pertanyaan_kerja_4 = IntVar()
        self.__prioritas_pertanyaan_kerja_5 = IntVar()
        self.__no_pekerjaan_input_from_user = int()
        self.__id_pekerjaan_input_from_user = int()

        window.remove_current_frame(frame_header)
        window.remove_current_frame(frame)
        window.remove_current_frame(frame_footer)

        window.menu_input_modify_akhir_kerja_admin()

    def menu_delete_lowongan_pekerjaan(self, frame_header, frame, frame_footer):

        label_menu_delete_kerja_admin = Label(frame,
                                              text="Pilih Lowongan Kerja yang ingin di hapus")
        label_menu_delete_kerja_admin.grid(row=50, column=0, columnspan=2, pady=(20, 30), padx=(0, 10))

        data = super().retrievedata("pekerjaan")
        data_option = list()
        for i in range(0, len(data)):
            data_option.append(str(i + 1) + ".   " + data[i][1])

        pilihan_user = StringVar()
        pilihan_user.set(data_option[0])

        dropdown_data = OptionMenu(frame, pilihan_user, *data_option)
        dropdown_data.grid(row=50, column=2, columnspan=2, pady=(20, 30), sticky=EW)

        submit_pilihan_btn = Button(frame, text="Submit",
                                    command=lambda: [
                                        self.__submit_pekerjaan_pilihan_user(pilihan_user.get()),
                                        self.__delete_lowongan_pekerjaan(),
                                        window.remove_current_frame(frame_header),
                                        window.destroy_current_frame(frame),
                                        window.remove_current_frame(frame_footer),
                                        window.menu_delete_akhir_kerja_admin()
                                    ])
        submit_pilihan_btn.grid(row=50, column=4, pady=(20, 30), ipadx=10, ipady=10)

    def __delete_lowongan_pekerjaan(self):

        data = super(Admin, self).retrievedata("pekerjaan")

        # get id pekerjaan
        self.__id_pekerjaan_input_from_user = data[(self.__no_pekerjaan_input_from_user - 1)][0]

        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()

        c.execute("DELETE FROM pekerjaan WHERE rowid = (?) ", (str(self.__id_pekerjaan_input_from_user),))
        conn.commit()

        c.execute("DELETE FROM pelamar WHERE id_pekerjaan = (?) ", (str(self.__id_pekerjaan_input_from_user),))
        conn.commit()

        conn.close()

        # clear attributes
        self.__no_pekerjaan_input_from_user = int()
        self.__id_pekerjaan_input_from_user = int()

    # test psikologi panel

    def tambah_test_psikologi(self, frame_header, frame, frame_footer, jumlah_soal):
        Label(frame, text="Isi Data Test Psikologi").grid(row=0, column=0, columnspan=2, sticky=W, padx=(20, 0),
                                                          pady=(0, 10))
        Label(frame, text="5 : Sangat Setuju | 4 : Cukup Setuju | 3 : Setuju"
                          " | 2 : Kurang Setuju | 1 : Tidak Setuju", fg="red").grid(row=1, column=0, columnspan=3,
                                                                                    sticky=W,
                                                                                    padx=(20, 0), pady=(0, 10))

        Label(frame, text="Soal Psikologi").grid(row=2, column=0, sticky=W, padx=(20, 10), pady=(0, 10))
        self.__soal_psikologi = Entry(frame, width=40)
        self.__soal_psikologi.grid(row=2, column=1, columnspan=2, sticky=W + E, padx=(0, 10), pady=(0, 10))

        Label(frame, text="Nilai Minimum Psikologi").grid(row=3, column=0, sticky=W, padx=(20, 10), pady=(0, 10))
        self.__nilai_minimum_psikologi = Entry(frame, width=40)
        self.__nilai_minimum_psikologi.grid(row=3, column=1, columnspan=2, sticky=W + E, padx=(0, 10), pady=(0, 10))

        Label(frame, text="Nilai Maximum Psikologi").grid(row=4, column=0, sticky=W, padx=(20, 10), pady=(0, 20))
        self.__nilai_maximum_psikologi = Entry(frame, width=40)
        self.__nilai_maximum_psikologi.grid(row=4, column=1, columnspan=2, sticky=W + E, padx=(0, 10), pady=(0, 20))

        submit_btn = Button(frame, text="Submit",
                            command=lambda: self.__proses_tambah_test_psikologi(frame_header, frame, frame_footer))

        if jumlah_soal == 5:
            Label(frame, text="""Tidak bisa menambahkan pertanyaan karena\ntelah mencapai limit jumlah pertanyaan""",
                  fg="red", anchor=W).grid(row=5, rowspan=2, column=0, columnspan=2, sticky=W, padx=(20, 10),
                                           pady=(5, 20))
            submit_btn['state'] = DISABLED

        submit_btn.grid(row=5, column=2, pady=(10, 20), sticky=W+E)

    def __proses_tambah_test_psikologi(self, frame_header, frame, frame_footer):
        list_data = list()
        list_data.append(self.__soal_psikologi.get())
        list_data.append(self.__nilai_minimum_psikologi.get())
        list_data.append(self.__nilai_maximum_psikologi.get())

        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()

        c.execute("INSERT INTO test_psikologi VALUES (?, ?, ?)", tuple(list_data))
        conn.commit()

        conn.close()

        # clear semua data attribute di object setelah input data test psikologi ke db berhasil
        self.__soal_psikologi = ""
        self.__nilai_minimum_psikologi = ""
        self.__nilai_maximum_psikologi = ""

        window.remove_current_frame(frame_header)
        window.destroy_current_frame(frame)
        window.remove_current_frame(frame_footer)

        window.menu_input_akhir_psikologi_admin()

    def menu_modify_test_psikologi(self, frame_header, frame, frame_footer):

        label_menu_modify_psikologi_admin = Label(frame,
                                                  text="Pilih Soal Psikologi yang ingin di edit")
        label_menu_modify_psikologi_admin.grid(row=50, column=0, pady=(20, 30), padx=(0, 10))

        data = super().retrievedata("test_psikologi")
        data_option = list()
        for i in range(0, len(data)):
            data_option.append(str(i + 1) + ".   " + data[i][1])

        pilihan_user = StringVar()
        pilihan_user.set(data_option[0])

        dropdown_data = OptionMenu(frame, pilihan_user, *data_option)
        dropdown_data.grid(row=50, column=1, columnspan=2, pady=(20, 30), sticky=EW)

        submit_pilihan_btn = Button(frame, text="Submit",
                                    command=lambda: [
                                        self.__submit_psikologi_pilihan_user(pilihan_user.get()),
                                        self.__get_data_modify_test_psikologi(),
                                        window.remove_current_frame(frame_header),
                                        window.destroy_current_frame(frame),
                                        window.remove_current_frame(frame_footer),
                                        window.menu_input_modify_psikologi_admin()
                                    ])
        submit_pilihan_btn.grid(row=50, column=3, pady=(20, 30), ipadx=10, ipady=10)

    def __submit_psikologi_pilihan_user(self, value):

        temp = ""

        for v in value:
            if v != ".":
                temp += v
            else:
                break

        self.__no_psikologi_input_from_user = int(temp)

    def __get_data_modify_test_psikologi(self):

        data = super(Admin, self).retrievedata("test_psikologi")

        # get id pekerjaan
        self.__id_psikologi_input_from_user = data[(self.__no_psikologi_input_from_user-1)][0]

        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()

        c.execute("SELECT rowid, * FROM test_psikologi WHERE rowid=(?)", (str(self.__id_psikologi_input_from_user),))
        conn.commit()

        data = c.fetchone()

        conn.close()

        # retrieve data pekerjaan from db and save to atribute lowongan kerja
        self.__soal_psikologi = data[1]
        self.__nilai_minimum_psikologi = data[2]
        self.__nilai_maximum_psikologi = data[3]

    def input_modify_psikologi(self, frame_header, frame, frame_footer):

        Label(frame, text="Modifikasi Data Soal Psikologi").grid(row=0, column=0, columnspan=2, sticky=W,
                                                                 padx=(20, 0), pady=(0, 10))

        Label(frame, text="Soal Psikologi").grid(row=1, column=0, sticky=W, padx=(20, 10), pady=(0, 10))
        temp_soal_psikologi = self.__soal_psikologi
        self.__soal_psikologi = Entry(frame, width=40)
        self.__soal_psikologi.insert(0, temp_soal_psikologi)
        self.__soal_psikologi.grid(row=1, column=1, columnspan=2, sticky=W + E, padx=(0, 10), pady=(0, 10))

        Label(frame, text="Nilai Minimum Kelulusan").grid(row=2, column=0, sticky=W, padx=(20, 10), pady=(0, 10))
        temp_nilai_minimum_psikologi = self.__nilai_minimum_psikologi
        self.__nilai_minimum_psikologi = Entry(frame, width=40)
        self.__nilai_minimum_psikologi.insert(0, temp_nilai_minimum_psikologi)
        self.__nilai_minimum_psikologi.grid(row=2, column=1, columnspan=2, sticky=W + E, padx=(0, 10), pady=(0, 10))

        Label(frame, text="Nilai Maximum Kelulusan").grid(row=3, column=0, sticky=W, padx=(20, 10), pady=(0, 10))
        temp_nilai_maximum_psikologi = self.__nilai_maximum_psikologi
        self.__nilai_maximum_psikologi = Entry(frame, width=40)
        self.__nilai_maximum_psikologi.insert(0, temp_nilai_maximum_psikologi)
        self.__nilai_maximum_psikologi.grid(row=3, column=1, columnspan=2, sticky=W + E, padx=(0, 10), pady=(0, 10))

        submit_btn = Button(frame, text="Submit",
                            command=lambda: self.__proses_modify_psikologi(frame_header, frame, frame_footer))
        submit_btn.grid(row=13, column=1, columnspan=2, pady=20, sticky=W + E)

    def __proses_modify_psikologi(self, frame_header, frame, frame_footer):
        list_modify = list()
        list_modify.append(self.__soal_psikologi.get())
        list_modify.append(self.__nilai_minimum_psikologi.get())
        list_modify.append(self.__nilai_maximum_psikologi.get())

        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()

        c.execute("UPDATE test_psikologi SET soal = ?, nilai_minimum_kelulusan = ?, nilai_maximum_kelulusan = ?"
                  "WHERE rowid = ?",
                  (list_modify[0], list_modify[1], list_modify[2], str(self.__id_psikologi_input_from_user)))

        conn.commit()

        conn.close()

        # clear semua data attribute di object setelah input data soal psikologi ke db berhasil
        self.__soal_psikologi = ""
        self.__nilai_minimum_psikologi = ""
        self.__nilai_maximum_psikologi = ""
        self.__no_psikologi_input_from_user = int()
        self.__id_psikologi_input_from_user = int()

        window.remove_current_frame(frame_header)
        window.remove_current_frame(frame)
        window.remove_current_frame(frame_footer)

        window.menu_input_modify_akhir_psikologi_admin()

    def menu_delete_test_psikologi(self, frame_header, frame, frame_footer):

        label_menu_delete_psikologi_admin = Label(frame,
                                                  text="Pilih Soal Psikologi yang ingin di hapus")
        label_menu_delete_psikologi_admin.grid(row=50, column=0, pady=(20, 30), padx=(0, 10))

        data = super().retrievedata("test_psikologi")
        data_option = list()
        for i in range(0, len(data)):
            data_option.append(str(i + 1) + ".   " + data[i][1])

        pilihan_user = StringVar()
        pilihan_user.set(data_option[0])

        dropdown_data = OptionMenu(frame, pilihan_user, *data_option)
        dropdown_data.grid(row=50, column=1, columnspan=2, pady=(20, 30), sticky=EW)

        submit_pilihan_btn = Button(frame, text="Submit",
                                    command=lambda: [
                                        self.__submit_psikologi_pilihan_user(pilihan_user.get()),
                                        self.__delete_test_psikologi(),
                                        window.remove_current_frame(frame_header),
                                        window.destroy_current_frame(frame),
                                        window.remove_current_frame(frame_footer),
                                        window.menu_delete_akhir_psikologi_admin()
                                    ])
        submit_pilihan_btn.grid(row=50, column=3, pady=(20, 30), ipadx=10, ipady=10)

    def __delete_test_psikologi(self):

        data = super(Admin, self).retrievedata("test_psikologi")

        # get id pekerjaan
        self.__id_psikologi_input_from_user = data[(self.__no_psikologi_input_from_user - 1)][0]

        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()

        c.execute("DELETE FROM test_psikologi WHERE rowid = (?) ", (str(self.__id_psikologi_input_from_user),))
        conn.commit()

        conn.close()

        # clear attributes
        self.__no_psikologi_input_from_user = int()
        self.__id_psikologi_input_from_user = int()


class Window:
    def __init__(self):
        self.root = Tk()
        self.root.title("Program Seleksi Kerja PT XYZ")
        self.root.iconbitmap('icon.ico')
        self.root.rowconfigure(3, weight=1)
        self.program_geometry = "500x300+525+200"
        self.date_time_label = Label(self.root, text="", fg="Red", font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.root, text="Menu Sebelumnya", state=DISABLED)
        self.menu_utama_button = Button(self.root, text="Menu Utama", state=DISABLED)

        # image in program
        self.__program_logo_image = ImageTk.PhotoImage((Image.open("logo1.png")).resize((75, 75)))
        self.__harap_tunggu_image = ImageTk.PhotoImage((Image.open("harap_tunggu.png")).resize((150, 100)))
        self.__sukses_image = ImageTk.PhotoImage((Image.open("sukses.png")).resize((150, 100)))

        # create menu pelamar and admin object
        self.__menu_pelamar = MenuPelamar()
        self.__admin = Admin()

        # counter for clearing entry once
        self.__clear_entry_jenis_kelamin_counter = 1
        self.__clear_entry_pendidikan_terakhir_counter = 1
        self.__clear_entry_pengalaman_kerja_counter = 1
        self.__clear_entry_status_counter = 1
        self.__clear_entry_kategori_counter = 1

        # frame menu utama
        self.menu_utama_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_utama_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_utama_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # kumpulan frame menu pelamar kerja

        # frame menu pelamar kerja
        self.menu_utama_pelamar_kerja_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_utama_pelamar_kerja_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu isi data diri pelamar kerja
        self.menu_isi_data_diri_pelamar_kerja_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_isi_data_diri_pelamar_kerja_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu isi pertanyaan pelamar kerja
        self.menu_isi_pertanyaan_pelamar_kerja_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_isi_pertanyaan_pelamar_kerja_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu proses pelamar kerja
        self.menu_proses_pelamar_kerja_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_proses_pelamar_kerja_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_proses_pelamar_kerja_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu akhir pelamar kerja
        self.menu_akhir_pelamar_kerja_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_akhir_pelamar_kerja_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_akhir_pelamar_kerja_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # kumpulan frame menu admin

        # frame menu login admin
        self.menu_login_admin_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_login_admin_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_login_admin_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu utama admin
        self.menu_utama_admin_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_utama_admin_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_utama_admin_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu panel lowongan kerja admin
        self.menu_panel_kerja_admin_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_panel_kerja_admin_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_panel_kerja_admin_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu list lowongan kerja admin
        self.menu_list_kerja_admin_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_list_kerja_admin_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu list pelamar kerja admin
        self.menu_list_pelamar_admin_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_list_pelamar_admin_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu input lowongan kerja admin
        self.menu_input_kerja_admin_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_input_kerja_admin_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_input_kerja_admin_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu input akhir lowongan kerja admin
        self.menu_input_akhir_kerja_admin_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_input_akhir_kerja_admin_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_input_akhir_kerja_admin_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu modify lowongan kerja admin
        self.menu_modify_kerja_admin_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_modify_kerja_admin_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu input modify lowongan kerja admin
        self.menu_input_modify_kerja_admin_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_input_modify_kerja_admin_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_input_modify_kerja_admin_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu input modify akhir lowongan kerja admin
        self.menu_input_modify_akhir_kerja_admin_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_input_modify_akhir_kerja_admin_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_input_modify_akhir_kerja_admin_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu delete lowongan kerja admin
        self.menu_delete_kerja_admin_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_delete_kerja_admin_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu akhir delete lowongan kerja admin
        self.menu_delete_akhir_kerja_admin_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_delete_akhir_kerja_admin_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_delete_akhir_kerja_admin_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu panel test psikologi admin
        self.menu_panel_psikologi_admin_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_panel_psikologi_admin_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_panel_psikologi_admin_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu list test psikologi admin
        self.menu_list_psikologi_admin_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_list_psikologi_admin_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu input test psikologi admin
        self.menu_input_psikologi_admin_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_input_psikologi_admin_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu input akhir test psikologi admin
        self.menu_input_akhir_psikologi_admin_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_input_akhir_psikologi_admin_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_input_akhir_psikologi_admin_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu modify test psikologi admin
        self.menu_modify_psikologi_admin_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_modify_psikologi_admin_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu input modify test psikologi admin
        self.menu_input_modify_psikologi_admin_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_input_modify_psikologi_admin_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_input_modify_psikologi_admin_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu input modify akhir test psikologi admin
        self.menu_input_modify_akhir_psikologi_admin_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_input_modify_akhir_psikologi_admin_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_input_modify_akhir_psikologi_admin_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu delete test psikologi admin
        self.menu_delete_psikologi_admin_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_delete_psikologi_admin_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

        # frame menu akhir delete test psikologi admin
        self.menu_delete_akhir_psikologi_admin_header_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_delete_akhir_psikologi_admin_frame = LabelFrame(self.root, bd=0, highlightthickness=0)
        self.menu_delete_akhir_psikologi_admin_footer_frame = LabelFrame(self.root, bd=0, highlightthickness=0)

    @staticmethod
    def remove_current_frame(current_frame):
        current_frame.grid_remove()

    @staticmethod
    def destroy_current_frame(current_frame):
        current_frame.destroy()

    def clear_entry_jenis_kelamin_once(self, entry):
        if self.__clear_entry_jenis_kelamin_counter == 1:
            entry.delete(0, END)
            self.__clear_entry_jenis_kelamin_counter -= 1

    def clear_entry_pendidikan_terakhir_once(self, entry):
        if self.__clear_entry_pendidikan_terakhir_counter == 1:
            entry.delete(0, END)
            self.__clear_entry_pendidikan_terakhir_counter -= 1

    def clear_entry_pengalaman_kerja_once(self, entry):
        if self.__clear_entry_pengalaman_kerja_counter == 1:
            entry.delete(0, END)
            self.__clear_entry_pengalaman_kerja_counter -= 1

    def clear_entry_status_once(self, entry):
        if self.__clear_entry_status_counter == 1:
            entry.delete(0, END)
            self.__clear_entry_status_counter -= 1

    def clear_entry_kategori_once(self, entry):
        if self.__clear_entry_kategori_counter == 1:
            entry.delete(0, END)
            self.__clear_entry_kategori_counter -= 1

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
                                                    self.menu_utama_pelamar_kerja(
                                                        LabelFrame(self.root, bd=0, highlightthickness=0))])

        btn_admin = Button(self.menu_utama_frame, text="Admin",
                           command=lambda: [self.remove_current_frame(self.menu_utama_header_frame),
                                            self.remove_current_frame(self.menu_utama_frame),
                                            self.remove_current_frame(self.menu_utama_footer_frame),
                                            self.menu_login_admin("true")])

        btn_pelamar_kerja.grid(row=0, column=0, padx=(0, 50), pady=(35, 50), ipadx=15, ipady=25)
        btn_admin.grid(row=0, column=1, padx=(0, 65), pady=(35, 50), ipadx=30, ipady=25)

        # footer section
        self.date_time_label = Label(self.menu_utama_footer_frame, text="", fg="Red", font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_utama_footer_frame, text="Menu Sebelumnya", state=DISABLED)
        self.menu_utama_button = Button(self.menu_utama_footer_frame, text="Menu Utama", state=DISABLED)
        self.footer(self.menu_utama_footer_frame)

    def menu_utama_pelamar_kerja(self, frame):
        self.program_geometry = "550x300+525+200"
        self.root.geometry(self.program_geometry)

        self.menu_utama_pelamar_kerja_header_frame.grid(row=0, rowspan=2, column=0, columnspan=3, sticky="WE",
                                                        padx=(25, 0))
        frame.grid(row=2, column=0, columnspan=3, sticky="WE", padx=(25, 0))
        self.menu_utama_pelamar_kerja_footer_frame.grid(row=3, column=0, columnspan=3, sticky="WE", padx=(25, 0))

        # header section
        self.header(self.menu_utama_pelamar_kerja_header_frame)

        # container section
        self.__menu_pelamar.menu_utama(self.menu_utama_pelamar_kerja_header_frame, frame,
                                       self.menu_utama_pelamar_kerja_footer_frame)

        # footer section
        self.date_time_label = Label(self.menu_utama_pelamar_kerja_footer_frame, text="", fg="Red",
                                     font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_utama_pelamar_kerja_footer_frame, text="Menu Sebelumnya",
                                             state=ACTIVE,
                                             command=lambda: [
                                                 self.remove_current_frame(self.menu_utama_pelamar_kerja_header_frame),
                                                 self.destroy_current_frame(frame),
                                                 self.remove_current_frame(self.menu_utama_pelamar_kerja_footer_frame),
                                                 self.menu_utama()])
        self.menu_utama_button = Button(self.menu_utama_pelamar_kerja_footer_frame, text="Menu Utama", state=ACTIVE,
                                        command=lambda: [
                                            self.remove_current_frame(self.menu_utama_pelamar_kerja_header_frame),
                                            self.destroy_current_frame(frame),
                                            self.remove_current_frame(
                                                self.menu_utama_pelamar_kerja_footer_frame),
                                            self.menu_utama()])
        self.footer(self.menu_utama_pelamar_kerja_footer_frame)

    def menu_isi_data_diri_pelamar_kerja(self, pelamar, frame):
        self.program_geometry = "590x450+500+150"
        self.root.geometry(self.program_geometry)

        self.menu_isi_data_diri_pelamar_kerja_header_frame.grid(row=0, rowspan=2, column=0, columnspan=3, sticky="WE",
                                                                padx=(25, 0))
        frame.grid(row=2, column=0, columnspan=3, sticky="WE", padx=(25, 0))
        self.menu_isi_data_diri_pelamar_kerja_footer_frame.grid(row=3, column=0, columnspan=3, sticky="WE",
                                                                padx=(25, 0))

        # header section
        self.header(self.menu_isi_data_diri_pelamar_kerja_header_frame)

        # container section
        pelamar.isi_data_diri(frame)

        submit_btn = Button(frame, text="Submit",
                            command=lambda: [
                                pelamar.get_data_diri(),
                                self.remove_current_frame(self.menu_isi_data_diri_pelamar_kerja_header_frame),
                                self.destroy_current_frame(frame),
                                self.remove_current_frame(self.menu_isi_data_diri_pelamar_kerja_footer_frame),
                                self.menu_isi_pertanyaan_pelamar_kerja(pelamar, LabelFrame(self.root, bd=0,
                                                                                           highlightthickness=0))])
        submit_btn.grid(row=7, column=2, pady=(20, 40), ipadx=10, sticky=W + E)

        # footer section
        self.date_time_label = Label(self.menu_isi_data_diri_pelamar_kerja_footer_frame, text="", fg="Red",
                                     font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_isi_data_diri_pelamar_kerja_footer_frame, text="Menu Sebelumnya",
                                             state=ACTIVE,
                                             command=lambda: [
                                                 self.remove_current_frame(
                                                     self.menu_isi_data_diri_pelamar_kerja_header_frame),
                                                 self.destroy_current_frame(frame),
                                                 self.remove_current_frame(
                                                     self.menu_isi_data_diri_pelamar_kerja_footer_frame),
                                                 self.menu_utama_pelamar_kerja(
                                                     LabelFrame(self.root, bd=0, highlightthickness=0))])
        self.menu_utama_button = Button(self.menu_isi_data_diri_pelamar_kerja_footer_frame, text="Menu Utama",
                                        state=ACTIVE,
                                        command=lambda: [
                                            self.remove_current_frame(
                                                self.menu_isi_data_diri_pelamar_kerja_header_frame),
                                            self.destroy_current_frame(frame),
                                            self.remove_current_frame(
                                                self.menu_isi_data_diri_pelamar_kerja_footer_frame),
                                            self.menu_utama()])
        self.footer(self.menu_isi_data_diri_pelamar_kerja_footer_frame)

    def menu_isi_pertanyaan_pelamar_kerja(self, pelamar, frame):
        self.program_geometry = "900x710+300+50"
        self.root.geometry(self.program_geometry)

        self.menu_isi_pertanyaan_pelamar_kerja_header_frame.grid(row=0, rowspan=2, column=0, columnspan=3, sticky="WE",
                                                                 padx=(25, 0))
        frame.grid(row=2, column=0, columnspan=3, sticky="WE", padx=(25, 0))
        self.menu_isi_pertanyaan_pelamar_kerja_footer_frame.grid(row=3, column=0, columnspan=3,
                                                                 sticky="WE", padx=(25, 0))

        # header section
        self.header(self.menu_isi_pertanyaan_pelamar_kerja_header_frame)

        # container section
        pelamar.isi_data_pertanyaan(frame)

        submit_btn = Button(frame, text="Submit", width=20,
                            command=lambda: [
                                self.remove_current_frame(self.menu_isi_pertanyaan_pelamar_kerja_header_frame),
                                self.destroy_current_frame(frame),
                                self.remove_current_frame(self.menu_isi_pertanyaan_pelamar_kerja_footer_frame),
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
                                                 self.destroy_current_frame(frame),
                                                 self.remove_current_frame(
                                                     self.menu_isi_pertanyaan_pelamar_kerja_footer_frame),
                                                 self.menu_isi_data_diri_pelamar_kerja(pelamar,
                                                                                       LabelFrame(self.root, bd=0,
                                                                                                  highlightthickness=0))
                                             ])
        self.menu_utama_button = Button(self.menu_isi_pertanyaan_pelamar_kerja_footer_frame, text="Menu Utama",
                                        state=ACTIVE,
                                        command=lambda: [
                                            self.remove_current_frame(
                                                self.menu_isi_pertanyaan_pelamar_kerja_header_frame),
                                            self.destroy_current_frame(frame),
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
        Label(self.menu_login_admin_frame, text="Username", font=("Helvetica", 10)).grid(row=0, column=0, pady=(15, 15))
        Label(self.menu_login_admin_frame, text="Password", font=("Helvetica", 10)).grid(row=1, column=0, pady=(0, 20))

        username_input = Entry(self.menu_login_admin_frame)
        username_input.grid(row=0, column=1, columnspan=2, pady=(20, 20), sticky=W)

        password_input = Entry(self.menu_login_admin_frame, show="*")
        password_input.grid(row=1, column=1, columnspan=2, pady=(0, 20), sticky=W)

        submit_btn = Button(self.menu_login_admin_frame, text="Submit", font=("Helvetica", 10),
                            command=lambda: self.admin_verification(self.menu_login_admin_header_frame,
                                                                    self.menu_login_admin_frame,
                                                                    self.menu_login_admin_footer_frame,
                                                                    username_input, password_input))
        submit_btn.grid(row=2, column=1, pady=(0, 10))

        label_check = Label(self.menu_login_admin_frame, text="Username atau Password anda salah, silahkan coba lagi",
                            font=("Helvetica", "10", "bold"), fg=self.menu_login_admin_frame.cget('bg'))

        if check != "true":
            label_check.configure(fg="red")

        label_check.grid(row=3, column=0, columnspan=3, pady=(0, 10))

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
                                                  self.remove_current_frame(self.menu_utama_admin_footer_frame),
                                                  self.menu_panel_kerja_admin()])

        btn_panel_psikologi = Button(self.menu_utama_admin_frame, text="Panel Test Psikologi",
                                     command=lambda: [self.remove_current_frame(self.menu_utama_admin_header_frame),
                                                      self.remove_current_frame(self.menu_utama_admin_frame),
                                                      self.remove_current_frame(self.menu_utama_admin_footer_frame),
                                                      self.menu_panel_psikologi_admin(
                                                          LabelFrame(self.root, bd=0, highlightthickness=0))])

        btn_panel_kerja.grid(row=0, column=0, padx=(15, 50), pady=(35, 50), ipadx=25, ipady=25)
        btn_panel_psikologi.grid(row=0, column=1, pady=(35, 50), ipadx=30, ipady=25)

        # footer section
        self.date_time_label = Label(self.menu_utama_admin_footer_frame, text="", fg="Red",
                                     font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_utama_admin_footer_frame, text="Menu Sebelumnya",
                                             state=DISABLED)
        self.menu_utama_button = Button(self.menu_utama_admin_footer_frame, text="Logout",
                                        command=lambda: [
                                            self.remove_current_frame(self.menu_utama_admin_header_frame),
                                            self.remove_current_frame(self.menu_utama_admin_frame),
                                            self.remove_current_frame(self.menu_utama_admin_footer_frame),
                                            self.menu_utama()])
        self.footer(self.menu_utama_admin_footer_frame)

    def menu_panel_kerja_admin(self):
        self.program_geometry = "670x450+425+150"
        self.root.geometry(self.program_geometry)

        self.menu_panel_kerja_admin_header_frame.grid(row=0, rowspan=2, column=0, columnspan=3)
        self.menu_panel_kerja_admin_frame.grid(row=2, column=0, columnspan=3)
        self.menu_panel_kerja_admin_footer_frame.grid(row=3, column=0, columnspan=3)

        # header section
        self.header(self.menu_panel_kerja_admin_header_frame)

        # container section
        btn_list_lowongan_kerja = Button(self.menu_panel_kerja_admin_frame, text="List Lowongan Kerja",
                                         command=lambda: [
                                             self.remove_current_frame(self.menu_panel_kerja_admin_header_frame),
                                             self.remove_current_frame(self.menu_panel_kerja_admin_frame),
                                             self.remove_current_frame(self.menu_panel_kerja_admin_footer_frame),
                                             self.menu_list_kerja_admin(
                                                 LabelFrame(self.root, bd=0, highlightthickness=0))
                                             ])

        btn_list_pelamar_kerja = Button(self.menu_panel_kerja_admin_frame, text="List Pelamar Kerja",
                                        command=lambda: [
                                            self.remove_current_frame(self.menu_panel_kerja_admin_header_frame),
                                            self.remove_current_frame(self.menu_panel_kerja_admin_frame),
                                            self.remove_current_frame(self.menu_panel_kerja_admin_footer_frame),
                                            self.menu_list_pelamar_admin(
                                                LabelFrame(self.root, bd=0, highlightthickness=0))
                                        ])

        btn_input_lowongan_kerja = Button(self.menu_panel_kerja_admin_frame, text="Input Lowongan Kerja",
                                          command=lambda: [
                                              self.remove_current_frame(self.menu_panel_kerja_admin_header_frame),
                                              self.remove_current_frame(self.menu_panel_kerja_admin_frame),
                                              self.remove_current_frame(self.menu_panel_kerja_admin_footer_frame),
                                              self.menu_input_kerja_admin()])

        btn_modify_lowongan_kerja = Button(self.menu_panel_kerja_admin_frame, text="Modifikasi Lowongan Kerja",
                                           command=lambda: [
                                               self.remove_current_frame(self.menu_panel_kerja_admin_header_frame),
                                               self.remove_current_frame(self.menu_panel_kerja_admin_frame),
                                               self.remove_current_frame(self.menu_panel_kerja_admin_footer_frame),
                                               self.menu_modify_kerja_admin(
                                                   LabelFrame(self.root, bd=0, highlightthickness=0))])

        btn_hapus_lowongan_kerja = Button(self.menu_panel_kerja_admin_frame, text="Hapus Lowongan Kerja",
                                          command=lambda: [
                                              self.remove_current_frame(self.menu_panel_kerja_admin_header_frame),
                                              self.remove_current_frame(self.menu_panel_kerja_admin_frame),
                                              self.remove_current_frame(self.menu_panel_kerja_admin_footer_frame),
                                              self.menu_delete_kerja_admin(
                                                  LabelFrame(self.root, bd=0, highlightthickness=0))])

        btn_list_lowongan_kerja.grid(row=0, column=0, padx=(15, 50), pady=(35, 20), ipadx=20, ipady=25, sticky=W)
        btn_list_pelamar_kerja.grid(row=0, column=2, padx=(15, 50), pady=(35, 20), ipadx=30, ipady=25, sticky=E)
        btn_input_lowongan_kerja.grid(row=1, column=0, padx=(15, 50), pady=(35, 50), ipadx=15, ipady=25)
        btn_modify_lowongan_kerja.grid(row=1, column=1, padx=(15, 50), pady=(35, 50), ipadx=15, ipady=25)
        btn_hapus_lowongan_kerja.grid(row=1, column=2, padx=(15, 50), pady=(35, 50), ipadx=15, ipady=25)

        # footer section
        self.date_time_label = Label(self.menu_panel_kerja_admin_footer_frame, text="", fg="Red",
                                     font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_panel_kerja_admin_footer_frame, text="Menu Sebelumnya",
                                             command=lambda: [
                                                 self.remove_current_frame(self.menu_panel_kerja_admin_header_frame),
                                                 self.remove_current_frame(self.menu_panel_kerja_admin_frame),
                                                 self.remove_current_frame(self.menu_panel_kerja_admin_footer_frame),
                                                 self.menu_utama_admin()])
        self.menu_utama_button = Button(self.menu_panel_kerja_admin_footer_frame, text="Logout",
                                        command=lambda: [
                                            self.remove_current_frame(self.menu_panel_kerja_admin_header_frame),
                                            self.remove_current_frame(self.menu_panel_kerja_admin_frame),
                                            self.remove_current_frame(self.menu_panel_kerja_admin_footer_frame),
                                            self.menu_utama()])
        self.footer(self.menu_panel_kerja_admin_footer_frame)

    def menu_list_kerja_admin(self, frame):
        self.program_geometry = "800x450+340+150"
        self.root.geometry(self.program_geometry)

        self.menu_list_kerja_admin_header_frame.grid(row=0, rowspan=2, column=0, columnspan=3, padx=(25, 0))
        frame.grid(row=2, column=0, columnspan=3, sticky="WE", padx=(25, 0))
        self.menu_list_kerja_admin_footer_frame.grid(row=3, column=0, columnspan=3, sticky="WE", padx=(25, 0))

        # header section
        self.header(self.menu_list_kerja_admin_header_frame)

        # container section
        self.__admin.printlist(frame)

        # footer section
        self.date_time_label = Label(self.menu_list_kerja_admin_footer_frame, text="", fg="Red",
                                     font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_list_kerja_admin_footer_frame, text="Menu Sebelumnya",
                                             command=lambda: [
                                                 self.remove_current_frame(self.menu_list_kerja_admin_header_frame),
                                                 self.destroy_current_frame(frame),
                                                 self.remove_current_frame(self.menu_list_kerja_admin_footer_frame),
                                                 self.menu_panel_kerja_admin()])
        self.menu_utama_button = Button(self.menu_list_kerja_admin_footer_frame, text="Logout",
                                        command=lambda: [
                                            self.remove_current_frame(self.menu_list_kerja_admin_header_frame),
                                            self.destroy_current_frame(frame),
                                            self.remove_current_frame(self.menu_list_kerja_admin_footer_frame),
                                            self.menu_utama()])
        self.footer(self.menu_list_kerja_admin_footer_frame)

    def menu_list_pelamar_admin(self, frame):
        self.program_geometry = "800x450+340+150"
        self.root.geometry(self.program_geometry)

        self.menu_list_pelamar_admin_header_frame.grid(row=0, rowspan=2, column=0, columnspan=3, padx=(25, 0))
        frame.grid(row=2, column=0, columnspan=3, sticky="WE", padx=(25, 0))
        self.menu_list_pelamar_admin_footer_frame.grid(row=3, column=0, columnspan=3, sticky="WE", padx=(25, 0))

        # header section
        self.header(self.menu_list_pelamar_admin_header_frame)

        # container section
        self.__admin.printlist_pelamar(frame)

        # footer section
        self.date_time_label = Label(self.menu_list_pelamar_admin_footer_frame, text="", fg="Red",
                                     font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_list_pelamar_admin_footer_frame, text="Menu Sebelumnya",
                                             command=lambda: [
                                                 self.remove_current_frame(self.menu_list_pelamar_admin_header_frame),
                                                 self.destroy_current_frame(frame),
                                                 self.remove_current_frame(self.menu_list_pelamar_admin_footer_frame),
                                                 self.menu_panel_kerja_admin()])
        self.menu_utama_button = Button(self.menu_list_pelamar_admin_footer_frame, text="Logout",
                                        command=lambda: [
                                            self.remove_current_frame(self.menu_list_pelamar_admin_header_frame),
                                            self.destroy_current_frame(frame),
                                            self.remove_current_frame(self.menu_list_pelamar_admin_footer_frame),
                                            self.menu_utama()])
        self.footer(self.menu_list_pelamar_admin_footer_frame)

    def menu_input_kerja_admin(self):
        self.program_geometry = "600x650+450+50"
        self.root.geometry(self.program_geometry)

        self.menu_input_kerja_admin_header_frame.grid(row=0, rowspan=2, column=0, columnspan=3)
        self.menu_input_kerja_admin_frame.grid(row=2, column=0, columnspan=3)
        self.menu_input_kerja_admin_footer_frame.grid(row=3, column=0, columnspan=3)

        # header section
        self.header(self.menu_input_kerja_admin_header_frame)

        # container section
        self.__admin.tambah_lowongan_pekerjaan(self.menu_input_kerja_admin_header_frame,
                                               self.menu_input_kerja_admin_frame,
                                               self.menu_input_kerja_admin_footer_frame)

        # footer section
        self.date_time_label = Label(self.menu_input_kerja_admin_footer_frame, text="", fg="Red",
                                     font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_input_kerja_admin_footer_frame, text="Menu Sebelumnya",
                                             command=lambda: [
                                                 self.remove_current_frame(self.menu_input_kerja_admin_header_frame),
                                                 self.remove_current_frame(self.menu_input_kerja_admin_frame),
                                                 self.remove_current_frame(self.menu_input_kerja_admin_footer_frame),
                                                 self.menu_panel_kerja_admin()])
        self.menu_utama_button = Button(self.menu_input_kerja_admin_footer_frame, text="Logout",
                                        command=lambda: [
                                            self.remove_current_frame(self.menu_input_kerja_admin_header_frame),
                                            self.remove_current_frame(self.menu_input_kerja_admin_frame),
                                            self.remove_current_frame(self.menu_input_kerja_admin_footer_frame),
                                            self.menu_utama()])
        self.footer(self.menu_input_kerja_admin_footer_frame)

    def menu_input_akhir_kerja_admin(self):
        self.program_geometry = "670x350+430+200"
        self.root.geometry(self.program_geometry)

        self.menu_input_akhir_kerja_admin_header_frame.grid(row=0, rowspan=2, column=0, columnspan=3, sticky="WE",
                                                            padx=(25, 0))
        self.menu_input_akhir_kerja_admin_frame.grid(row=2, column=0, columnspan=3, sticky="WE", padx=(25, 0))
        self.menu_input_akhir_kerja_admin_footer_frame.grid(row=3, column=0, columnspan=3, sticky="WE", padx=(25, 0))

        # header section
        self.header(self.menu_input_akhir_kerja_admin_header_frame)

        # container section
        sukses_image = Label(self.menu_input_akhir_kerja_admin_frame, image=self.__sukses_image)
        sukses_image.grid(row=0, rowspan=2, column=0, columnspan=3, pady=(10, 10))

        Label(self.menu_input_akhir_kerja_admin_frame,
              text="Sukses menambahkan lowongan pekerjaan, silahkan kembali ke menu admin atau logout",
              font=("Helvetica", 10, "bold")).grid(row=2, column=0, columnspan=3, pady=(10, 10))

        # footer section
        self.date_time_label = Label(self.menu_input_akhir_kerja_admin_footer_frame, text="", fg="Red",
                                     font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_input_akhir_kerja_admin_footer_frame, text="Menu Admin",
                                             command=lambda: [
                                                 self.remove_current_frame(
                                                     self.menu_input_akhir_kerja_admin_header_frame),
                                                 self.remove_current_frame(self.menu_input_akhir_kerja_admin_frame),
                                                 self.remove_current_frame(
                                                     self.menu_input_akhir_kerja_admin_footer_frame),
                                                 self.menu_utama_admin()
                                             ])
        self.menu_utama_button = Button(self.menu_input_akhir_kerja_admin_footer_frame, text="Logout", state=ACTIVE,
                                        command=lambda: [
                                            self.remove_current_frame(self.menu_input_akhir_kerja_admin_header_frame),
                                            self.remove_current_frame(self.menu_input_akhir_kerja_admin_frame),
                                            self.remove_current_frame(self.menu_input_akhir_kerja_admin_footer_frame),
                                            self.menu_utama()
                                        ])
        self.footer(self.menu_input_akhir_kerja_admin_footer_frame)

    def menu_modify_kerja_admin(self, frame):
        self.program_geometry = "800x450+340+150"
        self.root.geometry(self.program_geometry)

        self.menu_modify_kerja_admin_header_frame.grid(row=0, rowspan=2, column=0, columnspan=3, padx=(25, 0))
        frame.grid(row=2, column=0, columnspan=3, sticky="WE", padx=(25, 0))
        self.menu_modify_kerja_admin_footer_frame.grid(row=3, column=0, columnspan=3, sticky="WE", padx=(25, 0))

        # header section
        self.header(self.menu_modify_kerja_admin_header_frame)

        # container section
        self.__admin.printlist(frame)
        self.__admin.menu_modify_lowongan_pekerjaan(self.menu_modify_kerja_admin_header_frame,
                                                    frame,
                                                    self.menu_modify_kerja_admin_footer_frame)

        # footer section
        self.date_time_label = Label(self.menu_modify_kerja_admin_footer_frame, text="", fg="Red",
                                     font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_modify_kerja_admin_footer_frame, text="Menu Sebelumnya",
                                             command=lambda: [
                                                 self.remove_current_frame(
                                                     self.menu_modify_kerja_admin_header_frame),
                                                 self.destroy_current_frame(frame),
                                                 self.remove_current_frame(
                                                     self.menu_modify_kerja_admin_footer_frame),
                                                 self.menu_panel_kerja_admin()
                                             ])
        self.menu_utama_button = Button(self.menu_modify_kerja_admin_footer_frame, text="Logout", state=ACTIVE,
                                        command=lambda: [
                                            self.remove_current_frame(self.menu_modify_kerja_admin_header_frame),
                                            self.destroy_current_frame(frame),
                                            self.remove_current_frame(self.menu_modify_kerja_admin_footer_frame),
                                            self.menu_utama()
                                        ])
        self.footer(self.menu_modify_kerja_admin_footer_frame)

    def menu_input_modify_kerja_admin(self):
        self.program_geometry = "600x650+450+50"
        self.root.geometry(self.program_geometry)

        self.menu_input_modify_kerja_admin_header_frame.grid(row=0, rowspan=2, column=0, columnspan=3, padx=(25, 0))
        self.menu_input_modify_kerja_admin_frame.grid(row=2, column=0, columnspan=3, sticky="WE", padx=(25, 0))
        self.menu_input_modify_kerja_admin_footer_frame.grid(row=3, column=0, columnspan=3, sticky="WE", padx=(25, 0))

        # header section
        self.header(self.menu_input_modify_kerja_admin_header_frame)

        # container section
        self.__admin.input_modify_lowongan_pekerjaan(self.menu_input_modify_kerja_admin_header_frame,
                                                     self.menu_input_modify_kerja_admin_frame,
                                                     self.menu_input_modify_kerja_admin_footer_frame)

        # footer section
        self.date_time_label = Label(self.menu_input_modify_kerja_admin_footer_frame, text="", fg="Red",
                                     font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_input_modify_kerja_admin_footer_frame, text="Menu Sebelumnya",
                                             command=lambda: [
                                                 self.remove_current_frame(
                                                     self.menu_input_modify_kerja_admin_header_frame),
                                                 self.remove_current_frame(self.menu_input_modify_kerja_admin_frame),
                                                 self.remove_current_frame(
                                                     self.menu_input_modify_kerja_admin_footer_frame),
                                                 self.menu_modify_kerja_admin(
                                                     LabelFrame(self.root, bd=0, highlightthickness=0))
                                             ])
        self.menu_utama_button = Button(self.menu_input_modify_kerja_admin_footer_frame, text="Logout",
                                        state=ACTIVE,
                                        command=lambda: [
                                            self.remove_current_frame(self.menu_input_modify_kerja_admin_header_frame),
                                            self.remove_current_frame(self.menu_input_modify_kerja_admin_frame),
                                            self.remove_current_frame(self.menu_input_modify_kerja_admin_footer_frame),
                                            self.menu_utama()
                                        ])
        self.footer(self.menu_input_modify_kerja_admin_footer_frame)

    def menu_input_modify_akhir_kerja_admin(self):
        self.program_geometry = "670x350+430+200"
        self.root.geometry(self.program_geometry)

        self.menu_input_modify_akhir_kerja_admin_header_frame.grid(row=0, rowspan=2, column=0, columnspan=3,
                                                                   sticky="WE", padx=(25, 0))
        self.menu_input_modify_akhir_kerja_admin_frame.grid(row=2, column=0, columnspan=3, sticky="WE", padx=(25, 0))
        self.menu_input_modify_akhir_kerja_admin_footer_frame.grid(row=3, column=0, columnspan=3, sticky="WE",
                                                                   padx=(25, 0))

        # header section
        self.header(self.menu_input_modify_akhir_kerja_admin_header_frame)

        # container section
        sukses_image = Label(self.menu_input_modify_akhir_kerja_admin_frame, image=self.__sukses_image)
        sukses_image.grid(row=0, rowspan=2, column=0, columnspan=3, pady=(10, 10))

        Label(self.menu_input_modify_akhir_kerja_admin_frame,
              text="Sukses mengubah lowongan pekerjaan, silahkan kembali ke menu admin atau logout",
              font=("Helvetica", 10, "bold")).grid(row=2, column=0, columnspan=3, pady=(10, 10))

        # footer section
        self.date_time_label = Label(self.menu_input_modify_akhir_kerja_admin_footer_frame, text="", fg="Red",
                                     font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_input_modify_akhir_kerja_admin_footer_frame, text="Menu Admin",
                                             command=lambda: [
                                                 self.remove_current_frame(
                                                     self.menu_input_modify_akhir_kerja_admin_header_frame),
                                                 self.remove_current_frame(
                                                     self.menu_input_modify_akhir_kerja_admin_frame),
                                                 self.remove_current_frame(
                                                     self.menu_input_modify_akhir_kerja_admin_footer_frame),
                                                 self.menu_utama_admin()
                                             ])
        self.menu_utama_button = Button(self.menu_input_modify_akhir_kerja_admin_footer_frame, text="Logout",
                                        state=ACTIVE,
                                        command=lambda: [
                                            self.remove_current_frame(
                                                self.menu_input_modify_akhir_kerja_admin_header_frame),
                                            self.remove_current_frame(self.menu_input_modify_akhir_kerja_admin_frame),
                                            self.remove_current_frame(
                                                self.menu_input_modify_akhir_kerja_admin_footer_frame),
                                            self.menu_utama()
                                        ])
        self.footer(self.menu_input_modify_akhir_kerja_admin_footer_frame)

    def menu_delete_kerja_admin(self, frame):
        self.program_geometry = "800x450+340+150"
        self.root.geometry(self.program_geometry)

        self.menu_delete_kerja_admin_header_frame.grid(row=0, rowspan=2, column=0, columnspan=3, padx=(25, 0))
        frame.grid(row=2, column=0, columnspan=3, sticky="WE", padx=(25, 0))
        self.menu_delete_kerja_admin_footer_frame.grid(row=3, column=0, columnspan=3, sticky="WE", padx=(25, 0))

        # header section
        self.header(self.menu_delete_kerja_admin_header_frame)

        # container section
        self.__admin.printlist(frame)
        self.__admin.menu_delete_lowongan_pekerjaan(self.menu_delete_kerja_admin_header_frame,
                                                    frame,
                                                    self.menu_delete_kerja_admin_footer_frame)

        # footer section
        self.date_time_label = Label(self.menu_delete_kerja_admin_footer_frame, text="", fg="Red",
                                     font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_delete_kerja_admin_footer_frame, text="Menu Sebelumnya",
                                             command=lambda: [
                                                 self.remove_current_frame(
                                                     self.menu_delete_kerja_admin_header_frame),
                                                 self.destroy_current_frame(frame),
                                                 self.remove_current_frame(
                                                     self.menu_delete_kerja_admin_footer_frame),
                                                 self.menu_panel_kerja_admin()
                                             ])
        self.menu_utama_button = Button(self.menu_delete_kerja_admin_footer_frame, text="Logout", state=ACTIVE,
                                        command=lambda: [
                                            self.remove_current_frame(self.menu_delete_kerja_admin_header_frame),
                                            self.destroy_current_frame(frame),
                                            self.remove_current_frame(self.menu_delete_kerja_admin_footer_frame),
                                            self.menu_utama()
                                        ])
        self.footer(self.menu_delete_kerja_admin_footer_frame)

    def menu_delete_akhir_kerja_admin(self):
        self.program_geometry = "670x350+430+200"
        self.root.geometry(self.program_geometry)

        self.menu_delete_akhir_kerja_admin_header_frame.grid(row=0, rowspan=2, column=0, columnspan=3,
                                                             sticky="WE", padx=(25, 0))
        self.menu_delete_akhir_kerja_admin_frame.grid(row=2, column=0, columnspan=3, sticky="WE", padx=(25, 0))
        self.menu_delete_akhir_kerja_admin_footer_frame.grid(row=3, column=0, columnspan=3, sticky="WE",
                                                             padx=(25, 0))

        # header section
        self.header(self.menu_delete_akhir_kerja_admin_header_frame)

        # container section
        sukses_image = Label(self.menu_delete_akhir_kerja_admin_frame, image=self.__sukses_image)
        sukses_image.grid(row=0, rowspan=2, column=0, columnspan=3, pady=(10, 10))

        Label(self.menu_delete_akhir_kerja_admin_frame,
              text="Sukses menghapus lowongan pekerjaan, silahkan kembali ke menu admin atau logout",
              font=("Helvetica", 10, "bold")).grid(row=2, column=0, columnspan=3, pady=(10, 10))

        # footer section
        self.date_time_label = Label(self.menu_delete_akhir_kerja_admin_footer_frame, text="", fg="Red",
                                     font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_delete_akhir_kerja_admin_footer_frame, text="Menu Admin",
                                             command=lambda: [
                                                 self.remove_current_frame(
                                                     self.menu_delete_akhir_kerja_admin_header_frame),
                                                 self.remove_current_frame(
                                                     self.menu_delete_akhir_kerja_admin_frame),
                                                 self.remove_current_frame(
                                                     self.menu_delete_akhir_kerja_admin_footer_frame),
                                                 self.menu_utama_admin()
                                             ])
        self.menu_utama_button = Button(self.menu_delete_akhir_kerja_admin_footer_frame, text="Logout",
                                        state=ACTIVE,
                                        command=lambda: [
                                            self.remove_current_frame(
                                                self.menu_delete_akhir_kerja_admin_header_frame),
                                            self.remove_current_frame(self.menu_delete_akhir_kerja_admin_frame),
                                            self.remove_current_frame(
                                                self.menu_delete_akhir_kerja_admin_footer_frame),
                                            self.menu_utama()
                                        ])
        self.footer(self.menu_delete_akhir_kerja_admin_footer_frame)

    def menu_panel_psikologi_admin(self, frame):
        self.program_geometry = "690x450+405+150"
        self.root.geometry(self.program_geometry)

        self.menu_panel_psikologi_admin_header_frame.grid(row=0, rowspan=2, column=0, columnspan=3)
        frame.grid(row=2, column=0, columnspan=3)
        self.menu_panel_psikologi_admin_footer_frame.grid(row=3, column=0, columnspan=3)

        # header section
        self.header(self.menu_panel_psikologi_admin_header_frame)

        # get berapa jumlah soal psikologi
        jumlah_soal = self.__admin.count_soal_psikologi()

        # container section
        btn_list_tes_psikologi = Button(frame, text="List Test Psikologi",
                                        command=lambda: [
                                            self.remove_current_frame(self.menu_panel_psikologi_admin_header_frame),
                                            self.destroy_current_frame(frame),
                                            self.remove_current_frame(self.menu_panel_psikologi_admin_footer_frame),
                                            self.menu_list_psikologi_admin(
                                                LabelFrame(self.root, bd=0, highlightthickness=0))
                                        ])

        btn_input_tes_psikologi = Button(frame, text="Input Test Psikologi",
                                         command=lambda: [
                                             self.remove_current_frame(self.menu_panel_psikologi_admin_header_frame),
                                             self.destroy_current_frame(frame),
                                             self.remove_current_frame(self.menu_panel_psikologi_admin_footer_frame),
                                             self.menu_input_psikologi_admin(jumlah_soal,
                                                                             LabelFrame(self.root, bd=0,
                                                                                        highlightthickness=0))])

        btn_modify_tes_psikologi = Button(frame, text="Modifikasi Test Psikologi",
                                          command=lambda: [
                                              self.remove_current_frame(self.menu_panel_psikologi_admin_header_frame),
                                              self.destroy_current_frame(frame),
                                              self.remove_current_frame(self.menu_panel_psikologi_admin_footer_frame),
                                              self.menu_modify_psikologi_admin(
                                                  LabelFrame(self.root, bd=0, highlightthickness=0))])

        btn_hapus_tes_psikologi = Button(frame, text="Hapus Test Psikologi",
                                         command=lambda: [
                                             self.remove_current_frame(self.menu_panel_psikologi_admin_header_frame),
                                             self.destroy_current_frame(frame),
                                             self.remove_current_frame(self.menu_panel_psikologi_admin_footer_frame),
                                             self.menu_delete_psikologi_admin(
                                                 LabelFrame(self.root, bd=0, highlightthickness=0))])

        btn_list_tes_psikologi.grid(row=0, column=1, padx=(15, 50), pady=(35, 20), ipadx=20, ipady=25, sticky=W + E)
        btn_input_tes_psikologi.grid(row=1, column=0, padx=(15, 50), pady=(35, 30), ipadx=15, ipady=25)
        btn_modify_tes_psikologi.grid(row=1, column=1, padx=(15, 50), pady=(35, 30), ipadx=15, ipady=25)
        btn_hapus_tes_psikologi.grid(row=1, column=2, padx=(15, 50), pady=(35, 30), ipadx=15, ipady=25)

        if jumlah_soal != 5:
            Label(frame,
                  text="Peringatan : Hanya ada {} dari 5 Pertanyaan Test Psikologi! Harap tambahkan {} Pertanyaan !".
                  format(jumlah_soal, 5 - jumlah_soal), font=("Helvetica", "10", "bold"),
                  fg="red").grid(row=2, column=0, columnspan=3, pady=(0, 10))

        # footer section
        self.date_time_label = Label(self.menu_panel_psikologi_admin_footer_frame, text="", fg="Red",
                                     font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_panel_psikologi_admin_footer_frame, text="Menu Sebelumnya",
                                             command=lambda: [
                                                 self.remove_current_frame(
                                                     self.menu_panel_psikologi_admin_header_frame),
                                                 self.destroy_current_frame(frame),
                                                 self.remove_current_frame(
                                                     self.menu_panel_psikologi_admin_footer_frame),
                                                 self.menu_utama_admin()])
        self.menu_utama_button = Button(self.menu_panel_psikologi_admin_footer_frame, text="Logout",
                                        command=lambda: [
                                            self.remove_current_frame(self.menu_panel_psikologi_admin_header_frame),
                                            self.destroy_current_frame(frame),
                                            self.remove_current_frame(self.menu_panel_psikologi_admin_footer_frame),
                                            self.menu_utama()])
        self.footer(self.menu_panel_psikologi_admin_footer_frame)

    def menu_list_psikologi_admin(self, frame):
        self.program_geometry = "1040x450+240+150"
        self.root.geometry(self.program_geometry)

        self.menu_list_psikologi_admin_header_frame.grid(row=0, rowspan=2, column=0, columnspan=3, padx=(25, 0))
        frame.grid(row=2, column=0, columnspan=3, sticky="WE", padx=(25, 0))
        self.menu_list_psikologi_admin_footer_frame.grid(row=3, column=0, columnspan=3, sticky="WE", padx=(25, 0))

        # header section
        self.header(self.menu_list_psikologi_admin_header_frame)

        # container section
        self.__admin.printlist_psikologi(frame)

        # footer section
        self.date_time_label = Label(self.menu_list_psikologi_admin_footer_frame, text="", fg="Red",
                                     font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_list_psikologi_admin_footer_frame, text="Menu Sebelumnya",
                                             command=lambda: [
                                                 self.remove_current_frame(self.menu_list_psikologi_admin_header_frame),
                                                 self.destroy_current_frame(frame),
                                                 self.remove_current_frame(self.menu_list_psikologi_admin_footer_frame),
                                                 self.menu_panel_psikologi_admin(
                                                     LabelFrame(self.root, bd=0, highlightthickness=0))])
        self.menu_utama_button = Button(self.menu_list_psikologi_admin_footer_frame, text="Logout",
                                        command=lambda: [
                                            self.remove_current_frame(self.menu_list_psikologi_admin_header_frame),
                                            self.destroy_current_frame(frame),
                                            self.remove_current_frame(self.menu_list_psikologi_admin_footer_frame),
                                            self.menu_utama()])
        self.footer(self.menu_list_psikologi_admin_footer_frame)

    def menu_input_psikologi_admin(self, jumlah_soal, frame):
        self.program_geometry = "600x650+450+50"
        self.root.geometry(self.program_geometry)

        self.menu_input_psikologi_admin_header_frame.grid(row=0, rowspan=2, column=0, columnspan=3)
        frame.grid(row=2, column=0, columnspan=3)
        self.menu_input_psikologi_admin_footer_frame.grid(row=3, column=0, columnspan=3)

        # header section
        self.header(self.menu_input_psikologi_admin_header_frame)

        # container section
        self.__admin.tambah_test_psikologi(self.menu_input_psikologi_admin_header_frame,
                                           frame, self.menu_input_psikologi_admin_footer_frame, jumlah_soal)

        # footer section
        self.date_time_label = Label(self.menu_input_psikologi_admin_footer_frame, text="", fg="Red",
                                     font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_input_psikologi_admin_footer_frame, text="Menu Sebelumnya",
                                             command=lambda: [
                                                 self.remove_current_frame(
                                                     self.menu_input_psikologi_admin_header_frame),
                                                 self.destroy_current_frame(frame),
                                                 self.remove_current_frame(
                                                     self.menu_input_psikologi_admin_footer_frame),
                                                 self.menu_panel_psikologi_admin(
                                                     LabelFrame(self.root, bd=0, highlightthickness=0))])
        self.menu_utama_button = Button(self.menu_input_psikologi_admin_footer_frame, text="Logout",
                                        command=lambda: [
                                            self.remove_current_frame(self.menu_input_psikologi_admin_header_frame),
                                            self.destroy_current_frame(frame),
                                            self.remove_current_frame(self.menu_input_psikologi_admin_footer_frame),
                                            self.menu_utama()])
        self.footer(self.menu_input_psikologi_admin_footer_frame)

    def menu_input_akhir_psikologi_admin(self):
        self.program_geometry = "670x350+430+200"
        self.root.geometry(self.program_geometry)

        self.menu_input_akhir_psikologi_admin_header_frame.grid(row=0, rowspan=2, column=0, columnspan=3, sticky="WE",
                                                                padx=(25, 0))
        self.menu_input_akhir_psikologi_admin_frame.grid(row=2, column=0, columnspan=3, sticky="WE", padx=(25, 0))
        self.menu_input_akhir_psikologi_admin_footer_frame.grid(row=3, column=0, columnspan=3, sticky="WE",
                                                                padx=(25, 0))

        # header section
        self.header(self.menu_input_akhir_psikologi_admin_header_frame)

        # container section
        sukses_image = Label(self.menu_input_akhir_psikologi_admin_frame, image=self.__sukses_image)
        sukses_image.grid(row=0, rowspan=2, column=0, columnspan=3, pady=(10, 10))

        Label(self.menu_input_akhir_psikologi_admin_frame,
              text="Sukses menambahkan soal psikologi, silahkan kembali ke menu admin atau logout",
              font=("Helvetica", 10, "bold")).grid(row=2, column=0, columnspan=3, pady=(10, 10))

        # footer section
        self.date_time_label = Label(self.menu_input_akhir_psikologi_admin_footer_frame, text="", fg="Red",
                                     font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_input_akhir_psikologi_admin_footer_frame, text="Menu Admin",
                                             command=lambda: [
                                                 self.remove_current_frame(
                                                     self.menu_input_akhir_psikologi_admin_header_frame),
                                                 self.remove_current_frame(self.menu_input_akhir_psikologi_admin_frame),
                                                 self.remove_current_frame(
                                                     self.menu_input_akhir_psikologi_admin_footer_frame),
                                                 self.menu_utama_admin()
                                             ])
        self.menu_utama_button = Button(self.menu_input_akhir_psikologi_admin_footer_frame, text="Logout", state=ACTIVE,
                                        command=lambda: [
                                            self.remove_current_frame(
                                                self.menu_input_akhir_psikologi_admin_header_frame),
                                            self.remove_current_frame(self.menu_input_akhir_psikologi_admin_frame),
                                            self.remove_current_frame(
                                                self.menu_input_akhir_psikologi_admin_footer_frame),
                                            self.menu_utama()
                                        ])
        self.footer(self.menu_input_akhir_psikologi_admin_footer_frame)

    def menu_modify_psikologi_admin(self, frame):
        self.program_geometry = "1240x450+140+150"
        self.root.geometry(self.program_geometry)

        self.menu_modify_psikologi_admin_header_frame.grid(row=0, rowspan=2, column=0, columnspan=3, padx=(25, 0))
        frame.grid(row=2, column=0, columnspan=3, sticky="WE", padx=(25, 0))
        self.menu_modify_psikologi_admin_footer_frame.grid(row=3, column=0, columnspan=3, sticky="WE", padx=(25, 0))

        # header section
        self.header(self.menu_modify_psikologi_admin_header_frame)

        # container section
        self.__admin.printlist_psikologi(frame)
        self.__admin.menu_modify_test_psikologi(self.menu_modify_psikologi_admin_header_frame,
                                                frame,
                                                self.menu_modify_psikologi_admin_footer_frame)

        # footer section
        self.date_time_label = Label(self.menu_modify_psikologi_admin_footer_frame, text="", fg="Red",
                                     font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_modify_psikologi_admin_footer_frame, text="Menu Sebelumnya",
                                             command=lambda: [
                                                 self.remove_current_frame(
                                                     self.menu_modify_psikologi_admin_header_frame),
                                                 self.destroy_current_frame(frame),
                                                 self.remove_current_frame(
                                                     self.menu_modify_psikologi_admin_footer_frame),
                                                 self.menu_panel_psikologi_admin(
                                                     LabelFrame(self.root, bd=0, highlightthickness=0))
                                             ])
        self.menu_utama_button = Button(self.menu_modify_psikologi_admin_footer_frame, text="Logout", state=ACTIVE,
                                        command=lambda: [
                                            self.remove_current_frame(self.menu_modify_psikologi_admin_header_frame),
                                            self.destroy_current_frame(frame),
                                            self.remove_current_frame(self.menu_modify_psikologi_admin_footer_frame),
                                            self.menu_utama()
                                        ])
        self.footer(self.menu_modify_psikologi_admin_footer_frame)

    def menu_input_modify_psikologi_admin(self):
        self.program_geometry = "600x650+450+50"
        self.root.geometry(self.program_geometry)

        self.menu_input_modify_psikologi_admin_header_frame.grid(row=0, rowspan=2, column=0, columnspan=3, padx=(25, 0))
        self.menu_input_modify_psikologi_admin_frame.grid(row=2, column=0, columnspan=3, sticky="WE", padx=(25, 0))
        self.menu_input_modify_psikologi_admin_footer_frame.grid(row=3, column=0, columnspan=3, sticky="WE",
                                                                 padx=(25, 0))

        # header section
        self.header(self.menu_input_modify_psikologi_admin_header_frame)

        # container section
        self.__admin.input_modify_psikologi(self.menu_input_modify_psikologi_admin_header_frame,
                                            self.menu_input_modify_psikologi_admin_frame,
                                            self.menu_input_modify_psikologi_admin_footer_frame)

        # footer section
        self.date_time_label = Label(self.menu_input_modify_psikologi_admin_footer_frame, text="", fg="Red",
                                     font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_input_modify_psikologi_admin_footer_frame,
                                             text="Menu Sebelumnya",
                                             command=lambda: [
                                                 self.remove_current_frame(
                                                     self.menu_input_modify_psikologi_admin_header_frame),
                                                 self.remove_current_frame(
                                                     self.menu_input_modify_psikologi_admin_frame),
                                                 self.remove_current_frame(
                                                     self.menu_input_modify_psikologi_admin_footer_frame),
                                                 self.menu_modify_psikologi_admin(
                                                     LabelFrame(self.root, bd=0, highlightthickness=0))
                                             ])
        self.menu_utama_button = Button(self.menu_input_modify_psikologi_admin_footer_frame, text="Logout",
                                        state=ACTIVE,
                                        command=lambda: [
                                            self.remove_current_frame(
                                                self.menu_input_modify_psikologi_admin_header_frame),
                                            self.remove_current_frame(self.menu_input_modify_psikologi_admin_frame),
                                            self.remove_current_frame(
                                                self.menu_input_modify_psikologi_admin_footer_frame),
                                            self.menu_utama()
                                        ])
        self.footer(self.menu_input_modify_psikologi_admin_footer_frame)

    def menu_input_modify_akhir_psikologi_admin(self):
        self.program_geometry = "670x350+430+200"
        self.root.geometry(self.program_geometry)

        self.menu_input_modify_akhir_psikologi_admin_header_frame.grid(row=0, rowspan=2, column=0, columnspan=3,
                                                                       sticky="WE", padx=(25, 0))
        self.menu_input_modify_akhir_psikologi_admin_frame.grid(row=2, column=0, columnspan=3, sticky="WE",
                                                                padx=(25, 0))
        self.menu_input_modify_akhir_psikologi_admin_footer_frame.grid(row=3, column=0, columnspan=3, sticky="WE",
                                                                       padx=(25, 0))

        # header section
        self.header(self.menu_input_modify_akhir_psikologi_admin_header_frame)

        # container section
        sukses_image = Label(self.menu_input_modify_akhir_psikologi_admin_frame, image=self.__sukses_image)
        sukses_image.grid(row=0, rowspan=2, column=0, columnspan=3, pady=(10, 10))

        Label(self.menu_input_modify_akhir_psikologi_admin_frame,
              text="Sukses mengubah soal psikologi, silahkan kembali ke menu admin atau logout",
              font=("Helvetica", 10, "bold")).grid(row=2, column=0, columnspan=3, pady=(10, 10))

        # footer section
        self.date_time_label = Label(self.menu_input_modify_akhir_psikologi_admin_footer_frame, text="", fg="Red",
                                     font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_input_modify_akhir_psikologi_admin_footer_frame,
                                             text="Menu Admin",
                                             command=lambda: [
                                                 self.remove_current_frame(
                                                     self.menu_input_modify_akhir_psikologi_admin_header_frame),
                                                 self.remove_current_frame(
                                                     self.menu_input_modify_akhir_psikologi_admin_frame),
                                                 self.remove_current_frame(
                                                     self.menu_input_modify_akhir_psikologi_admin_footer_frame),
                                                 self.menu_utama_admin()
                                             ])
        self.menu_utama_button = Button(self.menu_input_modify_akhir_psikologi_admin_footer_frame, text="Logout",
                                        state=ACTIVE,
                                        command=lambda: [
                                            self.remove_current_frame(
                                                self.menu_input_modify_akhir_psikologi_admin_header_frame),
                                            self.remove_current_frame(
                                                self.menu_input_modify_akhir_psikologi_admin_frame),
                                            self.remove_current_frame(
                                                self.menu_input_modify_akhir_psikologi_admin_footer_frame),
                                            self.menu_utama()
                                        ])
        self.footer(self.menu_input_modify_akhir_psikologi_admin_footer_frame)

    def menu_delete_psikologi_admin(self, frame):
        self.program_geometry = "1240x450+140+150"
        self.root.geometry(self.program_geometry)

        self.menu_delete_psikologi_admin_header_frame.grid(row=0, rowspan=2, column=0, columnspan=3, padx=(25, 0))
        frame.grid(row=2, column=0, columnspan=3, sticky="WE", padx=(25, 0))
        self.menu_delete_psikologi_admin_footer_frame.grid(row=3, column=0, columnspan=3, sticky="WE", padx=(25, 0))

        # header section
        self.header(self.menu_delete_psikologi_admin_header_frame)

        # container section
        self.__admin.printlist_psikologi(frame)
        self.__admin.menu_delete_test_psikologi(self.menu_delete_psikologi_admin_header_frame,
                                                frame,
                                                self.menu_delete_psikologi_admin_footer_frame)

        # footer section
        self.date_time_label = Label(self.menu_delete_psikologi_admin_footer_frame, text="", fg="Red",
                                     font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_delete_psikologi_admin_footer_frame, text="Menu Sebelumnya",
                                             command=lambda: [
                                                 self.remove_current_frame(
                                                     self.menu_delete_psikologi_admin_header_frame),
                                                 self.destroy_current_frame(frame),
                                                 self.remove_current_frame(
                                                     self.menu_delete_psikologi_admin_footer_frame),
                                                 self.menu_panel_psikologi_admin(
                                                     LabelFrame(self.root, bd=0, highlightthickness=0))
                                             ])
        self.menu_utama_button = Button(self.menu_delete_psikologi_admin_footer_frame, text="Logout", state=ACTIVE,
                                        command=lambda: [
                                            self.remove_current_frame(self.menu_delete_psikologi_admin_header_frame),
                                            self.destroy_current_frame(frame),
                                            self.remove_current_frame(self.menu_delete_psikologi_admin_footer_frame),
                                            self.menu_utama()
                                        ])
        self.footer(self.menu_delete_psikologi_admin_footer_frame)

    def menu_delete_akhir_psikologi_admin(self):

        self.program_geometry = "670x350+430+200"
        self.root.geometry(self.program_geometry)

        self.menu_delete_akhir_psikologi_admin_header_frame.grid(row=0, rowspan=2, column=0, columnspan=3,
                                                                 sticky="WE", padx=(25, 0))
        self.menu_delete_akhir_psikologi_admin_frame.grid(row=2, column=0, columnspan=3, sticky="WE", padx=(25, 0))
        self.menu_delete_akhir_psikologi_admin_footer_frame.grid(row=3, column=0, columnspan=3, sticky="WE",
                                                                 padx=(25, 0))

        # header section
        self.header(self.menu_delete_akhir_psikologi_admin_header_frame)

        # container section
        sukses_image = Label(self.menu_delete_akhir_psikologi_admin_frame, image=self.__sukses_image)
        sukses_image.grid(row=0, rowspan=2, column=0, columnspan=3, pady=(10, 10))

        Label(self.menu_delete_akhir_psikologi_admin_frame,
              text="Sukses menghapus soal psikologi, silahkan kembali ke menu admin atau logout",
              font=("Helvetica", 10, "bold")).grid(row=2, column=0, columnspan=3, pady=(10, 10))

        # footer section
        self.date_time_label = Label(self.menu_delete_akhir_psikologi_admin_footer_frame, text="", fg="Red",
                                     font=("Helvetica", 10))
        self.menu_sebelumnya_button = Button(self.menu_delete_akhir_psikologi_admin_footer_frame, text="Menu Admin",
                                             command=lambda: [
                                                 self.remove_current_frame(
                                                     self.menu_delete_akhir_psikologi_admin_header_frame),
                                                 self.remove_current_frame(
                                                     self.menu_delete_akhir_psikologi_admin_frame),
                                                 self.remove_current_frame(
                                                     self.menu_delete_akhir_psikologi_admin_footer_frame),
                                                 self.menu_utama_admin()
                                             ])
        self.menu_utama_button = Button(self.menu_delete_akhir_psikologi_admin_footer_frame, text="Logout",
                                        state=ACTIVE,
                                        command=lambda: [
                                            self.remove_current_frame(
                                                self.menu_delete_akhir_psikologi_admin_header_frame),
                                            self.remove_current_frame(self.menu_delete_akhir_psikologi_admin_frame),
                                            self.remove_current_frame(
                                                self.menu_delete_akhir_psikologi_admin_footer_frame),
                                            self.menu_utama()
                                        ])
        self.footer(self.menu_delete_akhir_psikologi_admin_footer_frame)

    def keep_program_alive(self):
        self.root.mainloop()


# menu utama
window = Window()
window.menu_utama()
window.keep_program_alive()
