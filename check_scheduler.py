"""
Hızlı scheduler durumu kontrol script'i
Scheduler'ın neden çalışmadığını anında gösterir
"""
import sys

# Fix Windows encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

print("\n" + "="*80)
print("🔍 SCHEDULER SORUN TESPİT ARACI")
print("="*80 + "\n")

issues = []
warnings = []
success = []

# Check 1: Scheduler module
print("1️⃣ Scheduler modülü kontrol ediliyor...")
try:
    from scheduler import query_scheduler, TIMEZONE
    success.append("✅ Scheduler modülü yüklendi")
    print("   ✅ Scheduler modülü yüklendi")
except Exception as e:
    issues.append(f"❌ Scheduler modülü yüklenemedi: {e}")
    print(f"   ❌ HATA: {e}")
    sys.exit(1)

# Check 2: Scheduler running
print("\n2️⃣ Scheduler durumu kontrol ediliyor...")
is_running = query_scheduler.scheduler.running
if is_running:
    success.append("✅ Scheduler çalışıyor")
    print("   ✅ Scheduler ÇALIŞIYOR")
else:
    issues.append("❌ Scheduler ÇALIŞMIYOR - Uygulamayı başlatın: python app.py")
    print("   ❌ Scheduler ÇALIŞMIYOR")
    print("   💡 Çözüm: python app.py ile uygulamayı başlatın")

# Check 3: Services configured
print("\n3️⃣ Scheduler servisleri kontrol ediliyor...")
if query_scheduler.db_manager and query_scheduler.ai_service:
    success.append("✅ Scheduler servisleri yapılandırılmış")
    print("   ✅ Database ve AI servisleri yapılandırılmış")
else:
    issues.append("❌ Scheduler servisleri yapılandırılmamış - Database bağlantısı kurun")
    print("   ❌ Servisler yapılandırılmamış")
    print("   💡 Çözüm: Web arayüzünden database bağlantısı kurun")

# Check 4: Jobs scheduled
print("\n4️⃣ Zamanlanmış işler kontrol ediliyor...")
jobs = query_scheduler.scheduler.get_jobs()
if len(jobs) > 0:
    success.append(f"✅ {len(jobs)} adet job zamanlanmış")
    print(f"   ✅ {len(jobs)} adet job zamanlanmış")
    
    from datetime import datetime
    current_time = datetime.now(TIMEZONE)
    
    for job in jobs:
        print(f"\n   📋 Job: {job.id}")
        if job.next_run_time:
            time_diff = job.next_run_time - current_time
            total_seconds = int(time_diff.total_seconds())
            
            if total_seconds > 0:
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                print(f"   ⏰ Bir sonraki çalışma: {hours}s {minutes}d sonra")
                print(f"   📅 Tarih: {job.next_run_time.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                warnings.append(f"⚠️ Job {job.id} geç kalmış ({abs(total_seconds)}s)")
                print(f"   ⚠️ UYARI: {abs(total_seconds)} saniye GEÇ!")
else:
    issues.append("❌ Hiç job zamanlanmamış - Zamanlanmış sorgu oluşturun")
    print("   ❌ Hiç job zamanlanmamış")
    print("   💡 Çözüm: Web arayüzünden zamanlanmış sorgu oluşturun")

# Check 5: Database check
if query_scheduler.db_manager:
    print("\n5️⃣ Database zamanlanmış sorguları kontrol ediliyor...")
    try:
        scheduled_queries = query_scheduler.db_manager.get_all_scheduled_queries(active_only=True)
        if len(scheduled_queries) > 0:
            success.append(f"✅ Database'de {len(scheduled_queries)} aktif sorgu")
            print(f"   ✅ Database'de {len(scheduled_queries)} aktif sorgu bulundu")
            
            for sq in scheduled_queries:
                print(f"\n   📝 Sorgu #{sq.id}: {sq.question[:50]}...")
                print(f"      Tip: {sq.schedule_type}")
                if sq.schedule_time:
                    print(f"      Zaman: {sq.schedule_time}")
                if sq.last_run_at:
                    print(f"      Son çalışma: {sq.last_run_at}")
                else:
                    print(f"      Son çalışma: Henüz çalışmadı")
        else:
            issues.append("❌ Database'de aktif sorgu yok")
            print("   ❌ Database'de aktif sorgu bulunamadı")
            print("   💡 Çözüm: Web arayüzünden zamanlanmış sorgu oluşturun")
    except Exception as e:
        issues.append(f"❌ Database sorgusu başarısız: {e}")
        print(f"   ❌ Database sorgusu başarısız: {e}")
else:
    print("\n5️⃣ Database kontrol edilemiyor (bağlantı yok)")
    warnings.append("⚠️ Database bağlantısı yok")

# Final summary
print("\n" + "="*80)
print("📊 ÖZET")
print("="*80 + "\n")

if success:
    print("✅ BAŞARILAR:")
    for s in success:
        print(f"   {s}")

if warnings:
    print("\n⚠️ UYARILAR:")
    for w in warnings:
        print(f"   {w}")

if issues:
    print("\n❌ SORUNLAR:")
    for i in issues:
        print(f"   {i}")
    
    print("\n" + "="*80)
    print("🔧 ÖNERİLEN ÇÖZÜM ADIMLARI")
    print("="*80 + "\n")
    
    if not is_running:
        print("1️⃣ Uygulamayı başlatın:")
        print("   python app.py")
        print()
    
    if not (query_scheduler.db_manager and query_scheduler.ai_service):
        print("2️⃣ Tarayıcıda http://localhost:5000 açın")
        print("   - Database connection string girin")
        print("   - 'Bağlan' butonuna tıklayın")
        print()
    
    if len(jobs) == 0:
        print("3️⃣ Zamanlanmış sorgu oluşturun:")
        print("   - 'Zamanlanmış Sorgular' sekmesine gidin")
        print("   - Yeni sorgu oluşturun")
        print("   - Schedule type: HOURLY seçin (test için)")
        print()
    
    print("4️⃣ Test edin:")
    print("   python test_scheduler.py")
    print()
    print("5️⃣ Manuel çalıştırın:")
    print("   - Web'den: 'Şimdi Çalıştır' butonu")
    print("   - Terminal'den: python test_scheduler.py <sorgu_id>")
else:
    print("\n" + "="*80)
    print("🎉 HARIKA! TÜM SİSTEMLER ÇALIŞIYOR!")
    print("="*80 + "\n")
    print("Scheduler düzgün çalışıyor ve job'lar zamanlanmış.")
    print()
    print("Test etmek için:")
    print("  • Web arayüzünden 'Şimdi Çalıştır' butonuna tıklayın")
    print("  • Veya: python test_scheduler.py 1")
    print()

print("="*80 + "\n")

# Exit with appropriate code
if issues:
    sys.exit(1)
else:
    sys.exit(0)

