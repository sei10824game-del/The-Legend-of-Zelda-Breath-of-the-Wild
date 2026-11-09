package com.hyrulecreatures;

import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.ai.control.FlyingMoveControl;
import net.minecraft.world.entity.ai.navigation.*;
import net.minecraft.world.level.Level;

public class Keese extends HyruleBiped {
    public Keese(EntityType<? extends HyruleBiped> t, Level l, Species s) {
        super(t, l, s);
        moveControl = new FlyingMoveControl(this, 20, true);
        setNoGravity(true);
    }
    @Override protected PathNavigation createNavigation(Level l) {
        FlyingPathNavigation n = new FlyingPathNavigation(this, l);
        n.setCanOpenDoors(false); n.setCanFloat(true); n.setCanPassDoors(true);
        return n;
    }
}
