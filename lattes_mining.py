#!/usr/bin/python
# coding=utf-8

authors_file_name = 'wie_authors.csv'
downloaded_file_name = 'wie_downloaded.csv'
error_file_name = 'wie_error.csv'
not_found_file_name = 'wie_not_found.csv'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import unittest
import csv
import codecs

def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
        csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
        for row in csv_reader:
            yield [unicode(cell, 'utf-8') for cell in row]

def remove_first_line_from_file(file_name):
    with codecs.open(file_name, 'r', encoding='utf-8') as fin:
        data = fin.read().splitlines(True)
    with codecs.open(file_name, 'w', encoding='utf-8') as fout:
        fout.writelines(data[1:])

class LattesBusca(unittest.TestCase):

    def setUp(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.download.dir', os.getcwd()+'/data')
        profile.set_preference('browser.download.folderList', 2)
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/zip')
        self.driver = webdriver.Firefox(firefox_profile=profile)
        self.driver.implicitly_wait(30)
        self.base_url = 'http://buscatextual.cnpq.br/buscatextual'
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_lattes_busca(self):
        erros, acertos = 0, 0
        driver = self.driver
        file_name = authors_file_name
        csv_reader = unicode_csv_reader(open(file_name))
        ids_downloaded = os.listdir(os.getcwd()+'/data')
        for id_downloaded in ids_downloaded:
            ids_downloaded = ids_downloaded[:-4]
        print(ids_downloaded)
        for row in csv_reader:
            author_name = row[0]
            paper_title = row[1].encode('utf-8')
            driver.get(self.base_url)
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
                        print(self.base_url+'/visualizacv.do?id='+id)
                        driver.get(self.base_url+'/visualizacv.do?id='+id)
                        # QUEBRAR CAPTCHA #
                        driver.implicitly_wait(31622400)
                        informacoes_autor = driver.find_element_by_class_name('informacoes-autor')
                        page_source = driver.page_source.encode('utf-8')
                        if paper_title.lower().replace(' ', '') in page_source.lower().replace(' ', ''):
                            paper_found = True
                            id_autor_xml = informacoes_autor.find_element_by_tag_name('li')
                            id_autor_xml = id_autor_xml.text[-16:]
                            if not id_autor_xml in ids_downloaded:
                                print(self.base_url+'/download.do?idcnpq='+id_autor_xml)
                                driver.get(self.base_url+'/download.do?idcnpq='+id_autor_xml)
                                # QUEBRAR CAPTCHA #
                                WebDriverWait(driver, 31622400).until(EC.invisibility_of_element_located((By.ID, 'btn_validar_captcha')))
                            ids_downloaded.append(id_autor_xml)
                            with open(downloaded_file_name, 'a') as downloaded_file:
                                downloaded_file.write('"'+author_name.encode('utf-8')+'","'+paper_title+'"\n')
                            break
                if not paper_found:
                    with open(error_file_name, 'a') as error_file:
                        error_file.write('"'+author_name.encode('utf-8')+'","'+paper_title+'"\n')
            else:
                with open(not_found_file_name, 'a') as not_found_file:
                        not_found_file.write('"'+author_name.encode('utf-8')+'","'+paper_title+'"\n')
            remove_first_line_from_file(file_name)

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
