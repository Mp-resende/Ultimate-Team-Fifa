import pyautogui as pgui
import time

def minha_funcao():
    # Defina o que sua função faz aqui
    time.sleep(2)
    pgui.leftClick(x=339, y=466)
    pgui.PAUSE = 2
    pgui.leftClick(x=1554, y=784)
    pgui.PAUSE = 1.8
    pgui.leftClick(x=1403, y=1001)
    pgui.PAUSE = 1
    print("Executando minha função!")

# Quantidade de vezes que deseja executar a função
quantidade = 30

# Loop for para executar a função 'quantidade' vezes
for _ in range(quantidade):
    minha_funcao()

 

