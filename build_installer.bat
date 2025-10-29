@echo off
title SQL Agent - Build & Installer Creator
color 0A

echo.
echo ================================================================
echo                SQL Agent Build & Installer Creator
echo ================================================================
echo.

echo [1/4] Temizlik yapiliyor...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo ✅ Eski build dosyalari temizlendi

echo.
echo [2/4] PyInstaller ile executable olusturuluyor...
pyinstaller build.spec --clean --noconfirm
if %errorlevel% neq 0 (
    echo ❌ PyInstaller hatasi!
    pause
    exit /b 1
)
echo ✅ Executable basariyla olusturuldu

echo.
echo [3/4] NSIS installer olusturuluyor...
where makensis >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ NSIS bulunamadi!
    echo.
    echo 📥 Lutfen NSIS yukleyin:
    echo    https://nsis.sourceforge.io/Download
    echo.
    echo NSIS kurduktan sonra PATH'e eklemeyi unutmayin!
    pause
    exit /b 1
)

makensis installer.nsi
if %errorlevel% neq 0 (
    echo ❌ NSIS installer olusturma hatasi!
    pause
    exit /b 1
)
echo ✅ Installer basariyla olusturuldu

echo.
echo [4/4] Dosya boyutlari kontrol ediliyor...
for %%f in (dist\SQLAgent.exe) do echo    SQLAgent.exe: %%~zf bytes
for %%f in (SQLAgent_Setup.exe) do echo    SQLAgent_Setup.exe: %%~zf bytes

echo.
echo ================================================================
echo                        TAMAMLANDI!
echo ================================================================
echo.
echo 📦 Dosyalar:
echo    - dist\SQLAgent.exe        (Standalone executable)
echo    - SQLAgent_Setup.exe       (Windows Installer)
echo.
echo 🚀 Kullanim:
echo    - Gelistiriciler: dist\SQLAgent.exe
echo    - Son kullanicilar: SQLAgent_Setup.exe
echo.
echo ✅ Artik projenizi GitHub'a pushleyabilirsiniz!
echo    (dist/ ve build/ klasorleri .gitignore'da)
echo.
pause
