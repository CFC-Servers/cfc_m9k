if SERVER then AddCSLuaFile() end

CFC_M9k_Stubber.registerStub( function()
    local weapon = weapons.GetStored( "cw_ak74" )

    weapon.Shots = 1
    weapon.Damage = 33
    weapon.DeployTime = 0.6
end )