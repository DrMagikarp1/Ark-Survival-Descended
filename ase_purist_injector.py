#!/usr/bin/env python3
"""
ARK: Survival Ascended (ASA) - ASE Purist Game.ini Manager
===========================================================
Strips post-launch ASA creatures, paid DLCs, and unofficial expansions
back to classic ARK: Survival Evolved (ASE) standards using native
Unreal Engine NPCReplacements in Game.ini.

Features an interactive terminal menu:
  1) Block All (Pure ASE - Full Purge)
  2) Select Which to Block (Category & Dino Fine-Tuning)
  3) Remove All Blocks (Restore Vanilla Spawns)
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
        "title": "The Nemesis (Deinotherium)",
        "description": "Deinotherium (Garuga / Standalone Mod - User's Nemesis!)",
        "classes": [
            ("DeinotheriumASA_Character_BP_C", "Deinotherium (ASA Official/Mod)"),
            ("Deinotherium_Character_BP_C", "Deinotherium (ASE/Legacy Mod Port)")
        ]
    },
    "LOST_COLONY": {
        "title": "Lost Colony Expansion DLC",
        "description": "Lost Colony Expansion DLC Creatures & Thralls",
        "classes": [
            ("SnowDragon_Character_BP_C", "Aureliax (Snow Dragon)"),
            ("Cryolophosaurus_Character_BP_C", "Cryolophosaurus"),
            ("BossBat_Character_BP_C", "Gigadesmodus"),
            ("BossBat_Character_BP_LostKing_C", "Gigadesmodus (Lost King Variant)"),
            ("LostCharge_LanternPet_Char_BP_C", "Gloon (Lantern Pet)"),
            ("DevilFox_Character_BP_C", "Malwyn"),
            ("SnowMonster_Character_BP_C", "Ossidon"),
            ("MegaSnowMonster_Character_BP_C", "Ossidon (Alpha / Mega)"),
            ("AngelFox_Character_BP_C", "Solwyn"),
            ("YoungIceFox_DinoCompanion_Character_BP_C", "Veilwyn (Ice Fox Companion)"),
            ("Ghost_YoungIceFox_DinoCompanion_Character_BP_C", "Veilwyn (Ghost Ice Fox)"),
            ("YoungIceFox_Character_BP_C", "Veilwyn (Base Ice Fox Alias)"),
            ("ShoulderDragon_Character_BP_Spring_C", "Spring Drakeling (Shoulder Dragon)"),
            ("ShoulderDragon_Character_BP_Summer_C", "Summer Drakeling (Shoulder Dragon)"),
            ("ShoulderDragon_Character_BP_Autumn_C", "Autumn Drakeling (Shoulder Dragon)"),
            ("ShoulderDragon_Character_BP_Winter_C", "Winter Drakeling (Shoulder Dragon)"),
            ("ShoulderDragon_Character_BP_C", "Drakeling (Base Shoulder Dragon)"),
            ("Ghost_ShoulderDragon_Character_BP_Spring_C", "Spring Drakeling (Ghost Variant)"),
            ("Ghost_ShoulderDragon_Character_BP_Summer_C", "Summer Drakeling (Ghost Variant)"),
            ("Ghost_ShoulderDragon_Character_BP_Autumn_C", "Autumn Drakeling (Ghost Variant)"),
            ("Ghost_ShoulderDragon_Character_BP_Winter_C", "Winter Drakeling (Ghost Variant)"),
            ("Thrall_Character_BP_Fighter_C", "Lost Colony Thrall (Fighter)"),
            ("Thrall_Character_BP_Soldier_C", "Lost Colony Thrall (Soldier)"),
            ("Thrall_Character_BP_Cultist_C", "Lost Colony Thrall (Cultist)"),
            ("Thrall_Character_BP_Harvester_C", "Lost Colony Thrall (Harvester)"),
            ("Thrall_Character_BP_Tamer_C", "Lost Colony Thrall (Tamer)"),
            ("Neophyte_Character_BP_C", "Lost Colony Neophyte")
        ]
    },
    "DRAGONTOPIA": {
        "title": "Dragontopia Expansion DLC",
        "description": "Dragontopia Expansion DLC Dragons & Beasts",
        "classes": [
            ("Draco_Character_BP_C", "Draco (Base Dragon - Official DevKit Class)"),
            ("Umbra_Character_BP_C", "Eclipsar Umbra (Shadow Dragon)"),
            ("Eclipsar_Character_BP_C", "Eclipsar (Alt Class Reference)"),
            ("Lumina_Character_BP_C", "Lumina (Light Dragon)"),
            ("Gargantar_Character_BP_C", "Gargantar (Belly Beast Alias)")
        ]
    },
    "TIDES_OF_FORTUNE": {
        "title": "Tides of Fortune Expansion DLC",
        "description": "Tides of Fortune Naval Expansion Creatures",
        "classes": [
            ("Axolotl_Character_BP_C", "Tidepup (Axolotl - Official DevKit Class)"),
            ("Axolotl_Large_Character_BP_C", "Tidepup Large (Axolotl Large - DevKit Class)"),
            ("Axolotl_Small_Character_BP_C", "Tidepup Small (Axolotl Small - DevKit Class)"),
            ("Tidepup_Character_BP_C", "Tidepup (Direct Alias)"),
            ("Parrot_Character_BP_C", "Parrot (Treasure Seeker)"),
            ("Palaeoctopus_Character_BP_C", "Palaeoctopus (Aquatic Expansion)"),
            ("MegaPalaeoctopus_Character_BP_C", "Palaeoctopus (Alpha / Mega Variant)")
        ]
    },
    "FANTASTIC_TAMES": {
        "title": "Fantastic Tames (Paid Micro-DLC)",
        "description": "Fantastic Tames Paid Micro-DLC Creatures",
        "classes": [
            ("SpiritBear_Character_BP_C", "Elderclaw (Spirit Bear - Official DevKit Class)"),
            ("Elderclaw_Character_BP_C", "Elderclaw (Direct Alias)"),
            ("FireLion_Character_BP_C", "Pyromane (Fire Lion - Official DevKit Class)"),
            ("FireLion_Character_BP_Thrall_C", "Pyromane Thrall (Lost Colony Variant)"),
            ("Pyromane_Character_BP_C", "Pyromane (Direct Alias)"),
            ("DarkPegasus_Character_BP_C", "Dreadmare (Dark Pegasus - Official DevKit Class)"),
            ("Dreadmare_Character_BP_C", "Dreadmare (Direct Alias)"),
            ("Jackalope_Character_BP_C", "Burrowbuck (Jackalope - Official DevKit Class)"),
            ("Burrowbuck_Character_BP_C", "Burrowbuck (Direct Alias)"),
            ("Cerberax_Character_BP_C", "Cerberax (Three-headed Hound)"),
            ("Enigmasaur_Character_BP_C", "Enigmasaur")
        ]
    },
    "BOBS_TALL_TALES": {
        "title": "Bob's Tall Tales (Adventure Pass)",
        "description": "Bob's Tall Tales Adventure Pass Creatures",
        "classes": [
            ("Oasisaur_Character_BP_C", "Oasisaur (Frontier Showdown)"),
            ("Bison_Character_BP_C", "Bison (Frontier Showdown - Official DevKit Class)"),
            ("JumpingSpider_Character_BP_C", "Cosmo (Jumping Spider - Official DevKit Class)"),
            ("Cosmo_Character_BP_C", "Cosmo (Direct Alias)"),
            ("HelperBot_Character_BP_C", "Sir-5rM-8 (Helper Bot - Official DevKit Class)"),
            ("Sir5rM8_Character_BP_C", "Sir-5rM-8 (Direct Alias)"),
            ("Doggo_Character_BP_C", "Armadoggo (Doggo - Official DevKit Class)"),
            ("Armadoggo_Character_BP_C", "Armadoggo (Direct Alias)"),
            ("Zeppelin_Character_BP_C", "Zeppelin (Steampunk Airship)")
        ]
    },
    "ASA_STORY_VOTES": {
        "title": "ASA Community Votes & Story Newcomers",
        "description": "ASA Official Community Votes & Base Game Newcomers",
        "classes": [
            ("Fasola_Character_BP_C", "Fasolasuchus (Scorched Earth)"),
            ("Fasola_Character_BP_Aberrant_C", "Fasolasuchus Aberrant (Official DevKit Class)"),
            ("Gigantoraptor_Character_BP_C", "Gigantoraptor (The Island / Center)"),
            ("Gigantoraptor_Character_BP_Aberrant_C", "Gigantoraptor Aberrant (Official DevKit Class)"),
            ("Ghost_Gigantoraptor_Character_BP_C", "Gigantoraptor Ghost (Official DevKit Class)"),
            ("Shastasaurus_Character_BP_C", "Shastasaurus (The Center)"),
            ("YiLing_Character_BP_C", "Yi Ling (Aberration)"),
            ("Ghost_YiLing_Character_BP_C", "Yi Ling Ghost (Official DevKit Class)"),
            ("Dreadnoughtus_Character_BP_C", "Dreadnoughtus (Extinction)"),
            ("Boaratos_Character_BP_C", "Boaratos (Astraeos Map)"),
            ("MegaBoaratos_Character_BP_C", "Boaratos Alpha / Mega (Astraeos Map)"),
            ("GrandTortugar_Character_BP_C", "Grand Tortugar (Official DevKit Class)"),
            ("Maelizard_Character_BP_C", "Maelizard (Official DevKit Class)")
        ]
    },
    "GARUGA_ADDITIONS": {
        "title": "Garuga's ARK Additions (Official ASA)",
        "description": "Garuga123's ARK Additions (Official ASA Base Game Integrations)",
        "classes": [
            ("Xiphactinus_Character_BP_ASA_C", "Xiphactinus (Official ASA Class)"),
            ("Xiphactinus_Character_BP_C", "Xiphactinus (Additions Port Class)"),
            ("Ceratosaurus_Character_BP_ASA_C", "Ceratosaurus (Official ASA Class)"),
            ("Ghost_Ceratosaurus_Character_BP_ASA_C", "Ceratosaurus Ghost (Official ASA Class)"),
            ("CeratosaurusAA_Character_BP_C", "Ceratosaurus (Additions Mod Class)"),
            ("Ceratosaurus_Character_BP_C", "Ceratosaurus (Direct Alias)"),
            ("DeinosuchusASA_Character_BP_C", "Deinosuchus (Official ASA Class)"),
            ("Deinosuchus_Character_BP_ASA_C", "Deinosuchus (Official ASA Alt)"),
            ("DeinosuchusAA_Character_BP_C", "Deinosuchus (Additions Mod Class)"),
            ("Deinosuchus_Character_BP_C", "Deinosuchus (Direct Alias)"),
            ("Archelon_Character_BP_ASA_C", "Archelon (Official ASA Class)"),
            ("Archelon_Character_BP_C", "Archelon (Direct Alias)"),
            ("Brachiosaurus_Character_BP_C", "Brachiosaurus (Additions Class)"),
            ("Brachiosaurus_Character_BP_ASA_C", "Brachiosaurus (Official ASA Class)"),
            ("BrachiosaurusAA_Character_BP_C", "Brachiosaurus (Additions Mod Class)"),
            ("Helicoprion_Character_BP_C", "Helicoprion (Additions / Official Class)"),
            ("Helicoprion_Character_BP_ASA_C", "Helicoprion (Official ASA Alt)"),
            ("Acrocanthosaurus_Character_BP_C", "Acrocanthosaurus (Additions / Official Class)"),
            ("Acrocanthosaurus_Character_BP_ASA_C", "Acrocanthosaurus (Official ASA Alt)"),
            ("AcrocanthosaurusAA_Character_BP_C", "Acrocanthosaurus (Additions Mod Class)"),
            ("Concavenator_Character_BP_C", "Concavenator (Additions / Official Class)"),
            ("Concavenator_Character_BP_Aberrant_C", "Concavenator Aberrant (Official DevKit Class)"),
            ("Concavenator_Character_BP_ASA_C", "Concavenator (Official ASA Alt)"),
            ("ConcavenatorAA_Character_BP_C", "Concavenator (Additions Mod Class)")
        ]
    }
}

SECTION_HEADER = "[/script/shootergame.shootergamemode]"
BLOCK_MARKER_START = "; >>> ASE_PURIST_INJECTOR_START <<<"
BLOCK_MARKER_END   = "; >>> ASE_PURIST_INJECTOR_END <<<"

# Common default install paths for ASA Game.ini
POSSIBLE_PATHS = [
    # Local relative directory (drag-and-drop or run in server folder)
    Path("./Game.ini"),
    # Windows Singleplayer / Client
    Path("C:/Program Files (x86)/Steam/steamapps/common/ARK Survival Ascended/ShooterGame/Saved/Config/Windows/Game.ini"),
    # Windows Dedicated Server
    Path("C:/Program Files (x86)/Steam/steamapps/common/ARK Survival Ascended Dedicated Server/ShooterGame/Saved/Config/WindowsServer/Game.ini"),
    # Linux Proton / Steam Deck Client
    Path.home() / ".local/share/Steam/steamapps/compatdata/2399830/pfx/drive_c/Program Files (x86)/Steam/steamapps/common/ARK Survival Ascended/ShooterGame/Saved/Config/Windows/Game.ini",
    # Linux Native / Wine Dedicated Server
    Path.home() / ".local/share/Steam/steamapps/common/ARK Survival Ascended Dedicated Server/ShooterGame/Saved/Config/WindowsServer/Game.ini"
]


def find_game_ini():
    """Attempt to locate Game.ini automatically across standard OS paths."""
    for p in POSSIBLE_PATHS:
        try:
            if p.is_file():
                return p.resolve()
        except Exception:
            continue
    return None


def get_all_classes():
    """Return a set of all creature classes in the database."""
    classes = set()
    for cat in CREATURE_DATABASE.values():
        for cls, _ in cat["classes"]:
            classes.add(cls)
    return classes


def generate_replacement_block(blocked_classes: set):
    """
    Generate the formatted NPCReplacements text block for all blocked_classes.
    """
    lines = [
        BLOCK_MARKER_START,
        "; Generated by ASE Purist Manager on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "; Strips ASA-exclusive, paid DLC, and unofficial expansion creatures.",
        "; Legacy ASE creatures (Desmodus, Wyverns, Sinomacrops, etc.) spawn normally!"
    ]

    total_blocked = 0
    for cat_key, cat_data in CREATURE_DATABASE.items():
        cat_lines = []
        for class_name, display_name in cat_data["classes"]:
            if class_name in blocked_classes:
                cat_lines.append(f'NPCReplacements=(FromClassName="{class_name}",ToClassName="")')
                total_blocked += 1
            else:
                cat_lines.append(f'; [ALLOWED] {display_name} ({class_name})')

        if cat_lines:
            lines.append(f"\n; --- {cat_data['description']} ---")
            lines.extend(cat_lines)

    lines.append(f"\n{BLOCK_MARKER_END}\n")
    return "\n".join(lines), total_blocked


def inject_into_game_ini(file_path: Path, replacement_block: str):
    """Safely inject the replacement block into Game.ini."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = file_path.with_suffix(f".ini.bak_{timestamp}")
    shutil.copy2(file_path, backup_path)
    print(f"\n[✓] Safe backup created at: {backup_path.name}")

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # Strip existing block if present
    if BLOCK_MARKER_START in content and BLOCK_MARKER_END in content:
        start_idx = content.find(BLOCK_MARKER_START)
        end_idx = content.find(BLOCK_MARKER_END) + len(BLOCK_MARKER_END)
        content = content[:start_idx].rstrip() + "\n\n" + content[end_idx:].lstrip()

    header_lower = SECTION_HEADER.lower()
    content_lower = content.lower()

    if header_lower in content_lower:
        idx = content_lower.find(header_lower)
        header_end = content.find("\n", idx)
        if header_end == -1:
            header_end = len(content)
        new_content = content[:header_end] + "\n" + replacement_block + content[header_end:]
    else:
        new_content = content.rstrip() + "\n\n" + SECTION_HEADER + "\n" + replacement_block

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"[✓] Successfully injected spawn replacements into: {file_path}")


def remove_from_game_ini(file_path: Path):
    """Remove the injected block to restore original game spawns."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = file_path.with_suffix(f".ini.bak_{timestamp}")
    shutil.copy2(file_path, backup_path)
    print(f"\n[✓] Safe backup created at: {backup_path.name}")

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
        print("[!] No ASE Purist block was found in this file.")


# ==============================================================================
# INTERACTIVE TERMINAL MENUS
# ==============================================================================

def print_banner(target_file):
    print("=" * 66)
    print("          🦖 ARK: Survival Ascended - ASE Purist Manager 🦕")
    print("=" * 66)
    target_str = str(target_file) if target_file else "Not Selected"
    print(f" Target Game.ini: {target_str}")
    print("=" * 66)


def edit_creature_category_menu(cat_key, cat_data, blocked_classes):
    """Submenu for toggling individual creatures inside a category."""
    while True:
        print("\n" + "-" * 66)
        print(f" Category: {cat_data['title']}")
        print(" Enter creature number to toggle between [BLOCKED] and [ALLOWED]")
        print("-" * 66)

        for idx, (cls, name) in enumerate(cat_data["classes"], 1):
            status = "[BLOCKED]" if cls in blocked_classes else "[ALLOWED]"
            print(f"   [{idx:2d}] {status:9s} {name}")

        print("-" * 66)
        print("   [A] Allow ALL in this category")
        print("   [B] Block ALL in this category")
        print("   [D] Done (Return to Categories)")
        print("-" * 66)

        choice = input("Choice: ").strip().lower()

        if choice == 'd':
            break
        elif choice == 'a':
            for cls, _ in cat_data["classes"]:
                blocked_classes.discard(cls)
            print(" [✓] All creatures in this category set to ALLOWED.")
        elif choice == 'b':
            for cls, _ in cat_data["classes"]:
                blocked_classes.add(cls)
            print(" [✓] All creatures in this category set to BLOCKED.")
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(cat_data["classes"]):
                cls, name = cat_data["classes"][idx]
                if cls in blocked_classes:
                    blocked_classes.remove(cls)
                    print(f" [✓] {name} is now ALLOWED.")
                else:
                    blocked_classes.add(cls)
                    print(f" [✓] {name} is now BLOCKED.")
            else:
                print(" [!] Invalid creature number.")
        else:
            print(" [!] Invalid option.")


def customize_blocks_menu(target_file, blocked_classes):
    """Submenu for browsing and toggling creature categories."""
    cat_keys = list(CREATURE_DATABASE.keys())

    while True:
        total_dinos = len(get_all_classes())
        blocked_count = len(blocked_classes)

        print("\n" + "=" * 66)
        print(f" SELECT WHICH TO BLOCK (Currently Blocking {blocked_count}/{total_dinos} Creatures)")
        print("=" * 66)
        print(" Enter a category number to fine-tune individual creatures:")

        for idx, key in enumerate(cat_keys, 1):
            cat = CREATURE_DATABASE[key]
            cat_classes = [c[0] for c in cat["classes"]]
            cat_blocked = sum(1 for c in cat_classes if c in blocked_classes)
            total_in_cat = len(cat_classes)

            if cat_blocked == total_in_cat:
                status = "[BLOCKED]"
            elif cat_blocked == 0:
                status = "[ALLOWED]"
            else:
                status = f"[{cat_blocked}/{total_in_cat} BLOCKED]"

            print(f"   [{idx}] {cat['title']:<38} -> {status}")

        print("-" * 66)
        print(" Actions:")
        print("   [#]     Enter category number (1-8) to fine-tune creatures")
        print("   [T #]   Toggle entire category (e.g. 't 6' to toggle Bob's Tall Tales)")
        print("   [A]     Allow ALL creatures (Clear blacklist)")
        print("   [B]     Block ALL creatures (Full purge)")
        print("   [S]     SAVE & APPLY to Game.ini now")
        print("   [X]     Cancel / Discard changes and return to Main Menu")
        print("-" * 66)

        raw = input("Choice: ").strip()
        cmd = raw.lower()

        if cmd == 'x':
            print(" [i] Changes discarded.")
            break
        elif cmd == 'a':
            blocked_classes.clear()
            print(" [✓] Cleared all blocks. (All creatures allowed).")
        elif cmd == 'b':
            blocked_classes.update(get_all_classes())
            print(" [✓] Set all creatures to BLOCKED.")
        elif cmd == 's':
            block_text, count = generate_replacement_block(blocked_classes)
            inject_into_game_ini(target_file, block_text)
            print_completion_notice(count)
            break
        elif cmd.startswith('t ') or (len(cmd) > 1 and cmd[0] == 't'):
            parts = cmd.split()
            cat_num = parts[1] if len(parts) > 1 else cmd[1:]
            if cat_num.isdigit():
                idx = int(cat_num) - 1
                if 0 <= idx < len(cat_keys):
                    key = cat_keys[idx]
                    cat = CREATURE_DATABASE[key]
                    cat_classes = [c[0] for c in cat["classes"]]
                    # If all or most are blocked, unblock all. Otherwise, block all.
                    if any(c in blocked_classes for c in cat_classes):
                        for c in cat_classes:
                            blocked_classes.discard(c)
                        print(f" [✓] {cat['title']} set to ALLOWED.")
                    else:
                        for c in cat_classes:
                            blocked_classes.add(c)
                        print(f" [✓] {cat['title']} set to BLOCKED.")
                else:
                    print(" [!] Invalid category number.")
        elif raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(cat_keys):
                key = cat_keys[idx]
                edit_creature_category_menu(key, CREATURE_DATABASE[key], blocked_classes)
            else:
                print(" [!] Invalid category number.")
        else:
            print(" [!] Invalid command. Type number, 't <#>', 's', or 'x'.")


def print_completion_notice(count):
    print("\n" + "=" * 66)
    print(" ✨ ALL DONE! SPATIAL INJECTION COMPLETE! ✨")
    print(f" Injected blocks for {count} non-ASE creature classes.")
    print(" Legacy creatures (Desmodus, Sinomacrops, Wyverns, etc.) will spawn!")
    print("\n NEXT STEP:")
    print(" 1. Start your game or server.")
    print(" 2. Open the in-game console (Tab or ~) and run:")
    print("    admincheat DestroyWildDinos")
    print("=" * 66 + "\n")


def interactive_main_menu():
    target_file = find_game_ini()

    while True:
        print_banner(target_file)
        total_dinos = len(get_all_classes())
        print(f"   [1] Block ALL (Pure ASE - Full Purge of all {total_dinos} creature classes)")
        print("   [2] Select Which to Block (Category & Creature Fine-Tuning)")
        print("   [3] Remove All Blocks (Restore Official Vanilla Spawns)")
        print("   [4] Change Game.ini File Location")
        print("   [5] Exit\n")
        print("=" * 66)

        choice = input("Select an option (1-5): ").strip()

        if choice == '1':
            if not target_file:
                target_file = prompt_for_path()
                if not target_file:
                    continue
            all_classes = get_all_classes()
            block_text, count = generate_replacement_block(all_classes)
            inject_into_game_ini(target_file, block_text)
            print_completion_notice(count)
            input("Press Enter to continue...")

        elif choice == '2':
            if not target_file:
                target_file = prompt_for_path()
                if not target_file:
                    continue
            # Default to all blocked when opening customization
            blocked_classes = set(get_all_classes())
            customize_blocks_menu(target_file, blocked_classes)
            input("Press Enter to continue...")

        elif choice == '3':
            if not target_file:
                target_file = prompt_for_path()
                if not target_file:
                    continue
            remove_from_game_ini(target_file)
            print("\n[i] Vanilla spawns restored.")
            print("Don't forget to run 'admincheat DestroyWildDinos' in-game!")
            input("Press Enter to continue...")

        elif choice == '4':
            target_file = prompt_for_path()

        elif choice == '5':
            print("\nExiting ASE Purist Manager. Happy surviving! 🦖")
            sys.exit(0)

        else:
            print("\n[!] Invalid selection. Please enter a number from 1 to 5.")


def prompt_for_path():
    print("\n--- Enter Game.ini Location ---")
    user_input = input("Drag-and-drop or type the full path to Game.ini: ").strip().strip('"').strip("'")
    if not user_input:
        return None
    p = Path(user_input)
    if p.is_file():
        print(f"[✓] Loaded: {p.resolve()}")
        return p.resolve()
    else:
        print(f"[ERROR] File not found at: {p}")
        return None


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="ARK: Survival Ascended - ASE Purist Game.ini Manager"
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="Path to Game.ini (optional; launches interactive menu if omitted)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Headless mode: Block all modern creatures without prompting"
    )
    parser.add_argument(
        "--allow",
        nargs="*",
        default=[],
        help="Headless mode: Class names of creatures to allow (whitelist)"
    )
    parser.add_argument(
        "--remove",
        action="store_true",
        help="Headless mode: Remove previously injected ASE Purist lines from Game.ini"
    )

    args = parser.parse_args()

    # If any headless flags are used, run in non-interactive batch mode
    if args.all or args.allow or args.remove:
        target = Path(args.file) if args.file else find_game_ini()
        if not target or not target.is_file():
            print("[ERROR] Game.ini not found. Specify path: python ase_purist_injector.py <path>")
            sys.exit(1)

        if args.remove:
            remove_from_game_ini(target)
            return

        all_classes = get_all_classes()
        allowed = set(args.allow)
        blocked = all_classes - allowed

        block_text, count = generate_replacement_block(blocked)
        inject_into_game_ini(target, block_text)
        print_completion_notice(count)
        return

    # Otherwise, launch the full interactive terminal menu!
    try:
        interactive_main_menu()
    except (KeyboardInterrupt, EOFError):
        print("\n\nOperation cancelled. Exiting.")
        sys.exit(0)


if __name__ == "__main__":
    main()
