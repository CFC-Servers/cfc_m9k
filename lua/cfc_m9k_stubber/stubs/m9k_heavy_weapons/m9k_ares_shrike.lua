if SERVER then AddCSLuaFile() end

CFC_M9k_stubber.registerStub(function()
    local weapon = weapons.GetStored("m9k_ares_shrike")

    weapon.Primary.Ammo = "AirboatGun"
    weapon.Primary.Damage = 20
    weapon.Primary.Spread = .08
end)