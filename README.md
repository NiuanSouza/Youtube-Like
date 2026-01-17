**YouTube Liked Videos Cleaner 🧹**

Este script automatiza a remoção de vídeos da playlist "Vídeos de que gostei" (Liked Videos) do YouTube. Ele é especialmente útil para realizar limpezas em massa, incluindo a capacidade de detetar e remover vídeos que já foram marcados como indisponíveis ou privados.

## **🚀 Funcionalidades**

* **Remoção em Lote:** Processa vídeos em pequenos grupos para evitar sobrecarga de memória e bloqueios.  
* **Gestão de Vídeos Indisponíveis:** Ativa automaticamente a opção de exibir vídeos ocultos/indisponíveis para que possam ser removidos da lista.  
* **Persistência de Sessão:** Utiliza o teu perfil real do Google Chrome para evitar a necessidade de login manual a cada execução.  
* **Estabilidade:** Inclui mecanismos de recarregamento (refresh) e tratamento de erros de conexão com o browser.

## **🛠️ Pré-requisitos**

Antes de correr o script, certifica-te de que tens:

1. **Python 3.x** instalado.  
2. **Google Chrome** instalado.  
3. **ChromeDriver** compatível com a sua versão do Chrome.  
4. Dependências do Python:  
   Bash  
   pip install selenium

## **📋 Como Usar**

1. **Configuração do Perfil:** O script está configurado para usar o perfil padrão do Chrome no Linux (\~/.config/google-chrome). Se usares Windows ou macOS, altera o perfil\_path na função criar\_browser().  
2. **Execução:**  
   Bash  
   python youtubeLike.py

3. **Funcionamento:** O script abrirá o browser, navegará até a sua playlist de vídeos marcados com "Gostei" e começará a remover os itens um por um através de comandos JavaScript injetados.

## **⚠️ Notas Importantes**

* **Segurança:** O ficheiro .gitignore já está configurado para ignorar o ambiente virtual (.venv/) e ficheiros de configuração sensíveis (.env), garantindo que não envies dados desnecessários ou privados para o teu repositório.  
* **Ambiente Virtual:** Recomenda-se o uso de um ambiente virtual para gerir as dependências:  
  Bash  
  python \-m venv .venv  
  source .venv/bin/activate  \# Linux/Mac  
  \# ou  
  .venv\\Scripts\\activate     \# Windows

## **📄 Estrutura do Projeto**

* youtubeLike.py: Script principal contendo a lógica de automação com Selenium.  
* .gitignore: Define os ficheiros e pastas que o Git deve ignorar (como o .venv).  
* README.md: Documentação do projeto.

---

**Contribuinte:** \[Niuansouza\]