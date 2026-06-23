# # ==========================================================
# # =====================  УТИЛІТА 1  ========================
# # ==========================================================

# import sys
# import os
# import re
# import json
# from deep_translator import GoogleTranslator
# from docx import Document
# import whisper

# # ==========================================================
# # HEADER FUNCTION
# # ==========================================================

# def show_engine_header(version="1.5", codename="UNITY"):
#     print(f"\n\n === SUBTITLE TOOL V{version} ({codename}) ===")

# # ==========================================================
# # ВИБІР РЕЖИМУ
# # ==========================================================

# if len(sys.argv) < 2:
#     print("\n Використання:")
#     print("  python subtitle_tool.py translate \"file.srt\"")
#     print("  python subtitle_tool.py compile \"original.srt\" \"author.docx\"")
#     sys.exit(1)

# mode = sys.argv[1].lower()







# # ==========================================================
# # =====================  УТИЛІТА 2  ========================
# # ==========================================================

# elif mode == "compile":

#     sys.argv = [sys.argv[0]] + sys.argv[2:]

#     show_engine_header()
#     print("\n\n === Subtitle Compiler v1.0 ===")

#     if len(sys.argv) < 3:
#         print(" Використання:")
#         print(" python compile_author_to_srt.py original.srt author.docx")
#         sys.exit(1)

#     original_srt_path = sys.argv[1]
#     author_doc_path = sys.argv[2]

#     if not os.path.isfile(original_srt_path):
#         print(" Оригінальний SRT не знайдено!")
#         sys.exit(1)

#     if not os.path.isfile(author_doc_path):
#         print(" Author DOCX не знайдено!")
#         sys.exit(1)

#     with open(original_srt_path, "r", encoding="utf-8-sig") as f:
#         content = f.read()

#     blocks = re.split(r"\r?\n\r?\n+", content.strip())

#     timings = []

#     for block in blocks:
#         lines = block.strip().split("\n")
#         if len(lines) >= 2 and re.match(r"\d{2}:\d{2}:\d{2},\d{3}", lines[1]):
#             timings.append(lines[1])
#         elif len(lines) >= 1 and re.match(r"\d{2}:\d{2}:\d{2},\d{3}", lines[0]):
#             timings.append(lines[0])

#     print(f" Знайдено таймінгів: {len(timings)}")

#     doc = Document(author_doc_path)
#     full_text = "\n".join([p.text for p in doc.paragraphs])

#     author_blocks = re.findall(r"\|\|(.*?)\|\|", full_text, re.DOTALL)

#     print(f" Знайдено авторських блоків: {len(author_blocks)}")

#     if len(author_blocks) != len(timings):
#         print("\n ПОМИЛКА!")
#         print(" Кількість блоків не співпадає з кількістю таймінгів!")
#         print(f" Таймінгів: {len(timings)}")
#         print(f" Блоків: {len(author_blocks)}")
#         sys.exit(1)

#     compiled_blocks = []

#     for i, (timing, block) in enumerate(zip(timings, author_blocks), start=1):

#         block = block.strip()
#         lines = [line.strip() for line in block.split("|")]

#         # збираємо текст блоку
#         formatted_text = "\n".join(lines)
#         srt_block = "\n".join([str(i), timing, formatted_text])
#         compiled_blocks.append(srt_block)

#     # =============================
#     # Очищення блоків безпосередньо перед записом у файл
#     # =============================
#     cleaned_blocks = []
#     for block in compiled_blocks:
#         lines = block.split("\n")
#         text_lines = lines[2:]  # текст блоку
#         # пропускаємо блок, якщо він порожній або містить +=+
#         if all(not line.strip() for line in text_lines):
#             continue
#     #    if any("+=+" in line for line in text_lines):
#     #        continue
#         cleaned_blocks.append("\n".join(lines))

#     base_folder = os.path.dirname(original_srt_path)
#     filename = os.path.splitext(os.path.basename(original_srt_path))[0]

#     output_path = os.path.join(base_folder, f"MY_{filename}.srt")

#     with open(output_path, "w", encoding="utf-8") as f:
#         f.write("\n\n".join(cleaned_blocks))

#     print("\n === Готово! ===")
#     print(" Створено файл:")
#     print(" ", output_path)
#     print()



# # ==========================================================
# # НЕВІДОМИЙ РЕЖИМ
# # ==========================================================

# else:
#     print(" Невідомий режим!")
#     print(" Використовуйте: translate або compile")
