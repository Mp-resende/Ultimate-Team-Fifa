import tkinter as tk
from tkinter import ttk, scrolledtext
import pyautogui as pgui
import time
import threading
import sys
# import keyboard <-- Removido, pois não era usado e conflitava com a variável 'keyboard'
from pynput.keyboard import Key, Controller

# -----------------------------------------------------------------------------
# VARIÁVEIS GLOBAIS E DE CONTROLE
# -----------------------------------------------------------------------------
stop_event = threading.Event()
keyboard = Controller()

# -----------------------------------------------------------------------------
# FUNÇÃO DE PAUSA INTELIGENTE
# -----------------------------------------------------------------------------
def pausa_com_verificacao(segundos, stop_event):
    print(f"Pausando por {segundos} segundos. (Pode ser interrompido)")
    for _ in range(segundos):
        if stop_event.is_set():
            break
        time.sleep(1)

# -----------------------------------------------------------------------------
# FUNÇÕES DE AUTOMAÇÃO
# -----------------------------------------------------------------------------
def abrir_pacotes_funcao():
    if stop_event.is_set(): return
    print("Clicando para abrir o pacote...")
    time.sleep(1)
    pgui.leftClick(x=283, y=644, duration=0.5)

    if stop_event.is_set(): return
    time.sleep(1.5)
    print("Procurando Organizar não atribuído...")
    OrganizarNaoAtribuido = pgui.locateCenterOnScreen("organizarNaoAtt.png", confidence=0.8)
    OrganizarNaoAtribuido2 = pgui.locateCenterOnScreen("organizarNaoAtt2.png", confidence=0.8)
    clicar_levemeparala = pgui.locateCenterOnScreen("levemeparala.png", confidence=0.9) 
    if not OrganizarNaoAtribuido and not clicar_levemeparala:
        print("AVISO: 'SendToClub' ou 'levemeparala' não encontrados.")
        return
    
    if OrganizarNaoAtribuido: pgui.click(OrganizarNaoAtribuido, duration=0.5); print("Clicou em 'organizarNaoAtt.png'.")
    elif clicar_levemeparala: 
        pgui.click(clicar_levemeparala, duration=0.5); 
        print("Clicou em 'levemeparala.png'."); 
        time.sleep(1.5) 
        if OrganizarNaoAtribuido2: 
            pgui.click(OrganizarNaoAtribuido2, duration=0.5); 
            print("Clicou em 'organizarNaoAtt.png'.")
            time.sleep(1.5)
        else: print("AVISO: 'SendToClub' ou 'levemeparala' não encontrados.")

    # if stop_event.is_set(): return
    # time.sleep(1.5)
    # print("Procurando 'OrganizarNaoAttt.png' novamente...")
    # # OrganizarNaoAtribuido = pgui.locateCenterOnScreen("organizarNaoAtt.png", confidence=0.9)
    # # if OrganizarNaoAtribuido: pgui.click(OrganizarNaoAtribuido, duration=0.5); print("Clicou em 'organizarNaoAtt.png' (2ª vez).")
    # else: print("AVISO: Imagem 'organizarNaoAtt.png' (2ª vez) não encontrada!")

    # if stop_event.is_set(): return
    # time.sleep(1.5)
    # print("Procurando 'enviar_armazem.png'...")
    # enviar_armazem = pgui.locateCenterOnScreen("enviar_armazem.png", confidence=0.9)
    # if enviar_armazem: pgui.click(enviar_armazem); print("Clicou em 'enviar_armazem.png'.")
    # else: print("AVISO: Imagem 'enviar_armazem.png' não encontrada!")

    if stop_event.is_set(): return
    time.sleep(3)
    print("Voltando para a loja...")
    keyboard.press('1')
    time.sleep(1)

def automation_loop_pacotes(quantidade, pausa_segundos):
    print(f"Tarefa 'Abrir Pacotes' iniciada ({quantidade} vez(es)).")
    print("Aguarde 2 segundos para focar na janela de destino...")
    time.sleep(2)

    for i in range(quantidade):
        if stop_event.is_set(): print("\n--- TAREFA INTERROMPIDA PELO USUÁRIO ---"); break
        print(f"\n--- PACOTES: CICLO {i + 1} de {quantidade} ---")
        abrir_pacotes_funcao()
        if i < quantidade - 1:
            if stop_event.is_set(): break
            pausa_com_verificacao(pausa_segundos, stop_event)
    else:
        print("\n--- TAREFA 'ABRIR PACOTES' CONCLUÍDA ---")
    
    enable_all_start_buttons()

COORDENADAS_SLOTS = {1: (280, 395), 2: (745, 523), 3: (1189, 501), 4: (1671, 572), 5: (327, 937), 6: (772, 931)}

def executar_dme(slot):
    coordenadas = COORDENADAS_SLOTS.get(slot, COORDENADAS_SLOTS[1])
    print(f"Clicando no slot {slot} em {coordenadas}...")
    pgui.leftClick(x=coordenadas[0], y=coordenadas[1])
    time.sleep(1)
    if stop_event.is_set(): return
    print("Procurando 'template.png'...")
    time.sleep(1)
    keyboard.press('t')  # Pressiona 't' para abrir o template
    time.sleep(4)
    keyboard.press('s')
    time.sleep(1)
    # (Restante do código comentado permanece igual)

def automation_loop_dme(quantidade, slot, pausa_segundos):
    print(f"Tarefa 'DME' iniciada (Slot: {slot}, Repetições: {quantidade}).")
    print("Aguarde 2 segundos para focar na janela de destino...")
    time.sleep(2)

    for i in range(quantidade):
        if stop_event.is_set(): print("\n--- TAREFA INTERROMPIDA PELO USUÁRIO ---"); break
        print(f"\n--- DME: CICLO {i + 1} de {quantidade} ---")
        executar_dme(slot)
        if i < quantidade - 1:
            if stop_event.is_set(): break
            pausa_com_verificacao(pausa_segundos, stop_event)
    else:
        print("\n--- TAREFA 'DME' CONCLUÍDA ---")
    
    enable_all_start_buttons()

# -----------------------------------------------------------------------------
# <<< NOVAS FUNÇÕES PARA DME DIÁRIOS >>>
# -----------------------------------------------------------------------------

def executar_dme_diario(slot):
    """Cópia da função executar_dme, para a nova aba."""
    coordenadas = COORDENADAS_SLOTS.get(slot, COORDENADAS_SLOTS[1])
    print(f"[DME DIÁRIO] Clicando no slot {slot} em {coordenadas}...")
    pgui.leftClick(x=coordenadas[0], y=coordenadas[1])
    time.sleep(1)
    if stop_event.is_set(): return

    irParaDesafio = pgui.locateCenterOnScreen("irParaDesafio.png", confidence=0.9)
    comecarDesafio = pgui.locateCenterOnScreen("comecarDesafio.png", confidence=0.9)

    if irParaDesafio or comecarDesafio: 
        pgui.click(irParaDesafio)
        pgui.click(comecarDesafio)
        print("[DME DIÁRIO] Clicou em 'irParaDesafio.png'.")
    else:
        return

    print("[DME DIÁRIO] Procurando 'template.png'...")
    time.sleep(1.5)
    keyboard.press('a') # Clicar em autocomplete SBC
    time.sleep(1)
    build = pgui.locateCenterOnScreen("build.png", confidence=0.9)
    if build:
        pgui.click(build)
        print("[DME DIÁRIO] Clicou em 'build.png'.")
    else:
        print("[DME DIÁRIO] AVISO: Imagem 'build.png' não encontrada!")
        return
    time.sleep(2)
    keyboard.press('s')
    time.sleep(1.5)
    # (Restante do código comentado permanece igual)

def automation_loop_dme_diario(quantidade, slot, pausa_segundos):
    """Loop de automação para a função DME Diário."""
    print(f"Tarefa 'DME DIÁRIO' iniciada (Slot: {slot}, Repetições: {quantidade}).")
    print("Aguarde 2 segundos para focar na janela de destino...")
    time.sleep(2)

    for i in range(quantidade):
        if stop_event.is_set(): print("\n--- TAREFA INTERROMPIDA PELO USUÁRIO ---"); break
        print(f"\n--- DME DIÁRIO: CICLO {i + 1} de {quantidade} ---")
        executar_dme_diario(slot) # Chama a nova função
        if i < quantidade - 1:
            if stop_event.is_set(): break
            pausa_com_verificacao(pausa_segundos, stop_event)
    else:
        print("\n--- TAREFA 'DME DIÁRIO' CONCLUÍDA ---")
    
    enable_all_start_buttons()

# -----------------------------------------------------------------------------
# LÓGICA DA INTERFACE TKINTER (UI)
# -----------------------------------------------------------------------------
def start_automation_pacotes():
    try:
        quantidade = int(entry_pacotes_qtd.get())
        pausa = int(entry_pacotes_pausa.get())
        if quantidade <= 0 or pausa < 0: raise ValueError
        disable_all_start_buttons()
        thread = threading.Thread(target=automation_loop_pacotes, args=(quantidade, pausa), daemon=True)
        thread.start()
    except ValueError:
        print("ERRO: Insira valores numéricos válidos (Qtd > 0, Pausa >= 0).")

def start_automation_dme():
    try:
        quantidade = int(entry_dme_qtd.get())
        slot = int(combo_dme_slot.get())
        pausa = int(entry_dme_pausa.get())
        if quantidade <= 0 or pausa < 0: raise ValueError
        disable_all_start_buttons()
        thread = threading.Thread(target=automation_loop_dme, args=(quantidade, slot, pausa), daemon=True)
        thread.start()
    except (ValueError, tk.TclError):
        print("ERRO: Insira valores válidos para 'DME' (Qtd, Slot, Pausa).")

# <<< NOVA FUNÇÃO DE START PARA DME DIÁRIOS >>>
def start_automation_dme_diario():
    try:
        quantidade = int(entry_dme_diario_qtd.get())
        slot = int(combo_dme_diario_slot.get())
        pausa = int(entry_dme_diario_pausa.get())
        if quantidade <= 0 or pausa < 0: raise ValueError
        disable_all_start_buttons()
        thread = threading.Thread(target=automation_loop_dme_diario, args=(quantidade, slot, pausa), daemon=True)
        thread.start()
    except (ValueError, tk.TclError):
        print("ERRO: Insira valores válidos para 'DME Diário' (Qtd, Slot, Pausa).")

def stop_automation():
    if stop_button['state'] == tk.NORMAL:
        print("Sinal de parada enviado. O robô irá parar em breve.")
        stop_event.set()
        stop_button.config(state=tk.DISABLED)

# <<< MODIFICADO >>>
def reset_interface():
    print("--- RESETANDO INTERFACE ---")
    stop_event.set() 
    log_text.delete(1.0, tk.END)

    # Resetar Aba Pacotes
    entry_pacotes_qtd.delete(0, tk.END)
    entry_pacotes_qtd.insert(0, "5")
    entry_pacotes_pausa.delete(0, tk.END)
    entry_pacotes_pausa.insert(0, "1")

    # Resetar Aba DME
    entry_dme_qtd.delete(0, tk.END)
    entry_dme_qtd.insert(0, "10")
    entry_dme_pausa.delete(0, tk.END)
    entry_dme_pausa.insert(0, "1")
    combo_dme_slot.current(0)
    
    # <<< NOVO >>> Resetar Aba DME Diários
    entry_dme_diario_qtd.delete(0, tk.END)
    entry_dme_diario_qtd.insert(0, "3") # Valor padrão diferente
    entry_dme_diario_pausa.delete(0, tk.END)
    entry_dme_diario_pausa.insert(0, "1")
    combo_dme_diario_slot.current(0)

    enable_all_start_buttons()
    print("Interface resetada para o estado inicial.")

# <<< MODIFICADO >>>
def disable_all_start_buttons():
    stop_event.clear()
    start_button_pacotes.config(state=tk.DISABLED)
    start_button_dme.config(state=tk.DISABLED)
    start_button_dme_diario.config(state=tk.DISABLED) # <<< ADICIONADO
    stop_button.config(state=tk.NORMAL)
    log_text.delete(1.0, tk.END)

# <<< MODIFICADO >>>
def enable_all_start_buttons():
    start_button_pacotes.config(state=tk.NORMAL)
    start_button_dme.config(state=tk.NORMAL)
    start_button_dme_diario.config(state=tk.NORMAL) # <<< ADICIONADO
    stop_button.config(state=tk.DISABLED)

class PrintLogger:
    def __init__(self, textbox): self.textbox = textbox
    def write(self, text): self.textbox.insert(tk.END, text); self.textbox.see(tk.END)
    def flush(self): pass

root = tk.Tk()
root.title("Assistente de Automação v2.4") # Versão atualizada
root.geometry("500x520")
notebook = ttk.Notebook(root, padding="10")

# --- Aba 1: Abrir Pacotes ---
frame_pacotes = ttk.Frame(notebook, padding="10")
notebook.add(frame_pacotes, text='Abrir Pacotes')
ttk.Label(frame_pacotes, text="Repetir quantas vezes?").grid(row=0, column=0, padx=5, pady=10, sticky="w")
entry_pacotes_qtd = ttk.Entry(frame_pacotes, width=10)
entry_pacotes_qtd.insert(0, "5")
entry_pacotes_qtd.grid(row=0, column=1, padx=5, pady=10, sticky="w")
ttk.Label(frame_pacotes, text="Pausa entre ciclos (seg):").grid(row=1, column=0, padx=5, pady=10, sticky="w")
entry_pacotes_pausa = ttk.Entry(frame_pacotes, width=10)
entry_pacotes_pausa.insert(0, "1")
entry_pacotes_pausa.grid(row=1, column=1, padx=5, pady=10, sticky="w")
start_button_pacotes = ttk.Button(frame_pacotes, text="Iniciar 'Abrir Pacotes'", command=start_automation_pacotes)
start_button_pacotes.grid(row=2, column=0, columnspan=2, pady=10)

# --- Aba 2: DME ---
frame_dme = ttk.Frame(notebook, padding="10")
notebook.add(frame_dme, text='DME')
ttk.Label(frame_dme, text="Repetir quantas vezes?").grid(row=0, column=0, padx=5, pady=10, sticky="w")
entry_dme_qtd = ttk.Entry(frame_dme, width=10)
entry_dme_qtd.insert(0, "10")
entry_dme_qtd.grid(row=0, column=1, padx=5, pady=10, sticky="w")
ttk.Label(frame_dme, text="Qual slot será o DME?").grid(row=1, column=0, padx=5, pady=10, sticky="w")
combo_dme_slot = ttk.Combobox(frame_dme, values=[1, 2, 3, 4, 5, 6], width=8, state="readonly")
combo_dme_slot.current(0)
combo_dme_slot.grid(row=1, column=1, padx=5, pady=10, sticky="w")
ttk.Label(frame_dme, text="Pausa entre ciclos (seg):").grid(row=2, column=0, padx=5, pady=10, sticky="w")
entry_dme_pausa = ttk.Entry(frame_dme, width=10)
entry_dme_pausa.insert(0, "1")
entry_dme_pausa.grid(row=2, column=1, padx=5, pady=10, sticky="w")
start_button_dme = ttk.Button(frame_dme, text="Iniciar 'DME'", command=start_automation_dme)
start_button_dme.grid(row=3, column=0, columnspan=2, pady=10)

# -----------------------------------------------------------------------------
# <<< NOVA ABA: DME DIÁRIOS >>>
# -----------------------------------------------------------------------------
frame_dme_diario = ttk.Frame(notebook, padding="10")
notebook.add(frame_dme_diario, text='DME Diários')

ttk.Label(frame_dme_diario, text="Repetir quantas vezes?").grid(row=0, column=0, padx=5, pady=10, sticky="w")
entry_dme_diario_qtd = ttk.Entry(frame_dme_diario, width=10)
entry_dme_diario_qtd.insert(0, "3") # Valor padrão
entry_dme_diario_qtd.grid(row=0, column=1, padx=5, pady=10, sticky="w")

ttk.Label(frame_dme_diario, text="Qual slot será o DME?").grid(row=1, column=0, padx=5, pady=10, sticky="w")
combo_dme_diario_slot = ttk.Combobox(frame_dme_diario, values=[1, 2, 3, 4, 5, 6], width=8, state="readonly")
combo_dme_diario_slot.current(0)
combo_dme_diario_slot.grid(row=1, column=1, padx=5, pady=10, sticky="w")

ttk.Label(frame_dme_diario, text="Pausa entre ciclos (seg):").grid(row=2, column=0, padx=5, pady=10, sticky="w")
entry_dme_diario_pausa = ttk.Entry(frame_dme_diario, width=10)
entry_dme_diario_pausa.insert(0, "1")
entry_dme_diario_pausa.grid(row=2, column=1, padx=5, pady=10, sticky="w")

start_button_dme_diario = ttk.Button(frame_dme_diario, text="Iniciar 'DME Diário'", command=start_automation_dme_diario)
start_button_dme_diario.grid(row=3, column=0, columnspan=2, pady=10)
# -----------------------------------------------------------------------------

notebook.pack(expand=True, fill="both")

# --- Controles Compartilhados (Fora das Abas) ---
controls_frame = ttk.Frame(root, padding="0 10 10 10")
stop_button = ttk.Button(controls_frame, text="Parar Tarefa Atual", command=stop_automation, state=tk.DISABLED)
stop_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True)

reset_button = ttk.Button(controls_frame, text="Resetar Interface", command=reset_interface)
reset_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True)
controls_frame.pack(fill="x")

# --- Log ---
log_frame = ttk.LabelFrame(root, text="Log de Execução", padding="10")
log_frame.pack(expand=True, fill="both", padx=10, pady=(0, 10))
log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD)
log_text.pack(expand=True, fill="both")

sys.stdout = PrintLogger(log_text)
root.mainloop()