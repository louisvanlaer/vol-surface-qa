import streamlit as st
import pandas as pd
from datetime import date
from fonction import choose_date, count_alerts
from fonction import (
    load_json,
    get_available_dates,
    get_available_instruments,
    merge_volatility,
)


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
        try:
            df = load_json(uploaded_file)
        except Exception as error:
            st.error(f"Erreur lors du chargement du JSON : {error}")
            st.stop()

        instruments = get_available_instruments(df)

        if not instruments:
            st.error("Aucun instrument disponible dans le fichier.")
            st.stop()

        if choose_instrument not in instruments:
            st.warning(
                f"L'instrument '{choose_instrument}' n'est pas disponible. "
                "Veuillez choisir un instrument valide."
            )
            st.stop()

        available_dates = get_available_dates(df, choose_instrument)

        if Date1 not in available_dates or Date2 not in available_dates:
            st.warning(
                "Les dates sélectionnées ne sont pas disponibles pour l'instrument choisi."
            )
            st.stop()

        if Date1 >= Date2:
            st.warning("La date de début doit être antérieure à la date de fin.")
            st.stop()

        merged_df = merge_volatility(df, choose_instrument, Date1, Date2)

        if merged_df.empty:
            st.warning("Aucune donnée disponible pour les paramètres sélectionnés.")
            st.stop()

        # Display the merged DataFrame
        st.subheader("Merged Volatility Data")
        st.dataframe(merged_df, height=400, width=800, use_container_width=True)

        number_alerts = count_alerts(merged_df,tolerance)

        if number_alerts > 0:
            st.warning(
            f"{number_alerts} lignes dépassent la tolérance de {tolerance:.2f}."
            f"dépassent la tolérance de {tolerance:.2f}."
        )
        else:
            st.success(
                f"Aucune ligne ne dépasse la tolérance "
                f"de {tolerance:.2f}."
            )

if __name__ == "__main__":
    main()
