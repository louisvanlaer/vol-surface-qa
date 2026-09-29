import pandas as pd
import streamlit as st

from fonction import (
    choose_date,
    count_alerts,
    create_plot,
    export_to_excel,
    filter_expiry,
    get_available_dates,
    get_available_expiries,
    get_available_instruments,
    highlight_tolerance,
    load_json,
    merge_volatility,
)

st.set_page_config(layout="wide", page_title="Volatility Surface")


def _reset_run():
    st.session_state.run = False


def _trigger_run():
    st.session_state.run = True


def main():
    debut_aout, fin_aout = choose_date()

    st.title("Volatility Surface")

    if "run" not in st.session_state:
        st.session_state.run = False

    with st.sidebar:
        st.header("Configuration")
        st.subheader("Upload json request")

        uploaded_file = st.file_uploader(
            "", type=["json"], on_change=_reset_run
        )

        choose_instrument = st.text_input(
            "Enter an instrument name",
            value="demo_asset_v1",
            on_change=_reset_run,
        )

        tolerance_input = st.text_input(
            "Tolerance (%)", value="0.01", on_change=_reset_run
        )
        try:
            tolerance = float(tolerance_input)
        except ValueError:
            st.error("Veuillez saisir un seuil de tolérance numérique valide.")
            st.stop()

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

        st.button("Run", on_click=_trigger_run)

    if uploaded_file and st.session_state.run:
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
                f"Instruments disponibles : {', '.join(instruments)}"
            )
            st.stop()

        available_dates = get_available_dates(df, choose_instrument)

        if Date1 not in available_dates or Date2 not in available_dates:
            st.warning(
                "Les dates sélectionnées ne sont pas disponibles pour l'instrument choisi."
            )
            st.stop()

        if Date1 >= Date2:
            st.warning(
                "La date de début doit être antérieure à la date de fin."
            )
            st.stop()

        merged_df = merge_volatility(df, choose_instrument, Date1, Date2)

        if merged_df.empty:
            st.warning(
                "Aucune donnée disponible pour les paramètres sélectionnés."
            )
            st.stop()

        # Contrôle qualité et alertes
        number_alerts = count_alerts(merged_df, tolerance)
        if number_alerts > 0:
            st.warning(
                f"{number_alerts} ligne(s) dépasse(nt) le seuil de tolérance de {tolerance:.2f}."
            )
        else:
            st.success(
                f"Aucune ligne ne dépasse la tolérance de {tolerance:.2f}."
            )

        # Tableau des données fusionnées avec mise en évidence
        st.subheader("Merged Volatility Data")
        styled_df = merged_df.style.apply(
            highlight_tolerance, tolerance=tolerance, axis=1
        )
        st.dataframe(styled_df, height=400, use_container_width=True)

        # Visualisations graphiques par échéance
        st.subheader("Visualisation par échéance")
        expiries = get_available_expiries(merged_df)
        selected_expiry = st.selectbox(
            "Sélectionner une échéance", options=expiries
        )

        if selected_expiry:
            df_exp = filter_expiry(merged_df, selected_expiry)
            fig = create_plot(df_exp, Date1, Date2)
            st.pyplot(fig)

        # Export Excel multi-onglets
        st.subheader("Export des résultats")
        df_date1 = df[
            (df["instrument"] == choose_instrument)
            & (df["trade_date"].dt.date == Date1)
        ]
        df_date2 = df[
            (df["instrument"] == choose_instrument)
            & (df["trade_date"].dt.date == Date2)
        ]

        excel_file = export_to_excel(df_date1, df_date2, merged_df)
        st.download_button(
            label="Télécharger le rapport Excel",
            data=excel_file,
            file_name=f"volatility_comparison_{choose_instrument}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )


if __name__ == "__main__":
    main()