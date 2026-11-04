# Mikael StoneBlock Lite 0.5.13

Modpack para Minecraft Java **1.12.2**, com **Forge 14.23.5.2860**.

## Instalação

Este repositório contém um manifesto CurseForge e a pasta `overrides`. Um launcher compatível com o formato de modpack CurseForge deve ler o `manifest.json`, baixar os arquivos listados e aplicar os overrides. Os JARs não são armazenados individualmente neste repositório.

O ZIP de distribuição é gerado automaticamente pelo GitHub Actions. Abra **Actions → Validar e empacotar modpack**, selecione a execução mais recente e baixe o artefato `Mikael-StoneBlock-Lite-...`.

## Conteúdo e validações

- Minecraft 1.12.2 / Forge 14.23.5.2860.
- 65 referências CurseForge no manifesto.
- Placebo e ConnectedTexturesMod (CTM) incluídos como dependências identificadas.
- O empacotador verifica JSON, IDs repetidos, IDs inválidos, entradas obrigatórias e versão do Forge.
- O empacotador tenta recuperar a configuração FTB Quests de um ZIP antigo se ela não estiver em `overrides/config/ftbquests`.

## FTB Quests

A configuração de quests não está visível como arquivos individuais na árvore atual do repositório. Durante o empacotamento, o script procura essa configuração nos ZIPs antigos. O relatório dentro do ZIP informa se ela foi recuperada. **Não considere as 500 missões confirmadas até conferir esse relatório e testar o carregamento no jogo.**

## Limitações de teste

A validação automática é estática: não inicia o Minecraft, não carrega os mods e não garante ausência de crash ou conflito em runtime. É necessário testar a instância no launcher e guardar o `latest.log` ou `crash-reports` se houver falha.

OptiFine não está incluído no manifesto.
