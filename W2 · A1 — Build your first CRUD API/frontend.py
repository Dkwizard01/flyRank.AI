import streamlit as sl
import requests as rq
sl.header("Api test site.")
button = sl.button("Call API")
url = "http://127.0.0.1:8000"
if button:
       sl.write(rq.get(url).json())