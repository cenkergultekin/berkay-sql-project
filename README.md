# NIQ Desktop — Natural Intelligence Query

Doğal dil sorularını Microsoft SQL Server için optimize edilmiş SQL sorgularına dönüştüren modern masaüstü uygulaması. PyQt5 WebEngine ile geliştirilmiş, yeni nesil veritabanı etkileşim aracıdır.

## Özellikler

### Modern Tasarım
- Minimal, kullanıcı dostu arayüz
- Dashboard-first kullanım deneyimi
- Dinamik hızlı işlemler (bağlantı durumuna göre akıllı sıralama)

### AI Destekli Sorgu Oluşturma
- OpenAI GPT-4o-mini ile doğal dil işleme
- Otomatik tablo ve sütun keşfi
- AI destekli performans önerileri
- Akıllı SQL hata analizi ve çözüm önerileri

### Veri Görselleştirme
- Chart.js ile etkileşimli grafikler
- Çoklu grafik türleri (bar, line, pie, scatter)
- Responsive tasarım
- PNG/SVG formatında dışa aktarma

### Güvenlik
- Windows Credential Manager ile OS seviyesi şifreleme
- Zero Trust Architecture (şifreler asla düz metin saklanmaz)
- Güvenli oturum yönetimi
- Sorgu geçmişi güvenli saklama

## Hızlı Başlangıç

### Son Kullanıcılar İçin
1. Release kısmında yer alan NIQDesktop_Setup.exe dosyasını indirin
2. Kurulum sihirbazını çalıştırın
3. Masaüstü kısayolundan NIQ Desktop'ı başlatın
4. Veritabanı bağlantınızı kurun ve sorgularınızı oluşturun

### Geliştiriciler İçin
```bash
# Repository'yi klonlayın
git clone https://github.com/cenkergultekin/berkay-sql-project.git
cd berkay-sql-project

# Sanal ortam oluşturun
python -m venv venv
venv\Scripts\activate  # Windows

# Bağımlılıkları kurun
pip install -r requirements.txt

# Ortam değişkenlerini ayarlayın
copy env_example.txt .env
# .env dosyasını düzenleyin ve OpenAI API anahtarınızı ekleyin

# Masaüstü uygulamasını çalıştırın
python main_desktop.py
```

## Sistem Gereksinimleri

### Minimum Gereksinimler
- Windows 10+ (64-bit)
- 4GB RAM
- 2GB boş alan
- Python 3.10+ (geliştiriciler için)

### Veritabanı Gereksinimleri
- SQL Server 2016+ (2019+ önerilen)
- Microsoft ODBC Driver 17/18 for SQL Server
- TCP/IP bağlantısı
- Veritabanı okuma ve metadata erişimi

### Harici Hizmetler
- OpenAI API anahtarı
- İnternet bağlantısı (AI model iletişimi için)

## Kullanım

### 1. Veritabanı Bağlantısı
1. Uygulamayı başlatın
2. "Veritabanı Bağla" kartına tıklayın
3. Bağlantı bilgilerinizi girin (sunucu, veritabanı, kullanıcı adı, şifre)
4. "Bağlan" butonuna tıklayın

### 2. Doğal Dil Sorguları
1. "Yeni Sorgu" kartına tıklayın
2. Doğal dilde sorunuzu yazın
3. "Sorguyu Çalıştır" butonuna tıklayın
4. Sonuçları görüntüleyin ve grafikler oluşturun

### 3. Veri Görselleştirme
1. Sorgu sonuçlarını görüntüleyin
2. "Grafikler" sekmesine geçin
3. Grafik türünü seçin ve özelleştirin
4. Grafiği dışa aktarın

## Teknoloji Yığını

- **Frontend**: PyQt5 WebEngine, Vanilla JavaScript, Chart.js, CSS3
- **Backend**: Flask, PyQt5, pyodbc, OpenAI API
- **Güvenlik**: Windows Credential Manager, Keyring

## Build İşlemleri

```bash
# Masaüstü uygulaması build etme
build_desktop.bat

# NSIS installer oluşturma (NSIS kurulu olmalı)
makensis installer-desktop.nsi
```

## Sorun Giderme

### Bağlantı Sorunları
- "Login failed for user": Kullanıcı adı/şifre kontrol edin
- "Cannot connect to server": Sunucu adı ve port kontrol edin
- "Driver not found": ODBC Driver 17/18 kurulumunu kontrol edin

### UI Sorunları
- Renkler görünmüyor: Tarayıcı cache'ini temizleyin
- Font yüklenmiyor: İnternet bağlantısını kontrol edin
- İkonlar bozuk: CSS cache'ini temizleyin

## Lisans

MIT License - Detaylar için [LICENSE.txt](LICENSE.txt) dosyasına bakın.

*NIQ Desktop - Doğal dilinizi SQL'e dönüştürün*
