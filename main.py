import sys
import os
from core.translate import run_translate
from core.compile import run_compile
from core.wisper import run_transcribe
from docx import Document
sys.stdout.reconfigure(encoding="utf-8")
sys.path.append(os.path.dirname(__file__))

def show_help():
    print("\n=== Subtitle Tool ===")
    print("Використання:")
    print("  python main.py translate <file.srt>")
    print("  python main.py compile <original.srt> <author.docx>")
    print("  python main.py transcribe <audio.mp3>\n")

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Помилка: не вказано режим роботи.")
        show_help()
        sys.exit(1)

    mode = sys.argv[1].lower()

    try:
        if mode == "translate":
            if len(sys.argv) < 3:
                print("Помилка: не вказано файл для перекладу.")
                show_help()
                sys.exit(1)

            else:
                run_translate(sys.argv[2])

        elif mode == "compile":
            if len(sys.argv) < 4:
                print("Помилка: не вказано обидва файли для компіляції.")
                show_help()
                sys.exit(1)
            else:
                run_compile(sys.argv[2], sys.argv[3])

        elif mode == "wisper":

            if len(sys.argv) < 3:
                print("Помилка: не вказано аудіофайл.")
                show_help()
                sys.exit(1)

            audio_file = sys.argv[2]
            model_name = sys.argv[3] if len(sys.argv) > 3 else "small"

            run_transcribe(audio_file, model_name=model_name)

        else:
            print(f"Помилка: невідомий режим '{mode}'")
            show_help()

    except Exception as e:
        print("\nСталася помилка під час виконання:")
        print(e)
        print()