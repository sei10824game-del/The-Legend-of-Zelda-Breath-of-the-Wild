package com.hyrulecreatures.client;

import com.hyrulecreatures.*;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.client.event.EntityRenderersEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

@Mod.EventBusSubscriber(modid = HyruleCreatures.ID, bus = Mod.EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
public class ClientSetup {
    @SubscribeEvent
    public static void layers(EntityRenderersEvent.RegisterLayerDefinitions e) {
        for (Species s : Species.values()) e.registerLayerDefinition(HyruleRenderer.layer(s), () -> Spec.get(s.id).layer());
    }
    @SubscribeEvent
    public static void renderers(EntityRenderersEvent.RegisterRenderers e) {
        e.registerEntityRenderer(ModRegistry.SHOT.get(), net.minecraft.client.renderer.entity.ThrownItemRenderer::new);
        ModRegistry.TYPES.forEach((s, t) -> e.registerEntityRenderer(t.get(), ctx -> new HyruleRenderer(ctx, s)));
    }
}
