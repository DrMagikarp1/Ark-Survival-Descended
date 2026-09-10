#!/usr/bin/env python3
"""
ARK: Survival Ascended (ASA) - Ark Survival Descended Game.ini Manager
=====================================================================
Strips post-launch ASA creatures, paid DLCs, and unofficial expansions
back to classic ARK: Survival Evolved (ASE) standards using native
Unreal Engine NPCReplacements in Game.ini.
"""
import sys
from pathlib import Path

# Import all core database, interactive menus, and injector routines
from ase_purist_injector import (
    CREATURE_DATABASE,
    SECTION_HEADER,
    BLOCK_MARKER_START,
    BLOCK_MARKER_END,
    POSSIBLE_PATHS,
    find_game_ini,
    get_all_classes,
    generate_replacement_block,
    inject_into_game_ini,
    remove_from_game_ini,
    interactive_main_menu,
    main,
)

if __name__ == "__main__":
    main()
