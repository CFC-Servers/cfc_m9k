if SERVER then AddCSLuaFile() end

CFC_M9k_Stubber.registerStub( function()
    local weapon = weapons.GetStored( "m9k_m98b" )

    weapon.Primary.ClipSize = 1
    weapon.Primary.Damage = 1000
    weapon.Primary.Spread = .1
    weapon.Primary.IronAccuracy = .001
end )
