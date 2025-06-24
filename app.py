
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="🥃 Jeopardy x bOurBon biChessss", layout="wide")

@st.cache_data
def load_clues(folder="clues"):
    files = [f for f in os.listdir(folder) if f.endswith(".csv")]
    df_list = [pd.read_csv(os.path.join(folder, f)) for f in files]
    return pd.concat(df_list, ignore_index=True)

df = load_clues("clues")
categories = df["Category"].unique()
values = sorted(df["Value"].unique())

# Initialize session state
if "selected_clue" not in st.session_state:
    st.session_state.selected_clue = None
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False
if "used_clues" not in st.session_state:
    st.session_state.used_clues = {}

st.title("🥃 Jeopardy x bOurBon biChessss 🎉")

if st.session_state.selected_clue is not None:
    row = df.loc[st.session_state.selected_clue]

    st.markdown("## 🧐 Jeopardy Clue")
    st.markdown("---")
    st.markdown(f"<div style='font-size:36px;text-align:center'>{row['Clue']}</div>", unsafe_allow_html=True)

    if not st.session_state.show_answer:
        if st.button("🔁 Flip Card to Reveal Answer"):
            st.session_state.show_answer = True
    else:
        st.markdown(f"<div style='font-size:32px;text-align:center;color:green'>✅ {row['Answer']}</div>", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("⬅️ Back to Board"):
        used_key = f"{row['Category']}_{row['Value']}"
        st.session_state.used_clues[used_key] = True
        st.session_state.selected_clue = None
        st.session_state.show_answer = False

else:
    # Display category headers
    cols = st.columns(len(categories))
    for i, cat in enumerate(categories):
        cols[i].markdown(f"### {cat}")

    for val in values:
        cols = st.columns(len(categories))
        for i, cat in enumerate(categories):
            key = f"{cat}_{val}"
            clue_row = df[(df["Category"] == cat) & (df["Value"] == val)]
            used = st.session_state.used_clues.get(key, False)
            label = f"${val}" if not used else f"❌ ${val}"

            if not clue_row.empty:
                if cols[i].button(label, key=key, disabled=used):
                    st.session_state.selected_clue = clue_row.index[0]
