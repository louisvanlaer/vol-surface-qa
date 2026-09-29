import calendar
from datetime import date
import io
import json
import matplotlib.pyplot as plt
import pandas as pd


def load_json(file):
    """Charge un fichier JSON et retourne un DataFrame propre.

    Colonnes attendues : instrument, trade_date, strike, expiry, vol
    """
    data = json.load(file)

    if isinstance(data, dict) and "data" in data:
        data = data["data"]

    df = pd.DataFrame(data)

    required_columns = {
        "instrument",
        "trade_date",
        "strike",
        "expiry",
        "vol",
    }

    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(
            "Colonnes manquantes dans le JSON : " + ", ".join(sorted(missing))
        )

    df["trade_date"] = pd.to_datetime(df["trade_date"], errors="coerce")
    df["expiry"] = pd.to_datetime(df["expiry"], errors="coerce")
    df["strike"] = pd.to_numeric(df["strike"], errors="coerce")
    df["vol"] = pd.to_numeric(df["vol"], errors="coerce")

    df = df.dropna(
        subset=["instrument", "trade_date", "strike", "expiry", "vol"]
    )

    return df


def choose_date():
    annee, mois = 2026, 8
    dernier_jour = calendar.monthrange(annee, mois)[1]
    debut_mois = date(annee, mois, 1)
    fin_mois = date(annee, mois, dernier_jour)
    return debut_mois, fin_mois


def get_available_dates(df, instrument=None):
    temp = df
    if instrument is not None:
        temp = temp[temp["instrument"] == instrument]
    return sorted(temp["trade_date"].dt.date.unique())


def get_available_instruments(df):
    """Retourne les instruments disponibles."""
    return sorted(df["instrument"].dropna().unique())


def merge_volatility(df, instrument, date1, date2):
    df_date1 = df[
        (df["instrument"] == instrument) & (df["trade_date"].dt.date == date1)
    ][["instrument", "strike", "expiry", "vol"]].copy()

    df_date2 = df[
        (df["instrument"] == instrument) & (df["trade_date"].dt.date == date2)
    ][["instrument", "strike", "expiry", "vol"]].copy()

    merged_df = pd.merge(
        df_date1,
        df_date2,
        on=["instrument", "strike", "expiry"],
        how="inner",
        suffixes=("_date1", "_date2"),
    )

    merged_df["diff"] = (
        merged_df["vol_date1"] - merged_df["vol_date2"]
    ).abs()
    merged_df = merged_df.sort_values(by=["expiry", "strike"]).reset_index(
        drop=True
    )

    return merged_df


def get_available_expiries(merged_df):
    """Retourne les échéances communes aux deux dates."""
    return sorted(merged_df["expiry"].dt.date.unique())


def filter_expiry(df, expiry):
    """Filtre le DataFrame sur une échéance donnée."""
    return df[df["expiry"].dt.date == expiry].copy()


def count_alerts(df, tolerance):
    """Compte le nombre de lignes dont la différence de volatilité dépasse la tolérance."""
    return int((df["diff"] > tolerance).sum())


def highlight_tolerance(row, tolerance):
    """Colore toute la ligne en rouge lorsque diff > tolerance."""
    if row["diff"] > tolerance:
        return [
            "background-color: #ff4b4b; color: white; font-weight: 600;"
        ] * len(row)
    return [""] * len(row)


def create_plot(df_expiry, date1, date2):
    """Trie les données par strike et génère un graphique comparatif des volatilités."""
    df_sorted = df_expiry.sort_values(by="strike")

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(
        df_sorted["strike"],
        df_sorted["vol_date1"],
        "o-",
        label=f"Date 1 ({date1})",
    )
    ax.plot(
        df_sorted["strike"],
        df_sorted["vol_date2"],
        "o-",
        label=f"Date 2 ({date2})",
    )

    ax.set_xlabel("Strike")
    ax.set_ylabel("Volatilité (%)")
    ax.set_title(
        f"Comparaison de volatilité - Échéance : {df_sorted['expiry'].dt.date.iloc[0]}"
    )
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.6)

    return fig


def export_to_excel(df_date1, df_date2, merged_df):
    """Regroupe les DataFrames dans un fichier Excel multi-onglets."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_date1.to_excel(writer, sheet_name="Date 1", index=False)
        df_date2.to_excel(writer, sheet_name="Date 2", index=False)
        merged_df.to_excel(writer, sheet_name="Merge", index=False)
    output.seek(0)
    return output