# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main_desktop.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('frontend/templates', 'frontend/templates'),
        ('frontend/static', 'frontend/static'),
        ('backend', 'backend'),
        ('.env', '.'),
    ],
    hiddenimports=[
        # Backend modules
        'backend.config.config',
        'backend.models.models',
        'backend.services.database',
        'backend.services.ai_service',
        'backend.routes.routes',
        'backend.core.utils',
        
        # Database & API
        'pyodbc',
        'openai',
        'keyring',
        'requests',
        
        # Flask & web
        'flask',
        'werkzeug',
        'jinja2',
        
        # PyQt5 & WebEngine
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'PyQt5.QtWebEngineWidgets',
        'PyQt5.QtWebEngineCore',
        'PyQt5.sip',
        
        # System modules
        'threading',
        'webbrowser',
        'logging',
        'json',
        'datetime',
        'dataclasses',
        'typing',
        'contextlib',
        'enum',
        'time',
        'sys',
        'os',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary modules to reduce size
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'cv2',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyd = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyd,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NIQ-Desktop',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window for desktop app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one
)
