import os
import openai
from dotenv import load_dotenv
import json
import streamlit as st
from docx import Document
from io import BytesIO

load_dotenv()

openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_press_release(notes):
    prompt = f"""
    Write a detailed press release for Igus based on the following announcement notes:
    {notes}

    Ensure the press release is comprehensive, highlights key achievements, incorporates Igus's goals, and is engaging for the reader.
    """
    try:
        response = openai.ChatCompletion.create(
            engine=os.getenv("OPENAI_ENGINE_ID"),
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": notes}
            ],
            temperature=0,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
        content = response['choices'][0]['message']['content']
        return content
    except Exception as e:
        print(f"Error generating press release: {e}")
        return "An error occurred while generating the press release."


def fill_docx_template(content, template_path="template/pressrelease.docx"):
    doc = Document(template_path)
    for paragraph in doc.paragraphs:
        if "Cologne" in paragraph.text:
            # Clear the placeholder text
            paragraph.clear()
            # Add the new content
            paragraph.add_run(content)
            break
    return doc


def download_docx(document):
    # Save the docx to a BytesIO object
    doc_io = BytesIO()
    document.save(doc_io)
    doc_io.seek(0)
    return doc_io


def docx_to_text(doc):
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)


def main():
    st.title('Future Press Release for Igus')
    notes = st.text_area("Enter Announcement Notes Here:", height=100)
    if st.button('Generate Draft'):
        with st.spinner('Generating Press Release Draft...'):
            press_release_draft = generate_press_release(notes)
            st.markdown("### Draft Press Release")
            st.write(press_release_draft)

            # Fill the docx template with the generated content
            doc = fill_docx_template(press_release_draft)
            doc_io = download_docx(doc)

            # Convert docx content to text for display
            doc_text = docx_to_text(doc)
            st.markdown("### Document Preview")
            st.text_area("Preview", value=doc_text, height=300, disabled=True)

            # Provide a download button for the filled docx
            st.download_button(
                label="Download Press Release",
                data=doc_io,
                file_name="Generated_Press_Release.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

if __name__ == "__main__":
    main()
