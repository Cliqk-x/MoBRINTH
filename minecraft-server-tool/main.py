"""
MoBRINTH — Minecraft Server Setup Tool
Simplified beginner-friendly GUI. PyQt6, no tkinter.
"""

import sys
import subprocess
import threading
from pathlib import Path

import requests
import json
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject, QTimer
from PyQt6.QtGui import QFont, QTextCursor, QIcon
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox,
    QSlider, QSpinBox, QTextEdit, QProgressBar, QTabWidget, QScrollArea,
    QFileDialog, QMessageBox, QFrame, QSizePolicy, QSplitter, QDialog,
    QDialogButtonBox,
)

# ─────────────────────────────────────────────────────────────────────────────
# PALETTE
# ─────────────────────────────────────────────────────────────────────────────
BG      = "#1c2033"
PANEL   = "#252a40"
CARD    = "#2e3450"
INPUT   = "#363d58"
TEXT    = "#e2e8f0"
MUTED   = "#94a3b8"
BORDER  = "#404868"
BLUE    = "#6ea8fe"
GREEN   = "#4ade80"
RED     = "#f87171"
YELLOW  = "#fbbf24"
ORANGE  = "#fb923c"
PURPLE  = "#c084fc"
EULA_URL = "https://www.minecraft.net/en-us/eula"

MC_VERSIONS  = ["Latest Release", "1.21.4", "1.21.1", "1.20.4", "1.19.4", "1.18.2", "1.17.1", "1.16.5"]
SERVER_TYPES = ["Paper  (Recommended)", "Purpur", "Vanilla"]

FEATURED_PLUGINS = [
    ("EssentialsX",  "EssentialsX",  "Homes, warps, economy, chat — the essential starter pack."),
    ("enginehub",    "WorldEdit",    "Build and edit your world with powerful commands."),
    ("LuckPerms",    "LuckPerms",    "Give players ranks and control what they can do."),
    ("ViaVersion",   "ViaVersion",   "Let different Minecraft versions join your server."),
    ("GeyserMC",     "Geyser-Spigot","Let Bedrock/mobile/console players join your Java server."),
    ("ViaVersion",   "ViaBackwards", "Let older Minecraft clients connect — pairs with ViaVersion."),
]

PAPER_API  = "https://api.papermc.io/v2/projects/paper"
PURPUR_API = "https://api.purpurmc.org/v2/purpur"
GEYSER_API = "https://download.geysermc.org/v2/projects"
HANGAR_API = "https://hangar.papermc.io/api/v1"
MOJANG_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
HEADERS    = {"User-Agent": "MoBRINTH/2.0"}

# ─────────────────────────────────────────────────────────────────────────────
# STYLE
# ─────────────────────────────────────────────────────────────────────────────
STYLE = f"""
* {{ font-family: 'Segoe UI', Arial; }}
QMainWindow, QWidget {{ background: {BG}; color: {TEXT}; font-size: 13px; }}

QTabWidget::pane {{
    border: 1px solid {BORDER};
    border-radius: 10px;
    background: {PANEL};
    margin-top: -1px;
}}
QTabBar::tab {{
    background: {CARD};
    color: {MUTED};
    padding: 9px 24px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    margin-right: 3px;
    font-size: 13px;
}}
QTabBar::tab:selected {{ background: {BLUE}; color: #0f1629; font-weight: bold; }}
QTabBar::tab:hover:!selected {{ background: {BORDER}; color: {TEXT}; }}

QLineEdit {{
    background: {INPUT};
    border: 1.5px solid {BORDER};
    border-radius: 8px;
    padding: 6px 10px;
    color: {TEXT};
    font-size: 13px;
}}
QLineEdit:focus {{ border-color: {BLUE}; }}
QLineEdit:disabled {{ color: {MUTED}; background: {CARD}; border-color: {CARD}; }}

QSpinBox {{
    background: {INPUT};
    border: 1.5px solid {BORDER};
    border-radius: 8px;
    padding: 6px 8px;
    color: {TEXT};
    font-size: 13px;
    min-width: 58px;
}}
QSpinBox:focus {{ border-color: {BLUE}; }}
QSpinBox::up-button, QSpinBox::down-button {{
    width: 18px;
    border: none;
    background: {BORDER};
    border-radius: 4px;
}}
QSpinBox::up-button:hover, QSpinBox::down-button:hover {{ background: {BLUE}; }}

QComboBox {{
    background: {INPUT};
    border: 1.5px solid {BORDER};
    border-radius: 8px;
    padding: 6px 10px;
    color: {TEXT};
    font-size: 13px;
}}
QComboBox::drop-down {{ border: none; width: 26px; }}
QComboBox QAbstractItemView {{
    background: {PANEL};
    border: 1px solid {BORDER};
    selection-background-color: {BLUE};
    selection-color: #0f1629;
    outline: none;
    padding: 4px;
}}

QCheckBox {{ spacing: 8px; font-size: 13px; color: {TEXT}; }}
QCheckBox::indicator {{
    width: 18px; height: 18px;
    border-radius: 5px;
    border: 1.5px solid {BORDER};
    background: {INPUT};
}}
QCheckBox::indicator:checked {{ background: {BLUE}; border-color: {BLUE}; }}
QCheckBox::indicator:hover {{ border-color: {BLUE}; }}
QCheckBox:disabled {{ color: {MUTED}; }}
QCheckBox::indicator:disabled {{ background: {CARD}; border-color: {CARD}; }}

QSlider::groove:horizontal {{
    height: 6px; background: {BORDER}; border-radius: 3px;
}}
QSlider::sub-page:horizontal {{ background: {BLUE}; border-radius: 3px; }}
QSlider::handle:horizontal {{
    background: {BLUE};
    width: 18px; height: 18px;
    margin: -6px 0; border-radius: 9px;
    border: 2px solid {BG};
}}
QSlider:disabled::groove:horizontal {{ background: {CARD}; }}
QSlider:disabled::sub-page:horizontal {{ background: {BORDER}; }}
QSlider:disabled::handle:horizontal {{ background: {BORDER}; }}

QTextEdit {{
    background: #141824;
    border: 1px solid {BORDER};
    border-radius: 8px;
    color: #7dd3fc;
    font-family: Consolas, monospace;
    font-size: 11.5px;
    padding: 8px;
}}

QProgressBar {{
    background: {BORDER};
    border-radius: 5px;
    max-height: 8px;
    text-align: center;
    border: none;
}}
QProgressBar::chunk {{ background: {BLUE}; border-radius: 5px; }}

QScrollArea {{ border: none; background: transparent; }}
QScrollBar:vertical {{
    background: {CARD}; width: 8px; border-radius: 4px; border: none;
}}
QScrollBar::handle:vertical {{
    background: {BORDER}; border-radius: 4px; min-height: 24px;
}}
QScrollBar::handle:vertical:hover {{ background: {BLUE}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{ height: 0; }}

QFrame#card {{
    background: {CARD};
    border-radius: 10px;
    border: 1px solid {BORDER};
}}
"""

# ─────────────────────────────────────────────────────────────────────────────
# WIDGET HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def _mix(a, b, t=0.5):
    ah, bh = a.lstrip("#"), b.lstrip("#")
    ar, ag, ab_ = int(ah[0:2],16), int(ah[2:4],16), int(ah[4:6],16)
    br, bg_, bb = int(bh[0:2],16), int(bh[2:4],16), int(bh[4:6],16)
    return "#{:02x}{:02x}{:02x}".format(
        int(ar+(br-ar)*t), int(ag+(bg_-ag)*t), int(ab_+(bb-ab_)*t))


def _btn(text, bg=BLUE, fg="#0f1629", w=None, h=38):
    b = QPushButton(text)
    light = _mix(bg, "#ffffff", 0.18)
    b.setStyleSheet(f"""
        QPushButton {{
            background:{bg}; color:{fg};
            border:none; border-radius:8px;
            padding:5px 18px; font-weight:600; font-size:13px;
        }}
        QPushButton:hover {{ background:{light}; }}
        QPushButton:pressed {{ background:{bg}; }}
        QPushButton:disabled {{ background:{BORDER}; color:{MUTED}; }}
    """)
    if w: b.setFixedWidth(w)
    if h: b.setFixedHeight(h)
    return b


def _ghost(text, w=None, h=32):
    b = QPushButton(text)
    b.setStyleSheet(f"""
        QPushButton {{
            background:{CARD}; color:{MUTED};
            border:1px solid {BORDER}; border-radius:8px;
            padding:4px 14px; font-size:12px;
        }}
        QPushButton:hover {{ background:{BORDER}; color:{TEXT}; }}
        QPushButton:disabled {{ background:{PANEL}; color:{BORDER}; }}
    """)
    if w: b.setFixedWidth(w)
    if h: b.setFixedHeight(h)
    return b


def _lbl(text, color=TEXT, bold=False, size=13, wrap=False):
    l = QLabel(text)
    l.setStyleSheet(
        f"color:{color}; font-size:{size}px; "
        f"{'font-weight:bold;' if bold else ''} background:transparent;")
    if wrap:
        l.setWordWrap(True)
    return l


def _sep():
    l = QFrame()
    l.setFrameShape(QFrame.Shape.HLine)
    l.setStyleSheet(f"background:{BORDER}; max-height:1px; border:none;")
    l.setFixedHeight(1)
    return l


# ─────────────────────────────────────────────────────────────────────────────
# API / DOWNLOAD
# ─────────────────────────────────────────────────────────────────────────────
def _get(url, timeout=12):
    try:
        r = requests.get(url, timeout=timeout, headers=HEADERS)
        r.raise_for_status(); return r.json()
    except Exception: return None

def _text(url, timeout=12):
    try:
        r = requests.get(url, timeout=timeout, headers=HEADERS)
        r.raise_for_status(); return r.text.strip()
    except Exception: return None

def latest_mc():
    d = _get(MOJANG_URL)
    return d["latest"]["release"] if d else None

def vanilla_url(ver):
    d = _get(MOJANG_URL)
    if not d: return None
    for e in d.get("versions", []):
        if e["id"] == ver:
            m = _get(e["url"])
            return m["downloads"]["server"]["url"] if m else None
    return None

def paper_url(ver):
    d = _get(f"{PAPER_API}/versions/{ver}")
    if not d: return None
    builds = d.get("builds", [])
    if not builds: return None
    lb = builds[-1]
    b = _get(f"{PAPER_API}/versions/{ver}/builds/{lb}")
    if not b: return None
    name = b["downloads"]["application"]["name"]
    return f"{PAPER_API}/versions/{ver}/builds/{lb}/downloads/{name}"

def purpur_url(ver):
    d = _get(f"{PURPUR_API}/{ver}")
    if not d: return None
    lb = d.get("builds", {}).get("latest")
    return f"{PURPUR_API}/{ver}/{lb}/download" if lb else None

def geyser_dl_url():
    vd = _get(f"{GEYSER_API}/geyser/versions/latest")
    if not vd: return None
    v = vd.get("version")
    bd = _get(f"{GEYSER_API}/geyser/versions/{v}/builds/latest")
    if not bd: return None
    build = bd.get("build")
    dl = bd.get("downloads", {})
    fl = "spigot" if "spigot" in dl else next(iter(dl), None)
    return f"{GEYSER_API}/geyser/versions/{v}/builds/{build}/downloads/{fl}" if fl else None

def floodgate_dl_url():
    vd = _get(f"{GEYSER_API}/floodgate/versions/latest")
    if not vd: return None
    v = vd.get("version")
    bd = _get(f"{GEYSER_API}/floodgate/versions/{v}/builds/latest")
    if not bd: return None
    build = bd.get("build")
    dl = bd.get("downloads", {})
    fl = "spigot" if "spigot" in dl else next(iter(dl), None)
    return f"{GEYSER_API}/floodgate/versions/{v}/builds/{build}/downloads/{fl}" if fl else None

def hangar_latest(owner, slug):
    return _text(f"{HANGAR_API}/projects/{owner}/{slug}/latestrelease")

def hangar_dl(owner, slug, version):
    return f"{HANGAR_API}/projects/{owner}/{slug}/versions/{version}/PAPER/download"

def hangar_search(q, limit=12):
    url = f"{HANGAR_API}/projects?q={requests.utils.quote(q)}&limit={limit}&platform=PAPER"
    d = _get(url)
    return d.get("result", []) if d else []

def download_file(url, dest: Path, progress_cb=None):
    try:
        with requests.get(url, stream=True, timeout=120,
                          headers=HEADERS, allow_redirects=True) as r:
            r.raise_for_status()
            total = int(r.headers.get("content-length", 0))
            done = 0
            with open(dest, "wb") as f:
                for chunk in r.iter_content(65536):
                    f.write(chunk); done += len(chunk)
                    if progress_cb and total:
                        progress_cb(done, total)
        return True
    except Exception:
        if dest.exists(): dest.unlink()
        return False


# ─────────────────────────────────────────────────────────────────────────────
# BUILD WORKER
# ─────────────────────────────────────────────────────────────────────────────
class BuildWorker(QObject):
    log      = pyqtSignal(str)
    status   = pyqtSignal(str)
    progress = pyqtSignal(int)
    launched = pyqtSignal()
    done     = pyqtSignal(bool)
    error    = pyqtSignal(str)

    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self._proc = None

    def get_proc(self): return self._proc

    def run(self):
        c = self.cfg
        stype  = c["server_type"]
        mcver  = c["mc_version"]
        name   = c["server_name"]
        ram    = c["ram_gb"]
        outdir = Path(c["output_dir"])
        cross  = c["crossplay"]
        multi  = c["multiversion"]     # ViaVersion + ViaBackwards only
        allcli = c["all_clients"]      # ViaVersion + ViaBackwards + ViaRewind
        online = "true" if c["online_mode"] else "false"

        L = self.log.emit
        S = self.status.emit
        P = self.progress.emit
        has_plugins = stype in ("Paper", "Purpur")

        try:
            L("══════════════════════════════════")
            L(f"  MoBRINTH  |  {name}")
            L(f"  {stype}  ·  {ram} GB RAM")
            L("══════════════════════════════════")

            # Resolve MC version
            S("Fetching Minecraft version info…"); P(5)
            if mcver == "Latest Release":
                L("[→] Checking latest Minecraft release…")
                mcver = latest_mc()
                if not mcver:
                    raise RuntimeError("Cannot reach Mojang API. Check your internet.")
                L(f"[✓] Latest release: {mcver}")

            # Resolve server JAR
            S(f"Finding {stype} download…"); P(12)
            L(f"[→] Fetching {stype} JAR for {mcver}…")
            jar_url = (vanilla_url(mcver) if stype == "Vanilla"
                       else paper_url(mcver) if stype == "Paper"
                       else purpur_url(mcver))
            if not jar_url:
                raise RuntimeError(
                    f"No {stype} build found for Minecraft {mcver}.\n"
                    "Try a different version or server type.")
            L("[✓] Server download link found.")

            # Build plugin list
            plugin_jobs = []

            if cross and has_plugins:
                S("Fetching Bedrock support plugins…"); P(16)
                L("[→] Fetching Geyser…")
                gu = geyser_dl_url()
                L("[→] Fetching Floodgate…")
                fu = floodgate_dl_url()
                if gu: plugin_jobs.append(("Geyser-Spigot",    gu, "Geyser-Spigot.jar"))
                if fu: plugin_jobs.append(("Floodgate-Spigot", fu, "Floodgate-Spigot.jar"))
                L(f"[{'✓' if gu else '!'}] Geyser  [{'✓' if fu else '!'}] Floodgate")

            # All-clients mode installs ViaVersion + ViaBackwards + ViaRewind
            # Normal multi-version installs ViaVersion + ViaBackwards only
            via_slugs = []
            if (allcli or multi) and has_plugins:
                via_slugs = ["ViaVersion", "ViaBackwards"]
                if allcli:
                    via_slugs.append("ViaRewind")   # adds 1.7/1.8 support
                label_str = "ViaVersion + ViaBackwards" + (" + ViaRewind" if allcli else "")
                S(f"Fetching {label_str}…"); P(20)
                for slug in via_slugs:
                    L(f"[→] Fetching {slug} from Hangar…")
                    ver = hangar_latest("ViaVersion", slug)
                    if ver:
                        plugin_jobs.append((slug, hangar_dl("ViaVersion", slug, ver),
                                            f"{slug}-{ver}.jar"))
                        L(f"[✓] {slug} {ver}")
                    else:
                        L(f"[!] {slug} not found — skipping.")

            if (cross or multi or allcli) and not has_plugins:
                L("[i] Plugins need Paper or Purpur. Vanilla skips plugins.")

            # Create folders
            safe = "".join(ch if ch.isalnum() or ch in " _-" else "_" for ch in name)
            sdir = outdir / safe
            sdir.mkdir(parents=True, exist_ok=True)
            pdir = sdir / "plugins"
            pdir.mkdir(exist_ok=True)
            L(f"[✓] Server folder: {sdir}"); P(26)

            # Download server JAR
            jar_path = sdir / "server.jar"
            if jar_path.exists():
                L("[✓] server.jar already downloaded — skipping."); P(64)
            else:
                S("Downloading server JAR…")
                L("[↓] Downloading server.jar…")
                def jp(done, total):
                    P(int(26 + done/total*38))
                    S(f"Downloading JAR… {done/1_048_576:.1f}/{total/1_048_576:.1f} MB")
                if not download_file(jar_url, jar_path, jp):
                    raise RuntimeError("Server JAR download failed. Check your internet.")
                L(f"[✓] server.jar ready ({jar_path.stat().st_size/1_048_576:.1f} MB)")
                P(64)

            # Download plugins
            for i, (pname, purl, pfile) in enumerate(plugin_jobs):
                pdest = pdir / pfile
                if pdest.exists():
                    L(f"[✓] {pname} cached — skipping."); continue
                S(f"Downloading {pname}…")
                L(f"[↓] Downloading {pname}…")
                def pp(done, total, n=pname):
                    S(f"Downloading {n}… {done/1_048_576:.1f}/{total/1_048_576:.1f} MB")
                ok = download_file(purl, pdest, pp)
                L(f"[{'✓' if ok else '!'}] {pname} {'ready' if ok else 'FAILED (continuing)'}")
            P(82)

            # Write config
            S("Writing config…")
            (sdir / "eula.txt").write_text("eula=true\n")
            props = sdir / "server.properties"
            if not props.exists():
                props.write_text(
                    f"server-name={name}\n"
                    "motd=\\u00A7aPowered by MoBRINTH!\n"
                    f"online-mode={online}\nmax-players=20\n"
                    "difficulty=easy\ngamemode=survival\npvp=true\nserver-port=25565\n")
            L(f"[✓] Config written  (online-mode={online})"); P(90)

            # Launch
            S("Launching server…"); P(96)
            L(f"\n[▶] Starting {stype} {mcver} — {ram} GB RAM…")
            L("[i] Type 'stop' in the terminal below to shut down.\n")
            cmd = ["java", f"-Xms{ram}G", f"-Xmx{ram}G",
                   "-XX:+UseG1GC", "-jar", "server.jar", "--nogui"]
            try:
                self._proc = subprocess.Popen(
                    cmd, cwd=str(sdir),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT, text=True,
                    creationflags=(subprocess.CREATE_NO_WINDOW
                                   if sys.platform == "win32" else 0))
            except FileNotFoundError:
                raise RuntimeError(
                    "Java not found.\n\n"
                    "Install Java 17+ from: https://adoptium.net\n"
                    "Then re-run MoBRINTH.")

            P(100); self.launched.emit()
            S(f"Running — {name}")
            for line in self._proc.stdout:
                L(line.rstrip())
            self._proc.wait()
            L(f"\n[■] Server stopped (exit {self._proc.returncode}).")
            self.done.emit(True)

        except RuntimeError as e:
            L(f"\n[ERROR] {e}")
            self.error.emit(str(e)); self.done.emit(False)
        except Exception as e:
            L(f"\n[CRASH] {e}")
            self.error.emit(str(e)); self.done.emit(False)


# ─────────────────────────────────────────────────────────────────────────────
# PLUGIN INSTALL WORKER
# ─────────────────────────────────────────────────────────────────────────────
class PluginWorker(QObject):
    status_sig = pyqtSignal(str, str)
    log_sig    = pyqtSignal(str)
    done_sig   = pyqtSignal(bool, str)

    def __init__(self, owner, slug, server_dir: Path):
        super().__init__()
        self.owner = owner; self.slug = slug; self.sdir = server_dir

    def run(self):
        self.status_sig.emit("Resolving…", YELLOW)
        ver = hangar_latest(self.owner, self.slug)
        if not ver:
            self.status_sig.emit("Not found", RED)
            self.log_sig.emit(f"[!] Could not find {self.slug} on Hangar.")
            self.done_sig.emit(False, "Install"); return
        url  = hangar_dl(self.owner, self.slug, ver)
        dest = self.sdir / "plugins" / f"{self.slug}-{ver}.jar"
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            self.status_sig.emit(f"✓ {ver}", GREEN)
            self.log_sig.emit(f"[✓] {self.slug} {ver} already installed.")
            self.done_sig.emit(True, "✓ Done"); return
        self.status_sig.emit("Downloading…", YELLOW)
        self.log_sig.emit(f"[↓] Downloading {self.slug} {ver}…")
        ok = download_file(url, dest)
        if ok:
            self.status_sig.emit(f"✓ {ver}", GREEN)
            self.log_sig.emit(f"[✓] {self.slug} {ver} installed.")
            self.done_sig.emit(True, "✓ Done")
        else:
            self.status_sig.emit("Failed", RED)
            self.log_sig.emit(f"[!] Failed to download {self.slug}.")
            self.done_sig.emit(False, "Retry")


# ─────────────────────────────────────────────────────────────────────────────
# LAUNCH WORKER  — starts an already-built server directory
# ─────────────────────────────────────────────────────────────────────────────
class LaunchWorker(QObject):
    log      = pyqtSignal(str)
    status   = pyqtSignal(str)
    launched = pyqtSignal()
    done     = pyqtSignal()

    def __init__(self, server_dir: Path, ram_gb: int):
        super().__init__()
        self._dir = server_dir
        self._ram = ram_gb
        self._proc = None

    def get_proc(self): return self._proc

    def run(self):
        L = self.log.emit
        jar = self._dir / "server.jar"
        if not jar.exists():
            L(f"[ERROR] server.jar not found in {self._dir}")
            self.done.emit(); return

        # Read server name from properties if available
        name = self._dir.name
        props = self._dir / "server.properties"
        if props.exists():
            for line in props.read_text(errors="ignore").splitlines():
                if line.startswith("server-name="):
                    name = line.split("=", 1)[1].strip() or name
                    break

        L("══════════════════════════════════")
        L(f"  MoBRINTH  |  {name}")
        L(f"  Launching from: {self._dir.name}")
        L(f"  RAM: {self._ram} GB")
        L("══════════════════════════════════")
        self.status.emit(f"Launching {name}…")

        cmd = ["java", f"-Xms{self._ram}G", f"-Xmx{self._ram}G",
               "-XX:+UseG1GC", "-jar", "server.jar", "--nogui"]
        try:
            self._proc = subprocess.Popen(
                cmd, cwd=str(self._dir),
                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, text=True,
                creationflags=(subprocess.CREATE_NO_WINDOW
                               if sys.platform == "win32" else 0))
        except FileNotFoundError:
            L("[ERROR] Java not found.\nInstall Java 17+ from: https://adoptium.net")
            self.done.emit(); return

        self.launched.emit()
        self.status.emit(f"Running — {name}")
        for line in self._proc.stdout:
            L(line.rstrip())
        self._proc.wait()
        L(f"\n[■] Server stopped (exit {self._proc.returncode}).")
        self.done.emit()


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def _get_local_ip() -> str:
    """Best-effort local LAN IP (falls back to 127.0.0.1)."""
    try:
        import socket as _s
        sock = _s.socket(_s.AF_INET, _s.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        sock.close()
        return ip
    except Exception:
        return "127.0.0.1"


def scan_servers(root: Path) -> list[dict]:
    """Return info dicts for every MoBRINTH server found under root."""
    servers = []
    if not root.is_dir():
        return servers
    for d in sorted(root.iterdir()):
        if not d.is_dir(): continue
        if not (d / "server.jar").exists(): continue
        if not (d / "eula.txt").exists(): continue
        info = {"path": d, "name": d.name, "port": "25565",
                "online": "true", "players": "20", "plugins": 0,
                "bedrock": False, "bedrock_port": "19132"}
        props = d / "server.properties"
        if props.exists():
            for line in props.read_text(errors="ignore").splitlines():
                k, _, v = line.partition("=")
                k = k.strip(); v = v.strip()
                if k == "server-name" and v: info["name"] = v
                elif k == "server-port":    info["port"] = v
                elif k == "online-mode":    info["online"] = v
                elif k == "max-players":    info["players"] = v
        pdir = d / "plugins"
        if pdir.is_dir():
            jars = list(pdir.glob("*.jar"))
            info["plugins"] = len(jars)
            # Detect Geyser (Bedrock crossplay)
            geyser = [j for j in jars if j.name.lower().startswith("geyser")]
            if geyser:
                info["bedrock"] = True
                # Try reading port from Geyser config (default 19132)
                gcfg = pdir / "Geyser-Spigot" / "config.yml"
                if not gcfg.exists():
                    gcfg = pdir / "Geyser-Paper" / "config.yml"
                if gcfg.exists():
                    in_bedrock = False
                    for line in gcfg.read_text(errors="ignore").splitlines():
                        if line.strip().startswith("bedrock:"):
                            in_bedrock = True
                        elif in_bedrock and "port:" in line:
                            try:
                                info["bedrock_port"] = line.split("port:")[1].strip().split()[0]
                            except Exception:
                                pass
                            break
                        elif in_bedrock and line and not line.startswith(" "):
                            break
        servers.append(info)
    return servers


# ─────────────────────────────────────────────────────────────────────────────
# MAIN WINDOW
# ─────────────────────────────────────────────────────────────────────────────
class MoBRINTH(QMainWindow):
    _log_sig = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MoBRINTH — Minecraft Server Setup")
        self.resize(980, 900)
        self.setMinimumSize(880, 780)

        self._build_thread = self._build_worker = None
        self._active_sdir: Path | None = None
        self._cmd_hist: list[str] = []
        self._cmd_idx = -1
        self._install_threads = []
        self._pending_search = None
        self._log_first = True       # used to clear watermark on first log

        self._log_sig.connect(self._do_log)

        root = QWidget(); self.setCentralWidget(root)
        lay  = QVBoxLayout(root)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        lay.addWidget(self._make_header())

        body = QWidget()
        bl   = QVBoxLayout(body)
        bl.setContentsMargins(16, 12, 16, 4)
        bl.setSpacing(0)

        self._tabs = QTabWidget()

        t1 = QWidget(); self._tabs.addTab(t1, "🖥  Setup")
        t2 = QWidget(); self._tabs.addTab(t2, "🔌  Plugins")
        t3 = QWidget(); self._tabs.addTab(t3, "📂  My Servers")
        self._build_setup_tab(t1)
        self._build_plugin_tab(t2)
        self._build_myservers_tab(t3)

        # Splitter — drag the divider to resize tabs vs console
        self._splitter = QSplitter(Qt.Orientation.Vertical)
        self._splitter.setStyleSheet(f"""
            QSplitter::handle {{
                background: {BORDER};
                height: 5px;
                border-radius: 2px;
                margin: 2px 20px;
            }}
            QSplitter::handle:hover {{
                background: {BLUE};
            }}
        """)
        self._splitter.addWidget(self._tabs)
        self._splitter.addWidget(self._make_console())
        self._splitter.setSizes([380, 420])
        self._splitter.setChildrenCollapsible(False)
        bl.addWidget(self._splitter, stretch=1)
        lay.addWidget(body)
        lay.addWidget(self._make_footer())

        threading.Thread(target=self._startup, daemon=True).start()

    # ── Footer ────────────────────────────────────────────────────────────────
    def _make_footer(self):
        w = QWidget()
        w.setFixedHeight(26)
        w.setStyleSheet(
            f"background:{PANEL}; border-top:1px solid {BORDER};")
        h = QHBoxLayout(w)
        h.setContentsMargins(16, 0, 16, 0)
        h.addStretch()
        wm = QLabel("⛏ MoBRINTH  ·  by <b>Legendary OM</b>")
        wm.setStyleSheet(
            f"color:{BORDER}; font-size:11px; background:transparent; letter-spacing:0.5px;")
        h.addWidget(wm)
        h.addStretch()
        return w

    # ── Header ────────────────────────────────────────────────────────────────
    def _make_header(self):
        w = QWidget()
        w.setFixedHeight(56)
        w.setStyleSheet(
            f"background: qlineargradient(x1:0,y1:0,x2:1,y2:0,"
            f"stop:0 {PANEL}, stop:1 {CARD});"
            f"border-bottom:1px solid {BORDER};")
        h = QHBoxLayout(w)
        h.setContentsMargins(20, 0, 20, 0); h.setSpacing(0)
        h.addWidget(_lbl("⛏  ", color=BLUE, bold=True, size=20))
        h.addWidget(_lbl("MoBRINTH", color=TEXT, bold=True, size=18))
        h.addWidget(_lbl("   Minecraft Server Setup Tool", color=MUTED, size=12))
        h.addStretch()
        h.addWidget(_lbl("v2.0", color=MUTED, size=11))
        return w

    # ── Setup Tab ─────────────────────────────────────────────────────────────
    def _build_setup_tab(self, parent):
        # Wrap in a scroll area so nothing ever overlaps on small windows
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        inner = QWidget()
        inner.setStyleSheet(f"background: {PANEL};")
        lay = QVBoxLayout(inner)
        lay.setContentsMargins(14, 12, 14, 14)
        lay.setSpacing(10)

        # ── Row 1: Server name + MC version ──────────────────────────────
        r1 = QHBoxLayout(); r1.setSpacing(12)

        nc = QVBoxLayout(); nc.setSpacing(4)
        nc.addWidget(_lbl("Server Name", color=MUTED, size=11))
        self._name = QLineEdit("My MoBRINTH Server")
        self._name.setFixedHeight(36)
        nc.addWidget(self._name)
        r1.addLayout(nc, stretch=3)

        vc = QVBoxLayout(); vc.setSpacing(4)
        vc.addWidget(_lbl("Minecraft Version", color=MUTED, size=11))
        self._ver = QComboBox(); self._ver.addItems(MC_VERSIONS)
        self._ver.setFixedHeight(36)
        vc.addWidget(self._ver)
        r1.addLayout(vc, stretch=2)

        lay.addLayout(r1)

        # ── Row 2: Server type + RAM ──────────────────────────────────────
        r2 = QHBoxLayout(); r2.setSpacing(12)

        sc = QVBoxLayout(); sc.setSpacing(4)
        sc.addWidget(_lbl("Server Type", color=MUTED, size=11))
        self._stype = QComboBox(); self._stype.addItems(SERVER_TYPES)
        self._stype.setFixedHeight(36)
        self._stype.currentTextChanged.connect(self._on_type_change)
        sc.addWidget(self._stype)
        r2.addLayout(sc, stretch=2)

        rc = QVBoxLayout(); rc.setSpacing(4)
        rc.addWidget(_lbl("RAM Allocation (GB)", color=MUTED, size=11))

        ram_row = QHBoxLayout(); ram_row.setSpacing(8)
        self._ram_slider = QSlider(Qt.Orientation.Horizontal)
        self._ram_slider.setRange(1, 32)
        self._ram_slider.setValue(2)
        self._ram_slider.setFixedHeight(36)

        self._ram_spin = QSpinBox()
        self._ram_spin.setRange(1, 32)
        self._ram_spin.setValue(2)
        self._ram_spin.setSuffix(" GB")
        self._ram_spin.setFixedHeight(36)
        self._ram_spin.setFixedWidth(72)

        # Keep slider and spinbox in sync
        self._ram_slider.valueChanged.connect(
            lambda v: self._ram_spin.blockSignals(True) or
                      self._ram_spin.setValue(v) or
                      self._ram_spin.blockSignals(False))
        self._ram_spin.valueChanged.connect(
            lambda v: self._ram_slider.blockSignals(True) or
                      self._ram_slider.setValue(v) or
                      self._ram_slider.blockSignals(False))

        ram_row.addWidget(self._ram_slider, stretch=1)
        ram_row.addWidget(self._ram_spin)
        rc.addLayout(ram_row)
        r2.addLayout(rc, stretch=3)

        lay.addLayout(r2)

        # ── Output folder ─────────────────────────────────────────────────
        fc = QVBoxLayout(); fc.setSpacing(4)
        fc.addWidget(_lbl("Save server to", color=MUTED, size=11))
        fr = QHBoxLayout(); fr.setSpacing(8)
        self._folder = QLineEdit(str(Path.home() / "MinecraftServers"))
        self._folder.setFixedHeight(36)
        br = _ghost("Browse", w=80, h=36)
        br.clicked.connect(self._browse)
        fr.addWidget(self._folder); fr.addWidget(br)
        fc.addLayout(fr)
        lay.addLayout(fc)

        lay.addWidget(_sep())

        # ── Features ──────────────────────────────────────────────────────
        lay.addWidget(_lbl("Features", color=MUTED, bold=True, size=11))

        self._cross_cb = self._feature_row(lay,
            "🌐  Bedrock & Mobile Support",
            "Let players on phones, Xbox, PlayStation, or Switch join  (downloads Geyser + Floodgate)")

        self._multi_cb = self._feature_row(lay,
            "🔄  Support Newer & Older Versions",
            "Different Minecraft versions can connect  (downloads ViaVersion + ViaBackwards)")

        self._allcli_cb = self._feature_row(lay,
            "🕹️  Support ALL Client Versions  (1.7 to Latest)",
            "Includes very old clients like 1.7 & 1.8  (downloads ViaVersion + ViaBackwards + ViaRewind)",
            color=PURPLE)

        self._online_cb = self._feature_row(lay,
            "🔒  Require Official Minecraft Account  (Recommended)",
            "Only players with a real Minecraft purchase can join. Keeps out cracked accounts.",
            default=True)

        # Wire mutual exclusion: allcli supersedes multi
        self._allcli_cb.stateChanged.connect(self._on_allcli)
        self._multi_cb.stateChanged.connect(self._on_multi)
        self._cross_cb.stateChanged.connect(self._on_cross)
        self._online_cb.stateChanged.connect(self._on_online)

        # EULA note
        eula = _lbl(
            f'📋 By clicking Build, you agree to Mojang\'s '
            f'<a href="{EULA_URL}" style="color:{BLUE}">EULA</a>.',
            color=MUTED, size=11)
        eula.setOpenExternalLinks(True)
        lay.addWidget(eula)

        lay.addStretch()
        scroll.setWidget(inner)

        outer = QVBoxLayout(parent)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    def _feature_row(self, parent_lay, title, hint, default=False, color=TEXT):
        row = QHBoxLayout(); row.setSpacing(10); row.setContentsMargins(0, 2, 0, 2)
        cb = QCheckBox(); cb.setChecked(default); cb.setFixedSize(20, 20)

        col = QVBoxLayout(); col.setSpacing(2)
        col.addWidget(_lbl(title, bold=True, size=12, color=color))
        col.addWidget(_lbl(hint, color=MUTED, size=11))

        row.addWidget(cb, alignment=Qt.AlignmentFlag.AlignTop)
        row.addLayout(col, stretch=1)
        parent_lay.addLayout(row)
        return cb

    def _on_type_change(self, txt):
        is_vanilla = "Vanilla" in txt
        for cb in (self._cross_cb, self._multi_cb, self._allcli_cb):
            cb.setEnabled(not is_vanilla)
        if is_vanilla:
            self._log_sig.emit("[i] Vanilla doesn't support plugins — feature options disabled.")

    def _on_cross(self, state):
        self._log_sig.emit(
            "[✓] Bedrock/Mobile support enabled — Geyser + Floodgate will be downloaded." if state
            else "[i] Bedrock/Mobile support disabled.")

    def _on_multi(self, state):
        if state and self._allcli_cb.isChecked():
            self._multi_cb.blockSignals(True)
            self._multi_cb.setChecked(False)
            self._multi_cb.blockSignals(False)
            return
        self._log_sig.emit(
            "[✓] Multi-version enabled — ViaVersion + ViaBackwards will be downloaded." if state
            else "[i] Multi-version support disabled.")

    def _on_allcli(self, state):
        if state:
            # All clients supersedes multi-version
            self._multi_cb.blockSignals(True)
            self._multi_cb.setChecked(False)
            self._multi_cb.blockSignals(False)
            self._log_sig.emit(
                "[✓] All-client support enabled — ViaVersion + ViaBackwards + ViaRewind will be downloaded.")
        else:
            self._log_sig.emit("[i] All-client support disabled.")

    def _on_online(self, state):
        self._log_sig.emit(
            "[✓] Official accounts required — server is protected." if state
            else "[!] Offline mode — anyone can join without a real account.")

    # ── Plugin Tab ────────────────────────────────────────────────────────────
    def _build_plugin_tab(self, parent):
        lay = QVBoxLayout(parent)
        lay.setContentsMargins(14, 12, 14, 12)
        lay.setSpacing(8)

        sr = QHBoxLayout(); sr.setSpacing(8)
        self._search = QLineEdit()
        self._search.setPlaceholderText("Search plugins on Hangar (PaperMC hub)…")
        self._search.setFixedHeight(38)
        self._search.returnPressed.connect(self._do_search)
        sb = _btn("Search", w=90, h=38)
        sb.clicked.connect(self._do_search)
        fb = _ghost("Featured", w=90, h=38)
        fb.clicked.connect(self._show_featured)
        sr.addWidget(self._search, stretch=1)
        sr.addWidget(sb); sr.addWidget(fb)
        lay.addLayout(sr)

        self._plugin_info = _lbl(
            "Popular plugins — click Install to add to your server.",
            color=MUTED, size=11)
        lay.addWidget(self._plugin_info)

        self._pscroll = QScrollArea()
        self._pscroll.setWidgetResizable(True)
        self._pscroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._pcontainer = QWidget()
        self._pcontainer.setStyleSheet(f"background:{PANEL};")
        self._plist = QVBoxLayout(self._pcontainer)
        self._plist.setContentsMargins(0, 0, 4, 0)
        self._plist.setSpacing(6)
        self._plist.addStretch()
        self._pscroll.setWidget(self._pcontainer)
        lay.addWidget(self._pscroll)

        self._show_featured()

    # ── My Servers Tab ────────────────────────────────────────────────────────
    def _build_myservers_tab(self, parent):
        lay = QVBoxLayout(parent)
        lay.setContentsMargins(14, 12, 14, 12)
        lay.setSpacing(8)

        # Header row
        hr = QHBoxLayout()
        hr.addWidget(_lbl("Servers built with MoBRINTH", bold=True, size=13))
        hr.addStretch()
        self._srv_folder_lbl = _lbl("", color=MUTED, size=11)
        hr.addWidget(self._srv_folder_lbl)
        refresh_btn = _ghost("⟳  Refresh", w=100, h=32)
        refresh_btn.clicked.connect(self._refresh_servers)
        hr.addWidget(refresh_btn)
        lay.addLayout(hr)

        self._srv_info = _lbl(
            "No servers found. Build one from the Setup tab first.",
            color=MUTED, size=11)
        lay.addWidget(self._srv_info)

        # Scroll area for server cards
        self._srv_scroll = QScrollArea()
        self._srv_scroll.setWidgetResizable(True)
        self._srv_scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._srv_container = QWidget()
        self._srv_container.setStyleSheet(f"background:{PANEL};")
        self._srv_list = QVBoxLayout(self._srv_container)
        self._srv_list.setContentsMargins(0, 0, 4, 0)
        self._srv_list.setSpacing(8)
        self._srv_list.addStretch()
        self._srv_scroll.setWidget(self._srv_container)
        lay.addWidget(self._srv_scroll)

        # Switch to My Servers tab triggers a refresh and hides the build row
        def _on_tab_change(i):
            self._refresh_servers() if i == 2 else None
            # Build & Start button only relevant on Setup tab
            if hasattr(self, "_build_row"):
                self._build_row.setVisible(i != 2)
        self._tabs.currentChanged.connect(_on_tab_change)

    def _refresh_servers(self):
        root = Path(self._folder.text())
        self._srv_folder_lbl.setText(str(root))

        # Clear existing cards
        while self._srv_list.count() > 1:
            item = self._srv_list.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        servers = scan_servers(root)
        if not servers:
            self._srv_info.setText(
                "No servers found in that folder. Build one from the Setup tab first.")
            return

        self._srv_info.setText(
            f"{len(servers)} server{'s' if len(servers) != 1 else ''} found "
            f"in {root.name}/")

        for info in servers:
            self._add_server_card(info)

    def _add_server_card(self, info: dict):
        f = QFrame(); f.setObjectName("card")
        fl = QHBoxLayout(f)
        fl.setContentsMargins(16, 12, 16, 12)
        fl.setSpacing(14)

        # Left: name + details
        left = QVBoxLayout(); left.setSpacing(4)

        name_row = QHBoxLayout(); name_row.setSpacing(10)
        name_row.addWidget(_lbl(info["name"], bold=True, size=14))
        online_badge = _lbl(
            "🔒 Online" if info["online"] == "true" else "🔓 Offline",
            color=(GREEN if info["online"] == "true" else YELLOW),
            size=11)
        name_row.addWidget(online_badge)
        name_row.addStretch()
        left.addLayout(name_row)

        meta_row = QHBoxLayout(); meta_row.setSpacing(16)
        meta_row.addWidget(_lbl(f"📁 {info['path'].name}", color=MUTED, size=11))
        meta_row.addWidget(_lbl(f"🔌 Port {info['port']}", color=MUTED, size=11))
        meta_row.addWidget(_lbl(f"👥 Max {info['players']} players", color=MUTED, size=11))
        if info["plugins"] > 0:
            meta_row.addWidget(
                _lbl(f"🧩 {info['plugins']} plugin{'s' if info['plugins']!=1 else ''}",
                     color=MUTED, size=11))
        meta_row.addStretch()
        left.addLayout(meta_row)

        # ── Connect addresses ──────────────────────────────────────────────
        local_ip = _get_local_ip()

        def _copy_pill(label: str, address: str, accent: str) -> QWidget:
            """A labelled pill that copies `address` to clipboard on click."""
            pill = QFrame()
            pill.setObjectName("connectPill")
            pill.setStyleSheet(
                f"QFrame#connectPill {{background:{CARD}; border:1px solid {accent};"
                f" border-radius:6px; padding:0px;}}"
                f"QFrame#connectPill:hover {{background:{accent}22;}}")
            row = QHBoxLayout(pill)
            row.setContentsMargins(8, 4, 8, 4); row.setSpacing(8)

            tag = _lbl(label, bold=True, size=10)
            tag.setStyleSheet(
                f"color:{accent}; font-size:10px; font-weight:bold;"
                " background:transparent; border:none;")
            addr_lbl = _lbl(address, size=11)
            addr_lbl.setStyleSheet(
                f"color:{TEXT}; font-size:11px; font-family:Consolas;"
                " background:transparent; border:none;")
            copy_lbl = _lbl("📋 click to copy", color=MUTED, size=10)
            copy_lbl.setStyleSheet(
                f"color:{MUTED}; font-size:10px; background:transparent; border:none;")
            row.addWidget(tag)
            row.addWidget(addr_lbl)
            row.addStretch()
            row.addWidget(copy_lbl)

            def do_copy(*_):
                QApplication.clipboard().setText(address)
                copy_lbl.setText("✅ Copied!")
                copy_lbl.setStyleSheet(
                    f"color:{GREEN}; font-size:10px; background:transparent; border:none;")
                QTimer.singleShot(1800, lambda: (
                    copy_lbl.setText("📋 click to copy"),
                    copy_lbl.setStyleSheet(
                        f"color:{MUTED}; font-size:10px;"
                        " background:transparent; border:none;")))

            pill.mousePressEvent = do_copy
            pill.setCursor(Qt.CursorShape.PointingHandCursor)
            return pill

        java_addr = f"{local_ip}:{info['port']}"
        left.addSpacing(6)
        left.addWidget(_copy_pill("☕  JAVA MC", java_addr, BLUE))

        if info.get("bedrock"):
            bedrock_addr = f"{local_ip}:{info['bedrock_port']}"
            left.addSpacing(4)
            left.addWidget(_copy_pill("🪨  BEDROCK MC", bedrock_addr, ORANGE))

        fl.addLayout(left, stretch=1)

        # Right: RAM picker + Start + Open buttons
        right = QVBoxLayout()
        right.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right.setSpacing(6)

        ram_row = QHBoxLayout(); ram_row.setSpacing(6)
        ram_row.addWidget(_lbl("RAM:", color=MUTED, size=11))
        ram_spin = QSpinBox()
        ram_spin.setRange(1, 32); ram_spin.setValue(2)
        ram_spin.setSuffix(" GB")
        ram_spin.setFixedWidth(72); ram_spin.setFixedHeight(28)
        ram_row.addWidget(ram_spin)
        right.addLayout(ram_row)

        btns = QHBoxLayout(); btns.setSpacing(6)
        start_btn = _btn("▶  Start", bg=GREEN, w=90, h=32)
        open_btn  = _ghost("📁 Open", w=74, h=32)

        status_lbl = _lbl("", color=MUTED, size=11)
        status_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Capture path/widgets via closure — NOT default args (default args get
        # overridden by QPushButton.clicked's bool "checked" argument).
        _srv_path = info["path"]

        def on_start(*_):           # *_ absorbs any stray signal argument
            if self._build_worker and self._build_worker.get_proc() and \
               self._build_worker.get_proc().poll() is None:
                QMessageBox.warning(self, "Server Running",
                    "A server is already running. Stop it first.")
                return
            ram = ram_spin.value()
            start_btn.setEnabled(False); start_btn.setText("Starting…")
            status_lbl.setText("Starting…"); status_lbl.setStyleSheet(
                f"color:{YELLOW}; font-size:11px; background:transparent;")

            worker = LaunchWorker(_srv_path, ram)
            thread = QThread()
            worker.moveToThread(thread)
            worker.log.connect(self._log_sig.emit)
            worker.status.connect(self._status.setText)
            worker.launched.connect(self._on_launched)
            worker.launched.connect(lambda: (
                start_btn.setEnabled(True), start_btn.setText("■  Stop"),
                status_lbl.setText("Running"),
                status_lbl.setStyleSheet(
                    f"color:{GREEN}; font-size:11px; background:transparent;")))
            worker.done.connect(lambda: (
                start_btn.setEnabled(True), start_btn.setText("▶  Start"),
                status_lbl.setText("Stopped"),
                status_lbl.setStyleSheet(
                    f"color:{MUTED}; font-size:11px; background:transparent;")))
            worker.done.connect(lambda: self._on_done(True))
            worker.done.connect(lambda: thread.quit())

            def on_stop(*_):        # *_ absorbs checked bool from clicked signal
                proc = worker.get_proc()
                if proc and proc.poll() is None:
                    try:
                        proc.stdin.write("stop\n"); proc.stdin.flush()
                        self._log_sig.emit("[→] Sent 'stop' to server…")
                    except Exception:
                        proc.terminate()
                    start_btn.setText("Stopping…"); start_btn.setEnabled(False)

            # Swap button to Stop while server is running
            start_btn.clicked.disconnect()
            start_btn.clicked.connect(on_stop)

            # Store worker so main console stop button can also reach it
            self._build_worker = worker
            self._build_thread = thread
            thread.started.connect(worker.run)
            thread.start()

            # Restore Start button after server exits
            worker.done.connect(lambda: (
                start_btn.clicked.disconnect(),
                start_btn.clicked.connect(on_start)))

        start_btn.clicked.connect(on_start)
        open_btn.clicked.connect(
            lambda: subprocess.Popen(
                f'explorer "{info["path"]}"' if sys.platform == "win32"
                else f'open "{info["path"]}"', shell=True))

        btns.addWidget(start_btn); btns.addWidget(open_btn)
        right.addWidget(status_lbl)
        right.addLayout(btns)

        fl.addLayout(right)

        self._srv_list.insertWidget(self._srv_list.count()-1, f)

    def _clear_plugins(self):
        while self._plist.count() > 1:
            item = self._plist.takeAt(0)
            if item.widget(): item.widget().deleteLater()

    def _show_featured(self):
        self._clear_plugins()
        self._plugin_info.setText(f"{len(FEATURED_PLUGINS)} popular plugins ready to install.")
        for owner, slug, desc in FEATURED_PLUGINS:
            self._add_plugin(slug, owner, slug, desc, None)

    def _do_search(self):
        q = self._search.text().strip()
        if not q: self._show_featured(); return
        self._plugin_info.setText(f'Searching for "{q}"…')
        self._clear_plugins()
        threading.Thread(target=self._search_thread, args=(q,), daemon=True).start()

    def _search_thread(self, q):
        results = hangar_search(q, 12)
        self._pending_search = (q, results)
        QTimer.singleShot(0, self._render_search)

    def _render_search(self):
        if not self._pending_search: return
        q, results = self._pending_search
        self._pending_search = None
        self._clear_plugins()
        if not results:
            self._plugin_info.setText(f'No results for "{q}".')
            return
        for r in results:
            ns   = r.get("namespace", {})
            name = r.get("name", ns.get("slug", "?"))
            ownr = ns.get("owner", "?")
            slug = ns.get("slug", "?")
            desc = r.get("description", "")
            dl   = r.get("stats", {}).get("downloads")
            self._add_plugin(name, ownr, slug, desc, dl)
        self._plugin_info.setText(f'{len(results)} plugins found for "{q}".')

    def _add_plugin(self, name, owner, slug, desc, downloads):
        f = QFrame(); f.setObjectName("card")
        fl = QHBoxLayout(f)
        fl.setContentsMargins(14, 8, 14, 8); fl.setSpacing(12)

        info = QVBoxLayout(); info.setSpacing(3)
        nr = QHBoxLayout(); nr.setSpacing(8)
        nr.addWidget(_lbl(name, bold=True, size=13))
        nr.addWidget(_lbl(f"by {owner}", color=MUTED, size=11))
        if downloads is not None:
            nr.addWidget(_lbl(f"↓ {downloads:,}", color=MUTED, size=11))
        nr.addStretch()
        info.addLayout(nr)
        info.addWidget(_lbl(desc or "No description.", color=MUTED, size=11, wrap=True))
        fl.addLayout(info, stretch=1)

        right = QVBoxLayout()
        right.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right.setSpacing(4)
        slbl = _lbl("", color=GREEN, size=11)
        slbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        slbl.setMinimumWidth(84)
        ibtn = _btn("Install", bg=GREEN, w=88, h=32)

        def on_install(_o=owner, _s=slug, _lbl=slbl, _b=ibtn):
            if not self._active_sdir:
                QMessageBox.warning(self, "Build First",
                    "Build a server first so MoBRINTH knows where to install the plugin.")
                return
            _b.setEnabled(False); _b.setText("…")
            w = PluginWorker(_o, _s, self._active_sdir)
            t = QThread()
            w.moveToThread(t)
            w.status_sig.connect(lambda tx, cl, lbl=_lbl:
                (lbl.setStyleSheet(f"color:{cl};font-size:11px;background:transparent;"),
                 lbl.setText(tx)))
            w.log_sig.connect(self._log_sig.emit)
            w.done_sig.connect(lambda ok, tx, b=_b: (b.setEnabled(True), b.setText(tx)))
            w.done_sig.connect(lambda *_: t.quit())
            t.started.connect(w.run)
            t.start()
            self._install_threads.append((t, w))

        ibtn.clicked.connect(on_install)
        right.addWidget(slbl); right.addWidget(ibtn)
        fl.addLayout(right)

        self._plist.insertWidget(self._plist.count()-1, f)

    # ── Console ───────────────────────────────────────────────────────────────
    def _make_console(self):
        f = QFrame(); f.setObjectName("card")
        lay = QVBoxLayout(f)
        lay.setContentsMargins(14, 10, 14, 12)
        lay.setSpacing(8)

        hr = QHBoxLayout()
        hr.addWidget(_lbl("📋  Console", bold=True, size=13))
        hr.addStretch()
        cl = _ghost("Clear", w=58, h=26)
        cl.clicked.connect(lambda: self._log_area.clear())
        hr.addWidget(cl)
        lay.addLayout(hr)

        self._log_area = QTextEdit()
        self._log_area.setReadOnly(True)
        self._log_area.setHtml(f"""
            <div style='text-align:center; margin-top:48px;'>
                <p style='font-size:28px; font-weight:bold; color:{BLUE}; margin:0;'>⛏ MoBRINTH</p>
                <p style='font-size:13px; color:{MUTED}; margin:6px 0 0 0;'>by <b style="color:{TEXT};">Legendary OM</b></p>
                <p style='font-size:11px; color:{BORDER}; margin:18px 0 0 0;'>
                    Configure your server above, then click<br>
                    <b style="color:{BLUE};">Build &amp; Start Server</b> — logs will appear here.
                </p>
            </div>
        """)
        lay.addWidget(self._log_area, stretch=1)

        # Terminal input
        tr = QFrame()
        tr.setStyleSheet(
            f"background:#141824; border-radius:8px; border:1px solid {BORDER};")
        tl = QHBoxLayout(tr)
        tl.setContentsMargins(10, 4, 6, 4); tl.setSpacing(8)
        tl.addWidget(_lbl(">", color=GREEN, bold=True, size=14))
        self._cmd = QLineEdit()
        self._cmd.setPlaceholderText("Server not running yet…")
        self._cmd.setEnabled(False)
        self._cmd.setStyleSheet(
            f"background:transparent; border:none; color:{TEXT};"
            "font-family:Consolas; font-size:12px;")
        self._cmd.returnPressed.connect(self._send_cmd)
        tl.addWidget(self._cmd, stretch=1)
        self._send = _btn("Send", w=64, h=28)
        self._send.setEnabled(False)
        self._send.clicked.connect(self._send_cmd)
        tl.addWidget(self._send)
        lay.addWidget(tr)

        # Build / Stop — hidden when user is on My Servers tab
        self._build_row = QWidget()
        br = QHBoxLayout(self._build_row)
        br.setContentsMargins(0, 0, 0, 0); br.setSpacing(10)
        self._build_btn = _btn("⚒  Build & Start Server", h=50)
        self._build_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self._build_btn.clicked.connect(self._on_build)
        self._stop_btn = _btn("■  Stop", bg=RED, w=110, h=50)
        self._stop_btn.setEnabled(False)
        self._stop_btn.clicked.connect(self._on_stop)
        br.addWidget(self._build_btn, stretch=1)
        br.addWidget(self._stop_btn)
        lay.addWidget(self._build_row)

        self._prog = QProgressBar()
        self._prog.setRange(0, 100); self._prog.setValue(0)
        self._prog.setTextVisible(False); self._prog.setFixedHeight(7)
        lay.addWidget(self._prog)

        self._status = _lbl("Ready", color=MUTED, size=11)
        lay.addWidget(self._status)

        return f

    # ── Actions ───────────────────────────────────────────────────────────────
    def _browse(self):
        p = QFileDialog.getExistingDirectory(self, "Choose Server Folder")
        if p:
            self._folder.setText(p)
            self._log_sig.emit(f"[✓] Output folder: {p}")

    def _on_build(self):
        name = self._name.text().strip()
        if not name:
            QMessageBox.critical(self, "Missing Name", "Please enter a server name."); return

        stype_raw = self._stype.currentText()
        stype = ("Paper" if "Paper" in stype_raw
                 else "Purpur" if "Purpur" in stype_raw
                 else "Vanilla")

        cfg = {
            "server_type":  stype,
            "mc_version":   self._ver.currentText(),
            "server_name":  name,
            "ram_gb":       self._ram_spin.value(),
            "output_dir":   self._folder.text(),
            "crossplay":    self._cross_cb.isChecked(),
            "multiversion": self._multi_cb.isChecked(),
            "all_clients":  self._allcli_cb.isChecked(),
            "online_mode":  self._online_cb.isChecked(),
        }
        safe = "".join(ch if ch.isalnum() or ch in " _-" else "_" for ch in name)
        self._active_sdir = Path(cfg["output_dir"]) / safe

        self._build_btn.setEnabled(False)
        self._stop_btn.setEnabled(True)
        self._prog.setValue(0)

        self._build_thread = QThread()
        self._build_worker = BuildWorker(cfg)
        self._build_worker.moveToThread(self._build_thread)
        self._build_worker.log.connect(self._log_sig.emit)
        self._build_worker.status.connect(self._status.setText)
        self._build_worker.progress.connect(self._prog.setValue)
        self._build_worker.launched.connect(self._on_launched)
        self._build_worker.done.connect(self._on_done)
        self._build_worker.error.connect(
            lambda m: QMessageBox.critical(self, "Build Error", m))
        self._build_thread.started.connect(self._build_worker.run)
        self._build_thread.start()

    def _on_launched(self):
        self._cmd.setEnabled(True)
        self._cmd.setPlaceholderText("Type a command and press Enter or Send…")
        self._send.setEnabled(True)
        self._cmd.setFocus()

    def _on_done(self, _ok):
        self._build_btn.setEnabled(True)
        self._stop_btn.setEnabled(False)
        self._cmd.setEnabled(False)
        self._cmd.setPlaceholderText("Server not running yet…")
        self._send.setEnabled(False)
        self._prog.setValue(0)
        self._status.setText("Ready")
        if self._build_thread: self._build_thread.quit()

    def _on_stop(self):
        if self._build_worker:
            proc = self._build_worker.get_proc()
            if proc and proc.poll() is None:
                try:
                    proc.stdin.write("stop\n"); proc.stdin.flush()
                    self._log_sig.emit("[→] Sent 'stop' to server…")
                except Exception:
                    proc.terminate()
        self._stop_btn.setEnabled(False)
        self._build_btn.setEnabled(True)
        self._cmd.setEnabled(False)
        self._send.setEnabled(False)
        self._status.setText("Stopped")
        self._prog.setValue(0)

    def _send_cmd(self):
        cmd = self._cmd.text().strip()
        if not cmd: return
        if self._build_worker:
            proc = self._build_worker.get_proc()
            if proc and proc.poll() is None:
                try:
                    proc.stdin.write(cmd + "\n"); proc.stdin.flush()
                    self._log_sig.emit(f"[You] > {cmd}")
                    if not self._cmd_hist or self._cmd_hist[-1] != cmd:
                        self._cmd_hist.append(cmd)
                    self._cmd_idx = -1
                    self._cmd.clear(); return
                except Exception as e:
                    self._log_sig.emit(f"[!] Send failed: {e}")
        self._log_sig.emit("[!] Server isn't running.")

    def keyPressEvent(self, e):
        if self._cmd.hasFocus() and self._cmd_hist:
            if e.key() == Qt.Key.Key_Up:
                if self._cmd_idx == -1: self._cmd_idx = len(self._cmd_hist)-1
                elif self._cmd_idx > 0: self._cmd_idx -= 1
                self._cmd.setText(self._cmd_hist[self._cmd_idx]); return
            if e.key() == Qt.Key.Key_Down:
                if self._cmd_idx < len(self._cmd_hist)-1:
                    self._cmd_idx += 1
                    self._cmd.setText(self._cmd_hist[self._cmd_idx])
                else:
                    self._cmd_idx = -1; self._cmd.clear()
                return
        super().keyPressEvent(e)

    def _do_log(self, msg: str):
        if self._log_first:
            self._log_area.clear()
            self._log_first = False
        self._log_area.moveCursor(QTextCursor.MoveOperation.End)
        self._log_area.insertPlainText(msg + "\n")
        self._log_area.moveCursor(QTextCursor.MoveOperation.End)

    def _startup(self):
        v = latest_mc()
        self._log_sig.emit(
            f"[✓] Latest Minecraft: {v}" if v
            else "[!] Could not reach Mojang API — check internet.")


# ─────────────────────────────────────────────────────────────────────────────
# LICENSE AGREEMENT DIALOG
# ─────────────────────────────────────────────────────────────────────────────
LICENSE_TEXT = """\
MoBRINTH — End User License Agreement
Version 1.0  |  Created by Legendary OM
══════════════════════════════════════════════════════════════════

1. ACCEPTANCE
   By clicking "I Agree & Launch", you accept the terms of this agreement.
   If you do not agree, click "Decline" to exit the application.

2. LICENSE GRANT
   MoBRINTH is provided free of charge for personal, non-commercial use.
   You may not sell, redistribute, or rebrand this software without written
   permission from the author (Legendary OM).

3. THIRD-PARTY SOFTWARE
   MoBRINTH downloads and manages third-party software including Minecraft
   server JARs, Paper/Purpur builds, and plugins (Geyser, ViaVersion, etc.).
   Each of those tools is subject to its own license. You are responsible for
   complying with the Minecraft EULA (minecraft.net/en-us/eula) before running
   any server.

4. NO WARRANTY
   This software is provided "as is", without warranty of any kind, express or
   implied. The author is not liable for any data loss, server issues, or other
   damages arising from the use of MoBRINTH.

5. PRIVACY
   MoBRINTH does not collect, transmit, or store any personal data. All server
   files are stored locally on your machine.

6. UPDATES
   The author may release updates at any time. Continued use after an update
   constitutes acceptance of any revised terms.

7. CONTACT
   For support or inquiries, reach out to Legendary OM.

══════════════════════════════════════════════════════════════════
© 2025 Legendary OM. All rights reserved.
"""

_AGREE_FILE = Path.home() / ".mobrinth_agreed"

def _has_agreed() -> bool:
    try:
        data = json.loads(_AGREE_FILE.read_text())
        return data.get("agreed") is True
    except Exception:
        return False

def _save_agreed():
    try:
        _AGREE_FILE.write_text(json.dumps({"agreed": True, "version": "1.0"}))
    except Exception:
        pass


class LicenseDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MoBRINTH — License Agreement")
        self.setMinimumSize(620, 520)
        self.setModal(True)
        self.setStyleSheet(STYLE)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 20, 24, 20)
        lay.setSpacing(14)

        # Header
        hdr = QVBoxLayout(); hdr.setSpacing(4)
        title = QLabel("⛏  MoBRINTH")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title.setStyleSheet(f"color:{BLUE};")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub = QLabel("by Legendary OM  ·  License Agreement")
        sub.setStyleSheet(f"color:{MUTED}; font-size:12px;")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hdr.addWidget(title); hdr.addWidget(sub)
        lay.addLayout(hdr)

        # Divider
        div = QFrame(); div.setFrameShape(QFrame.Shape.HLine)
        div.setStyleSheet(f"color:{BORDER};")
        lay.addWidget(div)

        # Scrollable licence text
        txt = QTextEdit()
        txt.setReadOnly(True)
        txt.setPlainText(LICENSE_TEXT)
        txt.setFont(QFont("Consolas", 10))
        txt.setStyleSheet(
            f"background:{CARD}; color:{TEXT}; border:1px solid {BORDER};"
            " border-radius:8px; padding:10px;")
        lay.addWidget(txt, stretch=1)

        # Checkbox + buttons row
        note = QLabel("Please read the agreement above before proceeding.")
        note.setStyleSheet(f"color:{MUTED}; font-size:11px;")
        note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(note)

        btns = QHBoxLayout(); btns.setSpacing(12)
        decline_btn = QPushButton("✕  Decline")
        decline_btn.setFixedHeight(42)
        decline_btn.setStyleSheet(
            f"QPushButton{{background:{CARD}; color:{MUTED}; border:1px solid {BORDER};"
            " border-radius:8px; font-size:13px; font-weight:600;}}"
            f"QPushButton:hover{{background:{INPUT}; color:{TEXT};}}")
        agree_btn = QPushButton("✔  I Agree & Launch")
        agree_btn.setFixedHeight(42)
        agree_btn.setStyleSheet(
            f"QPushButton{{background:{BLUE}; color:#0d1117; border:none;"
            " border-radius:8px; font-size:13px; font-weight:700;}}"
            f"QPushButton:hover{{background:#88bbff;}}")
        btns.addWidget(decline_btn, stretch=1)
        btns.addWidget(agree_btn, stretch=2)
        lay.addLayout(btns)

        agree_btn.clicked.connect(self._on_agree)
        decline_btn.clicked.connect(self.reject)

    def _on_agree(self, *_):
        _save_agreed()
        self.accept()


# ─────────────────────────────────────────────────────────────────────────────
def _app_icon() -> QIcon:
    here = Path(__file__).parent
    for name in ("icon.ico", "icon.png"):
        p = here / name
        if p.exists():
            return QIcon(str(p))
    return QIcon()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLE)
    icon = _app_icon()
    app.setWindowIcon(icon)

    if not _has_agreed():
        dlg = LicenseDialog()
        dlg.setWindowIcon(icon)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            sys.exit(0)

    w = MoBRINTH()
    w.setWindowIcon(icon)
    w.show()
    sys.exit(app.exec())
