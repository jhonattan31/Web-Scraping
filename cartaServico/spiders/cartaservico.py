import scrapy
import re
#import pandas as pd

import time

def multipleReplace(text):
    return "".join(["" if char in "0123456789.()-_/\&;:~!?,\"" else char for char in text])

def funTrata(dados):
    if(dados == None):
        return 'Vazio'
    if(dados.isspace()):
        return 'Vazio'
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

total = 9000
current_page = 324
#teste = pd.read_excel('C://Users//jh0nn//Documents//TesteRasas//rasa_ontologias_exemplo-master//dados.xls')

class CartaservicoSpider(scrapy.Spider):
    name = 'cartaservico'
    def start_requests(self):
        urls = [
            'https://cartadeservicos.ce.gov.br/ConsultaCesec/pg_cs_servico_detalhe.aspx?idservico='+str(current_page),
        ]
        for url in urls:
            #print(url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        global current_page
        global total
        #print(current_page)
        page = response.url.split("=")[-1]
        #print(page)
        
        if page != None:
            #print(page)
            num_page = int(page)
            carta_servico = {}
            if(response.xpath('//*[(@id = "ctl00_body_lblServico")]/text()').get().isspace() and not response.xpath('//*[(@id = "ctl00_body_lblServico")]//p/text()').get().isspace()):
                carta_servico['nom_servico'] = multipleReplace(funTrata(response.xpath('//*[(@id = "ctl00_body_lblServico")]//p/text()').get().replace('\n', "").replace('  ',' ').replace('solicitar', '').strip()))
            elif(response.xpath('//*[(@id = "ctl00_body_lblServico")]/text()').get().isspace() and response.xpath('//*[(@id = "ctl00_body_lblServico")]//p/text()').get().isspace()):
                vetor = response.xpath('//*[(@id = "ctl00_body_lblServico")]//p/text()').getall()
                for item in vetor:
                    if(not item.isspace()):
                        carta_servico['nom_servico'] = multipleReplace(funTrata(item.replace('\n', "").replace('  ',' ')))
                        break
            else:
                carta_servico['nom_servico'] = multipleReplace(funTrata(response.xpath('//*[(@id = "ctl00_body_lblServico")]/text()').get().replace('\n', "").replace('\n', "").replace('  ',' ').replace('solicitar', '').strip()))
            if carta_servico['nom_servico'] != None:
                carta_servico['cod_servico'] = num_page
                                
                carta_servico['dsc_poder'] = funTrata(response.xpath('//*[(@id="ctl00_body_lblPoder")]/text()').get())
                carta_servico['nom_orgao'] = funTrata(response.xpath('//*[(@id="ctl00_body_lblOrgao")]/text()').get())
            #    #carta_servico['nom_categoria'] = funTrata()
                carta_servico['dsc_servico'] = funTrata(response.xpath('//*[(@id="ctl00_body_lbFinalidade")]/text()').get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                nomServ = ['dsc_solicitante', 'dsc_prazo_entrega', 'dsc_servico_gratuito', 'dsc_doc_necessarios', 'dsc_etapas_atendimento', 'dsc_tempo_atendimento_priori', 'dsc_endereco', 'dsc_tempo_atendiment', 'dsc_horario_atendimento', 'nom_unidade_prestadora', 'nom_area_responsavel', 'dsc_servico_digital', 'publico_alvo', 'dsc_legislacao', 'dsc_requisitos']
                for index in nomServ:                    
                    if(response.xpath('//*[(@id="ctl00_body_lblSolicitante")]/text()').get() != None and index == 'dsc_solicitante'):
                        carta_servico[index] = funTrata(response.xpath('//*[(@id="ctl00_body_lblSolicitante")]/text()').get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                    elif(response.xpath('//*[(@id = "ctl00_body_lblPrazoEntrega")]/text()').get() != None and index == 'dsc_prazo_entrega'):
                        carta_servico[index] = funTrata(response.xpath('//*[(@id = "ctl00_body_lblPrazoEntrega")]/text()').get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                    elif(response.xpath('//*[@id="ctl00_body_lblServicoGratuito"]/text()').get() != None and index == 'dsc_servico_gratuito'):
                        carta_servico[index] = funTrata(response.xpath('//*[(@id="ctl00_body_lblServicoGratuito")]/text()').get())
                        if(response.xpath('//*[@id="ctl00_body_lblServicoGratuito"]//p/text()').get() != None):
                            carta_servico[index] += funTrata(response.xpath('//*[@id="ctl00_body_lblServicoGratuito"]/p/text()').get())                
                    elif(response.xpath('//*[(@id="ctl00_body_lblDocNecessarios")]/text()').get() != None and index == 'dsc_doc_necessarios'):
                        carta_servico[index] = funTrata(response.xpath('//*[(@id="ctl00_body_lblDocNecessarios")]/text()').get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                    elif(response.xpath('//*[(@id="ctl00_body_lblEtapas")]/text()').get() != None and index == 'dsc_etapas_atendimento'):
                        carta_servico[index] = funTrata(response.xpath('//*[(@id="ctl00_body_lblEtapas")]/text()').get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                    elif(response.xpath('//*[(@id="ctl00_body_lblTempoMedioPriori")]/text()').get() != None and index == 'dsc_tempo_atendimento_priori'):
                        carta_servico[index] = funTrata(response.xpath('//*[(@id="ctl00_body_lblTempoMedioPriori")]/text()').get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())    
                    elif(response.xpath('//*[(@id="ctl00_body_lblEndereco")]/text()').get() != None and index == 'dsc_endereco'):
                        carta_servico[index] = funTrata(response.xpath('//*[(@id="ctl00_body_lblEndereco")]/text()').get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                    elif(response.xpath('//*[(@id="ctl00_body_lblTempoMedio")]/text()').get() != None and index == 'dsc_tempo_atendiment'):
                        carta_servico[index] = funTrata(response.xpath('//*[(@id="ctl00_body_lblTempoMedio")]/text()').get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                    elif(response.xpath('//*[(@id="ctl00_body_lblHorarioAtendimento")]/text()').get() != None and index == 'dsc_horario_atendimento'):
                        carta_servico[index] = funTrata(response.xpath('//*[(@id="ctl00_body_lblHorarioAtendimento")]/text()').get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                    elif(response.xpath('//*[(@id = "ctl00_body_lblUndPrestadora")]/text()').get() != None and index == 'nom_unidade_prestadora'):
                        carta_servico[index] = funTrata(response.xpath('//*[(@id = "ctl00_body_lblUndPrestadora")]/text()').get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                    elif(response.xpath('//*[(@id = "ctl00_body_lblAreaResponsavel")] /text()').get() != None and index == 'nom_area_responsavel'):
                        carta_servico[index] = funTrata(response.xpath('//*[(@id = "ctl00_body_lblAreaResponsavel")] /text()').get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                    elif(response.xpath('//*[(@id = "ctl00_body_lblDigital")]/text()').get() != None and index == 'dsc_servico_digital'):
                        carta_servico[index] = funTrata(response.xpath('//*[(@id = "ctl00_body_lblDigital")]/text()').get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                    elif(response.xpath('//*[(@id="ctl00_body_lblPublicoAlvo")]/text()').get() != None and index == 'publico_alvo'):
                        carta_servico[index] = funTrata(response.xpath('//*[(@id="ctl00_body_lblPublicoAlvo")]/text()').get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                    elif(response.xpath('//*[(@id = "ctl00_body_lblLegs")]/text()').get() != None and index == 'dsc_legislacao'):
                        carta_servico[index] = funTrata(response.xpath('//*[(@id = "ctl00_body_lblLegs")]/text()').get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                    elif(response.xpath('//*[(@id = "ctl00_body_lbRequisitos")]/text()').get() != None and index == 'dsc_requisitos'):
                        carta_servico[index] = funTrata(response.xpath('//*[(@id = "ctl00_body_lbRequisitos")]/text()').get().replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                    else:
                        carta_servico[index] = 'Vazio'
                cont = []
                
                if(response.css('#ctl00_body_lblFormaAcesso ::text').getall() != None):
                    vetor = response.css('#ctl00_body_lblFormaAcesso ::text').getall()
                    for index, row in enumerate(vetor):
                        if(row == 'Presencial: '):
                            carta_servico['dsc_acesso_presencial'] = funTrata(vetor[index+1].replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                            cont.append('presencial')
                        elif(row == 'Online: '):
                            carta_servico['dsc_acesso_online'] = funTrata(vetor[index+1].replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                            cont.append('online')
                        elif(row == 'Telefônico: '):
                            carta_servico['dsc_acesso_telefone'] = funTrata(vetor[index+1].replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower())
                            cont.append('telefone')
               
                print(cont) 

                vetor2 = response.css('#ctl00_body_divlblFormaAcomp b::text').getall()
                for v in vetor2:
                    if(v == 'Presencial: ' and vetor2.count() == 3):
                        carta_servico['dsc_acesso_presencial_acomp'] = funTrata(response.css('#ctl00_body_lblFormaAcomp::text').get())
                        carta_servico['dsc_acesso_presencial_acomp'] = carta_servico['dsc_acesso_presencial_acomp'].replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower()
                    elif(v == 'Presencial: ' and vetor2.count() == 2):
                        carta_servico['dsc_acesso_presencial_acomp'] = funTrata(response.css('#ctl00_body_lblFormaAcomp::text').get())
                        carta_servico['dsc_acesso_presencial_acomp'] = carta_servico['dsc_acesso_presencial_acomp'].replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower()
                    elif(v == 'Online: ' and vetor2.count() == 3):
                        carta_servico['dsc_acesso_online_acomp'] = funTrata(response.css('#ctl00_body_lblFormaAcomp p::text').get())
                        carta_servico['dsc_acesso_online_acomp'] = carta_servico['dsc_acesso_online_acomp'].replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower()
                    elif(v == 'Online: ' and vetor2.count() == 2):
                        carta_servico['dsc_acesso_online_acomp'] = funTrata(response.css('#ctl00_body_lblFormaAcomp::text').get())
                        carta_servico['dsc_acesso_online_acomp'] = carta_servico['dsc_acesso_online_acomp'].replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower()
                    elif(v == 'Telefônico: ' and vetor2.count() == 3):
                        carta_servico['dsc_acesso_telefone_acomp'] = funTrata(response.css('#ctl00_body_lblFormaAcomp a::text').get())
                        carta_servico['dsc_acesso_telefone_acomp'] = carta_servico['dsc_acesso_telefone_acomp'].replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower()
                    elif(v == 'Telefônico: ' and vetor2.count() == 2):
                        carta_servico['dsc_acesso_telefone_acomp'] = funTrata(response.css('#ctl00_body_lblFormaAcomp p::text').get())
                        carta_servico['dsc_acesso_telefone_acomp'] = carta_servico['dsc_acesso_telefone_acomp'].replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower()
                    elif(v == 'Telefônico: ' and vetor2.count() == 1):
                        carta_servico['dsc_acesso_telefone_acomp'] = funTrata(response.css('#ctl00_body_lblFormaAcomp::text').get())
                        carta_servico['dsc_acesso_telefone_acomp'] = carta_servico['dsc_acesso_telefone_acomp'].replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower()
                    else:
                        carta_servico['dsc_acesso_online_acomp'] = funTrata(response.css('#ctl00_body_lblFormaAcomp::text').get())
                        carta_servico['dsc_acesso_online_acomp'] = carta_servico['dsc_acesso_online_acomp'].replace(';', '*').replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('\xa0', ' ').replace('\"', ' ').replace('  ', ' ').strip().lower()                
            yield carta_servico               
                           
        while(current_page < total):
            current_page += 1
            #page = response.url.split("=")[-1] 
            #print("page ", page)
            next_page = response.url.split("=")[0]+"="+str(current_page)#response.urljoin(current_page)
            if (next_page is not None):
                yield response.follow(next_page, callback=self.parse)