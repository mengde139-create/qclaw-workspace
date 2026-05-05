import subprocess, os

os.chdir(r'C:\Users\mengdejun\.qclaw\workspace')
g = r'C:\Users\mengdejun\.qclaw\tools\git\cmd\git.exe'

# Add
r = subprocess.run([g, 'add', '-A'], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('Add:', r.returncode)

# Commit
r2 = subprocess.run([g, 'commit', '-m', 'test token push'], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('Commit:', r2.returncode, r2.stderr[:200])

# Push
r3 = subprocess.run([g, 'push', 'origin', 'main'], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=20)
print('Push:', r3.returncode)
print('Stdout:', r3.stdout[:300])
print('Stderr:', r3.stderr[:300])