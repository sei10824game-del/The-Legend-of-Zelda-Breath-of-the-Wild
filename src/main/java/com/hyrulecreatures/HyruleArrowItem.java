package com.hyrulecreatures;

import net.minecraft.world.effect.*;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.projectile.AbstractArrow;
import net.minecraft.world.entity.projectile.Arrow;
import net.minecraft.world.item.ArrowItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;

/** Fire / ice / shock arrows. */
public class HyruleArrowItem extends ArrowItem {
    private final int element;
    public HyruleArrowItem(int element) { super(new Item.Properties()); this.element = element; }
    @Override public AbstractArrow createArrow(Level l, ItemStack st, LivingEntity shooter) {
        Arrow a = new Arrow(l, shooter);
        switch (element) {
            case 1 -> a.setSecondsOnFire(100);
            case 2 -> a.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 100, 3));
            default -> a.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 100, 1));
        }
        return a;
    }
}
