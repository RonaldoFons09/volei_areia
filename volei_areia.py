import streamlit as st
from datetime import datetime

# Título do app
st.title("Contador de Participantes de Vôlei 🏐")

# Entrada do texto
texto = st.text_area("Digite a lista de participantes e horários:", """
1. Natan 18h
2. Ronaldo 18h
3. Gabriel 17h
4. Daniel Farias 17h - 18h
5. Gabi 17h - 18h
6. Mailson 17h - 18h
13. Thailan 17h
14. Débora 17h
15. Fabio 17h
""", height=300)

# Entrada do valor da hora
valor_hora = st.number_input("Digite o valor da hora (R$):", min_value=0.0, step=1.0, value=45.0)

# Botão para processar o texto
if st.button("Calcular"):
    # Obter a data atual
    data_atual = datetime.now().strftime("%d/%m/%Y")
    
    # Converte o texto em uma lista, removendo os números e espaços extras
    lista = [linha.split('. ', 1)[-1].strip() for linha in texto.strip().splitlines()]

    # Dicionário para contabilizar os horários
    contagem_horarios = {f"{hora}h": 0 for hora in range(24)}

    # Processa cada entrada
    for item in lista:
        # Captura os horários no formato "17h", "18h", etc.
        horarios = [h.strip() for h in item.split() if h.endswith('h')]
        for horario in horarios:
            contagem_horarios[horario] += 1

    # Variável para somar os valores dos participantes
    total_participantes = 0

    # String para armazenar a saída formatada
    resultado = f"**Vôlei hoje ({data_atual})**\n\n"

    # Contagem de horários e valores por participante
    resultado += "### Contagem de horários e valores por participante:\n"
    for hora, quantidade in contagem_horarios.items():
        if quantidade > 0:  # Mostra apenas horários que aparecem na lista
            valor_por_participante = valor_hora / quantidade
            total_participantes += valor_por_participante  # Soma o valor de cada participante
            resultado += f"- {hora}: ({quantidade}P), R$ {valor_por_participante:.2f}\n"

    # Total dos valores por participante
    resultado += f"\n**Todos os horários: R$ {total_participantes:.2f}**\n"
    resultado += "\nPix: (adicione a chave)\n"

    # Exibir o resultado formatado dentro de uma caixinha
    st.code(resultado, language="markdown")
