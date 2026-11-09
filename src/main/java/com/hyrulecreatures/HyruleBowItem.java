package com.hyrulecreatures;

import net.minecraft.world.item.BowItem;
import net.minecraft.world.item.Item;

public class HyruleBowItem extends BowItem {
    public final int dmg;
    public HyruleBowItem(int durability, int dmg) { super(new Item.Properties().durability(durability)); this.dmg = dmg; }
}
