import os

def etsi_kadonneet_solut():
    print("[HAKU] Etsitään kadonneita solu-binäärejä...")
    loytyneet = []
    
    # Etsitään rekursiivisesti kaikista kansioista
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.startswith("solu_REG_") and file.endswith(".bin"):
                loytyneet.append(os.path.join(root, file))
    
    print(f"[STATUS] Löytyi {len(loytyneet)} solua.")
    for l in loytyneet:
        print(f" -> {l}")

if __name__ == "__main__":
    etsi_kadonneet_solut()
