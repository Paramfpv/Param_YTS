from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from youtube_transcript_api.formatters import TextFormatter

import streamlit as st
import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

st.cache_data.clear()
st.cache_resource.clear()

st.header("Youtube Video Summarizer")

system_prompt = """You are Yotube video summarizer. You will be taking the transcript text
    and summarizing the entire video and providing the important summary in points
    with heading. First read the whole transcript and then summarize it. The content should be well organised. """

url = st.text_input("Enter the URL of the youtube video: ")
    
extra = st.text_input("enter extra instructions here")
system_prompt = system_prompt + extra


def get_transcript(url):
        video_id = url.split("/")[3]
        video_id = video_id.split("?")[0]
        st.write("video id = "+video_id)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = TextFormatter()
        final = formatter.format_transcript(transcript)
        return final

def get_summary(final):
        prompt = system_prompt + final
        llm = ChatMistralAI(model_name="mistral-large-latest")
        result = llm.invoke(prompt)
        ans = result
        return ans.content

if st.button("Print Transcript"):
        transcript = get_transcript(url)
        st.write(transcript)

if st.button("Print Summary"):
        transcript = get_transcript(url)
        summary = get_summary(transcript)
        st.write(summary)



