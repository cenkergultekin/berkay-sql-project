# NIQ Desktop — Natural Intelligence Query

Modern, kullanıcı dostu masaüstü uygulaması ile doğal dil sorularınızı Microsoft SQL Server için optimize edilmiş SQL sorgularına dönüştürün. PyQt5 WebEngine ile geliştirilmiş, Poppins font ve profesyonel renk paleti ile tasarlanmış, dashboard-first yaklaşımı benimseyen yeni nesil veritabanı etkileşim aracı.

## 🎨 Özellikler

### ✨ Modern Tasarım
- **Poppins Font**: Profesyonel ve okunabilir tipografi
- **Minimal Modern UI**: Temiz, kullanıcı dostu arayüz
- **Dashboard-First**: Ana sayfa odaklı kullanım deneyimi
- **Dinamik Hızlı İşlemler**: Bağlantı durumuna göre akıllı sıralama
- **Geometrik İkonlar**: Emoji-free, modern görsel tasarım

### 🤖 AI Destekli Sorgu Oluşturma
- **Doğal Dil İşleme**: OpenAI GPT-4o-mini ile güçlendirilmiş
- **Akıllı Şema Keşfi**: Otomatik tablo ve sütun keşfi
- **Sorgu Optimizasyonu**: AI destekli performans önerileri
- **Hata Düzeltme**: Akıllı SQL hata analizi ve çözüm önerileri

### 📊 Veri Görselleştirme
- **Otomatik Grafik Önerileri**: Chart.js ile etkileşimli grafikler
- **Çoklu Grafik Türleri**: Bar, line, pie, scatter plot
- **Responsive Tasarım**: Farklı ekran boyutlarına uyum
- **Export Özellikleri**: PNG/SVG formatında dışa aktarma

### 🔒 Güvenlik ve Performans
- **Windows Credential Manager**: OS seviyesi şifreleme
- **Zero Trust Architecture**: Şifreler asla düz metin olarak saklanmaz
- **Session Management**: Güvenli oturum yönetimi
- **Query History**: Güvenli sorgu geçmişi saklama

## 🚀 Hızlı Başlangıç

### End Kullanıcılar İçin (Önerilen)
1. **NIQDesktop_Setup.exe** dosyasını indirin
2. Kurulum sihirbazını çalıştırın
3. Masaüstü kısayolundan NIQ Desktop'ı başlatın
4. Veritabanı bağlantınızı kurun ve sorgularınızı oluşturun!

### Geliştiriciler İçin
```bash
# Repository'yi klonlayın
git clone https://github.com/cenkergultekin/berkay-sql-project.git
cd berkay-sql-project

# Sanal ortam oluşturun
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

# Bağımlılıkları kurun
pip install -r requirements.txt

# Ortam değişkenlerini ayarlayın
copy env_example.txt .env
# .env dosyasını düzenleyin ve OpenAI API anahtarınızı ekleyin

# Masaüstü uygulamasını çalıştırın
python main_desktop.py

# Veya web versiyonunu çalıştırın
python main.py
```

## 📋 Sistem Gereksinimleri

### Minimum Gereksinimler
- **İşletim Sistemi**: Windows 10+ (64-bit)
- **Bellek**: 4GB RAM
- **Depolama**: 2GB boş alan
- **Python**: 3.10+ (geliştiriciler için)

### Veritabanı Gereksinimleri
- **SQL Server**: 2016+ (2019+ önerilen)
- **ODBC Driver**: Microsoft ODBC Driver 17/18 for SQL Server
- **Ağ**: TCP/IP bağlantısı
- **İzinler**: Veritabanı okuma ve metadata erişimi

### Harici Hizmetler
- **OpenAI API**: Aktif API anahtarı
- **İnternet**: AI model iletişimi için

## 🛠️ Teknoloji Yığını

### Frontend
- **PyQt5 WebEngine**: Native masaüstü uygulaması
- **Vanilla JavaScript**: Framework-free, yüksek performans
- **Chart.js**: Etkileşimli veri görselleştirme
- **CSS3**: Modern, responsive tasarım
- **Poppins Font**: Google Fonts entegrasyonu

### Backend
- **Flask**: Hafif ve esnek web framework
- **PyQt5**: Masaüstü uygulama framework'ü
- **pyodbc**: SQL Server bağlantısı
- **OpenAI API**: Doğal dil işleme

### Güvenlik
- **Windows Credential Manager**: OS seviyesi şifreleme
- **Keyring**: Güvenli kimlik bilgisi yönetimi
- **Session Management**: Güvenli oturum kontrolü

## 📖 Kullanım Rehberi

### 1. Veritabanı Bağlantısı
1. Uygulamayı başlatın
2. "Veritabanı Bağla" kartına tıklayın
3. Bağlantı bilgilerinizi girin:
   - **Sunucu**: `localhost\SQLEXPRESS` (veya sunucunuz)
   - **Veritabanı**: Hedef veritabanı adı
   - **Kullanıcı Adı**: SQL Server kullanıcı adı
   - **Şifre**: Şifreniz (güvenli şekilde saklanır)
4. "Bağlan" butonuna tıklayın

### 2. Doğal Dil Sorguları
1. "Yeni Sorgu" kartına tıklayın
2. Doğal dilde sorunuzu yazın:
   - "En çok satan 10 ürünü göster"
   - "Geçen ayın satış raporunu hazırla"
   - "Hangi müşteriler 6 aydır sipariş vermemiş?"
3. "Sorguyu Çalıştır" butonuna tıklayın
4. Sonuçları görüntüleyin ve grafikler oluşturun

### 3. Veri Görselleştirme
1. Sorgu sonuçlarını görüntüleyin
2. "Grafikler" sekmesine geçin
3. Otomatik önerilen grafik türünü seçin
4. Grafik ayarlarını özelleştirin
5. Grafiği PNG/SVG olarak dışa aktarın

### 4. Sorgu Geçmişi
1. "Sorgu Geçmişi" sekmesine geçin
2. Önceki sorgularınızı görüntüleyin
3. Sorguları tekrar çalıştırın
4. Performans metriklerini inceleyin

## 🔧 Geliştirme

### Proje Yapısı
```
berkay-sql-project/
├── main_desktop.py          # Masaüstü uygulaması giriş noktası
├── main.py                  # Web uygulaması giriş noktası
├── app.py                   # Flask uygulaması
├── backend/                 # Backend modülleri
│   ├── config/             # Yapılandırma
│   ├── core/               # Temel yardımcılar
│   ├── models/             # Veri modelleri
│   ├── routes/             # API rotaları
│   └── services/           # İş mantığı servisleri
├── frontend/               # Frontend dosyaları
│   ├── static/            # CSS, JS, görseller
│   └── templates/         # HTML şablonları
├── dist/                   # Build çıktıları
├── build_desktop.bat       # Masaüstü build scripti
├── Setup.bat              # Kurulum scripti
└── installer-desktop.nsi  # NSIS installer scripti
```

### Build İşlemleri
```bash
# Masaüstü uygulaması build etme
build_desktop.bat

# NSIS installer oluşturma (NSIS kurulu olmalı)
makensis installer-desktop.nsi
```

### Ortam Değişkenleri
```bash
# .env dosyası
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini
DEFAULT_ODBC_DRIVER=ODBC Driver 17 for SQL Server
DB_CONNECTION_TIMEOUT=30
DEBUG=False
```

## 🚨 Sorun Giderme

### Yaygın Sorunlar

#### Bağlantı Sorunları
- **"Login failed for user"**: Kullanıcı adı/şifre kontrol edin
- **"Cannot connect to server"**: Sunucu adı ve port kontrol edin
- **"Driver not found"**: ODBC Driver 17/18 kurulumunu kontrol edin

#### Performans Sorunları
- **Yavaş sorgular**: AI'dan optimizasyon önerilerini kullanın
- **Bellek sorunları**: MAX_QUERY_LENGTH ayarını artırın
- **Timeout hataları**: DB_CONNECTION_TIMEOUT değerini artırın

#### UI Sorunları
- **Renkler görünmüyor**: Tarayıcı cache'ini temizleyin
- **Font yüklenmiyor**: İnternet bağlantısını kontrol edin
- **İkonlar bozuk**: CSS cache'ini temizleyin

## 📄 Lisans

MIT License - Detaylar için [LICENSE.txt](LICENSE.txt) dosyasına bakın.

## 🤝 Katkıda Bulunma

1. Repository'yi fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📞 Destek

- **GitHub Issues**: [Sorun bildirimi](https://github.com/cenkergultekin/berkay-sql-project/issues)
- **GitHub Discussions**: [Topluluk tartışmaları](https://github.com/cenkergultekin/berkay-sql-project/discussions)

## 🎯 Roadmap

### v4.0 (Gelecek)
- [ ] Çoklu veritabanı desteği
- [ ] Gelişmiş grafik türleri
- [ ] Sorgu şablonları
- [ ] Export/Import özellikleri
- [ ] Plugin sistemi

### v3.1 (Yakında)
- [ ] Performans iyileştirmeleri
- [ ] Ek grafik türleri
- [ ] Gelişmiş hata mesajları
- [ ] Kullanıcı tercihleri

---

**Veri topluluğu için ❤️ ile inşa edildi**

*NIQ Desktop - Doğal dilinizi SQL'e dönüştürün*