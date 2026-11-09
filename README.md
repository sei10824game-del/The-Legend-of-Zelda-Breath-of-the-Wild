# Hyrule Creatures (Minecraft 1.20.1 / Forge 47)

BotW + TotK creatures & weapons. TotK variants take priority over BotW.

- Assets are generated: `python3 tools/gen_assets.py` (models spec, textures, lang, weapons, biome spawns). Add a species = add an entry in `SPECIES`/`PAL` + a `Species` enum entry.
- Rank (red/blue/black/silver/gold) scales HP/damage and picks weapons. Stagger: a hit ≥35% max HP or 4 hits within ~1.5s knocks the mob down (80 ticks, takes 1.5x damage).
- Attack styles: SMASH / SLASH (3-hit combo) / THRUST / SPIN / BITE, each with its own keyframed animation (`CreatureModel`).
- Every non-mod mob is hostile to these mobs and vice versa (`FactionEvents`).

## Done
Bokoblin, Moblin, Lizalfos, Keese, Hinox, Talus, Gibdo, Horriblin, Octorok, Wizzrobe, Lynel, Chuchu, Guardian Stalker, Stalkoblin, Stalmoblin, Stalizalfos, Yiga Footsoldier, Blademaster, Soldier/Captain Construct, Frox, Phantom Ganon, Gleeok (3 heads, elemental breath); 57 weapons (melee, bows, shields; mobs block with shields); monster-part drops (horn/fang/guts per species); ranged system (SHOOT: arrows, rocks, fire/ice/spark balls, returning boomerang).
## TODO: Gleeok, Molduga, Frox, Gloom Hands, Phantom Ganon, Calamity Ganon, Demise etc.; hand-polished models; in-client visual check.
Remaining creatures (Lynel, Guardian, Chuchu, Wizzrobe, Octorok, Gleeok, Gibdo, Horriblin, Construct, Phantom Ganon, bosses...), elemental variants, loot tables, hand-polished models.

## Visual check (dev)
`./gradlew runClient -Pshowcase` (needs a world copied to `run/saves/showcase`, e.g. from `runServer`) screenshots every creature/pose to `run/screenshots` (client-side only, no server mobs). Under Xvfb: `Xvfb :99 &; DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 ...`.
