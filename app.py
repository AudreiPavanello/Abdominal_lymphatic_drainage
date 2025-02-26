import streamlit as st

# Configura o layout para widescreen
st.set_page_config(layout="wide")

def main():
    st.title("Visualização da Drenagem Linfática Abdominal – Versão Detalhada")
    st.write(
        "Selecione um órgão para visualizar as rotas de drenagem linfática. Caso o órgão apresente múltiplas rotas, "
        "escolha a desejada para ver cada etapa do percurso em abas."
    )

    # Dados dos órgãos e rotas de drenagem
    organs = {
        "estomago": {
            "nome": "Estômago",
            "rotas": [
                {
                    "Rota": "Curvatura menor do Estômago",
                    "Trajeto": [
                        "Linfonodos gástricos (direitos e esquerdos)",
                        "Linfonodos celíacos",
                        "Tronco intestinal",
                        "Cisterna do quilo",
                        "Ducto torácico",
                        "Ângulo venoso esquerdo"
                    ]
                },
                {
                    "Rota": "Curvatura maior",
                    "Trajeto": [
                        "Linfonodos gastromentais (direitos e esquerdos)",
                        "Linfonodos celíacos",
                        "Tronco intestinal",
                        "Cisterna do quilo",
                        "Ducto torácico",
                        "Ângulo venoso esquerdo"
                    ]
                },
                {
                    "Rota": "Fundo gástrico",
                    "Trajeto": [
                        "Linfonodos pancreaticoesplênicos",
                        "Linfonodos celíacos",
                        "Tronco intestinal",
                        "Cisterna do quilo",
                        "Ducto torácico",
                        "Ângulo venoso esquerdo"
                    ]
                },
                {
                    "Rota": "Parte Pilórica",
                    "Trajeto": [
                        "Linfonodos pilóricos",
                        "Linfonodos celíacos",
                        "Tronco intestinal",
                        "Cisterna do quilo",
                        "Ducto torácico",
                        "Ângulo venoso esquerdo"
                    ]
                }
            ]
        },
        "figado": {
            "nome": "Fígado",
            "rotas": [
                {
                    "Rota": "Drenagem Hepática descendente (maior parte da linfa)",
                    "Trajeto": [
                        "Linfonodos hepáticos",
                        "Linfonodos celíacos",
                        "Tronco intestinal",
                        "Cisterna do quilo",
                        "Ducto torácico",
                        "Ângulo venoso esquerdo"
                    ]
                },
                {
                    "Rota": "Drenagem Hepática ascendente (menor parte da linfa)",
                    "Trajeto": [
                        "Linfonodos frênicos (superiores e inferiores)",
                        "Tronco broncomediastinal",
                        "Ducto torácico ou Ducto linfático direito",
                        "Ângulo venoso esquerdo ou direito"
                    ]
                }
            ]
        },
        "baco": {
            "nome": "Baço",
            "rotas": [
                {
                    "Rota": "Drenagem Esplênica",
                    "Trajeto": [
                        "Linfonodos esplênicos",
                        "Linfonodos pancreaticoesplênicos",
                        "Linfonodos celíacos",
                        "Tronco intestinal",
                        "Cisterna do quilo",
                        "Ducto torácico",
                        "Ângulo venoso esquerdo"
                    ]
                }
            ]
        },
        "rins": {
            "nome": "Rins",
            "rotas": [
                {
                    "Rota": "Drenagem Renal",
                    "Trajeto": [
                        "Linfonodos lombares (direitos e esquerdos)",
                        "Troncos lombares (esquerdo e direito)",
                        "Cisterna do quilo",
                        "Ducto torácico",
                        "Ângulo venoso esquerdo"
                    ]
                }
            ]
        },
        "intestino_delgado": {
            "nome": "Intestino Delgado",
            "rotas": [
                {
                    "Rota": "Duodeno - face anterior",
                    "Trajeto": [
                        "Linfonodos pancreatoduodenais",
                        "Linfonodos celíacos",
                        "Tronco intestinal",
                        "Cisterna do quilo",
                        "Ducto torácico",
                        "Ângulo venoso esquerdo"
                    ]
                },
                {
                    "Rota": "Duodeno - face posterior",
                    "Trajeto": [
                        "Linfonodos pancreatoduodenais",
                        "Linfonodos mesentéricos superiores",
                        "Tronco intestinal",
                        "Cisterna do quilo",
                        "Ducto torácico",
                        "Ângulo venoso esquerdo"
                    ]
                },
                {
                    "Rota": "Jejuno/Íleo",
                    "Trajeto": [
                        "Linfonodos justaintestinais",
                        "Linfonodos mesentéricos",
                        "Linfonodos centrais superiores",
                        "Linfonodos mesentéricos superiores",
                        "Tronco intestinal",
                        "Cisterna do quilo",
                        "Ducto torácico",
                        "Ângulo venoso esquerdo"
                    ]
                }
            ]
        },
        "intestino_grosso": {
            "nome": "Intestino Grosso",
            "rotas": [
                {
                    "Rota": "Colo Ascendente",
                    "Trajeto": [
                        "Linfonodos epicólicos",
                        "Linfonodos paracólicos",
                        "Linfonodos colicos direitos",
                        "Linfonodos mesentéricos superiores",
                        "Tronco intestinal",
                        "Cisterna do quilo",
                        "Ducto torácico",
                        "Ângulo venoso esquerdo"
                    ]
                },
                {
                    "Rota": "Colo Transverso",
                    "Trajeto": [
                        "Linfonodos epicólicos",
                        "Linfonodos paracólicos",
                        "Linfonodos colicos médios",
                        "Linfonodos mesentéricos superiores",
                        "Tronco intestinal",
                        "Cisterna do quilo",
                        "Ducto torácico",
                        "Ângulo venoso esquerdo"
                    ]
                },
                {
                    "Rota": "Colo Descendente/Colo Sigmoide",
                    "Trajeto": [
                        "Linfonodos epicólicos",
                        "Linfonodos paracólicos",
                        "Linfonodos colicos esquerdos",
                        "Linfonodos mesentéricos inferiores",
                        "Tronco lombar esquerdo",
                        "Cisterna do quilo",
                        "Ducto torácico",
                        "Ângulo venoso esquerdo"
                    ]
                }
            ]
        }
    }

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

    st.subheader(f"Trajeto de drenagem - {rota['Rota']}")

    # Cria abas para cada etapa da rota de drenagem
    abas = st.tabs([f"Etapa {i+1}: {etapa}" for i, etapa in enumerate(caminho)])
    for i, aba in enumerate(abas):
        with aba:
            st.markdown(f"### Etapa {i+1}: {caminho[i]}")
            if i == 0:
                st.write(f"Início da drenagem linfática.")
            elif i < len(caminho) - 1:
                st.write(f"Drenagem para {caminho[i+1].lower()}.")
            else:
                st.write("Etapa final: Chegada a circulação venosa.")

if __name__ == "__main__":
    main()
