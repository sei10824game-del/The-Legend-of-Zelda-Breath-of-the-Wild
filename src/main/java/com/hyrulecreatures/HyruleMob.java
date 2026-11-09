package com.hyrulecreatures;

import java.util.EnumSet;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.network.syncher.*;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.*;
import net.minecraft.world.entity.ai.goal.*;
import net.minecraft.world.entity.ai.goal.target.*;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/** Base: rank, synced attack animation, stagger/knockdown, faction. */
public abstract class HyruleMob extends Monster {
    static final EntityDataAccessor<Integer> RANK = SynchedEntityData.defineId(HyruleMob.class, EntityDataSerializers.INT);
    static final EntityDataAccessor<Integer> ATK = SynchedEntityData.defineId(HyruleMob.class, EntityDataSerializers.INT);
    static final EntityDataAccessor<Integer> ATK_T = SynchedEntityData.defineId(HyruleMob.class, EntityDataSerializers.INT);
    static final EntityDataAccessor<Integer> COMBO = SynchedEntityData.defineId(HyruleMob.class, EntityDataSerializers.INT);
    static final EntityDataAccessor<Boolean> MINI = SynchedEntityData.defineId(HyruleMob.class, EntityDataSerializers.BOOLEAN);
    static final EntityDataAccessor<Integer> DOWN = SynchedEntityData.defineId(HyruleMob.class, EntityDataSerializers.INT);
    public static final int DOWN_TIME = 80;

    private float stagger;
    private int streak, lastHit, cooldown;

    protected HyruleMob(EntityType<? extends HyruleMob> t, Level l) { super(t, l); }

    @Override protected void defineSynchedData() {
        super.defineSynchedData();
        entityData.define(RANK, 0); entityData.define(ATK, -1); entityData.define(ATK_T, 0);
        entityData.define(COMBO, 0); entityData.define(MINI, false); entityData.define(DOWN, 0);
    }
    @Override public void addAdditionalSaveData(CompoundTag t) { super.addAdditionalSaveData(t); t.putInt("Rank", rank()); t.putBoolean("Mini", isMini()); }
    @Override public void readAdditionalSaveData(CompoundTag t) { super.readAdditionalSaveData(t); setRank(t.getInt("Rank")); setMini(t.getBoolean("Mini")); }

    public boolean isMini() { return entityData.get(MINI); }
    public void setMini(boolean m) { entityData.set(MINI, m); }
    public int rank() { return entityData.get(RANK); }
    public void setRank(int r) { entityData.set(RANK, Math.max(0, Math.min(4, r))); }
    public AttackKind atkKind() { int k = entityData.get(ATK); return k < 0 ? null : AttackKind.values()[k]; }
    public int atkTick() { return entityData.get(ATK_T); }
    public int combo() { return entityData.get(COMBO); }
    public int downLeft() { return entityData.get(DOWN); }
    public boolean isDown() { return downLeft() > 0; }

    public abstract AttackKind defaultAttack();
    public abstract double reach();
    protected float spinChance() { return 0; }
    protected double engageRange() { return reach(); }
    protected boolean ranged() { return false; }
    protected void shoot(LivingEntity target) {}

    /** Foe = anything outside this mod. */
    public static boolean isFoe(LivingEntity e) {
        return !(e instanceof HyruleMob) && e.isAlive() && !(e instanceof Player p && p.isSpectator());
    }

    @Override protected Component getTypeName() {
        return Component.translatable("rank." + HyruleCreatures.ID + "." + Species.RANKS[rank()]).append(" ").append(super.getTypeName());
    }

    @Override protected void registerGoals() {
        goalSelector.addGoal(0, new FloatGoal(this));
        goalSelector.addGoal(1, new AttackGoal());
        goalSelector.addGoal(5, new WaterAvoidingRandomStrollGoal(this, 0.8));
        goalSelector.addGoal(6, new LookAtPlayerGoal(this, Player.class, 8));
        goalSelector.addGoal(7, new RandomLookAroundGoal(this));
        targetSelector.addGoal(1, new HurtByTargetGoal(this, HyruleMob.class).setAlertOthers());
        targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, LivingEntity.class, 10, true, false, HyruleMob::isFoe));
    }

    @Override protected boolean isImmobile() { return super.isImmobile() || isDown(); }

    // ---------------------------------------------------------------- stagger / knockdown
    @Override public boolean hurt(DamageSource s, float a) {
        if (level().isClientSide) return super.hurt(s, a);
        boolean down = isDown();
        if (down) a *= 1.5f;
        else if (getOffhandItem().getItem() instanceof net.minecraft.world.item.ShieldItem && atkKind() == null
                && s.getDirectEntity() != null && random.nextFloat() < 0.5f
                && getViewVector(1).dot(s.getDirectEntity().position().subtract(position()).normalize()) > 0.4) {
            playSound(SoundEvents.SHIELD_BLOCK, 1f, 1f); stagger += a * 0.5f; return false; // guarded
        }
        boolean r = super.hurt(s, a);
        if (r && !down && s.getEntity() != null && isAlive()) {
            if (tickCount - lastHit > 30) streak = 0;
            streak++; lastHit = tickCount; stagger += a;
            if (stagger >= getMaxHealth() * 0.35f || streak >= 4) knockDown(s.getEntity());
        }
        return r;
    }

    private void knockDown(Entity src) {
        entityData.set(DOWN, DOWN_TIME); entityData.set(ATK, -1);
        stagger = 0; streak = 0; getNavigation().stop();
        knockback(1.1, src.getX() - getX(), src.getZ() - getZ());
        setDeltaMovement(getDeltaMovement().add(0, 0.25, 0)); hurtMarked = true;
        playSound(SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1f, 0.7f);
    }

    // ---------------------------------------------------------------- attack state machine
    public boolean canStartAttack() { return atkKind() == null && cooldown <= 0 && !isDown(); }

    public void startAttack(AttackKind k) {
        entityData.set(ATK, k.ordinal()); entityData.set(ATK_T, 0);
    }

    protected AttackKind chooseAttack() { // may return null = keep approaching

        AttackKind k = getMainHandItem().getItem() instanceof HyruleWeaponItem w ? w.attack : defaultAttack();
        if (k == AttackKind.SMASH && random.nextFloat() < spinChance()) return AttackKind.SPIN;
        return k;
    }

    @Override public void aiStep() {
        super.aiStep();
        if (level().isClientSide) return;
        stagger *= 0.97f;
        if (cooldown > 0) cooldown--;
        int d = downLeft();
        if (d > 0) { entityData.set(DOWN, d - 1); return; }
        AttackKind a = atkKind();
        if (a == null) return;
        int t = atkTick() + 1;
        LivingEntity tg = getTarget();
        if (tg != null && t <= a.hit) { getLookControl().setLookAt(tg, 60, 60); faceTarget(tg); }
        if (a == AttackKind.THRUST && t == a.windup && tg != null) lunge(0.55);
        if (a == AttackKind.BITE && t == a.windup && tg != null)
            setDeltaMovement(tg.getEyePosition().subtract(position()).normalize().scale(0.75));
        if (a == AttackKind.SMASH && t == a.windup) lunge(0.25);
        if (t == a.hit) {
            if (a == AttackKind.SHOOT) { if (tg != null) shoot(tg); } else strike(a, tg);
        }
        if (t >= a.total) {
            int c = combo();
            if (a == AttackKind.SLASH && tg != null && c < 2 && distanceTo(tg) < reach() + 0.8) {
                entityData.set(COMBO, c + 1); startAttack(AttackKind.SLASH); return;
            }
            entityData.set(COMBO, 0); entityData.set(ATK, -1); cooldown = 20 + random.nextInt(12);
        } else entityData.set(ATK_T, t);
    }

    private void faceTarget(LivingEntity tg) {
        double dx = tg.getX() - getX(), dz = tg.getZ() - getZ();
        float yaw = (float) (Math.toDegrees(Math.atan2(dz, dx)) - 90);
        setYRot(yaw); yBodyRot = yaw; yHeadRot = yaw;
    }

    private void lunge(double power) {
        Vec3 f = Vec3.directionFromRotation(0, getYRot()).scale(power);
        setDeltaMovement(getDeltaMovement().add(f.x, 0.1, f.z)); hurtMarked = true;
    }

    private void strike(AttackKind a, LivingEntity tg) {
        double r = reach() + (a == AttackKind.THRUST ? 1.2 : a == AttackKind.SPIN ? 0.8 : 0);
        if (a == AttackKind.SPIN) {
            for (LivingEntity e : level().getEntitiesOfClass(LivingEntity.class, getBoundingBox().inflate(r), HyruleMob::isFoe))
                doHurtTarget(e);
        } else if (tg != null && distanceTo(tg) < r + tg.getBbWidth() / 2) doHurtTarget(tg);
        playSound(SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.8f + random.nextFloat() * 0.4f);
    }

    private class AttackGoal extends Goal {
        int repath;
        AttackGoal() { setFlags(EnumSet.of(Flag.MOVE, Flag.LOOK)); }
        @Override public boolean canUse() { LivingEntity t = getTarget(); return t != null && t.isAlive(); }
        @Override public void stop() { getNavigation().stop(); }
        @Override public void tick() {
            LivingEntity t = getTarget();
            if (atkKind() != null) { getNavigation().stop(); return; }
            getLookControl().setLookAt(t, 30, 30);
            double reach = engageRange() + t.getBbWidth() / 2;
            double d2 = distanceToSqr(t.getX(), t.getY(), t.getZ());
            boolean los = hasLineOfSight(t);
            if (d2 <= reach * reach && canStartAttack() && los) {
                AttackKind k = chooseAttack();
                if (k != null) { startAttack(k); return; }
            }
            if (ranged() && los && d2 < reach * reach * 0.6) { getNavigation().stop(); return; }
            if (--repath <= 0) { getNavigation().moveTo(t, 1.15); repath = 4 + random.nextInt(7); }
        }
    }
}
