document.getElementById("dmg").addEventListener('input', calculate);
document.getElementById("frag").addEventListener('input', calculate);
document.getElementById("wr").addEventListener('input', calculate);
document.getElementById("spot").addEventListener('input', calculate);
document.getElementById("def").addEventListener('input', calculate);

function calculate(){
    var dmg = document.getElementById('dmg').value;
    var frag = document.getElementById('frag').value;
    var wr = document.getElementById('wr').value;
    var spot = document.getElementById('spot').value;
    var def = document.getElementById('def').value;

    document.getElementById('result_wn8').innerHTML = 10;
}

function calculate_wn8(dmg, frag, wr, spot, def){

}

function calculate_wn8(tankId, avgDmg, avgSpot, avgFrag, avgDef, avgWinRate){
    model = TankExpectations.objects.filter(tank_id=tankId)[0]
    rDAMAGE = avgDmg / model.exp_Damage
    rSPOT = avgSpot / model.exp_Spot
    rFRAG = avgFrag / model.exp_Frag
    rDEF = avgDef / model.exp_Def
    rWIN = avgWinRate / model.exp_WinRate

    rWINc = max(0, (rWIN - 0.71) / (1 - 0.71))
    rDAMAGEc = max(0, (rDAMAGE - 0.22) / (1 - 0.22))
    rFRAGc = max(0, min(rDAMAGEc + 0.2, (rFRAG - 0.12) / (1 - 0.12)))
    rSPOTc = max(0, min(rDAMAGEc + 0.1, (rSPOT - 0.38) / (1 - 0.38)))
    rDEFc = max(0, min(rDAMAGEc + 0.1, (rDEF - 0.10) / (1 - 0.10)))

    WN8 = 980 * rDAMAGEc + 210 * rDAMAGEc * rFRAGc + 155 * rFRAGc * rSPOTc + 75 * rDEFc * rFRAGc + 145 * min(1.8,
                                                                                                             rWINc)
    return round(WN8)
}