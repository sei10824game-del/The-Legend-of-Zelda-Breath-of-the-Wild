package com.hyrulecreatures;

import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.entity.player.Player;
import net.minecraftforge.event.entity.living.LivingHurtEvent;
import net.minecraftforge.event.entity.player.PlayerInteractEvent;
import net.minecraftforge.event.entity.player.ItemTooltipEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.registries.ForgeRegistries;

/** Tears-of-the-Kingdom style fusion: sneak + right-click a weapon with a material in the off-hand. */
public class FusionEvents {
    static final String TAG = "hc_fuse";

    static int bonus(ItemStack mat) {
        String id = ForgeRegistries.ITEMS.getKey(mat.getItem()).getPath();
        if (id.endsWith("_horn")) return 4;
        if (id.endsWith("_fang")) return 3;
        if (id.endsWith("_guts")) return 2;
        if (mat.is(net.minecraft.world.item.Items.BLAZE_ROD) || mat.is(net.minecraft.world.item.Items.DIAMOND) || mat.is(net.minecraft.world.item.Items.NETHERITE_SCRAP)) return 4;
        return 2;
    }
    /** 0 none, 1 fire, 2 ice, 3 shock */
    static int element(ItemStack mat) {
        var i = mat.getItem();
        if (i == net.minecraft.world.item.Items.BLAZE_ROD || i == net.minecraft.world.item.Items.MAGMA_CREAM || i == net.minecraft.world.item.Items.FIRE_CHARGE) return 1;
        if (i == net.minecraft.world.item.Items.SNOWBALL || i == net.minecraft.world.item.Items.BLUE_ICE || i == net.minecraft.world.item.Items.PACKED_ICE) return 2;
        if (i == net.minecraft.world.item.Items.COPPER_INGOT || i == net.minecraft.world.item.Items.LIGHTNING_ROD || i == net.minecraft.world.item.Items.GLOWSTONE_DUST) return 3;
        String p = ForgeRegistries.ITEMS.getKey(i).getPath();
        return p.contains("fire") || p.contains("keese_fire") ? 1 : p.contains("ice") || p.contains("frost") ? 2 : p.contains("elec") || p.contains("thunder") ? 3 : 0;
    }

    @SubscribeEvent
    public void onUse(PlayerInteractEvent.RightClickItem e) {
        Player p = e.getEntity();
        if (!p.isShiftKeyDown() || e.getHand() != InteractionHand.MAIN_HAND) return;
        ItemStack w = p.getMainHandItem(), m = p.getOffhandItem();
        if (!(w.getItem() instanceof HyruleWeaponItem) || w.getItem() instanceof HyruleRodItem || m.isEmpty() || w.getOrCreateTag().contains(TAG)) return;
        if (!p.level().isClientSide) {
            CompoundTag t = w.getOrCreateTag(); t.putString(TAG, ForgeRegistries.ITEMS.getKey(m.getItem()).toString());
            t.putInt("hc_bonus", bonus(m)); t.putInt("hc_el", element(m));
            w.setDamageValue(Math.max(0, w.getDamageValue() - w.getMaxDamage() / 4)); // fusing also repairs a bit
            m.shrink(1);
            p.level().playSound(null, p.getX(), p.getY(), p.getZ(), SoundEvents.ANVIL_USE, SoundSource.PLAYERS, 0.8f, 1.6f);
        }
        e.setCanceled(true);
    }

    @SubscribeEvent
    public void onHurt(LivingHurtEvent e) {
        if (!(e.getSource().getEntity() instanceof LivingEntity a)) return;
        ItemStack w = a.getMainHandItem();
        if (!w.hasTag() || !w.getTag().contains(TAG)) return;
        e.setAmount(e.getAmount() + w.getTag().getInt("hc_bonus"));
        LivingEntity t = e.getEntity();
        switch (w.getTag().getInt("hc_el")) {
            case 1 -> t.setSecondsOnFire(4);
            case 2 -> { t.setTicksFrozen(t.getTicksRequiredToFreeze() + 100); t.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 80, 2)); }
            case 3 -> t.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 100, 1));
            default -> {}
        }
    }

    @SubscribeEvent
    public void tip(ItemTooltipEvent e) {
        ItemStack w = e.getItemStack();
        if (w.hasTag() && w.getTag().contains(TAG)) e.getToolTip().add(Component.literal("§bFused: " + w.getTag().getString(TAG) + " (+" + w.getTag().getInt("hc_bonus") + ")"));
        else if (w.getItem() instanceof HyruleWeaponItem && !(w.getItem() instanceof HyruleRodItem)) e.getToolTip().add(Component.literal("§7Sneak + right-click with a material in the off-hand to fuse"));
    }
}
