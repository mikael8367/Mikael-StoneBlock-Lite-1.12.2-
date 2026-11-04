#!/usr/bin/env python3
"""Static validation and CurseForge ZIP packaging for Mikael StoneBlock Lite."""
from pathlib import Path
import gzip
import io
import json
import math
import re
import shutil
import struct
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest.json"
OUT = ROOT / "dist"
OUT.mkdir(exist_ok=True)


def read_exact(stream, length):
    data = stream.read(length)
    if len(data) != length:
        raise ValueError("NBT truncado")
    return data


def read_u8(stream):
    return struct.unpack(">B", read_exact(stream, 1))[0]


def read_i32(stream):
    return struct.unpack(">i", read_exact(stream, 4))[0]


def read_nbt_string(stream):
    length = struct.unpack(">H", read_exact(stream, 2))[0]
    return read_exact(stream, length).decode("utf-8")


def read_nbt_payload(tag, stream):
    if tag == 1:
        return struct.unpack(">b", read_exact(stream, 1))[0]
    if tag == 2:
        return struct.unpack(">h", read_exact(stream, 2))[0]
    if tag == 3:
        return read_i32(stream)
    if tag == 4:
        return struct.unpack(">q", read_exact(stream, 8))[0]
    if tag == 5:
        return struct.unpack(">f", read_exact(stream, 4))[0]
    if tag == 6:
        return struct.unpack(">d", read_exact(stream, 8))[0]
    if tag == 7:
        length = read_i32(stream)
        if length < 0:
            raise ValueError("NBT byte array com tamanho negativo")
        return read_exact(stream, length)
    if tag == 8:
        return read_nbt_string(stream)
    if tag == 9:
        child_tag = read_u8(stream)
        length = read_i32(stream)
        if length < 0 or length > 2_000_000:
            raise ValueError("NBT list com tamanho inválido")
        return [read_nbt_payload(child_tag, stream) for _ in range(length)]
    if tag == 10:
        compound = {}
        while True:
            child_tag = read_u8(stream)
            if child_tag == 0:
                return compound
            name = read_nbt_string(stream)
            compound[name] = read_nbt_payload(child_tag, stream)
    if tag == 11:
        length = read_i32(stream)
        if length < 0 or length > 2_000_000:
            raise ValueError("NBT int array com tamanho inválido")
        return list(struct.unpack(">" + "i" * length, read_exact(stream, 4 * length)))
    if tag == 12:
        length = read_i32(stream)
        if length < 0 or length > 2_000_000:
            raise ValueError("NBT long array com tamanho inválido")
        return list(struct.unpack(">" + "q" * length, read_exact(stream, 8 * length)))
    raise ValueError(f"Tipo NBT desconhecido: {tag}")


def load_structure(path):
    raw = path.read_bytes()
    if raw[:2] != b"\x1f\x8b":
        raise ValueError("island.nbt não está em formato gzip NBT")
    stream = io.BytesIO(gzip.decompress(raw))
    root_tag = read_u8(stream)
    if root_tag != 10:
        raise ValueError("Raiz NBT não é Compound")
    read_nbt_string(stream)
    return read_nbt_payload(root_tag, stream)


def config_value(text, key, kind="S"):
    match = re.search(r"^\s*" + re.escape(kind) + ":" + re.escape(key) + r"=(.*?)\s*$", text, re.M)
    if not match:
        raise AssertionError(f"Config Void Island Control sem {key}")
    return match.group(1)


def validate_world_config(config_text, stone_config, manifest_projects):
    world_type = config_value(config_text, "worldGenType")
    assert world_type == "SUPERFLAT", f"worldGenType inesperado: {world_type}"
    preset = config_value(config_text, "worldGenSpecialParameters")
    preset_match = re.fullmatch(r"(\d+);(.+)", preset)
    assert preset_match, "Preset superflat malformado"
    assert int(preset_match.group(1)) == 3, "Versão do preset superflat inesperada"

    total_layers = 0
    for layer in preset_match.group(2).split(","):
        item = re.fullmatch(r"(\d+\*)?([a-z0-9_.-]+:[a-z0-9_./-]+)", layer)
        assert item, f"Camada superflat inválida: {layer}"
        count = int(item.group(1)[:-1]) if item.group(1) else 1
        block_id = item.group(2)
        assert block_id.startswith("minecraft:"), f"Bloco externo não previsto no preset: {block_id}"
        total_layers += count
    assert total_layers == 256, f"Preset tem {total_layers} camadas, esperado 256"

    assert int(config_value(config_text, "baseDimension", "I")) == 0
    assert config_value(config_text, "netherVoid", "B").lower() == "false"
    assert config_value(config_text, "endVoid", "B").lower() == "false"
    assert config_value(config_text, "islandMainSpawnType") == "island"
    assert config_value(config_text, "islandSpawnType") == "island"
    assert config_value(config_text, "islandYLevel", "I") == "88"
    assert config_value(config_text, "islandDistance", "I") == "1000"
    assert config_value(config_text, "autoCreate", "B").lower() == "true"
    assert config_value(config_text, "resetInventory", "B").lower() == "false", (
        "resetInventory deve ficar desativado para preservar inventário em recuperação"
    )

    custom_match = re.search(r"S:customIslands\s*<([\s\S]*?)>", config_text)
    assert custom_match, "Lista customIslands ausente"
    custom_islands = [line.strip() for line in custom_match.group(1).splitlines() if line.strip()]
    assert "island" in custom_islands, "A estrutura 'island' não está registrada na config"

    inventory_match = re.search(r"S:startingItems\s*<([\s\S]*?)>", config_text)
    assert inventory_match, "Lista startingItems ausente"
    starting_items = [line.strip() for line in inventory_match.group(1).splitlines() if line.strip()]
    assert len(starting_items) == 36, f"Inventário inicial precisa ter exatamente 36 slots; encontrados: {len(starting_items)}"
    for item in starting_items:
        item_match = re.fullmatch(r"([a-z0-9_.-]+:[a-z0-9_./-]+):(\d+)\*(\d+)", item)
        assert item_match, f"Entrada startingItems inválida: {item}"
        assert item_match.group(1) == "minecraft:stone" and int(item_match.group(3)) == 0, (
            f"Slot inicial deve ser vazio e usar item vanilla válido: {item}"
        )
    assert 250193 not in manifest_projects and 238856 not in manifest_projects, (
        "O modpack não deve depender do Better Questing Triggerer nem Better Questing"
    )

    validate_sbu_config(stone_config, manifest_projects)


def parse_registry_reference(value, label):
    assert isinstance(value, str), f"{label} deve ser texto"
    parts = value.split(":")
    assert len(parts) == 3, f"{label} inválido: {value}"
    namespace, name, metadata = parts
    assert re.fullmatch(r"[a-z0-9_.-]+", namespace), f"Namespace inválido em {label}: {value}"
    assert re.fullmatch(r"[a-z0-9_./-]+", name), f"ID inválido em {label}: {value}"
    assert metadata.isdigit(), f"Metadata inválida em {label}: {value}"
    return namespace, name, int(metadata)


def validate_sbu_config(config, manifest_projects):
    # StoneBlock Utilities 2.2.0 changed this schema. Older configs can crash
    # during startup because the current parser iterates handDrops/crookDrops.
    assert isinstance(config, dict), "Config StoneBlock Utilities não é um objeto JSON"
    assert isinstance(config.get("active_render"), bool), "active_render ausente ou inválido"
    hand = config.get("handDrops")
    crook = config.get("crookDrops")
    assert isinstance(hand, list) and hand, "handDrops ausente; possível config antiga do SBU"
    assert isinstance(crook, list) and crook, "crookDrops ausente; possível config antiga do SBU"

    for index, entry in enumerate(hand):
        assert isinstance(entry, dict), f"handDrops[{index}] inválido"
        block_ns, block_name, block_meta = parse_registry_reference(entry.get("block"), f"handDrops[{index}].block")
        drop_ns, drop_name, drop_meta = parse_registry_reference(entry.get("drop"), f"handDrops[{index}].drop")
        assert block_ns == "minecraft" and block_name == "stone" and block_meta == 0, (
            f"Drop de mão deve referenciar pedra vanilla: handDrops[{index}]"
        )
        assert drop_ns == "exnihilocreatio" and drop_name == "item_pebble", (
            f"Drop de pedra inesperado: handDrops[{index}].drop"
        )
        assert 274456 in manifest_projects, "Ex Nihilo Creatio ausente, mas o drop de pebble depende dele"
        for key in ("drop_with", "drop_without"):
            assert isinstance(entry.get(key), int) and entry[key] >= 0, f"{key} inválido em handDrops[{index}]"
        assert isinstance(entry.get("chance"), int) and 0 <= entry["chance"] <= 100, (
            f"chance fora de 0..100 em handDrops[{index}]"
        )
        speed = entry.get("speed")
        assert isinstance(speed, (int, float)) and math.isfinite(speed) and 0 < speed <= 100, (
            f"speed inválido em handDrops[{index}]"
        )

    for index, entry in enumerate(crook):
        assert isinstance(entry, dict), f"crookDrops[{index}] inválido"
        block_ns, block_name, block_meta = parse_registry_reference(entry.get("block"), f"crookDrops[{index}].block")
        assert block_ns == "minecraft" and block_name == "dirt" and block_meta == 0, (
            f"Drop de crook deve referenciar dirt vanilla: crookDrops[{index}]"
        )
        assert isinstance(entry.get("randomDrop"), bool), f"randomDrop inválido em crookDrops[{index}]"
        amount = entry.get("randomDropAmount")
        drops = entry.get("drops")
        assert isinstance(amount, int) and amount >= 1, f"randomDropAmount inválido em crookDrops[{index}]"
        assert isinstance(drops, list) and drops, f"Lista drops vazia em crookDrops[{index}]"
        assert amount <= len(drops), f"randomDropAmount maior que a lista em crookDrops[{index}]"
        for drop_index, drop in enumerate(drops):
            assert isinstance(drop, dict), f"crookDrops[{index}].drops[{drop_index}] inválido"
            ns, name, meta = parse_registry_reference(
                drop.get("drop"), f"crookDrops[{index}].drops[{drop_index}].drop"
            )
            assert ns == "minecraft" and name == "sapling" and 0 <= meta <= 5, (
                f"Drop de crook fora da lista de mudas vanilla: {drop}"
            )
            assert isinstance(drop.get("drop_size"), int) and drop["drop_size"] >= 1, (
                f"drop_size inválido em crookDrops[{index}].drops[{drop_index}]"
            )


def validate_structure(path, island_y):
    root = load_structure(path)
    size = root.get("size")
    palette = root.get("palette")
    blocks = root.get("blocks")
    assert root.get("DataVersion") == 1343, f"DataVersion NBT inesperado: {root.get('DataVersion')}"
    assert size == [11, 11, 11], f"Dimensão NBT inesperada: {size}"
    assert isinstance(palette, list) and palette, "Palette NBT ausente"
    assert isinstance(blocks, list) and len(blocks) == 11 * 11 * 11, "Quantidade de blocos NBT incorreta"
    assert island_y >= 0 and island_y + size[1] <= 256, "Estrutura ultrapassa os limites verticais"

    names = [entry.get("Name") for entry in palette]
    assert "minecraft:stone" in names, "Estrutura sem pedra"
    assert "minecraft:air" in names, "Estrutura sem cavidade de ar"
    assert "minecraft:structure_block" in names, "Estrutura sem bloco de dados de spawn"

    block_by_pos = {}
    seen_positions = set()
    markers = []
    counts = {}
    for entry in blocks:
        pos = entry.get("pos")
        state_index = entry.get("state")
        assert isinstance(pos, list) and len(pos) == 3, "Posição de bloco NBT inválida"
        assert all(isinstance(v, int) and 0 <= v < size[i] for i, v in enumerate(pos)), (
            f"Bloco fora dos limites da estrutura: {pos}"
        )
        assert isinstance(state_index, int) and 0 <= state_index < len(palette), (
            f"Índice de palette inválido em {pos}"
        )
        state_name = names[state_index]
        position = tuple(pos)
        assert position not in seen_positions, f"Posição NBT duplicada: {position}"
        seen_positions.add(position)
        block_by_pos[position] = state_name
        counts[state_name] = counts.get(state_name, 0) + 1
        tile = entry.get("nbt", {})
        if state_name == "minecraft:structure_block" and tile.get("mode") == "DATA" and tile.get("metadata") == "spawn_point":
            markers.append(tuple(pos))

    assert len(seen_positions) == len(blocks), "A estrutura contém posições duplicadas"
    assert len(seen_positions) == size[0] * size[1] * size[2], "A estrutura não contém todos os blocos do volume 11x11x11"
    assert len(markers) == 1, f"Esperado exatamente 1 marcador spawn_point; encontrados: {len(markers)}"
    sx, sy, sz = markers[0]
    origin = (-(size[0] // 2), 0, -(size[2] // 2))
    spawn_offset = (sx + origin[0], sy, sz + origin[2])
    assert spawn_offset == (0, 2, 0), f"Offset de spawn inesperado: {spawn_offset}"

    center_x, center_z = size[0] // 2, size[2] // 2
    feet_y = sy + 2
    head_y = sy + 3
    assert block_by_pos.get((center_x, feet_y, center_z)) == "minecraft:air", "Espaço dos pés bloqueado"
    assert block_by_pos.get((center_x, head_y, center_z)) == "minecraft:air", "Espaço da cabeça bloqueado"
    assert block_by_pos.get((center_x, 1, center_z)) == "minecraft:stone", "Piso central de pedra ausente"
    return {
        "size": size,
        "blocks": len(blocks),
        "stone": counts.get("minecraft:stone", 0),
        "air": counts.get("minecraft:air", 0),
        "spawn_marker": markers[0],
        "spawn_offset": spawn_offset,
    }


data = json.loads(MANIFEST.read_text(encoding="utf-8"))
assert data.get("manifestType") == "minecraftModpack"
assert data.get("manifestVersion") == 1
assert data.get("minecraft", {}).get("version") == "1.12.2"
loaders = data.get("minecraft", {}).get("modLoaders", [])
assert any(x.get("id") == "forge-14.23.5.2860" and x.get("primary") for x in loaders)
forge_id = next(x["id"] for x in loaders if x.get("primary"))
forge_parts = tuple(int(part) for part in forge_id.removeprefix("forge-").split("."))
assert forge_parts >= (14, 23, 5, 2856), "Forge abaixo do mínimo suportado pelo VIC Remastered"
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
assert by_project.get(1709173) == 8980529, "Void Island Control Remastered 1.5.5 ausente"
assert 257655 not in by_project, "Versão original do Void Island Control ainda está no manifesto"
assert by_project.get(258911) == 2866063, "World Primer 0.6.0-dev.20200122.211517 ausente; não usar 0.5.0"

overrides = ROOT / "overrides"
assert overrides.is_dir(), "Pasta overrides ausente"
vic_path = overrides / "config" / "voidislandcontrol.cfg"
stone_path = overrides / "config" / "stoneblockutilities.json"
structure_path = overrides / "config" / "voidislandcontrolstructures" / "island.nbt"
vic_cfg = vic_path.read_text(encoding="utf-8")
stone_cfg = json.loads(stone_path.read_text(encoding="utf-8"))
validate_world_config(vic_cfg, stone_cfg, set(projects))
server_properties = (ROOT / "overrides" / "server.properties").read_text(encoding="utf-8")
assert re.search(r"^level-type=voidworld\s*$", server_properties, re.M), (
    "server.properties precisa usar level-type=voidworld para servidores dedicados"
)
structure_info = validate_structure(structure_path, int(config_value(vic_cfg, "islandYLevel", "I")))

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
                               n.replace("\\", "/").startswith(
                                   ("overrides/config/ftbquests/", "config/ftbquests/"))]
                    for name in matches:
                        normalized = name.replace("\\", "/")
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
                        warnings.append(f"Config FTB Quests recuperada de {archive.name}; validar missões no jogo.")
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
        "World type: Void? World (pré-seleção do single-player deve ser conferida)",
        "Superflat: versão 3, 256 camadas; pedra + lava",
        f"Custom island: {structure_info['size']} / {structure_info['blocks']} blocos",
        f"NBT: DataVersion 1343; {structure_info['stone']} pedra; {structure_info['air']} ar",
        f"Spawn marker: {structure_info['spawn_marker']} -> offset {structure_info['spawn_offset']}",
        "Starting inventory: 36 slots válidos, vazios (minecraft:stone x0)",
        "Void Island Control Remastered: 1.5.5 (GUI fallback / crash fix)",
        "Inventory reset: disabled (preserva itens em recuperação)",
        "StoneBlock Utilities config: schema 2.2.0 validado",
        "World Primer: 0.6.0-dev.20200122.211517 (Forge 1.12.2)",
        "Nether/End: providers vanilla preservados (overrides void desativados)",
        "Server level-type: voidworld",
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
