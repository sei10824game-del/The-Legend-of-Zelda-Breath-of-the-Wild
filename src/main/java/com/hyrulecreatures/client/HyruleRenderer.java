package com.hyrulecreatures.client;

import com.hyrulecreatures.*;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.math.Axis;
import net.minecraft.client.model.geom.ModelLayerLocation;
import net.minecraft.client.renderer.entity.*;
import net.minecraft.client.renderer.entity.layers.ItemInHandLayer;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.Mth;

public class HyruleRenderer extends MobRenderer<HyruleBiped, CreatureModel> {
    private final Species species;
    private final boolean side;

    public static ModelLayerLocation layer(Species s) {
        return new ModelLayerLocation(new ResourceLocation(HyruleCreatures.ID, s.id), "main");
    }

    public HyruleRenderer(EntityRendererProvider.Context ctx, Species s) {
        super(ctx, new CreatureModel(ctx.bakeLayer(layer(s)), Spec.get(s.id)), 0.4f * s.scale);
        species = s; side = Spec.get(s.id).names().contains("frontLeftLeg") || Spec.get(s.id).names().contains("leg0");
        addLayer(new RankLayers.Glow(this)); addLayer(new RankLayers.Damage(this));
        if (Spec.get(s.id).names().contains("rightArm")) addLayer(new ItemInHandLayer<>(this, ctx.getItemInHandRenderer()));
    }

    @Override public ResourceLocation getTextureLocation(HyruleBiped e) {
        return new ResourceLocation(HyruleCreatures.ID, "textures/entity/" + species.id + "_" + Species.RANKS[e.rank()] + ".png");
    }

    @Override protected void scale(HyruleBiped e, PoseStack ps, float pt) { float rise = e.tickCount < 24 ? 0.4f + 0.6f * (1 - (1 - e.tickCount / 24f) * (1 - e.tickCount / 24f)) : 1f; // summon: grows out of the ground
        float k = species.scale * (e.isMini() ? 0.55f : 1f) * rise; ps.scale(k, k, k); }

    @Override protected float getWhiteOverlayProgress(HyruleBiped e, float pt) { // flash just before a heavy attack lands
        AttackKind k = e.atkKind();
        if (k == null || !(k == AttackKind.SMASH || k == AttackKind.SPIN || k == AttackKind.STOMP || k == AttackKind.AREA || k == AttackKind.BEAM || k == AttackKind.CHARGE || k == AttackKind.LEAP)) return 0;
        float t = e.atkTick() + pt, w = k.windup;
        return t >= w - 6 && t <= w + 1 ? 0.55f * Math.min(1f, (t - (w - 6)) / 6f) : 0;
    }

    @Override protected net.minecraft.client.renderer.RenderType getRenderType(HyruleBiped e, boolean vis, boolean invisToPlayer, boolean glowing) {
        switch (species) {
            case CHUCHU, POE, BUBBLE_FIRE, BUBBLE_ICE, BUBBLE_DARK: return net.minecraft.client.renderer.RenderType.entityTranslucent(getTextureLocation(e));
            default: return super.getRenderType(e, vis, invisToPlayer, glowing);
        }
    }

    @Override protected void setupRotations(HyruleBiped e, PoseStack ps, float age, float yaw, float pt) {
        super.setupRotations(e, ps, age, yaw, pt);
        int dl = e.downLeft();
        if (dl > 0) { // fall onto back, stay, get up
            float left = dl - pt;
            float dp = Mth.clamp(Math.min((HyruleMob.DOWN_TIME - left) / 6f, left / 12f), 0, 1);
            dp = dp * dp * (3 - 2 * dp);
            ps.translate(0, 0.22 * dp * species.scale, 0);
            ps.mulPose(side ? Axis.ZP.rotationDegrees(90 * dp) : Axis.XP.rotationDegrees(-90 * dp));
        }
        AttackKind k = e.atkKind();
        if (k == AttackKind.SPIN) {
            float t = (e.atkTick() + pt - k.windup) / (k.total - 6 - k.windup);
            t = Mth.clamp(t, 0, 1);
            ps.mulPose(Axis.YP.rotationDegrees(360 * t * t * (3 - 2 * t)));
        }
    }
}
