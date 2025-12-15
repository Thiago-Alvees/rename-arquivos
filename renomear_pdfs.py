import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import fitz  # PyMuPDF
from PIL import Image, ImageTk

# Variável global para armazenar a área selecionada
rect_selecionado = None

def limpar_nome(nome):
    """Remove caracteres inválidos do Windows"""
    return re.sub(r'[\\/*?:"<>|]', "_", nome.strip())

def selecionar_pasta():
    pasta = filedialog.askdirectory(title="Selecione a pasta com os PDFs")
    if pasta:
        entry_pasta.delete(0, tk.END)
        entry_pasta.insert(0, pasta)

def escolher_area():
    """Permite selecionar a área de referência em um PDF de exemplo"""
    global rect_selecionado

    caminho_pdf = filedialog.askopenfilename(
        title="Selecione um PDF de exemplo",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )
    if not caminho_pdf:
        return

    seletor = tk.Toplevel(janela)
    seletor.title("Selecionar área de referência")
    seletor.geometry("1000x800")
    seletor.configure(bg="white")

    try:
        doc = fitz.open(caminho_pdf)
    except Exception as e:
        messagebox.showerror("Erro ao abrir PDF", f"Não foi possível abrir o arquivo:\n{e}")
        seletor.destroy()
        return

    pagina_atual = 0
    zoom = 3
    img_tk = None
    start_x = start_y = None
    rect_id = None

    canvas = tk.Canvas(seletor, bg="white")
    canvas.pack(expand=True, fill="both")

    def exibir_pagina():
        nonlocal img_tk
        pagina = doc.load_page(pagina_atual)
        pix = pagina.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img_tk = ImageTk.PhotoImage(img)
        canvas.delete("all")
        canvas.create_image(0, 0, anchor="nw", image=img_tk)
        canvas.img_tk = img_tk  # mantém referência viva

    def ao_pressionar(event):
        nonlocal start_x, start_y, rect_id
        start_x, start_y = event.x, event.y
        if rect_id:
            canvas.delete(rect_id)
        rect_id = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline="red", width=2)

    def ao_arrastar(event):
        nonlocal rect_id
        if rect_id:
            canvas.coords(rect_id, start_x, start_y, event.x, event.y)

    def ao_soltarselecao(event):
        nonlocal rect_id
        global rect_selecionado
        if not rect_id:
            return

        x0, y0, x1, y1 = canvas.coords(rect_id)
        if x1 < x0: x0, x1 = x1, x0
        if y1 < y0: y0, y1 = y1, y0

        # Armazena coordenadas relativas ao PDF
        rect_selecionado = (x0 / zoom, y0 / zoom, x1 / zoom, y1 / zoom)

        messagebox.showinfo("Área selecionada", "Área de referência salva! Agora o script usará esta região para renomear os PDFs.")
        seletor.destroy()

    def proxima_pagina():
        nonlocal pagina_atual
        if pagina_atual < len(doc) - 1:
            pagina_atual += 1
            exibir_pagina()

    def pagina_anterior():
        nonlocal pagina_atual
        if pagina_atual > 0:
            pagina_atual -= 1
            exibir_pagina()

    canvas.bind("<ButtonPress-1>", ao_pressionar)
    canvas.bind("<B1-Motion>", ao_arrastar)
    canvas.bind("<ButtonRelease-1>", ao_soltarselecao)

    frame_nav = tk.Frame(seletor, bg="white")
    frame_nav.pack(pady=5)
    tk.Button(frame_nav, text="⬅ Página anterior", command=pagina_anterior).pack(side="left", padx=10)
    tk.Button(frame_nav, text="➡ Próxima página", command=proxima_pagina).pack(side="left", padx=10)

    exibir_pagina()
    seletor.mainloop()

def extrair_texto_area(pdf_path, pagina_index=0):
    """Extrai o texto dentro da área selecionada"""
    global rect_selecionado
    if rect_selecionado is None:
        return None

    try:
        doc = fitz.open(pdf_path)
        pagina = doc.load_page(pagina_index)
        area = fitz.Rect(rect_selecionado)
        palavras = pagina.get_text("words")
        selecionadas = [p[4] for p in palavras if fitz.Rect(p[:4]).intersects(area)]
        if selecionadas:
            return " ".join(selecionadas).strip()
    except Exception as e:
        print(f"Erro ao extrair texto de {pdf_path}: {e}")
    return None

def renomear_pdfs():
    pasta = entry_pasta.get()
    if not pasta or not os.path.exists(pasta):
        messagebox.showerror("Erro", "Selecione uma pasta válida!")
        return
    if rect_selecionado is None:
        messagebox.showerror("Erro", "Selecione primeiro a área de referência em um PDF de exemplo!")
        return

    log = []
    erros = 0

    for arquivo in os.listdir(pasta):
        if arquivo.lower().endswith(".pdf"):
            caminho_antigo = os.path.join(pasta, arquivo)
            try:
                texto = extrair_texto_area(caminho_antigo)
                if texto:
                    novo_nome = limpar_nome(texto) + ".pdf"
                else:
                    base = os.path.splitext(arquivo)[0]
                    data = datetime.now().strftime("%Y%m%d_%H%M%S")
                    novo_nome = f"{base}_{data}.pdf"

                caminho_novo = os.path.join(pasta, novo_nome)
                contador = 1
                while os.path.exists(caminho_novo):
                    caminho_novo = os.path.join(pasta, f"{os.path.splitext(novo_nome)[0]}_{contador}.pdf")
                    contador += 1

                os.rename(caminho_antigo, caminho_novo)
                log.append(f" {arquivo} → {os.path.basename(caminho_novo)}")
            except Exception as e:
                erros += 1
                log.append(f" Erro ao renomear {arquivo}: {e}")

    log_path = os.path.join(pasta, "log_renomeacao.txt")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(log))

    messagebox.showinfo("Concluído", f"Processo finalizado!\nErros: {erros}\nLog salvo em {log_path}")

# ----- INTERFACE -----
janela = tk.Tk()
janela.title("Renomeador de PDFs por Área Selecionada")
janela.geometry("650x250")
janela.resizable(False, False)

frame = tk.Frame(janela, padx=10, pady=10)
frame.pack(expand=True, fill="both")

tk.Label(frame, text="Selecione a pasta com os PDFs:", font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=(0,5))
entry_pasta = tk.Entry(frame, width=50)
entry_pasta.grid(row=1, column=0, padx=(0,10))
btn_selecionar = tk.Button(frame, text="📁 Procurar", command=selecionar_pasta)
btn_selecionar.grid(row=1, column=1)

tk.Button(frame, text=" Selecionar área de referência em PDF de exemplo", command=escolher_area).grid(row=2, column=0, columnspan=2, pady=20)

tk.Button(janela, text=" Renomear PDFs", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=renomear_pdfs).pack(pady=20)

janela.mainloop()
