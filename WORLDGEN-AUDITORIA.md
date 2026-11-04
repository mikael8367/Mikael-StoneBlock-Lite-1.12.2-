# Auditoria de travamentos e encerramentos — Mikael StoneBlock Lite 1.12.2

Versão auditada: 0.5.16  
Minecraft: 1.12.2  
Forge: 14.23.5.2860

## Correções e verificações do pacote

- Inventário inicial agora tem 36 slots com item vanilla válido e quantidade zero; não depende de Better Questing.
- StoneBlock Utilities 2.2.0 usa o esquema novo de `stoneblockutilities.json`. O pacote inclui o arquivo correto; atualização de instalação antiga exige substituir a configuração antiga.
- O validador verifica os campos `handDrops` e `crookDrops`, nomes de blocos/itens, metadados, limites de chance e velocidade, quantidade de drops e dependência de Ex Nihilo Creatio.
- Preset de mundo: 256 camadas, com 255 pedras e lava no topo.
- Configuração exige dimensão 0, Nether/End vanilla, tipo de ilha registrado, spawn automático e as distâncias previstas.
- NBT da ilha: arquivo GZIP/NBT decodificado, 11×11×11, 1.331 posições únicas, marcador único e espaço de nascimento livre.
- Servidor dedicado: `level-type=voidworld`.

## Tela Criar mundo

O código original do Void Island Control intercepta a abertura de `GuiCreateWorld` a partir de `GuiWorldSelection` e tenta selecionar o tipo especial registrado. O método de seleção percorre `WorldType.WORLD_TYPES`; se não encontrar o tipo, retorna índice 0 (Padrão). Isso pode produzir mundo errado sem necessariamente gerar um crash.

**Como conferir:** abra Singleplayer → Criar novo mundo e olhe o seletor de tipo de mundo antes de clicar em Criar. Confirme `Void? World`. Não use `Default/Padrão` nem o `Superflat` vanilla.

Foi identificado no código upstream um erro em `WorldTypeVoid.isCustomizable()`: a condição repete `CUSTOMIZED` em vez de verificar `WORLDTYPE`. Isso afeta a disponibilidade do botão Customize para a configuração WORLDTYPE; o pack usa SUPERFLAT, então não deve bloquear a tela atual.

## Histórico upstream relevante

- [VIC #69](https://github.com/Bartz24/VoidIslandControl/issues/69): `IndexOutOfBoundsException` ao criar ilha com dimensão base diferente da principal e lista vazia. O pack fixa `baseDimension=0`; a falha relatada não é reproduzida por essa configuração.
- [VIC #67](https://github.com/Bartz24/VoidIslandControl/issues/67): crash por tipo/estrutura de ilha customizada inválida. O pack fixa os tipos `island`, a lista `customIslands` e valida o arquivo NBT/marcador.
- [VIC #27](https://github.com/Bartz24/VoidIslandControl/issues/27): jogador preso após renascer em ilha customizada numa versão antiga 1.3.2. A estrutura atual passa pelas verificações de espaço livre, mas só o teste no jogo pode confirmar o respawn.
- [VIC #70](https://github.com/Bartz24/VoidIslandControl/issues/70): relato de perda de ilha após crash e saída de LAN. StoneBlock Utilities 2.2.0 adiciona backup da ilha nos dados individuais dos jogadores e recuperação quando `VICData.dat` é perdido.
- [VIC #86](https://github.com/Bartz24/VoidIslandControl/issues/86): falhas ao criar ilhas em dimensão não vanilla. Este pack usa dimensão 0 e mantém Nether/End vanilla.

Os issues são relatos históricos; não provam que o mesmo defeito acontece na configuração atual.

## StoneBlock Utilities: risco de config antiga

O StoneBlock oficial 1.0.38 avisa que o arquivo antigo `config/stoneblockutilities.json` causa crash na inicialização após atualizar para SBU 2.2.0; a nova configuração precisa ser aplicada também em instalações existentes. O pacote 0.5.16 contém o formato atualizado. Se o launcher preservou a config anterior, substitua-a pela versão de `overrides/config/stoneblockutilities.json` após fazer backup.

Referência: https://www.curseforge.com/minecraft/modpacks/stoneblock/files/9131806

## Encerramento inesperado durante o jogo

O manifesto atual não inclui Cyclic (Project ID 239286). Portanto, o crash loop histórico do StoneBlock oficial causado pela poção Saturation do Cyclic não corresponde à lista atual deste pacote.

A tela que parece congelada também pode estar aguardando geração/carregamento de chunks. O gerador usa 256 camadas por coluna de chunk; em Android com pouca memória disponível, um pico de memória/GC pode fechar o processo. Isso não pode ser confirmado sem o log do aparelho.

## Como classificar o próximo crash

- `Failed to load cfg`, `handDrops` ou `crookDrops`: provável config antiga/corrompida do StoneBlock Utilities.
- `IndexOutOfBoundsException` em `getSpawnOffset` ou `IslandGenerations.get`: tipo de ilha inexistente/desativado ou lista de gerações vazia.
- `OutOfMemoryError`, `GC overhead limit exceeded` ou encerramento sem crash report: suspeita de pressão de memória/processo encerrado pelo Android; verificar `latest.log` e o log do sistema.
- Travamento depois de morrer/renascer: verificar posição do marcador, espaço livre e stack trace de `PlayerRespawnEvent`.
- Tela Create World mostra Padrão: tipo `Void? World` não foi selecionado/registrado; não criar esse save até confirmar.

Não apague saves. Faça cópia antes de testar qualquer alteração.

## Limites

O validador verifica arquivos e metadados. Não clica na tela do Minecraft, não carrega Forge, não gera chunks reais e não reproduz a saída para o menu. Para fechar a investigação de um crash real, é necessário o `latest.log` ou arquivo em `crash-reports` obtido no launcher Android.
