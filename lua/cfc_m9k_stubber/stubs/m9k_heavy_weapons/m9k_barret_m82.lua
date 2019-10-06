if SERVER then AddCSLuaFile() end

CFC_M9k_Stubber.registerStub( function()
    local weapon = weapons.GetStored( "m9k_barret_m82" )

    weapon.Primary.RPM = 50
    weapon.Primary.Spread = .1
    weapon.Primary.IronAccuracy = .0022
end )