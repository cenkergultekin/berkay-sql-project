@echo off
title NIQ Desktop - Build Creator
color 0A

echo.
echo ================================================================
echo                NIQ Desktop Build Creator
echo ================================================================
echo.

echo [1/3] Temizlik yapiliyor...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo ✅ Eski build dosyalari temizlendi

echo.
echo [2/3] PyInstaller ile NIQ Desktop executable olusturuluyor...
echo 🖥️  Native masaustu uygulamasi olarak build ediliyor...
pyinstaller build-desktop.spec --clean --noconfirm
if %errorlevel% neq 0 (
    echo ❌ PyInstaller hatasi!
    pause
    exit /b 1
)
echo ✅ Desktop executable basariyla olusturuldu

echo.
echo [3/3] Dosya boyutlari kontrol ediliyor...
for %%f in (dist\NIQ-Desktop.exe) do echo    NIQ-Desktop.exe: %%~zf bytes

echo.
echo ================================================================
echo                        TAMAMLANDI!
echo ================================================================
echo.
echo 📦 Dosya:
echo    - dist\NIQ-Desktop.exe    (Native Desktop App)
echo.
echo 🚀 Kullanim:
echo    - Cift tikla: NIQ masaustu uygulamasi acilir
echo    - Gelistirici: http://127.0.0.1:5000 (browser)
echo.
echo ✨ Ozellikler:
echo    - Native PyQt5 WebEngine
echo    - Modern Poppins font
echo    - Profesyonel renk paleti
echo    - Menu bar ve kisa yollar
echo    - Tam ekran modu (F11)
echo    - Gelistirici araclari (F12)
echo.
pause
