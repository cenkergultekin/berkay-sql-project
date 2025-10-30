"""
NIQ - Natural Intelligence Query Desktop Application
Native desktop version using PyQt5 WebEngine
"""
import sys
import os
import threading
import time
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMenuBar, QAction, QMessageBox, QSystemTrayIcon, QMenu
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl, QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
import requests
from app import app
from backend.config.config import Config

class NIQDesktopApp(QMainWindow):
    """Main desktop application window"""
    
    def __init__(self):
        super().__init__()
        self.flask_thread = None
        self.flask_running = False
        self.init_ui()
        self.start_flask_server()
        
    def init_ui(self):
        """Initialize the user interface"""
        # Window properties
        self.setWindowTitle("NIQ - Natural Intelligence Query")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Web engine view
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)
        
        # Configure web engine settings
        settings = self.web_view.settings()
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Status bar
        self.statusBar().showMessage("Starting NIQ...")
        
        # Timer to check Flask and load app
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.check_flask_and_load)
        self.check_timer.start(1000)  # Check every second
        
    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('Dosya')
        
        refresh_action = QAction('Yenile', self)
        refresh_action.setShortcut('F5')
        refresh_action.triggered.connect(self.refresh_app)
        file_menu.addAction(refresh_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Çıkış', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu('Görünüm')
        
        fullscreen_action = QAction('Tam Ekran', self)
        fullscreen_action.setShortcut('F11')
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(fullscreen_action)
        
        # Help menu
        help_menu = menubar.addMenu('Yardım')
        
        about_action = QAction('Hakkında', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        dev_tools_action = QAction('Geliştirici Araçları', self)
        dev_tools_action.setShortcut('F12')
        dev_tools_action.triggered.connect(self.toggle_dev_tools)
        help_menu.addAction(dev_tools_action)
        
    def start_flask_server(self):
        """Start Flask server in background thread"""
        def run_flask():
            try:
                print("Starting Flask server...")
                app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False, threaded=True)
            except Exception as e:
                print(f"Flask server error: {e}")
                
        self.flask_thread = threading.Thread(target=run_flask, daemon=True)
        self.flask_thread.start()
        
    def check_flask_and_load(self):
        """Check if Flask is ready and load the application"""
        try:
            response = requests.get('http://127.0.0.1:5000/api/health', timeout=1)
            if response.status_code == 200 and not self.flask_running:
                self.flask_running = True
                self.load_application()
                self.check_timer.stop()
                self.statusBar().showMessage("NIQ hazır - Modern arayüz yüklendi")
        except requests.exceptions.RequestException:
            pass  # Still waiting for Flask to start
            
    def load_application(self):
        """Load the NIQ application in web view"""
        self.web_view.load(QUrl("http://127.0.0.1:5000"))
        
    def refresh_app(self):
        """Refresh the application"""
        self.web_view.reload()
        self.statusBar().showMessage("Uygulama yenilendi", 2000)
        
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
            
    def toggle_dev_tools(self):
        """Toggle developer tools"""
        # Note: PyQt5 WebEngine doesn't have built-in dev tools
        # But we can open browser for development
        import webbrowser
        webbrowser.open('http://127.0.0.1:5000')
        self.statusBar().showMessage("Geliştirici modu tarayıcıda açıldı", 3000)
        
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "NIQ Hakkında", 
                         """
                         <h3>NIQ - Natural Intelligence Query</h3>
                         <p><b>Versiyon:</b> 2.0 Desktop</p>
                         <p><b>Açıklama:</b> Doğal dille SQL sorguları oluşturun</p>
                         <p><b>Özellikler:</b></p>
                         <ul>
                         <li>Modern Poppins font ailesi</li>
                         <li>Profesyonel renk paleti</li>
                         <li>Geometrik icon tasarımı</li>
                         <li>Native masaüstü deneyimi</li>
                         </ul>
                         <p><b>Geliştirici Erişimi:</b> http://127.0.0.1:5000</p>
                         """)
        
    def closeEvent(self, event):
        """Handle application close event"""
        reply = QMessageBox.question(self, 'NIQ Kapat', 
                                   'NIQ uygulamasını kapatmak istediğinizden emin misiniz?',
                                   QMessageBox.Yes | QMessageBox.No, 
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.statusBar().showMessage("NIQ kapatılıyor...")
            event.accept()
        else:
            event.ignore()

def main():
    """Main function for desktop application"""
    # Enable high DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Create application
    app_qt = QApplication(sys.argv)
    app_qt.setApplicationName("NIQ")
    app_qt.setApplicationVersion("2.0")
    app_qt.setOrganizationName("NIQ Team")
    
    # Set application style
    app_qt.setStyle('Fusion')  # Modern look
    
    print("=" * 60)
    print("🚀 NIQ - Natural Intelligence Query Desktop")
    print("=" * 60)
    print("✅ PyQt5 WebEngine başlatılıyor...")
    print("✅ Flask server arka planda çalışacak...")
    print("✅ Modern arayüz yükleniyor...")
    print("🌐 Geliştirici erişimi: http://127.0.0.1:5000")
    print("=" * 60)
    
    # Create and show main window
    window = NIQDesktopApp()
    window.show()
    
    # Run application
    sys.exit(app_qt.exec_())

if __name__ == "__main__":
    main()
