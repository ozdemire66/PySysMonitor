import socket
import curses
import psutil
import time
import platform
import subprocess
import getpass

def ag_ekrani(stdscr):
    stdscr.nodelay(True)

    eski = psutil.net_io_counters()

    while True:
        stdscr.clear()

        try:
            ip = socket.gethostbyname(socket.gethostname())
            bagli = "Bagli"

        except:
            ip = "Yok"
            bagli = "Bagli degil"


        simdi = psutil.net_io_counters()

        download = (simdi.bytes_recv - eski.bytes_recv) / 1024
        upload = (simdi.bytes_sent - eski.bytes_sent) / 1024

        eski = simdi


        stdscr.addstr(2, 2, "===== AG BILGISI =====")
        stdscr.addstr(4, 2, f"Internet: {bagli}")
        stdscr.addstr(5, 2, f"IP: {ip}")
        stdscr.addstr(6, 2, f"Download: {download:.2f} KB/s")
        stdscr.addstr(7, 2, f"Upload: {upload:.2f} KB/s")

        stdscr.addstr(9, 2, "0 = Geri")

        stdscr.refresh()

        tus = stdscr.getch()

        if tus == ord("0"):
            break

        time.sleep(1)

def sistem_ekrani(stdscr):
    stdscr.nodelay(True)

    while True:
        stdscr.clear()

        windows = platform.platform()
        bilgisayar = platform.node()
        kullanici = getpass.getuser()

        stdscr.addstr(2, 2, "===== SISTEM BILGISI =====")
        stdscr.addstr(4, 2, f"Windows: {windows[:45]}")
        stdscr.addstr(5, 2, f"Bilgisayar Adi: {bilgisayar[:45]}")
        stdscr.addstr(6, 2, f"Kullanici: {kullanici[:45]}")

        stdscr.addstr(8, 2, "0 = Geri")

        stdscr.refresh()

        tus = stdscr.getch()

        if tus == ord("0"):
            break

        time.sleep(0.5)

def anakart_bilgisi(stdscr):
    stdscr.nodelay(True)

    try:
        model = subprocess.check_output(
            'powershell "Get-CimInstance Win32_BaseBoard | Select-Object -ExpandProperty Product"',
            shell=True
        ).decode(errors="ignore").strip()

        uretici = subprocess.check_output(
            'powershell "Get-CimInstance Win32_BaseBoard | Select-Object -ExpandProperty Manufacturer"',
            shell=True
        ).decode(errors="ignore").strip()

        bios = subprocess.check_output(
            'powershell "Get-CimInstance Win32_BIOS | Select-Object -ExpandProperty SMBIOSBIOSVersion"',
            shell=True
        ).decode(errors="ignore").strip()

    except:
        model = "Bulunamadi"
        uretici = "Bulunamadi"
        bios = "Bulunamadi"


    while True:
        stdscr.clear()

        stdscr.addstr(2, 2, "===== ANAKART =====")
        stdscr.addstr(4, 2, f"Model: {model[:45]}")
        stdscr.addstr(5, 2, f"Uretici: {uretici[:45]}")
        stdscr.addstr(6, 2, f"BIOS: {bios[:45]}")

        stdscr.addstr(8, 2, "0 = Geri")

        stdscr.refresh()

        tus = stdscr.getch()

        if tus == ord("0"):
            break

        time.sleep(0.5)

def gpu_adi_al():
    try:
        sonuc = subprocess.check_output(
            "wmic path win32_VideoController get name",
            shell=True
        )

        satirlar = sonuc.decode(errors="ignore").split("\n")

        for satir in satirlar:
            satir = satir.strip()
            if satir and satir.lower() != "name":
                return satir

        return "Bulunamadi"

    except:
        return "Bulunamadi"


def ram_ekrani(stdscr):
    stdscr.nodelay(True)

    while True:
        stdscr.clear()

        ram = psutil.virtual_memory()

        stdscr.addstr(2, 2, "===== RAM Ekrani =====")
        stdscr.addstr(4, 2, f"Toplam RAM: {ram.total / (1024**3):.2f} GB")
        stdscr.addstr(5, 2, f"Kullanilan: {ram.used / (1024**3):.2f} GB")
        stdscr.addstr(6, 2, f"RAM: %{ram.percent}")
        stdscr.addstr(8, 2, "0 = Geri")

        stdscr.refresh()

        tus = stdscr.getch()

        if tus == ord("0"):
            break

        time.sleep(0.5)


def cpu_ekrani(stdscr):
    stdscr.nodelay(True)

    while True:
        stdscr.clear()

        cpu = psutil.cpu_percent()
        cpu_cekirdek = psutil.cpu_count()

        cpu_adi = platform.processor()
        if cpu_adi == "":
            cpu_adi = "Bulunamadi"

        gpu = gpu_adi_al()

        stdscr.addstr(2, 2, "===== CPU Ekrani =====")
        stdscr.addstr(4, 2, f"CPU: {cpu_adi}")
        stdscr.addstr(5, 2, f"Kullanim: %{cpu}")
        stdscr.addstr(6, 2, f"Cekirdek: {cpu_cekirdek}")

        stdscr.addstr(8, 2, "===== GPU =====")
        stdscr.addstr(9, 2, f"Ekran Karti: {gpu[:45]}")

        stdscr.addstr(11, 2, "0 = Geri")

        stdscr.refresh()

        tus = stdscr.getch()

        if tus == ord("0"):
            break

        time.sleep(0.5)


def disk_ekrani(stdscr):
    stdscr.nodelay(True)

    while True:
        stdscr.clear()

        disk = psutil.disk_usage("/")

        stdscr.addstr(2, 2, "===== DISK Ekrani =====")
        stdscr.addstr(4, 2, f"Toplam: {disk.total / (1024**3):.2f} GB")
        stdscr.addstr(5, 2, f"Kullanilan: {disk.used / (1024**3):.2f} GB")
        stdscr.addstr(6, 2, f"Bos: {disk.free / (1024**3):.2f} GB")
        stdscr.addstr(7, 2, f"Doluluk: %{disk.percent}")

        stdscr.addstr(9, 2, "0 = Geri")

        stdscr.refresh()

        tus = stdscr.getch()

        if tus == ord("0"):
            break

        time.sleep(0.5)


def ekran(stdscr):
    curses.curs_set(0)

    while True:
        stdscr.clear()

        stdscr.addstr(2, 2, "===== MERKEZ =====")
        stdscr.addstr(4, 2, "1 - RAM")
        stdscr.addstr(5, 2, "2 - CPU ")
        stdscr.addstr(6, 2, "3 - DISK")
        stdscr.addstr(7, 2, "4 - ANAKART")
        stdscr.addstr(8, 2, "5 - SISTEM")
        stdscr.addstr(9, 2, "6 - AG")
        stdscr.addstr(10, 2, "0 - Cikis")

        stdscr.refresh()

        tus = stdscr.getch()

        if tus == ord("1"):
            ram_ekrani(stdscr)

        elif tus == ord("2"):
            cpu_ekrani(stdscr)

        elif tus == ord("3"):
            disk_ekrani(stdscr)

        elif tus == ord("4"):
            anakart_bilgisi(stdscr)
        
        elif tus == ord("5"):
            sistem_ekrani(stdscr)

        elif tus == ord("6"):
            ag_ekrani(stdscr)

        elif tus == ord("0"):
            break

        else:
            stdscr.addstr(9, 2, "Gecersiz secim! Lutfen tekrar deneyin.")
            stdscr.refresh()
            time.sleep(1)


curses.wrapper(ekran)