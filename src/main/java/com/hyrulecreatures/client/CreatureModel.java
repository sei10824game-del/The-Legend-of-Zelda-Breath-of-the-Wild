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

/** One model class for every species; poses come from the spec, attack/down/idle animation is procedural. */
public class CreatureModel extends EntityModel<HyruleBiped> implements ArmedModel {
    private final ModelPart root;
    private final Map<String, ModelPart> p = new HashMap<>();
    private final float hunch;

    public CreatureModel(ModelPart root, Spec spec) {
        this.root = root; this.hunch = spec.hunch;
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

    // keyframe channels: rArmX rArmY rArmZ lArmX lArmY lArmZ bodyX bodyY headX headY rLegX lLegX
    private static final Map<AttackKind, float[][]> KF = new EnumMap<>(AttackKind.class);
    static {
        KF.put(AttackKind.SMASH, new float[][]{{0, -3.0f, 0.3f, 0}, {0, 0, 0, 0}, {0, -.25f, 0, 0}, {0, -3.0f, 0.3f, 0}, {0, 0, 0, 0}, {0, .25f, 0, 0},
                {0, -.35f, .5f, 0}, {0, 0, 0, 0}, {0, -.2f, .35f, 0}, {0, 0, 0, 0}, {0, .4f, -.35f, 0}, {0, -.4f, .35f, 0}});
        KF.put(AttackKind.SLASH, new float[][]{{0, -1.3f, -1.1f, 0}, {0, 1.4f, -1.2f, 0}, {0, 0, 0, 0}, {0, -.4f, -.2f, 0}, {0, .6f, -.4f, 0}, {0, .3f, .3f, 0},
                {0, .1f, .2f, 0}, {0, .7f, -.8f, 0}, {0, 0, 0, 0}, {0, .3f, -.3f, 0}, {0, .3f, -.3f, 0}, {0, -.3f, .3f, 0}});
        KF.put(AttackKind.THRUST, new float[][]{{0, -.7f, -1.55f, 0}, {0, -.5f, .1f, 0}, {0, .1f, 0, 0}, {0, -.9f, -1.45f, 0}, {0, .7f, .2f, 0}, {0, 0, 0, 0},
                {0, -.15f, .3f, 0}, {0, .5f, -.4f, 0}, {0, 0, .1f, 0}, {0, -.2f, .2f, 0}, {0, .6f, -.7f, 0}, {0, -.6f, .7f, 0}});
        KF.put(AttackKind.SPIN, new float[][]{{0, 0, 0, 0}, {0, 0, 0, 0}, {0, 1.45f, 1.45f, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, -1.45f, -1.45f, 0},
                {0, -.2f, .1f, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, .3f, .3f, 0}, {0, -.3f, -.3f, 0}});
        KF.put(AttackKind.BITE, new float[][]{{0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0},
                {0, -.7f, .9f, 0}, {0, 0, 0, 0}, {0, -.3f, .5f, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}});
    }

    private static final float[][] CAST = {{0, -2.8f, -2.4f, 0}, {0, 0, 0, 0}, {0, -.3f, -.3f, 0}, {0, -2.8f, -2.4f, 0}, {0, 0, 0, 0}, {0, .3f, .3f, 0},
            {0, -.45f, .3f, 0}, {0, 0, 0, 0}, {0, -.3f, .2f, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}};
    private static final float[][] BOW = {{0, -1.5f, -1.55f, 0}, {0, -.15f, -.15f, 0}, {0, 0, 0, 0}, {0, -1.5f, -1.5f, 0}, {0, .25f, .2f, 0}, {0, 0, 0, 0},
            {0, -.05f, .1f, 0}, {0, .3f, .25f, 0}, {0, 0, 0, 0}, {0, .1f, .1f, 0}, {0, .1f, .1f, 0}, {0, -.1f, -.1f, 0}};
    private static final float[][] THROW = {{0, -2.7f, -.4f, 0}, {0, 0, 0, 0}, {0, -.3f, .2f, 0}, {0, -.6f, -.2f, 0}, {0, 0, 0, 0}, {0, 0, 0, 0},
            {0, -.3f, .4f, 0}, {0, .4f, -.5f, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, .4f, -.4f, 0}, {0, -.4f, .4f, 0}};

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

        // ---- locomotion / idle
        if (head != null) { head.xRot += hpitch * rad - hunch; head.yRot += hyaw * rad; }
        if (!flier) {
            body.xRot += hunch;
            float g = Mth.cos(limb * .6662f) * 1.0f * amt, g2 = Mth.cos(limb * .6662f + Mth.PI) * 1.0f * amt;
            add("frontLeftLeg", g, 0, 0); add("backRightLeg", g, 0, 0); add("frontRightLeg", g2, 0, 0); add("backLeftLeg", g2, 0, 0);
            if (e.species == Species.CHUCHU) body.y -= Math.abs(Mth.sin(limb * .4f)) * 3 * amt;
            add("rightLeg", Mth.cos(limb * .6662f) * 1.4f * amt, 0, 0);
            add("leftLeg", Mth.cos(limb * .6662f + Mth.PI) * 1.4f * amt, 0, 0);
            boolean armed = !e.getMainHandItem().isEmpty();
            add("rightArm", (armed ? -.7f : 0) + Mth.cos(limb * .6662f + Mth.PI) * .7f * amt + Mth.sin(age * .09f) * .03f, 0, .06f);
            add("leftArm", (armed ? -.35f : 0) + Mth.cos(limb * .6662f) * .9f * amt - Mth.sin(age * .09f) * .03f, 0, -.06f);
            body.y += Mth.sin(age * .1f) * .3f;
        }
        add("tail1", 0, Mth.sin(age * .1f) * .15f + Mth.sin(limb * .6f) * .35f * amt, 0);
        add("tail2", 0, Mth.sin(age * .1f - .6f) * .2f + Mth.sin(limb * .6f - .8f) * .35f * amt, 0);
        add("tail3", 0, Mth.sin(age * .1f - 1.2f) * .25f + Mth.sin(limb * .6f - 1.6f) * .4f * amt, 0);
        add("earL", 0, 0, Mth.sin(age * .13f) * .06f);
        add("earR", 0, 0, -Mth.sin(age * .13f + 1) * .06f);
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
        if (k != null) {
            float t = e.atkTick() + pt;
            int[] T = {0, k.windup, k.hit, k.total};
            net.minecraft.world.item.Item held = e.getMainHandItem().getItem();
            float[][] c = k != AttackKind.SHOOT ? KF.get(k) : held instanceof HyruleBowItem ? BOW
                    : held != net.minecraft.world.item.Items.AIR ? THROW : CAST;
            float dir = k == AttackKind.SLASH && e.combo() % 2 == 1 ? -1 : 1;
            add("rightArm", key(t, T, c[0]), key(t, T, c[1]) * dir, key(t, T, c[2]));
            add("leftArm", key(t, T, c[3]), key(t, T, c[4]) * dir, key(t, T, c[5]));
            if (body != null) { body.xRot += key(t, T, c[6]); body.yRot += key(t, T, c[7]) * dir; }
            if (head != null) { head.xRot += key(t, T, c[8]); head.yRot += key(t, T, c[9]) * dir; }
            add("rightLeg", key(t, T, c[10]), 0, 0);
            add("leftLeg", key(t, T, c[11]), 0, 0);
            if (k == AttackKind.SHOOT) add("snout", key(t, T, new float[]{0, -.5f, .25f, 0}), 0, 0);
            if (k == AttackKind.BITE) { flap = 1.6f; add("jaw", key(t, T, new float[]{0, .7f, 0, 0}), 0, 0); }
            if (k == AttackKind.SLASH || k == AttackKind.SMASH) add("jaw", key(t, T, new float[]{0, .5f, .1f, 0}), 0, 0);
        }

        if (flier) {
            float f = Mth.sin(age * .9f * flap) * .9f;
            add("wingL", 0, 0, -f); add("wingR", 0, 0, f);
            body.y += Mth.sin(age * .3f) * .8f;
            add("rightArm", -.2f + Mth.sin(age * .1f) * .06f, 0, .15f); add("leftArm", -.2f - Mth.sin(age * .1f) * .06f, 0, -.15f);
            add("footL", .5f, 0, 0); add("footR", .5f, 0, 0);
        }

        // ---- knocked down: limbs flail, then recover
        int dl = e.downLeft();
        if (dl > 0) {
            float s = Math.min(1f, (dl - pt) / 12f), tw = Mth.sin(age * .4f) * .12f;
            add("rightArm", -.2f * s, 0, (.9f + tw) * s); add("leftArm", -.2f * s, 0, (-.9f - tw) * s);
            add("rightLeg", .1f * s, 0, .25f * s); add("leftLeg", .1f * s, 0, -.25f * s);
            if (head != null) head.xRot -= .3f * s;
            add("wingL", 0, 0, 1.2f * s); add("wingR", 0, 0, -1.2f * s);
        }
    }
}
