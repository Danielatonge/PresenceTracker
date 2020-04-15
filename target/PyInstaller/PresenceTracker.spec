# -*- mode: python -*-

block_cipher = None


a = Analysis(['/Users/macbookpro/Documents/UserPresence/PresenceTracker/src/main/python/main.py'],
             pathex=['/Users/macbookpro/Documents/UserPresence/PresenceTracker/target/PyInstaller'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['/usr/local/lib/python3.7/site-packages/fbs/freeze/hooks'],
             runtime_hooks=['/var/folders/5p/dtq4v8f51db5xkhqh69xcpw40000gn/T/tmp0uokg8pa/fbs_pyinstaller_hook.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='PresenceTracker',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False , icon='/Users/macbookpro/Documents/UserPresence/PresenceTracker/target/Icon.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='PresenceTracker')
app = BUNDLE(coll,
             name='PresenceTracker.app',
             icon='/Users/macbookpro/Documents/UserPresence/PresenceTracker/target/Icon.icns',
             bundle_identifier=None)
