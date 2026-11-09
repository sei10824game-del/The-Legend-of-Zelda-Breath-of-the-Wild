package com.hyrulecreatures;

/** Attack styles. windup = pose fully loaded, hits = damage ticks, total = length. */
public enum AttackKind {
    SMASH(14, 30, 17), SLASH(7, 18, 10), THRUST(10, 22, 13), SPIN(12, 38, 20), BITE(6, 18, 9), SHOOT(14, 32, 16),
    CHOP(9, 22, 12), LEAP(12, 34, 18), MULTI(8, 36, 12, 18, 24), CHARGE(14, 44, 20, 30), STOMP(16, 34, 20), BASH(8, 20, 11), BEAM(40, 70, 50);
    public final int windup, total, hit;
    public final int[] hits;
    AttackKind(int w, int t, int... h) { windup = w; total = t; hit = h[0]; hits = h; }
    public boolean hitsAt(int t) { for (int x : hits) if (x == t) return true; return false; }
    public int[] keys() { return this == MULTI ? new int[]{0, 8, 12, 15, 18, 21, 24, 36} : new int[]{0, windup, hit, total}; }
}
