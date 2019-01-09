if SERVER then AddCSLuaFile() end

CFC_M9k_stubber.registerStub(function()
    local weapon = weapons.GetStored("m9k_minigun")

    weapon.Primary.RPM = 1000
    weapon.Primary.DefaultClip = 100
    weapon.Primary.KickDown = 0.2
    weapon.Primary.KickHorizontal = 0.2
    weapon.Primary.NumShots = 2
    weapon.Primary.Damage = 3
    weapon.Primary.Spread = .08
    weapon.Primary.IronAccuracy = .08
end)