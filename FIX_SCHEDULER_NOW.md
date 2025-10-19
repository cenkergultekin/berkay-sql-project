# 🚀 Scheduler Sorunlarını Hemen Çözüm Kılavuzu

## ❗ ŞU AN SORUNLAR:

1. ✅ **"Total Jobs Scheduled: 0"** - Scheduler çalışmıyor çünkü:
   - Uygulama başlatılmamış VEYA
   - Database bağlantısı kurulmamış VEYA
   - Zamanlanmış sorgu oluşturmadınız

2. ❓ **"Şimdi Çalıştır" endpoint not found** - Endpoint var, ama scheduler services ayarlanmamış olabilir

## 🔧 HEMEN DÜZELTME ADIMLARI

### Adım 1: Uygulamayı Başlatın

Terminal'de:
```bash
python app.py
```

Görmek istediğiniz log'lar:
```
Query scheduler initialized with timezone: Europe/Istanbul
🚀 Query scheduler started successfully!
🕐 Current time: 2025-10-12 12:30:00 +03
🌍 Timezone: Europe/Istanbul
✅ Scheduler started at application startup
```

### Adım 2: Tarayıcıda Veritabanı Bağlantısı Kurun

1. http://localhost:5000 adresini açın
2. Connection string'inizi girin
3. "Bağlan" butonuna tıklayın

Terminal'de görmek istediğiniz log'lar:
```
✅ Scheduler services configured (db_manager, ai_service)
ℹ️ Scheduler already running - Ready to load jobs
📋 Loading X active scheduled queries...
✅ Successfully loaded X/X scheduled queries
```

### Adım 3: Zamanlanmış Sorgu Oluşturun

1. Web arayüzünde "Zamanlanmış Sorgular" sekmesine gidin
2. Yeni bir zamanlanmış sorgu oluşturun:
   - Soru: "Toplam satış sayısı"
   - Tablo: Bir tablo seçin
   - Schedule Type: **HOURLY** (test için en iyi)
   - "Zamanlanmış Sorgu Oluştur" butonuna tıklayın

Terminal'de görmek istediğiniz log:
```
✅ Added scheduled query 1 with type 'hourly' - Next run: 2025-10-12 13:00:00 +03
```

### Adım 4: Şimdi Test Edin

**YÖNTEM 1: Web Arayüzünden "Şimdi Çalıştır" Butonu**
1. Zamanlanmış sorgular listesinde "▶️ Şimdi Çalıştır" butonuna tıklayın
2. Başarılı olursa: "✅ Sorgu başarıyla çalıştırıldı!" mesajını göreceksiniz
3. "Geçmiş" sekmesinden sonuçları kontrol edin

Terminal'de görmek istediğiniz log:
```
🔔 EXECUTING SCHEDULED QUERY #1 at 2025-10-12 12:35:00 +03
✅ Scheduled query #1 executed successfully! Saved as query ID: 42
```

**YÖNTEM 2: Test Script ile**

Yeni bir terminal açın:
```bash
python test_scheduler.py
```

Çıktı şöyle olmalı:
```
================================================================================
🔍 SCHEDULER STATUS CHECK
================================================================================

📊 Scheduler Running: ✅ YES
🕐 Current Time (Turkey): 2025-10-12 12:35:00 +03

📋 Total Jobs Scheduled: 1

--------------------------------------------------------------------------------

🔹 Job ID: scheduled_query_1
   Next Run: 2025-10-12 13:00:00+03:00
   ⏰ Time Until Run: 0h 25m 0s
--------------------------------------------------------------------------------
```

Sorguyu manuel çalıştırmak için:
```bash
python test_scheduler.py 1
```

## 🐛 HALA ÇALIŞMIYORSA

### Problem: "Scheduler Running: NO"

**Sebep:** Uygulama çalışmıyor veya scheduler başlatılmadı

**Çözüm:**
```bash
# Uygulamayı başlatın
python app.py

# Başka terminal'de kontrol edin
python test_scheduler.py
```

### Problem: "Total Jobs Scheduled: 0" ama sorgu oluşturdum

**Sebepeler:**
1. Sorgu "Pasif" durumda
2. Database bağlantısı kurulmadan önce oluşturuldu
3. Scheduler hata verdi (terminal log'larına bakın)

**Çözüm 1: Toggle Trick**
- Sorguyu "Pasif" yapın
- Tekrar "Aktif" yapın
- Bu scheduler'ı yeniden yükler

**Çözüm 2: Uygulamayı Yeniden Başlatın**
```bash
# Ctrl+C ile durdurun
# Tekrar başlatın
python app.py

# Database bağlantısını kurun
# Scheduler otomatik olarak job'ları yükleyecek
```

**Çözüm 3: Database'i Kontrol Edin**

Python console'da:
```python
from database import DatabaseManager

# Connection string'inizi buraya girin
conn_str = "YOUR_CONNECTION_STRING"
db = DatabaseManager(conn_str)

# Zamanlanmış sorguları kontrol edin
queries = db.get_all_scheduled_queries(active_only=True)
print(f"Aktif sorgular: {len(queries)}")

for q in queries:
    print(f"ID: {q.id}, Soru: {q.question}, Aktif: {q.is_active}")
```

### Problem: "Şimdi Çalıştır" butonu "endpoint not found" hatası veriyor

**Sebep:** Scheduler services ayarlanmamış

**Kontrol:**
1. Terminal log'larında şu satır var mı?
   ```
   ✅ Scheduler services configured (db_manager, ai_service)
   ```

2. Yoksa, database bağlantısını tekrar kurun:
   - Connection string'i tekrar girin
   - "Bağlan" butonuna tıklayın

**Alternatif Çözüm:**

Tarayıcı console'unda (F12) test edin:
```javascript
// Scheduler durumunu kontrol et
fetch('/api/scheduler/status')
  .then(r => r.json())
  .then(d => console.log(d));

// Sorgu çalıştır (ID'yi değiştirin)
fetch('/api/scheduled-queries/1/run-now', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'}
})
  .then(r => r.json())
  .then(d => console.log(d));
```

### Problem: Sorgu çalışıyor ama sonuç yok

**Kontrol 1: sorgularim.txt dosyası**
```bash
# En son 50 satırı göster
tail -n 50 sorgularim.txt

# Windows'ta:
Get-Content sorgularim.txt -Tail 50
```

**Kontrol 2: Database'de saved_queries tablosu**
```sql
SELECT TOP 10 id, question, created_at, is_successful, is_scheduled 
FROM saved_queries 
ORDER BY created_at DESC
```

**Kontrol 3: Terminal log'ları**
- ❌ ile başlayan hata mesajlarını arayın
- Error executing scheduled query mesajlarına bakın

## ✅ BAŞARILI KURULUM KONTROL LİSTESİ

Hepsini işaretleyin:

- [ ] Uygulama çalışıyor (`python app.py`)
- [ ] Terminal'de "Scheduler started successfully" mesajı görünüyor
- [ ] Veritabanı bağlantısı kuruldu
- [ ] Terminal'de "Scheduler services configured" mesajı görünüyor
- [ ] En az bir zamanlanmış sorgu oluşturuldu
- [ ] `python test_scheduler.py` komutu "✅ YES" gösteriyor
- [ ] `python test_scheduler.py` komutu en az 1 job gösteriyor
- [ ] "Şimdi Çalıştır" butonu çalışıyor
- [ ] `sorgularim.txt` dosyasında yeni kayıtlar görünüyor
- [ ] "Geçmiş" sekmesinde sonuçlar görünüyor

## 🎯 HIZLI TESTköre (5 Dakikada)

```bash
# Terminal 1: Uygulamayı başlat
python app.py

# Tarayıcı: http://localhost:5000
# - Database bağlantısı kur
# - Zamanlanmış sorgu oluştur (HOURLY)
# - "Şimdi Çalıştır" butonuna tıkla
# - "Geçmiş" sekmesinden sonucu gör

# Terminal 2: Kontrol et
python test_scheduler.py

# Çıktıda görmek istediğiniz:
# ✅ Scheduler Running: YES
# 📋 Total Jobs Scheduled: 1
# ⏰ Time Until Run: X minutes

# Manuel trigger
python test_scheduler.py 1

# Beklenen: ✅ Query #1 executed successfully!
```

## 📞 EN SON ÇARE

Hiçbir şey işe yaramazsa:

1. **Uygulamayı tamamen kapat** (Ctrl+C)

2. **Python cache'i temizle:**
   ```bash
   # Windows
   del /s /q __pycache__
   del /s /q *.pyc
   
   # Linux/Mac
   find . -type d -name __pycache__ -exec rm -rf {} +
   find . -type f -name "*.pyc" -delete
   ```

3. **Test scheduler ile setup yap:**
   ```bash
   python test_scheduler.py --setup
   ```
   
4. **Connection string'i gir ve adımları takip et**

5. **Test et:**
   ```bash
   python test_scheduler.py
   ```

## 🆘 YARDıM İÇİN GEREKLİ BİLGİLER

Hala çözülmediyse, şu bilgileri toplayın:

**1. Scheduler durumu:**
```bash
python test_scheduler.py > scheduler_output.txt
```

**2. Uygulama log'ları:**
- Terminal'deki TÜM output'u kopyalayın
- Özellikle ❌ ve "error" içeren satırları

**3. Database durumu:**
```python
from database import DatabaseManager

db = DatabaseManager("YOUR_CONNECTION_STRING")
queries = db.get_all_scheduled_queries()
print(f"Toplam: {len(queries)}")
for q in queries:
    print(f"ID: {q.id}, Aktif: {q.is_active}, Tip: {q.schedule_type}")
```

**4. Ortam bilgisi:**
```bash
python --version
pip show apscheduler
pip show flask
```

Bu bilgilerle sorunu çözebiliriz!

