# 🔧 Scheduler Sorun Giderme Kılavuzu

## 🚨 Scheduler Çalışmıyor - Adım Adım Çözüm

### Adım 1: Scheduler'ın Durumunu Kontrol Edin

Terminal'de:
```bash
python test_scheduler.py
```

Bu komut size şunları gösterecek:
- ✅ Scheduler çalışıyor mu?
- 🕐 Şu anki zaman (Türkiye saati)
- 📋 Kaç tane job zamanlanmış
- ⏰ Her job'un bir sonraki çalışma zamanı

### Adım 2: Sorunları Tespit Edin

#### Problem 1: "Scheduler Running: ❌ NO"

**Sebep:** Scheduler başlatılmamış.

**Çözüm:**
1. Uygulamayı başlatın: `python app.py`
2. Web arayüzünden veritabanı bağlantısını kurun
3. Tekrar kontrol edin: `python test_scheduler.py`

**Alternatif:** Test için manuel başlatma:
```bash
python test_scheduler.py --setup
```

#### Problem 2: "Total Jobs Scheduled: 0"

**Sebep:** Aktif zamanlanmış sorgu yok.

**Nedenler:**
- Hiç zamanlanmış sorgu oluşturmadınız
- Zamanlanmış sorgu "pasif" durumda
- Database bağlantısı kurulmadan önce job oluşturuldu

**Çözüm:**
1. Web arayüzünden "Zamanlanmış Sorgu" oluşturun
2. Sorgunun "Aktif" olduğundan emin olun
3. Sayfayı yenileyin veya toggle (pasif→aktif) yapın
4. Kontrol: `python test_scheduler.py`

#### Problem 3: Job var ama "Next Run Time" çok uzakta

**Sebep:** Daily/Weekly/Monthly schedule'ın zamanı geçmiş.

**Örnek:**
- Saat 14:30'a ayarladınız
- Şu an 14:35
- Sonraki çalışma: YARIN 14:30

**Çözüm:**
- Hemen test için: "Şimdi Çalıştır" butonu
- Veya: HOURLY schedule seçin (her saat başı çalışır)

#### Problem 4: "Time Until Run: X seconds ago (missed)"

**Sebep:** Job'un zamanı geldi ama çalışmadı.

**Olası Nedenler:**
1. Scheduler o sırada çalışmıyordu
2. Database/AI servis bağlantısı yoktu
3. Uygulama yeniden başlatıldı

**Çözüm:**
1. Scheduler'ın çalıştığından emin olun
2. Log dosyalarını kontrol edin
3. Manuel çalıştırın: `python test_scheduler.py <query_id>`

---

## 🔍 Log Dosyalarını İnceleme

### Terminal Log'ları

Uygulama başlatıldığında görmemeniz gereken log'lar:

✅ **BAŞARILI:**
```
Query scheduler initialized with timezone: Europe/Istanbul
🚀 Query scheduler started successfully!
🕐 Current time: 2025-10-12 15:30:00 +03
🌍 Timezone: Europe/Istanbul
📋 Loading 2 active scheduled queries...
  - Loading query #1: Günlük satış raporu... (daily)
✅ Added scheduled query 1 with type 'daily' - Next run: 2025-10-13 09:00:00 +03
  - Loading query #2: Saatlik kontrol... (hourly)  
✅ Added scheduled query 2 with type 'hourly' - Next run: 2025-10-12 16:00:00 +03
✅ Successfully loaded 2/2 scheduled queries
```

❌ **SORUNLU:**
```
❌ Database manager not set - Cannot load scheduled queries
```
→ **Çözüm:** Veritabanı bağlantısını kurun

```
⚠️ Added scheduled query 1 but no next_run_time set!
```
→ **Çözüm:** Schedule type veya time yanlış girilmiş olabilir

### Scheduled Query Çalıştığında

✅ **BAŞARILI:**
```
🔔 EXECUTING SCHEDULED QUERY #1 at 2025-10-12 16:00:00 +03
✅ Scheduled query #1 executed successfully! Saved as query ID: 42
```

❌ **BAŞARISIZ:**
```
🔔 EXECUTING SCHEDULED QUERY #1 at 2025-10-12 16:00:00 +03
❌ Error executing scheduled query #1: [error message]
```
→ Hata mesajını kontrol edin ve sorguyu düzeltin

### sorgularim.txt Dosyası

Her çalıştırılan sorgu burada loglanır:
```
================================================================================
ZAMANLANMIŞ SORGU #42 (Schedule ID: 1)
TARİH: 2025-10-12 16:00:00 +03
DURUM: ✅ BAŞARILI
================================================================================

📝 SORU:
Bugünkü toplam satış tutarını getir

📋 TABLOLAR:
Sales, Products

🔍 SQL SORGUSU:
SELECT SUM(total_amount) FROM Sales WHERE date = CAST(GETDATE() AS DATE)

📊 SONUÇLAR: 1 satır
```

---

## 🐛 Yaygın Hatalar ve Çözümleri

### Hata: "No database connection found"

**Sebep:** Veritabanı bağlantısı kurulmamış.

**Çözüm:**
1. Uygulamayı başlatın
2. Web arayüzünden "Veritabanı Bağlantısı" bölümüne gidin
3. Connection string'i girin ve "Bağlan" butonuna tıklayın

### Hata: "OPENAI_API_KEY environment variable is required"

**Sebep:** OpenAI API key'i ayarlanmamış.

**Çözüm:**
1. `.env` dosyası oluşturun (veya var olanı düzenleyin)
2. Ekleyin: `OPENAI_API_KEY=sk-your-key-here`
3. Uygulamayı yeniden başlatın

### Hata: Timezone yanlış görünüyor

**Kontrol:**
```bash
python test_scheduler.py
```
"Current Time (Turkey)" kısmına bakın.

**Çözüm:**
- Sistem Türkiye saatini gösteriyorsa her şey doğru
- Yanlış timezone gösteriyorsa, `scheduler.py` dosyasındaki `TIMEZONE` ayarını kontrol edin

### Hata: Job çalıştı ama sonuç yok

**Kontrol edin:**
1. `sorgularim.txt` dosyasını açın → Son sorguyu görün
2. "Geçmiş" sekmesine bakın → Query ID'yi bulun
3. Log'larda hata var mı?

**Olası sebepler:**
- SQL sorgusu hatalı
- Tablo/kolon adları yanlış
- Veritabanı bağlantısı kesildi

---

## 🧪 Test Adımları

### 1. Hızlı Test (Manuel Trigger)

```bash
# Scheduler durumunu kontrol et
python test_scheduler.py

# Sorgu ID'si 1'i hemen çalıştır
python test_scheduler.py 1
```

### 2. Saatlik Test (Hourly)

1. Yeni zamanlanmış sorgu oluşturun
2. Schedule Type: **HOURLY**
3. Bekleyin: Bir sonraki saat başı çalışacak
4. Kontrol: `sorgularim.txt` dosyası

### 3. Gerçek Zamanlı Test (Özel Zaman)

1. Schedule Type: **DAILY**
2. Time: **Şu andan 2-3 dakika sonrası** (örn: şu an 15:45 ise → 15:48)
3. Kaydet ve bekle
4. 2-3 dakika sonra kontrol et

### 4. API Test

```bash
# Scheduler durumu
curl http://localhost:5000/api/scheduler/status | python -m json.tool

# Zamanlanmış sorguları listele
curl http://localhost:5000/api/scheduled-queries | python -m json.tool

# Query #1'i hemen çalıştır
curl -X POST http://localhost:5000/api/scheduled-queries/1/run-now | python -m json.tool
```

---

## 📊 Detaylı Debugging

### APScheduler Job'larını İnceleme

Python console'da:
```python
from scheduler import query_scheduler

# Scheduler çalışıyor mu?
print(query_scheduler.scheduler.running)

# Tüm job'lar
jobs = query_scheduler.scheduler.get_jobs()
for job in jobs:
    print(f"ID: {job.id}")
    print(f"Next run: {job.next_run_time}")
    print(f"Trigger: {job.trigger}")
    print("---")

# Belirli bir job'u al
job = query_scheduler.scheduler.get_job("scheduled_query_1")
print(job)
```

### Database'deki Scheduled Queries

Python console'da:
```python
from database import DatabaseManager
from config import Config

# Veritabanına bağlan
db = DatabaseManager("YOUR_CONNECTION_STRING")

# Tüm scheduled query'leri al
queries = db.get_all_scheduled_queries()

for q in queries:
    print(f"ID: {q.id}")
    print(f"Question: {q.question}")
    print(f"Schedule: {q.schedule_type} - {q.schedule_time}")
    print(f"Active: {q.is_active}")
    print(f"Last run: {q.last_run_at}")
    print("---")
```

---

## 🔄 Scheduler'ı Yeniden Başlatma

### Yöntem 1: Uygulamayı Yeniden Başlat

1. Uygulamayı kapat (Ctrl+C)
2. Tekrar başlat: `python app.py`
3. Veritabanı bağlantısını kur
4. Scheduler otomatik başlayacak

### Yöntem 2: Toggle ile Yenile

Web arayüzünden:
1. Zamanlanmış sorguyu "Pasif" yap
2. Tekrar "Aktif" yap
3. Bu job'u yeniden yükler

### Yöntem 3: Manuel Reload

Python console'da:
```python
from scheduler import query_scheduler

# Job'ları temizle
query_scheduler.scheduler.remove_all_jobs()

# Yeniden yükle
query_scheduler.load_all_scheduled_queries()
```

---

## 💊 Son Çare: Sıfırdan Kurulum

Hiçbir şey çalışmıyorsa:

1. **Uygulamayı tamamen kapat**
2. **Database'deki tabloları kontrol et:**
   ```sql
   SELECT * FROM scheduled_queries WHERE is_active = 1
   ```
3. **Test scheduler'ı çalıştır:**
   ```bash
   python test_scheduler.py --setup
   ```
4. **Connection string'i gir**
5. **Durum kontrol:**
   ```bash
   python test_scheduler.py
   ```
6. **Manuel test:**
   ```bash
   python test_scheduler.py 1
   ```

---

## 📞 Hala Çözülmediyse

Lütfen aşağıdaki bilgileri toplayın:

1. **Scheduler durumu:**
   ```bash
   python test_scheduler.py > scheduler_status.txt
   ```

2. **Son log'lar:**
   - Terminal'deki tüm output
   - `sorgularim.txt` dosyasının son 50 satırı

3. **Database durumu:**
   ```sql
   SELECT id, question, schedule_type, schedule_time, is_active, last_run_at 
   FROM scheduled_queries
   ```

4. **Ortam bilgisi:**
   - Python versiyonu: `python --version`
   - OS: Windows/Linux/Mac
   - APScheduler versiyonu: `pip show apscheduler`

---

## ✅ İşe Yaraması Gereken Minimum Setup

```bash
# 1. Uygulamayı başlat
python app.py

# 2. Başka bir terminal'de
python test_scheduler.py --setup
# Connection string'i gir

# 3. Scheduler durumunu kontrol et
python test_scheduler.py

# Beklenen çıktı:
# ✅ Scheduler Running: YES
# ✅ Database bağlantısı var
# ✅ Job'lar yüklü

# 4. Test
python test_scheduler.py 1
# Beklenen: ✅ Query executed successfully
```

Eğer bu adımlar sonunda çalışmıyorsa, kod seviyesinde bir sorun var demektir.

