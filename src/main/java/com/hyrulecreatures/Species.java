package com.hyrulecreatures;

public enum Species {
    //            id         w     h     hp  dmg  speed knock reach scale  attack            spin  flies  weapons per rank (red,blue,black,silver,gold)
    BOKOBLIN("bokoblin", 0.6f, 1.7f, 20, 2, 0.27, 0.4, 1.9, 1.0f, AttackKind.SMASH, 0f, false, new String[][]{
        {"boko_club", "boko_spear", "boko_bat"}, {"spiked_boko_club", "spiked_boko_spear", "boko_bat"},
        {"dragonbone_boko_club", "dragonbone_boko_spear", "spiked_boko_club"},
        {"dragonbone_boko_club", "dragonbone_boko_spear", "knights_broadsword"},
        {"dragonbone_boko_club", "royal_broadsword", "royal_halberd"}}),
    MOBLIN("moblin", 1.0f, 2.6f, 50, 4, 0.24, 1.6, 2.6, 1.4f, AttackKind.SMASH, 0.25f, false, new String[][]{
        {"moblin_club"}, {"spiked_moblin_club"}, {"dragonbone_moblin_club"},
        {"dragonbone_moblin_club", "lynel_crusher"}, {"dragonbone_moblin_club", "savage_lynel_crusher"}}),
    LIZALFOS("lizalfos", 0.6f, 1.8f, 24, 3, 0.33, 0.5, 2.0, 1.0f, AttackKind.SLASH, 0f, false, new String[][]{
        {"lizal_boomerang"}, {"lizal_forked_boomerang"}, {"lizal_tri_boomerang"}, {"lizal_tri_boomerang"}, {"lizal_tri_boomerang"}}),
    KEESE("keese", 0.5f, 0.5f, 6, 2, 0.5, 0.1, 1.4, 1.0f, AttackKind.BITE, 0f, true, new String[][]{{}, {}, {}, {}, {}});

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
