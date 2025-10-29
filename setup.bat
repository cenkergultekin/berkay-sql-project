@echo off
title NIQ Desktop - Kurulum Sihirbazi
color 0A

echo.
echo ================================================================
echo                NIQ Desktop - Kurulum Sihirbazi
echo                    Natural Intelligence Query
echo ================================================================
echo.
echo 🚀 NIQ Desktop v3.0 - Modern SQL Sorgu Asistani
echo 💡 Dogal dille SQL sorguları olusturun
echo 🎨 Modern Poppins font ve profesyonel tasarim
echo.
echo ================================================================
echo.

echo [1/4] Kurulum dosyalari kontrol ediliyor...

REM Check if NIQ-Desktop.exe exists in the same directory as this batch file
if not exist "%~dp0NIQ-Desktop.exe" (
    echo ❌ NIQ-Desktop.exe bulunamadi!
    echo 💡 Bu dosya NIQ-Desktop.exe ile ayni klasorde olmali
    echo.
    pause
    exit /b 1
)
echo ✅ NIQ-Desktop.exe bulundu

echo.
echo [2/4] ODBC Driver kontrol ediliyor...
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

echo [3/4] NIQ Desktop kuruluyor...
set "INSTALL_DIR=%PROGRAMFILES%\NIQ Desktop"
set "DESKTOP=%PUBLIC%\Desktop"
set "START_MENU=%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs"
set "SOURCE_FILE=%~dp0NIQ-Desktop.exe"

echo 📁 Kurulum dizini: %INSTALL_DIR%
echo 🖥️  Masaüstü kısayolu: %DESKTOP%\NIQ Desktop.lnk
echo 📋 Başlat menüsü: %START_MENU%\NIQ Desktop.lnk

REM Check for admin rights
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ Yönetici yetkisi gerekli!
    echo 💡 Bu dosyayı "Yönetici olarak çalıştır" ile açın
    echo.
    pause
    exit /b 1
)

REM Create installation directory
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
    if %errorlevel% neq 0 (
        echo ❌ Kurulum dizini oluşturulamadı!
        pause
        exit /b 1
    )
)

REM Copy executable to installation directory
copy "%SOURCE_FILE%" "%INSTALL_DIR%\NIQ-Desktop.exe" >nul
if %errorlevel% neq 0 (
    echo ❌ Dosya kopyalanamadı!
    pause
    exit /b 1
)

REM Set file permissions
icacls "%INSTALL_DIR%" /grant Users:F /T >nul 2>&1

echo ✅ NIQ Desktop başarıyla kuruldu: %INSTALL_DIR%

echo.
echo [4/4] Kısayollar oluşturuluyor...

REM Create desktop shortcut
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\NIQ Desktop.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\NIQ-Desktop.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'NIQ - Natural Intelligence Query Desktop'; $Shortcut.Save()"
if %errorlevel% neq 0 (
    echo ❌ Masaüstü kısayolu oluşturulamadı!
) else (
    echo ✅ Masaüstü kısayolu oluşturuldu
)

REM Create start menu shortcut
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%START_MENU%\NIQ Desktop.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\NIQ-Desktop.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'NIQ - Natural Intelligence Query Desktop'; $Shortcut.Save()"
if %errorlevel% neq 0 (
    echo ❌ Başlat menüsü kısayolu oluşturulamadı!
) else (
    echo ✅ Başlat menüsü kısayolu oluşturuldu
)

REM Add to Windows Registry for Add/Remove Programs
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\NIQ Desktop" /v "DisplayName" /t REG_SZ /d "NIQ Desktop" /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\NIQ Desktop" /v "DisplayVersion" /t REG_SZ /d "3.0" /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\NIQ Desktop" /v "Publisher" /t REG_SZ /d "A'im Done Ekibi" /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\NIQ Desktop" /v "InstallLocation" /t REG_SZ /d "%INSTALL_DIR%" /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\NIQ Desktop" /v "DisplayIcon" /t REG_SZ /d "%INSTALL_DIR%\NIQ-Desktop.exe" /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\NIQ Desktop" /v "UninstallString" /t REG_SZ /d "%INSTALL_DIR%\Uninstall.bat" /f >nul 2>&1

echo ✅ Windows kayıt defterine eklendi

REM Create uninstaller
echo @echo off > "%INSTALL_DIR%\Uninstall.bat"
echo title NIQ Desktop - Kaldirma >> "%INSTALL_DIR%\Uninstall.bat"
echo color 0C >> "%INSTALL_DIR%\Uninstall.bat"
echo. >> "%INSTALL_DIR%\Uninstall.bat"
echo echo ================================================================ >> "%INSTALL_DIR%\Uninstall.bat"
echo echo                NIQ Desktop - Kaldirma >> "%INSTALL_DIR%\Uninstall.bat"
echo echo ================================================================ >> "%INSTALL_DIR%\Uninstall.bat"
echo echo. >> "%INSTALL_DIR%\Uninstall.bat"
echo echo NIQ Desktop kaldiriliyor... >> "%INSTALL_DIR%\Uninstall.bat"
echo echo. >> "%INSTALL_DIR%\Uninstall.bat"
echo del /f /q "%PUBLIC%\Desktop\NIQ Desktop.lnk" ^>nul 2^>^&1 >> "%INSTALL_DIR%\Uninstall.bat"
echo del /f /q "%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs\NIQ Desktop.lnk" ^>nul 2^>^&1 >> "%INSTALL_DIR%\Uninstall.bat"
echo reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\NIQ Desktop" /f ^>nul 2^>^&1 >> "%INSTALL_DIR%\Uninstall.bat"
echo cd /d "%TEMP%" >> "%INSTALL_DIR%\Uninstall.bat"
echo rd /s /q "%INSTALL_DIR%" ^>nul 2^>^&1 >> "%INSTALL_DIR%\Uninstall.bat"
echo echo ✅ NIQ Desktop basariyla kaldirildi! >> "%INSTALL_DIR%\Uninstall.bat"
echo echo. >> "%INSTALL_DIR%\Uninstall.bat"
echo pause >> "%INSTALL_DIR%\Uninstall.bat"

echo ✅ Kaldırma programı oluşturuldu

echo.
echo ================================================================
echo                        KURULUM TAMAMLANDI!
echo ================================================================
echo.
echo ✅ NIQ Desktop başarıyla kuruldu!
echo 📁 Kurulum yeri: %INSTALL_DIR%
echo 🖥️  Masaüstü kısayolu: NIQ Desktop.lnk
echo 📋 Başlat menüsü kısayolu: NIQ Desktop.lnk
echo.
echo 🚀 Kullanım:
echo    - Masaüstündeki "NIQ Desktop" kısayoluna çift tıklayın
echo    - Veya Başlat menüsünden "NIQ Desktop" arayın
echo.
echo 🎨 Özellikler:
echo    - Modern Poppins font ve profesyonel renk paleti
echo    - Native PyQt5 WebEngine masaüstü uygulaması
echo    - Doğal dille SQL sorguları oluşturabilirsiniz
echo    - Dashboard-first yaklaşım ve dinamik hızlı işlemler
echo.
echo 🔧 Kaldırma:
echo    - Denetim Masası ^> Programlar ve Özellikler ^> NIQ Desktop
echo    - Veya: %INSTALL_DIR%\Uninstall.bat
echo.
echo ================================================================
echo          Kurulum tamamlandı! Masaüstü kısayolunu kullanın.
echo ================================================================
echo.
pause
