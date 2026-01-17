import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException


def criar_browser():
    options = Options()
    perfil_path = os.path.expanduser("~/.config/google-chrome")
    options.add_argument(f"--user-data-dir={perfil_path}")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # Limita o uso de memória para evitar o crash
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(options=options)


# Script JS focado em estabilidade (lotes curtos)
JS_ESTAVEL = """
const callback = arguments[arguments.length - 1];
async function limpar() {
    let contadorLocal = 0;
    const LIMITE_LOTE = 30; // Reduzido para evitar crash de memória
    
    try {
        let videos = document.querySelectorAll('ytd-playlist-video-renderer');
        
        for (let i = 0; i < videos.length && contadorLocal < LIMITE_LOTE; i++) {
            let videoRow = videos[i];
            let btnMenu = videoRow.querySelector('button.yt-icon-button');
            if (!btnMenu) continue;

            btnMenu.click();
            await new Promise(r => setTimeout(r, 250)); // Tempo para renderizar menu

            const itensMenu = document.querySelectorAll('ytd-menu-service-item-renderer, tp-yt-paper-item');
            let clicou = false;
            for (let item of itensMenu) {
                if (item.innerText.includes("Remover") || item.innerText.includes("Remove")) {
                    item.click();
                    clicou = true;
                    contadorLocal++;
                    break;
                }
            }

            if (!clicou) document.body.click();
            await new Promise(r => setTimeout(r, 300)); // Espera o YouTube processar
        }
        callback(contadorLocal);
    } catch (e) {
        callback(0);
    }
}
limpar();
"""


def executar_limpeza():
    total_removido = 0
    browser = criar_browser()

    try:
        browser.get("https://www.youtube.com/playlist?list=LL")
        time.sleep(5)

        while True:
            try:
                print("Ativando 'Exibir vídeos indisponíveis'...")

                wait = WebDriverWait(browser, 10)
                # Seletor robusto para o botão de três pontos do cabeçalho da playlist
                botao_menu_xpath = "//ytd-playlist-header-renderer//yt-button-shape//button"
                botao = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, botao_menu_xpath)))
                browser.execute_script("arguments[0].click();", botao)

                time.sleep(1)

                # Procura pela opção tanto em português quanto em inglês
                xpath_opcao = "//yt-formatted-string[contains(text(), 'Exibir vídeos indisponíveis') or contains(text(), 'Show unavailable videos')]"
                elemento_opcao = wait.until(
                    EC.element_to_be_clickable((By.XPATH, xpath_opcao)))
                browser.execute_script("arguments[0].click();", elemento_opcao)

                time.sleep(2)
                print("Vídeos indisponíveis agora estão visíveis.")

            except Exception:
                print("Aviso: Opção de vídeos ocultos não encontrada ou já ativa.")

            try:
                print(f"--- Processando Lote --- (Total: {total_removido})")

                # Executa o JS
                resultado = browser.execute_async_script(JS_ESTAVEL)
                removidos_no_ciclo = int(resultado) if isinstance(
                    resultado, (int, float)) else 0
                total_removido += removidos_no_ciclo
                time.sleep(1)

                if removidos_no_ciclo == 0:
                    print("Lote vazio. Tentando scroll...")
                    browser.execute_script(
                        "window.scrollTo(0, document.documentElement.scrollHeight);")
                    time.sleep(3)
                    if len(browser.find_elements("css selector", "ytd-playlist-video-renderer")) == 0:
                        print("Fim da playlist.")
                        break

                # Refresh frequente para liberar memória
                browser.refresh()
                time.sleep(3)

            except WebDriverException:
                print("Conexão perdida com o Chrome. Reiniciando o driver...")
                browser.quit()
                time.sleep(5)
                browser = criar_browser()
                browser.get("https://www.youtube.com/playlist?list=LL")
                time.sleep(5)

    except KeyboardInterrupt:
        print("Interrompido pelo usuário.")
    finally:
        print(f"--- PROCESSO FINALIZADO --- Total removido: {total_removido}")
        browser.quit()


if __name__ == "__main__":
    executar_limpeza()
