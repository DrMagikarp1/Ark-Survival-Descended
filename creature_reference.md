# ARK: Survival Ascended (ASA) - Ark Survival Descended Creature Reference Sheet

This document catalogs the exact character Blueprint classes for creatures introduced during **ARK: Survival Ascended (ASA)** and **Garuga's ARK Additions**, as well as legacy **ARK: Survival Evolved (ASE)** creatures that must remain unblocked.

---

## 1. ASA-Exclusive Creatures (Blocked by Default)

These creatures were newly created and introduced for *ARK: Survival Ascended* (launching October 2023 onwards). Under Ark Survival Descended, these will be intercepted and prevented from spawning.

| Common Name | Blueprint Class Name | Content Source / DLC | Default Action |
| :--- | :--- | :--- | :--- |
| **Fasolasuchus** | `Fasola_Character_BP_C` | Scorched Earth (Community Vote) | **BLOCK** |
| **Oasisaur** | `Oasisaur_Character_BP_C` | Bob's Tall Tales (Frontier Showdown) | **BLOCK** |
| **Pyromane** | `Pyromane_Character_BP_C` | Fantastic Tames (Paid DLC) | **BLOCK** |
| **Gigantoraptor** | `Gigantoraptor_Character_BP_C` | The Island / Center (Community Vote) | **BLOCK** |
| **Shastasaurus** | `Shastasaurus_Character_BP_C` | The Center (Community Vote) | **BLOCK** |
| **Yi Ling** | `YiLing_Character_BP_C` | Aberration (Community Vote) | **BLOCK** |
| **Cosmo** | `Cosmo_Character_BP_C` | Bob's Tall Tales (Steampunk Ascent) | **BLOCK** |
| **Sir-5rM-8** | `Sir5rM8_Character_BP_C` | Bob's Tall Tales (Steampunk Ascent) | **BLOCK** |
| **Dreadmare** | `Dreadmare_Character_BP_C` | Fantastic Tames (Paid DLC) | **BLOCK** |
| **Dreadnoughtus** | `Dreadnoughtus_Character_BP_C` | Extinction (Community Vote) | **BLOCK** |
| **Armadoggo** | `Armadoggo_Character_BP_C` | Bob's Tall Tales (Wasteland War) | **BLOCK** |

---

## 2. Garuga123's ARK Additions (Officialized in ASA)

These creatures originated as popular third-party mods in ASE and were integrated by Studio Wildcard into official base-game ASA releases. They are blocked by default in Ark Survival Descended, but can be individually or globally toggled via `.ini`.

| Common Name | Blueprint Class Name | Original Source | Default Action |
| :--- | :--- | :--- | :--- |
| **Ceratosaurus** | `Ceratosaurus_Character_BP_C` | ARK Additions: The Collection | **BLOCK (Configurable)** |
| **Deinosuchus** | `Deinosuchus_Character_BP_C` | ARK Additions: The Collection | **BLOCK (Configurable)** |
| **Archelon** | `Archelon_Character_BP_C` | ARK Additions: The Collection | **BLOCK (Configurable)** |
| **Brachiosaurus** | `Brachiosaurus_Character_BP_C` | ARK Additions: The Collection | **BLOCK (Configurable)** |
| **Xiphactinus** | `Xiphactinus_Character_BP_C` | ARK Additions: The Collection | **BLOCK (Configurable)** |
| **Helicoprion** | `Helicoprion_Character_BP_C` | ARK Additions: The Collection | **BLOCK (Configurable)** |

---

## 3. Legacy ASE Creatures (ALWAYS ALLOWED)

These creatures were released during the lifespan of *ARK: Survival Evolved*. Even if they appear on modded maps (e.g., *Scorched Earth Reborn*) or out of their native ASE order, **they MUST NEVER be blocked**.

| Creature | Debut Map in ASE | Release Date | Rule |
| :--- | :--- | :--- | :--- |
| **Desmodus** | Fjordur (ASE) | June 2022 | **ALLOW EVERYWHERE** |
| **Andrewsarchus** | Fjordur (ASE) | June 2022 | **ALLOW EVERYWHERE** |
| **Fjordhawk** | Fjordur (ASE) | June 2022 | **ALLOW EVERYWHERE** |
| **Fenrir** | Fjordur (ASE) | June 2022 | **ALLOW EVERYWHERE** |
| **Sinomacrops** | Lost Island (ASE) | Dec 2021 | **ALLOW EVERYWHERE** |
| **Dinopithecus** | Lost Island (ASE) | Dec 2021 | **ALLOW EVERYWHERE** |
| **Amargasaurus** | Lost Island (ASE) | Dec 2021 | **ALLOW EVERYWHERE** |
| **Tropeognathus** | Crystal Isles (ASE) | June 2020 | **ALLOW EVERYWHERE** |
| **Deinonychus** | Valguero (ASE) | June 2019 | **ALLOW EVERYWHERE** |
| **Managarmr, Velonasaur, Snow Owl, Gacha** | Extinction (ASE) | Nov 2018 | **ALLOW EVERYWHERE** |
| **Rock Drake, Reaper, Karkinos, Ravager** | Aberration (ASE) | Dec 2017 | **ALLOW EVERYWHERE** |
| **Wyverns, Phoenix, Mantis, Jerboa** | Scorched Earth (ASE) | Sept 2016 | **ALLOW EVERYWHERE** |
| **All The Island / The Center Vanilla Dinos** | Base Game | 2015-2016 | **ALLOW EVERYWHERE** |

---

## 4. Special Case: Rhyniognatha

* **Blueprint Class:** `Rhynio_Character_BP_C`
* **Release:** June 2023 on *ARK: Survival Evolved* (The Island / Lost Island) as the final community creature vote in ASE prior to ASA.
* **Mod Rule:** Treated as an official ASE creature and allowed to spawn by default. An optional `.ini` toggle `BlockRhyniognatha=False` can be provided for players who consider it too modern.
