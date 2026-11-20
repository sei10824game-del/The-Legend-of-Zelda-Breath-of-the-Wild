package com.hyrulecreatures;

public enum Species {
    //            id         w     h     hp  dmg  speed knock reach scale  attack            spin  flies  weapons per rank (red,blue,black,silver,gold)
    BOKOBLIN("bokoblin", 0.6f, 1.7f, 20, 2, 0.27, 0.4, 1.9, 1.0f, AttackKind.SMASH, 0f, false, new String[][]{
        {"boko_club", "boko_spear", "boko_bat", "boko_bow"}, {"spiked_boko_club", "spiked_boko_spear", "spiked_boko_bow"},
        {"dragonbone_boko_club", "dragonbone_boko_spear", "dragonbone_boko_bow"},
        {"dragonbone_boko_bow", "dragonbone_boko_spear", "knights_broadsword", "knights_bow"},
        {"royal_bow", "royal_broadsword", "royal_halberd"}}),
    MOBLIN("moblin", 1.87f, 3.61f, 50, 4, 0.24, 1.6, 2.8, 1.52f, AttackKind.SMASH, 0.25f, false, new String[][]{
        {"moblin_club"}, {"spiked_moblin_club"}, {"dragonbone_moblin_club"},
        {"dragonbone_moblin_club", "lynel_crusher"}, {"dragonbone_moblin_club", "savage_lynel_crusher"}}),
    LIZALFOS("lizalfos", 1.51f, 2.41f, 24, 3, 0.33, 0.5, 2.3, 1.16f, AttackKind.SLASH, 0f, false, new String[][]{
        {"lizal_boomerang"}, {"lizal_forked_boomerang"}, {"lizal_tri_boomerang"}, {"lizal_tri_boomerang"}, {"lizal_tri_boomerang"}}),
    KEESE("keese", 2.49f, 0.9f, 6, 2, 0.5, 0.1, 1.7, 1.31f, AttackKind.BITE, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    HINOX("hinox", 4.96f, 7.01f, 120, 8, 0.2, 2.5, 4.6, 2.95f, AttackKind.SMASH, 0.2f, false, new String[][]{
        {"moblin_club"}, {"spiked_moblin_club"}, {"dragonbone_moblin_club"}, {"lynel_crusher"}, {"savage_lynel_crusher"}}),
    TALUS("talus", 5.87f, 5.5f, 80, 7, 0.18, 2.0, 4.7, 3.26f, AttackKind.SMASH, 0.15f, false, new String[][]{{}, {}, {}, {}, {}}),
    GIBDO("gibdo", 0.85f, 2.4f, 30, 3, 0.25, 0.3, 2.0, 1.09f, AttackKind.SLASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    OCTOROK("octorok", 1.44f, 1.8f, 16, 3, 0.24, 0.2, 14.0, 1.44f, AttackKind.SHOOT, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    WIZZROBE("wizzrobe", 1.12f, 2.79f, 24, 4, 0.2, 0.1, 14.0, 1.24f, AttackKind.SHOOT, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    LYNEL("lynel", 1.4f, 3.0f, 120, 8, 0.3, 2.5, 3.4, 1.6f, AttackKind.SLASH, 0f, false, new String[][]{
        {"lynel_sword", "lynel_spear", "lynel_crusher", "lynel_bow"}, {"mighty_lynel_sword", "mighty_lynel_spear", "mighty_lynel_crusher", "mighty_lynel_bow"},
        {"savage_lynel_sword", "savage_lynel_spear", "savage_lynel_crusher", "savage_lynel_bow"},
        {"savage_lynel_sword", "savage_lynel_spear", "savage_lynel_crusher", "savage_lynel_bow"},
        {"savage_lynel_sword", "savage_lynel_spear", "savage_lynel_crusher", "savage_lynel_bow"}}),
    CHUCHU("chuchu", 0.9f, 1.1f, 12, 3, 0.2, 0.2, 2.4, 1.47f, AttackKind.BITE, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    GUARDIAN("guardian", 3.4f, 6.0f, 100, 10, 0.26, 1.0, 6.2, 3.0f, AttackKind.BEAM, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    DECAYED_GUARDIAN("decayed_guardian", 2.6f, 4.4f, 60, 6, 0.16, 0.5, 4.6, 2.2f, AttackKind.BEAM, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    GUARDIAN_TURRET("guardian_turret", 2.4f, 3.8f, 120, 10, 0.0, 0.0, 3.8, 2.43f, AttackKind.BEAM, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    GUARDIAN_SKYWATCHER("guardian_skywatcher", 1.6f, 2.0f, 50, 8, 0.3, 0.3, 3.0, 1.8f, AttackKind.BEAM, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    GUARDIAN_SCOUT_1("guardian_scout_1", 1.97f, 2.8f, 70, 5, 0.22, 0.5, 3.9, 1.79f, AttackKind.SLASH, 0f, false, new String[][]{
        {"guardian_sword"}, {"guardian_sword"}, {"guardian_sword"}, {"guardian_sword"}, {"guardian_sword"}}),
    GUARDIAN_SCOUT_2("guardian_scout_2", 1.97f, 2.8f, 100, 7, 0.22, 0.5, 4.1, 1.79f, AttackKind.SLASH, 0f, false, new String[][]{
        {"guardian_spear"}, {"guardian_spear"}, {"guardian_spear"}, {"guardian_spear"}, {"guardian_spear"}}),
    GUARDIAN_SCOUT_3("guardian_scout_3", 2.53f, 3.59f, 150, 10, 0.22, 1.2, 4.8, 2.3f, AttackKind.SMASH, 0.3f, false, new String[][]{
        {"guardian_sword_plus"}, {"guardian_sword_plus"}, {"guardian_sword_plus"}, {"guardian_sword_plus"}, {"guardian_sword_plus"}}),
    GUARDIAN_SCOUT_4("guardian_scout_4", 2.53f, 3.59f, 240, 12, 0.26, 1.5, 4.8, 2.3f, AttackKind.SLASH, 0f, false, new String[][]{
        {"guardian_sword"}, {"guardian_sword"}, {"guardian_sword"}, {"guardian_sword"}, {"guardian_sword"}}),
    STALKOBLIN("stalkoblin", 0.6f, 1.7f, 1, 2, 0.28, 0.3, 1.9, 1.0f, AttackKind.SMASH, 0f, false, new String[][]{
        {"boko_club", "boko_spear"}, {"spiked_boko_club", "spiked_boko_spear"}, {"dragonbone_boko_club"}, {"dragonbone_boko_spear"}, {"dragonbone_boko_club"}}),
    STALMOBLIN("stalmoblin", 1.87f, 3.61f, 1, 4, 0.25, 1.2, 2.8, 1.52f, AttackKind.SMASH, 0.2f, false, new String[][]{
        {"moblin_club"}, {"spiked_moblin_club"}, {"dragonbone_moblin_club"}, {"dragonbone_moblin_club"}, {"dragonbone_moblin_club"}}),
    STALIZALFOS("stalizalfos", 1.51f, 2.41f, 1, 3, 0.34, 0.4, 2.3, 1.16f, AttackKind.SLASH, 0f, false, new String[][]{
        {"lizal_boomerang"}, {"lizal_forked_boomerang"}, {"lizal_tri_boomerang"}, {"lizal_tri_boomerang"}, {"lizal_tri_boomerang"}}),
    YIGA_FOOTSOLDIER("yiga_footsoldier", 0.6f, 1.8f, 30, 3, 0.32, 0.3, 1.9, 1.0f, AttackKind.SLASH, 0f, false, new String[][]{
        {"yiga_blade", "yiga_bow"}, {"yiga_blade", "soldiers_bow"}, {"yiga_blade", "knights_broadsword"}, {"yiga_blade", "knights_bow"}, {"royal_broadsword", "royal_bow"}}),
    YIGA_BLADEMASTER("yiga_blademaster", 0.6f, 1.8f, 70, 6, 0.36, 0.5, 2.0, 1.1f, AttackKind.SLASH, 0f, false, new String[][]{
        {"yiga_blade"}, {"yiga_blade"}, {"knights_broadsword"}, {"royal_broadsword"}, {"royal_guards_sword"}}),
    SOLDIER_CONSTRUCT("soldier_construct", 1.88f, 3.4f, 60, 6, 0.22, 0.8, 2.9, 1.59f, AttackKind.SLASH, 0f, false, new String[][]{
        {"soldiers_broadsword"}, {"knights_broadsword"}, {"royal_broadsword"}, {"royal_guards_sword"}, {"royal_guards_sword"}}),
    CAPTAIN_CONSTRUCT("captain_construct", 3.07f, 5.41f, 160, 11, 0.22, 2.0, 4.8, 2.79f, AttackKind.SMASH, 0.2f, false, new String[][]{
        {"soldiers_claymore"}, {"knights_claymore"}, {"royal_claymore"}, {"royal_claymore"}, {"royal_claymore"}}),
    FROX("frox", 6.0f, 6.01f, 200, 12, 0.18, 3.0, 6.0, 3.56f, AttackKind.SMASH, 0.2f, false, new String[][]{{}, {}, {}, {}, {}}),
    PHANTOM_GANON("phantom_ganon", 1.24f, 3.2f, 150, 9, 0.3, 1.5, 3.2, 1.55f, AttackKind.SLASH, 0f, true, new String[][]{
        {"royal_guards_sword"}, {"royal_guards_sword"}, {"royal_claymore"}, {"royal_guards_sword"}, {"royal_claymore"}}),
    GLEEOK("gleeok", 6.0f, 7.5f, 300, 10, 0.25, 2.0, 16.0, 2.79f, AttackKind.SHOOT, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    STALHINOX("stalhinox", 4.72f, 7.01f, 160, 8, 0.2, 2.5, 4.6, 2.95f, AttackKind.SMASH, 0.2f, false, new String[][]{{"moblin_club"}, {"spiked_moblin_club"}, {"dragonbone_moblin_club"}, {"lynel_crusher"}, {"savage_lynel_crusher"}}),
    CALAMITY_GANON("calamity_ganon", 7.0f, 13.01f, 1500, 25, 0.22, 3.0, 11.2, 6.12f, AttackKind.BEAM, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    MASTER_KOHGA("master_kohga", 0.9f, 2.6f, 300, 9, 0.34, 1.0, 2.8, 1.4f, AttackKind.SLASH, 0f, false, new String[][]{{"yiga_blade"}, {"yiga_blade"}, {"yiga_blade"}, {"yiga_blade"}, {"yiga_blade"}}),
    FIREBLIGHT_GANON("fireblight_ganon", 2.02f, 4.6f, 400, 12, 0.28, 1.5, 4.0, 1.84f, AttackKind.SLASH, 0f, false, new String[][]{{"royal_guards_sword"}, {"royal_guards_sword"}, {"royal_guards_sword"}, {"royal_guards_sword"}, {"royal_guards_sword"}}),
    WATERBLIGHT_GANON("waterblight_ganon", 2.27f, 4.61f, 400, 12, 0.28, 1.5, 4.3, 1.89f, AttackKind.SLASH, 0f, false, new String[][]{{"royal_halberd"}, {"royal_halberd"}, {"royal_halberd"}, {"royal_halberd"}, {"royal_halberd"}}),
    WINDBLIGHT_GANON("windblight_ganon", 3.78f, 4.61f, 400, 12, 0.32, 1.0, 3.8, 1.89f, AttackKind.SLASH, 0f, true, new String[][]{{"royal_bow"}, {"royal_bow"}, {"royal_bow"}, {"royal_bow"}, {"royal_bow"}}),
    THUNDERBLIGHT_GANON("thunderblight_ganon", 2.28f, 4.99f, 450, 14, 0.26, 2.0, 4.1, 1.9f, AttackKind.SMASH, 0.3f, false, new String[][]{{"royal_claymore"}, {"royal_claymore"}, {"royal_claymore"}, {"royal_claymore"}, {"royal_claymore"}}),
    LIZALFOS_FIRE("lizalfos_fire", 1.64f, 2.4f, 30, 3, 0.33, 0.5, 2.4, 1.26f, AttackKind.SLASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    LIZALFOS_ICE("lizalfos_ice", 1.64f, 2.4f, 30, 3, 0.33, 0.5, 2.4, 1.26f, AttackKind.SLASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    LIZALFOS_ELEC("lizalfos_elec", 1.64f, 2.4f, 30, 3, 0.33, 0.5, 2.4, 1.26f, AttackKind.SLASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    KEESE_FIRE("keese_fire", 2.49f, 0.9f, 6, 2, 0.5, 0.1, 1.7, 1.31f, AttackKind.BITE, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    KEESE_ICE("keese_ice", 2.49f, 0.9f, 6, 2, 0.5, 0.1, 1.7, 1.31f, AttackKind.BITE, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    KEESE_ELEC("keese_elec", 2.49f, 0.9f, 6, 2, 0.5, 0.1, 1.7, 1.31f, AttackKind.BITE, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    BLIZZROBE("blizzrobe", 1.12f, 2.79f, 40, 5, 0.2, 0.1, 14.0, 1.24f, AttackKind.SHOOT, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    THUNDER_WIZZROBE("thunder_wizzrobe", 1.12f, 2.79f, 40, 6, 0.2, 0.1, 14.0, 1.24f, AttackKind.SHOOT, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    STALFOS("stalfos", 0.6f, 1.8f, 30, 4, 0.28, 0.5, 2.0, 1.1f, AttackKind.SLASH, 0f, false, new String[][]{{"stalfos_sword"}, {"stalfos_sword"}, {"stalfos_sword"}, {"stalfos_sword"}, {"stalfos_sword"}}),
    STALMASTER("stalmaster", 1.0f, 3.2f, 200, 9, 0.26, 1.8, 3.2, 1.9f, AttackKind.SMASH, 0.3f, false, new String[][]{{"stalmaster_sword"}, {"stalmaster_sword"}, {"stalmaster_sword"}, {"stalmaster_sword"}, {"stalmaster_sword"}}),
    DARK_LIZALFOS("dark_lizalfos", 1.51f, 2.41f, 80, 6, 0.34, 0.8, 2.1, 1.16f, AttackKind.SLASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    ARMOS("armos", 0.9f, 2.4f, 120, 8, 0.2, 1.5, 2.6, 1.4f, AttackKind.SMASH, 0.2f, false, new String[][]{{"armos_sword"}, {"armos_sword"}, {"armos_sword"}, {"armos_sword"}, {"armos_sword"}}),
    BEAMOS("beamos", 1.83f, 3.81f, 100, 9, 0.0, 0.0, 3.8, 2.03f, AttackKind.BEAM, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    SKULLTULA("skulltula", 1.93f, 1.5f, 24, 4, 0.3, 0.3, 2.8, 2.09f, AttackKind.SLASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    DEKU_BABA("deku_baba", 1.26f, 2.4f, 30, 5, 0.0, 0.3, 4.7, 1.48f, AttackKind.BITE, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    CURSED_BOKOBLIN("cursed_bokoblin", 1.59f, 2.2f, 40, 4, 0.3, 0.4, 2.0, 1.06f, AttackKind.SMASH, 0f, false, new String[][]{{"boko_club", "boko_spear"}, {"spiked_boko_club", "spiked_boko_spear"}, {"dragonbone_boko_club"}, {"dragonbone_boko_spear"}, {"dragonbone_boko_club"}}),
    GHIRAHIM("ghirahim", 0.7f, 2.2f, 500, 10, 0.34, 1.0, 2.8, 1.3f, AttackKind.SLASH, 0f, false, new String[][]{{"ghirahim_sword"}, {"ghirahim_sword"}, {"ghirahim_sword"}, {"ghirahim_sword"}, {"ghirahim_sword"}}),
    DEMISE("demise", 6.0f, 10.0f, 1800, 22, 0.26, 3.0, 5.9, 3.72f, AttackKind.SMASH, 0.25f, false, new String[][]{{"demise_sword"}, {"demise_sword"}, {"demise_sword"}, {"demise_sword"}, {"demise_sword"}}),
    MOLDARACH("moldarach", 6.0f, 4.4f, 500, 12, 0.22, 2.0, 7.0, 4.69f, AttackKind.SMASH, 0.2f, false, new String[][]{{}, {}, {}, {}, {}}),
    KOLOKTOS("koloktos", 6.0f, 9.99f, 700, 14, 0.22, 2.5, 6.4, 4.44f, AttackKind.SMASH, 0.3f, false, new String[][]{{"koloktos_sword"}, {"koloktos_sword"}, {"koloktos_sword"}, {"koloktos_sword"}, {"koloktos_sword"}}),
    SCALDERA("scaldera", 5.5f, 5.5f, 500, 12, 0.2, 2.0, 5.4, 3.67f, AttackKind.SMASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    THE_IMPRISONED("the_imprisoned", 6.0f, 15.02f, 2500, 25, 0.18, 3.5, 6.9, 4.62f, AttackKind.SMASH, 0.25f, false, new String[][]{{}, {}, {}, {}, {}}),
    TENTALUS("tentalus", 4.16f, 7.51f, 800, 14, 0.2, 2.0, 6.8, 4.62f, AttackKind.SMASH, 0.2f, false, new String[][]{{}, {}, {}, {}, {}}),
    TECHNO_BOKOBLIN("techno_bokoblin", 0.6f, 1.7f, 50, 5, 0.3, 0.4, 1.9, 1.0f, AttackKind.SMASH, 0f, false, new String[][]{{"boko_club", "boko_spear"}, {"spiked_boko_club"}, {"dragonbone_boko_club"}, {"dragonbone_boko_spear"}, {"dragonbone_boko_club"}}),
    QUADRO_BABA("quadro_baba", 1.57f, 3.01f, 60, 7, 0.0, 0.4, 5.6, 1.85f, AttackKind.BITE, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    KEESE_DARK("keese_dark", 2.49f, 0.9f, 8, 2, 0.5, 0.1, 1.7, 1.31f, AttackKind.BITE, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    WALL_SKULLTULA("wall_skulltula", 1.16f, 0.9f, 8, 3, 0.32, 0.2, 2.5, 1.25f, AttackKind.SLASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    PETIT_MOLDORM("petit_moldorm", 2.17f, 0.8f, 6, 2, 0.28, 0.1, 2.7, 1.97f, AttackKind.BITE, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    SHAKOMITE("shakomite", 2.28f, 1.8f, 40, 6, 0.24, 1.0, 2.7, 1.69f, AttackKind.SMASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    FROG_MAGMA("frog_magma", 1.58f, 1.2f, 20, 5, 0.0, 0.1, 14.0, 1.75f, AttackKind.SHOOT, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    FROG_ELEC("frog_elec", 1.58f, 1.2f, 20, 5, 0.0, 0.1, 14.0, 1.75f, AttackKind.SHOOT, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    FROG_DARK("frog_dark", 1.58f, 1.2f, 20, 5, 0.0, 0.1, 14.0, 1.75f, AttackKind.SHOOT, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    FROG_WATER("frog_water", 1.58f, 1.2f, 20, 5, 0.0, 0.1, 14.0, 1.75f, AttackKind.SHOOT, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    DON_GERAR("don_gerar", 0.8f, 2.4f, 400, 11, 0.28, 1.0, 2.8, 1.4f, AttackKind.SLASH, 0f, false, new String[][]{{"don_cutlass"}, {"don_cutlass"}, {"don_cutlass"}, {"don_cutlass"}, {"don_cutlass"}}),
    DON_KILLER("don_killer", 0.8f, 2.4f, 400, 11, 0.28, 1.0, 2.8, 1.4f, AttackKind.SLASH, 0f, false, new String[][]{{"don_cutlass"}, {"don_cutlass"}, {"don_cutlass"}, {"don_cutlass"}, {"don_cutlass"}}),
    GUMARM("gumarm", 6.0f, 3.3f, 300, 12, 0.2, 2.0, 10.4, 7.54f, AttackKind.SMASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    PARASPALAS("paraspalas", 6.0f, 4.4f, 900, 12, 0.22, 1.5, 16.0, 3.52f, AttackKind.SHOOT, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    BULBLIN("bulblin", 0.7f, 2.0f, 40, 5, 0.28, 0.6, 2.2, 1.2f, AttackKind.SLASH, 0f, false, new String[][]{{"bulblin_club", "bulblin_spear", "bulblin_bow"}, {"bulblin_club", "bulblin_spear", "bulblin_bow"}, {"bulblin_club", "bulblin_spear", "bulblin_bow"}, {"bulblin_club", "bulblin_spear", "bulblin_bow"}, {"bulblin_club", "bulblin_spear", "bulblin_bow"}}),
    KING_BULBLIN("king_bulblin", 1.3f, 3.8f, 500, 14, 0.24, 2.5, 3.6, 2.1f, AttackKind.SMASH, 0.25f, false, new String[][]{{"king_bulblin_club"}, {"king_bulblin_club"}, {"king_bulblin_club"}, {"king_bulblin_club"}, {"king_bulblin_club"}}),
    STALHOUND("stalhound", 2.57f, 1.6f, 30, 5, 0.42, 0.5, 2.5, 1.51f, AttackKind.SLASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    SHADOW_BEAST("shadow_beast", 3.25f, 2.8f, 120, 9, 0.4, 1.2, 3.3, 2.24f, AttackKind.SLASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    REDEAD("redead", 0.77f, 2.2f, 50, 3, 0.2, 0.2, 1.9, 1.1f, AttackKind.SLASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    POE("poe", 1.3f, 2.2f, 30, 4, 0.2, 0.1, 14.0, 1.53f, AttackKind.SHOOT, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    TEKTITE("tektite", 0.97f, 1.4f, 24, 4, 0.3, 0.3, 2.3, 1.72f, AttackKind.SLASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    PEAHAT("peahat", 2.98f, 1.8f, 30, 5, 0.35, 0.3, 2.3, 1.75f, AttackKind.BITE, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    BUBBLE_FIRE("bubble_fire", 0.6f, 0.6f, 10, 3, 0.4, 0.1, 1.4, 1.0f, AttackKind.BITE, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    BUBBLE_ICE("bubble_ice", 0.6f, 0.6f, 10, 3, 0.4, 0.1, 1.4, 1.0f, AttackKind.BITE, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    BUBBLE_DARK("bubble_dark", 0.6f, 0.6f, 10, 3, 0.4, 0.1, 1.4, 1.0f, AttackKind.BITE, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    DODONGO("dodongo", 6.0f, 5.5f, 300, 12, 0.24, 2.0, 5.2, 3.67f, AttackKind.SMASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    HELMASAUR("helmasaur", 1.8f, 1.8f, 120, 8, 0.28, 1.0, 2.3, 1.8f, AttackKind.SMASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    DARK_NUT("dark_nut", 0.9f, 2.4f, 250, 12, 0.24, 2.0, 3.0, 1.4f, AttackKind.SMASH, 0.2f, false, new String[][]{{"dark_nut_sword"}, {"dark_nut_sword"}, {"dark_nut_sword"}, {"dark_nut_sword"}, {"dark_nut_sword"}}),
    DEATH_SWORD("death_sword", 2.38f, 5.5f, 700, 16, 0.3, 2.0, 4.6, 2.38f, AttackKind.SMASH, 0.3f, true, new String[][]{{"death_sword_blade"}, {"death_sword_blade"}, {"death_sword_blade"}, {"death_sword_blade"}, {"death_sword_blade"}}),
    ZANT("zant", 0.7f, 2.2f, 700, 12, 0.34, 1.0, 2.8, 1.3f, AttackKind.SLASH, 0f, true, new String[][]{{"zant_sword"}, {"zant_sword"}, {"zant_sword"}, {"zant_sword"}, {"zant_sword"}}),
    GANONDORF("ganondorf", 1.2f, 3.4f, 1200, 20, 0.28, 3.0, 4.2, 2.2f, AttackKind.SMASH, 0.25f, false, new String[][]{{"ganon_sword"}, {"ganon_sword"}, {"ganon_sword"}, {"ganon_sword"}, {"ganon_sword"}}),
    DIABABA("diababa", 4.05f, 7.5f, 600, 12, 0.14, 1.5, 16.0, 2.79f, AttackKind.SHOOT, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    ARGOROK("argorok", 6.0f, 13.01f, 1500, 16, 0.3, 2.5, 16.0, 4.84f, AttackKind.SHOOT, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    FYRUS("fyrus", 1.4f, 4.0f, 1000, 18, 0.22, 2.5, 4.0, 2.2f, AttackKind.SMASH, 0.2f, false, new String[][]{{"fyrus_blade"}, {"fyrus_blade"}, {"fyrus_blade"}, {"fyrus_blade"}, {"fyrus_blade"}}),
    ARMOGOHMA("armogohma", 5.09f, 5.5f, 900, 14, 0.22, 2.0, 16.0, 4.63f, AttackKind.SHOOT, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    AERALFOS("aeralfos", 2.99f, 2.59f, 70, 6, 0.3, 0.5, 2.4, 1.36f, AttackKind.SLASH, 0f, true, new String[][]{{"aeralfos_spear"}, {"aeralfos_spear"}, {"aeralfos_spear"}, {"aeralfos_spear"}, {"aeralfos_spear"}}),
    DINOLFOS("dinolfos", 1.69f, 2.6f, 80, 6, 0.34, 0.8, 2.3, 1.3f, AttackKind.SLASH, 0f, false, new String[][]{{"dinolfos_sword"}, {"dinolfos_sword"}, {"dinolfos_sword"}, {"dinolfos_sword"}, {"dinolfos_sword"}}),
    KARGAROK("kargarok", 3.72f, 1.8f, 40, 5, 0.4, 0.3, 2.1, 1.69f, AttackKind.BITE, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    HORRIBLIN("horriblin", 1.67f, 2.3f, 30, 3, 0.3, 0.4, 2.1, 1.11f, AttackKind.SLASH, 0f, false, new String[][]{
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
