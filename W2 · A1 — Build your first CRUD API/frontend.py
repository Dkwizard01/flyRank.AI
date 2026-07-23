import streamlit as sl
import requests as rq
sl.header("Api test site.")
button1 = sl.button("Call the root API")
url = "http://127.0.0.1:8000"
if button1:
       sl.write(rq.get(url).json())
button2 = sl.button("Call the health API.")
if button2:
       sl.write(rq.get(url + "/health").json())