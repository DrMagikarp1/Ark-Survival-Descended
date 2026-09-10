# ARK: Survival Ascended - Ark Survival Descended

> A lightweight, zero-dependency Python tool for **ARK: Survival Ascended (ASA)** that restores creature spawns to classic **ARK: Survival Evolved (ASE)** standards by injecting native Unreal Engine `NPCReplacements` into `Game.ini`.

---

## 🌟 Overview

**Ark Survival Descended** eliminates modern power-creep and paid DLC creatures introduced during the lifespan of *ARK: Survival Ascended*, returning the wild creature ecosystem to what existed in classic *ARK: Survival Evolved*.

### Why a Python Script Instead of an In-Engine Mod?
The original scope of this project was conceived as an in-engine DevKit mod (`ArkSurvivalDescended`). However, during development, we found that using a standalone **Python script** to manage native Unreal Engine `Game.ini` entries is vastly superior:
1. **No Mod Installation Required:** Works immediately on vanilla clients and dedicated servers without requiring players to download or subscribe to any CurseForge mod.
2. **Zero Performance Overhead:** Uses Unreal Engine's native `NPCReplacements` in `[/script/shootergame.shootergamemode]`. Spawns are blocked directly at the engine level with zero tick lag or background actors.
3. **Safe for Save Games:** Leaves zero mod dependencies or orphaned actors in your `.ark` save files. Spawns can be restored at any time with a clean one-click rollback.
*(For DevKit developers who still wish to explore the in-engine actor method, the original DevKit design notes are preserved in `blueprint_assembly_guide.md` and `GameUserSettings_template.ini`.)*

### Key Design Principles:
1. **Filter by Origin Date, NOT by Map:**
   * Any creature created **for or after ASA launched** (October 2023 onwards) is prevented from spawning.
   * Any creature created **during ASE** (such as the *Desmodus* from Fjordur, or *Sinomacrops* from Lost Island) is **100% allowed to spawn**, even on modded maps like *Scorched Earth Reborn*.
2. **Zero Container Invasiveness:**
   * Does **NOT** overwrite or remap map spawn containers (`NPCSpawnEntriesContainer`).
   * 100% compatible with custom modded maps and other creature mods.
3. **Total User Control:**
   * Don't want to block *Cosmo* because he's cute? Easily unblock individual creatures or whole categories via the interactive CLI!
   * Easily toggle *Garuga123's ARK Additions*, *Bob's Tall Tales*, *Fantastic Tames*, and community vote creatures.

---

## 📁 Repository Files

* **`ark_survival_descended.py` / `ase_purist_injector.py`:** The primary Python tool featuring an interactive terminal UI and headless CLI flags.
* **[creature_reference.md](file:///home/benc/antigravityprojects/arksurvivaldevolved/Ark-Survival-Descended/creature_reference.md):** The comprehensive database of Blueprint class names verified against the official ASA DevKit.
* **[GameUserSettings_template.ini](file:///home/benc/antigravityprojects/arksurvivaldevolved/Ark-Survival-Descended/GameUserSettings_template.ini):** Companion configuration template for in-engine setups.
* **[blueprint_assembly_guide.md](file:///home/benc/antigravityprojects/arksurvivaldevolved/Ark-Survival-Descended/blueprint_assembly_guide.md):** The original DevKit visual scripting guide.

---

## 🦖 Default Roster Rules

### 🚫 Blocked by Default (ASA Exclusives)
* **Bob's Tall Tales:** Oasisaur, Bison, Cosmo (`JumpingSpider`), Sir-5rM-8 (`HelperBot`), Armadoggo (`Doggo`), Zeppelin
* **Fantastic Tames (Paid DLC):** Pyromane (`FireLion`), Dreadmare (`DarkPegasus`), Burrowbuck (`Jackalope`), Elderclaw (`SpiritBear`)
* **ASA Community Votes & Story Newcomers:** Fasolasuchus, Gigantoraptor, Shastasaurus, Yi Ling, Dreadnoughtus, Boaratos, Grand Tortugar, Maelizard
* **Garuga Official Additions:** Ceratosaurus, Deinosuchus, Archelon, Brachiosaurus, Xiphactinus, Helicoprion, Acrocanthosaurus, Concavenator *(Configurable!)*
* **Expansion DLCs:** Lost Colony (Aureliax, Cryolophosaurus, Ossidon, Solwyn, Veilwyn, Drakelings, Thralls), Dragontopia (Draco, Eclipsar, Lumina), Tides of Fortune (Axolotl / Tidepups, Parrot, Palaeoctopus)

### ✅ Allowed Everywhere (ASE Legacy)
* **All The Island / Scorched Earth / Aberration / Extinction / Gen1 / Gen2 Creatures**
* **Fjordur Additions:** Desmodus, Andrewsarchus, Fjordhawk, Fenrir
* **Lost Island Additions:** Dinopithecus, Sinomacrops, Amargasaurus
* **Crystal Isles & Valguero:** Tropeognathus, Deinonychus
* **Final ASE Creature:** Rhyniognatha (Released June 2023 in ASE)

---

## ⚙️ Configuration & Usage

The script features an **Interactive Terminal UI** with zero external dependencies (pure Python 3 standard library):

```bash
python3 ark_survival_descended.py
```
*(or `python3 ase_purist_injector.py`)*

### Interactive Menu Features:
1. **[1] Block ALL:** One-click pure ASE setup (blocks all modern creatures and variants).
2. **[2] Select Which to Block:** 
   * View all 8 categories (Deinotherium, Lost Colony, Dragontopia, Tides of Fortune, Fantastic Tames, Bob's Tall Tales, Community Votes, Garuga Additions).
   * Toggle whole categories with `t <#>` (e.g. `t 6` to toggle Bob's Tall Tales).
   * Drill into any category to toggle individual dinos (e.g. unblock *Cosmo* while keeping everything else blocked).
   * Press `s` to save and inject!
3. **[3] Remove All Blocks:** Instant clean rollback to restore official vanilla spawns.
4. **[4] Change Game.ini Location:** Drag-and-drop or enter a custom path if not in the default directory.

---

### In-Game Step:
After running the script, boot up ARK and run this in the console (`Tab` or `~`):
```text
admincheat DestroyWildDinos
```
