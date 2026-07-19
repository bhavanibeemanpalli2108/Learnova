from ui import create_ui


app = create_ui()


if __name__ == "__main__":

    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        favicon_path=None,
        show_error=True,
        inbrowser=True,
        share=False,
        theme=None,
        css_paths="theme.css",
    )