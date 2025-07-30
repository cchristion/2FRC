"""Python script to display latest breachs from HIBP."""

import re

import pandas as pd
import requests
import streamlit as st

# ------ Page Config ------

st.set_page_config(
    page_title="2FRC: 2 File Regex compare",
    page_icon=":mag:",
    layout="wide",
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ------ End of Page Config ------

st.markdown("""# 2FRC: 2 File Regex compare""")

pattern = st.text_area(
    "Regex Pattern",
    value=r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}",
)
pattern = re.compile(pattern, re.IGNORECASE)

col1, col2 = st.columns(2)

with col1:
    url1 = st.text_area("Paste file URL", key="u1")
    url1_data = None
    if url1:
        url1_data = requests.get(url1, timeout=10).content.decode("utf-8")
    file1 = st.file_uploader("or Choose a file to compare", key="f1")
    if file1 is not None:
        file1 = file1.read().decode("utf-8", errors="replace")
    txt1 = st.text_area("or Paste text here", key="t1")
    data1 = url1_data or file1 or txt1

    # Adding new lines because regex is skipping the initial couple
    # of letters when matching patterns in the provided text
    data1 = "\n\n" + data1

with col2:
    url2 = st.text_area("Paste file URL", key="u2")
    url2_data = None
    if url2:
        url2_data = requests.get(url2, timeout=10).content.decode("utf-8")
    file2 = st.file_uploader("or Choose a file to compare", key="f2")
    if file2 is not None:
        file2 = file2.read().decode("utf-8", errors="replace")
    txt2 = st.text_area("or Paste text here", key="t2")
    data2 = url2_data or file2 or txt2

    # Adding new lines because regex is skipping the initial couple
    # of letters when matching patterns in the provided text
    data2 = "\n\n" + data2

if data1.strip() or data2.strip():
    st.markdown("""---""")
    col1, col2 = st.columns(2)

    with col1:
        if data1 and pattern:
            data1 = pattern.findall(data1, re.IGNORECASE)

            st.markdown("""### All Matchs""")
            data1_df = pd.DataFrame(data1, columns=["Matchs"])
            st.markdown(f"Count: {len(data1_df):,}")
            st.dataframe(data1_df, use_container_width=True)

            st.markdown("""### Unique Matchs""")
            data1_df = pd.DataFrame(
                set(map(str.lower, data1)), columns=["Unique Matchs"]
            )
            st.markdown(f"Count: {len(data1_df):,}")
            st.dataframe(data1_df, use_container_width=True)

    with col2:
        if data2 and pattern:
            data2 = pattern.findall(data2, re.IGNORECASE)

            st.markdown("""### All Matchs""")
            data2_df = pd.DataFrame(data2, columns=["Matchs"])
            st.markdown(f"Count: {len(data2_df):,}")
            st.dataframe(data2_df, use_container_width=True)

            st.markdown("""### Unique Matchs""")
            data2_df = pd.DataFrame(
                set(map(str.lower, data2)), columns=["Unique Matchs"]
            )
            st.markdown(f"Count: {len(data2_df):,}")
            st.dataframe(data2_df, use_container_width=True)

    if data1 and data2:
        st.markdown("""---""")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""### Matches that are not in the other""")
            diff1_df = set(map(str.lower, data1)) - set(map(str.lower, data2))
            diff1_df = pd.DataFrame(diff1_df, columns=["Matchs"])
            st.markdown(f"Count: {len(diff1_df):,}")
            st.dataframe(diff1_df, use_container_width=True)

        with col2:
            st.markdown("""### Matches that are not in the other""")
            diff2_df = set(map(str.lower, data2)) - set(map(str.lower, data1))
            diff2_df = pd.DataFrame(diff2_df, columns=["Matchs"])
            st.markdown(f"Count: {len(diff2_df):,}")
            st.dataframe(diff2_df, use_container_width=True)

        st.markdown("""### Common Matchs""")
        data_all_df = set(map(str.lower, data1)) & set(map(str.lower, data2))
        st.markdown(f"Count: {len(data_all_df):,}")
        data_all_df = pd.DataFrame(set(data1) & set(data2), columns=["Common Matchs"])
        st.dataframe(data_all_df, use_container_width=True)

st.markdown(
    """---
by **Christion C** | [LinkedIn](https://www.linkedin.com/in/cchristion) | [GitHub](https://github.com/cchristion)
""",
    help=None,
)
