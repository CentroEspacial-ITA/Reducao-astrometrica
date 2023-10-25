# Importar as bibliotecas necessárias
# Sistema operacional
import os 
from shutil import make_archive 

# Importar a biblioteca pandas para manipulação de dados tabulares
import pandas as pd

# Importar a classe datetime e timedelta para trabalhar com datas e intervalos de tempo
from datetime import datetime, timedelta

# Importar a biblioteca selenium para automação do navegador
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Importar a biblioteca BeautifulSoup para análise HTML
from bs4 import BeautifulSoup

# Importar a biblioteca requests para fazer requisições HTTP
import requests

# Importar a biblioteca math para funções matemáticas
import math

# Importar a biblioteca astropy para cálculos astronômicos
import astropy

# Importar classes específicas do astropy para coordenadas e tempo
from astropy.coordinates import SkyCoord, AltAz, EarthLocation
from astropy.time import Time
import astropy.units as u


# Definir o caminho base onde o script .py está sendo executado
base_path = os.path.dirname(os.path.abspath(__file__))

# Definir o caminho para a pasta "observacoes"
path_upload = os.path.join(base_path, "observacoes\\")

# Criar o diretório "observacoes" se ele não existir
if not os.path.exists(path_upload):
    os.makedirs(path_upload)


# Configurar as opções do navegador Chrome
options = webdriver.ChromeOptions()

# Inicializar uma instância do navegador Chrome
driver = webdriver.Chrome()

# URL para web scraping

# Definir a URL do site que será alvo do web scraping
url = "https://www.heavens-above.com/AllSats.aspx?lat=-23.2178&lng=-45.8702&loc=Observat%c3%b3rio&alt=620&tz=EBST"

# Abrir a página e aguardar o carregamento

# Abrir a URL no navegador
driver.get(url)

# Aguardar até 8 segundos para o carregamento completo da página
driver.implicitly_wait(8)

# Obter o conteúdo HTML após a execução do JavaScript

# Obter o código HTML da página carregada
html = driver.page_source

# Criar um objeto BeautifulSoup para análise do HTML
soup = BeautifulSoup(html, "html.parser")

# Encontrar todas as linhas da tabela de satélites

# Encontrar todas as linhas da tabela de satélites na página
rows = soup.find_all("tr", class_="clickableRow")

# Iniciar uma lista para armazenar os dados extraídos
data = []

# Loop pelas linhas da tabela para extrair informações
for row in rows:
    columns = row.find_all("td")
    if len(columns) >= 11:
        # Extrair informações das colunas
        satellite_name = columns[0].text
        satellite_designator = columns[1].text
        # Extrair informações sobre os três momentos de passagem
        pass_time_1, pass_altitude_1, pass_direction_1 = columns[2:5]
        pass_time_2, pass_azimuth_2, pass_direction_2 = columns[5:8]
        pass_time_3, pass_altitude_3, pass_direction_3 = columns[8:11]
        # Criar o link para mais informações
        link = "https://www.heavens-above.com/" + (row.find("a")["href"] if row.find("a") else "")
        # Adicionar os dados à lista
        data.append([
            satellite_name, satellite_designator,
            pass_time_1.text, pass_altitude_1.text, pass_direction_1.text,
            pass_time_2.text, pass_azimuth_2.text, pass_direction_2.text,
            pass_time_3.text, pass_altitude_3.text, pass_direction_3.text,
            link
        ])

# Fechar o navegador controlado pelo Selenium
driver.quit()

# Criar DataFrame com os dados extraídos

# Definir os nomes das colunas para o DataFrame
columns = [
    "Name", "Brightness_mag",
    "Time_start", "Altitude_start", "Azimuth_start",
    "Time_highest", "Altitude_highest", "Azimuth_highest",
    "Time_end", "Altitude_end", "Azimuth_end",
    "link"
]

# Criar um DataFrame a partir dos dados extraídos e das colunas definidas
df = pd.DataFrame(data, columns=columns)

# Filtrar dados conforme critérios

# Extrair apenas o valor numérico da coluna "Altitude_highest"
df["Altitude_highest"] = df["Altitude_highest"].str.extract(r"(\d+)").astype(float)

# Criar filtro para altitudes maiores ou iguais a 30
altitude_filter = df["Altitude_highest"] >= 30

# Converter strings de horário em objetos de tempo e criar filtro para horário de início após as 18:15
time_filter = df["Time_start"].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time() > datetime.strptime("18:15:00", "%H:%M:%S").time())

# Aplicar os filtros de altitude e horário ao DataFrame original
tabela = df[altitude_filter & time_filter]

# Filtrar dados para criar novo DataFrame

# Converter a coluna "Time_highest" para o formato de hora
tabela["Time_highest"] = pd.to_datetime(tabela["Time_highest"], format="%H:%M:%S")

# Inicializar uma lista com o primeiro valor da tabela filtrada
lista = [tabela.iloc[0].values]

# Loop para filtrar os dados de acordo com o critério de tempo mínimo entre passagens
for i in range(1, len(tabela)):
    # Verificar se a diferença entre os horários é maior ou igual a 10 minutos
    if pd.Timedelta(tabela.iloc[i]["Time_highest"] - lista[-1][5]) >= timedelta(minutes=10):
        lista.append(tabela.iloc[i].values)

# Criar DataFrame com lista filtrada
filtered_df = pd.DataFrame(lista, columns=columns)

# Extrair a parte de horário da coluna "Time_highest"
filtered_df['Time_highest'] = filtered_df['Time_highest'].astype(str).str[11:]
tabela['Time_highest'] = tabela['Time_highest'].astype(str).str[11:]

# Configuração para tirar screenshots das URLs no DataFrame filtrado

# Definir o nome do driver do Chrome
DRIVER = 'chromedriver'

# Inicializar uma lista para armazenar os nomes dos screenshots
screenshot_names = []

# Inicializar o navegador novamente
driver = webdriver.Chrome()

# Tirar screenshots das URLs no DataFrame filtrado
for index, row in filtered_df.iterrows():
    # Obter a URL e o nome do satélite
    url = row['link']
    satellite_name = row['Name']
    
    # Abrir a URL no navegador
    driver.get(url)
    
    # Realizar a rolagem para baixo na página
    driver.execute_script("window.scrollTo(0, 120)")  # Ajuste o valor conforme necessário

    # Reduzir o zoom da página
    driver.execute_script('document.body.style.zoom = "65%"')
    
    # Definir o nome do arquivo de screenshot
    screenshot_filename = path_upload + f"{satellite_name}.png"
    
    # Salvar o screenshot
    driver.save_screenshot(screenshot_filename)
    screenshot_names.append(screenshot_filename)
    
    # Obter o conteúdo HTML atualizado
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Encontrar a tabela de altitude máxima
    max_altitude_table = soup.find("table", class_="standardTable")
 
    if max_altitude_table:
        # Encontrar a linha relevante na tabela de altitude máxima
        max_altitude_row = max_altitude_table.find_all("tr")[3]  # Terceira linha da tabela, desconsiderando o título
        if max_altitude_row:
            # Extrair o valor de azimuth da célula apropriada
            max_azimuth = max_altitude_row.find_all("td")[3].text
            filtered_df.at[index, 'Azimuth_highest'] = max_azimuth

# Fechar o navegador
driver.quit()

# Função para converter AltAz em Equatorial

# Definir uma função para converter coordenadas AltAz em coordenadas Equatoriais
def altaz_to_equatorial(azimuth, altitude, latitude, longitude, time):
    observer_location = EarthLocation(lat=latitude*u.deg, lon=longitude*u.deg, height=0*u.m)
    altaz_coord = SkyCoord(az=azimuth, alt=altitude, frame=AltAz(obstime=time, location=observer_location))
    equatorial_coord = altaz_coord.transform_to('icrs')
    return equatorial_coord

# Converter 'Azimuth_highest', 'Altitude_highest' e 'Time_highest' para Equatorial (RA e Dec)

# Inicializar uma lista para armazenar as coordenadas Equatoriais calculadas
equatorial_coords = []

# Loop para calcular as coordenadas Equatoriais para cada satélite filtrado
for index, row in filtered_df.iterrows():
    # Extrair valores do DataFrame
    azimuth_highest = float(row['Azimuth_highest'].split('°')[0])
    altitude_highest = row['Altitude_highest']
    time_highest = Time(pd.to_datetime(row['Time_highest']))
    latitude = -23.2178
    longitude = -45.8702
    
    # Chamar a função para calcular as coordenadas Equatoriais
    equatorial_coord = altaz_to_equatorial(azimuth_highest*u.deg, altitude_highest*u.deg, latitude, longitude, time_highest)
    
    # Adicionar as coordenadas à lista
    equatorial_coords.append(equatorial_coord)

# Adicionar as colunas 'RA' e 'Dec' ao DataFrame
filtered_df['RA'] = [coord.ra.to_string(unit=u.hour, precision=2, pad=True, fields=3, alwayssign=True) for coord in equatorial_coords]
filtered_df['Dec'] = [coord.dec.to_string(unit=u.deg, precision=2, pad=True, alwayssign=True) for coord in equatorial_coords]

# Crie um arquivo Excel com duas planilhas: "Filtrados" e "Todos"

# Definir o nome do arquivo Excel
excel_filename = os.path.join(path_upload, "tabelinha.xlsx")

# Criar um arquivo Excel com duas planilhas: "Filtrados" e "Todos"
with pd.ExcelWriter(excel_filename) as writer:
    filtered_df.to_excel(writer, sheet_name="Filtrados", index=False)
    tabela.to_excel(writer, sheet_name="Todos", index=False)

# Compactar a pasta "observacoes" em um arquivo .zip
zip_filename = os.path.join(base_path, "observacoes")
make_archive(zip_filename, 'zip', path_upload)

# Exibir o DataFrame filtrado
print(filtered_df)
