"""Optional server-side DOCX rendering. No Word installation is required."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import threading
import sys
import time
import logging
import signal


def _run_converter(command, *, timeout):
    """Stop the entire converter process group on timeout, including office children."""
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        start_new_session=os.name != "nt",
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
    )
    try:
        stdout, stderr = process.communicate(timeout=timeout)
        return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)
    except BaseException:
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                           capture_output=True, timeout=10, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        process.kill() if process.poll() is None else None
        process.communicate(timeout=10)
        raise


class PdfConversionError(RuntimeError):
    pass


# Bound work across Streamlit sessions in this process.
_conversion_slot = threading.BoundedSemaphore(1)


def libreoffice_path():
    """Find the converter without requiring a terminal-specific PATH override."""
    configured = os.environ.get("LIBREOFFICE_PATH")
    if configured:
        resolved = shutil.which(configured)
        if resolved:
            return resolved
    resolved = shutil.which("soffice") or shutil.which("libreoffice")
    if resolved:
        return resolved
    if sys.platform == "win32":
        for root in (os.environ.get("ProgramW6432"), os.environ.get("ProgramFiles"),
                     os.environ.get("ProgramFiles(x86)"), r"C:\Program Files", r"C:\Program Files (x86)"):
            if root:
                candidate = Path(root) / "LibreOffice" / "program" / "soffice.com"
                if candidate.is_file():
                    return str(candidate)
    return None


def docx_to_pdf(document: bytes, *, timeout=60, wait_timeout=30, on_stage=None, timings=None) -> bytes:
    timings = timings if timings is not None else {}
    started = time.perf_counter()
    executable = libreoffice_path()
    if not executable:
        raise PdfConversionError("PDF downloads are not available on this server yet.")
    acquired = _conversion_slot.acquire(blocking=False)
    if not acquired:
        if on_stage:
            on_stage("Waiting for PDF conversion…")
        acquired = _conversion_slot.acquire(timeout=wait_timeout)
    timings["wait"] = time.perf_counter() - started
    if not acquired:
        logging.getLogger(__name__).warning("worksheet busy wait_seconds=%.3f", timings["wait"])
        raise PdfConversionError("The server is busy. Please retry.")
    conversion_started = time.perf_counter()
    try:
        if on_stage:
            on_stage("Creating your PDF…")
        with tempfile.TemporaryDirectory(prefix="physics-worksheet-") as directory:
            root = Path(directory)
            source = root / "worksheet.docx"
            source.write_bytes(document)
            try:
                result = _run_converter(
                    [executable, f"-env:UserInstallation={(root / 'profile').as_uri()}",
                     "--headless", "--convert-to", "pdf:writer_pdf_Export",
                     "--outdir", str(root), str(source)],
                    timeout=timeout,
                )
                output = root / "worksheet.pdf"
                if result.returncode != 0 or not output.is_file():
                    raise PdfConversionError("PDF conversion failed. Please try again.")
                pdf = output.read_bytes()
                if not pdf.startswith(b"%PDF-"):
                    raise PdfConversionError("PDF conversion returned an invalid file.")
                return pdf
            except subprocess.TimeoutExpired as exc:
                raise PdfConversionError("PDF conversion took too long. Try a shorter worksheet.") from exc
            except OSError as exc:
                raise PdfConversionError("The PDF converter could not run. Please try again later.") from exc
    finally:
        timings["conversion"] = time.perf_counter() - conversion_started
        logging.getLogger(__name__).warning("worksheet conversion wait_seconds=%.3f conversion_seconds=%.3f", timings["wait"], timings["conversion"])
        _conversion_slot.release()
