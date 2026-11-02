# Mikael StoneBlock Lite 1.12.2

Versão 0.3.0 — Forge 14.23.5.2860. Agora inclui geração e ilha StoneBlock, mods de início, FTB Quests, ProjectE, Thermal, Extreme Reactors, Draconic Evolution, Mekanism e otimizações para FPS/memória.

## Importação e mundo

Importe `Mikael-StoneBlock-Lite-0.3.0.zip` num launcher que aceite modpacks CurseForge. Os mods são resolvidos pelos IDs do manifest, não são JARs embutidos.

No single-player crie **um mundo novo** com `Void? World`. Em servidor, antes de gerar o mundo, use `level-type=voidworld` (a configuração vai em `overrides/server.properties`). O pacote contém a configuração e a estrutura NBT da ilha inicial StoneBlock.

## Conteúdo importante

- FPS/memória: FoamFix, TexFix, VanillaFix, BetterFps, FastWorkbench, FastFurnace, AI Improvements e Clumps. São ajustes independentes, sem garantia de FPS até testar no aparelho.
- Mekanism: Mekanism, Mekanism Generators e Mekanism Tools, todos na versão 9.8.3.390 para 1.12.2. Não incluí Mekanism Additions porque não achei release 1.12.2 desse módulo.
- Energia/máquinas: ProjectE, Thermal, Extreme Reactors + ZeroCore e Draconic Evolution + Brandon's Core, CodeChicken Lib e Project Intelligence.
- Início StoneBlock: StoneBlock Utilities, Ex Nihilo Creatio, Ex Compressum, Twerk Sim 2K16 + Game Stages, JEI/JER e itens de qualidade de vida.
- FTB Quests 1.9.0.11 + FTB Library, Item Filters e Forgelin. O mod está presente, mas capítulos/missões próprios ainda precisam ser escritos.

**Validação:** IDs/versões do manifest, JSON e arquivo ZIP foram conferidos. Não foi feito teste de inicialização nem de mundo no launcher do celular; este perfil é mais pesado que a versão anterior e pode passar da capacidade do Galaxy A12. Recomendo backup e teste em instância nova antes de usar um mundo importante.
