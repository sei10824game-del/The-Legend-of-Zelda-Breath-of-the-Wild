# Hyrule Creatures (Minecraft 1.20.1 / Forge 47)

BotW + TotK creatures & weapons. TotK variants take priority over BotW.

- Assets are generated: `python3 tools/gen_assets.py` (models spec, textures, lang, weapons, biome spawns). Add a species = add an entry in `SPECIES`/`PAL` + a `Species` enum entry.
- Rank (red/blue/black/silver/gold) scales HP/damage and picks weapons. Stagger: a hit ≥35% max HP or 4 hits within ~1.5s knocks the mob down (80 ticks, takes 1.5x damage).
- Attack styles: SMASH / SLASH (3-hit combo) / THRUST / SPIN / BITE, each with its own keyframed animation (`CreatureModel`).
- Every non-mod mob is hostile to these mobs and vice versa (`FactionEvents`).

## Done
Bokoblin, Moblin, Lizalfos, Keese, Hinox (rock throw), Talus (rock throw), Gibdo, Horriblin, Octorok, Wizzrobe (Blizzrobe, Thunder), Lynel, Chuchu, Guardian Stalker, Stalkoblin, Stalmoblin, Stalizalfos, Yiga Footsoldier, Blademaster, Soldier/Captain Construct, Frox, Stalhinox, Master Kohga, 4 Blight Ganons, Calamity Ganon, Phantom Ganon, Gleeok; Molduga, Molduking, Gloom Hands, Like Like, Marbled Gohma, Colgera, Queen Gibdo, Flux/Seized Construct, Boss Bokoblin; Twilight Princess: Bulblin (+King), Stalhound, Shadow Beast, Redead, Poe, Tektite, Peahat, Bubbles, Dodongo, Helmasaur, Dark Nut, Death Sword, Zant, Ganondorf, Diababa, Fyrus, Armogohma, Argorok, Aeralfos, Dinolfos, Kargarok; Skyward Sword: Stalfos, Stalmaster, Dinolfos, Aeralfos, Armos, Beamos, Skulltula, Deku Baba, Cursed Bokoblin, Ghirahim, Demise, Moldarach, Koloktos, Scaldera, The Imprisoned (3 heads, elemental breath); 57 weapons (melee, bows, shields; mobs block with shields); monster-part drops (horn/fang/guts per species); ranged system (SHOOT: arrows, rocks, fire/ice/spark balls, returning boomerang).
## TODO: Gleeok, Molduga, Frox, Gloom Hands, Phantom Ganon, Calamity Ganon, Demise etc.; hand-polished models; in-client visual check.
Remaining creatures (Lynel, Guardian, Chuchu, Wizzrobe, Octorok, Gleeok, Gibdo, Horriblin, Construct, Phantom Ganon, bosses...), elemental variants, loot tables, hand-polished models.

## Visual check (dev)
`./gradlew runClient -Pshowcase` (needs a world copied to `run/saves/showcase`, e.g. from `runServer`) screenshots every creature/pose to `run/screenshots` (client-side only, no server mobs). Under Xvfb: `Xvfb :99 &; DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 ...`.

## Variants
Every species has 5 colour ranks (red/blue/black/silver/gold). Creative tab "Hyrule Creatures: Variants" holds one spawn egg per species and rank (e.g. Silver Lynel). Elemental variants (Fire/Ice/Shock Lizalfos, Fire/Ice/Electric Keese) are separate species. `/summon hyrulecreatures:lynel ~ ~ ~ {Rank:3}` also fixes the rank.

## GeckoLib decision
Not migrated: the current rig (spec JSON + procedural poses) already covers 100 species with keyframed attacks. GeckoLib would require hand-authoring a .geo.json model and .animation.json for every species in Blockbench (~100 files) plus a new dependency. Recommended only for a handful of hero creatures (Lynel, Hinox, Guardian, Gleeok) if hand-made animation is wanted.
