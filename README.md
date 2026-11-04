# Mikael StoneBlock Lite 0.5.15

Modpack para Minecraft Java **1.12.2**, com **Forge 14.23.5.2860**.

## Criação do mundo

**No single-player, confira se "Void? World" está selecionado antes de clicar em Criar.** O Void Island Control tenta pré-selecionar esse tipo ao abrir a tela pelo menu de seleção de mundos. Se estiver em Padrão ou Superflat vanilla, selecione "Void? World".

Leia o guia: [LEIA-ME-CRIAR-MUNDO-PTBR.txt](overrides/LEIA-ME-CRIAR-MUNDO-PTBR.txt).

## Conteúdo

- 66 referências CurseForge no manifesto.
- StoneBlock Utilities 2.2.0 Beta e Stone Crafting Table.
- Void Island Control + World Primer.
- Preset superflat com 255 camadas de pedra e 1 camada de lava.
- Ilha personalizada de estrutura NBT 11 × 11 × 11.
- FTB Library, FTB Utilities, FTB Quests e FTB Backups.

## Instalação

O repositório contém manifesto CurseForge e a pasta overrides. Um launcher compatível deve baixar os arquivos do manifesto e aplicar os overrides. Os JARs não são armazenados individualmente aqui.

O ZIP é gerado pelo GitHub Actions. Abra **Actions → Validar e empacotar modpack**, selecione a execução mais recente e baixe o artefato.

## Validação e limitações

O script verifica IDs e dependências estáticas, preset de mundo, referências do inventário inicial e a estrutura NBT comprimida (dimensões, paleta, marcador de spawn e espaço de jogador). A auditoria detalhada está em [WORLDGEN-AUDITORIA.md](WORLDGEN-AUDITORIA.md).

Essas verificações não substituem a inicialização real do Minecraft nem garantem ausência de incompatibilidades em runtime. Se houver falha, envie latest.log ou crash-reports.

OptiFine não está incluído.
