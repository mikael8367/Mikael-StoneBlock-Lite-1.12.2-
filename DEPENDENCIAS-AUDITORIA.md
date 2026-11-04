# Auditoria técnica — Mikael StoneBlock Lite 1.12.2

Versão: 0.5.14  
Minecraft: 1.12.2  
Forge: 14.23.5.2860

## Atualizações desta revisão

- StoneBlock Utilities atualizado de fileID 2706845 (2.1.5) para fileID 9131646 (2.2.0 Beta), projeto 282561.
- Stone Crafting Table adicionado: projectID 302475, fileID 2722058 (1.12.2 Forge).
- Void Island Control (projectID 257655) e World Primer (projectID 258911) mantidos.
- A versão 2.2.0 Beta do StoneBlock Utilities informa correções para crash do Ex Compressum ao processar alimentos com efeitos de poção em fake players, restauração/persistência de ilhas do Void Island Control e drops do crook.
- Forge 14.23.5.2860 satisfaz o requisito mínimo informado de 14.23.5.2792 para o arquivo 2.2.0.

## Configuração do mundo verificada estaticamente

- `worldGenType=SUPERFLAT`.
- Preset contém `255*minecraft:stone,minecraft:lava`.
- Ilha inicial configurada como estrutura customizada `island`.
- `island.nbt` está presente no caminho de estruturas do Void Island Control.
- `stoneblockutilities.json` contém regras de drops de pedra e crook.

Isso confirma a configuração declarada nos arquivos, não a aparência final ou a geração real do mundo dentro do jogo.

## Verificações do manifesto

O workflow valida:
- JSON e formato CurseForge.
- Minecraft 1.12.2 e Forge 14.23.5.2860.
- IDs positivos, sem projectID/fileID duplicados.
- Todas as entradas obrigatórias.
- Presença e IDs esperados dos mods de mundo e bancada.
- Configurações de mundo e StoneBlock Utilities.
- Presença da estrutura inicial.

## Limites e riscos ainda abertos

- StoneBlock Utilities 2.2.0 é Beta, não Release estável. Foi escolhido porque contém correções relevantes para os mods que já estão no pack; ainda exige teste real.
- Stone Crafting Table adiciona uma bancada distinta da bancada de trabalho do StoneBlock Utilities. São dois mods diferentes; verificar receitas e registro de blocos em jogo.
- A pasta FTB Quests é recuperada de um ZIP antigo no build. O número e a integridade das missões não são confirmados automaticamente.
- Nenhum workflow estático consegue provar que os 66 mods iniciam juntos. É necessário obter `latest.log` ou `crash-reports` de uma execução real.
- Os JARs são baixados pelo launcher compatível com CurseForge; não estão armazenados neste repositório.

## Referências CurseForge

- StoneBlock Utilities: projectID 282561, fileID 9131646.
- Stone Crafting Table: projectID 302475, fileID 2722058.
- Void Island Control: projectID 257655, fileID 2666967.
- World Primer: projectID 258911, fileID 2489010.


## Revisão de criação de mundo 0.5.15

A auditoria dedicada de geração de mundo está em `WORLDGEN-AUDITORIA.md`. A revisão removeu a referência órfã `bqt:bqt:0*1` do inventário inicial e adicionou verificações do preset superflat e do NBT da ilha customizada ao build.
