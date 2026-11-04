# Base de instalação — Minecraft 1.12.2 + Forge

Esta pasta contém somente os metadados e as instruções para preparar a instalação-base.
**Nenhum mod é incluído aqui.**

- Minecraft: `1.12.2`
- Forge: `14.23.5.2860`
- Java recomendado para esta geração: Java 8 (64 bits)

## Instalador oficial

O instalador é distribuído pelo servidor oficial do Forge. Consulte `forge-installer.url`.
SHA-1 oficial publicado para esse instalador: `5e8a91f71ef3d1f77de3f8d3261aedcc2f551c9d`.

## Sobre versions/ e libraries/

Essas pastas não devem ser preenchidas com arquivos vazios nem com JARs inventados.
O instalador do Forge e o launcher devem gerar/baixar os arquivos reais, incluindo o perfil
de versão e as bibliotecas. A estrutura de uma instância varia conforme o launcher.

## Conteúdo desta pasta

- `forge-version.json`: versão, URL oficial e hash SHA-1.
- `forge-installer.url`: endereço direto do instalador oficial.
- `instance-layout.txt`: diretórios esperados da instância, sem conteúdo de mods.

O manifesto principal do modpack na raiz do repositório não foi alterado.
