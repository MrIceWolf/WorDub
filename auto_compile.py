from core.compile import run_compile


def auto_compile_project(english_srt_path, ukrainian_doc_path, threshold=0.7):
    """
    Тепер це просто обгортка без ML.
    GUI НЕ ЛАМАЄТЬСЯ.
    """
    return run_compile(english_srt_path, ukrainian_doc_path)