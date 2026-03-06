import py_compile
import sys

files = [
    'gavel/settings.py',
    'gavel/__init__.py',
    'gavel/utils.py',
    'gavel/models/item.py',
    'gavel/models/__init__.py',
    'gavel/models/annotator.py',
    'initialize.py',
]

errors = []
for f in files:
    try:
        py_compile.compile(f, doraise=True)
        print(f'OK: {f}')
    except py_compile.PyCompileError as e:
        print(f'ERROR: {f}: {e}')
        errors.append(f)

if errors:
    print(f'\nFAILED: {len(errors)} file(s) have syntax errors')
    sys.exit(1)
else:
    print(f'\nALL {len(files)} FILES SYNTAX OK')
