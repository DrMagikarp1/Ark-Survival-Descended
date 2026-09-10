#!/usr/bin/env python3
"""
ARK: Survival Ascended (ASA) - ASE Purist Game.ini Injector
===========================================================
Strips post-launch ASA creatures, paid DLCs, and unofficial expansions
back to classic ARK: Survival Evolved (ASE) standards using native
Unreal Engine NPCReplacements in Game.ini.

Legacy ASE creatures (Desmodus, Sinomacrops, Wyverns, etc.) remain
completely untouched and are allowed to spawn anywhere (including modded maps).
"""

import sys
import os
import shutil
import datetime
import argparse
from pathlib import Path

# ==============================================================================
# CREATURE REGISTRY (Targeted Blocklist for ASA-era additions)
# ==============================================================================
CREATURE_DATABASE = {
    "DEINOTHERIUM": {
        "description": "Deinotherium (Garuga / Standalone Mod - User's Nemesis!)",
        "default_block": True,
        "classes": [
            ("DeinotheriumASA_Character_BP_C", "Deinotherium (ASA Official/Mod)"),
            ("Deinotherium_Character_BP_C", "Deinotherium (ASE/Legacy Mod Port)")
        ]
    },
    "ASA_STORY_VOTES": {
        "description": "ASA Official Community Votes & Base Game Newcomers",
        "default_block": True,
        "classes": [
            ("Fasola_Character_BP_C", "Fasolasuchus (Scorched Earth)"),
            ("Gigantoraptor_Character_BP_C", "Gigantoraptor (The Island / Center)"),
            ("Shastasaurus_Character_BP_C", "Shastasaurus (The Center)"),
            ("YiLing_Character_BP_C", "Yi Ling (Aberration)"),
            ("Dreadnoughtus_Character_BP_C", "Dreadnoughtus (Extinction)"),
            ("Palaeoctopus_Character_BP_C", "Palaeoctopus (Aquatic Expansion)")
        ]
    },
    "BOBS_TALL_TALES": {
        "description": "Bob's Tall Tales Adventure Pass Creatures",
        "default_block": True,
        "classes": [
            ("Oasisaur_Character_BP_C", "Oasisaur (Frontier Showdown)"),
            ("Cosmo_Character_BP_C", "Cosmo (Steampunk Ascent)"),
            ("Sir5rM8_Character_BP_C", "Sir-5rM-8 Automaton (Steampunk Ascent)"),
            ("Armadoggo_Character_BP_C", "Armadoggo (Wasteland War)")
        ]
    },
    "FANTASTIC_TAMES": {
        "description": "Fantastic Tames Paid Micro-DLC Creatures",
        "default_block": True,
        "classes": [
            ("SpiritBear_Character_BP_C", "Elderclaw (Spirit Bear)"),
            ("Pyromane_Character_BP_C", "Pyromane (Fire Lion)"),
            ("Dreadmare_Character_BP_C", "Dreadmare (Dark Pegasus)"),
            ("Cerberax_Character_BP_C", "Cerberax (Three-headed Hound)"),
            ("Burrowbuck_Character_BP_C", "Burrowbuck"),
            ("Enigmasaur_Character_BP_C", "Enigmasaur")
        ]
    },
    "LOST_COLONY": {
        "description": "Lost Colony Expansion DLC Creatures & Thralls",
        "default_block": True,
        "classes": [
            ("SnowDragon_Character_BP_C", "Aureliax (Snow Dragon)"),
            ("Cryolophosaurus_Character_BP_C", "Cryolophosaurus"),
            ("BossBat_Character_BP_C", "Gigadesmodus"),
            ("LostCharge_LanternPet_Char_BP_C", "Gloon (Lantern Pet)"),
            ("DevilFox_Character_BP_C", "Malwyn"),
            ("SnowMonster_Character_BP_C", "Ossidon"),
            ("AngelFox_Character_BP_C", "Solwyn"),
            ("YoungIceFox_DinoCompanion_Character_BP_C", "Veilwyn (Ice Fox Companion)"),
            ("YoungIceFox_Character_BP_C", "Veilwyn (Base Ice Fox)"),
            ("ShoulderDragon_Character_BP_Spring_C", "Spring Drakeling (Shoulder Dragon)"),
            ("ShoulderDragon_Character_BP_Summer_C", "Summer Drakeling (Shoulder Dragon)"),
            ("ShoulderDragon_Character_BP_Autumn_C", "Autumn Drakeling (Shoulder Dragon)"),
            ("ShoulderDragon_Character_BP_Winter_C", "Winter Drakeling (Shoulder Dragon)"),
            ("ShoulderDragon_Character_BP_C", "Drakeling (Base Shoulder Dragon)"),
            ("Thrall_Character_BP_Fighter_C", "Lost Colony Thrall (Fighter)"),
            ("Thrall_Character_BP_Soldier_C", "Lost Colony Thrall (Soldier)"),
            ("Thrall_Character_BP_Cultist_C", "Lost Colony Thrall (Cultist)")
        ]
    },
    "DRAGONTOPIA": {
        "description": "Dragontopia Expansion DLC Dragons & Beasts",
        "default_block": True,
        "classes": [
            ("Umbra_Character_BP_C", "Eclipsar Umbra (Shadow Dragon)"),
            ("Eclipsar_Character_BP_C", "Eclipsar (Alt Class Reference)"),
            ("Lumina_Character_BP_C", "Lumina (Light Dragon)"),
            ("Gargantar_Character_BP_C", "Gargantar (Belly Beast)")
        ]
    },
    "TIDES_OF_FORTUNE": {
        "description": "Tides of Fortune Naval Expansion Creatures",
        "default_block": True,
        "classes": [
            ("Tidepup_Character_BP_C", "Tidepup (Salamander Companion)"),
            ("Parrot_Character_BP_C", "Parrot (Treasure Seeker)")
        ]
    },
    "ASTRAEOS": {
        "description": "Astraeos Expansion Additions",
        "default_block": True,
        "classes": [
            ("Boaratos_Character_BP_C", "Boaratos")
        ]
    },
    "GARUGA_ADDITIONS": {
        "description": "Garuga123's ARK Additions (Official ASA Base Game Integrations)",
        "default_block": True,
        "classes": [
            ("Ceratosaurus_Character_BP_C", "Ceratosaurus"),
            ("Deinosuchus_Character_BP_C", "Deinosuchus"),
            ("Acrocanthosaurus_Character_BP_C", "Acrocanthosaurus"),
            ("Concavenator_Character_BP_C", "Concavenator"),
            ("Archelon_Character_BP_C", "Archelon"),
            ("Brachiosaurus_Character_BP_C", "Brachiosaurus"),
            ("Xiphactinus_Character_BP_C", "Xiphactinus"),
            ("Helicoprion_Character_BP_C", "Helicoprion")
        ]
    }
}

SECTION_HEADER = "[/script/shootergame.shootergamemode]"
BLOCK_MARKER_START = "; >>> ASE_PURIST_INJECTOR_START <<<"
BLOCK_MARKER_END   = "; >>> ASE_PURIST_INJECTOR_END <<<"

# Common default install paths for ASA Game.ini
POSSIBLE_PATHS = [
    # Windows Singleplayer / Client
    Path("C:/Program Files (x86)/Steam/steamapps/common/ARK Survival Ascended/ShooterGame/Saved/Config/Windows/Game.ini"),
    # Windows Dedicated Server
    Path("C:/Program Files (x86)/Steam/steamapps/common/ARK Survival Ascended Dedicated Server/ShooterGame/Saved/Config/WindowsServer/Game.ini"),
    # Linux Proton / Steam Deck Client
    Path.home() / ".local/share/Steam/steamapps/compatdata/2399830/pfx/drive_c/Program Files (x86)/Steam/steamapps/common/ARK Survival Ascended/ShooterGame/Saved/Config/Windows/Game.ini",
    # Linux Native / Wine Dedicated Server
    Path.home() / ".local/share/Steam/steamapps/common/ARK Survival Ascended Dedicated Server/ShooterGame/Saved/Config/WindowsServer/Game.ini",
    # Local relative directory (testing)
    Path("./Game.ini")
]


def find_game_ini():
    """Attempt to locate Game.ini automatically across standard OS paths."""
    for p in POSSIBLE_PATHS:
        if p.is_file():
            return p
    return None


def generate_replacement_block(allowed_creatures=None):
    """
    Generate the formatted NPCReplacements text block.
    allowed_creatures: set/list of class names that the user explicitly wants to allow (whitelist).
    """
    if allowed_creatures is None:
        allowed_creatures = set()

    lines = [
        BLOCK_MARKER_START,
        "; Generated by ASE Purist Injector on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "; Strips ASA-exclusive, paid DLC, and unofficial expansion creatures.",
        "; Legacy ASE creatures (Desmodus, Wyverns, Sinomacrops, etc.) spawn normally!"
    ]

    total_blocked = 0
    for category_key, category_data in CREATURE_DATABASE.items():
        cat_lines = []
        for class_name, display_name in category_data["classes"]:
            if class_name in allowed_creatures:
                cat_lines.append(f"; [ALLOWED BY USER] {display_name} ({class_name})")
            else:
                cat_lines.append(f'NPCReplacements=(FromClassName="{class_name}",ToClassName="")')
                total_blocked += 1

        if cat_lines:
            lines.append(f"\n; --- {category_data['description']} ---")
            lines.extend(cat_lines)

    lines.append(f"\n{BLOCK_MARKER_END}\n")
    return "\n".join(lines), total_blocked


def inject_into_game_ini(file_path: Path, replacement_block: str):
    """Safely inject the replacement block into Game.ini."""
    # 1. Create a safe backup
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = file_path.with_suffix(f".ini.bak_{timestamp}")
    shutil.copy2(file_path, backup_path)
    print(f"[✓] Backup created at: {backup_path}")

    # 2. Read existing content
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # 3. Strip any previous injection block if present
    if BLOCK_MARKER_START in content and BLOCK_MARKER_END in content:
        print("[i] Found previous ASE Purist injection block. Replacing it...")
        start_idx = content.find(BLOCK_MARKER_START)
        end_idx = content.find(BLOCK_MARKER_END) + len(BLOCK_MARKER_END)
        content = content[:start_idx].rstrip() + "\n\n" + content[end_idx:].lstrip()

    # 4. Inject under [/script/shootergame.shootergamemode]
    header_lower = SECTION_HEADER.lower()
    content_lower = content.lower()

    if header_lower in content_lower:
        idx = content_lower.find(header_lower)
        header_end = content.find("\n", idx)
        if header_end == -1:
            header_end = len(content)
        new_content = content[:header_end] + "\n" + replacement_block + content[header_end:]
    else:
        print(f"[i] Section header {SECTION_HEADER} not found. Appending to end of file...")
        new_content = content.rstrip() + "\n\n" + SECTION_HEADER + "\n" + replacement_block

    # 5. Write back to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"[✓] Successfully injected into: {file_path}")


def remove_from_game_ini(file_path: Path):
    """Remove the injected block to restore original game spawns."""
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    if BLOCK_MARKER_START in content and BLOCK_MARKER_END in content:
        start_idx = content.find(BLOCK_MARKER_START)
        end_idx = content.find(BLOCK_MARKER_END) + len(BLOCK_MARKER_END)
        new_content = content[:start_idx].rstrip() + "\n" + content[end_idx:].lstrip()

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"[✓] Successfully removed ASE Purist blocks from: {file_path}")
    else:
        print("[!] No ASE Purist block found in this file.")


def main():
    parser = argparse.ArgumentParser(
        description="ARK: Survival Ascended - ASE Purist Game.ini Injector"
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="Path to Game.ini (optional; auto-detects if omitted)"
    )
    parser.add_argument(
        "--allow",
        nargs="*",
        default=[],
        help="Class names of creatures you want to allow (e.g., --allow Cosmo_Character_BP_C)"
    )
    parser.add_argument(
        "--remove",
        action="store_true",
        help="Remove previously injected ASE Purist lines from Game.ini"
    )

    args = parser.parse_args()

    # Determine file path
    if args.file:
        target_file = Path(args.file)
    else:
        print("[...] Searching for Game.ini in standard locations...")
        target_file = find_game_ini()

    if not target_file or not target_file.is_file():
        print("[!] Could not automatically locate Game.ini.")
        user_input = input("Please enter the full path to your Game.ini: ").strip().strip('"').strip("'")
        target_file = Path(user_input)
        if not target_file.is_file():
            print(f"[ERROR] File not found: {target_file}")
            sys.exit(1)

    print(f"[✓] Selected target: {target_file}")

    if args.remove:
        remove_from_game_ini(target_file)
        print("\nDon't forget to run 'admincheat DestroyWildDinos' in-game to repopulate!")
        return

    allowed = set(args.allow)
    block_text, count = generate_replacement_block(allowed_creatures=allowed)
    print(f"[i] Prepared {count} creature blocks across {len(CREATURE_DATABASE)} categories.")

    inject_into_game_ini(target_file, block_text)

    print("\n" + "=" * 60)
    print("ALL DONE! 🦖")
    print(f"Blocked {count} non-ASE creature classes.")
    print("Legacy creatures (Desmodus, Sinomacrops, Wyverns, etc.) will spawn normally!")
    print("\nNEXT STEP:")
    print("1. Start your game or server.")
    print("2. Open the in-game console (Tab or ~) and run:")
    print("   admincheat DestroyWildDinos")
    print("=" * 60)


if __name__ == "__main__":
    main()
