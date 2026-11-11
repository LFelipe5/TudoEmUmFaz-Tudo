"""Keep local sessions stable and migrate before starting the container command."""
import os
from pathlib import Path
import subprocess
import sys

from django.core.management.utils import get_random_secret_key

if not os.environ.get('DJANGO_SECRET_KEY'):
    key_file = Path('/data/.secret_key')
    try:
        with open(key_file, 'x', opener=lambda path, flags: os.open(path, flags, 0o600)) as key:
            key.write(get_random_secret_key())
    except FileExistsError:
        pass
    os.environ['DJANGO_SECRET_KEY'] = key_file.read_text().strip()

subprocess.run([sys.executable, 'manage.py', 'migrate', '--noinput'], check=True)
os.execvp(sys.argv[1], sys.argv[1:])
