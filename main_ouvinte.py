# main_ouvinte.py
import asyncio
from listener import ouvinte_sinais_tecnicos

if __name__ == "__main__":
    asyncio.run(ouvinte_sinais_tecnicos())
  
