package com.hyrulecreatures.client;

import com.hyrulecreatures.*;
import java.util.*;
import net.minecraft.client.Minecraft;
import net.minecraft.client.Screenshot;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.phys.Vec3;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.registries.ForgeRegistries;

/** Dev tool (-Phc.showcase): client-side-only lineup that screenshots each creature/pose. */
@Mod.EventBusSubscriber(modid = HyruleCreatures.ID, value = Dist.CLIENT)
public class Showcase {
    record Shot(String name, Species s, int rank, String weapon, String shield, AttackKind k, int t, int down, boolean guard, int aux) {}
    static final List<Shot> SHOTS = new ArrayList<>();
    static {
        Species B = Species.BOKOBLIN;
        SHOTS.add(new Shot("bokoblin_idle_side", B, 0, "boko_club", null, null, 0, 0, false, 0));
        SHOTS.add(new Shot("bokoblin_SMASH_side", B, 0, "boko_club", null, AttackKind.SMASH, 14, 0, false, 0));
        SHOTS.add(new Shot("bokoblin_idle", B, 0, "boko_club", null, null, 0, 0, false, 0));
        for (AttackKind k : new AttackKind[]{AttackKind.SMASH, AttackKind.CHOP, AttackKind.SLASH, AttackKind.LEAP, AttackKind.CHARGE, AttackKind.BASH})
            for (int ph = 0; ph < 3; ph++) {
                int t = ph == 0 ? k.windup : ph == 1 ? k.hits[0] : (k.hits[0] + k.total) / 2;
                SHOTS.add(new Shot("bokoblin_" + k + "_" + ph, B, 0, k == AttackKind.BASH ? "boko_club" : "boko_club", "boko_shield", k, t, 0, false, 0));
            }
        for (int ph = 0; ph < 3; ph++) {
            AttackKind k = AttackKind.MULTI; int[] T = {8, 12, 15};
            SHOTS.add(new Shot("bokoblin_MULTI_" + ph, B, 0, "boko_spear", null, k, T[ph], 0, false, 0));
            k = AttackKind.THRUST;
            SHOTS.add(new Shot("bokoblin_THRUST_" + ph, B, 0, "boko_spear", null, k, new int[]{10, 13, 17}[ph], 0, false, 0));
        }
        SHOTS.add(new Shot("bokoblin_guard", B, 0, "boko_club", "boko_shield", null, 0, 0, true, 0));
        SHOTS.add(new Shot("bokoblin_down", B, 0, "boko_club", null, null, 0, 40, false, 0));
        for (Species s : Species.values()) {
            if (s == B) continue;
            SHOTS.add(new Shot(s.id + "_idle", s, 0, null, null, null, 0, 0, false, 0));
            AttackKind k = s.attack == AttackKind.SHOOT ? AttackKind.SHOOT : s == Species.GUARDIAN ? AttackKind.BEAM : s.attack;
            SHOTS.add(new Shot(s.id + "_atk", s, 0, null, null, k, k.hits[0], 0, false, 0));
        }
        SHOTS.add(new Shot("guardian_legs_broken", Species.GUARDIAN, 0, null, null, null, 0, 0, false, 0b00110101));
        SHOTS.add(new Shot("moblin_SPIN", Species.MOBLIN, 0, "moblin_club", null, AttackKind.SPIN, 20, 0, false, 0));
        SHOTS.add(new Shot("hinox_STOMP", Species.HINOX, 0, "moblin_club", null, AttackKind.STOMP, 20, 0, false, 0));
        SHOTS.add(new Shot("lynel_SMASH", Species.LYNEL, 0, "lynel_crusher", null, AttackKind.SMASH, 17, 0, false, 0));
    }

    static int tick = 0, idx = -1, phase = 0;
    static HyruleBiped cur;

    @SubscribeEvent
    public static void onTick(TickEvent.ClientTickEvent e) {
        if (!Boolean.getBoolean("hc.showcase") || e.phase != TickEvent.Phase.END) return;
        Minecraft mc = Minecraft.getInstance();
        if (mc.level == null || mc.player == null) return;
        ClientLevel lv = mc.level;
        tick++;
        mc.options.hideGui = true;
        if (tick < 120) return;
        if (phase == 0) { // set up next shot
            if (cur != null) cur.discard();
            idx++;
            if (idx >= SHOTS.size()) { System.out.println("SHOWCASE_DONE"); mc.stop(); return; }
            Shot sh = SHOTS.get(idx);
            HyruleBiped m = ModRegistry.TYPES.get(sh.s).get().create(lv);
            double dist = 3.5 + sh.s.h * sh.s.scale * 1.1;
            Vec3 p = mc.player.position();
            mc.player.setYRot(0); mc.player.setXRot(0);
            float yaw = sh.name().endsWith("_side") ? 90 : 180;
            m.moveTo(p.x, p.y + (sh.s.flies ? 1.2 : 0), p.z + dist, yaw, 0);
            m.setYBodyRot(yaw); m.setYHeadRot(yaw); m.setRank(sh.rank);
            if (sh.weapon != null) m.setItemSlot(EquipmentSlot.MAINHAND, new ItemStack(ForgeRegistries.ITEMS.getValue(new net.minecraft.resources.ResourceLocation(HyruleCreatures.ID, sh.weapon))));
            if (sh.shield != null) m.setItemSlot(EquipmentSlot.OFFHAND, new ItemStack(ForgeRegistries.ITEMS.getValue(new net.minecraft.resources.ResourceLocation(HyruleCreatures.ID, sh.shield))));
            m.debugPose(sh.k, sh.t, sh.down, sh.guard, sh.aux);
            lv.putNonPlayerEntity(9000 + idx, m);
            cur = m;
            float mid = sh.s.h * sh.s.scale * 0.5f;
            mc.player.setXRot((float) Math.toDegrees(Math.atan((1.62 - mid) / dist)));
            phase = 1; return;
        }
        if (cur != null) { // hold pose constant (client tick would not advance attack state)
            Shot sh = SHOTS.get(idx); cur.debugPose(sh.k, sh.t, sh.down, sh.guard, sh.aux);
        }
        phase++;
        if (phase == 8) Screenshot.grab(mc.gameDirectory, SHOTS.get(idx).name() + ".png", mc.getMainRenderTarget(), msg -> {});
        if (phase >= 12) phase = 0;
    }
}
