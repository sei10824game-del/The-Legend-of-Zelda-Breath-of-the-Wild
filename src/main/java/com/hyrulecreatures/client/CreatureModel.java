package com.hyrulecreatures.client;

import com.hyrulecreatures.*;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import java.util.*;
import net.minecraft.client.model.ArmedModel;
import net.minecraft.client.model.EntityModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.HumanoidArm;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Items;

/** One model for every species. Hunched stance + exaggerated keyframed attacks (rigid lean about the hip). */
public class CreatureModel extends EntityModel<HyruleBiped> implements ArmedModel {
    private final ModelPart root;
    private final Map<String, ModelPart> p = new HashMap<>();
    private final float hunch, hipY;

    public CreatureModel(ModelPart root, Spec spec) {
        this.root = root; this.hunch = spec.hunch; this.hipY = spec.hipY();
        for (String n : spec.names()) {
            String par = spec.parentOf(n);
            p.put(n, (par == null ? root : p.get(par)).getChild(n));
        }
    }

    @Override public void translateToHand(HumanoidArm arm, PoseStack ps) {
        p.getOrDefault(arm == HumanoidArm.RIGHT ? "rightArm" : "leftArm", p.get("body")).translateAndRotate(ps);
    }
    @Override public void renderToBuffer(PoseStack ps, VertexConsumer vc, int light, int overlay, float r, float g, float b, float a) {
        root.render(ps, vc, light, overlay, r, g, b, a);
    }

    private void add(String n, float x, float y, float z) {
        ModelPart m = p.get(n);
        if (m != null) { m.xRot += x; m.yRot += y; m.zRot += z; }
    }

    /** Rotate torso+head+arms rigidly about the hip (forward lean th, twist psi) and sink them by dip px. */
    private void lean(float th, float psi, float dip) {
        float ct = Mth.cos(th), st = Mth.sin(th), cp = Mth.cos(psi), sp = Mth.sin(psi);
        for (String n : new String[]{"body", "head", "rightArm", "leftArm"}) {
            ModelPart m = p.get(n);
            if (m == null) continue;
            float y = m.y - hipY, z = m.z, x = m.x;
            float y1 = y * ct - z * st, z1 = y * st + z * ct;
            m.x = x * cp + z1 * sp; m.z = -x * sp + z1 * cp; m.y = y1 + hipY + dip;
            m.xRot += th; m.yRot += psi;
        }
    }

    // keyframe channels
    static final int RAX = 0, RAY = 1, RAZ = 2, LAX = 3, LAY = 4, LAZ = 5, BX = 6, BY = 7, HX = 8, HY = 9, RL = 10, LL = 11, DIP = 12, N = 13;
    private static final Map<AttackKind, float[][]> KF = new EnumMap<>(AttackKind.class);
    private static float[] f(float... v) { return v; }
    private static float[] neg(float[] v) { float[] o = v.clone(); for (int i = 0; i < o.length; i++) o[i] = -o[i]; return o; }
    private static float[][] mk(int n, Object... kv) {
        float[][] a = new float[N][n];
        for (int i = 0; i < kv.length; i += 2) a[(Integer) kv[i]] = (float[]) kv[i + 1];
        return a;
    }
    private static final float[][] CAST = mk(4, RAX, f(0, -2.8f, -2.4f, 0), RAZ, f(0, 0, 0, 0), LAX, f(0, -2.8f, -2.4f, 0), LAZ, f(0, .3f, .3f, 0), BX, f(0, -.5f, .35f, 0), HX, f(0, -.3f, .2f, 0), DIP, f(0, -1, 1, 0));
    private static final float[][] BOW = mk(4, RAX, f(0, -1.5f, -1.55f, 0), RAY, f(0, -.15f, -.15f, 0), LAX, f(0, -1.5f, -1.5f, 0), LAY, f(0, .25f, .2f, 0),
            BX, f(0, -.05f, .1f, 0), BY, f(0, .3f, .25f, 0), HY, f(0, .1f, .1f, 0), RL, f(0, .1f, .1f, 0), LL, f(0, -.1f, -.1f, 0));
    private static final float[][] THROW = mk(4, RAX, f(0, -2.9f, -.4f, 0), RAZ, f(0, -.3f, .2f, 0), LAX, f(0, -.8f, -.2f, 0), BX, f(0, -.5f, .6f, 0),
            BY, f(0, .6f, -.8f, 0), RL, f(0, .5f, -.5f, 0), LL, f(0, -.5f, .5f, 0), DIP, f(0, 1, 3, 0));
    static {
        KF.put(AttackKind.SMASH, mk(4, RAX, f(0, -3.4f, .6f, 0), RAZ, f(0, -.3f, 0, 0), LAX, f(0, -3.4f, .6f, 0), LAZ, f(0, .3f, 0, 0),
                BX, f(0, -.8f, .95f, 0), HX, f(0, -.4f, .5f, 0), RL, f(0, .7f, -.7f, 0), LL, f(0, -.7f, .7f, 0), DIP, f(0, -1, 3.5f, 0)));
        KF.put(AttackKind.CHOP, mk(4, RAX, f(0, -2.9f, .3f, 0), RAZ, f(0, -.25f, .1f, 0), LAX, f(0, .6f, -.5f, 0), LAZ, f(0, -.5f, -.3f, 0),
                BX, f(0, -.5f, .7f, 0), BY, f(0, .3f, -.3f, 0), HX, f(0, -.3f, .4f, 0), RL, f(0, .5f, -.5f, 0), LL, f(0, -.5f, .5f, 0), DIP, f(0, -.5f, 2.5f, 0)));
        KF.put(AttackKind.SLASH, mk(4, RAX, f(0, -1.5f, -1.2f, 0), RAY, f(0, 1.9f, -1.7f, 0), RAZ, f(0, .3f, -.2f, 0), LAX, f(0, -.5f, -.3f, 0), LAY, f(0, .9f, -.6f, 0),
                LAZ, f(0, .6f, .6f, 0), BX, f(0, .25f, .5f, 0), BY, f(0, 1.1f, -1.3f, 0), HY, f(0, .5f, -.5f, 0), RL, f(0, .5f, -.5f, 0), LL, f(0, -.5f, .5f, 0), DIP, f(0, 1, 2, 0)));
        KF.put(AttackKind.THRUST, mk(4, RAX, f(0, -.8f, -1.55f, 0), RAY, f(0, -.7f, .2f, 0), LAX, f(0, -1, -1.5f, 0), LAY, f(0, .7f, .3f, 0),
                BX, f(0, -.3f, .65f, 0), BY, f(0, .8f, -.7f, 0), HX, f(0, 0, .2f, 0), RL, f(0, .9f, -1f, 0), LL, f(0, -.9f, 1f, 0), DIP, f(0, 1.5f, 2.5f, 0)));
        KF.put(AttackKind.SPIN, mk(4, RAX, f(0, -.4f, -.4f, 0), RAZ, f(0, 1.45f, 1.45f, 0), LAX, f(0, -.4f, -.4f, 0), LAZ, f(0, -1.45f, -1.45f, 0),
                BX, f(0, -.5f, .2f, 0), RL, f(0, .5f, .5f, 0), LL, f(0, -.5f, -.5f, 0), DIP, f(0, 2, 2, 0)));
        KF.put(AttackKind.BEAM, mk(4, BX, f(0, -.25f, .4f, 0), HX, f(0, -.2f, .3f, 0), DIP, f(0, -1.5f, 2, 0)));
        KF.put(AttackKind.BITE, mk(4, BX, f(0, -.7f, .9f, 0), HX, f(0, -.3f, .5f, 0)));
        KF.put(AttackKind.LEAP, mk(4, RAX, f(0, -2.8f, .4f, 0), RAZ, f(0, -.3f, 0, 0), LAX, f(0, -1f, -.3f, 0), BX, f(0, .55f, .3f, 0), HX, f(0, .3f, .2f, 0),
                RL, f(0, 1f, -.6f, 0), LL, f(0, 1f, .8f, 0), DIP, f(0, 4.5f, -2, 0)));
        KF.put(AttackKind.MULTI, mk(8, RAX, f(0, -.6f, -1.55f, -.6f, -1.55f, -.6f, -1.55f, 0), LAX, f(0, -.8f, -1.45f, -.8f, -1.45f, -.8f, -1.45f, 0),
                LAY, f(0, .7f, .3f, .7f, .3f, .7f, .3f, 0), BX, f(0, .5f, .9f, .5f, .9f, .5f, .9f, 0), BY, f(0, .6f, -.4f, .6f, -.4f, .6f, -.4f, 0),
                HX, f(0, .3f, .4f, .3f, .4f, .3f, .4f, 0), RL, f(0, .9f, -.9f, .9f, -.9f, .9f, -.9f, 0), LL, f(0, -.9f, .9f, -.9f, .9f, -.9f, .9f, 0),
                DIP, f(0, 3, 3, 3, 3, 3, 3, 0)));
        KF.put(AttackKind.CHARGE, mk(4, RAX, f(0, .8f, 1f, 0), RAZ, f(0, .5f, .6f, 0), LAX, f(0, .8f, 1f, 0), LAZ, f(0, -.5f, -.6f, 0),
                BX, f(0, .9f, 1f, 0), HX, f(0, .5f, .4f, 0), DIP, f(0, 3, 2, 0)));
        KF.put(AttackKind.STOMP, mk(4, RAX, f(0, -1.5f, .3f, 0), RAZ, f(0, .9f, 0, 0), LAX, f(0, -1.5f, .3f, 0), LAZ, f(0, -.9f, 0, 0),
                BX, f(0, -.5f, .7f, 0), HX, f(0, -.3f, .4f, 0), RL, f(0, -1.6f, .3f, 0), DIP, f(0, -2, 4, 0)));
        KF.put(AttackKind.BASH, mk(4, RAX, f(0, -.9f, -.5f, 0), LAX, f(0, -.6f, -1.6f, 0), LAY, f(0, -.5f, .2f, 0), LAZ, f(0, -.2f, -.4f, 0),
                BX, f(0, -.1f, .4f, 0), BY, f(0, .5f, -.5f, 0), RL, f(0, .4f, -.5f, 0), LL, f(0, -.4f, .5f, 0), DIP, f(0, 1, 2, 0)));
    }

    static float key(float t, int[] T, float[] V) {
        if (t <= T[0]) return V[0];
        for (int i = 0; i < T.length - 1; i++) if (t < T[i + 1]) {
            float u = (t - T[i]) / (T[i + 1] - T[i]);
            u = i == 0 ? 1 - (1 - u) * (1 - u) : i == 1 ? u * u * u : u * u * (3 - 2 * u);
            return V[i] + (V[i + 1] - V[i]) * u;
        }
        return V[V.length - 1];
    }

    @Override public void setupAnim(HyruleBiped e, float limb, float amt, float age, float hyaw, float hpitch) {
        root.getAllParts().forEach(ModelPart::resetPose);
        float pt = age - e.tickCount, rad = Mth.DEG_TO_RAD;
        ModelPart head = p.get("head"), body = p.get("body");
        boolean flier = e.species.flies;
        if (head != null) head.visible = !(e.species.isStal() && e.headless());
        float lean = hunch, twist = 0, dip = 0;

        if (head != null) { head.xRot += hpitch * rad - hunch * .75f; head.yRot += hyaw * rad; }
        if (!flier) {
            float c = limb * .6662f;
            add("rightLeg", Mth.cos(c) * 1.4f * amt, 0, .1f * hunch); add("leftLeg", Mth.cos(c + Mth.PI) * 1.4f * amt, 0, -.1f * hunch);
            boolean armed = !e.getMainHandItem().isEmpty();
            add("rightArm", (armed ? -.9f : -.15f) + Mth.cos(c + Mth.PI) * .8f * amt + Mth.sin(age * .09f) * .05f, 0, .1f);
            add("leftArm", (armed ? -.4f : -.15f) + Mth.cos(c) * 1.0f * amt - Mth.sin(age * .09f) * .05f, 0, -.1f);
            dip += Math.abs(Mth.sin(c)) * 1.2f * amt + Mth.sin(age * .1f) * .3f; // plodding bob
            float g = Mth.cos(c) * amt, g2 = Mth.cos(c + Mth.PI) * amt;
            add("frontLeftLeg", g, 0, 0); add("backRightLeg", g, 0, 0); add("frontRightLeg", g2, 0, 0); add("backLeftLeg", g2, 0, 0);
            if (e.species == Species.CHUCHU) body.y -= Math.abs(Mth.sin(limb * .4f)) * 3 * amt;
        }
        add("tail1", 0, Mth.sin(age * .1f) * .15f + Mth.sin(limb * .6f) * .35f * amt, 0);
        add("tail2", 0, Mth.sin(age * .1f - .6f) * .2f + Mth.sin(limb * .6f - .8f) * .35f * amt, 0);
        add("tail3", 0, Mth.sin(age * .1f - 1.2f) * .25f + Mth.sin(limb * .6f - 1.6f) * .4f * amt, 0);
        add("earL", 0, 0, Mth.sin(age * .13f) * .08f + amt * .15f);
        add("earR", 0, 0, -Mth.sin(age * .13f + 1) * .08f - amt * .15f);
        add("jaw", Mth.sin(age * .07f) * .03f + 0.02f, 0, 0);

        AttackKind k = e.atkKind();
        if (e.species == Species.CHUCHU) { // squash & stretch instead of limbs
            float sq = 1 + Mth.sin(age * .15f) * .05f, sy = sq, sxz = 2 - sq;
            if (k != null) {
                float t = e.atkTick() + pt; int[] T = {0, k.windup, k.hit, k.total};
                sy = key(t, T, new float[]{1, .6f, 1.35f, 1}); sxz = key(t, T, new float[]{1, 1.3f, .8f, 1});
            }
            if (e.downLeft() > 0) { sy = .55f; sxz = 1.3f; }
            body.xScale = sxz; body.zScale = sxz; body.yScale = sy;
            return;
        }

        float flap = 1f;
        if (e.isGuard() && k == null && e.downLeft() == 0) { // shield up
            add("leftArm", -1.2f, .55f, -.35f); lean += .1f; dip += 1f;
        }
        if (k != null) {
            float t = e.atkTick() + pt;
            int[] T = k.keys();
            Item held = e.getMainHandItem().getItem();
            float[][] c = k == AttackKind.AREA ? CAST : k != AttackKind.SHOOT ? KF.get(k) : held instanceof HyruleBowItem ? BOW : held != Items.AIR ? THROW : CAST;
            float dir = k == AttackKind.SLASH && e.combo() % 2 == 1 ? -1 : 1;
            add("rightArm", key(t, T, c[RAX]), key(t, T, c[RAY]) * dir, key(t, T, c[RAZ]));
            add("leftArm", key(t, T, c[LAX]), key(t, T, c[LAY]) * dir, key(t, T, c[LAZ]));
            lean += key(t, T, c[BX]) * .5f; twist += key(t, T, c[BY]) * dir * .6f; dip += key(t, T, c[DIP]) * .5f;
            if (head != null) { head.xRot += key(t, T, c[HX]); head.yRot += key(t, T, c[HY]) * dir; }
            add("rightLeg", key(t, T, c[RL]), 0, 0); add("leftLeg", key(t, T, c[LL]), 0, 0);
            if (k == AttackKind.CHARGE && t > k.windup) { // gallop
                if (p.get("rightLeg") != null) { p.get("rightLeg").xRot = Mth.sin(t * .9f) * 1.2f; p.get("leftLeg").xRot = -Mth.sin(t * .9f) * 1.2f; }
                add("frontLeftLeg", Mth.sin(t * .9f) * 1.0f, 0, 0); add("backRightLeg", Mth.sin(t * .9f) * 1.0f, 0, 0);
                add("frontRightLeg", -Mth.sin(t * .9f) * 1.0f, 0, 0); add("backLeftLeg", -Mth.sin(t * .9f) * 1.0f, 0, 0);
            }
            if (k == AttackKind.BITE) { flap = 1.6f; add("jaw", key(t, T, new float[]{0, .7f, 0, 0}), 0, 0); }
            if (k == AttackKind.SLASH || k == AttackKind.SMASH || k == AttackKind.CHOP || k == AttackKind.CHARGE)
                add("jaw", key(t, T, new float[]{0, .6f, .1f, 0}), 0, 0);
            if (k == AttackKind.SHOOT) add("snout", key(t, T, new float[]{0, -.5f, .25f, 0}), 0, 0);
        }

        if (p.containsKey("leg0")) { // 8 spider legs: gait + hide destroyed ones
            for (int i = 0; i < 8; i++) {
                ModelPart leg = p.get("leg" + i);
                if (leg == null) continue;
                boolean gone = (e.aux() >> i & 1) != 0;
                leg.visible = !gone; p.get("leg" + i + "b").visible = !gone;
                int nl = p.containsKey("leg4") ? 8 : 4; float a = i * 2 * Mth.PI / nl + (nl == 8 ? Mth.PI / 8 : Mth.PI / 4), dx = Mth.cos(a), dz = Mth.sin(a);
                float lift = Mth.cos(limb * .6662f + (i % 2) * Mth.PI) * amt * .6f + (k == AttackKind.BEAM ? -.15f : 0);
                add("leg" + i, lift * dz, 0, -lift * dx);
            }
            if (k == AttackKind.BEAM) add("crest", 0, (e.atkTick() + pt) * .5f, 0);
        }
        if (flier) {
            float fl = Mth.sin(age * .9f * flap) * .9f;
            add("wingL", 0, 0, -fl); add("wingR", 0, 0, fl);
            dip += Mth.sin(age * .3f) * .8f;
            add("rightArm", -.2f + Mth.sin(age * .1f) * .06f, 0, .15f); add("leftArm", -.2f - Mth.sin(age * .1f) * .06f, 0, -.15f);
            add("footL", .5f, 0, 0); add("footR", .5f, 0, 0);
        }

        // knocked down: limbs flail, then recover
        int dl = e.downLeft();
        if (dl > 0) {
            float s = Math.min(1f, (dl - pt) / 12f), tw = Mth.sin(age * .4f) * .12f;
            add("rightArm", -.2f * s, 0, (.9f + tw) * s); add("leftArm", -.2f * s, 0, (-.9f - tw) * s);
            add("rightLeg", .1f * s, 0, .25f * s); add("leftLeg", .1f * s, 0, -.25f * s);
            if (head != null) head.xRot -= .3f * s;
            add("wingL", 0, 0, 1.2f * s); add("wingR", 0, 0, -1.2f * s);
            lean = 0; dip = 0; twist = 0;
        }
        lean(Mth.clamp(lean, -.6f, 1.05f), twist, Math.min(dip, 3f));
    }
}
