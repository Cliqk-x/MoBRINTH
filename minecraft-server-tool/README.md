# MoBRINTH — Minecraft Server Setup Tool

A beginner-friendly desktop GUI for creating and running Minecraft servers — no terminal required.

## Requirements

- **Windows 10 / 11**
- **Python 3.11+** — https://python.org (tick "Add Python to PATH" during install)
- **Java 17+** — https://adoptium.net (required to actually run the server)

## How to run

**Option A — Double-click (easiest):**
1. Copy the `minecraft-server-tool` folder to your PC
2. Double-click `launch.bat`
3. Dependencies install automatically and the app opens

**Option B — Manual:**
```
pip install -r requirements.txt
python main.py
```

## Features

### Server Setup Tab
| Feature | Status |
|---|---|
| Vanilla / Paper / Purpur server types | ✅ |
| Auto-fetches correct server JAR from official APIs | ✅ |
| RAM slider (1 – 16 GB) with G1GC JVM flags | ✅ |
| Custom server name & output folder | ✅ |
| Online Mode toggle (ON / OFF) | ✅ |

### Automatic Plugin Downloads (during Build)
| Plugin | API Used | Trigger |
|---|---|---|
| **Geyser-Spigot** | GeyserMC API | Enable Crossplay checkbox |
| **Floodgate-Spigot** | GeyserMC API | Enable Crossplay checkbox |
| **ViaVersion** | Hangar (PaperMC) | Multi-Version checkbox |

All plugin versions are resolved at build time — always the latest compatible release.

### Plugin Browser Tab
- Search the **Hangar** plugin hub (PaperMC's official plugin platform)
- Browse featured plugins: EssentialsX, WorldEdit, LuckPerms, ViaVersion, Geyser, ViaBackwards
- **One-click Install** — downloads directly into your server's `/plugins` folder
- Shows download counts and author info per plugin

### Console
- Live server output streamed into the app
- Built-in command terminal with **Up/Down arrow history**
- Stop button sends graceful `stop` to the server

## Supported Minecraft versions

- Latest Release (auto-detected from Mojang API)
- 1.21.1, 1.20.4, 1.19.4

> Paper and Purpur only support versions with an official build.
> Plugins (Geyser, ViaVersion etc.) require Paper or Purpur — not Vanilla.

## Notes

- Server JARs and plugins are cached in your output folder.
  Re-running MoBRINTH for the same server skips already-downloaded files.
- You **must** tick "Accept Mojang EULA" before building.
- Port `25565` (TCP) must be open in Windows Firewall / your router for friends to connect externally.
