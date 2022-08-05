from pickle import NONE
import scrapy
import re
#import settings
#import pandas as pd
import time
from dotenv import load_dotenv
import os

load_dotenv()
URL_BASE = os.getenv("URL_BASE")
URL_SERVICOS = os.getenv("URL_SERVICOS")
ID_SERVICO_MIN = os.getenv("ID_SERVICO_MIN")
ID_SERVICO_MAX = os.getenv("ID_SERVICO_MAX")
COD_SERVICO = os.getenv("COD_SERVICO")
DSC_PODER = os.getenv("DSC_PODER")
DSC_ORGAO = os.getenv("DSC_ORGAO")
DSC_SECRETARIA = os.getenv("DSC_SECRETARIA")
DSC_SERVICO = os.getenv("DSC_SERVICO")
DSC_CATEGORIA = os.getenv("DSC_CATEGORIA")
NOM_SERVICO = os.getenv("NOM_SERVICO")
DSC_SOLICITANTE = os.getenv("DSC_SOLICITANTE")
PRAZO_ENTREGA = os.getenv("PRAZO_ENTREGA")
SERV_GRATUITO = os.getenv("SERV_GRATUITO")
DOS_NECES = os.getenv("DOC_NECES")
ETAPAS = os.getenv("ETAPAS")
TEMPO_PRIOR = os.getenv("TEMPO_PRIOR")
ENDERECO = os.getenv("ENDERECO")
TEMPO_ATEND = os.getenv("TEMPO_ATEND")
HOR_FUNC = os.getenv("HOR_FUNC")
UNID_PRES = os.getenv("UNID_PRES")
AREA_RESPON = os.getenv("AREA_RESPON")
PUBLICO_ALVO = os.getenv("PUBLICO_ALVO")
LEGIS = os.getenv("LEGIS")
REQUI = os.getenv("REQUI")
SERV_DIGITAL = os.getenv("SERV_DIGITAL")
FORMA_ACESSO = os.getenv("FORMA_ACESSO")

def multipleReplace(text):
    return "".join(["" if char in "0123456789.()-_/\&;:~!?,\"" else char for char in text])

def limparDados(dados):
    if(dados == None):
        return ''
    if(dados.isspace()):
        return ''
    dados = dados.lower()
    dados.replace(';', '*')
    dados.replace(',', '*')
    dados.replace('\t', ' ')
    dados.replace('\r', ' ')
    dados.replace('\n', ' ')
    dados.replace('  ', ' ')
    dados.replace('"', ' ')
    dados.replace('\xa0', ' ')
    dados = dados.strip()
    return dados

current_page = ID_SERVICO_MIN

class CartaservicoSpider(scrapy.Spider):
    name = 'cartaservico'
    def start_requests(self):
        if (URL_SERVICOS == None or URL_SERVICOS == []):
            urls = [
                URL_BASE + str(current_page),
            ]
            for url in urls:
                #print(url)
                yield scrapy.Request(url=url, callback=self.parse)
        else:
            for s in URL_SERVICOS:
                next_page = s
                if (next_page is not None):
                    scrapy.Request(next_page, callback=self.parse)


    def parse(self, response):
        global current_page
        global total
        #print(current_page)
        page = response.url.split("=")[-1]
        #print(page)
    
        if page != None:
            
            carta_servico = {}
            
            carta_servico['nom_servico'] = multipleReplace(limparDados(response.xpath(NOM_SERVICO).get().replace('\n', "").replace('  ',' ').replace('solicitar', '').strip().lower()))
            if carta_servico['nom_servico'] != None:
                carta_servico['cod_servico'] = limparDados(response.xpath(COD_SERVICO).get())
                carta_servico['dsc_poder'] = limparDados(response.xpath(DSC_PODER).get())
                carta_servico['nom_orgao'] = limparDados(response.xpath(DSC_ORGAO).get())
                carta_servico['nom_secretaria'] = limparDados(response.xpath(DSC_SECRETARIA).get())
                carta_servico['nom_categoria'] = limparDados(response.xpath(DSC_CATEGORIA).get())
                carta_servico['dsc_servico'] = limparDados(response.xpath(DSC_SERVICO).get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                nomServ = ['dsc_solicitante', 'dsc_prazo_entrega', 'dsc_servico_gratuito', 'dsc_doc_necessarios', 'dsc_etapas_atendimento', 'dsc_tempo_atendimento_priori', 'dsc_endereco', 'dsc_servico_digital', 'dsc_tempo_atendiment', 'dsc_horario_atendimento', 'nom_unidade_prestadora', 'nom_area_responsavel', 'publico_alvo', 'dsc_legislacao', 'dsc_requisitos']
                for index in nomServ:                    
                    if(response.xpath(DSC_SOLICITANTE).get() != None and index == 'dsc_solicitante'):
                        carta_servico[index] = limparDados(response.xpath(DSC_SOLICITANTE).get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                    elif(response.xpath(PRAZO_ENTREGA).get() != None and index == 'dsc_prazo_entrega'):
                        carta_servico[index] = limparDados(response.xpath(PRAZO_ENTREGA).get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                    elif(response.xpath(SERV_GRATUITO).get() != None and index == 'dsc_servico_gratuito'):
                        carta_servico[index] = limparDados(response.xpath(SERV_GRATUITO).get())
                    elif(response.xpath(DOS_NECES).get() != None and index == 'dsc_doc_necessarios'):
                        carta_servico[index] = limparDados(response.xpath(DOS_NECES).get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                    elif(response.xpath(ETAPAS).get() != None and index == 'dsc_etapas_atendimento'):
                        carta_servico[index] = limparDados(response.xpath(ETAPAS).get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                    elif(response.xpath(TEMPO_PRIOR).get() != None and index == 'dsc_tempo_atendimento_priori'):
                        carta_servico[index] = limparDados(response.xpath(TEMPO_PRIOR).get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())    
                    elif(response.xpath(ENDERECO).get() != None and index == 'dsc_endereco'):
                        carta_servico[index] = limparDados(response.xpath(ENDERECO).get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                    elif(response.xpath(TEMPO_ATEND).get() != None and index == 'dsc_tempo_atendiment'):
                        carta_servico[index] = limparDados(response.xpath(TEMPO_ATEND).get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                    elif(response.xpath(HOR_FUNC).get() != None and index == 'dsc_horario_atendimento'):
                        carta_servico[index] = limparDados(response.xpath(HOR_FUNC).get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                    elif(response.xpath(UNID_PRES).get() != None and index == 'nom_unidade_prestadora'):
                        carta_servico[index] = limparDados(response.xpath(UNID_PRES).get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                    elif(response.xpath(AREA_RESPON).get() != None and index == 'nom_area_responsavel'):
                        carta_servico[index] = limparDados(response.xpath(AREA_RESPON).get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                    elif(response.xpath(SERV_DIGITAL).get() != None and index == 'dsc_servico_digital'):
                        carta_servico[index] = limparDados(response.xpath(SERV_DIGITAL).get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                    elif(response.xpath(PUBLICO_ALVO).get() != None and index == 'publico_alvo'):
                        carta_servico[index] = limparDados(response.xpath(PUBLICO_ALVO).get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                    elif(response.xpath(LEGIS).get() != None and index == 'dsc_legislacao'):
                        carta_servico[index] = limparDados(response.xpath(LEGIS).get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                    elif(response.xpath(REQUI).get() != None and index == 'dsc_requisitos'):
                        carta_servico[index] = limparDados(response.xpath(REQUI).get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                    else:
                        carta_servico[index] = ''
                cont = []
                
                if(response.css(FORMA_ACESSO).getall() != None):
                    vetor = response.css(FORMA_ACESSO).getall()
                    for index, row in enumerate(vetor):
                        if(row == 'Presencial: '):
                            carta_servico['dsc_acesso_presencial'] = limparDados(vetor[index+1].replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                            cont.append('presencial')
                        elif(row == 'Online: '):
                            carta_servico['dsc_acesso_online'] = limparDados(vetor[index+1].replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                            cont.append('online')                
            yield carta_servico               
                           
        if (URL_SERVICOS == None or URL_SERVICOS == []):
            while(current_page < ID_SERVICO_MAX):
                current_page += 1
                next_page = response.url.split("=")[0]+"="+str(current_page)#response.urljoin(current_page)
                if (next_page is not None):
                    yield response.follow(next_page, callback=self.parse)
        else:
            for s in URL_SERVICOS:
                next_page = s
                if (next_page is not None):
                    yield response.follow(next_page, callback=self.parse)