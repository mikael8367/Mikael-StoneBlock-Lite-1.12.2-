# Mikael StoneBlock Lite 1.12.2

Modpack em montagem para Minecraft Java 1.12.2, usando Forge 14.23.5.2860. Objetivo: progressão StoneBlock com seleção moderada e compatibilidade a verificar em dispositivos com memória limitada.

## Estado atual: esqueleto importável, ainda incompleto

O repositório contém um `manifest.json` CurseForge com dois mods referenciados por IDs, Forge 14.23.5.2860 e pasta `overrides/`. Isso dá a estrutura de um modpack CurseForge, mas ainda não representa um pacote final ou testado: faltam mods importantes para jogar/construir a progressão completa, configurações, quests e testes num launcher.

O manifest usa o formato de exportação CurseForge; cada mod é identificado por `projectID` e `fileID` e o conteúdo de `overrides/` é copiado para a instância.

## Como importar

1. Baixe o ZIP desta versão pelo GitHub (Code → Download ZIP).
2. Importe o ZIP no CurseForge App ou em um launcher compatível com manifest CurseForge.
3. Se o launcher disser que há poucos mods ou que o pack está incompleto, isso é esperado nesta versão de rascunho.

**Não renomeie o repositório inteiro para `.mrpack`:** a estrutura aqui é CurseForge `manifest.json`, não Modrinth `modrinth.index.json`.

## Conteúdo atual

- `manifest.json` — Minecraft 1.12.2, Forge 14.23.5.2860, dois mods referenciados.
- `overrides/` — pasta reservada para configurações, scripts e quests do pack.
- `modlist.html` — lista humana dos dois mods do manifest.
- `MODLIST.md` — conteúdo proposto e validações pendentes.

## Testes pendentes

- Completar e verificar a lista de mods, dependências e arquivos CurseForge.
- Adicionar JEI e os mods de quests e dependências depois de conferir versões e arquivos exatos.
- Configurar e testar progressão StoneBlock desde o início, incluindo receitas/itens realmente disponíveis.
- Testar inicialização e consumo de memória no launcher/dispositivo-alvo. Estrutura e JSON válidos não provam que o jogo inicia.

Não há JARs embutidos; o launcher baixa os arquivos referenciados. Respeite as licenças e permissões de cada mod. OptiFine não é distribuído neste pack.
