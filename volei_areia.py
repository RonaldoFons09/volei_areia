import streamlit as st
from datetime import datetime
import urllib.parse

# Título do app
st.title("Contador de Participantes de Vôlei 🏐")

# Entrada do texto
texto = st.text_area("Digite a lista de participantes e horários:", "", height=300)

# Entrada do valor da hora
valor_hora = st.number_input("Digite o valor da hora (R$):", min_value=0.0, step=1.0, value=45.0)

# Botão para processar o texto
if st.button("Calcular"):
    # Validação inicial
    if not texto.strip():
        st.error("Por favor, insira uma lista válida com horários no formato 'XXh'.")
        st.stop()

    # Obter a data atual
    data_atual = datetime.now().strftime("%d/%m/%Y")

    # Converte o texto em uma lista, removendo números e espaços extras
    lista = [linha.split('. ', 1)[-1].strip() for linha in texto.strip().splitlines()]

    # Dicionário para contabilizar os horários
    contagem_horarios = {f"{hora}h": 0 for hora in range(24)}

    # Processa cada entrada
    for item in lista:
        horarios = [h.strip().lower().replace(':00', 'h').replace(' h', 'h') for h in item.split() if 'h' in h]
        horarios = [h for h in horarios if h[:-1].isdigit() and 0 <= int(h[:-1]) < 24]
        for horario in horarios:
            contagem_horarios[horario] += 1

    # Monta o resultado
    resultado = f"*Vôlei hoje ({data_atual})* \n\n{texto}\n\nHorários e valores por participante:\n\n"
    horarios_com_participantes = 0
    total_participantes = 0

    for hora, quantidade in contagem_horarios.items():
        if quantidade > 0:
            horarios_com_participantes += 1
            valor_por_participante = valor_hora / quantidade
            total_participantes += valor_hora  # Soma os valores diretamente
            resultado += f"{hora}: ({quantidade}P), R$ {valor_por_participante:.2f}\n"

    if horarios_com_participantes > 1:
        resultado += f"Todos os horários: R$ {total_participantes:.2f}\n\n"

    chave_pix = st.text_input("Digite sua chave Pix (opcional):", "")
    resultado += f"\nPix: {chave_pix or '(adicione a chave)'}\n"

    st.code(resultado, language="markdown")

    # Verificar tamanho do texto para compartilhamento
    if len(resultado) > 4096:
        st.warning("O texto gerado é muito longo e pode não ser compartilhado corretamente pelo WhatsApp.")
    else:
        texto_compartilhar = urllib.parse.quote(resultado, safe="")
        compartilhar_url = f"https://wa.me/?text={texto_compartilhar}"
        st.markdown(f"[📤 Compartilhar no WhatsApp]({compartilhar_url})", unsafe_allow_html=True)
