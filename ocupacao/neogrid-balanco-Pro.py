from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as condicaoEsperada
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
from datetime import timedelta
from pymsgbox import *
from loguru import logger
import warnings
import pandas as pd
import numpy as np
import time
import os

class Neogrid_Venda:

    def __init__(self) -> None:
        warnings.simplefilter(action='ignore', category=FutureWarning)
        logger.success('Consulta no site iniciado com sucesso.')
        # self.proxy = '10.228.5.31:8080'
        self.diretorio_download = os.getcwd() + "\\BASE"
        self.arquivoParametros = os.getcwd() + '\\Parametros.txt'
        self.saidaArquivo = os.getcwd() + "\\BASE\\VENDA_APPROVED.csv"
        self.dePara = os.getcwd() + '\\DePara_Loja_CD.csv'
        usuario, senha, dias, setor = self.carrega_parametros(self.arquivoParametros)
        self.lista_de_tempo = []
        self.usuario = usuario
        self.senha = senha
        self.setor = setor
        self.arquivos = ['VENDA']
        self.lDataInicial = (datetime.now()- timedelta(days= dias + 1)).strftime('%d-%m-%Y')
        self.lDataFinal = (datetime.now()- timedelta(days = 1)).strftime('%d-%m-%Y')
        self.numeroDiaInicial = (datetime.now()- timedelta(days= dias + 1)).strftime('%d')
        self.numeroDiaFinal = (datetime.now()- timedelta(days = 1)).strftime('%d')
        self.url = 'https://planning-viavarejo.neogrid.com/planning/login.xhtml'
        self.urlRelatorio = 'https://planning-viavarejo.neogrid.com/planning/consultaDadosCustomizado.jsp'

    def start(self):
        self.limpa_pasta(self.diretorio_download, self.arquivos)
        self.carrega_pagina_web()
        self.login()
        self.relatorio_venda()
        self.realiza_download(self.setor)
        self.aguarda_download(self.diretorio_download)
        self.caminhoArquivo = self.arquivo_recente(self.diretorio_download)
        self.resumir_dados(self.dePara, self.caminhoArquivo, self.saidaArquivo)

        time.sleep(2)
        self.driver.quit()
        logger.success('Extração finalizada com sucesso.')

    def carrega_parametros(self,caminhoArquivo):
        logger.info('Verificando login e dias de extração.')
        try:
            plan = pd.read_table(caminhoArquivo, header=None, sep=":")  # latin-1
            usr = str(plan[1][0]).strip()
            senha = str(plan[1][1]).strip()
            dias = int(plan[1][2])
            setor = str(plan[1][3]).split(", ")
            logger.info(f'\nUsuário: {usr}\nExtração de: {dias} dias\nSetor: {setor}')
            return usr, senha, dias, setor
        except:
            pass
            logger.warning('Não foi possivel ler o arquivo')
            
    def carrega_pagina_web(self) -> None:

        options = Options()
        # if not self.proxy == '':
        #     options.add_argument(f'--proxy-server={self.proxy}')
        # options.add_argument('--headless')
        # options.add_argument("--log-level=4")
        options.add_argument("--start-maximized")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('prefs', {
            "download.default_directory": self.diretorio_download,
            "download.Prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        logger.info('Iniciando Browser')
        try:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            self.wait = WebDriverWait(self.driver, 1)
            self.wait2 = WebDriverWait(self.driver, 120)
            self.driver.get(self.url)
        except:
            logger.critical('Não foi possivel abrir a pagina web.')
        
        time.sleep(1)

    def login(self) -> None:
        logger.info('Realizando login')
        lLogin: str = '//*[@id="txtLogin"]'
        lSenha: str = '//*[@id="txtSenha"]'
        lEntrar: str = '//*[@id="btnEntrar"]'
        lAlerta: str = '//*[@id="growlMensagens_container"]/div/div/div[2]/span'
        lTitulo: str = '//*[@id="menu"]/ul/li[2]/a/span[1]'
        try:
            login = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lLogin)))
            login.send_keys(self.usuario)
        except:
            pass
            logger.critical('Campo login não encontrado.')

        try:
            senha = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSenha)))
            senha.send_keys(self.senha)
        except:
            pass
            logger.critical('Campo senha não encontrado.')

        try:
            bt_entrar = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lEntrar)))
            bt_entrar.click()
        except:
            pass
            logger.critical('Botão entrar não encontrado.')

        time.sleep(2)
        if self.valida_elemento(By.XPATH, lAlerta):
            tipo_erro = self.wait.until(
            condicaoEsperada.presence_of_element_located((By.XPATH, lAlerta))).text
            logger.warning('Login não efetuado')
            alert(tipo_erro, "Erro de Login")
            self.driver.quit()
        
        try:
            self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lTitulo)))
        except TimeoutException as e:
            logger.warning('Tempo de Login atingido.\nVerifique sua conexão e tente novamente.')
            alert(
                'Tempo de Login atingido.\nVerifique sua conexão e tente novamente.', "Tempo de Login")
            self.driver.quit()

    def relatorio_venda(self) -> None: #, listaRomaneios: list
        lMonitoramento: str = '//*[@id="menu"]/ul/li[4]'
        lRelatorio: str = '//*[@id="menu"]/ul/li[4]/ul/li/a/span[text() = "VENDA ON E OFF - APPROVED"]'
        lBarraProgress: str = '//*[@id="modalTransicao"]'

        try:
            selecionar = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lMonitoramento)))
            selecionar.click()
            selecionar.click()
        except:
            pass
            logger.warning('Elemento selecionar não encontrado.')

        try:
            selecionaRelatorio  = self.wait2.until(
                    condicaoEsperada.presence_of_element_located((By.XPATH,lRelatorio)))
            selecionaRelatorio.click()
        except:
            logger.warning('Relatorio não encontrado.')
            self.driver.quit()

        logger.info(f'Relatório VENDA ON E OFF - APPROVED')
        
        while self.valida_elemento(By.XPATH, lBarraProgress):
            pass
                   
    def realiza_download(self, listaSetor) -> None:
        lTitle: str = '//*[@id="labelItem"]'
        lSelecionaSetor: str = '//*[@id="itemGrupo1BtnSelCheck"]'
        lSetor: str = '//*[@id="itemGrupo1_panel"]/div[2]/ul/li[0]/label'
        lSetorCheck: str = '//*[@id="itemGrupo1_panel"]/div[2]/ul/li[1]/div/div[2]'
        lSetorFecha: str = '//*[@id="itemGrupo1_panel"]/div[1]/a'
        lCaixaInicio: str = '//*[@id="dataGenerica1"]/button'
        lCaixaFim: str = '//*[@id="dataGenerica2"]/button'
        lDataInicio: str = f'//*[@id="ui-datepicker-div"]/div[1]/table/tbody/tr/td/a[text() ={self.numeroDiaInicial}]'
        lDataFim: str = f'//*[@id="ui-datepicker-div"]/div[1]/table/tbody/tr/td/a[text() ={self.numeroDiaFinal}]'
        lSelecionaMes: str = '//*[@id="ui-datepicker-div"]/div[1]/div/div/select[1]'
        lSelecionaSaida: str = '//*[@id="btnPesquisar"]'
        lBarraProgress: str = '//*[@id="modalTransicao"]'
        lBotaoCsv = '//*[@id="j_idt77"]'

        try:
            titulo = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lTitle)))
        except:
            pass
            logger.warning('elemento não encontrado.')
        
        time.sleep(1)

        try:
            selecaoSetor = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaSetor)))
            selecaoSetor.click()
        except:
            pass
            logger.warning('elemento não encontrado.')
        
        while self.valida_elemento(By.XPATH, lBarraProgress):
            pass

        try:
            for setor in listaSetor:
                setor = setor.strip()
                selecionaRelatorio = self.wait2.until(
                    condicaoEsperada.presence_of_element_located((By.XPATH,F'//*[@id="itemGrupo1_panel"]/div/ul/li/label[text() = "{setor}"]')))
                selecionaRelatorio.click()
        except:
            pass
            logger.warning('Relatorio não encontrado.')
        
        try:
            selecaoFecha = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSetorFecha)))
            selecaoFecha.click()
        except:
            pass
            logger.warning('elemento não encontrado.')

        while self.valida_elemento(By.XPATH, lBarraProgress):
            pass

        # try:
        #     selecaoDataInicial = self.wait2.until(
        #         condicaoEsperada.presence_of_element_located((By.XPATH, '//*[@id="dataGenerica1_input"]')))
        #     selecaoDataInicial.send_keys('22/06/2022')
        # except:
        #     pass
        #     logger.warning('elemento não encontrado.')

        try:
            selecaoDataInicial = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lCaixaInicio)))
            selecaoDataInicial.click()
        except Exception as e:
            print(e)
            pass
            logger.warning('elemento não encontrado.')

        time.sleep(1)

        try:
            selecaoMes = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaMes)))
            selecao_object = Select(selecaoMes)
            try:
                numeroMes = int(self.lDataInicial[3:5]) - 1
            except:
                numeroMes = 0
            selecao_object.select_by_value(str(numeroMes))
        except:
            pass
            logger.warning('elemento selecaoTipo não encontrado.')
        
        time.sleep(1)

        try:
            selecaoDia = self.wait.until(
                        condicaoEsperada.presence_of_element_located((By.XPATH,lDataInicio)))
            selecaoDia.click()
        except:
            pass
            logger.warning('Relatorio não encontrado.')

        try:
            selecaoDatafim = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lCaixaFim)))
            selecaoDatafim.click()
        except:
            pass
            logger.warning('elemento não encontrado.')
        
        try:
            selecaoDia = self.wait.until(
                    condicaoEsperada.presence_of_element_located((By.XPATH,lDataFim)))
            selecaoDia.click()
        except:
            pass
            logger.warning('Relatorio não encontrado.')

        try:
            selecaoPesquisa = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaSaida)))
            selecaoPesquisa.click()
        except:
            pass
            logger.warning('elemento não encontrado.')
        
        logger.info('Pesquisando...')

        time.sleep(2)
        
        while self.valida_elemento(By.XPATH, lBarraProgress):
            pass
        
        time.sleep(1)

        try:
            selecaoCsv = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lBotaoCsv)))
            selecaoCsv.click()
        except:
            pass
            logger.warning('elemento não encontrado.')
            
        logger.info('Download CSV')
        
        while self.valida_elemento(By.XPATH, lBarraProgress):
            pass

        time.sleep(2)
        
    def aguarda_download(self,caminho): 
        fileends = "crdownload"
        logger.info('Downloading em andamento, aguarde...')
        while "crdownload" == fileends:
            time.sleep(2)
            newest_file = self.arquivo_recente(caminho)
            if "crdownload" in newest_file:
                fileends = "crdownload"
            else:
                fileends = "none"
                logger.info('Downloading Completo...')

    def arquivo_recente(self, caminho):
        path = caminho
        os.chdir(path)
        files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
        newest = files[-1]
        return newest

    def valida_elemento(self, tipo, path) -> bool:
        # logger.info('Aguardando processamento...')
        try:
            lVisibilidade = self.wait.until(
                condicaoEsperada.visibility_of_element_located((tipo, path)))
        except:
            return False
        return True
                
    def limpa_pasta(self, caminho, nomeArquivo):
        logger.warning('Limpando pasta...')
        for f in os.listdir(caminho):
            if nomeArquivo[0] in f or '.tmp' in f:
                os.remove(os.path.join(caminho,f))

    def resumir_dados(self, dePara, caminhoArquivo, saidaArquivo):
        logger.warning('Resumindo dados por CD...')
        baseDePara = pd.read_csv(dePara, sep=';')
        baseVenda = pd.read_csv(caminhoArquivo, sep=';')

        baseVenda['QUANTIDADE_VENDA'] = baseVenda['QUANTIDADE_VENDA'].str.replace(".", "").str.replace(",",".")

        baseVenda[['QUANTIDADE_VENDA']] = baseVenda[['QUANTIDADE_VENDA']].apply(pd.to_numeric) 

        baseConsolidada = pd.merge(baseVenda, baseDePara, how= 'left', on= 'FILIAL')

        baseConsolidadaTable = pd.pivot_table(baseConsolidada, values=["QUANTIDADE_VENDA"], 
            index=["CANAL", "CD ATENDE", "SETOR", "ITEM", "DESCRICAO", "DIRETORIA", "ESPECIE", "MARCA"], aggfunc=np.sum, fill_value=0)

        baseConsolidadaTable.to_csv(saidaArquivo)
        logger.success('Dados resumidos!')

if __name__ == '__main__':
    executa = Neogrid_Venda()
    executa.start()