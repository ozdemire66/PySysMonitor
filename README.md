# !_! PySysMonitor !_!

**PySysMonitor**, Python ile geliştirilmiş terminal tabanlı bir sistem monitörüdür.

CPU, GPU, RAM, disk, ağ, pil, anakart/BIOS, sistem bilgileri ve çalışan işlemleri tek bir terminal arayüzünden görüntülemek için geliştirilmektedir.

## ✨ Özellikler

- CPU kullanımını görüntüleme
- GPU bilgilerini görüntüleme
- Canlı RAM monitörü
- Disk kullanımını görüntüleme
- Ağ ve internet bilgileri
- Pil durumu ve şarj bilgisi
- Anakart ve BIOS bilgileri
- Sistem bilgileri
- Sistem çalışma süresi
- İşlem yöneticisi
- Yön tuşları ile menü kontrolü
- Enter ile menülere giriş
- Q / Esc ile geri dönme
- Logo boyutu ayarı
- Windows ve Linux desteği

## 🖥️ Görünüm

```text
              !_!
           PYSMONITOR

      ===== ANA MENU =====

    > RAM
      CPU / GPU
      Depolama
      Anakart / BIOS
      Sistem
      Ag Bilgisi
      Pil Bilgisi
      Islem Yoneticisi
      Ayarlar
      Cikis
```

## 📦 Gereksinimler

- Python 3.10 veya üzeri
- `psutil`
- Curses destekli bir terminal

## 🚀 Kurulum

### Linux

Projeyi indir:

```bash
git clone https://github.com/KULLANICI_ADI/PySysMonitor.git
cd PySysMonitor
```

Gerekli Python paketini yükle:

```bash
python -m pip install psutil
```

Sisteminde `python3` kullanılıyorsa:

```bash
python3 -m pip install psutil
```

CachyOS / Arch Linux üzerinde GPU bilgisi için `lspci` eksikse:

```bash
sudo pacman -S pciutils
```

Programı çalıştır:

```bash
python "Version 1.3.py"
```

veya:

```bash
python3 "Version 1.3.py"
```

### Windows

Python'u kontrol et:

```powershell
py --version
```

Gerekli paketi yükle:

```powershell
py -m pip install psutil
```

Programı çalıştır:

```powershell
py "Version 1.3.py"
```

Alternatif olarak:

```powershell
python "Version 1.3.py"
```

## 🎮 Kontroller

| Tuş | İşlev |
|---|---|
| ↑ | Yukarı |
| ↓ | Aşağı |
| Enter | Seç / Gir |
| Q | Geri |
| Esc | Geri |

İşlem yöneticisinde:

| Tuş | İşlev |
|---|---|
| ↑ | Önceki işlem |
| ↓ | Sonraki işlem |
| Q | Geri |
| Esc | Geri |

## 🪧 Logo

PySysMonitor'un kendine ait terminal logosu:

```text
!_! PYSMONITOR !_!
```

Logo boyutu **Ayarlar** bölümünden değiştirilebilir:

- Büyük
- Orta
- Küçük
- Yok

## 🧠 RAM Monitörü

RAM ekranında toplam RAM, kullanılan RAM, kullanılabilir RAM ve kullanım yüzdesi gösterilir.

Linux sistemlerinde RAM hesabı `/proc/meminfo` üzerinden yapılır ve ekran canlı olarak güncellenir.

## ⚡ CPU / GPU

CPU bölümünde CPU kullanım yüzdesi, fiziksel çekirdek sayısı, logical CPU sayısı ve CPU frekansı gösterilebilir.

GPU bilgisi işletim sistemine göre farklı yöntemlerle alınır.

- Windows: PowerShell / WMI
- Linux: `lspci`

## 💾 Disk Monitörü

Disk bölümünde:

- Toplam alan
- Kullanılan alan
- Boş alan
- Doluluk yüzdesi
- Kullanım çubuğu

gösterilir.

## 🌐 Ağ Bilgisi

Ağ ekranında:

- İnternet bağlantı durumu
- Yerel IP
- Download hızı
- Upload hızı
- Ağ trafiği

görüntülenebilir.

## 🔋 Pil Bilgisi

Desteklenen cihazlarda:

- Pil yüzdesi
- Şarj durumu
- Tahmini kalan süre

görüntülenebilir.

Masaüstü bilgisayarlarda pil bulunmuyorsa program bunu belirtir.

## 🖥️ Sistem Bilgisi

Sistem ekranında işletim sistemi, sürüm, mimari, bilgisayar adı, Python sürümü ve sistem çalışma süresi gösterilir.

## 🔧 Anakart / BIOS

Desteklenen sistemlerde:

- Anakart modeli
- Anakart üreticisi
- BIOS sürümü

gösterilir.

Windows ve Linux için uygun yöntem otomatik olarak seçilmeye çalışılır.

## ⚙️ İşlem Yöneticisi

İşlem yöneticisi çalışan işlemleri listeler ve CPU kullanımına göre sıralayabilir.

Gösterilen bilgiler:

- İşlem adı
- PID
- CPU kullanımı
- RAM kullanımı

## ⚙️ Ayarlar

Ayarlar bölümünde şu anda logo boyutu değiştirilebilir:

```text
===== AYARLAR =====

> Logo Boyutu
  Geri
```

## 🐧 Linux Desteği

Linux tarafında bazı sistem bilgileri sistem dosyalarından ve sistem araçlarından alınmaktadır.

Örneğin:

```text
/proc/meminfo
/sys/devices/
/sys/devices/virtual/dmi/
lspci
```

CachyOS ve Arch Linux geliştirme sırasında kullanılan sistemler arasındadır.

## 🪟 Windows Desteği

Windows tarafında sistem bilgileri için PowerShell ve Windows sistem araçları kullanılır.

Program işletim sistemini otomatik olarak algılayarak uygun yöntemi kullanmaya çalışır.

## ⚠️ Bilinen Sınırlamalar

Bazı bilgiler her bilgisayarda alınamayabilir.

- Masaüstü bilgisayarlarda pil bulunmayabilir.
- Bazı BIOS bilgileri erişilemeyebilir.
- Linux'ta GPU bilgisi için `lspci` gerekebilir.
- Bazı işlemlere erişim izni olmayabilir.
- Windows ve Linux aynı bilgileri farklı yöntemlerle sağlar.

Bu durumlarda program mümkün olduğunca hata vermek yerine bilgi göstermeye çalışır.

## 📁 Proje Yapısı

Şu anda sürümler ayrı Python dosyaları halinde tutulmaktadır:

```text
PySysMonitor/
├── Version 1.1.py
├── Version 1.2.py
├── Version 1.3.py
└── README.md
```

## 📜 Sürüm Geçmişi

### Version 1.1

PySysMonitor'un temel yapısının geliştirildiği ilk sürümlerden biridir. Terminal üzerinde sistem bilgilerini gösterme fikri ve temel menü yapısı oluşturulmaya başlandı.

### Version 1.2

Version 1.2 ile proje daha kapsamlı bir sistem monitörüne dönüştürüldü.

Öne çıkan geliştirmeler:

- Yön tuşlarıyla menü sistemi
- Enter ile menülere giriş
- CPU / GPU bilgileri
- RAM bilgileri
- Disk bilgileri
- Ağ bilgileri
- Sistem bilgileri
- Anakart / BIOS bilgileri
- Pil bilgileri
- İşlem yöneticisi
- Windows / Linux için farklı donanım algılama yöntemleri
- Logo sistemi
- Ayarlar bölümü

### Version 1.3

Version 1.3 ile mevcut monitörlerin ve terminal arayüzünün geliştirilmesine odaklanıldı.

Öne çıkan geliştirmeler:

- RAM monitörü geliştirildi
- RAM kullanım hesabı iyileştirildi
- CPU monitörü geliştirildi
- Disk monitörü geliştirildi
- Ağ monitörü geliştirildi
- Pil ekranı geliştirildi
- İşlem yöneticisi geliştirildi
- Linux / Windows donanım algılama geliştirildi
- Logo boyutu seçenekleri eklendi
- Küçük terminal ekranlarında taşma sorunları azaltıldı
- Menü sistemi geliştirildi

## 🛠️ Geliştirme

PySysMonitor geliştirme aşamasındaki bir projedir.

Uzun vadede projenin daha kararlı, daha hızlı, daha modüler ve daha fazla işletim sistemiyle uyumlu hale getirilmesi hedeflenmektedir.

## 📄 Lisans

Bu proje şu anda geliştirme aşamasındadır. Lisans bilgisi ilerleyen sürümlerde belirlenecektir.

## 👨‍💻 PySysMonitor

```text
          !_!
       PYSMONITOR

   Terminal System Monitor

       Version 1.3
       Python
 Linux / Windows
```

**PySysMonitor — System monitoring from the terminal.**
