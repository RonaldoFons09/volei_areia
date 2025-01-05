import streamlit as st
from datetime import datetime
import urllib.parse

def padronizar_horario(horario):
    return (
        horario.strip()
        .lower()
        .replace(':00', 'h')
        .replace('hr', 'h')
        .replace('hrs', 'h')
        .replace(' h', 'h')
        .replace('h ', 'h')
    )

# Título do app
st.title("Contador de Participantes de Vôlei 🏐")

# Entrada do texto
texto = st.text_area("Digite a lista de participantes e horários:", "", height=300)

# Entrada do valor da hora
valor_hora = st.number_input("Digite o valor da hora (R$):", min_value=0.0, step=1.0, value=45.0)

# Botão para processar o texto
if st.button("Calcular"):
    if not texto.strip():
        st.warning("Por favor, insira a lista de participantes e horários antes de calcular.")
        st.stop()

    data_atual = datetime.now().strftime("%d/%m/%Y")
    lista = [linha.split('. ', 1)[-1].strip() for linha in texto.strip().splitlines()]

    contagem_horarios = {f"{hora}h": 0 for hora in range(24)}

    for item in lista:
        horarios = [
            padronizar_horario(h)
            for h in item.split()
            if any(substring in h.lower() for substring in ['h', ' h', 'hrs', ':00']) or h.isdigit()
        ]
        for horario in horarios:
            contagem_horarios[horario] += 1

    total_participantes = 0
    resultado = f"*Vôlei hoje ({data_atual})* \n\n{texto}"
    resultado += "\n\n\nHorários e valores por participante:\n\n"
    horarios_com_participantes = 0

    for hora, quantidade in contagem_horarios.items():
        if quantidade > 0:
            horarios_com_participantes += 1
            valor_por_participante = valor_hora / quantidade
            total_participantes += valor_por_participante
            resultado += f"{hora}: ({quantidade}P), R$ {valor_por_participante:.2f}\n"

    if horarios_com_participantes > 1:
        resultado += f"Todos os horários: R$ {total_participantes:.2f}\n\n"

    resultado += "\nPix: (adicione a chave)\n"
    st.code(resultado, language="markdown")

    texto_compartilhar = urllib.parse.quote(resultado)
    col1, col2 = st.columns(2)

    with col1:
        st.caption("Clique no botão acima para copiar.")
    with col2:
        compartilhar_url = f"https://wa.me/?text={texto_compartilhar}"
        st.markdown(f"[📤 Compartilhar no WhatsApp]({compartilhar_url})", unsafe_allow_html=True)
