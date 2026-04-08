from remi import App, start
import remi.gui as gui
import datetime
import json

script = {
    "👋 Saudação": "Olá, boa tarde, me chamo Afonso, sou do TI da Softtek, tudo bem? Você já recebeu o equipamento e os acessos ao e-mail da Softtek?",
    "🔑 Etapas Iniciais": "1. Selecionar Windows 11\n2. Digitar o **PIN**: `12345678` e pressionar **ENTER**\n3. Digite o início do e-mail (sem `@softtek.com`)\n4. Digitar a senha: `Stk1234!`\n5. Conectar-se à internet e avisar para prosseguir com o acesso remoto",
    "❓ Pergunta": "Pode me descrever o problema que está enfrentando?",
    "💡 Solução": "Entendi. A solução é [solução].",
    "👋 Encerramento": "Obrigado pelo contato. Tenha um bom dia!"
}

class ScriptApp(App):
    def __init__(self, *args):
        super(ScriptApp, self).__init__(*args)

    def main(self):
        self.current_script = script.copy()
        self.current_key = None
        self.theme = 'Notion'

        main_container = gui.VBox(style={
            'width': '100%',
            'height': '100%',
            'align_items': 'center',
            'justify_content': 'flex-start',
            'background_color': '#f5f6f7',
            'font_family': 'Arial, sans-serif'
        })

        header = gui.HBox(style={
            'width': '100%',
            'justify_content': 'space-between',
            'align_items': 'center',
            'padding': '12px 20px',
            'background_color': '#ffffff',
            'box_shadow': '0 2px 8px rgba(0, 0, 0, 0.08)',
            'margin_bottom': '10px'
        })
        header.append(gui.Label('Script de Atendimento', style={
            'font_size': '22px',
            'font_weight': '700',
            'color': '#111111'
        }))
        self.theme_select = gui.DropDown(width='180px', height='32px')
        for theme in ['Notion', 'Dark', 'Light']:
            self.theme_select.append(gui.Option(theme, theme))
        self.theme_select.set_value('Notion')
        self.theme_select.set_on_change_listener(self.on_theme_change)
        header.append(self.theme_select)
        main_container.append(header)

        content = gui.HBox(style={
            'width': '100%',
            'justify_content': 'space-between',
            'padding': '0 20px 20px 20px'
        })

        self.button_panel = gui.VBox(style={
            'width': '280px',
            'min_height': '620px',
            'padding': '18px',
            'background_color': '#ffffff',
            'border_radius': '12px',
            'box_shadow': '0 2px 10px rgba(0,0,0,0.08)',
            'overflow': 'auto'
        })
        self.button_panel.append(gui.Label('Seções', style={
            'font_size': '18px',
            'font_weight': '700',
            'margin_bottom': '10px',
            'color': '#111111'
        }))
        for key in self.current_script:
            btn = gui.Button(key, style=self.get_button_style())
            btn.set_on_click_listener(self.on_section_click)
            self.button_panel.append(btn)
        self.button_panel.append(gui.Label('', height='10px'))
        add_btn = gui.Button('➕ Adicionar Campo', style=self.get_button_style('#e8f0fe', '#174ea6'))
        add_btn.set_on_click_listener(self.on_add)
        self.button_panel.append(add_btn)
        content.append(self.button_panel)

        editor_panel = gui.VBox(style={
            'flex': '1',
            'margin_left': '20px',
            'padding': '18px',
            'background_color': '#ffffff',
            'border_radius': '12px',
            'box_shadow': '0 2px 10px rgba(0,0,0,0.08)'
        })
        self.text_area = gui.TextInput(single_line=False, style={
            'width': '100%',
            'height': '340px',
            'resize': 'none',
            'font_size': '15px',
            'color': '#111111',
            'background_color': '#fcfcfc',
            'border': '1px solid #d5d7db',
            'border_radius': '8px',
            'padding': '12px'
        })
        editor_panel.append(self.text_area)

        btn_bar = gui.HBox(style={
            'width': '100%',
            'justify_content': 'space-between',
            'flex_wrap': 'wrap',
            'margin_top': '14px'
        })
        btn_bar.append(self.create_action_button('💾 Salvar', self.on_save))
        btn_bar.append(self.create_action_button('📋 Copiar', self.on_copy))
        btn_bar.append(self.create_action_button('🔄 Sugerir Alterações', self.on_suggest))
        btn_bar.append(self.create_action_button('😊 Emoji', self.on_insert_emoji))
        btn_bar.append(self.create_action_button('✏️ Editar Nome', self.on_edit_name))
        btn_bar.append(self.create_action_button('🗑️ Excluir Campo', self.on_delete_field))
        editor_panel.append(btn_bar)

        content.append(editor_panel)
        main_container.append(content)

        self.apply_theme('Notion')
        return main_container

    def get_button_style(self, background='#f6f7f8', color='#111111'):
        return {
            'width': '100%',
            'padding': '10px 14px',
            'margin_bottom': '8px',
            'text_align': 'left',
            'background_color': background,
            'color': color,
            'border': '1px solid #d5d7db',
            'border_radius': '8px',
            'font_size': '14px'
        }

    def create_action_button(self, text, listener):
        btn = gui.Button(text, style={
            'width': 'calc(33% - 10px)',
            'min_width': '140px',
            'padding': '10px 12px',
            'margin_bottom': '10px',
            'margin_right': '10px',
            'font_size': '13px',
            'border_radius': '8px',
            'background_color': '#f1f3f5',
            'color': '#111111',
            'border': '1px solid #d5d7db'
        })
        btn.set_on_click_listener(listener)
        return btn

    def on_section_click(self, widget):
        self.current_key = widget.get_text()
        self.text_area.set_value(self.current_script.get(self.current_key, ''))

    def on_save(self, widget):
        if self.current_key:
            self.current_script[self.current_key] = self.text_area.get_value()
            self.show_message('Texto salvo!')
        else:
            self.show_message('Selecione um campo primeiro.', False)

    def on_copy(self, widget):
        text = self.text_area.get_value() or ''
        js = f"navigator.clipboard.writeText({json.dumps(text)}).then(()=>alert('Texto copiado!')).catch(()=>alert('Não foi possível copiar.'))"
        self.execute_javascript(js)

    def on_suggest(self, widget):
        if '👋 Saudação' in self.current_script:
            self.current_script['👋 Saudação'] = self.replace_time_phrase(self.current_script['👋 Saudação'], self.get_greeting())
        if '👋 Encerramento' in self.current_script:
            self.current_script['👋 Encerramento'] = self.replace_time_phrase(self.current_script['👋 Encerramento'], self.get_closing())
        if self.current_key:
            self.text_area.set_value(self.current_script.get(self.current_key, ''))
        self.show_message('Alterações baseadas no horário aplicadas!')

    def replace_time_phrase(self, text, replacement):
        variants = ['bom dia', 'boa tarde', 'boa noite']
        lower_text = text.lower()
        for variant in variants:
            idx = lower_text.find(variant)
            if idx != -1:
                return text[:idx] + replacement + text[idx + len(variant):]
        return text

    def on_insert_emoji(self, widget):
        emojis = ['😊', '👍', '👋', '📝', '❓', '💡', '💾', '📋', '🔄', '➕', '❤️', '😂', '😍', '🤔', '😎']
        if hasattr(self, 'emoji_overlay') and self.emoji_overlay:
            self.remove_child(self.emoji_overlay)
            self.emoji_overlay = None
            return
        self.emoji_overlay = gui.VBox(style={
            'position': 'fixed',
            'top': '80px',
            'right': '20px',
            'width': '220px',
            'padding': '12px',
            'background_color': '#ffffff',
            'border': '1px solid #d5d7db',
            'border_radius': '12px',
            'box_shadow': '0 2px 10px rgba(0,0,0,0.12)',
            'z_index': '999'
        })
        self.emoji_overlay.append(gui.Label('Inserir Emoji', style={'font_weight': '700', 'margin_bottom': '8px'}))
        for emoji in emojis:
            btn = gui.Button(emoji, style={'width': '32px', 'margin': '2px', 'padding': '8px', 'border_radius': '8px'})
            btn.set_on_click_listener(self.on_emoji_click)
            self.emoji_overlay.append(btn)
        self.append(self.emoji_overlay)

    def on_emoji_click(self, widget):
        emoji = widget.get_text()
        self.text_area.set_value(self.text_area.get_value() + emoji)
        if hasattr(self, 'emoji_overlay') and self.emoji_overlay:
            self.remove_child(self.emoji_overlay)
            self.emoji_overlay = None

    def on_add(self, widget):
        self.show_modal('Adicionar novo campo', self.add_new_field)

    def on_edit_name(self, widget):
        if self.current_key:
            self.show_modal('Editar nome do campo', self.edit_current_name, self.current_key)
        else:
            self.show_message('Selecione um campo primeiro.', False)

    def on_delete_field(self, widget):
        if self.current_key and self.current_key in self.current_script:
            del self.current_script[self.current_key]
            if self.current_key in self.button_panel.children:
                self.button_panel.children[self.current_key].delete()
            self.current_key = None
            self.text_area.set_value('')
            self.show_message('Campo excluído!')
        else:
            self.show_message('Selecione um campo primeiro.', False)

    def show_modal(self, title, callback, default_text=''):
        modal = gui.VBox(style={
            'position': 'fixed',
            'top': '50%',
            'left': '50%',
            'transform': 'translate(-50%, -50%)',
            'width': '360px',
            'padding': '18px',
            'background_color': '#ffffff',
            'border': '1px solid #d5d7db',
            'border_radius': '12px',
            'box_shadow': '0 3px 18px rgba(0,0,0,0.2)',
            'z_index': '1000'
        })
        modal.append(gui.Label(title, style={'font_size': '18px', 'font_weight': '700', 'margin_bottom': '10px'}))
        name_input = gui.TextInput(single_line=True, style={'width': '100%', 'margin_bottom': '10px', 'padding': '8px'})
        name_input.set_value(default_text)
        value_input = gui.TextInput(single_line=False, style={'width': '100%', 'height': '120px', 'padding': '8px'})
        if callback == self.edit_current_name:
            value_input.hide()
        modal.append(name_input)
        modal.append(value_input)
        action_bar = gui.HBox(style={'width': '100%', 'justify_content': 'flex-end', 'margin_top': '10px'})
        ok_btn = gui.Button('Salvar', style={'margin_right': '8px', 'padding': '8px 14px'})
        cancel_btn = gui.Button('Cancelar', style={'padding': '8px 14px'})
        action_bar.append(ok_btn)
        action_bar.append(cancel_btn)
        modal.append(action_bar)
        self.append(modal)

        def on_ok(widget):
            callback(name_input.get_value(), value_input.get_value())
            self.remove_child(modal)

        def on_cancel(widget):
            self.remove_child(modal)

        ok_btn.set_on_click_listener(on_ok)
        cancel_btn.set_on_click_listener(on_cancel)

    def add_new_field(self, name, value):
        name = name.strip()
        value = value.strip()
        if not name or not value:
            self.show_message('Nome e texto são obrigatórios.', False)
            return
        if name in self.current_script:
            self.show_message('Esse nome já existe.', False)
            return
        self.current_script[name] = value
        btn = gui.Button(name, style=self.get_button_style())
        btn.set_on_click_listener(self.on_section_click)
        self.button_panel.append(btn)
        self.show_message('Campo adicionado!')

    def edit_current_name(self, name, _value):
        name = name.strip()
        if not name or name in self.current_script:
            self.show_message('Nome inválido ou já existe.', False)
            return
        if self.current_key:
            self.current_script[name] = self.current_script.pop(self.current_key)
            button = next((child for child in self.button_panel.children if child == self.current_key), None)
            self.current_key = name
            self.current_script[name] = self.current_script.pop(self.current_key, self.current_script.get(name, ''))
            self.show_message('Nome do campo alterado!')

    def show_message(self, message, success=True):
        alert = gui.Label(message, style={
            'color': '#155724' if success else '#721c24',
            'background_color': '#d4edda' if success else '#f8d7da',
            'padding': '10px',
            'border_radius': '8px',
            'margin_top': '10px'
        })
        self.append(alert)
        self.execute_javascript("setTimeout(function(){var a=document.querySelector('div[style*=\\\"position: fixed\\\"]'); if(a) a.remove();}, 2500);")

    def on_theme_change(self, widget, value):
        self.apply_theme(value)

    def apply_theme(self, theme_name):
        self.theme = theme_name
        if theme_name == 'Dark':
            self.set_style({'background_color': '#262b32'})
            self.button_panel.set_style({'background_color': '#2d333d'})
            self.text_area.set_style({'background_color': '#1f2228', 'color': '#f1f1f1'})
        elif theme_name == 'Light':
            self.set_style({'background_color': '#f7f8fa'})
            self.button_panel.set_style({'background_color': '#ffffff'})
            self.text_area.set_style({'background_color': '#ffffff', 'color': '#111111'})
        else:
            self.set_style({'background_color': '#f5f6f7'})
            self.button_panel.set_style({'background_color': '#ffffff'})
            self.text_area.set_style({'background_color': '#fcfcfc', 'color': '#111111'})

    def get_greeting(self):
        hour = datetime.datetime.now().hour
        if hour < 12:
            return 'Bom dia'
        elif hour < 18:
            return 'Boa tarde'
        return 'Boa noite'

    def get_closing(self):
        hour = datetime.datetime.now().hour
        if hour < 12:
            return 'bom dia'
        elif hour < 18:
            return 'boa tarde'
        return 'boa noite'

if __name__ == '__main__':
    start(ScriptApp, address='0.0.0.0', port=8081, start_browser=True)
