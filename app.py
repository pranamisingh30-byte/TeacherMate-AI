
import streamlit as st
import pymupdf

st.set_page_config(
    page_title="TeacherMate AI",
    page_icon="📚"
)

st.title("📚 TeacherMate AI")
st.subheader("Your AI assistant for educational materials")

st.write(
    "Upload an educational PDF to explore its content "
    "and prepare learning materials for your students."
)

uploaded_file = st.file_uploader(
    "Upload an educational PDF",
    type=["pdf"]
)

if uploaded_file is not None:
    pdf_bytes = uploaded_file.getvalue()

    try:
        with pymupdf.open(stream=pdf_bytes, filetype="pdf") as document:
            st.success(f"PDF uploaded successfully! Pages: {len(document)}")

            full_text = ""

            for page_number, page in enumerate(document, start=1):
                page_text = page.get_text()
                full_text += f"\n\n--- Page {page_number} ---\n"
                full_text += page_text

            if full_text.strip():
                st.subheader("Extracted PDF Text")
                st.text_area(
                    "Text from your document",
                    value=full_text,
                    height=350
                )
                st.info(
                    "Your PDF text is ready. Next, we will add "
                    "question-answering features."
                )
            
            else:
                st.warning(
                    "No selectable text was found. "
                    "This PDF may contain scanned images."
                )

            if full_text.strip():
                st.divider()
                st.subheader("Ask Your PDF")

                question = st.text_input(
                    "What would you like to know about this document?",
                    placeholder="e.g., What are the main concepts?"
                )

                if question:
                    words = [
                        word.lower().strip(".,?!:;()[]")
                        for word in question.split()
                    ]
                    keywords = [
                        word for word in words
                        if len(word) > 3
                    ]

                    sentences = [
                        sentence.strip()
                        for sentence in full_text.replace(
                            "\n", " "
                        ).split(".")
                        if sentence.strip()
                    ]

                    matches = [
                        sentence for sentence in sentences
                        if any(
                            keyword in sentence.lower()
                            for keyword in keywords
                        )
                    ]

                    if matches:
                        st.write("**Relevant passages from your PDF:**")
                        for match in matches[:5]:
                            st.write(f"- {match}.")
                    else:
                        st.info(
                            "I couldn't find a matching passage. "
                            "Try using keywords from the PDF."
                        )

    except Exception as error:
        st.error(f"Could not read this PDF: {error}")

