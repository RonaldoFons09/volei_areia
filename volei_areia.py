import streamlit as st
from datetime import datetime
import urllib.parse
import re


def validar_horarios(texto):
    """Valida os horários no texto (ex.: 17h, 17hr, 17hrs, 17hs), retornando válidos e inválidos."""
    # aceita número de 1 ou 2 dígitos seguido de h, hs, hr ou hrs
    padrao_horario = re.compile(r'\b\d{1,2}(?:h|hs|hr|hrs)\b', re.IGNORECASE)
    horarios_validos = []
    horarios_invalidos = []
    for palavra in texto.split():
        if padrao_horario.fullmatch(palavra):
            horarios_validos.append(palavra)
        else:
            horarios_invalidos.append(palavra)
    return horarios_validos, horarios_invalidos


import re


def processar_lista(texto):
    """
    Processa o texto de entrada:

    1. Remove numeração “1. ” a “100. ” do início de cada linha.
    2. Garante que **todos** os horários mencionados em cada linha estejam num dos formatos:
       17h, 17hr, 17hrs ou 17hs (sem espaço entre número e sufixo).
    3. Se qualquer horário inválido aparecer (i.e. qualquer token com dígito que não case),
       lança ValueError listando as linhas inválidas.
    4. Caso contrário, retorna a lista de linhas já “limpas” (sem prefixos numéricos).
    """

    def _remover_prefixo(linha: str) -> str:
        return re.sub(r'^\s*(?:[1-9][0-9]?|100)\.\s+', '', linha).strip()

    # 1) limpa prefixos e descarta linhas em branco
    linhas = [
        _remover_prefixo(linha)
        for linha in texto.strip().splitlines()
        if linha.strip()
    ]

    linhas_invalidas = []
    for l in linhas:
        validos, invalidos = validar_horarios(l)
        # Agora só considera inválido se o token inválido contiver dígito
        if any(re.search(r'\d', tok) for tok in invalidos):
            linhas_invalidas.append(l)

    if linhas_invalidas:
        raise ValueError(
            "Linhas inválidas detectadas (sem horário válido). Por favor, corrija essas linhas e tente novamente.\n  - "
            + "\n  - ".join(linhas_invalidas)
        )

    return linhas


def normalizar_horarios(horarios):
    """Normaliza formatos de horários (converte hr/hrs/hs para h)."""
    horarios_normalizados = []
    for h in horarios:
        h = h.lower().strip()
        # converte todas as variações para "h"
        # primeiro, tratar plural "hrs" e "hs", depois singular "hr"
        h = re.sub(r'hrs$|hs$', 'h', h)
        h = re.sub(r'hr$', 'h', h)
        # caso ainda reste algum espaço antes/depois
        h = h.replace(' h', 'h').replace('h ', 'h')
        horarios_normalizados.append(h)
    return horarios_normalizados


def calcular_valores(lista, valor_hora):
    """Calcula os valores por participante e total."""
    contagem_horarios = {f"{hora}h": 0 for hora in range(24)}
    for item in lista:
        validos, _ = validar_horarios(item)
        horarios = normalizar_horarios(validos)
        for horario in horarios:
            contagem_horarios[horario] += 1

    resultado = []
    for hora, quantidade in contagem_horarios.items():
        if quantidade > 0:
            valor_por_participante = valor_hora / quantidade
            resultado.append((hora, quantidade, valor_por_participante))
    return resultado


def gerar_relatorio(data, texto_original, valores):
    """Gera o relatório formatado."""
    # Verifica se existem mais de um horário
    exibir_total = len(valores) > 1
    total_horarios = sum(valor for _, _, valor in valores) if exibir_total else 0

    template = (
        "*Vôlei {data}*\n\n"
        "{texto_original}\n\n"
        "*Valores por participante:*\n"
        "{horarios}\n"
    )

    if exibir_total:
        template += "Todos os horários: R$ {total_horarios:.2f}\n\n"

    template += "\n\nPix: ventusbc@gmail.com"

    horarios = "\n".join(f"{hora}: ({qtd}P), R$ {valor:.2f}" for hora, qtd, valor in valores)
    return template.format(
        data=data,
        texto_original=texto_original,
        horarios=horarios,
        total_horarios=total_horarios,
    )


# --- Streamlit App ---
st.title("Contador de Participantes de Vôlei 🏐")

# Entrada do texto
texto = st.text_area("Digite a lista de participantes e horários:", "", height=300)

# Entrada do valor da hora
valor_hora = st.number_input("Digite o valor da hora (R$):", min_value=0.0, step=1.0, value=45.0)

if st.button("Calcular"):
    if not texto.strip():
        st.warning("Por favor, insira a lista de participantes e horários antes de calcular.")
        st.stop()

    try:
        # Obter a data atual
        data_atual = datetime.now().strftime("%d/%m/%Y")

        # Processar a lista
        lista = processar_lista(texto)

        # Verificar linhas inválidas
        linhas_invalidas = [linha for linha in lista if not validar_horarios(linha)[0]]
        if linhas_invalidas:
            st.warning(f"Linhas inválidas detectadas e ignoradas: {', '.join(linhas_invalidas)}")

        # Calcular os valores
        valores_calculados = calcular_valores(lista, valor_hora)

        # Gerar e exibir o relatório
        relatorio = gerar_relatorio(data_atual, texto, valores_calculados)
        st.code(relatorio, language=None)

        # Codificar o texto para compartilhamento
        texto_compartilhar = urllib.parse.quote(relatorio)
        compartilhar_url = f"https://wa.me/?text={texto_compartilhar}"

        col1, col2 = st.columns(2)
        with col1:
            st.success("Cálculo realizado com sucesso! Relatório gerado.")
        with col2:
            st.markdown(f"[📤 Compartilhar no WhatsApp]({compartilhar_url})", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Ocorreu um erro inesperado: {e}")
