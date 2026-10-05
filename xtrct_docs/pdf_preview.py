"""Inspect and rasterize the actual downloadable PDF, with bounded resources."""
import io
import threading
from contextlib import closing
import pypdfium2 as pdfium

# PDFium is not thread-safe, including independent documents.
_lock = threading.Lock()


def page_summary(data):
    with _lock, closing(pdfium.PdfDocument(data)) as document:
        answer_start = None
        for index in range(len(document)):
            page = document[index]
            try:
                text = page.get_textpage()
                try:
                    if "Answer Key - All Versions" in text.get_text_bounded():
                        answer_start = index
                        break
                finally:
                    text.close()
            finally:
                page.close()
        return {"total": len(document), "questions": answer_start if answer_start is not None else len(document),
                "answers": len(document) - answer_start if answer_start is not None else 0}


def render_page(data, index):
    with _lock, closing(pdfium.PdfDocument(data)) as document:
        page = document[index]
        try:
            bitmap = page.render(scale=1.3)
            try:
                output = io.BytesIO()
                bitmap.to_pil().save(output, format="PNG")
                return output.getvalue()
            finally:
                bitmap.close()
        finally:
            page.close()
