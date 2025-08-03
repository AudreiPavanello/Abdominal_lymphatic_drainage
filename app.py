import streamlit as st
import graphviz
import json

# Configura o layout para widescreen
st.set_page_config(layout="wide")

# Usa o cache do Streamlit para carregar os dados apenas uma vez
@st.cache_data
def load_data(path: str):
    """Carrega os dados dos órgãos de um arquivo JSON."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    st.title("Visualização da Drenagem Linfática Abdominal")
    st.write(
        "Selecione um órgão para visualizar as rotas de drenagem linfática. Caso o órgão apresente múltiplas rotas, "
        "escolha a desejada para ver cada etapa do trajeto."
    )
    
    # Carrega os dados do arquivo JSON
    organs = load_data('data.json')

    # Seleção do órgão
    organ_key = st.selectbox(
        "Selecione um órgão:",
        options=list(organs.keys()),
        format_func=lambda k: organs[k]["nome"]
    )
    organ = organs[organ_key]

    # Se o órgão possui mais de uma rota, o usuário escolhe a rota desejada
    if len(organ["rotas"]) > 1:
        rota_index = st.selectbox(
            "Selecione a rota de drenagem:",
            options=list(range(len(organ["rotas"]))),
            format_func=lambda i: organ["rotas"][i]["Rota"]
        )
    else:
        rota_index = 0

    rota = organ["rotas"][rota_index]
    caminho = rota["Trajeto"]

    st.subheader(f"Rota de Drenagem: {rota['Rota']}")
    st.markdown("---")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### Fluxograma da Drenagem")
        # Cria um novo gráfico direcionado (Digraph)
        graph = graphviz.Digraph()
        graph.attr('node', shape='box', style='rounded,filled', fillcolor='#e6f3ff', color='#0066cc')
        graph.attr('edge', color='#333333')
        graph.attr(rankdir='TB', splines='ortho') # Layout de cima para baixo

        # Adiciona os nós (etapas) e as arestas (fluxo)
        for i, etapa in enumerate(caminho):
            graph.node(str(i), etapa)
            if i > 0:
                graph.edge(str(i - 1), str(i))

        # Renderiza o gráfico no Streamlit
        st.graphviz_chart(graph)

    with col2:
        st.markdown("#### Detalhes de Cada Etapa")
        for i, etapa in enumerate(caminho):
            with st.expander(f"Etapa {i+1}: {etapa}"):
                if i == 0:
                    st.info(f"**Ponto de Partida:** A linfa é coletada e entra nos primeiros linfonodos: **{caminho[i]}**.")
                elif i < len(caminho) - 1:
                    st.write(f"A partir de **{caminho[i]}**, a linfa flui para a próxima estrutura no caminho: **{caminho[i+1]}**.")
                else:
                    st.success(f"**Destino Final:** A linfa de **{caminho[i]}** entra na circulação sanguínea, completando o trajeto.")

if __name__ == "__main__":
    main()
