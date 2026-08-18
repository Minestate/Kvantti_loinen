import os
kohteet = [f for f in os.listdir('.') if f.endswith('.py') and f != 'dna_ydin.py' and f != 'iskostaja.py']
import_rivi = 'from dna_ydin import hae_ydin, injektoi\n'
for tiedosto in kohteet:
    with open(tiedosto, 'r+') as f:
        sisalto = f.read()
        if 'dna_ydin' not in sisalto:
            f.seek(0, 0)
            f.write(import_rivi + sisalto)
            print(f'[DNA] Iskustettu: {tiedosto}')
