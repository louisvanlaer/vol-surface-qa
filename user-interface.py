import streamlit as st
import pandas as pd
from datetime import date
from fonction import get_request
from fonction import load_json_file
from fonction import choose_date



def _reset_run():
    st.session_state.run = False

def main():

    debut_aout, fin_aout = choose_date()

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
                st.write(request_path)

        except AttributeError:
            st.warning("Please upload a valid JSON file.")

        choose_instrument = st.text_input("Enter an instrument name", value="DEMO_ASSET", on_change=_reset_run)
        threshold = 0

        tolerance = st.text_input("Tolerance(%)", value="0.01", on_change=_reset_run)

        col1, col2 = st.columns(2)
        with col1:
            Date1 = st.date_input(
                "Start Date",
                value=debut_aout,
                min_value=debut_aout,
                max_value=fin_aout,
                on_change=_reset_run,
            )
        with col2: 
            Date2 = st.date_input(
                "End Date",
                value=fin_aout,
                min_value=debut_aout,
                max_value=fin_aout,
                on_change=_reset_run,
            )
        st.button("run")

############################################################################################################################

    if uploaded_file:
        req1 = get_request(request_path,str(Date1),choose_instrument)
        trade_dates, instruments = get_request(request_path,str(Date1),choose_instrument)
        st.write(trade_dates)
        st.write(instruments)
    



if __name__ == "__main__":
    main()
