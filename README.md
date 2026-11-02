# Mikael StoneBlock Lite 1.12.2

Projeto do modpack StoneBlock Lite para Minecraft Java 1.12.2, com foco em uma progressão StoneBlock e em manter o perfil moderado para dispositivos com pouca memória.

> **Estado: em montagem — ainda não é um pacote instalável.** A lista de mods é uma proposta inicial. Versões, dependências, receitas, quests e inicialização precisam ser validadas antes de publicar um manifest de launcher ou afirmar compatibilidade.

## Meta técnica

- Minecraft Java 1.12.2.
- Forge 14.23.5.2860 como versão-alvo inicial.
- Progressão em mundo de pedra: pedrinhas → bancada/crook → mudas e silkworm → terra e recursos básicos.
- Máquinas e magia em seleção moderada, com quests que ensinem cadeias realmente acessíveis.
- Evitar incluir OptiFine ou JARs redistribuíveis sem autorização; usar arquivos de distribuição oficiais do launcher/plataforma.

## Estrutura

- `MODLIST.md` — proposta de conteúdo e validações pendentes.
- `.gitignore` — evita enviar JARs, saves, logs e arquivos temporários por acidente.

## Instalação

Ainda não há um ZIP ou manifest importável. Não instale este repositório como modpack até que a lista esteja verificada e uma versão de distribuição seja publicada.

## Testes exigidos antes de marcar como pronto

1. Confirmar versão e dependências de cada mod para Forge 1.12.2.
2. Checar IDs, metadados, receitas e objetivos de quests contra os mods efetivamente incluídos.
3. Iniciar uma instância limpa, gerar o mundo StoneBlock e testar a progressão inicial.
4. Verificar inicialização e memória no dispositivo-alvo; validação de arquivos sozinha não prova compatibilidade no aparelho.

## Licenças

Cada mod mantém sua própria licença. Este repositório não redistribui JARs de terceiros; use as páginas oficiais de cada projeto e respeite seus termos.
