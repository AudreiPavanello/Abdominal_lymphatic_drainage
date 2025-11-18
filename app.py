import streamlit as st
import graphviz
import json
import random
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Drenagem Linfática Abdominal",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado para melhorar a aparência
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1e3a8a;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f8fafc;
        padding: 10px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        border: 2px solid #e2e8f0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1e3a8a !important;
        color: white !important;
        border-color: #1e3a8a !important;
    }
    .organ-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .pathway-info {
        background-color: #f0f9ff;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #0284c7;
        margin: 10px 0;
    }
    .score-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .achievement-badge {
        background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
        padding: 10px 20px;
        border-radius: 20px;
        color: white;
        display: inline-block;
        margin: 5px;
        font-weight: bold;
    }
    .game-mode-card {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        margin: 10px 0;
        transition: all 0.3s;
    }
    .game-mode-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Cache para carregar dados
@st.cache_data
def load_data(path: str):
    """Carrega os dados dos órgãos de um arquivo JSON."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Inicialização do estado da sessão
def init_session_state():
    """Inicializa variáveis de estado da sessão."""
    if 'total_score' not in st.session_state:
        st.session_state.total_score = 0
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = 0
    if 'achievements' not in st.session_state:
        st.session_state.achievements = set()
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0
    if 'quiz_total' not in st.session_state:
        st.session_state.quiz_total = 0
    if 'clinical_score' not in st.session_state:
        st.session_state.clinical_score = 0
    if 'clinical_total' not in st.session_state:
        st.session_state.clinical_total = 0
    if 'sequence_score' not in st.session_state:
        st.session_state.sequence_score = 0
    if 'sequence_total' not in st.session_state:
        st.session_state.sequence_total = 0

def check_achievements():
    """Verifica e adiciona conquistas baseadas no desempenho."""
    achievements = []

    # Conquistas por número de questões
    if st.session_state.total_questions >= 10 and 'primeira_decena' not in st.session_state.achievements:
        st.session_state.achievements.add('primeira_decena')
        achievements.append("🎯 Primeira Dezena - Completou 10 questões!")

    if st.session_state.total_questions >= 50 and 'meio_centenario' not in st.session_state.achievements:
        st.session_state.achievements.add('meio_centenario')
        achievements.append("🏆 Meio Centenário - Completou 50 questões!")

    # Conquistas por precisão
    if st.session_state.total_questions >= 10:
        accuracy = (st.session_state.total_score / st.session_state.total_questions) * 100
        if accuracy >= 80 and 'expert' not in st.session_state.achievements:
            st.session_state.achievements.add('expert')
            achievements.append("⭐ Expert - Alcançou 80% de acerto!")
        if accuracy >= 90 and 'mestre' not in st.session_state.achievements:
            st.session_state.achievements.add('mestre')
            achievements.append("👨‍⚕️ Mestre - Alcançou 90% de acerto!")
        if accuracy == 100 and 'perfeito' not in st.session_state.achievements:
            st.session_state.achievements.add('perfeito')
            achievements.append("💎 Perfeição - 100% de acerto!")

    return achievements

# ============================================================================
# ABA 1: VIAS DE DRENAGEM
# ============================================================================

def render_drainage_pathways_tab(organs):
    """Renderiza a aba de visualização das vias de drenagem."""
    st.markdown('<p class="main-header">🔍 Vias de Drenagem Linfática Abdominal</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Visualize os trajetos anatômicos completos da drenagem linfática</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### 📋 Seleção de Estrutura")
        organ_key = st.selectbox(
            "Selecione o órgão:",
            options=list(organs.keys()),
            format_func=lambda k: f"{get_organ_emoji(k)} {organs[k]['nome']}",
            key="pathway_organ"
        )
        organ = organs[organ_key]

        # Informações sobre o órgão
        st.markdown(f"""
        <div class="pathway-info">
            <h4>{organs[organ_key]['nome']}</h4>
            <p><strong>Número de vias:</strong> {len(organ['rotas'])}</p>
            <p><strong>Relevância clínica:</strong> Compreender a drenagem linfática é essencial para avaliar disseminação neoplásica e processos inflamatórios.</p>
        </div>
        """, unsafe_allow_html=True)

        # Seleção de rota
        if len(organ["rotas"]) > 1:
            rota_index = st.selectbox(
                "Selecione a via de drenagem:",
                options=list(range(len(organ["rotas"]))),
                format_func=lambda i: f"Via {i+1}: {organ['rotas'][i]['Rota']}",
                key="pathway_route"
            )
        else:
            rota_index = 0
            st.info(f"**Via única:** {organ['rotas'][0]['Rota']}")

    with col2:
        rota = organ["rotas"][rota_index]
        caminho = rota["Trajeto"]

        st.markdown(f"### 🗺️ Fluxograma: {rota['Rota']}")
        st.markdown(f"*Sequência de {len(caminho)} estruturas anatômicas*")

        # Criação do gráfico com cores aprimoradas
        graph = graphviz.Digraph()
        graph.attr('node', shape='box', style='rounded,filled', fontname='Arial', fontsize='11')
        graph.attr('edge', color='#475569', penwidth='2', arrowsize='0.8')
        graph.attr(rankdir='TB', splines='ortho', nodesep='0.5', ranksep='0.8')

        # Cores diferentes para diferentes tipos de nós
        for i, etapa in enumerate(caminho):
            if i == 0:
                # Primeiro nó (origem) - azul
                graph.node(str(i), etapa, fillcolor='#dbeafe', color='#1e40af', fontcolor='#1e3a8a', penwidth='3')
            elif i == len(caminho) - 1:
                # Último nó (destino final) - verde
                graph.node(str(i), etapa, fillcolor='#d1fae5', color='#059669', fontcolor='#065f46', penwidth='3')
            else:
                # Nós intermediários - cinza claro
                graph.node(str(i), etapa, fillcolor='#f1f5f9', color='#64748b', fontcolor='#334155')

            if i > 0:
                graph.edge(str(i - 1), str(i))

        st.graphviz_chart(graph, use_container_width=True)

        # Lista detalhada do trajeto
        with st.expander("📝 Visualizar trajeto em lista"):
            for i, etapa in enumerate(caminho, 1):
                if i == 1:
                    st.markdown(f"**{i}.** 🔵 {etapa} *(origem)*")
                elif i == len(caminho):
                    st.markdown(f"**{i}.** 🟢 {etapa} *(destino final)*")
                else:
                    st.markdown(f"**{i}.** ⚪ {etapa}")

# ============================================================================
# ABA 2: ESTUDO
# ============================================================================

def render_study_tab(organs):
    """Renderiza a aba de estudo com informações detalhadas."""
    st.markdown('<p class="main-header">📚 Modo Estudo</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Aprenda sobre anatomia da drenagem linfática abdominal</p>', unsafe_allow_html=True)

    # Cards com informações de cada órgão
    st.markdown("### 🫀 Órgãos Abdominais")

    # Cria grid de órgãos
    cols = st.columns(2)
    for idx, (organ_key, organ_data) in enumerate(organs.items()):
        with cols[idx % 2]:
            with st.expander(f"{get_organ_emoji(organ_key)} {organ_data['nome']}", expanded=False):
                st.markdown(f"**Número de vias de drenagem:** {len(organ_data['rotas'])}")

                for i, rota in enumerate(organ_data['rotas'], 1):
                    st.markdown(f"**Via {i}:** {rota['Rota']}")
                    st.markdown(f"- Etapas: {len(rota['Trajeto'])}")
                    st.markdown(f"- Primeiro linfonodo: *{rota['Trajeto'][0]}*")
                    st.markdown(f"- Destino final: *{rota['Trajeto'][-1]}*")
                    if i < len(organ_data['rotas']):
                        st.markdown("---")

    # Informações gerais
    st.markdown("---")
    st.markdown("### 📖 Conceitos Importantes")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Drenagem Linfática Abdominal**

        A drenagem linfática dos órgãos abdominais segue padrões anatômicos específicos e previsíveis.
        O conhecimento dessas vias é fundamental para:

        - Compreensão da disseminação de neoplasias malignas
        - Planejamento cirúrgico oncológico
        - Interpretação de exames de estadiamento
        - Avaliação de processos infecciosos e inflamatórios
        """)

    with col2:
        st.markdown("""
        **Principais Destinos**

        A maioria das vias de drenagem converge para:

        - **Linfonodos celíacos:** Derivados do intestino anterior
        - **Linfonodos mesentéricos superiores:** Derivados do intestino médio
        - **Linfonodos mesentéricos inferiores:** Derivados do intestino posterior
        - **Linfonodos lombares:** Órgãos retroperitoneais

        Destino final comum: **Ducto torácico → Ângulo venoso esquerdo**
        """)

    # Modo de teste rápido integrado
    st.markdown("---")
    st.markdown("### ✍️ Teste Seu Conhecimento")

    if st.button("📝 Iniciar Quiz Rápido de Estudo", use_container_width=True):
        st.session_state.study_quiz_active = True
        setup_quick_quiz_question(organs, 'study')

    if 'study_quiz_active' in st.session_state and st.session_state.study_quiz_active:
        render_embedded_quiz(organs, 'study')

def render_embedded_quiz(organs, mode='study'):
    """Renderiza um quiz embutido na aba de estudo."""
    quiz_key = f'{mode}_quiz'

    if quiz_key not in st.session_state or st.session_state[quiz_key] is None:
        setup_quick_quiz_question(organs, mode)

    question = st.session_state[quiz_key]

    st.markdown("---")
    st.markdown(question['prompt'])

    if question['submitted_answer']:
        user_answer = question['submitted_answer']
        correct_answer = question['correct_answer']

        if user_answer == correct_answer:
            st.success(f"✅ Correto! A resposta é **{correct_answer}**.")
        else:
            st.error(f"❌ Incorreto. A resposta correta é **{correct_answer}**.")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("➡️ Próxima Pergunta", key=f"next_{mode}"):
                setup_quick_quiz_question(organs, mode)
                st.rerun()
        with col2:
            if st.button("🔚 Encerrar Quiz", key=f"end_{mode}"):
                st.session_state.study_quiz_active = False
                st.rerun()
    else:
        user_answer = st.radio(
            "Selecione a próxima estrutura:",
            question['options'],
            key=f"radio_{mode}_{st.session_state.get(f'{mode}_quiz_count', 0)}"
        )
        if st.button("Confirmar Resposta", key=f"submit_{mode}"):
            st.session_state[quiz_key]['submitted_answer'] = user_answer
            if mode not in ['study']:
                if user_answer == question['correct_answer']:
                    st.session_state[f'{mode}_score'] += 1
                st.session_state[f'{mode}_total'] += 1
            st.rerun()

# ============================================================================
# ABA 3: JOGOS INTERATIVOS
# ============================================================================

def render_games_tab(organs):
    """Renderiza a aba de jogos interativos."""
    st.markdown('<p class="main-header">🎮 Jogos Interativos</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Aprenda de forma divertida e interativa</p>', unsafe_allow_html=True)

    # Estatísticas gerais
    col1, col2, col3 = st.columns(3)

    with col1:
        accuracy = (st.session_state.total_score / st.session_state.total_questions * 100) if st.session_state.total_questions > 0 else 0
        st.markdown(f"""
        <div class="score-card">
            <h2>{st.session_state.total_score}/{st.session_state.total_questions}</h2>
            <p>Pontuação Total</p>
            <h3>{accuracy:.1f}%</h3>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="score-card">
            <h2>{len(st.session_state.achievements)}</h2>
            <p>Conquistas Desbloqueadas</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        if st.button("🔄 Resetar Estatísticas", use_container_width=True):
            st.session_state.total_score = 0
            st.session_state.total_questions = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_total = 0
            st.session_state.clinical_score = 0
            st.session_state.clinical_total = 0
            st.session_state.sequence_score = 0
            st.session_state.sequence_total = 0
            st.session_state.achievements = set()
            st.rerun()

    # Conquistas
    if st.session_state.achievements:
        st.markdown("### 🏆 Conquistas Desbloqueadas")
        achievement_names = {
            'primeira_decena': '🎯 Primeira Dezena',
            'meio_centenario': '🏆 Meio Centenário',
            'expert': '⭐ Expert',
            'mestre': '👨‍⚕️ Mestre',
            'perfeito': '💎 Perfeição'
        }
        for ach in st.session_state.achievements:
            st.markdown(f'<span class="achievement-badge">{achievement_names.get(ach, ach)}</span>', unsafe_allow_html=True)
        st.markdown("---")

    # Seleção de modo de jogo
    st.markdown("### 🎯 Escolha o Modo de Jogo")

    game_mode = st.radio(
        "Selecione o modo:",
        ["Quiz Rápido", "Casos Clínicos", "Sequência Completa"],
        horizontal=True,
        key="game_mode_selection"
    )

    st.markdown("---")

    if game_mode == "Quiz Rápido":
        render_quick_quiz_mode(organs)
    elif game_mode == "Casos Clínicos":
        render_clinical_cases_mode(organs)
    else:  # Sequência Completa
        render_sequence_game_mode(organs)

# ============================================================================
# MODO QUIZ RÁPIDO
# ============================================================================

def setup_quick_quiz_question(organs, mode='quiz'):
    """Prepara uma pergunta de quiz rápido."""
    organ_key = random.choice(list(organs.keys()))
    organ = organs[organ_key]
    rota = random.choice(organ["rotas"])
    caminho = rota["Trajeto"]

    if len(caminho) < 2:
        return setup_quick_quiz_question(organs, mode)

    step_index = random.randint(0, len(caminho) - 2)

    question_prompt = f"A linfa do órgão **{organ['nome']}** (via: *{rota['Rota']}*) está na estrutura **{caminho[step_index]}**. Para qual estrutura ela segue?"
    correct_answer = caminho[step_index + 1]

    # Distratores
    all_nodes = list(set(node for org_data in organs.values() for r in org_data['rotas'] for node in r['Trajeto']))
    all_nodes.remove(correct_answer)
    if caminho[step_index] in all_nodes:
        all_nodes.remove(caminho[step_index])

    distractors = random.sample(all_nodes, min(3, len(all_nodes)))
    options = distractors + [correct_answer]
    random.shuffle(options)

    quiz_key = f'{mode}_quiz'
    st.session_state[quiz_key] = {
        "prompt": question_prompt,
        "options": options,
        "correct_answer": correct_answer,
        "submitted_answer": None
    }

def render_quick_quiz_mode(organs):
    """Renderiza o modo Quiz Rápido."""
    st.markdown("#### 🧠 Quiz Rápido")
    st.info("Teste seu conhecimento sobre as vias de drenagem linfática. Identifique a próxima estrutura no trajeto!")

    # Pontuação específica
    col1, col2 = st.columns([2, 1])
    with col1:
        st.metric(
            "Pontuação do Quiz",
            f"{st.session_state.quiz_score}/{st.session_state.quiz_total}",
            f"{(st.session_state.quiz_score/st.session_state.quiz_total*100):.0f}%" if st.session_state.quiz_total > 0 else "0%"
        )

    if 'quiz_quiz' not in st.session_state or st.session_state.quiz_quiz is None:
        setup_quick_quiz_question(organs, 'quiz')

    question = st.session_state.quiz_quiz

    st.markdown("---")
    st.markdown(question['prompt'])

    if question['submitted_answer']:
        user_answer = question['submitted_answer']
        correct_answer = question['correct_answer']

        if user_answer == correct_answer:
            st.success("✅ **Correto!** Excelente conhecimento anatômico!")
            st.balloons()
        else:
            st.error(f"❌ **Incorreto.** A resposta correta é: **{correct_answer}**")

        if st.button("➡️ Próxima Pergunta", key="next_quiz", use_container_width=True):
            # Verifica conquistas
            new_achievements = check_achievements()
            if new_achievements:
                for ach in new_achievements:
                    st.toast(ach, icon="🏆")

            setup_quick_quiz_question(organs, 'quiz')
            st.rerun()
    else:
        user_answer = st.radio(
            "Selecione a próxima estrutura:",
            question['options'],
            key=f"quiz_radio_{st.session_state.quiz_total}"
        )

        if st.button("✓ Confirmar Resposta", key="submit_quiz", use_container_width=True):
            st.session_state.quiz_quiz['submitted_answer'] = user_answer

            # Atualiza pontuações
            st.session_state.quiz_total += 1
            st.session_state.total_questions += 1

            if user_answer == question['correct_answer']:
                st.session_state.quiz_score += 1
                st.session_state.total_score += 1

            st.rerun()

# ============================================================================
# MODO CASOS CLÍNICOS
# ============================================================================

CASE_TEMPLATES = {
    "estomago": "Paciente {name}, {age} anos, sexo {sex}, apresenta quadro de dispepsia e perda ponderal progressiva. A endoscopia digestiva alta evidencia lesão vegetante na região da **{location}**. O exame anatomopatológico confirma adenocarcinoma gástrico. Considerando a drenagem linfática desta região, qual grupo de linfonodos será o primeiro a ser comprometido em caso de disseminação neoplásica?",

    "intestino_grosso": "Paciente {name}, {age} anos, sexo {sex}, procura atendimento médico por alteração do hábito intestinal e hematoquezia. A colonoscopia identifica lesão tumoral no **{location}**. A biópsia confirma adenocarcinoma. Considerando que a linfa desta região passa inicialmente pelos linfonodos epicólicos e paracólicos, qual é o próximo grupo linfonodal na cadeia de drenagem?",

    "pâncreas": "Paciente {name}, {age} anos, sexo {sex}, apresenta quadro de icterícia indolor progressiva e perda de peso. A tomografia computadorizada revela massa sólida na **{location}** do pâncreas. A biópsia guiada por ultrassom endoscópico confirma adenocarcinoma pancreático. Qual grupo de linfonodos constitui a primeira estação de drenagem linfática desta região?",

    "figado": "Paciente {name}, {age} anos, sexo {sex}, portador de cirrose hepática por hepatite C, apresenta elevação de alfa-fetoproteína e lesão hepática suspeita. A investigação confirma carcinoma hepatocelular. Considerando a via de drenagem '{location}', qual grupo linfonodal deve ser avaliado prioritariamente no estadiamento?",

    "rins": "Durante investigação de hematúria macroscópica em paciente {name}, {age} anos, sexo {sex}, a tomografia identifica massa renal sólida compatível com carcinoma de células renais. Qual é o principal grupo de linfonodos que recebe a drenagem linfática renal?",

    "intestino_delgado": "Paciente {name}, {age} anos, sexo {sex}, apresenta quadro de dor abdominal intermitente e anemia ferropriva. A enterotomografia identifica lesão no **{location}**. A investigação confirma tumor neuroendócrino de intestino delgado. Qual é a primeira estação linfonodal de drenagem desta região?",

    "baco": "Paciente {name}, {age} anos, sexo {sex}, vítima de traumatismo abdominal fechado de alta energia, apresenta lesão esplênica grau IV com necessidade de esplenectomia de urgência. Durante o procedimento cirúrgico, qual grupo de linfonodos regionais deve ser inspecionado, considerando a drenagem linfática esplênica?"
}

def setup_clinical_case_question(organs):
    """Prepara uma pergunta de caso clínico."""
    valid_organ_keys = list(CASE_TEMPLATES.keys())
    organ_key = random.choice(valid_organ_keys)
    organ = organs[organ_key]
    rota = random.choice(organ["rotas"])
    caminho = rota["Trajeto"]

    # Lógica específica
    if organ_key == "intestino_grosso":
        if len(caminho) < 3:
            return setup_clinical_case_question(organs)
        correct_answer = caminho[2]
    else:
        correct_answer = caminho[0]

    # Gera o caso
    template = CASE_TEMPLATES[organ_key]
    case_text = template.format(
        name=random.choice(["João Silva", "Maria Santos", "José Oliveira", "Ana Costa", "Carlos Ferreira", "Paula Rodrigues"]),
        age=random.randint(45, 75),
        sex=random.choice(["masculino", "feminino"]),
        location=rota["Rota"]
    )

    # Distratores
    all_nodes = list(set(node for org_data in organs.values() for r in org_data['rotas'] for node in r['Trajeto']))
    all_nodes.remove(correct_answer)

    distractors = random.sample(all_nodes, 3)
    options = distractors + [correct_answer]
    random.shuffle(options)

    st.session_state.clinical_quiz = {
        "prompt": case_text,
        "options": options,
        "correct_answer": correct_answer,
        "submitted_answer": None
    }

def render_clinical_cases_mode(organs):
    """Renderiza o modo de Casos Clínicos."""
    st.markdown("#### 🩺 Casos Clínicos")
    st.info("Aplique seu conhecimento anatômico em cenários clínicos realistas de oncologia e trauma.")

    # Pontuação específica
    col1, col2 = st.columns([2, 1])
    with col1:
        st.metric(
            "Pontuação de Casos Clínicos",
            f"{st.session_state.clinical_score}/{st.session_state.clinical_total}",
            f"{(st.session_state.clinical_score/st.session_state.clinical_total*100):.0f}%" if st.session_state.clinical_total > 0 else "0%"
        )

    if 'clinical_quiz' not in st.session_state or st.session_state.clinical_quiz is None:
        setup_clinical_case_question(organs)

    case = st.session_state.clinical_quiz

    st.markdown("---")
    st.markdown("**📋 Caso Clínico:**")
    st.markdown(case['prompt'])

    if case['submitted_answer']:
        user_answer = case['submitted_answer']
        correct_answer = case['correct_answer']

        if user_answer == correct_answer:
            st.success("✅ **Correto!** Excelente raciocínio clínico-anatômico!")
            st.balloons()
        else:
            st.error(f"❌ **Incorreto.** A primeira estação linfonodal é: **{correct_answer}**")
            st.info("💡 **Dica:** Revise a via de drenagem deste órgão no modo 'Vias de Drenagem'.")

        if st.button("➡️ Próximo Caso", key="next_clinical", use_container_width=True):
            # Verifica conquistas
            new_achievements = check_achievements()
            if new_achievements:
                for ach in new_achievements:
                    st.toast(ach, icon="🏆")

            setup_clinical_case_question(organs)
            st.rerun()
    else:
        user_answer = st.radio(
            "Qual grupo de linfonodos?",
            case['options'],
            key=f"clinical_radio_{st.session_state.clinical_total}"
        )

        if st.button("✓ Confirmar Resposta", key="submit_clinical", use_container_width=True):
            st.session_state.clinical_quiz['submitted_answer'] = user_answer

            # Atualiza pontuações
            st.session_state.clinical_total += 1
            st.session_state.total_questions += 1

            if user_answer == case['correct_answer']:
                st.session_state.clinical_score += 1
                st.session_state.total_score += 1

            st.rerun()

# ============================================================================
# MODO SEQUÊNCIA COMPLETA (NOVO!)
# ============================================================================

def setup_sequence_game(organs):
    """Prepara o jogo de sequência completa."""
    organ_key = random.choice(list(organs.keys()))
    organ = organs[organ_key]
    rota = random.choice(organ["rotas"])
    caminho = rota["Trajeto"].copy()

    # Embaralha a sequência
    correct_sequence = caminho.copy()
    shuffled_sequence = caminho.copy()
    random.shuffle(shuffled_sequence)

    # Garante que não seja a mesma sequência
    while shuffled_sequence == correct_sequence and len(caminho) > 1:
        random.shuffle(shuffled_sequence)

    st.session_state.sequence_game = {
        "organ": organ['nome'],
        "route": rota['Rota'],
        "correct_sequence": correct_sequence,
        "current_sequence": shuffled_sequence,
        "submitted": False
    }

def render_sequence_game_mode(organs):
    """Renderiza o modo de jogo de sequência completa."""
    st.markdown("#### 🎯 Sequência Completa")
    st.info("Organize as estruturas anatômicas na ordem correta da drenagem linfática!")

    # Pontuação específica
    col1, col2 = st.columns([2, 1])
    with col1:
        st.metric(
            "Pontuação de Sequências",
            f"{st.session_state.sequence_score}/{st.session_state.sequence_total}",
            f"{(st.session_state.sequence_score/st.session_state.sequence_total*100):.0f}%" if st.session_state.sequence_total > 0 else "0%"
        )

    if 'sequence_game' not in st.session_state or st.session_state.sequence_game is None:
        setup_sequence_game(organs)

    game = st.session_state.sequence_game

    st.markdown("---")
    st.markdown(f"**Órgão:** {game['organ']}")
    st.markdown(f"**Via:** {game['route']}")
    st.markdown("")
    st.markdown("**Instruções:** Organize as estruturas abaixo na ordem correta do trajeto de drenagem linfática.")

    if not game['submitted']:
        st.markdown("---")
        st.markdown("**🔀 Organize a sequência:**")

        # Permite ao usuário reordenar
        sequence_order = []
        for i, structure in enumerate(game['current_sequence']):
            col1, col2 = st.columns([1, 4])
            with col1:
                position = st.number_input(
                    "Posição",
                    min_value=1,
                    max_value=len(game['current_sequence']),
                    value=i+1,
                    key=f"pos_{i}",
                    label_visibility="collapsed"
                )
                sequence_order.append((position, structure))
            with col2:
                st.markdown(f"**{structure}**")

        if st.button("✓ Verificar Sequência", key="submit_sequence", use_container_width=True):
            # Ordena pela posição escolhida
            sequence_order.sort(key=lambda x: x[0])
            user_sequence = [s[1] for s in sequence_order]

            st.session_state.sequence_game['user_sequence'] = user_sequence
            st.session_state.sequence_game['submitted'] = True

            # Atualiza pontuações
            st.session_state.sequence_total += 1
            st.session_state.total_questions += 1

            if user_sequence == game['correct_sequence']:
                st.session_state.sequence_score += 1
                st.session_state.total_score += 1

            st.rerun()
    else:
        user_sequence = game.get('user_sequence', [])
        correct_sequence = game['correct_sequence']

        is_correct = user_sequence == correct_sequence

        if is_correct:
            st.success("✅ **Correto!** Você organizou a sequência perfeitamente!")
            st.balloons()
        else:
            st.error("❌ **Incorreto.** Veja a comparação abaixo:")

        # Mostra comparação
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Sua Resposta:**")
            for i, struct in enumerate(user_sequence, 1):
                # Verifica se está correto
                if i-1 < len(correct_sequence) and struct == correct_sequence[i-1]:
                    st.markdown(f"{i}. ✅ {struct}")
                else:
                    st.markdown(f"{i}. ❌ {struct}")

        with col2:
            st.markdown("**Sequência Correta:**")
            for i, struct in enumerate(correct_sequence, 1):
                st.markdown(f"{i}. ✓ {struct}")

        if st.button("➡️ Nova Sequência", key="next_sequence", use_container_width=True):
            # Verifica conquistas
            new_achievements = check_achievements()
            if new_achievements:
                for ach in new_achievements:
                    st.toast(ach, icon="🏆")

            setup_sequence_game(organs)
            st.rerun()

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def get_organ_emoji(organ_key):
    """Retorna emoji correspondente ao órgão."""
    emojis = {
        "estomago": "🫃",
        "figado": "🫁",
        "baco": "🩸",
        "pâncreas": "🫀",
        "rins": "🫘",
        "intestino_delgado": "🌀",
        "intestino_grosso": "〰️"
    }
    return emojis.get(organ_key, "🔬")

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Função principal da aplicação."""
    # Inicializa estado
    init_session_state()

    # Carrega dados
    organs = load_data('data.json')

    # Cabeçalho principal
    st.markdown('<p class="main-header">🫀 Drenagem Linfática Abdominal</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Plataforma interativa de estudo para estudantes de medicina</p>', unsafe_allow_html=True)

    # Sistema de abas
    tab1, tab2, tab3 = st.tabs([
        "🗺️ Vias de Drenagem",
        "📚 Estudo",
        "🎮 Jogos Interativos"
    ])

    with tab1:
        render_drainage_pathways_tab(organs)

    with tab2:
        render_study_tab(organs)

    with tab3:
        render_games_tab(organs)

    # Rodapé
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #64748b; font-size: 0.9rem;'>
        <p>Desenvolvido para estudantes de medicina • Conteúdo baseado em anatomia clássica</p>
        <p>Sempre consulte literatura médica atualizada e seus professores para confirmação</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
