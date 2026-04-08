# 🚀 Model Chat - Script Management Application

> Uma aplicação moderna de gerenciamento de scripts de atendimento com inteligência artificial integrada.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.14-blue?style=flat&logo=python)
![Visual Studio Code](https://img.shields.io/badge/IDE-VS%20Code-007ACC?style=flat&logo=visualstudiocode)
![CustomTkinter](https://img.shields.io/badge/Framework-CustomTkinter-green?style=flat)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-%23FFA500?style=flat)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat)

</div>

---

## 📋 Sobre o Projeto

**Model Chat** é uma ferramenta desktop desenvolvida em Python para gerenciamento inteligente de scripts de atendimento ao cliente. A aplicação permite criar, editar, organizar e testar scripts de forma visual e intuitiva, com suporte a modelos pré-configurados e IA generativa integrada.

### ✨ Características Principais

- 🎨 **Interface Moderna**: Desenvolvida com CustomTkinter para um visual clean e responsivo
- 📝 **Editor de Scripts**: Crie e edite scripts com facilidade através de uma interface intuitiva
- 🤖 **IA Generativa**: Integração com Gemini para sugestões automáticas e geração de conteúdo
- 💾 **Gerenciamento de Modelos**: Salve e reutilize templates de scripts
- 🎯 **Drag & Drop**: Reorganize campos com suporte a drag and drop
- 🌓 **Temas Personalizáveis**: Diferentes temas de aparência (Light, Dark, System)
- 💬 **Chat com IA**: Converse com a IA para aprimorar seus scripts
- 📋 **Sugestões Automáticas**: Sugestões baseadas em horários (bom dia, boa tarde, boa noite)

---

## 🛠️ Tecnologias Utilizadas

```
┌─────────────────────────────────┐
│  Tecnologias & Bibliotecas      │
├─────────────────────────────────┤
│ • Python 3.14                   │
│ • CustomTkinter (UI)            │
│ • Google Generative AI          │
│ • cx_Freeze (Compilação)        │
│ • Tkinter (Backend)             │
└─────────────────────────────────┘
```

- **Linguagem**: Python 3.14
- **IDE**: Visual Studio Code ✨
- **Framework UI**: CustomTkinter
- **IA**: Google Gemini API
- **Build**: cx_Freeze

---

## 📦 Instalação & Uso

### ⚡ Versão Executável (Recomendado)

A forma mais rápida de usar a aplicação! Nenhuma instalação de dependências necessária.

```bash
1. Acesse a pasta: build/exe.win-amd64-3.14/
2. Execute: Scritp.exe
3. Pronto! A aplicação abrirá automaticamente
```

**Requisitos do Sistema**:
- Windows 10 ou superior
- 100 MB de espaço em disco
- Sem necessidade de instalar Python

### 💻 Versão para Desenvolvimento

Para trabalhar com o código-fonte:

```bash
# Clone o repositório
git clone https://github.com/afonsopereira91/Model-chat.git
cd Model-chat

# Crie um ambiente virtual
python -m venv .venv

# Ative o ambiente
.venv\Scripts\Activate.ps1  # Windows PowerShell
source .venv/bin/activate    # Linux/Mac

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python Scritp.py
```

### 🔨 Compilar para Executável

Para gerar um novo build:

```bash
# Instale cx_Freeze se necessário
pip install cx_Freeze

# Execute o build
python setup.py build

# O executável estará em: build/exe.win-amd64-3.14/Scritp.exe
```

---

## 🎓 Ideal para Treinamento de QAs

Este projeto é **perfeito para treinamento de QAs** pois permite:

✅ **Praticar Testes de Interface**
- Validar comportamento de buttons, inputs e text areas
- Testar funcionalidades de drag & drop
- Verificar funcionamento de comboboxes e modais

✅ **Testes de Fluxo**
- Criação, edição e exclusão de scripts
- Salvamento e recuperação de modelos
- Integração com APIs externas (Gemini)

✅ **Testes de Integração**
- Comunicação com a IA (Google Gemini)
- Validar respostas de API
- Verificar tratamento de erros

✅ **Casos de Teste Diversos**
- Entrada de dados inválidos
- Limites de caracteres
- Ordemanção de elementos
- Temas e aparências

---

## 📁 Estrutura do Projeto

```
Model-chat/
├── 📄 Scritp.py              # Aplicação principal
├── 📄 setup.py               # Configuração de build (cx_Freeze)
├── 📄 test.py                # Testes básicos
├── 📄 README.md              # Este arquivo
├── 📦 build/
│   └── exe.win-amd64-3.14/
│       ├── ⚙️  Scritp.exe         # Executável principal
│       ├── 📚 lib/                 # Bibliotecas compiladas
│       └── 📂 share/               # Recursos adicionais
└── .venv/                    # Ambiente virtual
```

---

## 🚧 Em Desenvolvimento

Este projeto está em **desenvolvimento ativo** e receberá os seguintes ajustes em breve:

- [ ] Integração com banco de dados
- [ ] Suporte para múltiplos idiomas
- [ ] Exportação de scripts (PDF, TXT, DOCX)
- [ ] Sistema de controle de versão de scripts
- [ ] Autenticação de usuários
- [ ] Análise de performance de scripts
- [ ] Integração com CRMs (Salesforce, HubSpot)

---

## 🔑 Configuração da API Gemini

Para usar as funcionalidades de IA, configure sua chave da API do Google Gemini:

1. Acesse [Google AI Studio](https://aistudio.google.com)
2. Gere uma nova chave de API
3. Abra `Scritp.py` e substituia:
   ```python
   api_key="YOUR_API_KEY"  # ← Coloque sua chave aqui
   ```

> ⚠️ **Importante**: Nunca compartilhe sua chave de API em público!

---

## 📸 Screenshots

> Em breve! 🎬

---

## 🤝 Contribuições

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📞 Suporte

Se encontrar problemas ou tiver dúvidas:

- 📧 Email: [afonso.pereira@softtek.com](mailto:afonso.pereira@softtek.com)
- 🐛 GitHub Issues: [Reportar um bug](https://github.com/afonsopereira91/Model-chat/issues)

---

## 📄 Licença

Este projeto está sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

<div align="center">

### 💡 Desenvolvido com ❤️ em Python

**Desenvolvedor**: Afonso Pereira  
**Última Atualização**: Abril de 2026

⭐ Se este projeto foi útil, considere deixar uma estrela! ⭐

</div>
