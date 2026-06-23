import re

def srt_to_internal_format(srt_text):
    pattern = re.compile(
        r"\d+\s*\n"
        r"\d{2}:\d{2}:\d{2},\d+\s*-->\s*\d{2}:\d{2}:\d{2},\d+\s*\n"
        r"(.*?)(?=\n\d+\n|\Z)",
        re.DOTALL
    )

    matches = pattern.findall(srt_text)

    blocks = []
    for m in matches:
        lines = [l.strip() for l in m.split("\n") if l.strip()]
        blocks.append("||" + "|".join(lines) + "||")

    return "\n".join(blocks)

import re

# ==========================================
# СТРУКТУРА ОРИГІНАЛУ
# ==========================================
def extract_structure(original_text):
    blocks = re.findall(r"\|\|(.*?)\|\|", original_text, re.DOTALL)
    return [len(block.split("|")) for block in blocks]


# ==========================================
# SOFT SPLIT
# ==========================================
def split_soft(text):
    return [l.strip() for l in text.split("\n") if l.strip()]


# ==========================================
# CLEAN
# ==========================================
def clean_line(line):
    line = re.sub(r"^[-—]\s*", "", line)
    line = re.sub(r"\s+", " ", line)
    return line.strip()


# ==========================================
# NORMALIZE (більш стабільна версія)
# ==========================================
def normalize_text(line):
    line = re.sub(r"\s+([.!?,])", r"\1", line)
    line = re.sub(r",(?=\S)", ", ", line)
    line = re.sub(r"\s+", " ", line)
    return line.strip()


# ==========================================
# BALANCED SPLIT (основний fallback)
# ==========================================
def smart_balance_split(text, parts, max_len=42):
    if parts <= 1:
        return [text]

    words = text.split()

    target_len = min(max_len, max(1, len(text) // parts))

    chunks = []
    current = ""

    for word in words:
        if len(current) + len(word) + 1 <= target_len:
            current = word if not current else current + " " + word
        else:
            chunks.append(current.strip())
            current = word

    if current:
        chunks.append(current.strip())

    while len(chunks) < parts:
        chunks.append("")

    while len(chunks) > parts:
        chunks[-2] = chunks[-2] + " " + chunks[-1]
        chunks.pop()

    return chunks


# ==========================================
# SENTENCE SPLIT
# ==========================================
def sentence_split(line):
    parts = re.split(r'(?<=[.!?])\s+', line)
    return [p.strip() for p in parts if p.strip()]


# ==========================================
# ОСНОВНИЙ АЛГОРИТМ
# ==========================================
def align_text(original_text, author_text):
    structure = extract_structure(original_text)
    lines = [clean_line(l) for l in split_soft(author_text)]

    result = []
    idx = 0
    buffer = []

    for parts_needed in structure:
        block_lines = []

        while len(block_lines) < parts_needed:

            # =========================
            # 1. ДЖЕРЕЛО ТЕКСТУ
            # =========================
            if buffer:
                current_line = buffer.pop(0)
            elif idx < len(lines):
                current_line = lines[idx]
                idx += 1
            else:
                block_lines.append("")
                continue

            current_line = current_line.strip()
            if not current_line:
                continue

            remaining = parts_needed - len(block_lines)

            # =========================
            # 2. SPLIT ЛОГІКА
            # =========================
            if remaining > 1:

                sentences = sentence_split(current_line)

                if len(sentences) >= remaining:
                    split_parts = sentences
                else:
                    split_parts = smart_balance_split(current_line, remaining)

                block_lines.extend(split_parts[:remaining])

                rest = split_parts[remaining:]
                if rest:
                    buffer = rest + buffer

            else:
                block_lines.append(current_line)

        # =========================
        # ФІНАЛЬНИЙ БЛОК
        # =========================
        block_lines = block_lines[:parts_needed]
        block_lines = [normalize_text(l) for l in block_lines]

        result.append("||" + "|".join(block_lines) + "||")

    # =========================
    # CLEAN EMPTY TRAILING
    # =========================
    while result and re.match(r"\|\|\s*\|\|", result[-1]):
        result.pop()

    return result

# ==========================================
# ФОРМАТ ВИВОДУ
# ==========================================
def format_output(blocks):
    return "\n".join(blocks)

# ==========================================
# MAIN FUNCTION
# ==========================================
def process(original_text, author_text):
    blocks = align_text(original_text, author_text)
    return format_output(blocks)