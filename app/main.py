
import streamlit as st


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Scop - Single Player",
    page_icon="🎲",
    layout="wide",
)


# --------------------------------------------------
# Application Header
# --------------------------------------------------

st.title("Scop")
st.subheader("Single Player Game System")

st.markdown(
    """
    Welcome to **Scop**.

    This is the initial development interface for the
    single-player game system.
    """
)

st.divider()


# --------------------------------------------------
# Module Status
# --------------------------------------------------

st.header("System Modules")

modules = [
    ("B0", "Game Initialization", "In development"),
    ("B1", "Context Management", "Planned"),
    ("B2", "Player Action Parsing", "Planned"),
    ("B3", "Action Judgment & Checks", "Planned"),
    ("B4", "Game State Management", "Planned"),
    ("B5", "Narrative Generation", "Planned"),
    ("B6", "Save & Recovery", "Planned"),
]

for code, name, status in modules:
    col1, col2, col3 = st.columns([1, 4, 2])

    with col1:
        st.markdown(f"**{code}**")

    with col2:
        st.write(name)

    with col3:
        st.caption(status)


st.divider()

st.caption("Scop B Layer | Development Prototype")
