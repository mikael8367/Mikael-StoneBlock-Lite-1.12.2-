# Auditoria de dependências — Mikael StoneBlock Lite 1.12.2

Versão auditada: 0.5.13  
Minecraft: 1.12.2  
Forge: 14.23.5.2860

## Resultado da auditoria

- 65 entradas no manifesto.
- Nenhum `projectID` duplicado.
- Nenhum `fileID` duplicado.
- Todas as relações marcadas como `RequiredDependency` encontradas nas páginas dos 63 arquivos originais foram comparadas com o manifesto.
- Duas dependências obrigatórias ausentes foram adicionadas: Placebo e ConnectedTexturesMod (CTM).
- Os dois arquivos adicionados foram conferidos individualmente e são releases para Minecraft 1.12.2.
- As dependências obrigatórias identificadas já estão presentes ou foram adicionadas.

## Dependências adicionadas nesta auditoria

| Dependência | CurseForge Project ID | File ID | Arquivo |
|---|---:|---:|---|
| Placebo | 283644 | 2537494 | Placebo-1.12.2-1.3.1.jar |
| ConnectedTexturesMod (CTM) | 267602 | 2915363 | CTM-MC1.12.2-1.0.2.31.jar |

## Relações obrigatórias verificadas

- StoneBlockUtilities → Shadowfacts' Forgelin
- FTB Quests → FTB Library; Item Filters
- Thermal Foundation → CoFH Core; CoFH World
- Thermal Expansion → CodeChicken Lib; Thermal Foundation
- Extreme Reactors → ZeroCore 2
- Draconic Evolution → Brandon's Core; CodeChicken Lib; Redstone Flux
- Mekanism Generators → Mekanism
- Mekanism Tools → Mekanism
- Mod dependente de Placebo (Project ID 288885) → Placebo
- Game Stages → Bookshelf
- Dependência de JEI (Project ID 240630) → Just Enough Items (JEI)
- Builder's Bag - ProjectE Addon → Builder's Bag; ProjectE
- Dependência Draconic (Project ID 314515) → Baubles; Brandon's Core; Draconic Evolution; Project Intelligence
- FTB Utilities → FTB Library
- ProjectEX → Mike's Mods Library; ProjectE
- Thermal Cultivation → Thermal Foundation
- Thermal Dynamics → CodeChicken Lib; Thermal Foundation
- Thermal Innovation → Thermal Foundation
- Chisel → ConnectedTexturesMod (CTM)
- Botania → Baubles

## Relações que não exigem adicionar outro mod

- CoFH Lib aparece como `EmbeddedLibrary` na relação de CoFH Core; não foi adicionada como JAR separado.
- JourneyMap Tools aparece como `Tool`, não como dependência obrigatória de execução.
- Relações `OptionalDependency` foram preservadas como opcionais; não foram convertidas em dependências obrigatórias.

## Duplicatas

Nenhum `projectID` ou `fileID` repetido foi encontrado no manifesto após a atualização. Mods diferentes da mesma família (por exemplo, módulos separados de Mekanism) foram mantidos porque não são duplicatas.

## Empacotamento automatizado 0.5.13

- GitHub Actions executou a validação e o empacotamento com sucesso.
- Artefato ZIP gerado: `Mikael-StoneBlock-Lite-0.5.13.zip`.
- A configuração FTB Quests foi recuperada do arquivo antigo `Mikael-StoneBlock-Lite-0.5.7.zip` e incluída no pacote gerado.
- O log do build confirmou a presença da pasta de configuração, mas não contou nem validou individualmente as 500 missões.
- O pacote contém manifesto e overrides; os JARs continuam sendo baixados por um launcher compatível com CurseForge.

## Limites

A verificação cobre os metadados de dependência publicados pelo CurseForge para os arquivos listados. Ela não substitui um teste de inicialização real no launcher nem garante ausência de incompatibilidades entre mods.