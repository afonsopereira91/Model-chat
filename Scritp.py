import customtkinter as ctk
from tkinter import messagebox
import datetime
import google.genai as genai

# Configure Gemini API (substitua pela sua chave)
client = genai.Client(api_key="YOUR_API_KEY")  # Insira sua chave da API do Gemini aqui

# Script base de atendimento (exemplo, baseado em um script típico)
script = {
    "👋 Saudação": "Olá   , boa tarde, me chamo Afonso, sou do TI da Softtek, tudo bem? Você já recebeu o equipamento e os acessos ao e-mail da Softtek?",
    "🔑 Etapas Iniciais": "1. Selecionar Windows 11\n2. Digitar o **PIN**: `12345678` e pressionar **ENTER**\n3. Digite o início do e-mail (sem `@softtek.com`)\n4. Digitar a senha: `Stk1234!`\n5. Conectar-se à internet e avisar para prosseguir com o acesso remoto",
    "❓ Pergunta": "Pode me descrever o problema que está enfrentando?",
    "💡 Solução": "Entendi. A solução é [solução].",
    "👋 Encerramento": "Obrigado pelo contato. Tenha um bom dia!"
}

current_script = script.copy()
current_key = None
buttons = {}  # Dicionário para rastrear botões
templates = {}  # Modelos salvos para uso futuro
button_order = list(script.keys())  # Ordem dos botões para drag and drop

# Variáveis para drag and drop
dragging = False
drag_start_y = 0
dragged_button = None

def get_greeting():
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Bom dia"
    elif hour < 18:
        return "Boa tarde"
    else:
        return "Boa noite"

def get_closing():
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "bom dia"
    elif hour < 18:
        return "boa tarde"
    else:
        return "boa noite"

def show_text(key):
    global current_key
    current_key = key
    text_area.delete("1.0", "end")
    text_area.insert("end", current_script[key])

def copy_text():
    if current_key:
        root.clipboard_clear()
        root.clipboard_append(text_area.get("1.0", "end").strip())
        messagebox.showinfo("Copiado", "Texto copiado para a área de transferência!")

def save_text():
    if current_key:
        current_script[current_key] = text_area.get("1.0", "end").strip()
        messagebox.showinfo("Salvo", "Texto salvo!")

def replace_time_phrase(text, variants, replacement):
    lower_text = text.lower()
    for variant in variants:
        idx = lower_text.find(variant.lower())
        if idx != -1:
            return text[:idx] + replacement + text[idx + len(variant):]
    return text

def suggest_changes():
    greeting = get_greeting()
    closing = get_closing()
    greetings = ["bom dia", "boa tarde", "boa noite"]
    closings = ["bom dia", "boa tarde", "boa noite"]
    if "👋 Saudação" in current_script:
        text = current_script["👋 Saudação"]
        current_script["👋 Saudação"] = replace_time_phrase(text, greetings, greeting)
    if "👋 Encerramento" in current_script:
        text = current_script["👋 Encerramento"]
        current_script["👋 Encerramento"] = replace_time_phrase(text, closings, closing)
    if current_key:
        show_text(current_key)
    messagebox.showinfo("Sugestões Aplicadas", "Alterações baseadas no horário aplicadas!")

def save_as_model():
    if not current_key:
        messagebox.showwarning("Aviso", "Selecione um campo primeiro para salvar como modelo!")
        return
    def apply_model_name():
        model_name = model_name_entry.get().strip()
        if model_name:
            templates[model_name] = current_script[current_key]
            model_win.destroy()
            messagebox.showinfo("Modelo Salvo", f"Modelo '{model_name}' salvo com sucesso!")
        else:
            messagebox.showerror("Erro", "Informe um nome para o modelo.")
    model_win = ctk.CTkToplevel(root)
    model_win.title("Salvar como Modelo")
    ctk.CTkLabel(model_win, text="Nome do Modelo:").pack(pady=5)
    model_name_entry = ctk.CTkEntry(model_win)
    model_name_entry.pack(pady=5)
    ctk.CTkButton(model_win, text="Salvar Modelo", command=apply_model_name).pack(pady=10)


def apply_model():
    if not templates:
        messagebox.showwarning("Aviso", "Não há modelos salvos ainda.")
        return
    def insert_model(name):
        model_text = templates[name]
        text_area.delete("1.0", "end")
        text_area.insert("end", model_text)
        if current_key:
            current_script[current_key] = model_text
        model_list_win.destroy()
        messagebox.showinfo("Modelo Aplicado", f"Modelo '{name}' inserido no campo atual.")
    model_list_win = ctk.CTkToplevel(root)
    model_list_win.title("Modelos Salvos")
    model_frame = ctk.CTkScrollableFrame(model_list_win, width=360, height=260)
    model_frame.pack(padx=10, pady=10)
    for name in templates:
        row = ctk.CTkFrame(model_frame)
        row.pack(fill=ctk.X, pady=5, padx=5)
        ctk.CTkLabel(row, text=name).pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(row, text="Inserir", width=80, command=lambda n=name: insert_model(n)).pack(side=ctk.RIGHT, padx=5)


def chat_with_ai():
    def send_message():
        user_msg = chat_entry.get().strip()
        if user_msg:
            chat_text.insert("end", f"Você: {user_msg}\n")
            chat_entry.delete(0, "end")
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash-exp",
                    contents=user_msg
                )
                ai_msg = response.text
                chat_text.insert("end", f"Gemini: {ai_msg}\n\n")
            except Exception as e:
                chat_text.insert("end", f"Erro: {str(e)}\n\n")
    chat_win = ctk.CTkToplevel(root)
    chat_win.title("Chat com IA (Gemini)")
    chat_text = ctk.CTkTextbox(chat_win, width=400, height=300)
    chat_text.pack(padx=10, pady=10)
    chat_entry = ctk.CTkEntry(chat_win, placeholder_text="Digite sua mensagem...")
    chat_entry.pack(pady=5, padx=10, fill=ctk.X)
    send_btn = ctk.CTkButton(chat_win, text="Enviar", command=send_message)
    send_btn.pack(pady=5)

def insert_emoji():
    emojis = ["😊", "👍", "👋", "📝", "❓", "💡", "💾", "📋", "🔄", "➕", "❤️", "😂", "😍", "🤔", "😎"]
    def select_emoji(emoji):
        text_area.insert("insert", emoji)
        emoji_win.destroy()
    emoji_win = ctk.CTkToplevel(root)
    emoji_win.title("Inserir Emoji")
    emoji_frame = ctk.CTkScrollableFrame(emoji_win, width=200, height=200)
    emoji_frame.pack(padx=10, pady=10)
    for emoji in emojis:
        btn = ctk.CTkButton(emoji_frame, text=emoji, command=lambda e=emoji: select_emoji(e))
        btn.pack(pady=2)

def add_new():
    def save_new():
        name = name_entry.get().strip()
        text = text_entry.get().strip()
        if name and text:
            current_script[name] = text
            btn = ctk.CTkButton(buttons_frame, text=name, command=lambda k=name: show_text(k))
            btn.pack(pady=5, fill=ctk.X)
            btn.key = name
            btn.bind("<Button-1>", start_drag)
            btn.bind("<B1-Motion>", do_drag)
            btn.bind("<ButtonRelease-1>", end_drag)
            buttons[name] = btn
            button_order.append(name)
            new_win.destroy()
        else:
            messagebox.showerror("Erro", "Nome e texto são obrigatórios!")
    new_win = ctk.CTkToplevel(root)
    new_win.title("Adicionar Novo Campo")
    ctk.CTkLabel(new_win, text="Nome do Campo:").pack(pady=5)
    name_entry = ctk.CTkEntry(new_win)
    name_entry.pack(pady=5)
    ctk.CTkLabel(new_win, text="Texto:").pack(pady=5)
    text_entry = ctk.CTkEntry(new_win)
    text_entry.pack(pady=5)
    ctk.CTkButton(new_win, text="Salvar", command=save_new).pack(pady=10)

def edit_name():
    global current_key
    if current_key:
        def save_edit():
            new_name = edit_entry.get().strip()
            if new_name and new_name not in current_script:
                current_script[new_name] = current_script.pop(current_key)
                buttons[new_name] = buttons.pop(current_key)
                buttons[new_name].configure(text=new_name, command=lambda k=new_name: show_text(k))
                buttons[new_name].key = new_name
                idx = button_order.index(current_key)
                button_order[idx] = new_name
                current_key = new_name
                edit_win.destroy()
            else:
                messagebox.showerror("Erro", "Nome inválido ou já existe!")
        edit_win = ctk.CTkToplevel(root)
        edit_win.title("Editar Nome do Campo")
        ctk.CTkLabel(edit_win, text="Novo Nome:").pack(pady=5)
        edit_entry = ctk.CTkEntry(edit_win)
        edit_entry.insert(0, current_key)
        edit_entry.pack(pady=5)
        ctk.CTkButton(edit_win, text="Salvar", command=save_edit).pack(pady=10)
    else:
        messagebox.showwarning("Aviso", "Selecione um campo primeiro!")

def delete_field():
    global current_key
    if current_key and current_key in buttons:
        if messagebox.askyesno("Confirmar", f"Excluir o campo '{current_key}'?"):
            buttons[current_key].destroy()
            del buttons[current_key]
            del current_script[current_key]
            button_order.remove(current_key)
            current_key = None
            text_area.delete("1.0", "end")
    else:
        messagebox.showwarning("Aviso", "Selecione um campo primeiro!")

def import_script():
    def apply_import():
        script_text = import_text.get("1.0", "end").strip()
        if script_text:
            lines = script_text.split('\n')
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    if key and value and key not in current_script:
                        current_script[key] = value
                        btn = ctk.CTkButton(buttons_frame, text=key, command=lambda k=key: show_text(k))
                        btn.pack(pady=5, fill=ctk.X)
                        btn.key = key
                        btn.bind("<Button-1>", start_drag)
                        btn.bind("<B1-Motion>", do_drag)
                        btn.bind("<ButtonRelease-1>", end_drag)
                        buttons[key] = btn
                        button_order.append(key)
            import_win.destroy()
            messagebox.showinfo("Importado", "Script importado com sucesso!")
        else:
            messagebox.showerror("Erro", "Cole o script no formato 'Nome: Texto'")
    import_win = ctk.CTkToplevel(root)
    import_win.title("Importar Script")
    ctk.CTkLabel(import_win, text="Cole o script (formato: Nome: Texto por linha):").pack(pady=5)
    import_text = ctk.CTkTextbox(import_win, width=400, height=200)
    import_text.pack(pady=5)
    ctk.CTkButton(import_win, text="Importar", command=apply_import).pack(pady=10)

def customize_theme():
    def apply_custom():
        mode = mode_var.get()
        theme = theme_var.get()
        ctk.set_appearance_mode(mode)
        ctk.set_default_color_theme(theme)
        custom_win.destroy()
    custom_win = ctk.CTkToplevel(root)
    custom_win.title("Personalizar Tema")
    ctk.CTkLabel(custom_win, text="Modo de Aparência:").pack(pady=5)
    mode_var = ctk.StringVar(value="System")
    mode_combo = ctk.CTkComboBox(custom_win, values=["Light", "Dark", "System"], variable=mode_var)
    mode_combo.pack(pady=5)
    ctk.CTkLabel(custom_win, text="Tema de Cor:").pack(pady=5)
    theme_var = ctk.StringVar(value="blue")
    theme_combo = ctk.CTkComboBox(custom_win, values=["blue", "green", "dark-blue"], variable=theme_var)
    theme_combo.pack(pady=5)
    ctk.CTkButton(custom_win, text="Aplicar", command=apply_custom).pack(pady=10)


def change_appearance_mode(mode):
    ctk.set_appearance_mode(mode)


def change_color_theme(theme):
    ctk.set_default_color_theme(theme)

# Funções para drag and drop dos botões
def start_drag(event):
    global dragging, drag_start_y, dragged_button
    dragging = False
    drag_start_y = event.y_root
    dragged_button = event.widget

def do_drag(event):
    global dragging
    if abs(event.y_root - drag_start_y) > 10:  # Limite para considerar como drag
        dragging = True

def end_drag(event):
    global dragging, dragged_button
    if dragging:
        # Encontrar o botão alvo sob o mouse
        target = find_button_under_mouse(event)
        if target and target != dragged_button:
            # Trocar posições na ordem
            idx1 = button_order.index(dragged_button.key)
            idx2 = button_order.index(target.key)
            button_order[idx1], button_order[idx2] = button_order[idx2], button_order[idx1]
            # Reempacotar botões
            repack_buttons()
    else:
        # Clique normal, executar a ação do botão
        show_text(dragged_button.key)
    dragging = False
    dragged_button = None

def find_button_under_mouse(event):
    for btn in buttons.values():
        x1 = btn.winfo_rootx()
        y1 = btn.winfo_rooty()
        x2 = x1 + btn.winfo_width()
        y2 = y1 + btn.winfo_height()
        if x1 <= event.x_root <= x2 and y1 <= event.y_root <= y2:
            return btn
    return None

def repack_buttons():
    # Esconder todos os botões
    for btn in buttons.values():
        btn.pack_forget()
    # Reempacotar na nova ordem
    for key in button_order:
        buttons[key].pack(pady=5, fill=ctk.X)

# Configurar CustomTkinter
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Criar a janela principal
root = ctk.CTk()
root.title("Criador de Script de Atendimento")
root.geometry("800x600")

# Frame para os botões
buttons_frame = ctk.CTkScrollableFrame(root, width=250)
buttons_frame.pack(side=ctk.LEFT, padx=10, pady=10, fill=ctk.Y)

# Criar botões para cada seção do script
for key in script:
    btn = ctk.CTkButton(buttons_frame, text=key, command=lambda k=key: show_text(k))
    btn.pack(pady=5, fill=ctk.X)
    btn.key = key  # Armazenar a chave no botão
    # Bindings para drag and drop
    btn.bind("<Button-1>", start_drag)
    btn.bind("<B1-Motion>", do_drag)
    btn.bind("<ButtonRelease-1>", end_drag)
    buttons[key] = btn

# Painel de temas à esquerda
theme_panel = ctk.CTkFrame(buttons_frame)
theme_panel.pack(pady=15, padx=5, fill=ctk.X)
ctk.CTkLabel(theme_panel, text="Tema de Aparência:").pack(pady=(5, 2), anchor="w")
appearance_mode_combo = ctk.CTkComboBox(theme_panel, values=["System", "Light", "Dark"], command=change_appearance_mode)
appearance_mode_combo.set("System")
appearance_mode_combo.pack(pady=5, fill=ctk.X)

ctk.CTkLabel(theme_panel, text="Tema de Cor:").pack(pady=(10, 2), anchor="w")
color_theme_combo = ctk.CTkComboBox(theme_panel, values=["blue", "green", "dark-blue"], command=change_color_theme)
color_theme_combo.set("blue")
color_theme_combo.pack(pady=5, fill=ctk.X)

# Botões de gerenciamento no painel esquerdo
add_new_btn = ctk.CTkButton(buttons_frame, text="➕ Adicionar Novo", command=add_new)
add_new_btn.pack(pady=5, fill=ctk.X)

save_model_btn_left = ctk.CTkButton(buttons_frame, text="💾 Salvar Modelo", command=save_as_model)
save_model_btn_left.pack(pady=5, fill=ctk.X)

apply_model_btn_left = ctk.CTkButton(buttons_frame, text="📁 Aplicar Modelo", command=apply_model)
apply_model_btn_left.pack(pady=5, fill=ctk.X)

# Frame para a área de texto e botões
text_frame = ctk.CTkFrame(root)
text_frame.pack(side=ctk.RIGHT, padx=10, pady=10, fill=ctk.BOTH, expand=True)

# Área de texto rolável
text_area = ctk.CTkTextbox(text_frame, width=400, height=300, wrap="word")
text_area.pack(pady=10, fill=ctk.BOTH, expand=True)

# Botões
save_btn = ctk.CTkButton(text_frame, text="💾 Salvar", command=save_text)
save_btn.pack(pady=5, fill=ctk.X)

copy_btn = ctk.CTkButton(text_frame, text="📋 Copiar", command=copy_text)
copy_btn.pack(pady=5, fill=ctk.X)

suggest_btn = ctk.CTkButton(text_frame, text="🔄 Sugerir Alterações", command=suggest_changes)
suggest_btn.pack(pady=5, fill=ctk.X)

emoji_btn = ctk.CTkButton(text_frame, text="😊 Inserir Emoji", command=insert_emoji)
emoji_btn.pack(pady=5, fill=ctk.X)

edit_btn = ctk.CTkButton(text_frame, text="✏️ Editar Nome", command=edit_name)
edit_btn.pack(pady=5, fill=ctk.X)

delete_btn = ctk.CTkButton(text_frame, text="🗑️ Excluir Campo", command=delete_field)
delete_btn.pack(pady=5, fill=ctk.X)

save_model_btn = ctk.CTkButton(text_frame, text="💾 Salvar como Modelo", command=save_as_model)
save_model_btn.pack(pady=5, fill=ctk.X)

apply_model_btn = ctk.CTkButton(text_frame, text="📁 Aplicar Modelo", command=apply_model)
apply_model_btn.pack(pady=5, fill=ctk.X)
add_btn = ctk.CTkButton(text_frame, text="➕ Adicionar Novo", command=add_new)
add_btn.pack(pady=5, fill=ctk.X)

import_btn = ctk.CTkButton(text_frame, text="📄 Importar Script", command=import_script)
import_btn.pack(pady=5, fill=ctk.X)

custom_btn = ctk.CTkButton(text_frame, text="🎨 Personalizar Tema", command=customize_theme)
custom_btn.pack(pady=5, fill=ctk.X)

chat_btn = ctk.CTkButton(text_frame, text="💬 Chat com IA", command=chat_with_ai)
chat_btn.pack(pady=5, fill=ctk.X)

def generate_with_ai():
    if current_key:
        prompt = f"Gere um texto apropriado para '{current_key}' em um script de atendimento ao cliente, em português."
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt
            )
            generated_text = response.text.strip()
            current_script[current_key] = generated_text
            show_text(current_key)
            messagebox.showinfo("Gerado", "Texto gerado com IA!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar: {str(e)}")
    else:
        messagebox.showwarning("Aviso", "Selecione um campo primeiro!")

# Iniciar o loop principal
root.mainloop()