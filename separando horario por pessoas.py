import re
import streamlit as st

def validar_horarios(texto):
    """Identifica e retorna horários válidos e inválidos em um texto"""
    padrao = re.compile(r'\b\d{1,2}(h|:00|hr|hrs)\b')
    validos = []
    invalidos = []
    for palavra in texto.split():
        if padrao.match(palavra):
            validos.append(palavra)
        else:
            invalidos.append(palavra)
    return validos, invalidos

def processar_lista(texto):
    """Processa o texto removendo números iniciais e espaços extras"""
    linhas = []
    for linha in texto.strip().split('\n'):
        linha = linha.strip()
        if linha and linha[0].isdigit() and '. ' in linha:
            linha = linha.split('. ', 1)[-1]
        linhas.append(linha)
    return linhas

def normalizar_horarios(horarios):
    """Padroniza os formatos de horário para XXh"""
    normalizados = []
    for hora in horarios:
        hora_norm = hora.lower().replace(':00', 'h').replace('hrs', 'h').replace('hr', 'h').strip()
        if hora_norm.endswith('h'):
            num = hora_norm[:-1]
            if num.isdigit() and 0 <= int(num) <= 23:
                normalizados.append(f"{int(num)}h")
    return normalizados

st.title("Processamento de Horários")

default_input = """
Ianca 17h 18h 
Davi 17h
Gabriel 17h 18h
gabbs 17h 18h
Marcelo 17h 18h
Ana 18h
Paulo 17h 18h
Mailson 17h 18h
Daniel Farias 17h 18h
Mateus 17h 18h
Natan 18h
Janaice 18h
Jordanna 18h
Junior 17h
Vinícius 17h
Pinço 17h
"""

input_text = st.text_area("Digite os dados (nome e horários):", default_input, height=300)

if st.button("Processar"):
    pessoas = []
    for linha in processar_lista(input_text):
        horas_validas, partes_invalidas = validar_horarios(linha)
        if not horas_validas:
            continue

        nome = ' '.join(partes_invalidas).strip()
        horas = normalizar_horarios(horas_validas)

        if nome and horas:
            pessoas.append((nome, horas))

    if pessoas:
        # Organizar os horários disponíveis
        horarios_disponiveis = sorted(
            {hora for _, horas in pessoas for hora in horas},
            key=lambda x: int(x[:-1])
        )

        grupo_por_horario = {hora: [] for hora in horarios_disponiveis}

        for nome, horas in pessoas:
            for hora in horas:
                grupo_por_horario[hora].append(nome)

        # Exibir os resultados
        for hora in horarios_disponiveis:
            participantes = grupo_por_horario[hora]
            st.subheader(f"{hora} - {len(participantes)} Pessoas")
            for i, nome in enumerate(participantes, 1):
                st.write(f"{i}. {nome}")
            st.markdown("---")
    else:
        st.warning("Nenhum dado processado.")
