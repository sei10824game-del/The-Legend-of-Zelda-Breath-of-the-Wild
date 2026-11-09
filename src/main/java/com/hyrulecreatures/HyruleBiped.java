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

    @Override public boolean causeFallDamage(float f, float m, net.minecraft.world.damagesource.DamageSource s) {
        return !species.flies && super.causeFallDamage(f, m, s);
    }
}
