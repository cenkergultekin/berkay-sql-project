# 📅 Zamanlanmış Sorgular - Kullanım Kılavuzu

## ❗ ÖNEMLİ: Schedule Type'ları Nasıl Çalışır?

### 1. **HOURLY (Saatlik)** - Her saat başı
```
Çalışma: Her saat 00. dakikada
Örnek: 14:00, 15:00, 16:00, 17:00...
```

### 2. **DAILY (Günlük)** - Her gün aynı saatte ⚠️
```
Çalışma: Her gün belirtilen saatte
Örnek: Saat 14:30'a zamanladınız
  - Şu an saat 14:25 ise → BUGÜN 14:30'da çalışacak
  - Şu an saat 14:35 ise → YARIN 14:30'da çalışacak (bugün geçti)
```

### 3. **WEEKLY (Haftalık)** - Her hafta aynı gün/saatte
```
Çalışma: Seçilen günde, belirtilen saatte
Örnek: Her Pazartesi 14:30
```

### 4. **MONTHLY (Aylık)** - Her ay aynı gün/saatte
```
Çalışma: Her ayın belirtilen gününde, belirtilen saatte
Örnek: Her ayın 1. günü 14:30
```

---

## 🎯 Hemen Test İçin Çözümler

### Yöntem 1: Web Arayüzünden "Şimdi Çalıştır" Butonu ✅
1. Zamanlanmış sorgunuzu oluşturun
2. Zamanlanmış Sorgular listesinde **"▶️ Şimdi Çalıştır"** butonuna tıklayın
3. Sorgu anında çalıştırılacak!
4. Sonuçları "Geçmiş" sekmesinden görün

### Yöntem 2: Terminal ile Test
```bash
# Scheduler durumunu kontrol et
python test_scheduler.py

# Belirli bir sorguyu hemen çalıştır
python test_scheduler.py <scheduled_query_id>
# Örnek: python test_scheduler.py 1
```

### Yöntem 3: API ile Test
```bash
# Scheduler durumunu gör
curl http://localhost:5000/api/scheduler/status

# Sorguyu hemen çalıştır
curl -X POST http://localhost:5000/api/scheduled-queries/1/run-now
```

---

## 🔍 Sorun Giderme

### "Henüz Çalıştırılmadı" Diyor
**Neden?**
- Daily/Weekly/Monthly schedule'lar gelecekteki bir zamana ayarlıdır
- Şu anki saat, belirttiğiniz saati geçtiyse, bir sonraki defa çalışacak

**Çözüm:**
- **"Şimdi Çalıştır"** butonunu kullanın (test için)
- Veya gerçek zamanlı test için **HOURLY** seçin

### Scheduler Çalışıyor mu?
Terminal'de şu log'ları görmelisiniz:
```
Query scheduler initialized with timezone: Europe/Istanbul
Query scheduler started - Current time: 2025-10-12 14:35:00 +03
✅ Active scheduled queries loaded
```

### Timezone Problemi
- Uygulama artık **Europe/Istanbul (GMT+3)** kullanıyor
- Tüm zamanlar Türkiye saati ile çalışıyor
- Log dosyalarında "+03" göreceksiniz

---

## 📊 Scheduler Durumunu İnceleme

### Browser Developer Console'da:
```javascript
// Scheduler status'u çek
fetch('/api/scheduler/status')
  .then(r => r.json())
  .then(d => console.log(d));
```

### Python Script ile:
```python
python test_scheduler.py
```

Çıktı örneği:
```
================================================================================
🔍 SCHEDULER STATUS CHECK
================================================================================

📊 Scheduler Running: ✅ YES
🕐 Current Time (Turkey): 2025-10-12 14:35:00 +03

📋 Total Jobs Scheduled: 1

--------------------------------------------------------------------------------

🔹 Job ID: scheduled_query_1
   Function: scheduler:QueryScheduler._execute_scheduled_query
   Next Run: 2025-10-13 14:30:00+03:00
   Trigger: cron[hour='14', minute='30']
   ⏰ Time Until Run: 23h 55m 0s
--------------------------------------------------------------------------------
```

---

## 💡 En İyi Pratikler

### Test İçin:
1. **"Şimdi Çalıştır"** butonunu kullanın
2. Veya HOURLY seçin ve birkaç dakika bekleyin

### Gerçek Kullanım İçin:
1. DAILY: Günlük raporlar (örn: her sabah 09:00)
2. WEEKLY: Haftalık özetler (örn: her Pazartesi 10:00)
3. MONTHLY: Aylık raporlar (örn: her ayın ilk günü)

### Zamanı Geçmiş Sorgular:
- Daily schedule'da zamanı geçtiyse YARIN çalışır
- Hemen test etmek için **"Şimdi Çalıştır"** kullanın

---

## 🚀 Hızlı Başlangıç

1. **Uygulamayı başlatın:**
   ```bash
   python app.py
   ```

2. **Veritabanı bağlantısı kurun**

3. **Zamanlanmış sorgu oluşturun**

4. **Test edin:**
   - Web'den: "Şimdi Çalıştır" butonu
   - Terminal'den: `python test_scheduler.py 1`

5. **Sonuçları görün:**
   - "Geçmiş" sekmesinde
   - `sorgularim.txt` dosyasında

---

## ❓ Sık Sorulan Sorular

**S: Saati 14:30 yaptım, 14:35 oldu ama çalışmadı?**
C: Daily schedule yarın 14:30'da çalışacak. Hemen test için "Şimdi Çalıştır" kullanın.

**S: Scheduler başlamıyor?**
C: Veritabanı bağlantısını kurdunuz mu? Scheduler veritabanı bağlantısından sonra başlar.

**S: Hangi timezone kullanılıyor?**
C: Europe/Istanbul (GMT+3) - Türkiye saati

**S: Log dosyasına nasıl bakabilirim?**
C: `sorgularim.txt` dosyasına bakın. Her çalışan sorgu burada loglanır.

---

## 📞 Destek

Sorun yaşıyorsanız:
1. `python test_scheduler.py` çalıştırın
2. Terminal log'larını kontrol edin
3. `/api/scheduler/status` endpoint'ini kontrol edin

