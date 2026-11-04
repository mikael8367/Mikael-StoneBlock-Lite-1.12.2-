#!/usr/bin/env python3
"""Static validation and CurseForge ZIP packaging for Mikael StoneBlock Lite."""
from pathlib import Path
import json, shutil, zipfile, tempfile

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest.json"
OUT = ROOT / "dist"
OUT.mkdir(exist_ok=True)

data = json.loads(MANIFEST.read_text(encoding="utf-8"))
assert data.get("manifestType") == "minecraftModpack"
assert data.get("manifestVersion") == 1
assert data.get("minecraft", {}).get("version") == "1.12.2"
loaders = data.get("minecraft", {}).get("modLoaders", [])
assert any(x.get("id") == "forge-14.23.5.2860" and x.get("primary") for x in loaders)
files = data.get("files", [])
projects = [x.get("projectID") for x in files]
file_ids = [x.get("fileID") for x in files]
assert all(isinstance(x, int) and x > 0 for x in projects + file_ids)
assert len(projects) == len(set(projects)), "projectID duplicado"
assert len(file_ids) == len(set(file_ids)), "fileID duplicado"
assert all(x.get("required") is True for x in files), "Entrada não obrigatória"
by_project = {x["projectID"]: x["fileID"] for x in files}
assert by_project.get(282561) == 9131646, "StoneBlock Utilities atualizado ausente"
assert by_project.get(302475) == 2722058, "Stone Crafting Table ausente"
assert by_project.get(257655) == 2666967, "Void Island Control ausente"
assert by_project.get(258911) == 2489010, "World Primer ausente"

overrides = ROOT / "overrides"
assert overrides.is_dir(), "Pasta overrides ausente"
vic_cfg = (overrides / "config" / "voidislandcontrol.cfg").read_text(encoding="utf-8")
stone_cfg = json.loads((overrides / "config" / "stoneblockutilities.json").read_text(encoding="utf-8"))
structure = overrides / "config" / "voidislandcontrolstructures" / "island.nbt"
assert "S:worldGenType=SUPERFLAT" in vic_cfg, "Tipo de mundo não é SUPERFLAT"
assert "255*minecraft:stone,minecraft:lava" in vic_cfg, "Camadas de pedra/lava não encontradas"
assert "S:islandMainSpawnType=island" in vic_cfg, "Ilha inicial customizada ausente"
assert "island" in vic_cfg and structure.is_file() and structure.stat().st_size > 0, "Estrutura inicial ausente"
assert stone_cfg.get("handDrops"), "Drops de pedra/pebbles não configurados"
assert stone_cfg.get("crookDrops"), "Drops do crook não configurados"

warnings = []
with tempfile.TemporaryDirectory() as td:
    stage = Path(td) / "pack"
    stage.mkdir()
    shutil.copy2(MANIFEST, stage / "manifest.json")
    shutil.copytree(overrides, stage / "overrides", dirs_exist_ok=True)

    quest_dir = stage / "overrides" / "config" / "ftbquests"
    if not quest_dir.exists():
        archives = sorted(ROOT.glob("Mikael-StoneBlock-Lite-*.zip"),
                          key=lambda p: p.stat().st_size, reverse=True)
        recovered = False
        for archive in archives:
            try:
                with zipfile.ZipFile(archive) as zf:
                    matches = [n for n in zf.namelist() if
                               n.replace("\\\\", "/").startswith(
                                   ("overrides/config/ftbquests/", "config/ftbquests/"))]
                    for name in matches:
                        normalized = name.replace("\\\\", "/")
                        marker = ("overrides/config/ftbquests/" if normalized.startswith(
                            "overrides/config/ftbquests/") else "config/ftbquests/")
                        relative = normalized.split(marker, 1)[1]
                        if not relative or ".." in Path(relative).parts:
                            continue
                        target = quest_dir / relative
                        if name.endswith("/"):
                            target.mkdir(parents=True, exist_ok=True)
                        else:
                            target.parent.mkdir(parents=True, exist_ok=True)
                            target.write_bytes(zf.read(name))
                    recovered = quest_dir.exists() and any(quest_dir.rglob("*"))
                    if recovered:
                        warnings.append(f"Config FTB Quests recuperada de {archive.name}; validar as missões no jogo.")
                        break
            except (zipfile.BadZipFile, OSError, KeyError) as exc:
                warnings.append(f"Não foi possível ler {archive.name}: {exc}")
        if not recovered:
            warnings.append("Config FTB Quests não encontrada; não afirmar que as 500 missões estão incluídas.")

    report = [
        f"Modpack: {data.get('name')}",
        f"Versão: {data.get('version')}",
        "Minecraft: 1.12.2",
        "Forge: 14.23.5.2860",
        f"Entradas CurseForge: {len(files)}",
        f"Project IDs únicos: {len(set(projects))}",
        f"File IDs únicos: {len(set(file_ids))}",
        "StoneBlock Utilities: 2.2.0 Beta (file 9131646)",
        "Stone Crafting Table: 1.0.3 (file 2722058)",
        "World generation: Void Island Control SUPERFLAT, 255 camadas de pedra + lava",
        f"Estrutura de ilha customizada: {'presente' if structure.exists() else 'ausente'}",
        f"Config FTB Quests presente: {'sim' if quest_dir.exists() else 'não'}",
        "Validação estática; não comprova inicialização real do Minecraft."
    ] + ["AVISO: " + w for w in warnings]
    (stage / "BUILD-REPORT.txt").write_text("\n".join(report) + "\n", encoding="utf-8")

    output = OUT / f"Mikael-StoneBlock-Lite-{data['version']}.zip"
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(stage.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(stage).as_posix())
    print("\n".join(report))
    print(f"Pacote criado: {output}")
