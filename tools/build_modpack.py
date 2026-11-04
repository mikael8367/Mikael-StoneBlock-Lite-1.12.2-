#!/usr/bin/env python3
"""Validate and package the CurseForge modpack without downloading mod JARs."""
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
assert (ROOT / "overrides").is_dir(), "Pasta overrides ausente"

warnings = []
with tempfile.TemporaryDirectory() as td:
    stage = Path(td) / "pack"
    stage.mkdir()
    shutil.copy2(MANIFEST, stage / "manifest.json")
    shutil.copytree(ROOT / "overrides", stage / "overrides", dirs_exist_ok=True)

    quest_dir = stage / "overrides" / "config" / "ftbquests"
    if not quest_dir.exists():
        # Recover the quest config from the previous tracked package, if present.
        archives = sorted(ROOT.glob("Mikael-StoneBlock-Lite-*.zip"),
                          key=lambda p: p.stat().st_size, reverse=True)
        recovered = False
        for archive in archives:
            try:
                with zipfile.ZipFile(archive) as zf:
                    names = zf.namelist()
                    matches = [n for n in names if
                               n.replace("\\\\", "/").startswith(
                                   ("overrides/config/ftbquests/", "config/ftbquests/"))]
                    if not matches:
                        continue
                    for name in matches:
                        normalized = name.replace("\\\\", "/")
                        marker = "overrides/config/ftbquests/" if normalized.startswith("overrides/config/ftbquests/") else "config/ftbquests/"
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
                        warnings.append(f"Config FTB Quests recuperada de {archive.name}; valide as missões no jogo.")
                        break
            except (zipfile.BadZipFile, OSError, KeyError) as exc:
                warnings.append(f"Não foi possível ler {archive.name}: {exc}")
        if not recovered:
            warnings.append("Config FTB Quests não encontrada no pacote atual nem nos ZIPs antigos; não afirmar que as 500 missões estão incluídas.")

    report = [
        f"Modpack: {data.get('name')}",
        f"Versão: {data.get('version')}",
        "Minecraft: 1.12.2",
        "Forge: 14.23.5.2860",
        f"Entradas CurseForge: {len(files)}",
        f"Project IDs únicos: {len(set(projects))}",
        f"File IDs únicos: {len(set(file_ids))}",
        f"Config FTB Quests presente: {'sim' if quest_dir.exists() else 'não'}",
        "Observação: os JARs são baixados pelo launcher compatível com o manifesto CurseForge.",
        "Este pacote não comprova inicialização bem-sucedida do jogo."
    ] + ["AVISO: " + w for w in warnings]
    (stage / "BUILD-REPORT.txt").write_text("\n".join(report) + "\n", encoding="utf-8")

    output = OUT / f"Mikael-StoneBlock-Lite-{data['version']}.zip"
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(stage.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(stage).as_posix())
    print("\n".join(report))
    print(f"Pacote criado: {output}")
