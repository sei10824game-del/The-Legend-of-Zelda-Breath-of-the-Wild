package com.hyrulecreatures;

import net.minecraft.world.entity.SpawnPlacements;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraftforge.event.entity.EntityAttributeCreationEvent;
import net.minecraftforge.event.entity.SpawnPlacementRegisterEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.minecraftforge.eventbus.api.IEventBus;

@Mod(HyruleCreatures.ID)
public class HyruleCreatures {
    public static final String ID = "hyrulecreatures";

    public HyruleCreatures() {
        IEventBus bus = FMLJavaModLoadingContext.get().getModEventBus();
        ModRegistry.ENTITIES.register(bus);
        ModRegistry.ITEMS.register(bus);
        ModRegistry.TABS.register(bus);
        bus.addListener((EntityAttributeCreationEvent e) ->
                ModRegistry.TYPES.forEach((s, t) -> e.put(t.get(), HyruleBiped.attributes(s).build())));
        bus.addListener((EntityAttributeCreationEvent e) -> e.put(ModRegistry.STAL_HEAD.get(),
                net.minecraft.world.entity.Mob.createMobAttributes().add(net.minecraft.world.entity.ai.attributes.Attributes.MAX_HEALTH, 1)
                        .add(net.minecraft.world.entity.ai.attributes.Attributes.MOVEMENT_SPEED, 0.3).add(net.minecraft.world.entity.ai.attributes.Attributes.FOLLOW_RANGE, 48).build()));
        bus.addListener((SpawnPlacementRegisterEvent e) -> ModRegistry.TYPES.forEach((s, t) -> e.register(t.get(),
                s.flies ? SpawnPlacements.Type.NO_RESTRICTIONS : SpawnPlacements.Type.ON_GROUND,
                s.flies ? Heightmap.Types.MOTION_BLOCKING : Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
                Monster::checkMonsterSpawnRules, SpawnPlacementRegisterEvent.Operation.OR)));
        net.minecraftforge.common.MinecraftForge.EVENT_BUS.register(new FactionEvents());
    }
}
