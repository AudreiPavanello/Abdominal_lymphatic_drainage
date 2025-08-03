import streamlit as st
import graphviz
import json
import random

# Configura o layout para widescreen
st.set_page_config(layout="wide")

# Usa o cache do Streamlit para carregar os dados apenas uma vez
@st.cache_data
def load_data(path: str):
    """Carrega os dados dos órgãos de um arquivo JSON."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def render_study_mode(organs):
    """Renderiza a página do Modo Estudo (visualização do fluxograma)."""
    st.title("Visualização da Drenagem Linfática Abdominal")
    st.info("Selecione um órgão e uma rota para visualizar o trajeto completo da drenagem linfática.")
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
                    st.info(f"**Ponto de Partida:** A linfa é coletada e entra nos **{caminho[i]}**.")
                elif i < len(caminho) - 1:
                    st.write(f"Após isso, a linfa flui para: **{caminho[i+1]}**.")
                else:
                    st.success(f"**Destino Final:** A linfa do **{caminho[i]}** entra na circulação sanguínea, completando o trajeto.")

def setup_quiz_question(organs):
    """Seleciona uma pergunta aleatória e prepara as opções."""
    # Escolhe um órgão e uma rota aleatoriamente
    organ_key = random.choice(list(organs.keys()))
    organ = organs[organ_key]
    rota = random.choice(organ["rotas"])
    caminho = rota["Trajeto"]

    # Garante que o caminho tenha pelo menos 2 etapas para uma pergunta válida
    if len(caminho) < 2:
        return setup_quiz_question(organs)  # Tenta novamente com outro caminho

    # Escolhe uma etapa aleatória (exceto a última)
    step_index = random.randint(0, len(caminho) - 2)
    
    question_prompt = f"A linfa do **{organ['nome']}** (seguindo a rota *{rota['Rota']}*) está em **{caminho[step_index]}**. Para qual estrutura ela flui a seguir?"
    correct_answer = caminho[step_index + 1]

    # Coleta todos os nós possíveis para usar como distratores
    all_nodes = list(set(node for org_data in organs.values() for r in org_data['rotas'] for node in r['Trajeto']))
    all_nodes.remove(correct_answer)
    if caminho[step_index] in all_nodes:
        all_nodes.remove(caminho[step_index])

    # Seleciona 3 distratores aleatórios
    distractors = random.sample(all_nodes, 3)
    options = distractors + [correct_answer]
    random.shuffle(options)

    # Armazena a pergunta no estado da sessão
    st.session_state.quiz_question = {
        "prompt": question_prompt,
        "options": options,
        "correct_answer": correct_answer,
    }
    st.session_state.answer_submitted = None

def render_quiz_mode(organs):
    """Renderiza a página do Modo Quiz."""
    st.title("🧠 Modo Quiz: Teste seu Conhecimento!")

    # Inicializa o estado do quiz na primeira execução
    if 'quiz_question' not in st.session_state:
        setup_quiz_question(organs)
        st.session_state.score = 0
        st.session_state.total_questions = 0

    # Exibe a pontuação
    st.metric(label="Pontuação", value=f"{st.session_state.score} / {st.session_state.total_questions}")
    st.markdown("---")

    question = st.session_state.quiz_question
    st.markdown(question['prompt'])

    # Se a resposta já foi enviada, mostra o resultado
    if st.session_state.answer_submitted:
        user_answer = st.session_state.answer_submitted
        correct_answer = question['correct_answer']
        if user_answer == correct_answer:
            st.success(f"🎉 Correto! A resposta é **{correct_answer}**.")
        else:
            st.error(f"😕 Incorreto. A resposta correta é **{correct_answer}**.")
        
        if st.button("Próxima Pergunta"):
            setup_quiz_question(organs)
            st.rerun()
    else:
        # Mostra as opções de resposta
        user_answer = st.radio("Selecione a próxima etapa:", question['options'], key=f"q_{st.session_state.total_questions}")
        if st.button("Responder"):
            st.session_state.answer_submitted = user_answer
            st.session_state.total_questions += 1
            if user_answer == question['correct_answer']:
                st.session_state.score += 1
            st.rerun()

def main():
    st.sidebar.title("Navegação")
    app_mode = st.sidebar.radio(
        "Escolha o modo de uso:",
        ("Modo Estudo", "Modo Quiz")
    )

    organs = load_data('data.json')

    if app_mode == "Modo Estudo":
        render_study_mode(organs)
    else:
        render_quiz_mode(organs)

if __name__ == "__main__":
    main()
