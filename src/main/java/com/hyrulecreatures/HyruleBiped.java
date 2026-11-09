package com.hyrulecreatures;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.DifficultyInstance;
import net.minecraft.world.entity.*;
import net.minecraft.world.entity.ai.attributes.*;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.item.ItemStack;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.Level;
import net.minecraftforge.registries.ForgeRegistries;
import javax.annotation.Nullable;

/** Data-driven creature (Bokoblin, Moblin, Lizalfos, ...). */
public class HyruleBiped extends HyruleMob {
    public final Species species;
    private static final int[] RANK_WEIGHT = {50, 28, 14, 7, 1};

    public HyruleBiped(EntityType<? extends HyruleBiped> t, Level l, Species s) { super(t, l); species = s; }

    public static AttributeSupplier.Builder attributes(Species s) {
        return Monster.createMonsterAttributes().add(Attributes.MAX_HEALTH, s.hp).add(Attributes.ATTACK_DAMAGE, s.dmg)
                .add(Attributes.MOVEMENT_SPEED, s.speed).add(Attributes.ATTACK_KNOCKBACK, s.knock)
                .add(Attributes.FOLLOW_RANGE, 28).add(Attributes.FLYING_SPEED, s.speed).add(Attributes.KNOCKBACK_RESISTANCE, s.scale > 1.2 ? 0.5 : 0);
    }

    @Override public AttackKind defaultAttack() { return species.attack; }
    @Override public double reach() { return species.reach + (getMainHandItem().getItem() instanceof HyruleWeaponItem w && w.attack == AttackKind.THRUST ? 0.6 : 0); }
    @Override protected float spinChance() { return species.spin; }

    private static boolean isBoomerang(ItemStack s) { return ForgeRegistries.ITEMS.getKey(s.getItem()).getPath().contains("boomerang"); }
    @Override protected boolean ranged() { return getMainHandItem().getItem() instanceof HyruleBowItem || species.attack == AttackKind.SHOOT; }
    @Override protected double engageRange() {
        ItemStack h = getMainHandItem();
        return h.getItem() instanceof HyruleBowItem ? 14 : isBoomerang(h) ? 9 : reach();
    }

    @Override protected AttackKind chooseAttack() {
        ItemStack h = getMainHandItem(); LivingEntity t = getTarget();
        double d = t == null ? 0 : distanceTo(t);
        if (h.getItem() instanceof HyruleBowItem) return d <= reach() + 0.3 ? AttackKind.SLASH : AttackKind.SHOOT;
        if (isBoomerang(h)) return d > 4 ? (random.nextFloat() < 0.6f ? AttackKind.SHOOT : null) : d <= reach() + 0.5 ? AttackKind.SLASH : null;
        return super.chooseAttack();
    }

    @Override protected void shoot(LivingEntity t) {
        ItemStack h = getMainHandItem();
        double dx = t.getX() - getX(), dy = t.getY(0.33) - getEyeY(), dz = t.getZ() - getZ();
        double h2 = Math.sqrt(dx * dx + dz * dz);
        float dmg = (float) getAttributeValue(Attributes.ATTACK_DAMAGE);
        if (h.getItem() instanceof HyruleBowItem b) {
            net.minecraft.world.entity.projectile.Arrow a = new net.minecraft.world.entity.projectile.Arrow(level(), this);
            a.setBaseDamage(b.dmg * 0.4 + dmg * 0.3);
            a.pickup = net.minecraft.world.entity.projectile.AbstractArrow.Pickup.DISALLOWED;
            a.shoot(dx, dy + h2 * 0.2, dz, 1.6f, 3f);
            level().addFreshEntity(a);
        } else {
            boolean boom = isBoomerang(h);
            int ty = boom ? 4 : species == Species.OCTOROK ? 0 : species == Species.GUARDIAN ? 3 : new int[]{1, 2, 3, 1, 3}[rank()];
            Shot s = new Shot(level(), this, ty, boom ? h.copy() : new ItemStack(ModRegistry.shotItem(ty)), dmg);
            s.shoot(dx, dy + h2 * (ty == 0 ? 0.05 : 0), dz, boom ? 1.1f : 1.2f, 1f);
            level().addFreshEntity(s);
        }
        playSound(net.minecraft.sounds.SoundEvents.ARROW_SHOOT, 1f, 0.8f + random.nextFloat() * 0.4f);
    }

    @Override public SpawnGroupData finalizeSpawn(ServerLevelAccessor lv, DifficultyInstance d, MobSpawnType r,
                                                  @Nullable SpawnGroupData g, @Nullable net.minecraft.nbt.CompoundTag tag) {
        g = super.finalizeSpawn(lv, d, r, g, tag);
        int roll = random.nextInt(100), rank = 0;
        for (int i = 0; i < 5 && roll >= RANK_WEIGHT[i]; i++) { roll -= RANK_WEIGHT[i]; rank = i + 1; }
        setRank(Math.min(rank, 4));
        getAttribute(Attributes.MAX_HEALTH).setBaseValue(species.hp * Species.HP_MUL[rank()]);
        getAttribute(Attributes.ATTACK_DAMAGE).setBaseValue(species.dmg * Species.DMG_MUL[rank()]);
        setHealth(getMaxHealth());
        populateDefaultEquipmentSlots(lv.getRandom(), d);
        return g;
    }

    @Override protected void populateDefaultEquipmentSlots(RandomSource r, DifficultyInstance d) {
        String[] pool = species.weapons[rank()];
        if (pool.length == 0) return;
        var item = ForgeRegistries.ITEMS.getValue(new ResourceLocation(HyruleCreatures.ID, pool[r.nextInt(pool.length)]));
        ItemStack s = new ItemStack(item);
        s.setDamageValue(r.nextInt(Math.max(1, s.getMaxDamage() / 2)));
        setItemSlot(EquipmentSlot.MAINHAND, s);
        setDropChance(EquipmentSlot.MAINHAND, 0.2f);
    }

    @Override public boolean doHurtTarget(Entity t) {
        boolean ok = super.doHurtTarget(t);
        if (ok && species == Species.CHUCHU && t instanceof LivingEntity e) switch (rank()) {
            case 0 -> e.setSecondsOnFire(4);
            case 1 -> { e.addEffect(new net.minecraft.world.effect.MobEffectInstance(net.minecraft.world.effect.MobEffects.MOVEMENT_SLOWDOWN, 100, 2)); e.setTicksFrozen(e.getTicksRequiredToFreeze() + 80); }
            case 2, 4 -> e.addEffect(new net.minecraft.world.effect.MobEffectInstance(net.minecraft.world.effect.MobEffects.WEAKNESS, 100, 1));
            default -> {}
        }
        return ok;
    }

    @Override public boolean causeFallDamage(float f, float m, net.minecraft.world.damagesource.DamageSource s) {
        return !species.flies && super.causeFallDamage(f, m, s);
    }
}
