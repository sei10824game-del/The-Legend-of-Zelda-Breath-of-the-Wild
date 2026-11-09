package com.hyrulecreatures;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import java.io.InputStreamReader;
import java.util.*;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.*;
import net.minecraft.world.item.*;
import net.minecraftforge.common.ForgeSpawnEggItem;
import net.minecraftforge.registries.*;

public final class ModRegistry {
    public static final DeferredRegister<EntityType<?>> ENTITIES = DeferredRegister.create(ForgeRegistries.ENTITY_TYPES, HyruleCreatures.ID);
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(ForgeRegistries.ITEMS, HyruleCreatures.ID);
    public static final DeferredRegister<CreativeModeTab> TABS = DeferredRegister.create(Registries.CREATIVE_MODE_TAB, HyruleCreatures.ID);

    public static final Map<Species, RegistryObject<EntityType<HyruleBiped>>> TYPES = new EnumMap<>(Species.class);

    static {
        for (Species s : Species.values()) {
            TYPES.put(s, ENTITIES.register(s.id, () -> EntityType.Builder.<HyruleBiped>of(
                    (t, l) -> s.flies ? new Keese(t, l, s) : new HyruleBiped(t, l, s), MobCategory.MONSTER)
                    .sized(s.w, s.h).clientTrackingRange(10).build(s.id)));
            int[] c = switch (s) { case BOKOBLIN -> new int[]{0xc8452f, 0xe8dcb8}; case MOBLIN -> new int[]{0xa4552f, 0x3a2418};
                case LIZALFOS -> new int[]{0x5a9a3a, 0xe0d08a}; default -> new int[]{0x3a3040, 0xff4040}; };
            ITEMS.register(s.id + "_spawn_egg", () -> new ForgeSpawnEggItem(TYPES.get(s), c[0], c[1], new Item.Properties()));
        }
        JsonObject[] ws = new Gson().fromJson(new InputStreamReader(ModRegistry.class.getResourceAsStream(
                "/assets/" + HyruleCreatures.ID + "/weapons.json")), JsonObject[].class);
        for (JsonObject w : ws) {
            String kind = w.get("kind").getAsString();
            AttackKind ak = switch (kind) { case "club", "claymore" -> AttackKind.SMASH; case "spear", "halberd" -> AttackKind.THRUST; default -> AttackKind.SLASH; };
            float speed = switch (kind) { case "club" -> -3.0f; case "claymore" -> -3.2f; case "spear" -> -2.7f; case "halberd" -> -3.0f; default -> -2.4f; };
            int dmg = w.get("dmg").getAsInt(), dur = w.get("dur").getAsInt();
            ITEMS.register(w.get("id").getAsString(), () -> new HyruleWeaponItem(dmg, dur, speed, ak));
        }
    }

    public static final RegistryObject<CreativeModeTab> TAB = TABS.register("main", () -> CreativeModeTab.builder()
            .title(Component.translatable("itemGroup." + HyruleCreatures.ID))
            .icon(() -> new ItemStack(ITEMS.getEntries().stream().filter(e -> e.getId().getPath().equals("master_sword")).findFirst().get().get()))
            .displayItems((p, o) -> ITEMS.getEntries().forEach(e -> o.accept(e.get()))).build());

    private ModRegistry() {}
}
