import os
import re
import sys
from docx import Document

# ==========================================================
# FIX WINDOWS CONSOLE
# ==========================================================
try:
    sys.stdout.reconfigure(encoding="utf-8")
except:
    pass


# ==========================================================
# SAFE FILE READ
# ==========================================================
def read_file_safely(path):
    encodings = ["utf-8-sig", "utf-8", "cp1251", "latin-1"]

    for enc in encodings:
        try:
            with open(path, "r", encoding=enc, errors="ignore") as f:
                return f.read()
        except:
            continue

    raise Exception(f"Cannot read file: {path}")


# ==========================================================
# PARSE SRT (TIMINGS ONLY)
# ==========================================================
def parse_srt_timings(text):
    text = text.replace("\r\n", "\n").strip()

    blocks = re.split(r"\n\s*\n", text)

    timings = []

    for block in blocks:
        lines = [l.strip() for l in block.split("\n") if l.strip()]

        for line in lines:
            if "-->" in line:
                timings.append(line)
                break

    return timings


# ==========================================================
# PARSE DOCX (SAFE VERSION)
# ==========================================================
def parse_docx(path):
    doc = Document(path)
    raw = "\n".join(p.text for p in doc.paragraphs)

    raw = raw.replace("｜", "|")

    # беремо тільки блоки між ||...||
    blocks = re.findall(r"\|\|(.*?)\|\|", raw, re.DOTALL)

    result = []

    for b in blocks:
        b = b.replace("｜", "|").strip()

        # важливо: прибираємо порожні строки
        lines = [x.strip() for x in b.split("|") if x.strip()]

        if not lines:
            continue

        result.append("\n".join(lines))

    return result


# ==========================================================
# CORE
# ==========================================================
def run_compile(srt_path, doc_path):

    print("\n=== Subtitle Compiler v1.0 ===")

    srt_path = os.path.abspath(srt_path)
    doc_path = os.path.abspath(doc_path)

    if not os.path.isfile(srt_path):
        raise Exception("SRT not found")

    if not os.path.isfile(doc_path):
        raise Exception("DOC not found")

    # =====================
    # LOAD
    # =====================
    srt_text = read_file_safely(srt_path)

    timings = parse_srt_timings(srt_text)
    author_blocks = parse_docx(doc_path)

    print("\nDEBUG:")
    print("timings:", len(timings))
    print("blocks:", len(author_blocks))

    # =====================
    # NORMALIZATION FIX (ВАЖЛИВО)
    # =====================
    min_len = min(len(timings), len(author_blocks))

    if len(timings) != len(author_blocks):
        print("\n WARNING: mismatch, trimming to safe size")
        print("timings:", len(timings))
        print("blocks:", len(author_blocks))
        print("used:", min_len)

    timings = timings[:min_len]
    author_blocks = author_blocks[:min_len]

    # =====================
    # BUILD OUTPUT
    # =====================
    results = []

    for i, (timing, text) in enumerate(zip(timings, author_blocks), start=1):

        parts = timing.split(" --> ")
        if len(parts) != 2:
            raise Exception(f"Invalid timing: {timing}")

        start, end = parts

        clean_text = " ".join(
            l.strip() for l in text.split("\n") if l.strip()
        )

        results.append((clean_text, start, end))

    # =====================
    # SAVE
    # =====================
    base = os.path.dirname(srt_path)
    name = os.path.splitext(os.path.basename(srt_path))[0]

    out_path = os.path.join(base, f"{name}.srt")

    srt_blocks = []

    for i, (text, start, end) in enumerate(results, start=1):
        srt_blocks.append("\n".join([
            str(i),
            f"{start} --> {end}",
            text
        ]))

    print("\n=== DONE ===")
    print(out_path)

    return results


# ==========================================================
# MAIN
# ==========================================================
if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Usage: python script.py <srt> <docx>")
        sys.exit(1)

    run_compile(sys.argv[1], sys.argv[2])