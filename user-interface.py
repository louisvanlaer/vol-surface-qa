import streamlit as st
import pandas as pd
from datetime import date



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
                st.session_state.request_path = request_path
                data = load_json_file(request_path)
                underlying = data["underlying"]
                spot = data["spot"]
                surface = data["surface"]
                
                surface_df = pd.DataFrame(data["surface"])

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

    st.dataframe(surface_df, use_container_width=True)
    
    # st.write("Instrument :", underlying)
    # st.write("Spot :", spot)
    # st.write("Surface :", surface)



if __name__ == "__main__":
    main()
