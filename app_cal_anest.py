import streamlit as st

def calcular_dose_maxima(sal_anestesico, concentracao, peso, vasoconstritor=None, asa=None):
    doses = {
        'lidocaina': {'dose_maxima': 7.0, 'concentracao': {'2%': 20, '3%': 30}, 'dose_maxima_absoluta': 500},
        'mepivacaina': {'dose_maxima': 6.6, 'concentracao': {'3%': 30, '2%': 20}, 'dose_maxima_absoluta': 400},
        'prilocaina': {'dose_maxima': 8.0, 'concentracao': {'3%': 30, '4%': 40}, 'dose_maxima_absoluta': 600},
        'articaina': {'dose_maxima': 7.0, 'concentracao': {'4%': 40}, 'dose_maxima_absoluta': None},
        'bupivacaina': {'dose_maxima': 2.0, 'concentracao': {'0.5%': 5}, 'dose_maxima_absoluta': 90}
    }

    vasoconstritores = {
        '1:50000 epinefrina': {'ASA I/II': 5.5, 'ASA III/IV': 1},
        '1:100000 epinefrina': {'ASA I/II': 11, 'ASA III/IV': 2},
        '1:200000 epinefrina': {'ASA I/II': 22, 'ASA III/IV': 4},
        '1:30000 noradrenalina': {'ASA I/II': 5.5, 'ASA III/IV': 2},
        '1:2500 fenilefrina': {'ASA I/II': 5.5, 'ASA III/IV': 2},
        '0.03UI/ml felipressina': {'ASA I/II': float('inf'), 'ASA III/IV': 5}
    }

    if peso > 80:
        peso = 80

    if sal_anestesico not in doses or concentracao not in doses[sal_anestesico]['concentracao']:
        return "Sal anestésico ou concentração desconhecida."

    dose_maxima_kg = doses[sal_anestesico]['dose_maxima']
    dose_por_ml = doses[sal_anestesico]['concentracao'][concentracao]
    dose_maxima_absoluta = doses[sal_anestesico]['dose_maxima_absoluta']

    dose_maxima_mg = min(dose_maxima_kg * peso, dose_maxima_absoluta or float('inf'))
    volume_maximo_ml = dose_maxima_mg / dose_por_ml
    numero_de_tubetes = volume_maximo_ml / 1.8

    if vasoconstritor and vasoconstritor in vasoconstritores and asa:
        numero_de_tubetes = min(numero_de_tubetes, vasoconstritores[vasoconstritor].get(asa, float('inf')))

    return dose_maxima_mg, int(numero_de_tubetes)

st.title("Calculadora de Dose Máxima de Anestésico Local")

sal_anestesicos = ['lidocaina', 'mepivacaina', 'prilocaina', 'articaina', 'bupivacaina']
concentracoes_disponiveis = {
    'lidocaina': ['2%', '3%'],
    'mepivacaina': ['3%', '2%'],
    'prilocaina': ['3%', '4%'],
    'articaina': ['4%'],
    'bupivacaina': ['0.5%']
}
vasoconstritores = ['Nenhum', '1:50000 epinefrina', '1:100000 epinefrina', '1:200000 epinefrina', '1:30000 noradrenalina', '1:2500 fenilefrina', '0.03UI/ml felipressina']
asa_classes = ['ASA I/II', 'ASA III/IV']

sal_anestesico = st.selectbox("Sal Anestésico", sal_anestesicos)
concentracao = st.selectbox("Concentração", concentracoes_disponiveis.get(sal_anestesico, []))
peso = st.number_input("Peso do Paciente (kg)", min_value=1.0, max_value=80.0, value=70.0)
vasoconstritor = st.selectbox("Vasoconstritor", vasoconstritores)
asa = st.selectbox("Classificação ASA", asa_classes) if vasoconstritor != "Nenhum" else None

if st.button("Calcular"):
    if not sal_anestesico or not concentracao:
        st.error("Por favor, selecione um sal anestésico e uma concentração válida.")
    else:
        resultado = calcular_dose_maxima(sal_anestesico, concentracao, peso, vasoconstritor if vasoconstritor != "Nenhum" else None, asa)
        if isinstance(resultado, str):
            st.error(resultado)
        else:
            dose_maxima_mg, numero_de_tubetes = resultado
            st.success(f"Dose máxima: {dose_maxima_mg:.2f} mg\nNúmero máximo de tubetes: {numero_de_tubetes}")
            st.caption("Referência: Manual de anestesia local / Stanley F. Malamed; [tradução Fernando Mundim...et al.]. Rio de Janeiro: Elsevier, 2013.")
