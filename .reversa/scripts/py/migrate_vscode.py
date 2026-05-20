import os
import shutil
import sys
import subprocess
from pathlib import Path

BACKUP_DIR = 'vscode_backup'
USER_DIR = os.path.join(os.environ['APPDATA'], 'Code', 'User')

FILES_TO_COPY = [
    'settings.json',
    'keybindings.json',
]

SNIPPETS_DIR = 'snippets'
EXTENSIONS_FILE = 'extensions.txt'


def backup():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    # Copy settings and keybindings
    for fname in FILES_TO_COPY:
        src = os.path.join(USER_DIR, fname)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(BACKUP_DIR, fname))
    # Copy snippets
    snippets_src = os.path.join(USER_DIR, SNIPPETS_DIR)
    snippets_dst = os.path.join(BACKUP_DIR, SNIPPETS_DIR)
    if os.path.exists(snippets_src):
        shutil.copytree(snippets_src, snippets_dst, dirs_exist_ok=True)
    # Export extensions
    with open(os.path.join(BACKUP_DIR, EXTENSIONS_FILE), 'w') as f:
        subprocess.run(['code', '--list-extensions'], stdout=f, shell=True)
    print(f'Backup complete. Folder: {BACKUP_DIR}')


def restore():
    # Restore settings and keybindings
    for fname in FILES_TO_COPY:
        src = os.path.join(BACKUP_DIR, fname)
        dst = os.path.join(USER_DIR, fname)
        if os.path.exists(src):
            shutil.copy2(src, dst)
    # Restore snippets
    snippets_src = os.path.join(BACKUP_DIR, SNIPPETS_DIR)
    snippets_dst = os.path.join(USER_DIR, SNIPPETS_DIR)
    if os.path.exists(snippets_src):
        shutil.copytree(snippets_src, snippets_dst, dirs_exist_ok=True)
    # Install extensions
    ext_file = os.path.join(BACKUP_DIR, EXTENSIONS_FILE)
    if os.path.exists(ext_file):
        with open(ext_file) as f:
            for ext in f.read().splitlines():
                subprocess.run(['code', '--install-extension', ext], shell=True)
    print('Restore complete.')


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in {'backup', 'restore'}:
        print('Usage: python migrate_vscode.py [backup|restore]')
        return
    if sys.argv[1] == 'backup':
        backup()
    else:
        restore()


if __name__ == '__main__':
    main()
