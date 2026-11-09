package com.hyrulecreatures;

import net.minecraft.world.item.*;
import net.minecraft.world.item.crafting.Ingredient;

public class HyruleWeaponItem extends SwordItem {
    public final AttackKind attack;

    public HyruleWeaponItem(int dmg, int durability, float speed, AttackKind attack) {
        super(new Tier() {
            public int getUses() { return durability; }
            public float getSpeed() { return 1; }
            public float getAttackDamageBonus() { return 0; }
            public int getLevel() { return 2; }
            public int getEnchantmentValue() { return 10; }
            public Ingredient getRepairIngredient() { return Ingredient.EMPTY; }
        }, dmg, speed, new Item.Properties());
        this.attack = attack;
    }
}
