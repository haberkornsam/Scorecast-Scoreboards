# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['scoreboard.py'],
             pathex=['/Users/samuelhaberkorn/Desktop/Scorecast Scoreboards/scoreboardAPPv5.2'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.datas += [("basketballScoreboardImage.png", "/Users/samuelhaberkorn/Desktop/Scorecast Scoreboards/scoreboardAPPv5.2/Resources/basketballScoreboardImage.png", "DATA")]
a.datas += [("baseballScoreboardImage.png", "/Users/samuelhaberkorn/Desktop/Scorecast Scoreboards/scoreboardAPPv5.2/Resources/baseballScoreboardImage.png", "DATA")]
a.datas += [("wrestlingScoreboardImage.png", "/Users/samuelhaberkorn/Desktop/Scorecast Scoreboards/scoreboardAPPv5.2/Resources/wrestlingScoreboardImage.png", "DATA")]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='scoreboard',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Scorecast v5.2')
app = BUNDLE(coll,
             name='Scorecast.app',
             icon="/Users/samuelhaberkorn/Desktop/Scorecast Scoreboards/Scorecast Logos/macAppIcon.icns",
             bundle_identifier=None,
             info_plist={
                 'NSHighResolutionCapable': 'True'
                }
)
