#!/usr/bin/python
# coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import csv
import codecs
import sys

def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
        csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
        for row in csv_reader:
            yield [unicode(cell, 'utf-8') for cell in row]

def remove_first_line_from_file(authors_file_name):
    with codecs.open(authors_file_name, 'r', encoding='utf-8') as fin:
        data = fin.read().splitlines(True)
    with codecs.open(authors_file_name, 'w', encoding='utf-8') as fout:
        fout.writelines(data[1:])


if __name__ == '__main__':
    profile = webdriver.FirefoxProfile()
    profile.set_preference('permissions.default.stylesheet', 2)
    profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    profile.set_preference('browser.download.dir', os.getcwd()+'/data')
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/zip')
    driver = webdriver.Firefox(firefox_profile=profile)
    driver.implicitly_wait(30)
    base_url = 'http://buscatextual.cnpq.br/buscatextual'

    if (len(sys.argv)>1):
        prefix_file_name = sys.argv[1]
        authors_file_name = prefix_file_name+'_authors.csv'
        downloaded_file_name = prefix_file_name+'_downloaded.csv'
        error_file_name = prefix_file_name+'_error.csv'
        not_found_file_name = prefix_file_name+'_not_found.csv'
    else:
        authors_file_name = 'authors.csv'
        downloaded_file_name = 'downloaded.csv'
        error_file_name = 'error.csv'
        not_found_file_name = 'not_found.csv'

    try:
        csv_reader = unicode_csv_reader(open(authors_file_name))
    except:
    	driver.quit()
        sys.exit('Erro ao abrir o arquivo '+authors_file_name)

    ids_downloaded = os.listdir(os.getcwd()+'/data')

    for row in csv_reader:
        author_name = row[0]
        paper_title = row[1].encode('utf-8')

        driver.get(base_url)
        driver.find_element_by_id('textoBusca').clear()
        driver.find_element_by_id('textoBusca').send_keys(author_name)
        driver.find_element_by_id('buscarDemais').click()
        driver.find_element_by_id('botaoBuscaFiltros').click()

        if not 'Nenhum resultado foi encontrado para:' in driver.page_source.encode('utf-8'):
            resultado_geral = driver.find_element_by_class_name('resultado')
            resultados = resultado_geral.find_elements_by_tag_name('a')
            ids = []

            for resultado in resultados:
                ids.append(resultado.get_attribute('href')[24:34])
            
            paper_found = False
            for id in ids:
                if not paper_found:
                    print(author_name.encode('utf-8')+' - '+paper_title)
                    print(base_url+'/visualizacv.do?id='+id)
                    driver.get(base_url+'/visualizacv.do?id='+id)

                    # QUEBRAR CAPTCHA #
                    driver.implicitly_wait(31622400)
                    informacoes_autor = driver.find_element_by_class_name('informacoes-autor')
                    page_source = driver.page_source.encode('utf-8')
                    if paper_title.lower().replace(' ', '') in page_source.lower().replace(' ', ''):
                        paper_found = True
                        id_autor_xml = informacoes_autor.find_element_by_tag_name('li')
                        id_autor_xml = id_autor_xml.text[-16:]

                        if not (id_autor_xml+'.zip') in ids_downloaded:
                            print(base_url+'/download.do?idcnpq='+id_autor_xml)
                            driver.get(base_url+'/download.do?idcnpq='+id_autor_xml)

                            # QUEBRAR CAPTCHA #
                            WebDriverWait(driver, 31622400).until(EC.invisibility_of_element_located((By.ID, 'btn_validar_captcha')))
                        ids_downloaded.append(id_autor_xml+'.zip')

                        with open(downloaded_file_name, 'a') as downloaded_file:
                            downloaded_file.write('"'+author_name.encode('utf-8')+'","'+paper_title+'"\n')
                        break

            if not paper_found:
                with open(error_file_name, 'a') as error_file:
                    error_file.write('"'+author_name.encode('utf-8')+'","'+paper_title+'"\n')
        else:
            with open(not_found_file_name, 'a') as not_found_file:
                    not_found_file.write('"'+author_name.encode('utf-8')+'","'+paper_title+'"\n')

        remove_first_line_from_file(authors_file_name)

    driver.quit()