import socket
import curses
import psutil
import time
import platform
import subprocess
import getpass


# AĞ BİLGİSİ
def ag_ekrani(stdscr):
    stdscr.clear()

    eski = psutil.net_io_counters()

    try:
        ip = socket.gethostbyname(socket.gethostname())
        bagli = "Bagli"
    except:
        ip = "Yok"
        bagli = "Bagli degil"

    time.sleep(1)

    yeni = psutil.net_io_counters()

    download = (yeni.bytes_recv - eski.bytes_recv) / 1024
    upload = (yeni.bytes_sent - eski.bytes_sent) / 1024

    stdscr.addstr(2, 2, "===== AG BILGISI =====")
    stdscr.addstr(4, 2, f"Internet: {bagli}")
    stdscr.addstr(5, 2, f"IP: {ip}")
    stdscr.addstr(6, 2, f"Download: {download:.2f} KB/s")
    stdscr.addstr(7, 2, f"Upload: {upload:.2f} KB/s")

    stdscr.addstr(9, 2, "Geri icin tusa bas")

    stdscr.refresh()
    stdscr.getch()

# SISTEM BILGISI
def sistem_ekrani(stdscr):
    stdscr.clear()

    windows = platform.platform()
    bilgisayar = platform.node()
    kullanici = getpass.getuser()

    stdscr.addstr(2, 2, "===== SISTEM BILGISI =====")
    stdscr.addstr(4, 2, f"Isletim sistemi: {windows[:45]}")
    stdscr.addstr(5, 2, f"Bilgisayar: {bilgisayar[:45]}")
    stdscr.addstr(6, 2, f"Kullanici: {kullanici[:45]}")

    stdscr.addstr(8, 2, "Geri icin tusa bas")

    stdscr.refresh()
    stdscr.getch()



# ANAKART BILGISI
def anakart_bilgisi(stdscr):
    stdscr.clear()

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


    stdscr.addstr(2, 2, "===== ANAKART =====")
    stdscr.addstr(4, 2, f"Model: {model[:45]}")
    stdscr.addstr(5, 2, f"Uretici: {uretici[:45]}")
    stdscr.addstr(6, 2, f"BIOS: {bios[:45]}")

    stdscr.addstr(8, 2, "Geri icin tusa bas")

    stdscr.refresh()
    stdscr.getch()



# PIL BILGISI
def Pil_Bilgisi(stdscr):
    stdscr.clear()

    pil = psutil.sensors_battery()

    stdscr.addstr(2, 2, "===== PIL BILGISI =====")

    if pil is None:
        stdscr.addstr(4, 2, "Pil bulunamadi")
    else:
        stdscr.addstr(4, 2, f"Yuzde: %{pil.percent}")

        if pil.power_plugged:
            stdscr.addstr(5, 2, "Durum: Sarj oluyor")
        else:
            stdscr.addstr(5, 2, "Durum: Sarj olmuyor")

        if pil.secsleft > 0:
            saat = pil.secsleft // 3600
            dakika = (pil.secsleft % 3600) // 60
            stdscr.addstr(6, 2, f"Kalan sure: {saat} saat {dakika} dk")
        else:
            stdscr.addstr(6, 2, "Kalan sure: Bilinmiyor")

    stdscr.addstr(8, 2, "Geri icin tusa bas")

    stdscr.refresh()
    stdscr.getch()

# GPU BILGISI
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



# RAM
def ram_ekrani(stdscr):
    stdscr.clear()

    ram = psutil.virtual_memory()

    stdscr.addstr(2, 2, "===== RAM BILGISI =====")
    stdscr.addstr(4, 2, f"Toplam RAM: {ram.total / (1024**3):.2f} GB")
    stdscr.addstr(5, 2, f"Kullanilan: {ram.used / (1024**3):.2f} GB")
    stdscr.addstr(6, 2, f"Kullanim: %{ram.percent}")

    stdscr.addstr(8, 2, "Geri icin tusa bas")

    stdscr.refresh()
    stdscr.getch()



# CPU + GPU
def cpu_ekrani(stdscr):
    stdscr.clear()

    cpu_adi = platform.processor()

    if cpu_adi == "":
        cpu_adi = "Bulunamadi"

    cekirdek = psutil.cpu_count()
    kullanim = psutil.cpu_percent(interval=1)

    gpu = gpu_adi_al()

    stdscr.addstr(2, 2, "===== CPU BILGISI =====")
    stdscr.addstr(4, 2, f"CPU: {cpu_adi[:45]}")
    stdscr.addstr(5, 2, f"Kullanim: %{kullanim}")
    stdscr.addstr(6, 2, f"Cekirdek: {cekirdek}")

    stdscr.addstr(8, 2, "===== GPU =====")
    stdscr.addstr(9, 2, f"Ekran Karti: {gpu[:45]}")

    stdscr.addstr(11, 2, "Geri icin tusa bas")

    stdscr.refresh()
    stdscr.getch()



# DISK
def disk_ekrani(stdscr):
    stdscr.clear()

    disk = psutil.disk_usage("/")

    stdscr.addstr(2, 2, "===== DISK BILGISI =====")

    stdscr.addstr(4, 2, f"Toplam: {disk.total / (1024**3):.2f} GB")
    stdscr.addstr(5, 2, f"Kullanilan: {disk.used / (1024**3):.2f} GB")
    stdscr.addstr(6, 2, f"Bos: {disk.free / (1024**3):.2f} GB")
    stdscr.addstr(7, 2, f"Doluluk: %{disk.percent}")

    stdscr.addstr(9, 2, "Geri icin tusa bas")

    stdscr.refresh()
    stdscr.getch()

# ANA MENU
def ekran(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)

    secim = 0

    menuler = [
        "RAM",
        "CPU / GPU",
        "DISK",
        "ANAKART",
        "SISTEM",
        "AG",
        "PIL BILGISI",
        "CIKIS"
    ]

    while True:
        stdscr.clear()

        stdscr.addstr(2, 2, "===== PY SYSMONITOR =====")

        for i, menu in enumerate(menuler):
            if i == secim:
                stdscr.addstr(4 + i, 2, "> " + menu)
            else:
                stdscr.addstr(4 + i, 2, "  " + menu)

        stdscr.refresh()

        tus = stdscr.getch()


        # YUKARI
        if tus == curses.KEY_UP:
            secim -= 1

            if secim < 0:
                secim = len(menuler) - 1


        # ASAGI
        elif tus == curses.KEY_DOWN:
            secim += 1

            if secim >= len(menuler):
                secim = 0


        # ENTER
        elif tus == curses.KEY_ENTER or tus == 10:

            if secim == 0:
                ram_ekrani(stdscr)

            elif secim == 1:
                cpu_ekrani(stdscr)

            elif secim == 2:
                disk_ekrani(stdscr)

            elif secim == 3:
                anakart_bilgisi(stdscr)

            elif secim == 4:
                sistem_ekrani(stdscr)

            elif secim == 5:
                ag_ekrani(stdscr)

            elif secim == 6:
                Pil_Bilgisi(stdscr)

            elif secim == 7:
                break



# BASLAT
if __name__ == "__main__":
    curses.wrapper(ekran)