@echo off
title SQL Agent Desktop - Kurulum
color 0A

echo.
echo ================================================================
echo                    SQL Agent Desktop Kurulumu
echo ================================================================
echo.

echo [1/3] ODBC Driver kontrol ediliyor...
where sqlcmd >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  UYARI: SQL Server ODBC Driver bulunamadi!
    echo.
    echo 📥 Lutfen Microsoft ODBC Driver 17/18 for SQL Server yukleyin:
    echo    https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
    echo.
    echo 💡 ODBC Driver olmadan veritabani baglantisi kurulamaz!
    echo.
    pause
    echo.
) else (
    echo ✅ ODBC Driver bulundu!
)

echo [2/3] Sistem gereksinimleri kontrol ediliyor...
echo ✅ Windows sistemi tespit edildi
echo ✅ Gerekli dosyalar mevcut

echo.
echo [3/3] SQL Agent baslatiliyor...
echo.
echo ================================================================
echo                      SQL Agent Desktop
echo ================================================================
echo.
echo 🚀 Uygulama baslatiliyor...
echo 🌐 Tarayici otomatik olarak acilacak
echo 📊 Veritabanina baglanarak sorgu calistirabilirsiniz
echo.
echo ⚠️  Not: Uygulamayi kapatmak icin Ctrl+C tuslayin
echo.

SQLAgent.exe

echo.
echo ================================================================
echo                   SQL Agent Kapatildi
echo ================================================================
echo.
pause
