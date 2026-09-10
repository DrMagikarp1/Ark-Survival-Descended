# ARK: Survival Ascended - Ark Survival Descended

> A lightweight, highly compatible mod for **ARK: Survival Ascended (ASA)** that restores creature spawns to classic **ARK: Survival Evolved (ASE)** standards.

---

## 🌟 Overview

The **Ark Survival Descended** mod eliminates modern power-creep and paid DLC creatures introduced during the lifespan of *ARK: Survival Ascended*, returning the wild creature ecosystem to what existed in *ARK: Survival Evolved*.

### Key Design Principles:
1. **Filter by Origin Date, NOT by Map:**
   * Any creature created **for or after ASA launched** is prevented from spawning.
   * Any creature created **during ASE** (such as the *Desmodus* from Fjordur, or *Sinomacrops* from Lost Island) is **100% allowed to spawn**, even on modded maps like *Scorched Earth Reborn*.
2. **Zero Container Invasiveness:**
   * Does **NOT** overwrite or remap map spawn containers (`NPCSpawnEntriesContainer`).
   * 100% compatible with custom modded maps and other creature mods.
3. **Admin & Player Configurable via `.ini`:**
   * Don't want to block *Cosmo* because he's cute? Set `AllowCosmo=True` in `GameUserSettings.ini`!
   * Want to toggle *Garuga123's ARK Additions* (Ceratosaurus, Deinosuchus, etc.)? Simple one-line flags give server owners total authority.

---

## 📁 Repository Files

* **[creature_reference.md](file:///home/benc/antigravityprojects/arksurvivaldevolved/Ark-Survival-Descended/creature_reference.md):** The comprehensive database of Blueprint class names for all ASA-exclusive, Garuga, and ASE-legacy creatures.
* **[GameUserSettings_template.ini](file:///home/benc/antigravityprojects/arksurvivaldevolved/Ark-Survival-Descended/GameUserSettings_template.ini):** Complete, commented configuration file for server admins and singleplayer games.
* **[blueprint_assembly_guide.md](file:///home/benc/antigravityprojects/arksurvivaldevolved/Ark-Survival-Descended/blueprint_assembly_guide.md):** Step-by-step visual scripting and DevKit wiring guide to assemble the mod in Unreal Engine 5.

---

## 🦖 Default Roster Rules

### 🚫 Blocked by Default (ASA Exclusives)
* **Bob's Tall Tales:** Oasisaur, Cosmo, Sir-5rM-8, Armadoggo
* **Fantastic Tames (Paid DLC):** Pyromane, Dreadmare
* **ASA Community Votes:** Fasolasuchus, Gigantoraptor, Shastasaurus, Yi Ling, Dreadnoughtus
* **Garuga Official Additions:** Ceratosaurus, Deinosuchus, Archelon, Brachiosaurus, Xiphactinus, Helicoprion *(Configurable!)*

### ✅ Allowed Everywhere (ASE Legacy)
* **All The Island / Scorched / Aberration / Extinction / Gen1 / Gen2 Creatures**
* **Fjordur Additions:** Desmodus, Andrewsarchus, Fjordhawk, Fenrir
* **Lost Island Additions:** Dinopithecus, Sinomacrops, Amargasaurus
* **Crystal Isles & Valguero:** Tropeognathus, Deinonychus
* **Final ASE Creature:** Rhyniognatha (Released June 2023 in ASE)

---

## ⚙️ Configuration Quick Start

Add the `[ArkSurvivalDescended]` header to your `GameUserSettings.ini`:

```ini
[ArkSurvivalDescended]
; Allow Cosmo to spawn:
AllowCosmo=True

; Allow Garuga's Ceratosaurus:
AllowCeratosaurus=True
```

After modifying settings, run the following in the admin console to apply changes immediately:
```text
admincheat DestroyWildDinos
```
