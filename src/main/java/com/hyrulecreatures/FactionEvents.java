package com.hyrulecreatures;

import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.PathfinderMob;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.*;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraftforge.event.entity.EntityJoinLevelEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;

/** Every non-mod mob becomes hostile to our creatures (and fights back with melee if it has no attack goal). */
public class FactionEvents {
    @SubscribeEvent
    public void onJoin(EntityJoinLevelEvent e) {
        if (e.getLevel().isClientSide() || !(e.getEntity() instanceof Mob m) || m instanceof HyruleMob) return;
        m.targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(m, HyruleMob.class, 10, true, false, x -> true));
        if (m instanceof PathfinderMob p && p.getAttributes().hasAttribute(Attributes.ATTACK_DAMAGE)
                && p.goalSelector.getAvailableGoals().stream().noneMatch(w -> {
                    Goal g = w.getGoal();
                    return g instanceof MeleeAttackGoal || g instanceof RangedAttackGoal || g instanceof RangedBowAttackGoal<?>
                            || g instanceof RangedCrossbowAttackGoal<?> || g instanceof SwellGoal;
                }))
            p.goalSelector.addGoal(3, new MeleeAttackGoal(p, 1.1, true));
    }
}
