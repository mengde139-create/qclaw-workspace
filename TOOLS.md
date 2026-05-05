# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

### Git

- Path: `C:\Users\mengdejun\.qclaw\tools\git\cmd\git.exe` (MinGit 2.49.0 portable)
- 未加入系统 PATH，需用完整路径调用
- 仓库：`projects/writing-coach-app/` (首次提交 a1798cc)

### Scoop

- 已安装：`~/scoop/`
- Shim 路径：`C:\Users\mengdejun\scoop\shims\`
- 已装：7zip
- Git 安装失败（GitHub 源超时），改用华为镜像手动下载

---

Add whatever helps you do your job. This is your cheat sheet.
