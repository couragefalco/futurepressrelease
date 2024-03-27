import os 
import streamlit as st
import openai
from dotenv import load_dotenv 
import json 

load_dotenv()

openai.api_type = os.getenv("OPENAI_API_TYPE")  
openai.api_base = os.getenv("OPENAI_API_BASE")  
openai.api_version = os.getenv("OPENAI_API_VERSION")  
openai.api_key = os.getenv("OPENAI_API_KEY")  




prompt = f"""
Write a detailed press release for Igus based on the following announcement notes:
{notes}

Ensure the press release is comprehensive, highlights key achievements, incorporates Igus's goals, and is engaging for the reader.
"""


def generate_press_release(text):
    response = openai.ChatCompletion.create(
        engine=os.getenv("OPENAI_ENGINE_ID"),
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ],
        temperature=0,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
            
        )
    # Adjusted to correctly access and parse the JSON response
    content = json.loads(response.choices[0].message.content)
    print (content)
    return content  # Return the entire content as a dictionary
        

st.title('Future Press Release Generator for Igus')
notes = st.text_area("Enter Announcement Notes Here:", height=300)
if st.button('Generate Draft'):
    with st.spinner('Generating Press Release Draft...'):
        press_release_draft = generate_press_release(notes)
        st.markdown("### Draft Press Release")
        st.write(press_release_draft)


