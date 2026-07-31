import socket
import curses
import psutil
import time
import platform
import subprocess
import getpass

# AĞ BİLGİSİ
def ag_ekrani(stdscr):
    stdscr.timeout(100)

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

# SISTEM BILGISI
def sistem_ekrani(stdscr):
    stdscr.timeout(100)

    windows = platform.platform()
    bilgisayar = platform.node()
    kullanici = getpass.getuser()

    while True:
        stdscr.clear()

        stdscr.addstr(2, 2, "===== SISTEM BILGISI =====")
        stdscr.addstr(4, 2, f"Windows: {windows[:45]}")
        stdscr.addstr(5, 2, f"Bilgisayar: {bilgisayar[:45]}")
        stdscr.addstr(6, 2, f"Kullanici: {kullanici[:45]}")

        stdscr.addstr(8, 2, "0 = Geri")

        stdscr.refresh()

        tus = stdscr.getch()

        if tus == ord("0"):
            break

# ANAKART BILGISI
def anakart_bilgisi(stdscr):
    stdscr.timeout(100)

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
    stdscr.timeout(100)

    while True:
        stdscr.clear()

        ram = psutil.virtual_memory()

        stdscr.addstr(2, 2, "===== RAM EKRANI =====")
        stdscr.addstr(4, 2, f"Toplam RAM: {ram.total / (1024**3):.2f} GB")
        stdscr.addstr(5, 2, f"Kullanilan: {ram.used / (1024**3):.2f} GB")
        stdscr.addstr(6, 2, f"Kullanim: %{ram.percent}")

        stdscr.addstr(8, 2, "0 = Geri")

        stdscr.refresh()

        tus = stdscr.getch()

        if tus == ord("0"):
            break

# CPU + GPU
def cpu_ekrani(stdscr):
    stdscr.timeout(100)

    cpu_adi = platform.processor()

    if cpu_adi == "":
        cpu_adi = "Bulunamadi"

    cekirdek = psutil.cpu_count()

    gpu = gpu_adi_al()

    while True:
        stdscr.clear()

        cpu = psutil.cpu_percent(interval=0.5)

        stdscr.addstr(2, 2, "===== CPU EKRANI =====")

        stdscr.addstr(4, 2, f"CPU: {cpu_adi[:45]}")
        stdscr.addstr(5, 2, f"Kullanim: %{cpu}")
        stdscr.addstr(6, 2, f"Cekirdek: {cekirdek}")

        stdscr.addstr(8, 2, "===== GPU =====")
        stdscr.addstr(9, 2, f"Ekran Karti: {gpu[:45]}")

        stdscr.addstr(11, 2, "0 = Geri")

        stdscr.refresh()

        tus = stdscr.getch()

        if tus == ord("0"):
            break

# DISK
def disk_ekrani(stdscr):
    stdscr.timeout(100)

    while True:
        stdscr.clear()

        disk = psutil.disk_usage("/")

        stdscr.addstr(2, 2, "===== DISK EKRANI =====")

        stdscr.addstr(4, 2, f"Toplam: {disk.total / (1024**3):.2f} GB")
        stdscr.addstr(5, 2, f"Kullanilan: {disk.used / (1024**3):.2f} GB")
        stdscr.addstr(6, 2, f"Bos: {disk.free / (1024**3):.2f} GB")
        stdscr.addstr(7, 2, f"Doluluk: %{disk.percent}")

        stdscr.addstr(9, 2, "0 = Geri")

        stdscr.refresh()

        tus = stdscr.getch()

        if tus == ord("0"):
            break

# ANA MENU
def ekran(stdscr):
    curses.curs_set(0)
    stdscr.timeout(100)

    secim = 0

    menuler = [
        "RAM",
        "CPU / GPU",
        "DISK",
        "ANAKART",
        "SISTEM",
        "AG",
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

        # Yukari
        if tus == curses.KEY_UP:
            secim -= 1

            if secim < 0:
                secim = len(menuler) - 1

        # Asagi
        elif tus == curses.KEY_DOWN:
            secim += 1

            if secim >= len(menuler):
                secim = 0

        # Enter
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
                break

# BASLAT
if __name__ == "__main__":
    curses.wrapper(ekran)
