package com.hyrulecreatures;

import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.DifficultyInstance;
import net.minecraft.world.entity.*;
import net.minecraft.world.entity.ai.attributes.*;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.item.ItemStack;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.RandomSource;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.util.Mth;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;
import net.minecraftforge.registries.ForgeRegistries;
import javax.annotation.Nullable;

/** Data-driven creature (Bokoblin, Moblin, Lizalfos, ...). */
public class HyruleBiped extends HyruleMob {
    public final Species species;
    private static final java.util.Map<Species, String[]> SHIELDS = java.util.Map.of(
            Species.BOKOBLIN, new String[]{"boko_shield", "spiked_boko_shield", "dragonbone_boko_shield", "knights_shield", "royal_shield"},
            Species.HORRIBLIN, new String[]{"boko_shield", "spiked_boko_shield", "dragonbone_boko_shield", "knights_shield", "royal_shield"},
            Species.STALKOBLIN, new String[]{"boko_shield", "spiked_boko_shield", "dragonbone_boko_shield", "dragonbone_boko_shield", "dragonbone_boko_shield"},
            Species.SOLDIER_CONSTRUCT, new String[]{"soldiers_shield", "knights_shield", "royal_shield", "royal_shield", "hylian_shield"},
            Species.GUARDIAN_SCOUT_1, new String[]{"guardian_shield", "guardian_shield", "guardian_shield", "guardian_shield", "guardian_shield"},
            Species.GUARDIAN_SCOUT_2, new String[]{"guardian_shield", "guardian_shield", "guardian_shield", "guardian_shield", "guardian_shield"},
            Species.GUARDIAN_SCOUT_4, new String[]{"guardian_shield", "guardian_shield", "guardian_shield", "guardian_shield", "guardian_shield"},
            Species.FIREBLIGHT_GANON, new String[]{"royal_shield", "royal_shield", "royal_shield", "royal_shield", "royal_shield"},
            Species.YIGA_BLADEMASTER, new String[]{"soldiers_shield", "knights_shield", "knights_shield", "royal_shield", "royal_shield"});
    private static final java.util.Map<Species, String[]> SHIELDS2 = java.util.Map.of(
            Species.STALFOS, new String[]{"stalfos_sword", "stalfos_sword", "stalfos_sword", "stalfos_sword", "stalfos_sword"}, // dual-wield
            Species.CURSED_BOKOBLIN, new String[]{"boko_shield", "spiked_boko_shield", "dragonbone_boko_shield", "knights_shield", "royal_shield"},
            Species.GHIRAHIM, new String[]{"royal_shield", "royal_shield", "royal_shield", "royal_shield", "royal_shield"},
            Species.BULBLIN, new String[]{"bulblin_shield", "bulblin_shield", "bulblin_shield", "bulblin_shield", "bulblin_shield"},
            Species.DARK_NUT, new String[]{"dark_nut_shield", "dark_nut_shield", "dark_nut_shield", "dark_nut_shield", "dark_nut_shield"},
            Species.DINOLFOS, new String[]{"dinolfos_shield", "dinolfos_shield", "dinolfos_shield", "dinolfos_shield", "dinolfos_shield"},
            Species.ZANT, new String[]{"zant_sword", "zant_sword", "zant_sword", "zant_sword", "zant_sword"}); // dual scimitars
    private static final int[] RANK_WEIGHT = {50, 28, 14, 7, 1};

    public HyruleBiped(EntityType<? extends HyruleBiped> t, Level l, Species s) { super(t, l); species = s; }

    public static AttributeSupplier.Builder attributes(Species s) {
        return Monster.createMonsterAttributes().add(Attributes.MAX_HEALTH, s.hp).add(Attributes.ATTACK_DAMAGE, s.dmg)
                .add(Attributes.MOVEMENT_SPEED, s.speed).add(Attributes.ATTACK_KNOCKBACK, s.knock)
                .add(Attributes.FOLLOW_RANGE, 28).add(Attributes.FLYING_SPEED, s.speed).add(Attributes.KNOCKBACK_RESISTANCE, s.scale > 1.2 ? 0.5 : 0);
    }

    @Override protected Component getTypeName() { return species.hasRanks() ? super.getTypeName() : Component.translatable(getType().getDescriptionId()); }
    @Override public AttackKind defaultAttack() { return species.attack; }
    @Override public double reach() { return species.reach + (getMainHandItem().getItem() instanceof HyruleWeaponItem w && w.style == HyruleWeaponItem.Style.SPEAR ? 0.6 : 0); }
    @Override protected double stompChance() {
        return switch (species) { case GLOOM_HANDS, FLUX_CONSTRUCT, MOLDUGA, MOLDUKING, KING_BULBLIN, FYRUS, DODONGO, DARK_NUT, GUMARM, STALMASTER, KOLOKTOS, MOLDARACH, DEMISE, THE_IMPRISONED, HINOX, TALUS, GUARDIAN, STALHINOX, CALAMITY_GANON, THUNDERBLIGHT_GANON -> 0.3; case GUARDIAN_SCOUT_4 -> 0.2; case FROX -> 0.35; case CAPTAIN_CONSTRUCT -> 0.2; case MOBLIN -> 0.1; default -> 0; };
    }
    private boolean gapCloser() { return switch (species) { case LYNEL, MOBLIN, STALMOBLIN, BOSS_BOKOBLIN, LIZALFOS, LIZALFOS_FIRE, LIZALFOS_ICE, LIZALFOS_ELEC, DARK_LIZALFOS, GIBDO, REDEAD -> true; default -> false; }; }
    private boolean isLizalfos() { return switch (species) { case LIZALFOS, LIZALFOS_FIRE, LIZALFOS_ICE, LIZALFOS_ELEC, DARK_LIZALFOS -> true; default -> false; }; }
    private boolean isGiant() { return switch (species) { case HINOX, STALHINOX, TALUS, FROX, MOLDUGA, MOLDUKING, DODONGO -> true; default -> false; }; }
    @Override protected boolean canCharge() {
        return switch (species) { case MOLDUGA, MOLDUKING, HELMASAUR, DODONGO, SHAKOMITE, ARMOS, CURSED_BOKOBLIN, TECHNO_BOKOBLIN, BOKOBLIN, HORRIBLIN, STALKOBLIN, MOBLIN, STALMOBLIN, LYNEL, THUNDERBLIGHT_GANON, FIREBLIGHT_GANON, MASTER_KOHGA -> true; default -> false; };
    }
    // ---------------------------------------------------------------- Stal creatures: 1 HP, head pops off, body keeps fighting
    private java.util.UUID headId;
    public boolean headless() { return (aux() & 1) != 0; }
    private StalHead head() {
        return level() instanceof ServerLevel sl && headId != null && sl.getEntity(headId) instanceof StalHead h && h.isAlive() ? h : null;
    }
    private void popHead(net.minecraft.world.damagesource.DamageSource src) {
        setAux(aux() | 1);
        StalHead h = new StalHead(level(), this);
        headId = h.getUUID();
        if (src.getEntity() != null) {
            Vec3 away = h.position().subtract(src.getEntity().position()).multiply(1, 0, 1).normalize();
            h.setDeltaMovement(away.x * 0.5, 0.45, away.z * 0.5);
        }
        level().addFreshEntity(h);
        playSound(SoundEvents.SKELETON_HURT, 1f, 0.7f);
    }
    private void reattach() {
        StalHead h = head();
        if (h != null) h.discard();
        setAux(aux() & ~1); headId = null;
        playSound(SoundEvents.SKELETON_AMBIENT, 1f, 1.4f);
    }

    @Override protected void registerGoals() {
        super.registerGoals();
        goalSelector.addGoal(0, new net.minecraft.world.entity.ai.goal.Goal() { // fetch the skull
            { setFlags(java.util.EnumSet.of(Flag.MOVE)); }
            @Override public boolean canUse() {
                StalHead h = head();
                return species != null && species.isStal() && headless() && h != null && (getTarget() == null || distanceTo(getTarget()) > 3.5);
            }
            @Override public void tick() {
                StalHead h = head();
                if (h == null) return;
                getNavigation().moveTo(h, 1.15);
                if (distanceTo(h) < 1.5) reattach();
            }
        });
    }

    private net.minecraft.server.level.ServerBossEvent bar;
    private void tickBossBar() {
        if (getMaxHealth() < 300 || !(level() instanceof ServerLevel sl)) return;
        if (bar == null) bar = new net.minecraft.server.level.ServerBossEvent(getDisplayName(), net.minecraft.world.BossEvent.BossBarColor.RED, net.minecraft.world.BossEvent.BossBarOverlay.PROGRESS);
        bar.setProgress(Math.max(0f, getHealth() / getMaxHealth()));
        if (tickCount % 20 == 0) {
            for (var pl : sl.getPlayers(p -> p.distanceToSqr(this) < 48 * 48)) bar.addPlayer(pl);
            for (var pl : new java.util.ArrayList<>(bar.getPlayers())) if (pl.distanceToSqr(this) > 56 * 56) bar.removePlayer(pl);
        }
    }
    @Override public void remove(Entity.RemovalReason r) { if (bar != null) bar.removeAllPlayers(); super.remove(r); }
    private ItemStack altWeapon = ItemStack.EMPTY; // Yiga carry a blade AND a bow and swap by distance
    private boolean dualBow() { return species == Species.YIGA_FOOTSOLDIER || species == Species.YIGA_BLADEMASTER || species == Species.MASTER_KOHGA; }
    private void swapWeapons() { ItemStack m = getMainHandItem(); setItemSlot(EquipmentSlot.MAINHAND, altWeapon); altWeapon = m; }
    private boolean enraged;
    @Override public void aiStep() {
        super.aiStep();
        if (!level().isClientSide) tickBossBar();
        if (!level().isClientSide && !species.hasRanks() && rank() != 0) setRank(0);
        if (!level().isClientSide && dualBow() && !altWeapon.isEmpty() && tickCount % 10 == 0 && atkKind() == null && getTarget() != null) {
            double dd = distanceTo(getTarget()); boolean bow = getMainHandItem().getItem() instanceof HyruleBowItem;
            if (!bow && dd > 9 && altWeapon.getItem() instanceof HyruleBowItem) swapWeapons();
            else if (bow && dd < 5 && !(altWeapon.getItem() instanceof HyruleBowItem)) swapWeapons();
        }
        if (!level().isClientSide && tickCount % 5 == 0 && level() instanceof ServerLevel asl && auraParticle() != null)
            asl.sendParticles(auraParticle(), getX(), getY() + getBbHeight() * 0.6, getZ(), 2, getBbWidth() * 0.4, getBbHeight() * 0.3, getBbWidth() * 0.4, 0.01);
        if (!level().isClientSide && !enraged && getMaxHealth() >= 300 && getHealth() < getMaxHealth() * 0.5f) { // boss phase 2
            enraged = true;
            getAttribute(Attributes.MOVEMENT_SPEED).setBaseValue(getAttribute(Attributes.MOVEMENT_SPEED).getBaseValue() * 1.3);
            getAttribute(Attributes.ATTACK_DAMAGE).setBaseValue(getAttribute(Attributes.ATTACK_DAMAGE).getBaseValue() * 1.25);
            playSound(SoundEvents.ENDER_DRAGON_GROWL, 2f, 0.8f);
            if (level() instanceof ServerLevel sl) sl.sendParticles(ParticleTypes.ANGRY_VILLAGER, getX(), getY() + getBbHeight(), getZ(), 20, 1, 0.5, 1, 0);
        }
        if (!level().isClientSide && species.isStal() && headless() && tickCount % 20 == 0 && head() == null) setAux(aux() & ~1); // head lost: grow back
    }

    // ---------------------------------------------------------------- guardians: 8 legs with own HP, beam
    public boolean isLegged() { return species == Species.GUARDIAN || species == Species.DECAYED_GUARDIAN || species == Species.CALAMITY_GANON; }
    private boolean longShooter() { return switch (species) { case MARBLED_GOHMA, COLGERA, ZANT, GANONDORF, DODONGO, DIABABA, ARMOGOHMA, ARGOROK, LYNEL, HINOX, TALUS, FROX, STALHINOX, SCALDERA, THE_IMPRISONED, DEMISE, KOLOKTOS, LIZALFOS_FIRE, LIZALFOS_ICE, LIZALFOS_ELEC, MASTER_KOHGA, FIREBLIGHT_GANON, WATERBLIGHT_GANON, WINDBLIGHT_GANON, THUNDERBLIGHT_GANON -> true; default -> false; }; }
    private boolean pureBeamer() { return switch (species) { case GUARDIAN, DECAYED_GUARDIAN, GUARDIAN_TURRET, GUARDIAN_SKYWATCHER, CALAMITY_GANON, BEAMOS -> true; default -> false; }; }
    private float[] legHp;

    private Vec3 hitPoint(net.minecraft.world.damagesource.DamageSource s) {
        Entity src = s.getDirectEntity();
        if (!(src instanceof LivingEntity le)) return src.position();
        Vec3 eye = le.getEyePosition(), end = eye.add(le.getLookAngle().scale(8));
        return getBoundingBox().clip(eye, end).orElse(src.position());
    }

    /** returns true if the hit was absorbed by a leg. */
    private boolean hitLeg(net.minecraft.world.damagesource.DamageSource s, float a) {
        if (s.getDirectEntity() == null || aux() == 0xFF) return false;
        Vec3 hp = hitPoint(s);
        if ((hp.y - getY()) / getBbHeight() > 0.46) return false; // above the body line
        double yaw = Math.toRadians(yBodyRot), ox = hp.x - getX(), oz = hp.z - getZ();
        double fwd = ox * -Math.sin(yaw) + oz * Math.cos(yaw), left = ox * Math.cos(yaw) + oz * Math.sin(yaw);
        double ang = Math.atan2(-fwd, left); // model space (x = left, z = -forward)
        int best = -1; double bd = 9;
        for (int i = 0; i < 8; i++) {
            if ((aux() >> i & 1) != 0) continue;
            double df = Math.abs(Mth.wrapDegrees((float) Math.toDegrees(ang - (i * Math.PI / 4 + Math.PI / 8))));
            if (df < bd) { bd = df; best = i; }
        }
        if (best < 0) return false;
        if (legHp == null) { legHp = new float[8]; java.util.Arrays.fill(legHp, Math.max(8, getMaxHealth() * 0.12f)); }
        legHp[best] -= a;
        playSound(SoundEvents.IRON_GOLEM_DAMAGE, 1f, 0.6f);
        if (legHp[best] <= 0) {
            setAux(aux() | 1 << best);
            int alive = 8 - Integer.bitCount(aux());
            getAttribute(Attributes.MOVEMENT_SPEED).setBaseValue(species.speed * alive / 8.0);
            playSound(SoundEvents.ANVIL_BREAK, 1f, 0.8f);
            if (level() instanceof ServerLevel sl) sl.sendParticles(ParticleTypes.POOF, getX(), getY() + 0.5, getZ(), 12, .5, .3, .5, 0.02);
        }
        if (s.getEntity() instanceof LivingEntity le && HyruleMob.isFoe(le)) setTarget(le);
        return true;
    }

    private Vec3 aim, impact;
    private Vec3 beamEye() { return position().add(0, getBbHeight() * 0.58, 0).add(Vec3.directionFromRotation(0, getYRot()).scale(0.5 * species.scale)); }

    private void line(ServerLevel sl, Vec3 a, Vec3 b, net.minecraft.core.particles.ParticleOptions p, double step) {
        Vec3 dv = b.subtract(a); double len = dv.length(); dv = dv.normalize();
        for (double x = 0; x < len; x += step) sl.sendParticles(p, a.x + dv.x * x, a.y + dv.y * x, a.z + dv.z * x, 1, 0, 0, 0, 0);
    }

    private boolean isBlight() { return switch (species) { case FIREBLIGHT_GANON, WATERBLIGHT_GANON, WINDBLIGHT_GANON, THUNDERBLIGHT_GANON -> true; default -> false; }; }
    /** element of the ground-targeted magic: 1 fire, 2 water, 3 lightning, 4 wind */
    private int areaElement() {
        return switch (species) { case QUEEN_GIBDO -> 8; case COLGERA, MOLDUGA, MOLDUKING -> 4; case REDEAD -> 8; case ZANT -> 4; case GANONDORF -> 3; case TENTALUS -> 2; case GHIRAHIM -> 4; case DEMISE -> 3; case BLIZZROBE -> 5; case THUNDER_WIZZROBE -> 3; case WATERBLIGHT_GANON -> 2; case THUNDERBLIGHT_GANON -> 3; case WINDBLIGHT_GANON -> 4; default -> 1; };
    }
    private boolean areaUser() { return isBlight() || species == Species.QUEEN_GIBDO || species == Species.COLGERA || species == Species.MOLDUGA || species == Species.MOLDUKING || species == Species.ZANT || species == Species.GANONDORF || species == Species.FYRUS || species == Species.ARGOROK || species == Species.REDEAD || species == Species.TENTALUS || species == Species.GHIRAHIM || species == Species.DEMISE || species == Species.SCALDERA || species == Species.THE_IMPRISONED || species == Species.BLIZZROBE || species == Species.THUNDER_WIZZROBE || (species == Species.WIZZROBE && rank() == 3) || species == Species.CALAMITY_GANON || species == Species.MASTER_KOHGA; }

    private void fireSea(Vec3 center, int r) {
        if (!level().getGameRules().getBoolean(net.minecraft.world.level.GameRules.RULE_MOBGRIEFING)) return;
        BlockPos c = BlockPos.containing(center);
        for (int x = -r; x <= r; x++) for (int z = -r; z <= r; z++) {
            if (x * x + z * z > r * r + 2 || random.nextFloat() > 0.75f) continue;
            for (int y = 3; y >= -3; y--) {
                BlockPos p = c.offset(x, y, z);
                if (level().getBlockState(p).isAir() && net.minecraft.world.level.block.Blocks.FIRE.defaultBlockState().canSurvive(level(), p)) {
                    level().setBlockAndUpdate(p, net.minecraft.world.level.block.Blocks.FIRE.defaultBlockState()); break;
                }
            }
        }
    }

    private void areaTick(ServerLevel sl, AttackKind a, int t) {
        if (aim == null) return;
        int el = areaElement();
        org.joml.Vector3f col = switch (el) { case 8 -> new org.joml.Vector3f(0.7f, 0.9f, 0.7f); case 5 -> new org.joml.Vector3f(0.6f, 0.9f, 1f); case 2 -> new org.joml.Vector3f(0.2f, 0.5f, 1f); case 3 -> new org.joml.Vector3f(1f, 1f, 0.2f); case 4 -> new org.joml.Vector3f(0.6f, 1f, 0.7f); default -> new org.joml.Vector3f(1f, 0.35f, 0.05f); };
        if (t < a.hit) { // ground circle: thin while tracking, bright + pulsing once locked
            boolean locked = t > a.windup; double rad = 3.5;
            for (int i = 0; i < (locked ? 40 : 20); i++) {
                double ang = i * Math.PI * 2 / (locked ? 40 : 20) + t * 0.15;
                sl.sendParticles(new net.minecraft.core.particles.DustParticleOptions(col, locked ? 1.6f : 0.9f), aim.x + Math.cos(ang) * rad, aim.y + 0.1, aim.z + Math.sin(ang) * rad, 1, 0, 0, 0, 0);
            }
            if (locked && t % 4 == 0) { playSound(SoundEvents.NOTE_BLOCK_BIT.value(), 1f, 2f); sl.sendParticles(ParticleTypes.CLOUD, aim.x, aim.y + 4, aim.z, 3, 1, 0.5, 1, 0.01); }
        }
    }

    private void areaFire(ServerLevel sl) {
        int el = areaElement(); float dmg = (float) getAttributeValue(Attributes.ATTACK_DAMAGE);
        Vec3 c = aim;
        playSound(SoundEvents.GENERIC_EXPLODE, 2f, 1.3f);
        switch (el) {
            case 2 -> { // geyser: launch everything upward
                sl.sendParticles(ParticleTypes.SPLASH, c.x, c.y + 1, c.z, 160, 1.2, 2.5, 1.2, 0.3);
                sl.sendParticles(ParticleTypes.BUBBLE_POP, c.x, c.y + 1, c.z, 60, 1.2, 2, 1.2, 0.2);
                for (LivingEntity e : sl.getEntitiesOfClass(LivingEntity.class, new AABB(c, c).inflate(3.5), HyruleMob::isFoe)) {
                    e.hurt(damageSources().mobAttack(this), dmg * 0.8f); e.setDeltaMovement(e.getDeltaMovement().add(0, 1.2, 0)); e.hurtMarked = true;
                }
            }
            case 8 -> { // scream: paralyses everything near the target circle
                sl.sendParticles(ParticleTypes.NOTE, c.x, c.y + 1.5, c.z, 20, 2, 1, 2, 1);
                for (LivingEntity e : sl.getEntitiesOfClass(LivingEntity.class, new AABB(c, c).inflate(5), HyruleMob::isFoe)) {
                    e.addEffect(new net.minecraft.world.effect.MobEffectInstance(net.minecraft.world.effect.MobEffects.MOVEMENT_SLOWDOWN, 100, 6));
                    e.addEffect(new net.minecraft.world.effect.MobEffectInstance(net.minecraft.world.effect.MobEffects.WEAKNESS, 100, 1));
                }
            }
            case 5 -> { // blizzard: freezes everything in the circle
                sl.sendParticles(ParticleTypes.SNOWFLAKE, c.x, c.y + 1.5, c.z, 200, 2.5, 1.5, 2.5, 0.05);
                for (LivingEntity e : sl.getEntitiesOfClass(LivingEntity.class, new AABB(c, c).inflate(3.5), HyruleMob::isFoe)) {
                    e.hurt(damageSources().mobAttack(this), dmg * 0.7f); e.setTicksFrozen(e.getTicksRequiredToFreeze() + 200);
                    e.addEffect(new net.minecraft.world.effect.MobEffectInstance(net.minecraft.world.effect.MobEffects.MOVEMENT_SLOWDOWN, 120, 3));
                }
            }
            case 3 -> { // lightning
                net.minecraft.world.entity.LightningBolt bolt = EntityType.LIGHTNING_BOLT.create(sl);
                if (bolt != null) { bolt.moveTo(c.x, c.y, c.z); sl.addFreshEntity(bolt); }
                for (LivingEntity e : sl.getEntitiesOfClass(LivingEntity.class, new AABB(c, c).inflate(3.5), HyruleMob::isFoe)) e.hurt(damageSources().mobAttack(this), dmg * 0.8f);
            }
            case 4 -> { // whirlwind: heavy knockback outward and up
                sl.sendParticles(ParticleTypes.CLOUD, c.x, c.y + 1, c.z, 120, 2, 1.5, 2, 0.4);
                sl.sendParticles(ParticleTypes.SWEEP_ATTACK, c.x, c.y + 1, c.z, 12, 2, 0.5, 2, 0);
                for (LivingEntity e : sl.getEntitiesOfClass(LivingEntity.class, new AABB(c, c).inflate(4.5), HyruleMob::isFoe)) {
                    e.hurt(damageSources().mobAttack(this), dmg * 0.6f);
                    e.knockback(2.2, c.x - e.getX(), c.z - e.getZ()); e.setDeltaMovement(e.getDeltaMovement().add(0, 0.8, 0)); e.hurtMarked = true;
                }
            }
            default -> { // fire pillar + sea of fire
                sl.explode(this, c.x, c.y, c.z, 2.4f, false, Level.ExplosionInteraction.MOB);
                for (LivingEntity e : sl.getEntitiesOfClass(LivingEntity.class, new AABB(c, c).inflate(3.5), HyruleMob::isFoe)) { e.setSecondsOnFire(8); e.hurt(damageSources().mobAttack(this), dmg * 0.7f); }
                fireSea(c, 3);
                sl.sendParticles(ParticleTypes.FLAME, c.x, c.y + 0.5, c.z, 120, 1.5, 2.5, 1.5, 0.08);
            }
        }
    }

    @Override protected void tickAttack(AttackKind a, int t, LivingEntity tg) {
        speciesMoves(a, t, tg);
        if (a == AttackKind.AREA && level() instanceof ServerLevel asl) {
            if (t <= a.windup && tg != null) aim = Vec3.atBottomCenterOf(BlockPos.containing(tg.position())); // tracks the target's feet, then locks
            areaTick(asl, a, t);
            return;
        }
        if (a != AttackKind.BEAM || !(level() instanceof ServerLevel sl)) return;
        Vec3 eye = beamEye();
        if (t <= a.windup && tg != null) aim = tg.position().add(0, tg.getBbHeight() * 0.5, 0); // tracking
        if (aim == null) return;
        if (t < a.hit) { // laser sight: thin red while tracking, thick orange once locked
            boolean locked = t > a.windup;
            line(sl, eye, aim, new net.minecraft.core.particles.DustParticleOptions(new org.joml.Vector3f(1f, locked ? 0.45f : 0.05f, 0.05f), locked ? 1.6f : 1.0f), locked ? 0.2 : 0.35);
            if (t % 5 == 0) playSound(locked ? SoundEvents.NOTE_BLOCK_BIT.value() : SoundEvents.NOTE_BLOCK_HAT.value(), 1f, locked ? 2f : 1.2f);
        } else if (t <= a.hit + 8 && impact != null) { // the beam itself
            line(sl, eye, impact, ParticleTypes.END_ROD, 0.15);
            line(sl, eye, impact, new net.minecraft.core.particles.DustParticleOptions(new org.joml.Vector3f(0.4f, 1f, 1f), 2.6f), 0.2);
        }
    }

    @Override protected void beamFire() {
        if (atkKind() == AttackKind.AREA) { if (level() instanceof ServerLevel asl && aim != null) areaFire(asl); return; }
        if (!(level() instanceof ServerLevel sl) || aim == null) return;
        Vec3 eye = beamEye(), dir = aim.subtract(eye).normalize();
        impact = level().clip(new net.minecraft.world.level.ClipContext(eye, eye.add(dir.scale(48)), net.minecraft.world.level.ClipContext.Block.COLLIDER,
                net.minecraft.world.level.ClipContext.Fluid.NONE, this)).getLocation();
        playSound(SoundEvents.LIGHTNING_BOLT_THUNDER, 2f, 1.8f);
        sl.explode(this, impact.x, impact.y, impact.z, 3.2f, false, Level.ExplosionInteraction.MOB);
        float dmg = (float) getAttributeValue(Attributes.ATTACK_DAMAGE);
        for (LivingEntity e : level().getEntitiesOfClass(LivingEntity.class, new AABB(impact, impact).inflate(4.5), HyruleMob::isFoe)) {
            e.setSecondsOnFire(10); e.hurt(damageSources().mobAttack(this), dmg * 0.6f);
        }
        fireSea(impact, 4);
        sl.sendParticles(ParticleTypes.FLAME, impact.x, impact.y + 0.3, impact.z, 80, 2.5, 0.4, 2.5, 0.05);
        sl.sendParticles(ParticleTypes.LAVA, impact.x, impact.y + 0.3, impact.z, 20, 2, 0.3, 2, 0.1);
    }

    @Override public boolean hurt(net.minecraft.world.damagesource.DamageSource src, float a) {
        if ((species == Species.SKULLTULA || species == Species.WALL_SKULLTULA) && !level().isClientSide && src.getEntity() != null // hard back: only the front takes damage
                && getViewVector(1).dot(src.getEntity().position().subtract(position()).normalize()) < 0.2) { playSound(SoundEvents.ANVIL_LAND, 0.6f, 1.6f); return false; }
        if (species.isStal() && !level().isClientSide && !src.is(net.minecraft.tags.DamageTypeTags.BYPASSES_INVULNERABILITY)) {
            if (headless()) return false;          // headless body cannot be hurt: smash the skull
            if (a > 0 && src.getEntity() != null) { popHead(src); return true; }
        }
        if (isLegged() && !level().isClientSide && hitLeg(src, a)) return true;
        boolean r = super.hurt(src, a);
        if (r && species.teleports() && !level().isClientSide && isAlive())
            for (int i = 0; i < 8; i++) if (randomTeleport(getX() + (random.nextDouble() - .5) * 16, getY() + random.nextInt(3), getZ() + (random.nextDouble() - .5) * 16, true)) break;
        return r;
    }
    @Override public void addAdditionalSaveData(net.minecraft.nbt.CompoundTag t) { super.addAdditionalSaveData(t); if (!altWeapon.isEmpty()) t.put("Alt", altWeapon.save(new net.minecraft.nbt.CompoundTag())); }
    @Override public void readAdditionalSaveData(net.minecraft.nbt.CompoundTag t) { super.readAdditionalSaveData(t); if (t.contains("Alt")) altWeapon = ItemStack.of(t.getCompound("Alt")); }
    @Override protected float spinChance() { return species.spin; }

    private static boolean isBoomerang(ItemStack s) { return ForgeRegistries.ITEMS.getKey(s.getItem()).getPath().contains("boomerang"); }
    @Override protected boolean ranged() { return getMainHandItem().getItem() instanceof HyruleBowItem || species.attack == AttackKind.SHOOT || pureBeamer(); }
    @Override protected double engageRange() {
        ItemStack h = getMainHandItem();
        if (pureBeamer() || species == Species.GUARDIAN_SCOUT_4 || areaUser()) return 20;
        if (longShooter() && !(h.getItem() instanceof HyruleBowItem)) return 18;
        if (h.getItem() instanceof HyruleBowItem) return 14;
        if (isBoomerang(h)) return 9;
        double r = reach();
        if (canCharge() || gapCloser()) r = Math.max(r, 12);
        boolean oneHand = h.getItem() instanceof HyruleWeaponItem w ? w.style == HyruleWeaponItem.Style.ONE : defaultAttack() == AttackKind.SLASH;
        return oneHand ? Math.max(r, 6.5) : r;
    }

    @Override protected AttackKind chooseAttack() {
        ItemStack h = getMainHandItem(); LivingEntity t = getTarget();
        double d = t == null ? 0 : distanceTo(t);
        if (areaUser() && d > 4 && d < 22 && random.nextFloat() < (species == Species.CALAMITY_GANON ? 0.03f : 0.02f) * (enraged ? 2.5f : 1f)) return AttackKind.AREA;
        if ((species == Species.LIZALFOS || species == Species.DARK_LIZALFOS || species == Species.LIZALFOS_FIRE || species == Species.LIZALFOS_ICE || species == Species.LIZALFOS_ELEC) // tail sweep
                && d <= reach() + 0.4 && getMainHandItem().isEmpty() && random.nextFloat() < 0.15f) return AttackKind.SPIN;
        if ((species == Species.HINOX || species == Species.STALHINOX) && d <= 5 && random.nextFloat() < 0.1f) return AttackKind.STOMP; // ground pound
        if ((species == Species.LIZALFOS || species == Species.LIZALFOS_FIRE || species == Species.LIZALFOS_ICE || species == Species.LIZALFOS_ELEC || species == Species.DARK_LIZALFOS)
                && d > 3 && d < 9 && random.nextFloat() < 0.04f) return AttackKind.LEAP; // lunging jump
        if ((species == Species.MOBLIN || species == Species.STALMOBLIN || species == Species.BOSS_BOKOBLIN) && d > 4 && d < 10 && random.nextFloat() < 0.03f) return AttackKind.CHARGE; // shoulder rush
        if ((species == Species.TALUS || species == Species.FROX) && d <= 5 && random.nextFloat() < 0.08f) return AttackKind.STOMP;
        if ((species == Species.GIBDO || species == Species.REDEAD) && d > 2 && d < 6 && random.nextFloat() < 0.05f) return AttackKind.LEAP; // lunge-and-grab
        if (species == Species.LYNEL && d > reach() + 0.4 && d < 8 && random.nextFloat() < 0.12f) return AttackKind.SLASH; // ride-by slash
        if (species == Species.LYNEL) { // gallop charge from mid range, rear-up stomp up close (BotW/TotK Lynel moves)
            if (d > 5 && d < 14 && random.nextFloat() < 0.04f * (enraged ? 2f : 1f)) return AttackKind.CHARGE;
            if (d <= 4 && random.nextFloat() < 0.12f) return AttackKind.STOMP;
        }
        if (species.attack == AttackKind.SHOOT && !(h.getItem() instanceof HyruleBowItem) && !pureBeamer()) return d <= reach() + 0.4 ? AttackKind.SHOOT : null;
        if (pureBeamer()) return d > 5 ? AttackKind.BEAM : isLegged() && random.nextFloat() < 0.4f ? AttackKind.STOMP : null;
        if (longShooter() && !(h.getItem() instanceof HyruleBowItem) && d > 6 && d < 18 && random.nextFloat() < 0.06f) return AttackKind.SHOOT;
        if (species == Species.GUARDIAN_SCOUT_4 && d > 6 && random.nextFloat() < 0.02f) return AttackKind.BEAM;
        if (h.getItem() instanceof HyruleBowItem) return d <= reach() + 0.3 ? AttackKind.SLASH : AttackKind.SHOOT;
        if (isBoomerang(h)) return d > 4 ? (random.nextFloat() < 0.6f ? AttackKind.SHOOT : null) : d <= reach() + 0.5 ? AttackKind.SLASH : null;
        return super.chooseAttack();
    }

    // ---- Lynel: fast, mounted-combat style combos
    @Override protected int atkSpeed() { return species == Species.LYNEL ? 2 : 1; }
    @Override protected int cooldownBase() { return species == Species.LYNEL ? 8 : 20; }
    @Override protected AttackKind comboNext(AttackKind a, int c, LivingEntity tg) {
        if (species != Species.LYNEL || tg == null || !tg.isAlive() || c >= 4 || distanceTo(tg) > reach() + 2.5) return null;
        return switch (a) {
            case SLASH -> c < 3 ? AttackKind.SLASH : AttackKind.SPIN; // slash, slash, slash, whirl
            case CHOP -> AttackKind.SLASH;
            case SMASH -> random.nextBoolean() ? AttackKind.CHOP : AttackKind.SLASH;
            case THRUST -> AttackKind.MULTI;
            case MULTI -> AttackKind.SLASH;
            default -> null;
        };
    }
    private void mountedStrafe(AttackKind a, int t, LivingEntity tg) { // ride past the target while swinging
        if (tg == null || t < 1 || t > a.hit + 2 || (a != AttackKind.SLASH && a != AttackKind.CHOP && a != AttackKind.THRUST && a != AttackKind.SMASH && a != AttackKind.MULTI)) return;
        Vec3 to = tg.position().subtract(position()).multiply(1, 0, 1); double dist = to.length(); if (dist < 0.01) return;
        Vec3 n = to.scale(1 / dist), tan = new Vec3(-n.z, 0, n.x).scale(combo() % 2 == 0 ? 1 : -1);
        double fwd = dist > reach() * 0.7 ? 0.22 : -0.04;
        Vec3 v = n.scale(fwd).add(tan.scale(0.26));
        setDeltaMovement(v.x, getDeltaMovement().y, v.z); hurtMarked = true;
    }

    /** Per-species hit behaviour layered on the generic attack kinds. */
    private void speciesMoves(AttackKind a, int t, LivingEntity tg) {
        if (!(level() instanceof ServerLevel sl)) return;
        if (t == 1 && (a == AttackKind.CHARGE || a == AttackKind.STOMP || a == AttackKind.LEAP) && (species == Species.LYNEL || isGiant() || isLizalfos() || species == Species.MOBLIN || species == Species.BOSS_BOKOBLIN)) { // telegraph: roar + angry puff
            playSound(net.minecraft.sounds.SoundEvents.RAVAGER_ROAR, 1.2f, Math.max(0.5f, 1.6f - getBbHeight() * 0.15f));
            sl.sendParticles(net.minecraft.core.particles.ParticleTypes.ANGRY_VILLAGER, getX(), getY() + getBbHeight() * 0.9, getZ(), 4, 0.3, 0.2, 0.3, 0);
        }
        if (species == Species.LYNEL) mountedStrafe(a, t, tg);
        if (species == Species.LYNEL && a == AttackKind.CHARGE && t >= a.windup && t < a.windup + 20) { // trample everything on the path
            for (LivingEntity e : sl.getEntitiesOfClass(LivingEntity.class, getBoundingBox().inflate(0.6), HyruleMob::isFoe)) if (e.invulnerableTime <= 0) {
                e.hurt(damageSources().mobAttack(this), (float) getAttributeValue(Attributes.ATTACK_DAMAGE) * 0.6f);
                e.knockback(1.0, getX() - e.getX(), getZ() - e.getZ()); e.hurtMarked = true;
            }
            sl.sendParticles(net.minecraft.core.particles.ParticleTypes.CLOUD, getX(), getY() + 0.1, getZ(), 3, 0.4, 0.05, 0.4, 0.02);
        }
        if (a.hitsAt(t) && a == AttackKind.STOMP && isGiant()) { // expanding shockwave ring
            for (int ring = 1; ring <= 4; ring++) for (int i = 0; i < 16; i++) {
                double ang = i * Math.PI / 8, r = ring * 1.2;
                var bs = sl.getBlockState(BlockPos.containing(getX() + Math.cos(ang) * r, getY() - 0.5, getZ() + Math.sin(ang) * r));
                if (!bs.isAir()) sl.sendParticles(new net.minecraft.core.particles.BlockParticleOption(net.minecraft.core.particles.ParticleTypes.BLOCK, bs), getX() + Math.cos(ang) * r, getY() + 0.2, getZ() + Math.sin(ang) * r, 2, 0.1, 0.1, 0.1, 0.05);
            }
            for (LivingEntity e : sl.getEntitiesOfClass(LivingEntity.class, getBoundingBox().inflate(5.5, 1.5, 5.5), HyruleMob::isFoe)) if (e.onGround()) { e.setDeltaMovement(e.getDeltaMovement().add(0, 0.6, 0)); e.hurtMarked = true; }
        }
        if (a.hitsAt(t) && tg != null && distanceTo(tg) < reach() + 2.2) {
            if ((species == Species.MOBLIN || species == Species.STALMOBLIN || species == Species.BOSS_BOKOBLIN) && a == AttackKind.CHARGE) // rush slams you off your feet
                tg.addEffect(new net.minecraft.world.effect.MobEffectInstance(net.minecraft.world.effect.MobEffects.MOVEMENT_SLOWDOWN, 40, 2));
            if ((species == Species.GIBDO || species == Species.REDEAD) && a == AttackKind.LEAP) { // grab: held in place and drained
                tg.addEffect(new net.minecraft.world.effect.MobEffectInstance(net.minecraft.world.effect.MobEffects.MOVEMENT_SLOWDOWN, 50, 4));
                tg.addEffect(new net.minecraft.world.effect.MobEffectInstance(net.minecraft.world.effect.MobEffects.WEAKNESS, 80, 0));
            }
            if (isLizalfos() && a == AttackKind.LEAP) { tg.setDeltaMovement(tg.getDeltaMovement().add(0, 0.4, 0)); tg.hurtMarked = true; } // tail flick launches you
        }
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
            if (isBlight() || species == Species.MASTER_KOHGA || species == Species.YIGA_BLADEMASTER) // boss volley: 2 extra arrows fanned out
                for (int i = -1; i <= 1; i += 2) {
                    net.minecraft.world.entity.projectile.Arrow x = new net.minecraft.world.entity.projectile.Arrow(level(), this);
                    x.setBaseDamage(b.dmg * 0.4 + dmg * 0.3); x.pickup = net.minecraft.world.entity.projectile.AbstractArrow.Pickup.DISALLOWED;
                    double ang = i * 0.18, cs = Math.cos(ang), sn = Math.sin(ang);
                    x.shoot(dx * cs - dz * sn, dy + h2 * 0.2, dx * sn + dz * cs, 1.6f, 3f);
                    level().addFreshEntity(x);
                }
        } else {
            boolean boom = isBoomerang(h);
            int ty = boom ? 4 : species == Species.FIREBLIGHT_GANON || species == Species.MASTER_KOHGA || species == Species.LIZALFOS_FIRE || species == Species.DODONGO || species == Species.ARGOROK || species == Species.POE || species == Species.SCALDERA || species == Species.THE_IMPRISONED || species == Species.FROG_MAGMA ? 1 : species == Species.FROG_WATER ? 2 : species == Species.PARASPALAS || species == Species.FROG_ELEC || species == Species.FROG_DARK ? 3 : species == Species.MARBLED_GOHMA || species == Species.COLGERA || species == Species.DEMISE || species == Species.ZANT || species == Species.GANONDORF || species == Species.ARMOGOHMA ? 3 : species == Species.DIABABA ? 0 : species == Species.KOLOKTOS ? 0 : species == Species.LIZALFOS_ICE || species == Species.BLIZZROBE ? 2 : species == Species.THUNDER_WIZZROBE ? 3 : species == Species.LIZALFOS_ELEC ? 3 : species == Species.WATERBLIGHT_GANON ? 2 : species == Species.WINDBLIGHT_GANON || species == Species.THUNDERBLIGHT_GANON ? 3 : species == Species.OCTOROK || species == Species.HINOX || species == Species.STALHINOX || species == Species.TALUS || species == Species.FROX ? 0 :  new int[]{1, 2, 3, 1, 3}[rank()];
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
        if (!rankFixed && species.hasRanks()) setRank(Math.min(rank, 4)); else if (!species.hasRanks()) setRank(0);
        getAttribute(Attributes.MAX_HEALTH).setBaseValue(species.isStal() ? 1 : species.hp * Species.HP_MUL[rank()]);
        getAttribute(Attributes.ATTACK_DAMAGE).setBaseValue(species.dmg * Species.DMG_MUL[rank()]);
        setHealth(getMaxHealth());
        populateDefaultEquipmentSlots(lv.getRandom(), d);
        if (getBbHeight() >= 5) playSound(SoundEvents.ENDER_DRAGON_GROWL, 3f, 0.7f); // arrival roar
        return g;
    }

    @Override protected void populateDefaultEquipmentSlots(RandomSource r, DifficultyInstance d) {
        String[] pool = species.weapons[rank()];
        if (pool.length == 0) return;
        var item = ForgeRegistries.ITEMS.getValue(new ResourceLocation(HyruleCreatures.ID, pool[r.nextInt(pool.length)]));
        ItemStack s = new ItemStack(item);
        s.setDamageValue(r.nextInt(Math.max(1, s.getMaxDamage() / 2)));
        if (dualBow()) { // sword in hand, bow on the back
            setItemSlot(EquipmentSlot.MAINHAND, new ItemStack(ForgeRegistries.ITEMS.getValue(new ResourceLocation(HyruleCreatures.ID, "yiga_blade"))));
            altWeapon = new ItemStack(ForgeRegistries.ITEMS.getValue(new ResourceLocation(HyruleCreatures.ID, new String[]{"yiga_bow", "soldiers_bow", "knights_bow", "royal_bow", "royal_bow"}[rank()])));
            if (species == Species.MASTER_KOHGA) altWeapon = new ItemStack(ForgeRegistries.ITEMS.getValue(new ResourceLocation(HyruleCreatures.ID, "royal_bow")));
            setDropChance(EquipmentSlot.MAINHAND, 0.2f); return;
        }
        setItemSlot(EquipmentSlot.MAINHAND, s);
        setDropChance(EquipmentSlot.MAINHAND, 0.2f);
        String[] sh = SHIELDS.get(species);
        if (sh == null) sh = SHIELDS2.get(species);
        if (sh != null && !(s.getItem() instanceof HyruleBowItem) && !(s.getItem() instanceof HyruleWeaponItem w && w.style != HyruleWeaponItem.Style.ONE) && r.nextFloat() < 0.65f) {
            setItemSlot(EquipmentSlot.OFFHAND, new ItemStack(ForgeRegistries.ITEMS.getValue(new ResourceLocation(HyruleCreatures.ID, sh[rank()]))));
            setDropChance(EquipmentSlot.OFFHAND, 0.15f);
        }
    }

    // ---------------------------------------------------------------- sounds & particles
    private int soundGroup() { // 0 piglin-like, 1 lizard, 2 bat, 3 skeleton, 4 golem, 5 spirit, 6 slime, 7 zombie, 8 beast
        return switch (species) {
            case BOKOBLIN, MOBLIN, HORRIBLIN, TECHNO_BOKOBLIN, CURSED_BOKOBLIN, BULBLIN, KING_BULBLIN, QUADRO_BABA -> 0;
            case LIZALFOS, LIZALFOS_FIRE, LIZALFOS_ICE, LIZALFOS_ELEC, DARK_LIZALFOS, DINOLFOS, AERALFOS, SKULLTULA, WALL_SKULLTULA, TEKTITE, SHAKOMITE, PETIT_MOLDORM, MOLDARACH -> 1;
            case KEESE, KEESE_FIRE, KEESE_ICE, KEESE_ELEC, KEESE_DARK, KARGAROK, PEAHAT, GLEEOK, ARGOROK -> 2;
            case STALKOBLIN, STALMOBLIN, STALIZALFOS, STALHINOX, STALFOS, STALMASTER, DEATH_SWORD, STALHOUND, STALHORSE -> 3;
            case TALUS, FROX, HINOX, ARMOS, BEAMOS, GUARDIAN, DECAYED_GUARDIAN, GUARDIAN_TURRET, GUARDIAN_SKYWATCHER, GUARDIAN_SCOUT_1, GUARDIAN_SCOUT_2, GUARDIAN_SCOUT_3, GUARDIAN_SCOUT_4,
                 SOLDIER_CONSTRUCT, CAPTAIN_CONSTRUCT, KOLOKTOS, DARK_NUT, CALAMITY_GANON, SCALDERA, GUMARM, THE_IMPRISONED, TENTALUS, ARMOGOHMA, PARASPALAS -> 4;
            case WIZZROBE, BLIZZROBE, THUNDER_WIZZROBE, GHIRAHIM, ZANT, POE, BUBBLE_FIRE, BUBBLE_ICE, BUBBLE_DARK, PHANTOM_GANON, FIREBLIGHT_GANON, WATERBLIGHT_GANON, WINDBLIGHT_GANON, THUNDERBLIGHT_GANON -> 5;
            case CHUCHU -> 6;
            case GIBDO, REDEAD, YIGA_FOOTSOLDIER, YIGA_BLADEMASTER, MASTER_KOHGA -> 7;
            default -> 8;
        };
    }
    @Override public float getVoicePitch() { return Math.max(0.5f, Math.min(1.2f, 1.3f - species.scale * 0.1f)) + (random.nextFloat() - random.nextFloat()) * 0.05f; } // bigger = deeper
    @Override protected SoundEvent getAmbientSound() {
        return switch (soundGroup()) { case 0 -> SoundEvents.ZOMBIFIED_PIGLIN_AMBIENT; case 1 -> SoundEvents.ENDERMITE_AMBIENT; case 2 -> SoundEvents.BAT_AMBIENT; case 3 -> SoundEvents.SKELETON_AMBIENT;
            case 4 -> null; case 5 -> SoundEvents.VEX_AMBIENT; case 6 -> SoundEvents.SLIME_SQUISH_SMALL; case 7 -> SoundEvents.ZOMBIE_AMBIENT; default -> SoundEvents.RAVAGER_AMBIENT; };
    }
    @Override protected SoundEvent getHurtSound(net.minecraft.world.damagesource.DamageSource s) {
        return switch (soundGroup()) { case 0 -> SoundEvents.ZOMBIFIED_PIGLIN_HURT; case 1 -> SoundEvents.ENDERMITE_HURT; case 2 -> SoundEvents.BAT_HURT; case 3 -> SoundEvents.SKELETON_HURT;
            case 4 -> SoundEvents.IRON_GOLEM_HURT; case 5 -> SoundEvents.VEX_HURT; case 6 -> SoundEvents.SLIME_HURT_SMALL; case 7 -> SoundEvents.ZOMBIE_HURT; default -> SoundEvents.RAVAGER_HURT; };
    }
    @Override protected SoundEvent getDeathSound() {
        return switch (soundGroup()) { case 0 -> SoundEvents.ZOMBIFIED_PIGLIN_DEATH; case 1 -> SoundEvents.ENDERMITE_DEATH; case 2 -> SoundEvents.BAT_DEATH; case 3 -> SoundEvents.SKELETON_DEATH;
            case 4 -> SoundEvents.IRON_GOLEM_DEATH; case 5 -> SoundEvents.VEX_DEATH; case 6 -> SoundEvents.SLIME_DEATH_SMALL; case 7 -> SoundEvents.ZOMBIE_DEATH; default -> SoundEvents.RAVAGER_DEATH; };
    }
    private net.minecraft.core.particles.ParticleOptions deathParticle() {
        return switch (soundGroup()) {
            case 3 -> new net.minecraft.core.particles.BlockParticleOption(ParticleTypes.BLOCK, net.minecraft.world.level.block.Blocks.BONE_BLOCK.defaultBlockState());
            case 4 -> new net.minecraft.core.particles.BlockParticleOption(ParticleTypes.BLOCK, (species == Species.TALUS || species == Species.FROX || species == Species.SCALDERA || species == Species.THE_IMPRISONED
                    ? net.minecraft.world.level.block.Blocks.STONE : net.minecraft.world.level.block.Blocks.IRON_BLOCK).defaultBlockState());
            case 5 -> ParticleTypes.SOUL; case 6 -> ParticleTypes.ITEM_SLIME; default -> ParticleTypes.POOF;
        };
    }
    private net.minecraft.core.particles.ParticleOptions auraParticle() {
        return switch (species) {
            case FIREBLIGHT_GANON, SCALDERA, GUMARM, BUBBLE_FIRE, LIZALFOS_FIRE, KEESE_FIRE, FYRUS, DEMISE -> ParticleTypes.FLAME;
            case WATERBLIGHT_GANON, TENTALUS -> ParticleTypes.DRIPPING_WATER;
            case THUNDERBLIGHT_GANON, ZANT, THUNDER_WIZZROBE, KEESE_ELEC, LIZALFOS_ELEC, TECHNO_BOKOBLIN -> ParticleTypes.ELECTRIC_SPARK;
            case WINDBLIGHT_GANON -> ParticleTypes.CLOUD;
            case BLIZZROBE, BUBBLE_ICE, KEESE_ICE, LIZALFOS_ICE -> ParticleTypes.SNOWFLAKE;
            case CALAMITY_GANON, SHADOW_BEAST, HORRIBLIN, CURSED_BOKOBLIN, BUBBLE_DARK, KEESE_DARK -> ParticleTypes.SMOKE;
            case POE, GHIRAHIM -> ParticleTypes.SOUL_FIRE_FLAME;
            default -> null;
        };
    }

    @Override public void die(net.minecraft.world.damagesource.DamageSource src) {
        super.die(src);
        if (!level().isClientSide && level() instanceof ServerLevel dsl)
            dsl.sendParticles(deathParticle(), getX(), getY() + getBbHeight() * 0.5, getZ(), 25 + (int) (getBbHeight() * 8), getBbWidth() * 0.5, getBbHeight() * 0.4, getBbWidth() * 0.5, 0.05);
        if (!level().isClientSide && head() != null) head().discard();
        if (!level().isClientSide && species == Species.CHUCHU && !isMini())
            for (int i = 0; i < 2; i++) {
                HyruleBiped m = ModRegistry.TYPES.get(Species.CHUCHU).get().create(level());
                m.moveTo(getX() + (i * 2 - 1) * 0.4, getY(), getZ(), random.nextFloat() * 360, 0);
                m.setRank(rank()); m.setMini(true);
                m.getAttribute(Attributes.MAX_HEALTH).setBaseValue(4); m.setHealth(4);
                m.getAttribute(Attributes.ATTACK_DAMAGE).setBaseValue(species.dmg * 0.5);
                level().addFreshEntity(m);
            }
    }

    @Override public boolean doHurtTarget(Entity t) {
        boolean ok = super.doHurtTarget(t);
        if (ok && t instanceof LivingEntity e) {
            int el = switch (species) { case LIKE_LIKE, GLOOM_HANDS, SEIZED_CONSTRUCT -> 7; case BUBBLE_FIRE -> 1; case BUBBLE_ICE -> 2; case BUBBLE_DARK -> 7; case REDEAD -> 9; case DARK_LIZALFOS, KEESE_DARK -> 7; case TECHNO_BOKOBLIN, SHAKOMITE -> 3; case MOLDARACH -> 6; case KEESE_FIRE -> 1; case KEESE_ICE -> 2; case KEESE_ELEC -> 3; case CHUCHU -> rank() >= 1 && rank() <= 3 ? rank() : 0; default -> 0; };
            switch (el) {
                case 1 -> e.setSecondsOnFire(4);
                case 2 -> { e.addEffect(new net.minecraft.world.effect.MobEffectInstance(net.minecraft.world.effect.MobEffects.MOVEMENT_SLOWDOWN, 100, 2)); e.setTicksFrozen(e.getTicksRequiredToFreeze() + 80); }
                case 3 -> e.addEffect(new net.minecraft.world.effect.MobEffectInstance(net.minecraft.world.effect.MobEffects.WEAKNESS, 100, 1));
                case 6 -> e.addEffect(new net.minecraft.world.effect.MobEffectInstance(net.minecraft.world.effect.MobEffects.POISON, 120, 1));
                case 9 -> e.addEffect(new net.minecraft.world.effect.MobEffectInstance(net.minecraft.world.effect.MobEffects.MOVEMENT_SLOWDOWN, 80, 3));
                case 7 -> { e.addEffect(new net.minecraft.world.effect.MobEffectInstance(net.minecraft.world.effect.MobEffects.WEAKNESS, 140, 2)); e.addEffect(new net.minecraft.world.effect.MobEffectInstance(net.minecraft.world.effect.MobEffects.DIG_SLOWDOWN, 140, 2)); }
                default -> {}
            }
        }
        return ok;
    }

    @Override public boolean causeFallDamage(float f, float m, net.minecraft.world.damagesource.DamageSource s) {
        return !species.flies && super.causeFallDamage(f, m, s);
    }
}
