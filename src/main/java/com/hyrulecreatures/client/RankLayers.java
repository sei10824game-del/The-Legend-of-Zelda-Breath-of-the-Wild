package com.hyrulecreatures.client;

import com.hyrulecreatures.*;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.entity.RenderLayerParent;
import net.minecraft.client.renderer.entity.layers.RenderLayer;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.resources.ResourceLocation;

/** Emissive glow (eyes, circuits, magma...) and battle-damage overlay. */
public final class RankLayers {
    public static class Glow extends RenderLayer<HyruleBiped, CreatureModel> {
        public Glow(RenderLayerParent<HyruleBiped, CreatureModel> p) { super(p); }
        @Override public void render(PoseStack ps, MultiBufferSource buf, int light, HyruleBiped e, float limb, float amt, float pt, float age, float yaw, float pitch) {
            if (e.isInvisible()) return;
            ResourceLocation t = new ResourceLocation(HyruleCreatures.ID, "textures/entity/" + e.species.id + "_" + Species.RANKS[e.rank()] + "_glow.png");
            getParentModel().renderToBuffer(ps, buf.getBuffer(RenderType.eyes(t)), 0xF000F0, OverlayTexture.NO_OVERLAY, 1, 1, 1, 1);
        }
    }

    public static class Damage extends RenderLayer<HyruleBiped, CreatureModel> {
        private static final ResourceLocation TEX = new ResourceLocation(HyruleCreatures.ID, "textures/entity/damage.png");
        public Damage(RenderLayerParent<HyruleBiped, CreatureModel> p) { super(p); }
        @Override public void render(PoseStack ps, MultiBufferSource buf, int light, HyruleBiped e, float limb, float amt, float pt, float age, float yaw, float pitch) {
            float frac = e.getHealth() / e.getMaxHealth();
            if (e.isInvisible() || frac >= 0.6f || e.getMaxHealth() <= 1) return;
            float a = Math.min(1f, (0.6f - frac) / 0.45f);
            getParentModel().renderToBuffer(ps, buf.getBuffer(RenderType.entityTranslucent(TEX)), light, OverlayTexture.NO_OVERLAY, 1, 1, 1, a);
        }
    }
}
