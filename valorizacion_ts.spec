# valorizacion_ts.spec

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['scripts/workflow.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        # Include all files from input folder and subfolders
        ('input/calificacion/Anexo propuesta asignacion de calificacion 2024-2027.xlsx', 'input/calificacion'),
        ('input/calificacion/calificacion-nacional-1.xlsx', 'input/calificacion'),
        ('input/calificacion/calificacion-nacional-2.xlsx', 'input/calificacion'),
        ('input/familias_objetos.json', 'input'),
        ('input/nup/Anexo N1 Obras de Transmision.xlsx', 'input/nup'),
        ('input/nup/Revision_Literal_C.xlsx', 'input/nup'),
        ('input/parametros.json', 'input'),
        ('input/tipos_elementos_a_cotizar.xlsx', 'input'),
        ('input/README.md', 'input'),
        ('config/settings.py', 'config'),
    ],
    hiddenimports=[
        'numpy',
        'pandas',
        'typing_extensions',
        'sqlalchemy',
        'requests',
        'openpyxl',
        'psutil',
        'psycopg',
        'dropbox',
        'prefect',
        'pymysql',
        'python-dotenv',
        'tqdm',
        'unidecode',
        'xlsxwriter',
        'pyarrow',
        'tabulate',
        # Add imports for modules used in workflow.py
        'prefect.flow',
        'scripts.ci.clean_reports',
        'scripts.load.create_familias_and_objetos',
        'scripts.load.download_data',
        'scripts.load.load_data',
        'scripts.reports.campos_relevantes',
        'scripts.reports.compute_objetos',
        'scripts.reports.export_familias',
        'scripts.reports.export_parametros',
        'scripts.reports.full_dump',
        'scripts.reports.lista_cotizar',
        'scripts.reports.reporte_agregado_calificacion',
        'scripts.reports.reporte_tipo_obras',
        'scripts.reports.tipos_elementos',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='valorizacion-tx',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='valorizacion_tx',
)
