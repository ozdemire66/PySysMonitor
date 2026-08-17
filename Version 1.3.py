import curses
import psutil
import platform
import socket
import subprocess
import time
import os

logo_boyutu = "Orta"


# =========================
# YARDIMCI
# =========================

def yaz(stdscr, y, x, text):
    try:
        h, w = stdscr.getmaxyx()
        if 0 <= y < h and 0 <= x < w:
            stdscr.addstr(y, x, str(text)[:w - x - 1])
    except curses.error:
        pass


def baslik(stdscr, text):
    yaz(stdscr, 1, 2, f"===== {text} =====")


def geri(stdscr):
    yaz(stdscr, curses.LINES - 2, 2, "Q = Geri")
    stdscr.refresh()
    stdscr.nodelay(False)
    while True:
        tus = stdscr.getch()
        if tus != -1:
            break


# =========================
# LOGOLAR
# =========================

LOGO_BUYUK = [
    "██████╗ ██╗   ██╗███████╗███╗   ███╗",
    "██╔══██╗╚██╗ ██╔╝██╔════╝████╗ ████║",
    "██████╔╝ ╚████╔╝ ███████╗██╔████╔██║",
    "██╔═══╝   ╚██╔╝  ╚════██║██║╚██╔╝██║",
    "██║        ██║   ███████║██║ ╚═╝ ██║",
    "╚═╝        ╚═╝   ╚══════╝╚═╝     ╚═╝",
    "",
    "                !_!",
    "             PYSMONITOR"
]

LOGO_ORTA = [
    "██████╗ ██╗   ██╗███████╗",
    "██╔══██╗╚██╗ ██╔╝██╔════╝",
    "██████╔╝ ╚████╔╝ ███████╗",
    "██╔═══╝   ╚██╔╝  ╚════██║",
    "██║        ██║   ███████║",
    "╚═╝        ╚═╝   ╚══════╝",
    "",
    "          !_!",
    "       PYSMONITOR"
]

LOGO_KUCUK = ["!_! PYSMONITOR !_!"]


def logo_getir():
    if logo_boyutu == "Buyuk":
        return LOGO_BUYUK
    if logo_boyutu == "Kucuk":
        return LOGO_KUCUK
    if logo_boyutu == "Yok":
        return []
    return LOGO_ORTA


# =========================
# RAM
# =========================

def ram_ekrani(stdscr):
    stdscr.nodelay(True)

    while True:
        stdscr.clear()
        baslik(stdscr, "RAM MONITOR")

        try:
            if platform.system() == "Linux":
                total = 0
                available = 0

                with open("/proc/meminfo") as f:
                    for line in f:
                        if line.startswith("MemTotal:"):
                            total = int(line.split()[1])

                        elif line.startswith("MemAvailable:"):
                            available = int(line.split()[1])

                toplam = total / 1024 / 1024
                kullanilabilir = available / 1024 / 1024
                kullanilan = toplam - kullanilabilir

            else:
                ram = psutil.virtual_memory()
                toplam = ram.total / 1024**3
                kullanilabilir = ram.available / 1024**3
                kullanilan = toplam - kullanilabilir

            yuzde = (kullanilan / toplam) * 100 if toplam else 0

            yaz(stdscr, 4, 2, f"Toplam        : {toplam:.2f} GB")
            yaz(stdscr, 5, 2, f"Kullanilan    : {kullanilan:.2f} GB")
            yaz(stdscr, 6, 2, f"Kullanilabilir : {kullanilabilir:.2f} GB")
            yaz(stdscr, 7, 2, f"Kullanim      : %{yuzde:.1f}")

            bar_len = 30
            dolu = int(bar_len * yuzde / 100)
            bar = "█" * dolu + "░" * (bar_len - dolu)
            yaz(stdscr, 9, 2, f"[{bar}]")

        except Exception as e:
            yaz(stdscr, 4, 2, f"RAM hatasi: {e}")

        yaz(stdscr, 11, 2, "Q = Geri")
        stdscr.refresh()

        tus = stdscr.getch()

        if tus in (ord("q"), ord("Q"), 27):
            break

        time.sleep(1)

    stdscr.nodelay(False)


# =========================
# CPU / GPU
# =========================

def gpu_adi_al():
    try:
        if platform.system() == "Windows":
            out = subprocess.check_output(
                [
                    "powershell", "-Command",
                    "(Get-CimInstance Win32_VideoController).Name"
                ],
                text=True,
                stderr=subprocess.DEVNULL
            ).strip()

            return out.splitlines()[0] if out else "Bulunamadi"

        out = subprocess.check_output(
            ["lspci"],
            text=True,
            stderr=subprocess.DEVNULL
        )

        for line in out.splitlines():
            if any(x in line for x in (
                "VGA compatible controller",
                "3D controller",
                "Display controller"
            )):
                return line.split(": ", 1)[-1]

    except Exception:
        pass

    return "Bulunamadi"


def cpu_ekrani(stdscr):
    stdscr.nodelay(True)

    while True:
        stdscr.clear()
        baslik(stdscr, "CPU / GPU")

        cpu = psutil.cpu_percent(interval=0.2)
        fiziksel = psutil.cpu_count(logical=False)
        logical = psutil.cpu_count(logical=True)
        frekans = psutil.cpu_freq()
        gpu = gpu_adi_al()

        yaz(stdscr, 4, 2, f"CPU Kullanim : %{cpu:.1f}")
        yaz(stdscr, 5, 2, f"Cekirdek     : {fiziksel}")
        yaz(stdscr, 6, 2, f"Logical CPU  : {logical}")

        if frekans:
            yaz(stdscr, 7, 2, f"Frekans      : {frekans.current:.0f} MHz")

        yaz(stdscr, 9, 2, f"GPU          : {gpu}")
        yaz(stdscr, 11, 2, "Q = Geri")
        stdscr.refresh()

        tus = stdscr.getch()

        if tus in (ord("q"), ord("Q"), 27):
            break

        time.sleep(0.5)

    stdscr.nodelay(False)


# =========================
# DISK
# =========================

def disk_ekrani(stdscr):
    stdscr.nodelay(True)

    while True:
        stdscr.clear()
        baslik(stdscr, "DISK MONITOR")

        try:
            disk = psutil.disk_usage(os.path.abspath(os.sep))

            toplam = disk.total / 1024**3
            kullanilan = disk.used / 1024**3
            bos = disk.free / 1024**3

            yaz(stdscr, 4, 2, f"Toplam     : {toplam:.2f} GB")
            yaz(stdscr, 5, 2, f"Kullanilan : {kullanilan:.2f} GB")
            yaz(stdscr, 6, 2, f"Bos        : {bos:.2f} GB")
            yaz(stdscr, 7, 2, f"Doluluk    : %{disk.percent:.1f}")

        except Exception as e:
            yaz(stdscr, 4, 2, f"Disk hatasi: {e}")

        yaz(stdscr, 9, 2, "Q = Geri")
        stdscr.refresh()

        tus = stdscr.getch()

        if tus in (ord("q"), ord("Q"), 27):
            break

        time.sleep(1)

    stdscr.nodelay(False)


# =========================
# AG
# =========================

def ag_ekrani(stdscr):
    stdscr.nodelay(True)
    onceki = psutil.net_io_counters()

    while True:
        stdscr.clear()
        baslik(stdscr, "AG BILGISI")

        simdi = psutil.net_io_counters()

        download = (simdi.bytes_recv - onceki.bytes_recv) / 1024
        upload = (simdi.bytes_sent - onceki.bytes_sent) / 1024
        onceki = simdi

        try:
            ip = socket.gethostbyname(socket.gethostname())
            durum = "Bagli"
        except Exception:
            ip = "Yok"
            durum = "Bagli degil"

        yaz(stdscr, 4, 2, f"Internet : {durum}")
        yaz(stdscr, 5, 2, f"IP       : {ip}")
        yaz(stdscr, 6, 2, f"Download : {download:.2f} KB/s")
        yaz(stdscr, 7, 2, f"Upload   : {upload:.2f} KB/s")
        yaz(stdscr, 9, 2, "Q = Geri")

        stdscr.refresh()

        tus = stdscr.getch()

        if tus in (ord("q"), ord("Q"), 27):
            break

        time.sleep(1)

    stdscr.nodelay(False)


# =========================
# PIL
# =========================

def pil_bilgisi(stdscr):
    stdscr.nodelay(True)

    while True:
        stdscr.clear()
        baslik(stdscr, "PIL BILGISI")

        pil = psutil.sensors_battery()

        if pil is None:
            yaz(stdscr, 4, 2, "Pil bulunamadi.")
        else:
            yaz(stdscr, 4, 2, f"Yuzde : %{pil.percent:.0f}")
            yaz(
                stdscr,
                5,
                2,
                f"Durum : {'Sarj oluyor' if pil.power_plugged else 'Sarj olmuyor'}"
            )

            if pil.secsleft > 0:
                saat = pil.secsleft // 3600
                dakika = (pil.secsleft % 3600) // 60
                yaz(
                    stdscr,
                    6,
                    2,
                    f"Kalan : {saat} saat {dakika} dk"
                )

        yaz(stdscr, 8, 2, "Q = Geri")
        stdscr.refresh()

        tus = stdscr.getch()

        if tus in (ord("q"), ord("Q"), 27):
            break

        time.sleep(1)

    stdscr.nodelay(False)


# =========================
# SISTEM
# =========================

def sistem_ekrani(stdscr):
    stdscr.clear()
    baslik(stdscr, "SISTEM BILGISI")

    yaz(stdscr, 4, 2, f"OS        : {platform.system()}")
    yaz(stdscr, 5, 2, f"Surum     : {platform.release()}")
    yaz(stdscr, 6, 2, f"Mimari    : {platform.machine()}")
    yaz(stdscr, 7, 2, f"Bilgisayar: {platform.node()}")
    yaz(stdscr, 8, 2, f"Python    : {platform.python_version()}")

    try:
        uptime = time.time() - psutil.boot_time()
        gun = int(uptime // 86400)
        saat = int((uptime % 86400) // 3600)
        dakika = int((uptime % 3600) // 60)

        yaz(stdscr, 9, 2, f"Uptime    : {gun}g {saat}s {dakika}dk")
    except Exception:
        pass

    geri(stdscr)


# =========================
# ANAKART
# =========================

def anakart_bilgisi(stdscr):
    stdscr.clear()
    baslik(stdscr, "ANAKART / BIOS")

    model = "Bulunamadi"
    uretici = "Bulunamadi"
    bios = "Bulunamadi"

    try:
        if platform.system() == "Windows":
            model = subprocess.check_output(
                [
                    "powershell", "-Command",
                    "(Get-CimInstance Win32_BaseBoard).Product"
                ],
                text=True
            ).strip()

            uretici = subprocess.check_output(
                [
                    "powershell", "-Command",
                    "(Get-CimInstance Win32_BaseBoard).Manufacturer"
                ],
                text=True
            ).strip()

            bios = subprocess.check_output(
                [
                    "powershell", "-Command",
                    "(Get-CimInstance Win32_BIOS).SMBIOSBIOSVersion"
                ],
                text=True
            ).strip()

        else:
            with open("/sys/devices/virtual/dmi/id/board_name") as f:
                model = f.read().strip()

            with open("/sys/devices/virtual/dmi/id/board_vendor") as f:
                uretici = f.read().strip()

            with open("/sys/devices/virtual/dmi/id/bios_version") as f:
                bios = f.read().strip()

    except Exception:
        pass

    yaz(stdscr, 4, 2, f"Model   : {model}")
    yaz(stdscr, 5, 2, f"Uretici : {uretici}")
    yaz(stdscr, 6, 2, f"BIOS    : {bios}")

    geri(stdscr)


# =========================
# ISLEM YONETICISI
# =========================

def islem_yoneticisi(stdscr):
    stdscr.keypad(True)
    secim = 0

    while True:
        islemler = []

        for proc in psutil.process_iter(
            ["pid", "name", "cpu_percent", "memory_percent"]
        ):
            try:
                p = proc.info
                islemler.append(
                    (
                        p["name"] or "Bilinmiyor",
                        p["pid"],
                        p["cpu_percent"] or 0,
                        p["memory_percent"] or 0
                    )
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        islemler.sort(key=lambda x: x[2], reverse=True)

        limit = min(
            len(islemler),
            max(1, curses.LINES - 5)
        )

        if limit:
            secim %= limit

        stdscr.clear()
        baslik(stdscr, "ISLEM YONETICISI")

        for i in range(limit):
            isim, pid, cpu, ram = islemler[i]
            isaret = "> " if i == secim else "  "

            yaz(
                stdscr,
                3 + i,
                1,
                f"{isaret}{isim[:18]:18} "
                f"PID:{pid:<7} "
                f"CPU:%{cpu:<5.1f} "
                f"RAM:%{ram:.1f}"
            )

        yaz(stdscr, curses.LINES - 2, 2, "↑ ↓ Sec | Q = Geri")
        stdscr.refresh()

        tus = stdscr.getch()

        if tus == curses.KEY_UP and limit:
            secim = (secim - 1) % limit

        elif tus == curses.KEY_DOWN and limit:
            secim = (secim + 1) % limit

        elif tus in (ord("q"), ord("Q"), 27):
            break

        time.sleep(0.3)


# =========================
# LOGO AYARLARI
# =========================

def logo_sec(stdscr):
    global logo_boyutu

    secenekler = ["Buyuk", "Orta", "Kucuk", "Yok"]
    secim = secenekler.index(logo_boyutu)

    while True:
        stdscr.clear()
        baslik(stdscr, "LOGO BOYUTU")

        for i, secenek in enumerate(secenekler):
            isaret = "> " if i == secim else "  "
            yaz(stdscr, 4 + i, 2, isaret + secenek)

        yaz(stdscr, 10, 2, "↑ ↓ Sec | Enter Sec | Q Geri")
        stdscr.refresh()

        tus = stdscr.getch()

        if tus == curses.KEY_UP:
            secim = (secim - 1) % len(secenekler)

        elif tus == curses.KEY_DOWN:
            secim = (secim + 1) % len(secenekler)

        elif tus in (curses.KEY_ENTER, 10, 13):
            logo_boyutu = secenekler[secim]
            break

        elif tus in (ord("q"), ord("Q"), 27):
            break


# =========================
# AYARLAR
# =========================

def ayarlar(stdscr):
    secim = 0

    while True:
        stdscr.clear()
        baslik(stdscr, "AYARLAR")

        yaz(stdscr, 4, 2, f"Logo: {logo_boyutu}")
        yaz(stdscr, 7, 2, ("> " if secim == 0 else "  ") + "Logo Boyutu")
        yaz(stdscr, 8, 2, ("> " if secim == 1 else "  ") + "Geri")

        stdscr.refresh()
        tus = stdscr.getch()

        if tus == curses.KEY_UP:
            secim = (secim - 1) % 2

        elif tus == curses.KEY_DOWN:
            secim = (secim + 1) % 2

        elif tus in (curses.KEY_ENTER, 10, 13):
            if secim == 0:
                logo_sec(stdscr)
            else:
                break

        elif tus in (ord("q"), ord("Q"), 27):
            break


# =========================
# ANA MENU
# =========================

def ekran(stdscr):
    global logo_boyutu

    curses.curs_set(0)
    stdscr.keypad(True)

    secim = 0

    menuler = [
        "RAM",
        "CPU / GPU",
        "Depolama",
        "Anakart / BIOS",
        "Sistem",
        "Ag Bilgisi",
        "Pil Bilgisi",
        "Islem Yoneticisi",
        "Ayarlar",
        "Cikis"
    ]

    while True:
        stdscr.clear()

        h, w = stdscr.getmaxyx()

        # LOGO
        logo = logo_getir()

        if h < 20:
            logo = LOGO_KUCUK
        elif h < 26 and logo_boyutu == "Buyuk":
            logo = LOGO_ORTA

        # Logoyu yaz
        for i, satir in enumerate(logo):
            yaz(stdscr, i + 1, 2, satir)

        # Menü başlangıcı
        menu_baslangic = len(logo) + 3

        yaz(
            stdscr,
            menu_baslangic,
            2,
            "===== ANA MENU ====="
        )

        # Kaç satır sığıyor?
        ilk_menu = menu_baslangic + 2
        max_menu = max(1, h - ilk_menu - 2)

        # Listeyi kaydır
        kaydir = 0

        if secim >= max_menu:
            kaydir = secim - max_menu + 1

        for i in range(max_menu):
            index = i + kaydir

            if index >= len(menuler):
                break

            if index == secim:
                yazi = "> " + menuler[index]
            else:
                yazi = "  " + menuler[index]

            yaz(
                stdscr,
                ilk_menu + i,
                2,
                yazi
            )

        yaz(
            stdscr,
            h - 1,
            2,
            "Yukari/Asagi = Sec | Enter = Gir"
        )

        stdscr.refresh()

        tus = stdscr.getch()

        if tus == curses.KEY_UP:
            secim -= 1

            if secim < 0:
                secim = len(menuler) - 1

        elif tus == curses.KEY_DOWN:
            secim += 1

            if secim >= len(menuler):
                secim = 0

        elif tus in (curses.KEY_ENTER, 10, 13):

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
                pil_bilgisi(stdscr)

            elif secim == 7:
                islem_yoneticisi(stdscr)

            elif secim == 8:
                ayarlar(stdscr)

            elif secim == 9:
                break


# =========================
# BASLAT
# =========================

if __name__ == "__main__":
    curses.wrapper(ekran)
