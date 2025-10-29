; SQL Agent Desktop Installer
; NSIS Modern UI Installer Script

!define APP_NAME "SQL Agent Desktop"
!define APP_VERSION "2.0"
!define APP_PUBLISHER "A'im Done Ekibi"
!define APP_URL "https://github.com/cenkergulek/sql-agent"
!define APP_EXECUTABLE "SQLAgent.exe"
!define APP_UNINSTALLER "Uninstall.exe"

; Modern UI
!include "MUI2.nsh"
!include "FileFunc.nsh"

; Installer ayarları
Name "${APP_NAME}"
OutFile "SQLAgent_Setup.exe"
InstallDir "$PROGRAMFILES64\${APP_NAME}"
InstallDirRegKey HKLM "Software\${APP_NAME}" "InstallDir"
RequestExecutionLevel admin

; Modern UI ayarları
!define MUI_ABORTWARNING
; Icon dosyası yok, varsayılan kullan

; Installer sayfaları
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Uninstaller sayfaları
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; Dil
!insertmacro MUI_LANGUAGE "Turkish"

; Installer Sections
Section "Ana Uygulama" SecMain
    SectionIn RO
    
    ; Kurulum dizinini ayarla
    SetOutPath $INSTDIR
    
    ; Ana dosyaları kopyala
    File "dist\${APP_EXECUTABLE}"
    File /nonfatal "dist\README.txt"
    File /nonfatal "dist\sorgularim.txt"
    
    ; Masaüstü kısayolu oluştur
    CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_EXECUTABLE}" "" "$INSTDIR\${APP_EXECUTABLE}" 0
    
    ; Başlat menüsü klasörü oluştur
    CreateDirectory "$SMPROGRAMS\${APP_NAME}"
    CreateShortcut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\${APP_EXECUTABLE}" "" "$INSTDIR\${APP_EXECUTABLE}" 0
    CreateShortcut "$SMPROGRAMS\${APP_NAME}\Kaldır.lnk" "$INSTDIR\${APP_UNINSTALLER}"
    
    ; Registry kayıtları
    WriteRegStr HKLM "Software\${APP_NAME}" "InstallDir" "$INSTDIR"
    WriteRegStr HKLM "Software\${APP_NAME}" "Version" "${APP_VERSION}"
    
    ; Uninstaller oluştur
    WriteUninstaller "$INSTDIR\${APP_UNINSTALLER}"
    
    ; Add/Remove Programs kayıtları
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayName" "${APP_NAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString" "$INSTDIR\${APP_UNINSTALLER}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "InstallLocation" "$INSTDIR"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayIcon" "$INSTDIR\${APP_EXECUTABLE}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "Publisher" "${APP_PUBLISHER}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "URLInfoAbout" "${APP_URL}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayVersion" "${APP_VERSION}"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoRepair" 1
    
    ; Dosya boyutunu hesapla
    ${GetSize} "$INSTDIR" "/S=0K" $0 $1 $2
    IntFmt $0 "0x%08X" $0
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "EstimatedSize" "$0"
SectionEnd

Section "ODBC Driver Kontrolü" SecODBC
    ; ODBC Driver kontrolü
    DetailPrint "Microsoft ODBC Driver kontrol ediliyor..."
    
    ; Registry'de ODBC Driver'ı ara
    ReadRegStr $0 HKLM "SOFTWARE\ODBC\ODBCINST.INI\ODBC Driver 17 for SQL Server" "Driver"
    IfErrors 0 odbc17_found
    
    ReadRegStr $0 HKLM "SOFTWARE\ODBC\ODBCINST.INI\ODBC Driver 18 for SQL Server" "Driver"
    IfErrors 0 odbc18_found
    
    ; ODBC Driver bulunamadı
    MessageBox MB_YESNO|MB_ICONQUESTION "Microsoft ODBC Driver for SQL Server bulunamadı.$\n$\nSQL Agent'ın çalışması için bu driver gereklidir.$\n$\nİndirme sayfasını açmak ister misiniz?" IDNO odbc_skip
    ExecShell "open" "https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server"
    Goto odbc_skip
    
    odbc17_found:
    DetailPrint "ODBC Driver 17 for SQL Server bulundu: $0"
    Goto odbc_done
    
    odbc18_found:
    DetailPrint "ODBC Driver 18 for SQL Server bulundu: $0"
    Goto odbc_done
    
    odbc_skip:
    DetailPrint "ODBC Driver kontrolü atlandı"
    
    odbc_done:
SectionEnd

; Section açıklamaları
LangString DESC_SecMain ${LANG_TURKISH} "SQL Agent Desktop uygulamasının ana dosyaları"
LangString DESC_SecODBC ${LANG_TURKISH} "Microsoft ODBC Driver for SQL Server varlığını kontrol eder"

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
!insertmacro MUI_DESCRIPTION_TEXT ${SecMain} $(DESC_SecMain)
!insertmacro MUI_DESCRIPTION_TEXT ${SecODBC} $(DESC_SecODBC)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

; Uninstaller Section
Section "Uninstall"
    ; Dosyaları sil
    Delete "$INSTDIR\${APP_EXECUTABLE}"
    Delete "$INSTDIR\README.txt"
    Delete "$INSTDIR\sorgularim.txt"
    Delete "$INSTDIR\${APP_UNINSTALLER}"
    
    ; Kısayolları sil
    Delete "$DESKTOP\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\${APP_NAME}\Kaldır.lnk"
    RMDir "$SMPROGRAMS\${APP_NAME}"
    
    ; Registry kayıtlarını sil
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
    DeleteRegKey HKLM "Software\${APP_NAME}"
    
    ; Kurulum dizinini sil
    RMDir "$INSTDIR"
    
    MessageBox MB_OK "${APP_NAME} başarıyla kaldırıldı."
SectionEnd

; Installer fonksiyonları
Function .onInit
    ; Admin yetkisi kontrolü
    UserInfo::GetAccountType
    pop $0
    ${If} $0 != "admin"
        MessageBox MB_ICONSTOP "Bu yükleyici yönetici yetkisi gerektirir!"
        SetErrorLevel 740 ; ERROR_ELEVATION_REQUIRED
        Quit
    ${EndIf}
FunctionEnd
