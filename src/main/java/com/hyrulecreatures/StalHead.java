package com.hyrulecreatures;

import java.util.EnumSet;
import java.util.UUID;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.syncher.*;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.*;
import net.minecraft.world.entity.ai.goal.Goal;
import net.minecraft.world.level.Level;

/** The detached skull of a Stalkoblin/Stalmoblin/Stalizalfos: 1 HP, rolls back to its body. Killing it kills the body. */
public class StalHead extends PathfinderMob {
    static final EntityDataAccessor<Integer> SP = SynchedEntityData.defineId(StalHead.class, EntityDataSerializers.INT);
    static final EntityDataAccessor<Integer> RK = SynchedEntityData.defineId(StalHead.class, EntityDataSerializers.INT);
    private UUID owner;
    private int lost;

    public StalHead(EntityType<? extends StalHead> t, Level l) { super(t, l); }
    public StalHead(Level l, HyruleBiped body) {
        this(ModRegistry.STAL_HEAD.get(), l);
        owner = body.getUUID();
        entityData.set(SP, body.species.ordinal()); entityData.set(RK, body.rank());
        moveTo(body.getX(), body.getY() + body.getBbHeight() * 0.8, body.getZ(), body.getYRot(), 0);
    }

    @Override protected void defineSynchedData() { super.defineSynchedData(); entityData.define(SP, 0); entityData.define(RK, 0); }
    public Species species() { return Species.values()[entityData.get(SP)]; }
    public int rank() { return entityData.get(RK); }
    @Override public void addAdditionalSaveData(CompoundTag t) {
        super.addAdditionalSaveData(t); t.putInt("Sp", entityData.get(SP)); t.putInt("Rk", rank()); if (owner != null) t.putUUID("Owner", owner);
    }
    @Override public void readAdditionalSaveData(CompoundTag t) {
        super.readAdditionalSaveData(t); entityData.set(SP, t.getInt("Sp")); entityData.set(RK, t.getInt("Rk")); if (t.hasUUID("Owner")) owner = t.getUUID("Owner");
    }

    private HyruleBiped body() {
        return level() instanceof ServerLevel sl && owner != null && sl.getEntity(owner) instanceof HyruleBiped b && b.isAlive() ? b : null;
    }

    @Override protected void registerGoals() {
        goalSelector.addGoal(1, new Goal() {
            { setFlags(EnumSet.of(Flag.MOVE)); }
            @Override public boolean canUse() { return body() != null; }
            @Override public void tick() { HyruleBiped b = body(); if (b != null) getNavigation().moveTo(b, 1.4); }
        });
    }

    @Override public void aiStep() {
        super.aiStep();
        if (level().isClientSide) return;
        if (body() == null && ++lost > 60) discard(); else if (body() != null) lost = 0;
    }

    @Override public void die(DamageSource src) {
        super.die(src);
        if (level().isClientSide) return;
        HyruleBiped b = body();
        if (b != null) b.hurt(damageSources().genericKill(), Float.MAX_VALUE); // head destroyed -> the Stal collapses
    }
}
