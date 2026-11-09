package com.hyrulecreatures;

public enum Species {
    //            id         w     h     hp  dmg  speed knock reach scale  attack            spin  flies  weapons per rank (red,blue,black,silver,gold)
    BOKOBLIN("bokoblin", 0.6f, 1.7f, 20, 2, 0.27, 0.4, 1.9, 1.0f, AttackKind.SMASH, 0f, false, new String[][]{
        {"boko_club", "boko_spear", "boko_bat", "boko_bow"}, {"spiked_boko_club", "spiked_boko_spear", "spiked_boko_bow"},
        {"dragonbone_boko_club", "dragonbone_boko_spear", "dragonbone_boko_bow"},
        {"dragonbone_boko_bow", "dragonbone_boko_spear", "knights_broadsword", "knights_bow"},
        {"royal_bow", "royal_broadsword", "royal_halberd"}}),
    MOBLIN("moblin", 1.0f, 2.6f, 50, 4, 0.24, 1.6, 2.6, 1.4f, AttackKind.SMASH, 0.25f, false, new String[][]{
        {"moblin_club"}, {"spiked_moblin_club"}, {"dragonbone_moblin_club"},
        {"dragonbone_moblin_club", "lynel_crusher"}, {"dragonbone_moblin_club", "savage_lynel_crusher"}}),
    LIZALFOS("lizalfos", 0.6f, 1.8f, 24, 3, 0.33, 0.5, 2.0, 1.0f, AttackKind.SLASH, 0f, false, new String[][]{
        {"lizal_boomerang"}, {"lizal_forked_boomerang"}, {"lizal_tri_boomerang"}, {"lizal_tri_boomerang"}, {"lizal_tri_boomerang"}}),
    KEESE("keese", 0.5f, 0.5f, 6, 2, 0.5, 0.1, 1.4, 1.0f, AttackKind.BITE, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    HINOX("hinox", 1.4f, 4.2f, 120, 8, 0.2, 2.5, 3.6, 2.2f, AttackKind.SMASH, 0.2f, false, new String[][]{
        {"moblin_club"}, {"spiked_moblin_club"}, {"dragonbone_moblin_club"}, {"lynel_crusher"}, {"savage_lynel_crusher"}}),
    TALUS("talus", 1.2f, 3.2f, 80, 7, 0.18, 2.0, 2.9, 1.8f, AttackKind.SMASH, 0.15f, false, new String[][]{{}, {}, {}, {}, {}}),
    GIBDO("gibdo", 0.6f, 1.8f, 30, 3, 0.25, 0.3, 1.9, 1.0f, AttackKind.SLASH, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    OCTOROK("octorok", 0.9f, 0.9f, 16, 3, 0.24, 0.2, 14, 1.0f, AttackKind.SHOOT, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    WIZZROBE("wizzrobe", 0.6f, 1.8f, 24, 4, 0.2, 0.1, 14, 1.0f, AttackKind.SHOOT, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    LYNEL("lynel", 1.4f, 3.0f, 120, 8, 0.3, 2.5, 3.4, 1.6f, AttackKind.SLASH, 0f, false, new String[][]{
        {"lynel_sword", "lynel_spear", "lynel_crusher", "lynel_bow"}, {"mighty_lynel_sword", "mighty_lynel_spear", "mighty_lynel_crusher", "mighty_lynel_bow"},
        {"savage_lynel_sword", "savage_lynel_spear", "savage_lynel_crusher", "savage_lynel_bow"},
        {"savage_lynel_sword", "savage_lynel_spear", "savage_lynel_crusher", "savage_lynel_bow"},
        {"savage_lynel_sword", "savage_lynel_spear", "savage_lynel_crusher", "savage_lynel_bow"}}),
    CHUCHU("chuchu", 0.9f, 0.9f, 12, 3, 0.2, 0.2, 1.8, 1.0f, AttackKind.BITE, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    GUARDIAN("guardian", 3.0f, 4.5f, 100, 10, 0.26, 1.0, 4.5, 2.4f, AttackKind.BEAM, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    DECAYED_GUARDIAN("decayed_guardian", 2.2f, 3.4f, 60, 6, 0.16, 0.5, 3.6, 1.8f, AttackKind.BEAM, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    GUARDIAN_TURRET("guardian_turret", 1.6f, 2.8f, 120, 10, 0.0, 0.0, 3.0, 1.7f, AttackKind.BEAM, 0f, false, new String[][]{{}, {}, {}, {}, {}}),
    GUARDIAN_SKYWATCHER("guardian_skywatcher", 1.6f, 1.6f, 50, 8, 0.3, 0.3, 3.0, 1.8f, AttackKind.BEAM, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    GUARDIAN_SCOUT_1("guardian_scout_1", 1.1f, 3.2f, 70, 5, 0.2, 0.5, 3.2, 1.7f, AttackKind.SLASH, 0f, false, new String[][]{
        {"guardian_sword"}, {"guardian_sword"}, {"guardian_sword"}, {"guardian_sword"}, {"guardian_sword"}}),
    GUARDIAN_SCOUT_2("guardian_scout_2", 1.1f, 3.2f, 100, 7, 0.2, 0.5, 3.4, 1.7f, AttackKind.SLASH, 0f, false, new String[][]{
        {"guardian_spear"}, {"guardian_spear"}, {"guardian_spear"}, {"guardian_spear"}, {"guardian_spear"}}),
    GUARDIAN_SCOUT_3("guardian_scout_3", 1.4f, 3.9f, 150, 10, 0.2, 1.2, 3.8, 2.0f, AttackKind.SMASH, 0.3f, false, new String[][]{
        {"guardian_sword_plus"}, {"guardian_sword_plus"}, {"guardian_sword_plus"}, {"guardian_sword_plus"}, {"guardian_sword_plus"}}),
    GUARDIAN_SCOUT_4("guardian_scout_4", 1.4f, 3.9f, 240, 12, 0.24, 1.5, 3.8, 2.0f, AttackKind.SLASH, 0f, false, new String[][]{
        {"guardian_sword"}, {"guardian_sword"}, {"guardian_sword"}, {"guardian_sword"}, {"guardian_sword"}}),
    STALKOBLIN("stalkoblin", 0.6f, 1.7f, 14, 2, 0.28, 0.3, 1.9, 1.0f, AttackKind.SMASH, 0f, false, new String[][]{
        {"boko_club", "boko_spear"}, {"spiked_boko_club", "spiked_boko_spear"}, {"dragonbone_boko_club"}, {"dragonbone_boko_spear"}, {"dragonbone_boko_club"}}),
    STALMOBLIN("stalmoblin", 1.0f, 2.6f, 35, 4, 0.25, 1.2, 2.6, 1.4f, AttackKind.SMASH, 0.2f, false, new String[][]{
        {"moblin_club"}, {"spiked_moblin_club"}, {"dragonbone_moblin_club"}, {"dragonbone_moblin_club"}, {"dragonbone_moblin_club"}}),
    STALIZALFOS("stalizalfos", 0.6f, 1.8f, 20, 3, 0.34, 0.4, 2.0, 1.0f, AttackKind.SLASH, 0f, false, new String[][]{
        {"lizal_boomerang"}, {"lizal_forked_boomerang"}, {"lizal_tri_boomerang"}, {"lizal_tri_boomerang"}, {"lizal_tri_boomerang"}}),
    YIGA_FOOTSOLDIER("yiga_footsoldier", 0.6f, 1.8f, 30, 3, 0.32, 0.3, 1.9, 1.0f, AttackKind.SLASH, 0f, false, new String[][]{
        {"yiga_blade", "yiga_bow"}, {"yiga_blade", "soldiers_bow"}, {"yiga_blade", "knights_broadsword"}, {"yiga_blade", "knights_bow"}, {"royal_broadsword", "royal_bow"}}),
    YIGA_BLADEMASTER("yiga_blademaster", 0.6f, 1.8f, 70, 6, 0.36, 0.5, 2.0, 1.1f, AttackKind.SLASH, 0f, false, new String[][]{
        {"yiga_blade"}, {"yiga_blade"}, {"knights_broadsword"}, {"royal_broadsword"}, {"royal_guards_sword"}}),
    SOLDIER_CONSTRUCT("soldier_construct", 0.8f, 2.2f, 60, 6, 0.22, 0.8, 2.3, 1.2f, AttackKind.SLASH, 0f, false, new String[][]{
        {"soldiers_broadsword"}, {"knights_broadsword"}, {"royal_broadsword"}, {"royal_guards_sword"}, {"royal_guards_sword"}}),
    CAPTAIN_CONSTRUCT("captain_construct", 1.2f, 3.4f, 160, 11, 0.22, 2.0, 3.4, 1.8f, AttackKind.SMASH, 0.2f, false, new String[][]{
        {"soldiers_claymore"}, {"knights_claymore"}, {"royal_claymore"}, {"royal_claymore"}, {"royal_claymore"}}),
    FROX("frox", 1.6f, 3.6f, 200, 12, 0.18, 3.0, 3.8, 2.0f, AttackKind.SMASH, 0.2f, false, new String[][]{{}, {}, {}, {}, {}}),
    PHANTOM_GANON("phantom_ganon", 0.7f, 2.0f, 150, 9, 0.3, 1.5, 2.6, 1.2f, AttackKind.SLASH, 0f, true, new String[][]{
        {"royal_guards_sword"}, {"royal_guards_sword"}, {"royal_claymore"}, {"royal_guards_sword"}, {"royal_claymore"}}),
    GLEEOK("gleeok", 1.6f, 2.4f, 300, 10, 0.25, 2.0, 16, 1.6f, AttackKind.SHOOT, 0f, true, new String[][]{{}, {}, {}, {}, {}}),
    HORRIBLIN("horriblin", 0.6f, 1.7f, 30, 3, 0.3, 0.4, 1.9, 1.0f, AttackKind.SLASH, 0f, false, new String[][]{
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

    public static final String[] RANKS = {"red", "blue", "black", "silver", "gold"};
    public static final double[] HP_MUL = {1, 1.5, 2.5, 4, 6};
    public static final double[] DMG_MUL = {1, 1.3, 1.8, 2.4, 3.2};
}
