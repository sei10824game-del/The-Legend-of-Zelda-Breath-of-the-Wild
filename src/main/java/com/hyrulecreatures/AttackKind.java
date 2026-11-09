package com.hyrulecreatures;

/** Attack styles. Ticks: windup (pose fully loaded), hit (damage frame), total. */
public enum AttackKind {
    SMASH(14, 17, 30), SLASH(7, 10, 18), THRUST(10, 13, 22), SPIN(12, 20, 38), BITE(6, 9, 18);
    public final int windup, hit, total;
    AttackKind(int w, int h, int t) { windup = w; hit = h; total = t; }
}
