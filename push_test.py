import subprocess, os, sys

os.chdir(r'C:\Users\mengdejun\.qclaw\workspace')
g = r'C:\Users\mengdejun\.qclaw\tools\git\cmd\git.exe'

# Check status
r = subprocess.run([g, 'status', '--porcelain'], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('Changes:', len(r.stdout.splitlines()))
if not r.stdout.strip():
    print('Nothing to commit, exit')
    sys.exit(0)

# Add
r2 = subprocess.run([g, 'add', '-A'], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('Add:', r2.returncode, r2.stderr[:200])

# Commit
r3 = subprocess.run([g, 'commit', '-m', 'auto backup test'], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('Commit:', r3.returncode, r3.stderr[:200])

# Push with verbose
env = os.environ.copy()
env['GIT_TERMINAL_PROMPT'] = '0'
r4 = subprocess.run([g, 'push', '-v', 'origin', 'main'], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=30, env=env)
print('Push RC:', r4.returncode)
print('Stdout:', r4.stdout[:500])
print('Stderr:', r4.stderr[:500])