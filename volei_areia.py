import streamlit as st
from datetime import datetime
import urllib.parse
import re


def validar_horarios(texto):
    """Valida os horários no texto, retornando válidos e inválidos."""
    padrao_horario = re.compile(r'\b\d{1,2}(h|:00|hr|hrs)\b')
    horarios_validos = []
    horarios_invalidos = []
    for palavra in texto.split():
        if padrao_horario.match(palavra):
            horarios_validos.append(palavra)
        else:
            horarios_invalidos.append(palavra)
    return horarios_validos, horarios_invalidos


def processar_lista(texto):
    """Processa o texto, removendo números e filtrando horários."""
    lista = []
    for linha in texto.strip().splitlines():
        if linha.startswith(tuple(str(i) for i in range(1, 101))) and '. ' in linha:
            linha = linha.split('. ', 1)[-1].strip()
        lista.append(linha)
    return lista


def normalizar_horarios(horarios):
    """Normaliza formatos de horários (ex.: 17hr -> 17h)."""
    horarios_normalizados = []
    for horario in horarios:
        horario = (
            horario.lower()
            .replace(':00', 'h')
            .replace('hr', 'h')
            .replace('hrs', 'h')
            .replace(' h', 'h')
            .replace('h ', 'h')
        )
        horarios_normalizados.append(horario)
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
    template = """
    *Vôlei hoje ({data})*

    {texto_original}

    Horários e valores por participante:
    {horarios}

    Pix: (adicione a chave)
    """
    horarios = "\n".join(f"{hora}: ({qtd}P), R$ {valor:.2f}" for hora, qtd, valor in valores)
    return template.format(data=data, texto_original=texto_original, horarios=horarios)


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
        valor_total = sum(valor for _, _, valor in valores_calculados)

        # Gerar e exibir o relatório
        relatorio = gerar_relatorio(data_atual, texto, valores_calculados)
        st.code(relatorio, language=None)

        # Codificar o texto para compartilhamento
        texto_compartilhar = urllib.parse.quote(relatorio)
        compartilhar_url = f"https://wa.me/?text={texto_compartilhar}"

        col1, col2 = st.columns(2)
        with col1:
            st.success("Cálculo realizado com sucesso! Relatório gerado abaixo.")
        with col2:
            st.markdown(f"[📤 Compartilhar no WhatsApp]({compartilhar_url})", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Ocorreu um erro inesperado: {e}")