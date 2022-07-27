# Algoritmos de Aprendizado por Reforço Aplicados a Jogos Digitais

Este trabalho foi desenvolvido para a disciplina MS777 - Projeto Supervisionado, e teve como objetivo aplicar algoritmos de aprendizado por reforço ao jogo Pac-Man. Para isso, utilizamos uma técnica de Q-Learning aproximado, com a qual, combinamos as características do ambiente e seus respectivos pesos. Ao fim dos experimentos, pudemos otimizar o agente para obter altos índices de vitórias em diferentes layouts do jogo e pudemos concluir também quais as características mais importantes para sua vitória e os efeitos da normalização das características. 
O ambiente do jogo que utilizamos está disponível em: https://gitlab.techniek.hva.nl/artificial-intelligence/pacman-contest-3

Para reproduzir nossos resultados, basta clonar esse repositório e utilizar o seguinte comando no terminal:

$  python3 pacman.py -l originalClassic --pacman RLAgent_final -x 95 -n 115 -f 4

Note, o paramêtro -l (ou --layout) é passado para que você escolha qual layout gostaria de usar. O paramêtro -p (ou --pacman) é passado para que você escolha qual agente quer utilizar. Os agentes deve ser classes e com "Agent" nos nomes. O parâmetro -x representa o número de partidas de treino e -n o número total de partidas. Então, caso você passe -x 95 -n 115, o agente terá 95 partidas de treino e o restante de teste.
O parâmetro -f é apenas uma seed para que joguemos sempre as mesmas partidas e assim, possamos avaliar nossa real evolução nos jogos.
