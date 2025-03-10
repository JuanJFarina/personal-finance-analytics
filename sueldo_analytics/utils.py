from datetime import datetime
import pandas as pd
from matplotlib import pyplot as plt

datos_personales = pd.read_csv("../data/sueldos.csv")
bias: int = 0


def set_bias(last_check: datetime) -> None:
    global bias
    current_date = datetime.now()
    years_diff = current_date.year - last_check.year
    months_diff = current_date.month - last_check.month
    bias = years_diff * 12 + months_diff

def get_bias() -> int:
    global bias
    return bias


def obtener_escalar_de_inflacion(
    meses: int, datos_inflacion: pd.DataFrame = datos_personales
) -> float:
    global bias
    escalar = 1
    for m in range(meses + bias, 0, -1):
        inflacion_mes_anterior = datos_inflacion["inflacion_del_mes_anterior"].iloc[-m]
        escalar *= 1 + (inflacion_mes_anterior * 0.01)
    return escalar


def agregar_meses_segun_inflacion(
    data: pd.DataFrame,
    meses: int,
    campo: str,
    fecha: str | None = None,
    datos_inflacion: pd.DataFrame = datos_personales,
) -> pd.DataFrame:
    global bias
    new_data = data.copy()
    for m in range(meses + bias, 0, -1):
        new_row = new_data.iloc[-1].copy()
        inflacion_mes = datos_inflacion["inflacion_del_mes_anterior"].iloc[-m]
        new_row[campo] *= 1 + (inflacion_mes * 0.01)
        if fecha:
            new_row[fecha] = "ajustado"

        new_data = pd.concat(
            [new_data, pd.DataFrame([new_row], columns=new_data.columns)]
        )
    return new_data.copy()

def show_plot(plot_id: int, xlabel: str, ylabel: str, title: str) -> None:
    plt.figure(plot_id)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()
