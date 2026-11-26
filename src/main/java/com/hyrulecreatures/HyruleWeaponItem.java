package com.hyrulecreatures;

import net.minecraft.world.item.*;
import net.minecraft.world.item.crafting.Ingredient;

public class HyruleWeaponItem extends SwordItem {
    public enum Style { ONE, TWO, SPEAR }
    public final AttackKind attack;
    public final Style style;
    public final int element; // 0 none, 1 fire, 2 ice, 3 shock

    public HyruleWeaponItem(int dmg, int durability, float speed, AttackKind attack, Style style) { this(dmg, durability, speed, attack, style, 0); }

    public HyruleWeaponItem(int dmg, int durability, float speed, AttackKind attack, Style style, int element) {
        super(new Tier() {
            public int getUses() { return durability; }
            public float getSpeed() { return 1; }
            public float getAttackDamageBonus() { return 0; }
            public int getLevel() { return 2; }
            public int getEnchantmentValue() { return 10; }
            public Ingredient getRepairIngredient() { return Ingredient.EMPTY; }
        }, dmg, speed, new Item.Properties());
        this.attack = attack; this.style = style; this.element = element;
    }

    @Override public boolean hurtEnemy(net.minecraft.world.item.ItemStack st, net.minecraft.world.entity.LivingEntity target, net.minecraft.world.entity.LivingEntity user) {
        switch (element) {
            case 1 -> target.setSecondsOnFire(5);
            case 2 -> { target.setTicksFrozen(target.getTicksRequiredToFreeze() + 120); target.addEffect(new net.minecraft.world.effect.MobEffectInstance(net.minecraft.world.effect.MobEffects.MOVEMENT_SLOWDOWN, 80, 2)); }
            case 3 -> target.addEffect(new net.minecraft.world.effect.MobEffectInstance(net.minecraft.world.effect.MobEffects.WEAKNESS, 100, 1));
            default -> {}
        }
        var key = net.minecraftforge.registries.ForgeRegistries.ITEMS.getKey(this);
        if (key != null && key.getPath().startsWith("zonai") && !target.level().isClientSide) { // Zonai tech: armour-piercing pulse
            target.hurt(target.damageSources().magic(), 2f); target.invulnerableTime = 0;
            ((net.minecraft.server.level.ServerLevel) target.level()).sendParticles(net.minecraft.core.particles.ParticleTypes.ELECTRIC_SPARK, target.getX(), target.getY() + target.getBbHeight() * 0.6, target.getZ(), 8, 0.3, 0.3, 0.3, 0.1);
        }
        return super.hurtEnemy(st, target, user);
    }
}
