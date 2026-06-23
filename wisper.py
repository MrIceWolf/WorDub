import os
import whisper


# ==========================================================
# =====================  УТИЛІТА 3  ========================
# ==========================================================

def run_wisper(audio_path, model_name="small", output_path=None, log_callback=None):

    def to_srt_time(seconds: float) -> str:
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds - int(seconds)) * 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    print("\n=== Whisper Transcriber ===")

    if not os.path.isfile(audio_path):
        raise FileNotFoundError("Audio file not found")

    print(f"Завантаження моделі Whisper ({model_name})...")
    model_display = model_name.capitalize()
    model = whisper.load_model(model_name, device="cpu")

    print("Транскрибування аудіо...")
    try:
        result = model.transcribe(audio_path, fp16=False)
    except Exception as e:
        print("Medium/large злетів, fallback на small:", e)
        model = whisper.load_model("small", device="cpu")
        result = model.transcribe(audio_path, fp16=False)

    segments = result.get("segments", [])
    srt_blocks = []

    if not segments:
        text = result.get("text", "").strip()
        if text:
            duration = result.get("duration", 0)
            srt_blocks.append(
                f"1\n00:00:00,000 --> {to_srt_time(duration)}\n{text}"
            )
    else:
        for i, seg in enumerate(segments, start=1):
            start = seg["start"]
            end = seg["end"]
            text = seg["text"].strip()
            srt_blocks.append(
                f"{i}\n{to_srt_time(start)} --> {to_srt_time(end)}\n{text}"
            )

    if not output_path:
        base_folder = os.path.dirname(audio_path)
        filename = os.path.splitext(os.path.basename(audio_path))[0]
        output_filename = f"{model_display}_{filename}.srt"
        output_path = os.path.join(base_folder, output_filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(srt_blocks))

    print("\n=== Готово! ===")
    print("Створено файл:", output_path)

    return output_path

# ==========================================================
# =====================  MAIN  =============================
# ==========================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3 or sys.argv[1].lower() != "wisper":
        print("Використання:")
        print("python subtitle_tool.py wisper <шлях_до_аудіо>")
        sys.exit(1)

    audio_file = sys.argv[2]

    run_wisper(audio_file)