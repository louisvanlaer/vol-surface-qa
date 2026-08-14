import streamlit as st

def _reset_run():
    st.session_state.run = False

def main():

    st.title("Volatility Surface")

    if "run" not in st.session_state:
        st.session_state.run = False

    with st.sidebar:
        ###Config
        st.set_page_config(layout="wide")
        st.header("Configuration")
        st.subheader("Upload json request")

        try:
            uploaded_file = st.file_uploader("", type=["json"], on_change=_reset_run)
            request_path = None

            if uploaded_file is not None:
                request_path = uploaded_file.name
                st.session_state.request_path = request_path

        except AttributeError:
            st.warning("Please upload a valid JSON file.")

        choose_instrument = st.text_input("Enter an instrument name", value="AAPL", on_change=_reset_run)
        threshold = 0

        tolerance = st.text_input("Tolerance(%)", value="0.01", on_change=_reset_run)

        col1, col2 = st.columns(2)
        with col1:
            Date1 = st.date_input("Start Date", on_change=_reset_run)
        with col2: 
            Date2 = st.date_input("End Date", on_change=_reset_run)




if __name__ == "__main__":
    main()