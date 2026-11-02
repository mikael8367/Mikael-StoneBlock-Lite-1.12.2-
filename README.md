# Mikael StoneBlock Lite 0.5.10 — correção de índices FTB Quests

Minecraft 1.12.2 / Forge 14.23.5.2860.

## Alterações
- Mantidas as 500 missões opcionais, sem dependências entre quests.
- Removidos os 19 arquivos `index.nbt` redundantes dentro das pastas de capítulo; mantido o índice geral `chapters/index.nbt` usado pelo FTB Quests 1.12.2.
- Esta mudança trata os avisos `Failed to read quest ID index.nbt` registrados no log enviado.

## Download
[Baixar Mikael-StoneBlock-Lite-0.5.10.zip](https://raw.githubusercontent.com/mikael8367/Mikael-StoneBlock-Lite-1.12.2-/main/Mikael-StoneBlock-Lite-0.5.10.zip)

ZIP e contagem verificados: 500 quests, zero pré-requisitos entre elas, índice geral presente e índices de capítulo redundantes removidos. O log anterior mostra que o jogo carregou as 500 quests e entrou no mundo; ainda não existe log de teste desta versão corrigida.

Para substituir numa instância existente, faça backup e troque a pasta `config/ftbquests/normal` completa, senão arquivos antigos de índices podem continuar lá. OptiFine HD U G5 permanece fora do ZIP.
