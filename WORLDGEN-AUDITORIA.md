# Auditoria profunda de criação de mundo — Mikael StoneBlock Lite 1.12.2

Versão: 0.5.15  
Minecraft: 1.12.2  
Forge: 14.23.5.2860

## Resultado

A revisão encontrou e corrigiu uma referência de item inicial órfã e fortaleceu o validador para analisar o preset de geração e a estrutura NBT da ilha antes de empacotar.

## 1. Correção aplicada: item inicial inválido

A configuração antiga continha bqt:bqt:0*1 em startingItems. O manifesto não contém Better Questing Triggerer (projectID 250193) nem Better Questing (projectID 238856), requisito do Triggerer. O item não podia ser resolvido pelo comando de item do Minecraft. O método de inventário inicial do Void Island Control captura essa falha, limpa o inventário e exibe um erro.

A referência foi removida, preservando os espaços vazios restantes da lista de inventário inicial. Não adicionamos Better Questing: o modpack usa FTB Quests e não precisa de um segundo sistema de quests para corrigir esse problema.

## 2. Verificação do tipo de mundo

- worldGenType=SUPERFLAT.
- Preset 3;255*minecraft:stone,minecraft:lava.
- A validação lê cada camada, valida os identificadores e confere 256 camadas no total.
- baseDimension=0.
- islandYLevel=88.
- islandDistance=1000.
- islandMainSpawnType=island e islandSpawnType=island.
- A lista customIslands contém island.

**Ação obrigatória na tela de criação:** no modo single-player, selecionar o tipo de mundo **Void? World**. O preset só é usado pelo gerador personalizado do Void Island Control. Deixar o tipo em Padrão ou escolher o Superflat vanilla não ativa essa lógica de ilhas.

## 3. Verificação estrutural do island.nbt

O validador agora descompacta e interpreta o NBT de verdade, em vez de conferir apenas se o arquivo existe.

- GZIP/NBT válido.
- DataVersion 1343, correspondente à era do Minecraft 1.12.2.
- Dimensões 11 × 11 × 11.
- 1.331 entradas de blocos.
- Paleta contém pedra, ar e bloco de estrutura.
- Exatamente um bloco de estrutura em modo DATA com metadado spawn_point.
- O marcador está em [5, 2, 5] e gera offset de spawn [0, 2, 0] após centralizar a ilha.
- O validador verifica espaço livre para pés/cabeça e o bloco de piso central.
- As posições de todos os blocos precisam estar dentro dos limites 11 × 11 × 11.

## 4. Comportamentos que parecem estranhos, mas são intencionais

Com autoCreate=true, o Void Island Control prepara a ilha principal no centro (0,0) e depois cria uma ilha individual para o primeiro jogador. Como a primeira posição livre da grade é (-1,-1), a primeira ilha pessoal fica a 1.000 blocos nos eixos X e Z do centro. O jogador é levado para a ilha individual. Isso pode parecer uma duplicação, mas corresponde ao fluxo de hub + ilha pessoal.

A proteção de spawn está ligada e cobre uma área central de 500 blocos; a ilha pessoal fica além desse raio. Não alteramos essa proteção para não bloquear a progressão.

## 5. Riscos conhecidos do mod upstream

- O código upstream de Void Island Control tem uma condição repetida em isCustomizable(): a ramificação para WORLDTYPE parece testar CUSTOMIZED novamente. Isso afeta o botão Customize apenas se worldGenType=WORLDTYPE; o modpack usa SUPERFLAT e não passa por esse caminho.
- O projeto original Void Island Control declara que não recebe mais suporte/atualizações. Não foi trocado por um fork, porque substituir o gerador de mundo pode afetar saves existentes.
- StoneBlock Utilities 2.2.0 Beta inclui correção de recuperação dos dados das ilhas do VIC quando o arquivo data/VICData.dat é perdido após falha de gravação. Ainda assim, faça backup dos mundos.
- A análise estática não consegue simular o botão Criar Mundo, a geração de chunks nem os eventos de primeiro login no jogo.

## 6. O que o build verifica agora

- Formato do manifesto, versão de Minecraft/Forge, IDs únicos e obrigatoriedade dos mods.
- IDs/arquivos exatos de StoneBlock Utilities, Stone Crafting Table, Void Island Control e World Primer.
- Sintaxe e 256 camadas do preset superflat.
- Tipo de mundo, dimensão, coordenadas e nomes da ilha.
- Referências de item inicial órfãs conhecidas.
- Estrutura NBT comprimida, paleta, blocos, marcador, offset e espaço de spawn.
- Empacotamento de manifest + overrides e recuperação condicional de FTB Quests.

**Limite:** build aprovado significa que os arquivos passaram nessas verificações. Não comprova que Minecraft inicializa ou gera um mundo real sem crash; isso ainda precisa de teste no launcher e análise de latest.log.
