# 📄 Renomeador de PDFs por Área Selecionada

Este projeto é um script em Python que permite **renomear automaticamente arquivos PDF** com base no **texto extraído de uma área específica** dentro das páginas.  
A área de referência é escolhida manualmente pelo usuário em um PDF de exemplo, e o programa passa a usar essa região para extrair o texto e renomear os demais arquivos da pasta.

---

## 🚀 Funcionalidades

- Interface gráfica simples feita com **Tkinter**  
- Seleção de uma **pasta contendo PDFs**  
- Escolha de uma **área de referência** em um PDF de exemplo (com suporte a navegação entre páginas)  
- Extração do texto dentro da área selecionada usando **PyMuPDF (fitz)**  
- Renomeação automática dos PDFs com base no texto encontrado  
- Substituição de caracteres inválidos no nome do arquivo  
- Geração de um **log de renomeação** (`log_renomeacao.txt`) na pasta escolhida  
- Caso não seja possível extrair texto, o arquivo é renomeado com base no nome original + data/hora  

---

## 📦 Dependências

Instale as bibliotecas necessárias antes de executar:

```bash
pip install pymupdf pillow

O Tkinter já vem incluído na instalação padrão do Python (em sistemas Windows e Linux).

🖥️ Como usar
1. 	Execute o script:

python renomeador_pdfs.py

Na interface:
• 	Clique em 📁 Procurar para selecionar a pasta com os PDFs
• 	Clique em Selecionar área de referência em PDF de exemplo e escolha um PDF
• 	Na janela aberta:
• 	Navegue entre páginas com os botões ⬅ ➡
• 	Clique e arraste para desenhar um retângulo sobre a área desejada
• 	Ao soltar o mouse, a área será salva
3. 	Clique em Renomear PDFs
• 	O script processará todos os PDFs da pasta
• 	Os arquivos serão renomeados conforme o texto extraído
• 	Um arquivo  será criado na pasta, contendo o histórico das alterações

📂 Estrutura de saída
• 	PDFs renomeados com base no texto da área selecionada
• 	Caso não haja texto, o nome será algo como:

arquivo_original_20251215_180300.pdf

Log de renomeação:

documento1.pdf → Contrato_Cliente.pdf
documento2.pdf → Relatorio_20251215_180300.pdf
Erro ao renomear documento3.pdf: <mensagem de erro>

⚠️ Observações
• 	Certifique-se de que os PDFs tenham texto pesquisável (não apenas imagens)
• 	Se os arquivos forem digitalizados sem OCR, o script pode não conseguir extrair o texto
• 	A área selecionada é aplicada sempre na primeira página dos PDFs (padrão do script)

🛠️ Tecnologias utilizadas
• 	Python 3
• 	Tkinter (interface gráfica)
• 	PyMuPDF (fitz) (manipulação de PDFs)
• 	Pillow (PIL) (renderização de imagens)
