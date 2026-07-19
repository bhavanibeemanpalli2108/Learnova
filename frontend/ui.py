import gradio as gr

from handlers import (
    upload_document,
    ask_question,
    clear_chat,
    backend_status,
)


# ============================================================
# Theme
# ============================================================

THEME = gr.themes.Base()


# ============================================================
# Create UI
# ============================================================

def create_ui():

    with gr.Blocks(
        theme=THEME,
        title="AI Powered Study Assistant",
        css_paths="theme.css",
        fill_height=True,
    ) as demo:

        # =====================================================
        # HEADER
        # =====================================================

        with gr.Row(
            elem_id="header",
            equal_height=True,
        ):

            with gr.Column(scale=8):

                gr.Markdown(
                    """
# 🤖 AI Powered Study Assistant

### Learn Smarter • Retrieve Faster • Study Better
"""
                )

            with gr.Column(
                scale=2,
                min_width=180,
            ):

                backend_indicator = gr.Markdown(
                    backend_status(),
                    elem_id="backend-status",
                )

        # =====================================================
        # BODY
        # =====================================================

        with gr.Row(
            equal_height=True,
            elem_id="main-container",
        ):

            # =================================================
            # SIDEBAR
            # =================================================

            with gr.Column(
                scale=1,
                min_width=320,
                elem_id="sidebar",
            ):

                gr.Markdown(
                    """
## 📂 Knowledge Base

Upload your study material to build your personal AI knowledge base.
"""
                )

                upload_file = gr.File(
                    label="Choose Document",
                    file_types=[
                        ".pdf",
                        ".docx",
                        ".txt",
                    ],
                    file_count="single",
                    elem_id="upload-file",
                )

                upload_button = gr.Button(
                    value="📤 Upload Document",
                    variant="primary",
                    elem_id="upload-button",
                )

                upload_status = gr.Markdown(
                    "",
                    elem_id="upload-status",
                )

                gr.Markdown("---")

                gr.Markdown(
                    """
### 📚 Uploaded Documents
"""
                )

                document_list = gr.HTML(
                    """
<div class="document-list">

    <div class="empty-state">

        No documents uploaded yet.

    </div>

</div>
                    """,
                    elem_id="document-list",
                )

                gr.Markdown("---")

                clear_chat_button = gr.Button(
                    value="🗑 Clear Conversation",
                    variant="secondary",
                    elem_id="clear-button",
                )


            # =================================================
            # CHAT AREA
            # =================================================

            with gr.Column(
                scale=3,
                elem_id="chat-column",
            ):

                gr.Markdown(
                    """
## 💬 AI Tutor

Ask questions about your uploaded study material. The assistant will retrieve relevant context before generating answers.
"""
                )

                chatbot = gr.Chatbot(
                    label=None,
                    value=[],
                    height=650,
                    elem_id="chatbot",
                    avatar_images=(
                        None,
                        None,
                    ),
                )

                # ==============================================
                # SOURCES
                # ==============================================

                with gr.Row():

                    with gr.Column(scale=1):

                        with gr.Accordion(
                            "📖 Retrieved Sources",
                            open=False,
                        ):

                            sources = gr.Markdown(
                                value="_No retrieved sources yet._",
                                elem_id="sources-panel",
                            )

                    with gr.Column(scale=1):

                        with gr.Accordion(
                            "🌐 Web Sources",
                            open=False,
                        ):

                            web_sources = gr.Markdown(
                                value="_No web sources yet._",
                                elem_id="web-panel",
                            )

                # ==============================================
                # CHAT INPUT
                # ==============================================

                with gr.Group(elem_id="chat-input-container"):

                    question = gr.Textbox(
                        placeholder="Ask anything about your uploaded documents...",
                        show_label=False,
                        lines=2,
                        max_lines=6,
                        autofocus=True,
                        container=False,
                        elem_id="question-box",
                    )

                    with gr.Row():

                        send_button = gr.Button(
                            value="🚀 Send",
                            variant="primary",
                            scale=6,
                            elem_id="send-button",
                        )

                        clear_input_button = gr.Button(
                            value="✖ Clear",
                            variant="secondary",
                            scale=2,
                            elem_id="clear-input-button",
                        )


        # =====================================================
        # EVENTS
        # =====================================================

        upload_button.click(
            fn=upload_document,
            inputs=[
                upload_file,
            ],
            outputs=[
                upload_status,
                document_list,
            ],
            show_progress="full",
        )

        send_button.click(
            fn=ask_question,
            inputs=[
                question,
                chatbot,
            ],
            outputs=[
                chatbot,
                question,
                sources,
                web_sources,
            ],
            show_progress="minimal",
        )

        question.submit(
            fn=ask_question,
            inputs=[
                question,
                chatbot,
            ],
            outputs=[
                chatbot,
                question,
                sources,
                web_sources,
            ],
            show_progress="minimal",
        )

        clear_chat_button.click(
            fn=clear_chat,
            outputs=[
                chatbot,
                question,
                sources,
                web_sources,
            ],
        )

        clear_input_button.click(
            fn=lambda: "",
            outputs=[
                question,
            ],
        )

        demo.load(
            fn=backend_status,
            outputs=[
                backend_indicator,
            ],
        )

        return demo


