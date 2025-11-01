
import time
import threading
import pyautogui
from pynput import keyboard

# --- Variáveis de Controle ---
# Evento para pausar/retomar a thread principal. Começa "setado" (não pausado).
pause_event = threading.Event()
pause_event.set()

# Flag para parar o loop principal e finalizar o script.
running = True

# --- Funções ---

def ctrl_tab_loop():
    """
    Função que executa o loop principal.
    Pressiona Ctrl+Tab a cada 3 segundos enquanto o script não estiver pausado.
    """
    print("Loop iniciado. Pressionando Ctrl+Tab a cada 3 segundos...")
    print("Foque na janela desejada.")
    time.sleep(2) # Pequena pausa para você trocar de janela

    while running:
        # Espera até que o evento seja "setado". Se estiver "limpo" (pausado), ele bloqueia aqui.
        pause_event.wait()

        # Pressiona as teclas
        pyautogui.hotkey('ctrl', 'tab')
        # print(f"{time.strftime('%H:%M:%S')} - Ctrl+Tab pressionado.")

        # Espera 3 segundos
        time.sleep(3)

    print("Loop encerrado.")


def on_press(key):
    """
    Função chamada toda vez que uma tecla é pressionada.
    Controla o estado de pausa e o encerramento do script.
    """
    global running

    try:
        # Usamos 'p' para pausar/retomar
        if key.char == 'p':
            if pause_event.is_set():
                pause_event.clear() # Pausa o loop
                print("\n--- SCRIPT PAUSADO --- (Pressione 'p' para retomar)")
            else:
                pause_event.set() # Retoma o loop
                print("\n--- SCRIPT RETOMADO ---")

    except AttributeError:
        # Lida com teclas especiais como 'esc', 'ctrl', etc.
        if key == keyboard.Key.esc:
            print("\n--- Encerrando o script... ---")
            running = False   # Sinaliza para a thread do loop parar
            pause_event.set() # Libera o loop caso esteja pausado, para que ele possa verificar 'running'
            return False      # Para o listener do teclado

# --- Execução Principal ---

if __name__ == "__main__":
    print("="*40)
    print("Automatizador de Ctrl+Tab")
    print("Instruções:")
    print(" - Pressione 'p' a qualquer momento para pausar ou retomar.")
    print(" - Pressione 'Esc' para encerrar o script.")
    print("="*40)

    # 1. Cria e inicia a thread para o loop de Ctrl+Tab
    main_thread = threading.Thread(target=ctrl_tab_loop)
    main_thread.start()

    # 2. Inicia o listener do teclado no thread principal
    # O listener vai bloquear a execução aqui até que ele seja parado (pressionando Esc)
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    # Garante que a thread do loop termine antes de o script principal fechar
    main_thread.join()