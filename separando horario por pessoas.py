import streamlit as st
import re

def main():
    st.title("Organizador de Horários de Vôlei �")
    
    # Entrada de dados
    st.header("Entrada de Dados")
    texto = st.text_area("Cole aqui a lista de participantes:", height=300,
                        help="Formato: Nome Hora1 Hora2...\nEx: João 17h 19h\nMaria 18h")
    
    if st.button("Processar Dados"):
        if not texto.strip():
            st.error("Por favor, insira os dados dos participantes!")
            return
        
        try:
            # Processamento dos dados
            pessoas = processar_dados(texto)
            
            # Organização por horários
            horarios_organizados = organizar_horarios(pessoas)
            
            # Exibição dos resultados
            st.success("Dados processados com sucesso!")
            exibir_resultados(horarios_organizados)
            
        except Exception as e:
            st.error(f"Erro no processamento: {str(e)}")

def processar_dados(texto):
    """Processa o texto de entrada e retorna lista de participantes"""
    pessoas = []
    for linha in processar_lista(texto):
        horas_validas, partes_invalidas = validar_horarios(linha)
        if not horas_validas:
            st.warning(f"Linha ignorada (sem horários válidos): {linha}")
            continue
        
        nome = ' '.join(partes_invalidas).strip()
        horas = normalizar_horarios(horas_validas)
        
        if nome and horas:
            pessoas.append((nome, horas))
    return pessoas

def organizar_horarios(pessoas):
    """Organiza os participantes por horário"""
    horarios = sorted(
        {hora for _, horas in pessoas for hora in horas},
        key=lambda x: int(x[:-1])
    )
    
    grupos = {hora: [] for hora in horarios}
    for nome, horas in pessoas:
        for hora in horas:
            grupos[hora].append(nome)
    
    return grupos

def exibir_resultados(horarios):
    """Exibe os resultados formatados no Streamlit"""
    st.header("Resultado da Organização")
    
    for hora, participantes in horarios.items():
        with st.expander(f"{hora} - {len(participantes)} participantes"):
            st.write("\n".join([f"{i+1}. {nome}" for i, nome in enumerate(participantes)]))
            st.download_button(
                label="Baixar Lista",
                data="\n".join(participantes),
                file_name=f"lista_{hora}.txt",
                key=hora
            )

# Funções auxiliares (mantidas do código original)
def validar_horarios(texto):
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
    linhas = []
    for linha in texto.strip().split('\n'):
        linha = linha.strip()
        if linha and linha[0].isdigit() and '. ' in linha:
            linha = linha.split('. ', 1)[-1]
        linhas.append(linha)
    return linhas

def normalizar_horarios(horarios):
    normalizados = []
    for hora in horarios:
        hora_norm = hora.lower().replace(':00', 'h').replace('hrs', 'h').replace('hr', 'h').strip()
        if hora_norm.endswith('h'):
            num = hora_norm[:-1]
            if num.isdigit() and 0 <= int(num) <= 23:
                normalizados.append(f"{int(num)}h")
    return normalizados

if __name__ == "__main__":
    main()
