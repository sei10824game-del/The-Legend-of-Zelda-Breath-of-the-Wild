package com.hyrulecreatures;

public enum Species {
    //            id         w     h     hp  dmg  speed knock reach scale  attack            spin  flies  weapons per rank (red,blue,black,silver,gold)
    BOKOBLIN("bokoblin", 1.64f, 2.73f, 20, 2, 0.27, 0.4, 2.5, 1.33f, AttackKind.SMASH, 0f, false, new String[][]{
        {"boko_club", "boko_spear", "boko_bat", "boko_bow"}, {"spiked_boko_club", "spiked_boko_spear", "spiked_boko_bow"},
        {"dragonbone_boko_club", "dragonbone_boko_spear", "dragonbone_boko_bow"},
        {"dragonbone_boko_bow", "dragonbone_boko_spear", "knights_broadsword", "knights_bow"},
        {"royal_bow", "royal_broadsword", "royal_halberd"}}),
    MOBLIN("moblin", 2.21f, 4.5f, 50, 4, 0.24, 1.6, 3.4, 1.8f, AttackKind.SMASH, 0.25f, false, new String[][]{
        {"moblin_club"}, {"spiked_moblin_club"}, {"dragonbone_moblin_club"},
        {"dragonbone_moblin_club", "lynel_crusher"}, {"dragonbone_moblin_club", "savage_lynel_crusher"}}),
    LIZALFOS("lizalfos", 1.89f, 3.13f, 24, 3, 0.33, 0.5, 3.0, 1.51f, AttackKind.SLASH, 0f, false, new String[][]{
        {"lizal_boomerang"}, {"lizal_forked_boomerang"}, {"lizal_tri_boomerang"}, {"lizal_tri_boomerang"}, {"lizal_tri_boomerang"}}),
    KEESE("keese", 3.71f, 1.3f, 6, 2, 0.5, 0.1, 2.0, 1.48f, AttackKind.BITE, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    HINOX("hinox", 5.45f, 9.09f, 120, 8, 0.2, 2.5, 6.5, 4.28f, AttackKind.SMASH, 0.2f, false, new String[][]{
        {"moblin_club"}, {"spiked_moblin_club"}, {"dragonbone_moblin_club"}, {"lynel_crusher"}, {"savage_lynel_crusher"}}),
    TALUS("talus", 2.69f, 4.49f, 80, 7, 0.18, 2.0, 4.5, 2.88f, AttackKind.SMASH, 0.15f, false, new String[][]{{}, {}, {}, {}, {}}),
    GIBDO("gibdo", 1.1f, 3.12f, 30, 3, 0.25, 0.3, 2.6, 1.42f, AttackKind.SLASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    OCTOROK("octorok", 1.48f, 2.47f, 16, 3, 0.24, 0.2, 14.0, 1.52f, AttackKind.SHOOT, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    WIZZROBE("wizzrobe", 2.0f, 3.64f, 24, 4, 0.2, 0.1, 14.0, 1.66f, AttackKind.SHOOT, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    LYNEL("lynel", 2.6f, 5.0f, 120, 8, 0.3, 2.5, 3.8, 1.7f, AttackKind.SLASH, 0f, false, new String[][]{
        {"lynel_sword", "lynel_spear", "lynel_crusher", "lynel_bow"}, {"mighty_lynel_sword", "mighty_lynel_spear", "mighty_lynel_crusher", "mighty_lynel_bow"},
        {"savage_lynel_sword", "savage_lynel_spear", "savage_lynel_crusher", "savage_lynel_bow"},
        {"savage_lynel_sword", "savage_lynel_spear", "savage_lynel_crusher", "savage_lynel_bow"},
        {"savage_lynel_sword", "savage_lynel_spear", "savage_lynel_crusher", "savage_lynel_bow"}}),
    CHUCHU("chuchu", 1.66f, 1.56f, 12, 3, 0.2, 0.2, 3.4, 2.08f, AttackKind.BITE, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    GUARDIAN("guardian", 4.68f, 7.8f, 100, 10, 0.26, 1.0, 8.1, 3.9f, AttackKind.BEAM, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    DECAYED_GUARDIAN("decayed_guardian", 3.3f, 5.5f, 60, 6, 0.16, 0.5, 5.8, 2.75f, AttackKind.BEAM, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    GUARDIAN_TURRET("guardian_turret", 2.85f, 4.75f, 120, 10, 0.0, 0.0, 4.8, 3.04f, AttackKind.BEAM, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    GUARDIAN_SKYWATCHER("guardian_skywatcher", 1.56f, 2.6f, 50, 8, 0.3, 0.3, 3.9, 2.34f, AttackKind.BEAM, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    GUARDIAN_SCOUT_1("guardian_scout_1", 2.18f, 3.64f, 70, 5, 0.22, 0.5, 5.1, 2.33f, AttackKind.SLASH, 0f, false, new String[][]{
        {"guardian_sword"}, {"guardian_sword"}, {"guardian_sword"}, {"guardian_sword"}, {"guardian_sword"}}),
    GUARDIAN_SCOUT_2("guardian_scout_2", 2.18f, 3.64f, 100, 7, 0.22, 0.5, 5.3, 2.33f, AttackKind.SLASH, 0f, false, new String[][]{
        {"guardian_spear"}, {"guardian_spear"}, {"guardian_spear"}, {"guardian_spear"}, {"guardian_spear"}}),
    GUARDIAN_SCOUT_3("guardian_scout_3", 2.69f, 4.49f, 150, 10, 0.22, 1.2, 6.0, 2.88f, AttackKind.SMASH, 0.3f, false, new String[][]{
        {"guardian_sword_plus"}, {"guardian_sword_plus"}, {"guardian_sword_plus"}, {"guardian_sword_plus"}, {"guardian_sword_plus"}}),
    GUARDIAN_SCOUT_4("guardian_scout_4", 2.69f, 4.49f, 240, 12, 0.26, 1.5, 6.0, 2.88f, AttackKind.SLASH, 0f, false, new String[][]{
        {"guardian_sword"}, {"guardian_sword"}, {"guardian_sword"}, {"guardian_sword"}, {"guardian_sword"}}),
    STALKOBLIN("stalkoblin", 0.78f, 2.21f, 1, 2, 0.28, 0.3, 2.5, 1.3f, AttackKind.SMASH, 0f, false, new String[][]{
        {"boko_club", "boko_spear"}, {"spiked_boko_club", "spiked_boko_spear"}, {"dragonbone_boko_club"}, {"dragonbone_boko_spear"}, {"dragonbone_boko_club"}}),
    STALMOBLIN("stalmoblin", 2.34f, 4.51f, 1, 4, 0.25, 1.2, 3.5, 1.9f, AttackKind.SMASH, 0.2f, false, new String[][]{
        {"moblin_club"}, {"spiked_moblin_club"}, {"dragonbone_moblin_club"}, {"dragonbone_moblin_club"}, {"dragonbone_moblin_club"}}),
    STALIZALFOS("stalizalfos", 1.89f, 3.13f, 1, 3, 0.34, 0.4, 3.0, 1.51f, AttackKind.SLASH, 0f, false, new String[][]{
        {"lizal_boomerang"}, {"lizal_forked_boomerang"}, {"lizal_tri_boomerang"}, {"lizal_tri_boomerang"}, {"lizal_tri_boomerang"}}),
    YIGA_FOOTSOLDIER("yiga_footsoldier", 0.78f, 2.34f, 30, 3, 0.32, 0.3, 2.5, 1.3f, AttackKind.SLASH, 0f, false, new String[][]{
        {"yiga_blade", "yiga_bow"}, {"yiga_blade", "soldiers_bow"}, {"yiga_blade", "knights_broadsword"}, {"yiga_blade", "knights_bow"}, {"royal_broadsword", "royal_bow"}}),
    YIGA_BLADEMASTER("yiga_blademaster", 0.78f, 2.34f, 70, 6, 0.36, 0.5, 2.6, 1.43f, AttackKind.SLASH, 0f, false, new String[][]{
        {"yiga_blade"}, {"yiga_blade"}, {"knights_broadsword"}, {"royal_broadsword"}, {"royal_guards_sword"}}),
    SOLDIER_CONSTRUCT("soldier_construct", 2.35f, 4.25f, 60, 6, 0.22, 0.8, 3.6, 1.99f, AttackKind.SLASH, 0f, false, new String[][]{
        {"soldiers_broadsword"}, {"knights_broadsword"}, {"royal_broadsword"}, {"royal_guards_sword"}, {"royal_guards_sword"}}),
    CAPTAIN_CONSTRUCT("captain_construct", 3.84f, 6.76f, 160, 11, 0.22, 2.0, 6.0, 3.49f, AttackKind.SMASH, 0.2f, false, new String[][]{
        {"soldiers_claymore"}, {"knights_claymore"}, {"royal_claymore"}, {"royal_claymore"}, {"royal_claymore"}}),
    FROX("frox", 3.0f, 5.0f, 200, 12, 0.18, 3.0, 5.8, 3.2f, AttackKind.SMASH, 0.2f, false, new String[][]{{}, {}, {}, {}, {}}),
    PHANTOM_GANON("phantom_ganon", 1.55f, 4.0f, 150, 9, 0.3, 1.5, 4.0, 1.94f, AttackKind.SLASH, 0f, true, new String[][]{
        {"royal_guards_sword"}, {"royal_guards_sword"}, {"royal_claymore"}, {"royal_guards_sword"}, {"royal_claymore"}}),
    GLEEOK("gleeok", 5.85f, 9.75f, 300, 10, 0.25, 2.0, 16.0, 3.63f, AttackKind.SHOOT, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    STALHINOX("stalhinox", 5.47f, 9.11f, 160, 8, 0.2, 2.5, 6.0, 3.84f, AttackKind.SMASH, 0.2f, false, new String[][]{{"moblin_club"}, {"spiked_moblin_club"}, {"dragonbone_moblin_club"}, {"lynel_crusher"}, {"savage_lynel_crusher"}}),
    CALAMITY_GANON("calamity_ganon", 6.9f, 14.94f, 1500, 25, 0.22, 3.0, 11.2, 7.24f, AttackKind.BEAM, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    MASTER_KOHGA("master_kohga", 1.17f, 3.38f, 300, 9, 0.34, 1.0, 3.6, 1.82f, AttackKind.SLASH, 0f, false, new String[][]{{"yiga_blade"}, {"yiga_blade"}, {"yiga_blade"}, {"yiga_blade"}, {"yiga_blade"}}),
    FIREBLIGHT_GANON("fireblight_ganon", 2.52f, 5.75f, 400, 12, 0.28, 1.5, 5.0, 2.3f, AttackKind.SLASH, 0f, false, new String[][]{{"royal_guards_sword"}, {"royal_guards_sword"}, {"royal_guards_sword"}, {"royal_guards_sword"}, {"royal_guards_sword"}}),
    WATERBLIGHT_GANON("waterblight_ganon", 2.84f, 5.76f, 400, 12, 0.28, 1.5, 5.4, 2.36f, AttackKind.SLASH, 0f, false, new String[][]{{"royal_halberd"}, {"royal_halberd"}, {"royal_halberd"}, {"royal_halberd"}, {"royal_halberd"}}),
    WINDBLIGHT_GANON("windblight_ganon", 3.46f, 5.76f, 400, 12, 0.32, 1.0, 4.8, 2.36f, AttackKind.SLASH, 0f, true, new String[][]{{"royal_bow"}, {"royal_bow"}, {"royal_bow"}, {"royal_bow"}, {"royal_bow"}}),
    THUNDERBLIGHT_GANON("thunderblight_ganon", 2.85f, 6.24f, 450, 14, 0.26, 2.0, 5.1, 2.38f, AttackKind.SMASH, 0.3f, false, new String[][]{{"royal_claymore"}, {"royal_claymore"}, {"royal_claymore"}, {"royal_claymore"}, {"royal_claymore"}}),
    LIZALFOS_FIRE("lizalfos_fire", 1.87f, 3.12f, 30, 3, 0.33, 0.5, 3.1, 1.64f, AttackKind.SLASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    LIZALFOS_ICE("lizalfos_ice", 1.87f, 3.12f, 30, 3, 0.33, 0.5, 3.1, 1.64f, AttackKind.SLASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    LIZALFOS_ELEC("lizalfos_elec", 1.87f, 3.12f, 30, 3, 0.33, 0.5, 3.1, 1.64f, AttackKind.SLASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    KEESE_FIRE("keese_fire", 3.71f, 1.3f, 6, 2, 0.5, 0.1, 2.0, 1.48f, AttackKind.BITE, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    KEESE_ICE("keese_ice", 3.71f, 1.3f, 6, 2, 0.5, 0.1, 2.0, 1.48f, AttackKind.BITE, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    KEESE_ELEC("keese_elec", 3.71f, 1.3f, 6, 2, 0.5, 0.1, 2.0, 1.48f, AttackKind.BITE, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    BLIZZROBE("blizzrobe", 2.0f, 3.64f, 40, 5, 0.2, 0.1, 14.0, 1.66f, AttackKind.SHOOT, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    THUNDER_WIZZROBE("thunder_wizzrobe", 2.0f, 3.64f, 40, 6, 0.2, 0.1, 14.0, 1.66f, AttackKind.SHOOT, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    STALFOS("stalfos", 0.78f, 2.34f, 30, 4, 0.28, 0.5, 2.6, 1.43f, AttackKind.SLASH, 0f, false, new String[][]{{"stalfos_sword"}, {"stalfos_sword"}, {"stalfos_sword"}, {"stalfos_sword"}, {"stalfos_sword"}}),
    STALMASTER("stalmaster", 1.25f, 4.0f, 200, 9, 0.26, 1.8, 4.0, 2.38f, AttackKind.SMASH, 0.3f, false, new String[][]{{"stalmaster_sword"}, {"stalmaster_sword"}, {"stalmaster_sword"}, {"stalmaster_sword"}, {"stalmaster_sword"}}),
    DARK_LIZALFOS("dark_lizalfos", 1.89f, 3.13f, 80, 6, 0.34, 0.8, 2.7, 1.51f, AttackKind.SLASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    ARMOS("armos", 1.17f, 3.12f, 120, 8, 0.2, 1.5, 3.4, 1.82f, AttackKind.SMASH, 0.2f, false, new String[][]{{"armos_sword"}, {"armos_sword"}, {"armos_sword"}, {"armos_sword"}, {"armos_sword"}}),
    BEAMOS("beamos", 2.29f, 4.76f, 100, 9, 0.0, 0.0, 4.8, 2.54f, AttackKind.BEAM, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    SKULLTULA("skulltula", 1.17f, 1.95f, 24, 4, 0.3, 0.3, 3.6, 2.72f, AttackKind.SLASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    DEKU_BABA("deku_baba", 1.64f, 3.12f, 30, 5, 0.0, 0.3, 6.1, 1.92f, AttackKind.BITE, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    CURSED_BOKOBLIN("cursed_bokoblin", 1.72f, 2.86f, 40, 4, 0.3, 0.4, 2.6, 1.38f, AttackKind.SMASH, 0f, false, new String[][]{{"boko_club", "boko_spear"}, {"spiked_boko_club", "spiked_boko_spear"}, {"dragonbone_boko_club"}, {"dragonbone_boko_spear"}, {"dragonbone_boko_club"}}),
    GHIRAHIM("ghirahim", 0.91f, 2.86f, 500, 10, 0.34, 1.0, 3.6, 1.69f, AttackKind.SLASH, 0f, false, new String[][]{{"ghirahim_sword"}, {"ghirahim_sword"}, {"ghirahim_sword"}, {"ghirahim_sword"}, {"ghirahim_sword"}}),
    DEMISE("demise", 7.8f, 13.0f, 1800, 22, 0.26, 3.0, 7.7, 4.84f, AttackKind.SMASH, 0.25f, false, new String[][]{{"demise_sword"}, {"demise_sword"}, {"demise_sword"}, {"demise_sword"}, {"demise_sword"}}),
    MOLDARACH("moldarach", 3.3f, 5.5f, 500, 12, 0.22, 2.0, 8.8, 5.86f, AttackKind.SMASH, 0.2f, false, new String[][]{{}, {}, {}, {}, {}}),
    KOLOKTOS("koloktos", 7.79f, 12.99f, 700, 14, 0.22, 2.5, 8.3, 5.77f, AttackKind.SMASH, 0.3f, false, new String[][]{{"koloktos_sword"}, {"koloktos_sword"}, {"koloktos_sword"}, {"koloktos_sword"}, {"koloktos_sword"}}),
    SCALDERA("scaldera", 4.12f, 6.88f, 500, 12, 0.2, 2.0, 6.8, 4.59f, AttackKind.SMASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    THE_IMPRISONED("the_imprisoned", 6.9f, 17.27f, 2500, 25, 0.18, 3.5, 7.9, 5.31f, AttackKind.SMASH, 0.25f, false, new String[][]{{}, {}, {}, {}, {}}),
    TENTALUS("tentalus", 5.41f, 9.76f, 800, 14, 0.2, 2.0, 8.8, 6.01f, AttackKind.SMASH, 0.2f, false, new String[][]{{}, {}, {}, {}, {}}),
    TECHNO_BOKOBLIN("techno_bokoblin", 0.78f, 2.21f, 50, 5, 0.3, 0.4, 2.5, 1.3f, AttackKind.SMASH, 0f, false, new String[][]{{"boko_club", "boko_spear"}, {"spiked_boko_club"}, {"dragonbone_boko_club"}, {"dragonbone_boko_spear"}, {"dragonbone_boko_club"}}),
    QUADRO_BABA("quadro_baba", 1.96f, 3.76f, 60, 7, 0.0, 0.4, 7.0, 2.31f, AttackKind.BITE, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    KEESE_DARK("keese_dark", 3.71f, 1.3f, 8, 2, 0.5, 0.1, 2.0, 1.48f, AttackKind.BITE, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    WALL_SKULLTULA("wall_skulltula", 1.51f, 1.17f, 8, 3, 0.32, 0.2, 3.2, 1.62f, AttackKind.SLASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    PETIT_MOLDORM("petit_moldorm", 2.82f, 1.04f, 6, 2, 0.28, 0.1, 3.5, 2.56f, AttackKind.BITE, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    SHAKOMITE("shakomite", 1.4f, 2.34f, 40, 6, 0.24, 1.0, 3.5, 2.2f, AttackKind.SMASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    FROG_MAGMA("frog_magma", 2.05f, 1.56f, 20, 5, 0.0, 0.1, 14.0, 2.27f, AttackKind.SHOOT, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    FROG_ELEC("frog_elec", 2.05f, 1.56f, 20, 5, 0.0, 0.1, 14.0, 2.27f, AttackKind.SHOOT, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    FROG_DARK("frog_dark", 2.05f, 1.56f, 20, 5, 0.0, 0.1, 14.0, 2.27f, AttackKind.SHOOT, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    FROG_WATER("frog_water", 2.05f, 1.56f, 20, 5, 0.0, 0.1, 14.0, 2.27f, AttackKind.SHOOT, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    DON_GERAR("don_gerar", 1.04f, 3.12f, 400, 11, 0.28, 1.0, 3.6, 1.82f, AttackKind.SLASH, 0f, false, new String[][]{{"don_cutlass"}, {"don_cutlass"}, {"don_cutlass"}, {"don_cutlass"}, {"don_cutlass"}}),
    DON_KILLER("don_killer", 1.04f, 3.12f, 400, 11, 0.28, 1.0, 3.6, 1.82f, AttackKind.SLASH, 0f, false, new String[][]{{"don_cutlass"}, {"don_cutlass"}, {"don_cutlass"}, {"don_cutlass"}, {"don_cutlass"}}),
    GUMARM("gumarm", 2.48f, 4.12f, 300, 12, 0.2, 2.0, 10.4, 9.43f, AttackKind.SMASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    PARASPALAS("paraspalas", 3.3f, 5.5f, 900, 12, 0.22, 1.5, 16.0, 4.4f, AttackKind.SHOOT, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    BULBLIN("bulblin", 0.91f, 2.6f, 40, 5, 0.28, 0.6, 2.9, 1.56f, AttackKind.SLASH, 0f, false, new String[][]{{"bulblin_club", "bulblin_spear", "bulblin_bow"}, {"bulblin_club", "bulblin_spear", "bulblin_bow"}, {"bulblin_club", "bulblin_spear", "bulblin_bow"}, {"bulblin_club", "bulblin_spear", "bulblin_bow"}, {"bulblin_club", "bulblin_spear", "bulblin_bow"}}),
    KING_BULBLIN("king_bulblin", 1.62f, 4.75f, 500, 14, 0.24, 2.5, 4.5, 2.62f, AttackKind.SMASH, 0.25f, false, new String[][]{{"king_bulblin_club"}, {"king_bulblin_club"}, {"king_bulblin_club"}, {"king_bulblin_club"}, {"king_bulblin_club"}}),
    STALHOUND("stalhound", 1.25f, 2.08f, 30, 5, 0.42, 0.5, 3.2, 1.96f, AttackKind.SLASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    SHADOW_BEAST("shadow_beast", 2.18f, 3.64f, 120, 9, 0.4, 1.2, 4.3, 2.91f, AttackKind.SLASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    REDEAD("redead", 1.0f, 2.86f, 50, 3, 0.2, 0.2, 2.5, 1.43f, AttackKind.SLASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    POE("poe", 1.69f, 2.86f, 30, 4, 0.2, 0.1, 14.0, 1.99f, AttackKind.SHOOT, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    TEKTITE("tektite", 1.26f, 1.82f, 24, 4, 0.3, 0.3, 3.0, 2.24f, AttackKind.SLASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    PEAHAT("peahat", 1.4f, 2.34f, 30, 5, 0.35, 0.3, 3.0, 2.27f, AttackKind.BITE, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    BUBBLE_FIRE("bubble_fire", 0.78f, 0.78f, 10, 3, 0.4, 0.1, 1.8, 1.3f, AttackKind.BITE, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    BUBBLE_ICE("bubble_ice", 0.78f, 0.78f, 10, 3, 0.4, 0.1, 1.8, 1.3f, AttackKind.BITE, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    BUBBLE_DARK("bubble_dark", 0.78f, 0.78f, 10, 3, 0.4, 0.1, 1.8, 1.3f, AttackKind.BITE, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    DODONGO("dodongo", 4.12f, 6.88f, 300, 12, 0.24, 2.0, 6.5, 4.59f, AttackKind.SMASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    HELMASAUR("helmasaur", 1.4f, 2.34f, 120, 8, 0.28, 1.0, 3.0, 2.34f, AttackKind.SMASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    DARK_NUT("dark_nut", 1.17f, 3.12f, 250, 12, 0.24, 2.0, 3.9, 1.82f, AttackKind.SMASH, 0.2f, false, new String[][]{{"dark_nut_sword"}, {"dark_nut_sword"}, {"dark_nut_sword"}, {"dark_nut_sword"}, {"dark_nut_sword"}}),
    DEATH_SWORD("death_sword", 2.97f, 6.88f, 700, 16, 0.3, 2.0, 5.8, 2.97f, AttackKind.SMASH, 0.3f, true, new String[][]{{"death_sword_blade"}, {"death_sword_blade"}, {"death_sword_blade"}, {"death_sword_blade"}, {"death_sword_blade"}}),
    ZANT("zant", 0.91f, 2.86f, 700, 12, 0.34, 1.0, 3.6, 1.69f, AttackKind.SLASH, 0f, true, new String[][]{{"zant_sword"}, {"zant_sword"}, {"zant_sword"}, {"zant_sword"}, {"zant_sword"}}),
    GANONDORF("ganondorf", 1.5f, 4.25f, 1200, 20, 0.28, 3.0, 5.2, 2.75f, AttackKind.SMASH, 0.25f, false, new String[][]{{"ganon_sword"}, {"ganon_sword"}, {"ganon_sword"}, {"ganon_sword"}, {"ganon_sword"}}),
    DIABABA("diababa", 5.26f, 9.75f, 600, 12, 0.14, 1.5, 16.0, 3.63f, AttackKind.SHOOT, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    ARGOROK("argorok", 6.9f, 14.96f, 1500, 16, 0.3, 2.5, 16.0, 5.57f, AttackKind.SHOOT, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    FYRUS("fyrus", 1.75f, 5.0f, 1000, 18, 0.22, 2.5, 5.0, 2.75f, AttackKind.SMASH, 0.2f, false, new String[][]{{"fyrus_blade"}, {"fyrus_blade"}, {"fyrus_blade"}, {"fyrus_blade"}, {"fyrus_blade"}}),
    ARMOGOHMA("armogohma", 4.12f, 6.88f, 900, 14, 0.22, 2.0, 16.0, 5.79f, AttackKind.SHOOT, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    AERALFOS("aeralfos", 2.02f, 3.37f, 70, 6, 0.3, 0.5, 3.1, 1.77f, AttackKind.SLASH, 0f, true, new String[][]{{"aeralfos_spear"}, {"aeralfos_spear"}, {"aeralfos_spear"}, {"aeralfos_spear"}, {"aeralfos_spear"}}),
    DINOLFOS("dinolfos", 2.03f, 3.38f, 80, 6, 0.34, 0.8, 3.0, 1.69f, AttackKind.SLASH, 0f, false, new String[][]{{"dinolfos_sword"}, {"dinolfos_sword"}, {"dinolfos_sword"}, {"dinolfos_sword"}, {"dinolfos_sword"}}),
    KARGAROK("kargarok", 1.4f, 2.34f, 40, 5, 0.4, 0.3, 2.7, 2.2f, AttackKind.BITE, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    HORRIBLIN("horriblin", 1.79f, 2.99f, 30, 3, 0.3, 0.4, 2.7, 1.44f, AttackKind.SLASH, 0f, false, new String[][]{
        {"boko_club", "boko_spear"}, {"spiked_boko_club", "spiked_boko_spear"}, {"dragonbone_boko_club"}, {"dragonbone_boko_spear"}, {"dragonbone_boko_club"}});

    public final String id;
    public final float w, h, scale, spin;
    public final double hp, dmg, speed, knock, reach;
    public final AttackKind attack;
    public final boolean flies;
    public final String[][] weapons;

    Species(String id, float w, float h, double hp, double dmg, double speed, double knock, double reach, float scale,
            AttackKind attack, float spin, boolean flies, String[][] weapons) {
        this.id = id; this.w = w; this.h = h; this.hp = hp; this.dmg = dmg; this.speed = speed; this.knock = knock;
        this.reach = reach; this.scale = scale; this.attack = attack; this.spin = spin; this.flies = flies; this.weapons = weapons;
    }

    public boolean isStal() { return this == STALKOBLIN || this == STALMOBLIN || this == STALIZALFOS; }
    public boolean teleports() {
        return switch (this) { case ZANT, GHIRAHIM, WIZZROBE, BLIZZROBE, THUNDER_WIZZROBE, FIREBLIGHT_GANON, WATERBLIGHT_GANON, WINDBLIGHT_GANON, THUNDERBLIGHT_GANON, PHANTOM_GANON, MASTER_KOHGA, YIGA_FOOTSOLDIER, YIGA_BLADEMASTER -> true; default -> false; };
    }

    public static final String[] RANKS = {"red", "blue", "black", "silver", "gold"};
    public static final double[] HP_MUL = {1, 1.5, 2.5, 4, 6};
    public static final double[] DMG_MUL = {1, 1.3, 1.8, 2.4, 3.2};
}
