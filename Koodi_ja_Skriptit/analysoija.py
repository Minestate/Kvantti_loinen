import json
import base64

def luokittele_massa():
    tilasto = {"koodi": 0, "teksti": 0, "binääri": 0}
    
    with open("ledger.json", "r") as f:
        for line in f:
            tapahtuma = json.loads(line)
            sisalto = tapahtuma.get("sisältö", "")
            
            # Yksinkertainen heuristiikka:
            if sisalto.endswith("=="): # Todennäköisesti Base64-binääriä
                tilasto["binääri"] += len(sisalto)
            elif any(x in sisalto for x in ["def ", "class ", "import "]):
                tilasto["koodi"] += len(sisalto)
            else:
                tilasto["teksti"] += len(sisalto)
    
    return tilasto

#
