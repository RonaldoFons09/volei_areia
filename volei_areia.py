import streamlit as st
from datetime import datetime
import urllib.parse

# Título do app
st.title("Contador de Participantes de Vôlei 🏐")

# Entrada do texto
texto = st.text_area("Digite a lista de participantes e horários:", """ """, height=300)

# Entrada do valor da hora
valor_hora = st.number_input("Digite o valor da hora (R$):", min_value=0.0, step=1.0, value=45.0)

# Função para normalizar horários
def normalizar_horario(texto):
    horarios = []
    for palavra in texto.split():
        if any(substring in palavra.lower() for substring in ['h', 'hr', 'hrs', ':00']):
            horario = (
                palavra.lower()
                .replace(':00', 'h')
                .replace('hr', 'h')
                .replace('hrs', 'h')
                .replace(' h', 'h')
                .replace('h ', 'h')
            )
            horarios.append(horario)
    return horarios

# Botão para processar o texto
if st.button("Calcular"):
    if not texto.strip():
        st.warning("Por favor, insira a lista de participantes e horários antes de calcular.")
        st.stop()

    # Obter a data atual
    data_atual = datetime.now().strftime("%d/%m/%Y")

    # Converte o texto em uma lista, removendo os números e espaços extras
    lista = []
    for linha in texto.strip().splitlines():
        linha = linha.strip()
        # Verifica se a linha começa com um número seguido de ". "
        if linha.startswith(tuple(str(i) for i in range(1, 101))) and '. ' in linha:
            linha = linha.split('. ', 1)[-1].strip()
        lista.append(linha)

    # Detectar linhas inválidas (sem horários)
    linhas_invalidas = [linha for linha in lista if not any(substring in linha for substring in ['h', 'hr', 'hrs', ':00'])]
    if linhas_invalidas:
        st.warning(f"Linhas inválidas detectadas e ignoradas: {', '.join(linhas_invalidas)}")

    # Filtrar apenas linhas válidas
    lista = [linha for linha in lista if linha not in linhas_invalidas]

    # Dicionário para contabilizar os horários
    contagem_horarios = {f"{hora}h": 0 for hora in range(24)}

    # Processa cada entrada
    for item in lista:
        horarios = normalizar_horario(item)
        for horario in horarios:
            contagem_horarios[horario] += 1

    # Variável para somar os valores dos participantes
    total_participantes = 0

    # String para armazenar a saída formatada
    resultado = f"*Vôlei hoje ({data_atual})* \n\n{texto}"

    # Contagem de horários e valores por participante
    resultado += "\n\n\nHorários e valores por participante:\n\n"
    horarios_com_participantes = 0
    for hora, quantidade in contagem_horarios.items():
        if quantidade > 0:  # Mostra apenas horários que aparecem na lista
            horarios_com_participantes += 1
            valor_por_participante = valor_hora / quantidade
            total_participantes += valor_por_participante  # Soma o valor de cada participante
            resultado += f"{hora}: ({quantidade}P), R$ {valor_por_participante:.2f}\n"

    # Adiciona o total somente se houver mais de um horário com participantes
    if horarios_com_participantes > 1:
        resultado += f"Todos os horários: R$ {total_participantes:.2f}\n\n"

    resultado += "\nPix: (adicione a chave)\n"

    # Exibir o resultado formatado dentro de uma caixinha
    st.code(resultado, language="markdown")

    # Codificar o texto para ser compartilhado via URL
    texto_compartilhar = urllib.parse.quote(resultado)

    # Adicionar botões de copiar e compartilhar
    col1, col2 = st.columns(2)

    # Botão de copiar (já nativo no st.code)
    with col1:
        st.caption("Clique no botão acima para copiar.")

    # Botão de compartilhar
    with col2:
        compartilhar_url = f"https://wa.me/?text={texto_compartilhar}"
        st.markdown(f"[📤 Compartilhar no WhatsApp]({compartilhar_url})", unsafe_allow_html=True)
