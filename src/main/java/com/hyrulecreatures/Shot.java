package com.hyrulecreatures;

import net.minecraft.network.syncher.*;
import net.minecraft.world.effect.*;
import net.minecraft.world.entity.*;
import net.minecraft.world.entity.projectile.ThrowableItemProjectile;
import net.minecraft.world.item.*;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.*;

/** Rock / fire / ice / spark balls and returning boomerangs (type 4). */
public class Shot extends ThrowableItemProjectile {
    static final EntityDataAccessor<Integer> TYPE = SynchedEntityData.defineId(Shot.class, EntityDataSerializers.INT);
    private float damage = 3;
    private boolean returning;

    public Shot(EntityType<? extends Shot> t, Level l) { super(t, l); }
    public Shot(Level l, LivingEntity owner, int type, ItemStack stack, float damage) {
        super(ModRegistry.SHOT.get(), owner, l);
        entityData.set(TYPE, type); this.damage = damage; setItem(stack);
    }
    @Override protected void defineSynchedData() { super.defineSynchedData(); entityData.define(TYPE, 0); }
    @Override protected Item getDefaultItem() { return ModRegistry.shotItem(0); }
    @Override protected float getGravity() { return entityData.get(TYPE) == 0 ? 0.03f : 0f; }

    @Override public void tick() {
        super.tick();
        if (level().isClientSide) return;
        Entity o = getOwner();
        if (entityData.get(TYPE) == 4) {
            if (tickCount == 12) returning = true;
            if (returning && o != null) {
                Vec3 to = o.getEyePosition().subtract(position());
                if (to.length() < 1.3) { discard(); return; }
                setDeltaMovement(to.normalize().scale(0.9)); hurtMarked = true;
            }
            if (tickCount > 80) discard();
        } else if (tickCount > 100) discard();
    }

    @Override protected void onHitEntity(EntityHitResult r) {
        if (!(r.getEntity() instanceof LivingEntity e) || e == getOwner() || e instanceof HyruleMob) return;
        int type = entityData.get(TYPE);
        e.hurt(damageSources().thrown(this, getOwner()), damage);
        switch (type) {
            case 1 -> e.setSecondsOnFire(5);
            case 2 -> { e.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 100, 2)); e.setTicksFrozen(e.getTicksRequiredToFreeze() + 100); }
            case 3 -> e.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 100, 1));
            default -> {}
        }
        if (type == 4) returning = true; else discard();
    }

    @Override protected void onHitBlock(BlockHitResult r) {
        if (entityData.get(TYPE) == 4) returning = true; else if (!level().isClientSide) discard();
    }
}
