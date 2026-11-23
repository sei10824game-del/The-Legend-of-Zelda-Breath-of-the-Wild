package com.hyrulecreatures;

import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;

/** Fire / Ice / Lightning Rod: right-click shoots an elemental ball. */
public class HyruleRodItem extends HyruleWeaponItem {
    public HyruleRodItem(int dmg, int dur, float speed, int element) { super(dmg, dur, speed, AttackKind.SLASH, Style.ONE, element); }

    @Override public InteractionResultHolder<ItemStack> use(Level level, Player pl, InteractionHand hand) {
        ItemStack st = pl.getItemInHand(hand);
        if (!level.isClientSide) {
            Shot s = new Shot(level, pl, element, new ItemStack(ModRegistry.shotItem(element)), 4 + attackDamageBonus());
            s.shootFromRotation(pl, pl.getXRot(), pl.getYRot(), 0, 1.6f, 0.5f);
            level.addFreshEntity(s);
            level.playSound(null, pl.getX(), pl.getY(), pl.getZ(), SoundEvents.BLAZE_SHOOT, SoundSource.PLAYERS, 0.8f, 1.2f);
            st.hurtAndBreak(1, pl, p -> p.broadcastBreakEvent(hand));
        }
        pl.getCooldowns().addCooldown(this, 20);
        return InteractionResultHolder.sidedSuccess(st, level.isClientSide);
    }
    private float attackDamageBonus() { return 3f; }
}
