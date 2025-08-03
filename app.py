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

    # Centraliza o gráfico usando colunas para controlar o tamanho e dar um respiro nas laterais
    col1, col2, col3 = st.columns([0.5, 2, 0.5])
    with col2:
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

        # Renderiza o gráfico no Streamlit, usando a largura da coluna
        st.graphviz_chart(graph, use_container_width=True)

def setup_quick_quiz_question(organs):
    """Seleciona uma pergunta aleatória e prepara as opções."""
    # Escolhe um órgão e uma rota aleatoriamente
    organ_key = random.choice(list(organs.keys()))
    organ = organs[organ_key]
    rota = random.choice(organ["rotas"])
    caminho = rota["Trajeto"]
    # Garante que o caminho tenha pelo menos 2 etapas para uma pergunta válida
    if len(caminho) < 2:
        return setup_quick_quiz_question(organs)  # Tenta novamente com outro caminho

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
    st.session_state.quick_quiz = {
        "prompt": question_prompt,
        "options": options,
        "correct_answer": correct_answer,
        "submitted_answer": None
    }

def render_quick_quiz_mode(organs):
    """Renderiza a página do Modo Quiz."""
    st.title("🧠 Modo Quiz: Teste seu Conhecimento!")

    # Inicializa o estado do quiz na primeira execução
    if 'quick_quiz' not in st.session_state or st.session_state.quick_quiz is None:
        setup_quick_quiz_question(organs)
        st.session_state.quick_quiz_score = 0
        st.session_state.quick_quiz_total = 0

    # Exibe a pontuação
    st.metric(label="Pontuação", value=f"{st.session_state.quick_quiz_score} / {st.session_state.quick_quiz_total}")
    st.markdown("---")

    question = st.session_state.quick_quiz
    st.markdown(question['prompt'])

    # Se a resposta já foi enviada, mostra o resultado
    if question['submitted_answer']:
        user_answer = question['submitted_answer']
        correct_answer = question['correct_answer']
        if user_answer == correct_answer:
            st.success(f"🎉 Correto! A resposta é **{correct_answer}**.")
        else:
            st.error(f"😕 Incorreto. A resposta correta é **{correct_answer}**.")
        
        if st.button("Próxima Pergunta"):
            setup_quick_quiz_question(organs)
            st.rerun()
    else:
        # Mostra as opções de resposta
        user_answer = st.radio("Selecione a próxima etapa:", question['options'], key=f"q_{st.session_state.quick_quiz_total}")
        if st.button("Responder"):
            st.session_state.quick_quiz['submitted_answer'] = user_answer
            st.session_state.quick_quiz_total += 1
            if user_answer == question['correct_answer']:
                st.session_state.quick_quiz_score += 1
            st.rerun()

CASE_TEMPLATES = {
    "estomago": "Paciente de {age} anos apresenta queixa de dispepsia e perda de peso. Endoscopia revela um adenocarcinoma gástrico localizado na região da **{location}**. A disseminação linfática inicial deste tumor provavelmente ocorrerá para qual grupo de linfonodos?",
    "intestino_grosso": "{name}, {age} anos, relata alteração do hábito intestinal e hematoquezia. A colonoscopia diagnostica um adenocarcinoma no **{location}**. Sabendo que a linfa passa primeiro pelos linfonodos epicólicos e paracólicos, qual é o próximo grupo principal de linfonodos a ser afetado?",
    "pâncreas": "Um paciente de {age} anos é diagnosticado com um adenocarcinoma na **{location}** do pâncreas após apresentar icterícia indolor. A via de drenagem linfática primária envolverá qual grupo de linfonodos?",
    "figado": "Durante uma investigação de dor no quadrante superior direito, {name}, {age} anos, é diagnosticado com um colangiocarcinoma. Considerando a drenagem principal da rota '{location}', qual é o primeiro grupo de linfonodos a ser avaliado para metástase?",
    "rins": "Um achado incidental em um exame de imagem de {name}, {age} anos, revela um carcinoma de células renais. A drenagem linfática deste órgão é direcionada primariamente para qual grupo de linfonodos?",
    "intestino_delgado": "{name}, {age} anos, com histórico de dor abdominal crônica, é diagnosticado(a) com um tumor no **{location}**. Qual é o primeiro nível de linfonodos a receber a drenagem linfática desta área?",
    "baco": "Um paciente de {age} anos, vítima de um acidente automobilístico, necessita de uma esplenectomia de emergência. Durante o procedimento, os linfonodos regionais são inspecionados. Qual é o primeiro grupo de linfonodos que drena o baço?"
}

def setup_clinical_case_question(organs):
    """Prepara uma pergunta de caso clínico."""
    # Escolhe um órgão que tenha um template de caso clínico
    valid_organ_keys = list(CASE_TEMPLATES.keys())
    organ_key = random.choice(valid_organ_keys)
    organ = organs[organ_key]
    rota = random.choice(organ["rotas"])
    caminho = rota["Trajeto"]

    # Lógica específica para o tipo de pergunta
    if organ_key == "intestino_grosso":
        # Para o intestino grosso, a pergunta é sobre o 3º grupo de linfonodos
        if len(caminho) < 3:
            return setup_clinical_case_question(organs) # Rota muito curta, tenta de novo
        correct_answer = caminho[2]
    else:
        # Para os outros órgãos, a pergunta é sobre o 1º grupo
        correct_answer = caminho[0]

    # Gera o texto do caso clínico
    template = CASE_TEMPLATES[organ_key]
    case_text = template.format(
        name=random.choice(["João", "Maria", "José", "Ana", "Carlos"]),
        age=random.randint(45, 75),
        location=rota["Rota"]
    )

    # Coleta distratores
    all_nodes = list(set(node for org_data in organs.values() for r in org_data['rotas'] for node in r['Trajeto']))
    all_nodes.remove(correct_answer)
    
    distractors = random.sample(all_nodes, 3)
    options = distractors + [correct_answer]
    random.shuffle(options)

    st.session_state.clinical_case = {
        "prompt": case_text,
        "options": options,
        "correct_answer": correct_answer,
        "submitted_answer": None
    }

def render_clinical_cases_mode(organs):
    """Renderiza a página de Casos Clínicos."""
    st.title("🩺 Modo Casos Clínicos")
    st.info("Aplique seu conhecimento de anatomia para resolver casos clínicos de oncologia.")

    if 'clinical_case' not in st.session_state or st.session_state.clinical_case is None:
        setup_clinical_case_question(organs)
        st.session_state.clinical_case_score = 0
        st.session_state.clinical_case_total = 0

    col1, col2 = st.columns([3, 1])
    with col1:
        st.metric(label="Pontuação", value=f"{st.session_state.clinical_case_score} / {st.session_state.clinical_case_total}")
    with col2:
        if st.button("Zerar Placar", key="reset_clinical"):
            st.session_state.clinical_case_score = 0
            st.session_state.clinical_case_total = 0
            st.rerun()
    
    st.markdown("---")

    case = st.session_state.clinical_case
    st.markdown(case['prompt'])

    if case['submitted_answer']:
        user_answer = case['submitted_answer']
        correct_answer = case['correct_answer']
        if user_answer == correct_answer:
            st.success(f"🎉 Correto! A drenagem inicial ocorre para **{correct_answer}**.")
        else:
            st.error(f"😕 Incorreto. A resposta correta é **{correct_answer}**.")
        
        if st.button("Próximo Caso"):
            setup_clinical_case_question(organs)
            st.rerun()
    else:
        user_answer = st.radio("Selecione o grupo de linfonodos:", case['options'], key=f"case_{st.session_state.clinical_case_total}")
        if st.button("Responder"):
            st.session_state.clinical_case['submitted_answer'] = user_answer
            st.session_state.clinical_case_total += 1
            if user_answer == case['correct_answer']:
                st.session_state.clinical_case_score += 1
            st.rerun()

def main():
    st.sidebar.title("Navegação")
    app_mode = st.sidebar.radio(
        "Escolha o modo de uso:",
        ("Modo Estudo", "Modo Quiz Rápido", "Modo Casos Clínicos")
    )

    organs = load_data('data.json')

    if app_mode == "Modo Estudo":
        render_study_mode(organs)
    elif app_mode == "Modo Quiz Rápido":
        render_quick_quiz_mode(organs)
    else: # Modo Casos Clínicos
        render_clinical_cases_mode(organs)

if __name__ == "__main__":
    main()
