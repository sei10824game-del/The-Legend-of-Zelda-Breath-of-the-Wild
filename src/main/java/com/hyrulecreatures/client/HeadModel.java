package com.hyrulecreatures.client;

import com.hyrulecreatures.StalHead;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import java.util.*;
import net.minecraft.client.model.EntityModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.util.Mth;

/** Renders only the head part of a species model, lying on the ground and rolling. */
public class HeadModel extends EntityModel<StalHead> {
    private final ModelPart root, head;

    public HeadModel(ModelPart root, Spec spec) {
        this.root = root;
        Map<String, ModelPart> p = new HashMap<>();
        for (String n : spec.names()) { String par = spec.parentOf(n); p.put(n, (par == null ? root : p.get(par)).getChild(n)); }
        head = p.get("head");
        for (String n : spec.names()) { // hide everything except head and its descendants
            boolean keep = false; String q = n;
            while (q != null) { if (q.equals("head")) { keep = true; break; } q = spec.parentOf(q); }
            p.get(n).visible = keep;
        }
    }

    @Override public void setupAnim(StalHead e, float limb, float amt, float age, float yaw, float pitch) {
        head.resetPose();
        float hop = Math.abs(Mth.sin(age * .6f)) * (e.getDeltaMovement().horizontalDistanceSqr() > 1e-4 ? 3f : 0f);
        head.setPos(0, 24 - hop, 0); head.xRot = Mth.sin(age * .6f) * .25f; head.zRot = Mth.cos(age * .5f) * .2f; head.yRot = 0;
    }
    @Override public void renderToBuffer(PoseStack ps, VertexConsumer vc, int light, int overlay, float r, float g, float b, float a) {
        root.render(ps, vc, light, overlay, r, g, b, a);
    }
}
