import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
import sys
from playwright.sync_api import sync_playwright, Page, BrowserContext, Playwright, TimeoutError

# =================================================================================
# === CONFIGURAÇÃO OBRIGATÓRIA (MÉTODO 2) ===
# 1. Cole o caminho para a pasta de dados do seu perfil do Chrome abaixo.
#    Exemplo Windows: "C:\\Users\\SeuUsuario\\AppData\\Local\\Google\\Chrome\\User Data"
#    (Note as duas barras \\ ou use uma barra normal /)
CHROME_PROFILE_PATH = "C:\Users\Usuario\AppData\Local\Google\Chrome\User Data"

# === AVISO IMPORTANTE ===
# Para este método funcionar, o Google Chrome deve estar COMPLETAMENTE FECHADO
# antes de você clicar no botão "Conectar".
# - Feche todas as janelas do Chrome.
# - Verifique no Gerenciador de Tarefas (Ctrl+Shift+Esc) se não há processos "chrome.exe".
# - Verifique no canto inferior direito do Windows (bandeja do sistema) se o ícone do
#   Chrome não está lá. Se estiver, clique com o botão direito e em "Sair".
# =================================================================================


# URL constante para o Web App
WEB_APP_URL = "https://www.ea.com/pt-br/ea-sports-fc/ultimate-team/web-app/"

# -----------------------------------------------------------------------------
# VARIÁVEIS GLOBAIS E DE CONTROLE
# -----------------------------------------------------------------------------
stop_event = threading.Event()

# Variáveis globais para o Playwright
p: Playwright = None
context: BrowserContext = None # <<< MUDANÇA: Usaremos o contexto como principal
page: Page = None

# --- Dicionário de seletores para os slots do DME ---
SELECTORS_SLOTS = {
    1: ".sbc-objective-container .ut-sbc-objective-container", # Exemplo
    2: '#seletor-do-slot-2', # SUBSTITUIR
    3: '#seletor-do-slot-3', # SUBSTITUIR
    4: '#seletor-do-slot-4', # SUBSTITUIR
    5: '#seletor-do-slot-5', # SUBSTITUIR
    6: '#seletor-do-slot-6', # SUBSTITUIR
}
# -----------------------------------------------------------------------------

def pausa_com_verificacao(segundos, stop_event):
    """Função de pausa que verifica o evento de parada a cada segundo."""
    print(f"Pausando por {segundos} segundos. (Pode ser interrompido)")
    for _ in range(segundos):
        if stop_event.is_set():
            break
        time.sleep(1)

# -----------------------------------------------------------------------------
# FUNÇÕES DE AUTOMAÇÃO (Sem alterações aqui, apenas nas mensagens de erro)
# -----------------------------------------------------------------------------

def abrir_pacotes_funcao():
    """Função que executa o fluxo de abrir pacotes usando Playwright."""
    if stop_event.is_set(): return
    if not page:
        print("ERRO: O navegador não foi iniciado. Clique em 'Conectar Usando Perfil do Chrome'.")
        return

    try:
        print("Navegando até a loja...")
        page.locator("button.ut-tab-bar-item.icon-store").click()
        page.wait_for_timeout(1000)
        
        print("Clicando para abrir o pacote...")
        page.locator(".ut-store-pack-details-view .ut-store-reveal-pack-button").click()
        page.wait_for_timeout(3000)

        print("Procurando botão para guardar tudo...")
        guardar_locator = page.get_by_role("button", name="Store All in Club")
        
        if guardar_locator.is_visible():
            guardar_locator.click()
            print("Clicou em 'Guardar Tudo no Clube'.")
        else:
            print("AVISO: Botão 'Guardar Tudo no Clube' não encontrado!")

        if stop_event.is_set(): return
        page.wait_for_timeout(2000)

    except (TimeoutError, Exception) as e:
        print(f"ERRO no Playwright durante a abertura de pacotes: {e}")
        stop_automation()

def automation_loop_pacotes(quantidade, pausa_segundos):
    print(f"Tarefa 'Abrir Pacotes' iniciada ({quantidade} vez(es)).")
    for i in range(quantidade):
        if stop_event.is_set():
            print("\n--- TAREFA INTERROMPIDA PELO USUÁRIO ---")
            break
        print(f"\n--- PACOTES: CICLO {i + 1} de {quantidade} ---")
        abrir_pacotes_funcao()
        if i < quantidade - 1:
            if stop_event.is_set(): break
            pausa_com_verificacao(pausa_segundos, stop_event)
    else:
        print("\n--- TAREFA 'ABRIR PACOTES' CONCLUÍDA ---")
    
    root.after(0, enable_all_start_buttons)

def executar_dme(slot):
    if not page:
        print("ERRO: O navegador não foi iniciado. Clique em 'Conectar Usando Perfil do Chrome'.")
        return
        
    seletor_slot = SELECTORS_SLOTS.get(slot)
    if not seletor_slot:
        print(f"ERRO: Seletor para o slot {slot} não encontrado.")
        return

    try:
        print(f"Clicando no slot {slot} usando o seletor '{seletor_slot}'...")
        page.locator(seletor_slot).click()
        page.wait_for_timeout(1000)
        if stop_event.is_set(): return

        print("Procurando o template...")
        template_locator = page.locator('#seletor-do-template')
        
        if template_locator.is_visible():
            template_locator.click()
            print("Template encontrado e clicado.")
            page.wait_for_timeout(2000)
            if stop_event.is_set(): return
            
            print("Clicando em 'Enviar'...")
            page.locator('#seletor-do-botao-enviar-dme').click()
            page.wait_for_timeout(1000)
        else:
            print("AVISO: Template não encontrado!")
            if page.can_go_back(): page.go_back()
            page.wait_for_timeout(1000)

    except (TimeoutError, Exception) as e:
        print(f"ERRO no Playwright durante o DME: {e}")
        stop_automation()

def automation_loop_dme(quantidade, slot, pausa_segundos):
    print(f"Tarefa 'DME' iniciada (Slot: {slot}, Repetições: {quantidade}).")
    for i in range(quantidade):
        if stop_event.is_set():
            print("\n--- TAREFA INTERROMPIDA PELO USUÁRIO ---")
            break
        print(f"\n--- DME: CICLO {i + 1} de {quantidade} ---")
        executar_dme(slot)
        if i < quantidade - 1:
            if stop_event.is_set(): break
            pausa_com_verificacao(pausa_segundos, stop_event)
    else:
        print("\n--- TAREFA 'DME' CONCLUÍDA ---")
    
    root.after(0, enable_all_start_buttons)

# -----------------------------------------------------------------------------
# LÓGICA DA INTERFACE TKINTER (UI)
# -----------------------------------------------------------------------------

### ----- FUNÇÃO PRINCIPAL MODIFICADA PARA O MÉTODO 2 ----- ###
def initialize_browser():
    """Inicia o Playwright conectando-se a um perfil de usuário existente."""
    global p, context, page
    
    if context:
        print("Conexão com o navegador já parece estar ativa.")
        if page: page.bring_to_front()
        return

    if "COLE_O_CAMINHO" in CHROME_PROFILE_PATH:
        print("="*60)
        print("ERRO DE CONFIGURAÇÃO: O caminho do perfil do Chrome não foi definido.")
        print("Por favor, edite a variável 'CHROME_PROFILE_PATH' no topo do script.")
        print("="*60)
        return
        
    disable_all_start_buttons()
    print("Tentando conectar ao perfil do Chrome...")
    print("AVISO: Certifique-se que o Chrome está COMPLETAMENTE FECHADO!")
    
    def run_playwright():
        global p, context, page
        try:
            p = sync_playwright().start()
            
            # <<< MUDANÇA PRINCIPAL: Usa launch_persistent_context >>>
            context = p.chromium.launch_persistent_context(
                CHROME_PROFILE_PATH,
                headless=False,
                channel="chrome"  # Importante: usa o Chrome instalado e não o do Playwright
            )
            
            page = context.new_page() # Abre uma nova aba no navegador já aberto
            
            print("Conectado ao perfil. Navegando para o Web App...")
            page.goto(WEB_APP_URL)
            
            page.wait_for_selector("button.ut-tab-bar-item.icon-store", timeout=60000)

            print("Conectado ao Web App com sucesso!")
            root.after(0, enable_all_start_buttons)
            root.after(0, lambda: start_browser_button.config(state=tk.DISABLED))
        except TimeoutError:
            print("="*60)
            print("ERRO: A conexão falhou ou demorou demais.")
            print("Causa provável: O Chrome NÃO estava completamente fechado.")
            print("Verifique o Gerenciador de Tarefas e tente novamente.")
            print("="*60)
            if context: context.close()
            root.after(0, enable_all_start_buttons)
            root.after(0, lambda: start_browser_button.config(state=tk.NORMAL))
        except Exception as e:
            print(f"Falha ao iniciar o navegador: {e}")
            if context: context.close()
            root.after(0, enable_all_start_buttons)
            root.after(0, lambda: start_browser_button.config(state=tk.NORMAL))
            
    threading.Thread(target=run_playwright, daemon=True).start()

def start_automation_pacotes():
    if not page:
        print("ERRO: O navegador não foi iniciado. Clique em 'Conectar Usando Perfil do Chrome'.")
        return
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
    if not page:
        print("ERRO: O navegador não foi iniciado. Clique em 'Conectar Usando Perfil do Chrome'.")
        return
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

def stop_automation():
    if stop_button['state'] == tk.NORMAL:
        print("Sinal de parada enviado. O robô irá parar em breve.")
        stop_event.set()
        stop_button.config(state=tk.DISABLED)

def reset_interface():
    print("--- RESETANDO INTERFACE ---")
    stop_event.set()
    log_text.delete(1.0, tk.END)
    
    entry_pacotes_qtd.delete(0, tk.END); entry_pacotes_qtd.insert(0, "5")
    entry_pacotes_pausa.delete(0, tk.END); entry_pacotes_pausa.insert(0, "1")
    entry_dme_qtd.delete(0, tk.END); entry_dme_qtd.insert(0, "10")
    entry_dme_pausa.delete(0, tk.END); entry_dme_pausa.insert(0, "1")
    combo_dme_slot.current(0)
    
    enable_all_start_buttons()
    start_browser_button.config(state=tk.NORMAL if not context else tk.DISABLED)
    print("Interface resetada para o estado inicial.")

def disable_all_start_buttons():
    stop_event.clear()
    start_button_pacotes.config(state=tk.DISABLED)
    start_button_dme.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    log_text.delete(1.0, tk.END)

def enable_all_start_buttons():
    start_button_pacotes.config(state=tk.NORMAL)
    start_button_dme.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

class PrintLogger:
    def __init__(self, textbox): self.textbox = textbox
    def write(self, text): self.textbox.insert(tk.END, text); self.textbox.see(tk.END)
    def flush(self): pass

# --- Interface Principal ---
root = tk.Tk()
root.title("Assistente de Automação v3.2 (Perfil do Chrome)")
root.geometry("520x580")

# --- Frame de Controle do Navegador ---
browser_frame = ttk.Frame(root, padding="10 10 10 0")
# <<< MUDANÇA: Texto do botão atualizado para o Método 2 >>>
start_browser_button = ttk.Button(browser_frame, text="Conectar Usando Perfil do Chrome", command=initialize_browser)
start_browser_button.pack(fill='x', expand=True)
browser_frame.pack(fill='x')

notebook = ttk.Notebook(root, padding="10")

# Aba Abrir Pacotes
frame_pacotes = ttk.Frame(notebook, padding="10")
notebook.add(frame_pacotes, text='Abrir Pacotes')
ttk.Label(frame_pacotes, text="Repetir quantas vezes?").grid(row=0, column=0, padx=5, pady=10, sticky="w")
entry_pacotes_qtd = ttk.Entry(frame_pacotes, width=10); entry_pacotes_qtd.insert(0, "5")
entry_pacotes_qtd.grid(row=0, column=1, padx=5, pady=10, sticky="w")
ttk.Label(frame_pacotes, text="Pausa entre ciclos (seg):").grid(row=1, column=0, padx=5, pady=10, sticky="w")
entry_pacotes_pausa = ttk.Entry(frame_pacotes, width=10); entry_pacotes_pausa.insert(0, "1")
entry_pacotes_pausa.grid(row=1, column=1, padx=5, pady=10, sticky="w")
start_button_pacotes = ttk.Button(frame_pacotes, text="Iniciar 'Abrir Pacotes'", command=start_automation_pacotes)
start_button_pacotes.grid(row=2, column=0, columnspan=2, pady=10)

# Aba DME
frame_dme = ttk.Frame(notebook, padding="10")
notebook.add(frame_dme, text='DME')
ttk.Label(frame_dme, text="Repetir quantas vezes?").grid(row=0, column=0, padx=5, pady=10, sticky="w")
entry_dme_qtd = ttk.Entry(frame_dme, width=10); entry_dme_qtd.insert(0, "10")
entry_dme_qtd.grid(row=0, column=1, padx=5, pady=10, sticky="w")
ttk.Label(frame_dme, text="Qual slot será o DME?").grid(row=1, column=0, padx=5, pady=10, sticky="w")
combo_dme_slot = ttk.Combobox(frame_dme, values=list(SELECTORS_SLOTS.keys()), width=8, state="readonly")
combo_dme_slot.current(0)
combo_dme_slot.grid(row=1, column=1, padx=5, pady=10, sticky="w")
ttk.Label(frame_dme, text="Pausa entre ciclos (seg):").grid(row=2, column=0, padx=5, pady=10, sticky="w")
entry_dme_pausa = ttk.Entry(frame_dme, width=10); entry_dme_pausa.insert(0, "1")
entry_dme_pausa.grid(row=2, column=1, padx=5, pady=10, sticky="w")
start_button_dme = ttk.Button(frame_dme, text="Iniciar 'DME'", command=start_automation_dme)
start_button_dme.grid(row=3, column=0, columnspan=2, pady=10)

notebook.pack(expand=True, fill="both")

# Controles Compartilhados
controls_frame = ttk.Frame(root, padding="0 10 10 10")
stop_button = ttk.Button(controls_frame, text="Parar Tarefa Atual", command=stop_automation, state=tk.DISABLED)
stop_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True)
reset_button = ttk.Button(controls_frame, text="Resetar Interface", command=reset_interface)
reset_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True)
controls_frame.pack(fill="x")

# Log
log_frame = ttk.LabelFrame(root, text="Log de Execução", padding="10")
log_frame.pack(expand=True, fill="both", padx=10, pady=(0, 10))
log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD)
log_text.pack(expand=True, fill="both")
sys.stdout = PrintLogger(log_text)

def on_closing():
    """Função chamada ao fechar a janela para limpar os recursos do Playwright."""
    print("Fechando a aplicação e o navegador...")
    stop_event.set()
    # <<< MUDANÇA: Fecha o contexto, que é o objeto principal no Método 2 >>>
    if context:
        context.close()
    if p:
        p.stop()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()