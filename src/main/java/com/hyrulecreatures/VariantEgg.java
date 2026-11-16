package com.hyrulecreatures;

import java.util.function.Supplier;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.item.ItemStack;
import net.minecraftforge.common.ForgeSpawnEggItem;

/** Spawn egg that always spawns one specific rank (colour variant). Use the creative-tab stack: /give gives a random-rank egg. */
public class VariantEgg extends ForgeSpawnEggItem {
    private final int rank;
    public VariantEgg(Supplier<? extends EntityType<? extends Mob>> type, int rank) { super(type, 0xFFFFFF, 0xFFFFFF, new Properties()); this.rank = rank; }
    @Override public ItemStack getDefaultInstance() {
        ItemStack s = super.getDefaultInstance();
        s.getOrCreateTagElement("EntityTag").putInt("Rank", rank);
        return s;
    }
}
