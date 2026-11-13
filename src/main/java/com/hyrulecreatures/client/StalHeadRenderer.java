package com.hyrulecreatures.client;

import com.hyrulecreatures.*;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.entity.*;
import net.minecraft.resources.ResourceLocation;

public class StalHeadRenderer extends MobRenderer<StalHead, HeadModel> {
    private final Map3 models = new Map3();
    static class Map3 { HeadModel[] m = new HeadModel[Species.values().length]; }

    public StalHeadRenderer(EntityRendererProvider.Context ctx) {
        super(ctx, new HeadModel(ctx.bakeLayer(HyruleRenderer.layer(Species.STALKOBLIN)), Spec.get("stalkoblin")), 0.3f);
        for (Species s : new Species[]{Species.STALKOBLIN, Species.STALMOBLIN, Species.STALIZALFOS})
            models.m[s.ordinal()] = new HeadModel(ctx.bakeLayer(HyruleRenderer.layer(s)), Spec.get(s.id));
    }

    @Override public void render(StalHead e, float yaw, float pt, PoseStack ps, MultiBufferSource buf, int light) {
        HeadModel m = models.m[e.species().ordinal()];
        if (m != null) this.model = m;
        super.render(e, yaw, pt, ps, buf, light);
    }
    @Override protected void scale(StalHead e, PoseStack ps, float pt) { float k = e.species().scale; ps.scale(k, k, k); }
    @Override public ResourceLocation getTextureLocation(StalHead e) {
        return new ResourceLocation(HyruleCreatures.ID, "textures/entity/" + e.species().id + "_" + Species.RANKS[e.rank()] + ".png");
    }
}
