from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def coleta_noticia_banner(id_noticia, id_descricao):
    noticias_banner = driver.find_elements(By.XPATH, "//div[@class='bstn-hl-wrapper']")

    # alinhando tela as noticias de banner
    driver.execute_script(f'window.scrollTo(0, 300)')
    sleep(1)
    driver.execute_script(f'window.scrollTo(0, 520)')
    sleep(1)

    noticias_lista = []
    descricao_noticias_lista = []

    for noticia_banner in noticias_banner:

        noticias_dict = {}

        id_noticia += 1
        noticias_dict['id_noticia'] = id_noticia

        titulo = noticia_banner.find_element(By.CSS_SELECTOR, ".bstn-hl-mainitem")
        noticias_dict['titulo_noticia'] = titulo.text

        elemento_link = noticia_banner.find_element(By.CSS_SELECTOR,".bstn-hl-link")
        link = elemento_link.get_attribute("href")
        noticias_dict['link_noticia'] = link

        subtitulos = noticia_banner.find_elements(By.CSS_SELECTOR, ".bstn-hl-relateditem")

        for subtitulo in subtitulos:
            descricao_noticias_dict = {}
            id_descricao += 1
            descricao_noticias_dict['id_descricao'] = id_descricao
            descricao_noticias_dict['id_noticia'] = id_noticia
            descricao_noticias_dict['descricao_noticia'] = subtitulo.text
            descricao_noticias_lista.append(descricao_noticias_dict)

        # print
        path = "C://Info4//WebScrapping//Estudo//estudo_webscraping_spge//imagens_noticias//"
        noticia_banner.screenshot(path + str(id_noticia) + 'img.png')

        noticias_lista.append(noticias_dict)

    return id_noticia, id_descricao, noticias_lista, descricao_noticias_lista


def coleta_noticias(id_noticia, id_descricao):
    noticias = driver.find_elements(By.XPATH, "//div[@class='feed-post bstn-item-shape type-materia']")

    noticias_lista = []
    descricao_noticias_lista = []

    for noticia in noticias:

        noticias_dict = {}

        id_noticia += 1
        noticias_dict['id_noticia'] = id_noticia

        titulo = noticia.find_element(By.CSS_SELECTOR, ".feed-post-body-title ._evt")
        noticias_dict['titulo_noticia'] = titulo.text

        elemento_link = noticia.find_element(By.CSS_SELECTOR, ".feed-post-figure-link")
        link = elemento_link.get_attribute("href")
        noticias_dict['link_noticia'] = link

        subtitulos = noticia.find_elements(By.CSS_SELECTOR, ".bstn-fd-relatedtext")
        for subtitulo in subtitulos:
            descricao_noticias_dict = {}
            id_descricao += 1
            descricao_noticias_dict['id_descricao'] = id_descricao
            descricao_noticias_dict['id_noticia'] = id_noticia
            descricao_noticias_dict['descricao_noticia'] = subtitulo.text
            descricao_noticias_lista.append(descricao_noticias_dict)

        resumos = noticia.find_elements(By.CSS_SELECTOR, ".feed-post-body-resumo")
        for resumo in resumos:
            descricao_noticias_dict = {}
            id_descricao += 1
            descricao_noticias_dict['id_descricao'] = id_descricao
            descricao_noticias_dict['id_noticia'] = id_noticia
            descricao_noticias_dict['descricao_noticia'] = resumo.text
            descricao_noticias_lista.append(descricao_noticias_dict)

        # print
        driver.execute_script(f'window.scrollTo(0, {noticia.location['y'] - 150})')
        path = "C://Info4//WebScrapping//Estudo//estudo_webscraping_spge//imagens_noticias//"
        noticia.screenshot(path + str(id_noticia) + 'img.png')

        noticias_lista.append(noticias_dict)

    return id_noticia, id_descricao, noticias_lista, descricao_noticias_lista


def envia_email_noticias(corpo_email, lista_ids):
    msg = MIMEMultipart()

    msg['Subject'] = 'Noticias SP GE'
    msg['From'] = 'BOT Noticias SP GE'
    msg['To'] = 'brenoraeder97@gmail.com'

    msg.attach(MIMEText(corpo_email))

    for ids in lista_ids:
        with open(f'C://Info4//WebScrapping//Estudo//estudo_webscraping_spge//imagens_noticias//{ids}img.png', 'rb') as img_file:
            img = MIMEImage(img_file.read())
            img.add_header('Content-Disposition', 'attachment', filename='imagem.jpg')
            msg.attach(img)

    arquivo_senha = open("C://Info4//WebScrapping//Estudo//email_teste//env.txt", "r")
    senha = arquivo_senha.read()

    MyServer = smtplib.SMTP('smtp.gmail.com', 587)
    MyServer.starttls()
    MyServer.login('t9047688@gmail.com', senha)
    MyServer.send_message(msg)
    MyServer.quit()

    print('Email enviado')


def verifica_noticias(noticias_df, descriao_noticias_df):
    i = 0
    corpo_email = ''
    lista_ids = []
    lista_procura = ["Lucas", "Beraldo", "Pablo Maia", "Calleri", "Galopo", "Luciano", "Rafinha", "contratação", "mercado", "saída"]
    for noticia in noticias_df['titulo_noticia']:
        i += 1
        for palavra_procura in lista_procura:
            if palavra_procura in noticia:
                corpo_email += "Titulo da Notícia (" + palavra_procura + "): \n" + noticia + "\n\n"
                descricoes = descricao_noticias_df.loc[descricao_noticias_df['id_noticia'] == i]
                for descricao in descricoes['descricao_noticia']:
                    corpo_email += "Subtiutlo: \n" + descricao + "\n"
                links = noticias_df['link_noticia'].loc[noticias_df['id_noticia'] == i]
                for link in links:
                    corpo_email += "Link da Noticia: " + link + "\n"
                corpo_email += "\n ---\n\n"
                lista_ids.append(i)

    envia_email_noticias(corpo_email, lista_ids)


#############


# usando web driver para abrir e maximizar a página
driver = webdriver.Chrome()
driver.get('https://ge.globo.com/futebol/times/sao-paulo/')
driver.maximize_window()

sleep(3)

# descendo até o final da página
for i in range(4):
    driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
    sleep(2)

# fechando alerta de cookies
alerta_cookies = driver.find_element(By.XPATH, "//button[@class='cookie-banner-lgpd_accept-button']")
alerta_cookies.click()

# id para as noticias
id_noticia = 0
# id para as descricoes
id_descricao = 0

# recebendo lista de noticias e descrição
id_noticia, id_descricao, lista_noticias_banner, lista_descricao_noticias_banner = coleta_noticia_banner(id_noticia,
                                                                                                         id_descricao)
id_noticia, id_descricao, lista_noticias, lista_descricao_noticias = coleta_noticias(id_noticia, id_descricao)

# tranformando em df
noticias_banner_df = pd.DataFrame(lista_noticias_banner)
descricao_noticias_banner_df = pd.DataFrame(lista_descricao_noticias_banner)
noticias_df = pd.DataFrame(lista_noticias)
descricao_noticias_df = pd.DataFrame(lista_descricao_noticias)

# concatenando os df
noticias_df = pd.concat([noticias_banner_df, noticias_df], ignore_index=True)
descricao_noticias_df = pd.concat([descricao_noticias_banner_df, descricao_noticias_df], ignore_index=True)

print(noticias_df)
print(descricao_noticias_df)

# salvando como csv
path = "C://Info4//WebScrapping//Estudo//estudo_webscraping_spge//tabelas_noticias//"
noticias_df.to_csv(path + "noticias.csv", index=False)
descricao_noticias_df.to_csv(path + "descricao_noticias.csv", index=False)

# email
verifica_noticias(noticias_df, descricao_noticias_df)
