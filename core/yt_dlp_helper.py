import subprocess
import sys
import os


def run_command(cmd):
    print("\n>>> Виконується команда:")
    print(" ".join(cmd))
    print("-" * 50)

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    for line in process.stdout:
        print(line.strip())

    process.wait()
    print(f"[DEBUG] Код завершення: {process.returncode}")

    if process.returncode != 0:
        print("[WARNING] Команда завершилась з помилкою")


# ======================================================
# REAPER HELPERS
# ======================================================

def get_latest_file(folder, ext):
    files = []
    for root, _, filenames in os.walk(folder):
        for f in filenames:
            if f.endswith(ext):
                files.append(os.path.join(root, f))

    if not files:
        return None

    return max(files, key=os.path.getctime)


def extract_wav(video_path):
    folder = os.path.dirname(video_path)

    video_name = os.path.basename(video_path)

    clean_name = video_name.replace("V_", "").replace(".mp4", "")

    wav_path = os.path.join(
        folder,
        f"S_{clean_name}.wav"
    )

    return [
        "ffmpeg",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s24le",
        "-ar", "48000",
        wav_path,
        "-y"
    ]

# ======================================================
# MODES
# ======================================================

def build_commands(url, mode="reaper", sub_lang="en", output_folder=None):
    base = [sys.executable, "-m", "yt_dlp"]

    folder = output_folder or os.path.join(
        os.path.expanduser("~"),
        "Desktop"
    )

    os.makedirs(folder, exist_ok=True)

    commands = []

    # =========================
    # REAPER MODE
    # =========================
    if mode == "reaper":

        reaper_folder = os.path.join(folder, "%(title)s")

        output_template = os.path.join(
            reaper_folder,
            "V_%(title)s.%(ext)s"
        )

        commands.append(base + [
            url,

            # === ВІДЕО ===
            "-f", "bv*[vcodec^=avc1]+ba[ext=m4a]/b",
            "--merge-output-format", "mp4",

            "--no-write-subs",
            "--no-write-auto-subs",

            "-o", output_template
        ])

        # === СУБТИТРИ ===
        subs_template = os.path.join(
            reaper_folder,
            "S_%(title)s.%(ext)s"
        )

        commands.append(base + [
            url,
            "--skip-download",
            "--write-subs",
            "--write-auto-subs",
            "--sub-langs", "en.*,en,uk.*",
            "--sub-format", "srt",
            "--convert-subs", "srt",
            "-o", subs_template
        ])

        def postprocess(folder_path):
            video = get_latest_file(folder_path, ".mp4")
            if video:
                return extract_wav(video)
            return None

        commands.append(("POSTPROCESS", postprocess, folder))

    # =========================
    # VIDEO MODE
    # =========================
    elif mode == "video":
        commands.append(base + [
            url,
            "-f", "bv*+ba/b",
            "--merge-output-format", "mp4",
            "-o", os.path.join(
                folder,
                "%(title)s.%(ext)s"
            )
        ])

    # =========================
    # AUDIO MODE
    # =========================
    elif mode == "audio":
        commands.append(base + [
            url,
            "-x",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "-o", os.path.join(
                folder,
                "%(title)s.%(ext)s"
            )
        ])

    return commands
