if SERVER then AddCSLuaFile() end

CFC_M9k_Stubber.registerStub( function()
    local weapon = weapons.GetStored( "m9k_m16a4_acog" )

    weapon.Primary.KickDown = .2
    weapon.Primary.Damage = 25
    weapon.Primary.Spread = .06
    weapon.SelectiveFire = false
end )
