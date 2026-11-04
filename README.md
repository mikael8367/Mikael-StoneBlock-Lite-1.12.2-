# Mikael StoneBlock Lite 0.5.19

Modpack para Minecraft Java **1.12.2**, com **Forge 14.23.5.2860**.

## Criação do mundo

No single-player, confirme se **Void? World** está selecionado antes de clicar em Criar. O Void Island Control tenta pré-selecionar esse tipo no fluxo normal Singleplayer → seleção de mundos → Criar novo mundo. Padrão e Superflat vanilla não ativam a geração personalizada.

No servidor dedicado, o arquivo incluído usa `level-type=voidworld`.

Guia: [LEIA-ME-CRIAR-MUNDO-PTBR.txt](overrides/LEIA-ME-CRIAR-MUNDO-PTBR.txt).

## Correções e verificações de crash

- Inventário inicial corrigido para 36 slots válidos e vazios; removida referência Better Questing que não existia no manifesto.
- StoneBlock Utilities 2.2.0: formato JSON atualizado incluído. Instalações antigas precisam substituir o arquivo antigo `config/stoneblockutilities.json` pelo arquivo deste pacote; a versão nova do mod não migra automaticamente o esquema antigo.
- Nether e End mantêm os provedores vanilla; o pack não tenta sobrescrevê-los como dimensões vazias.
- Validador inspeciona o preset superflat, dimensões, tipo de mundo, configuração SBU e toda a estrutura NBT da ilha.
- A configuração da ilha exige o tipo `island` e o arquivo `island.nbt`.

## Conteúdo

- 65 referências CurseForge no manifesto (JourneyMap removido).
- JEI 4.16.5.1030 Release (substitui a build 4.22.0.1034 que falhou ao ler uma classe no log de teste).
- StoneBlock Utilities 2.2.0 Beta e Stone Crafting Table.
- Void Island Control Remastered 1.5.5 + World Primer 0.6.0-dev.20200122.211517 (atualizado após crash de inicialização na 0.5.0).
- Preset superflat com 255 camadas de pedra e 1 camada de lava.
- Ilha personalizada de estrutura NBT 11 × 11 × 11.
- FTB Library, FTB Utilities, FTB Quests e FTB Backups.
- JourneyMap removido do manifesto.
- `optionsof.txt` incluído com Fast Render, Render Regions e Smooth World desativados para instalações que usam OptiFine/GL4ES.

## Instalação

O repositório contém manifesto CurseForge e a pasta `overrides`. Um launcher compatível deve baixar os arquivos do manifesto e aplicar os overrides. Os JARs não são armazenados individualmente aqui.

O ZIP é gerado pelo GitHub Actions. Abra **Actions → Validar e empacotar modpack**, selecione a execução mais recente e baixe o artefato.

## Diagnóstico

Se o Minecraft fechar ao iniciar, abrir a tela de criação ou entrar no mundo, guarde `latest.log` e o relatório em `crash-reports`. Não apague o save nem as configurações antes de fazer uma cópia. Consulte [WORLDGEN-AUDITORIA.md](WORLDGEN-AUDITORIA.md).

As verificações automáticas são estáticas; não iniciam o Minecraft e não garantem ausência de crash em runtime. OptiFine não está incluído. Se o launcher preservar um `optionsof.txt` antigo, substitua-o pelo arquivo deste pacote ou faça uma instalação limpa para aplicar as opções seguras. O arquivo de opções não substitui o teste real no Android.
