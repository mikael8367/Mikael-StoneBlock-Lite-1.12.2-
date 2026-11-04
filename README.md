# Mikael StoneBlock Lite 0.5.14

Modpack para Minecraft Java **1.12.2**, com **Forge 14.23.5.2860**.

## Mundo StoneBlock

- Void Island Control configura o mundo SUPERFLAT com 255 camadas de pedra e uma camada de lava.
- A ilha inicial personalizada é carregada de `overrides/config/voidislandcontrolstructures/island.nbt`.
- World Primer permanece no manifesto.
- StoneBlock Utilities 2.2.0 Beta fornece os recursos do StoneBlock, incluindo bancada de trabalho de pedra e crook; esta versão também corrige problemas com Ex Compressum e persistência de ilhas do Void Island Control.
- Stone Crafting Table 1.0.3 adiciona uma bancada de pedra separada, conforme solicitado.

## Instalação

O repositório contém manifesto CurseForge e `overrides`. Um launcher compatível deve baixar os arquivos do manifesto e aplicar os overrides. Os JARs não são armazenados individualmente aqui.

O ZIP é gerado pelo GitHub Actions. Abra **Actions → Validar e empacotar modpack**, selecione a execução mais recente e baixe o artefato.

## Validação

O script valida JSON, IDs duplicados/inválidos, versões do Minecraft/Forge, presença dos mods de mundo, configuração de geração de pedra, configuração StoneBlock Utilities e estrutura inicial. Também tenta recuperar a configuração FTB Quests de ZIPs antigos.

A validação é estática: não inicia o jogo, não confirma a quantidade de missões e não garante ausência de crashes em runtime. Para isso, é necessário iniciar a instância no launcher e analisar `latest.log` ou `crash-reports`.

OptiFine não está incluído.
