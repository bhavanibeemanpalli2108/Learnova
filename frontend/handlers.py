import html
from pathlib import Path

import httpx

from config import BACKEND_URL


UPLOAD_URL = f"{BACKEND_URL}/upload"
CHAT_URL = f"{BACKEND_URL}/chat"
HEALTH_URL = f"{BACKEND_URL}/health"


# ---------------------------------------------------------
# Session State
# ---------------------------------------------------------

DOCUMENTS: list[str] = []


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def _render_documents(documents: list[str]) -> str:
    """
    Render uploaded documents.
    """

    if not documents:

        return """
        <div class="document-list">
            <div class="empty-state">
                No documents uploaded yet.
            </div>
        </div>
        """

    cards = []

    for document in documents:

        cards.append(
            f"""
            <div class="document-card">
                📄 {html.escape(document)}
            </div>
            """
        )

    return f"""
    <div class="document-list">
        {''.join(cards)}
    </div>
    """


# ---------------------------------------------------------
# Backend Health
# ---------------------------------------------------------

def backend_status():

    try:

        response = httpx.get(
            HEALTH_URL,
            timeout=5,
        )

        if response.status_code == 200:
            return "🟢 Backend Connected"

    except Exception:
        pass

    return "🔴 Backend Offline"


# ---------------------------------------------------------
# Upload Document
# ---------------------------------------------------------

def upload_document(file):

    if file is None:

        return (
            "Please select a document.",
            _render_documents(DOCUMENTS),
        )

    file_path = Path(file)

    try:

        with open(file_path, "rb") as uploaded_file:

            files = {
                "file": (
                    file_path.name,
                    uploaded_file,
                )
            }

            response = httpx.post(
                UPLOAD_URL,
                files=files,
                timeout=300,
            )

        response.raise_for_status()

        data = response.json()

        document = data.get("document", {})

        if isinstance(document, dict):

            filename = document.get(
                "filename",
                file_path.name,
            )

        else:

            filename = file_path.name

        if filename not in DOCUMENTS:
            DOCUMENTS.append(filename)

        chunk_count = data.get(
            "chunk_count",
            0,
        )

        status = (
            f"✅ Successfully uploaded <b>{filename}</b>"
            f"<br><br>"
            f"Chunks Indexed : <b>{chunk_count}</b>"
        )

        return (
            status,
            _render_documents(DOCUMENTS),
        )

    except httpx.HTTPStatusError as e:

        return (
            f"❌ Backend Error ({e.response.status_code})",
            _render_documents(DOCUMENTS),
        )

    except Exception as e:

        return (
            f"❌ Upload Failed<br><br>{str(e)}",
            _render_documents(DOCUMENTS),
        )


# ---------------------------------------------------------
# Ask Question
# ---------------------------------------------------------

def ask_question(question, history):

    history = history or []

    if not question.strip():

        return (
            history,
            "",
            "",
            "",
        )

    try:

        payload = {
            "query": question,
        }

        response = httpx.post(
            CHAT_URL,
            json=payload,
            timeout=300,
        )

        response.raise_for_status()

        data = response.json()

        answer = data.get(
            "answer",
            "No answer generated.",
        )

        history.append(
            {
                "role": "user",
                "content": question,
            }
        )

        history.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        source = data.get("source")

        if source:

            source_md = f"- {source}"

        else:

            source_md = "_No document source._"

        web_sources = data.get(
            "web_sources",
            [],
        )

        if web_sources:

            web_md = "\n".join(
                f"- [{item.get('title','Source')}]({item.get('url','#')})"
                for item in web_sources
            )

        else:

            web_md = "_No web sources._"

        return (
            history,
            "",
            source_md,
            web_md,
        )

    except httpx.HTTPStatusError as e:

        history.append(
            {
                "role": "assistant",
                "content": f"❌ Backend returned HTTP {e.response.status_code}",
            }
        )

        return (
            history,
            "",
            "",
            "",
        )

    except Exception as e:

        history.append(
            {
                "role": "assistant",
                "content": f"❌ {str(e)}",
            }
        )

        return (
            history,
            "",
            "",
            "",
        )

# Clear Chat

def clear_chat():

    return (
        [],
        "",
        "",
        "",
    )