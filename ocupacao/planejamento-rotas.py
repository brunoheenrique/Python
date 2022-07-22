from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as condicaoEsperada
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
from datetime import timedelta
from pymsgbox import *
from loguru import logger
import pandas as pd
import pyperclip as pc
import time
import os

class Vvlog_UX:

    def __init__(self) -> None:
        logger.success('Consulta no site iniciado com sucesso.')
        # self.proxy = '10.228.5.31:8080'
        self.diretorio_download = os.getcwd()
        self.arquivoParametros = os.getcwd() + "\\" + 'Parametros.txt'
        self.arquivoUpload = os.getcwd() + "\\bd_entregas.csv"
        usuario, senha, dias, unidades = self.carrega_parametros(self.arquivoParametros)
        self.usuarioTms = usuario[0]
        self.senhaTms = senha[0]
        self.usuarioSP = usuario[1]
        self.senhaSP = senha[1]
        self.listaUnidade = unidades
        self.arquivos = ['entrega']
        self.lDataInicial = (datetime.now() - timedelta(days=dias)).strftime('%d-%m-%Y')
        self.lDataFinal = datetime.today().strftime('%d-%m-%Y')
        self.urlEntrega = 'http://vvlog.uxdelivery.com.br/Entregas/EntregaVolumeConsulta'
        self.urlSharePoint = 'https://viavarejo.sharepoint.com/sites/planejamento_frotas/Documentos%20Compartilhados/Forms/AllItems.aspx?id=%2Fsites%2Fplanejamento%5Ffrotas%2FDocumentos%20Compartilhados%2F01%5FBases&viewid=70a085b1%2Dbd32%2D44c5%2D9eff%2D42aba6cfb708'
        self.nomeArquivoSaida = ['bd_entregas.csv']
            
    def start(self):
        self.limpa_pasta(self.diretorio_download, self.arquivos)
        self.carrega_pagina_web()
        self.login()
        self.consulta_entrega(self.listaUnidade)
        self.aguarda_download(self.diretorio_download)
        self.renomear_arquivo(self.diretorio_download, self.arquivos, self.nomeArquivoSaida)
        self.uploadSharePoint()

        time.sleep(1)
        self.driver.quit()
        logger.success('Consulta finalizada com sucesso.')

    def carrega_parametros(self, caminhoArquivo):
        logger.info('Verificando login e dias de extração.')
        try:
            plan = pd.read_table(caminhoArquivo, header=None, sep=":")  # latin-1
            usr = str(plan[1][0]).split(", ")
            senha = str(plan[1][1]).split(", ")
            dias = int(plan[1][2])
            unidades = str(plan[1][3]).split(", ")
            logger.info(f'Usuário: {usr}\nExtração de: {dias} dias')
            return usr, senha, dias, unidades
        except:
            pass
            logger.warning('Não foi possivel ler o arquivo')

    def carrega_pagina_web(self) -> None:

        options = Options()
        # if not self.proxy == '':
        #     options.add_argument(f'--proxy-server={self.proxy}')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('prefs', {
            "download.default_directory": self.diretorio_download,
            "download.Prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        options.add_argument("--start-maximized")
        logger.info('Iniciando Browser')
        try:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            self.wait = WebDriverWait(self.driver, 2)
            self.wait2 = WebDriverWait(self.driver, 120)
        except:
            logger.critical('Não foi possivel abrir a pagina web.')
            time.sleep(2)

    def login(self) -> None:
        logger.info('Realizando login')
        lLogin: str = "//input[@id='login']"
        lSenha: str = "//input[@id='senha']"
        lEntrar: str = '//button[@type="submit"]'
        lAlerta: str = '//div[@class="alert alert-error"]'
        lCampoVazio: str = '//span[@class="field-validation-error"]'
        lTitulo: str = '/html/body/div[2]/div/section[1]/h1'

        self.driver.get(self.urlEntrega)

        try:
            login = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lLogin)))
            login.send_keys(self.usuarioTms)
        except:
            pass
            logger.critical('Campo login não encontrado.')

        try:
            senha = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSenha)))
            senha.send_keys(self.senhaTms)
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

        time.sleep(5)
        if self.valida_elemento(By.XPATH, lAlerta):
            tipo_erro = self.wait.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lAlerta))).text
            logger.warning('Login não efetuado')
            alert(tipo_erro, "Erro de Login")
            self.driver.quit()
        elif self.valida_elemento(By.XPATH, lCampoVazio):
            erro_campo = self.wait.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lCampoVazio)))
            str_erro: str = ''
            for erro in erro_campo:
                str_erro + erro.text + '\n'

            logger.warning('Campos Vazios')
            alert(str_erro, "Campos Vazios")
            self.driver.quit()

        try:
            self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lTitulo)))
        except TimeoutException as e:
            logger.warning('Tempo de Login atingido.\nVerifique sua conexão e tente novamente.')
            alert(
                'Tempo de Login atingido.\nVerifique sua conexão e tente novamente.', "Tempo de Login")
            self.driver.quit()

    def consulta_entrega(self, listaUnidade) -> None:
        lTitulo: str = '/html/body/div[2]/div/section[1]/h1'
        lBotaoFilial: str = '/html/body/div[2]/div/section[2]/div[3]/div[2]/form/div[2]/div[2]/div/div[3]/div[1]/button'
        lSelecionaDataInicial = '//*[@id="dtIniRecepcao"]'
        lSelecionaDataFinal = '//*[@id="dtFimRecepcao"]'
        lSelecionaSaida: str = '//*[@id="flagTipoSaida"]'
        lBuscar: str = '/html/body/div[2]/div/section[2]/div[3]/div[2]/form/div[2]/div[2]/div/div[12]/div/div/button'
        lBarraProgress: str = '//*[@id="barraProgressoExcel"]/div'
        lDownload: str = '//*[@id="btDownload"]'

        try:
            self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lTitulo)))
        except TimeoutException as e:
            logger.warning('Tempo de Login atingido.\nVerifique sua conexão e tente novamente.')
            alert(
                'Tempo de Login atingido.\nVerifique sua conexão e tente novamente.', "Tempo de Login")
            self.driver.quit()

        time.sleep(2)

        try:
            bt_filial = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lBotaoFilial)))
            bt_filial.click()
        except:
            pass
            logger.warning('Elemento bt_filial não encontrado.')
        
        try:
            for unidade in listaUnidade:
                unidade: str = unidade.strip()
                selecionaUnidade = self.wait2.until(
                    condicaoEsperada.presence_of_element_located((By.XPATH,F'//*[@class="btn-group col-xs-12 no-padding open"]/ul/li/a/label[contains(text(), "{unidade}")]')))
                selecionaUnidade.click()
        except:
            pass
            logger.warning('Unidade não encontrado.')

        try:
            selecaoDataFinal = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaDataFinal)))
            selecaoDataFinal.click()
            selecaoDataFinal.send_keys(self.lDataFinal)
        except:
            pass
            logger.warning('Elemento selecaoDataFinal não encontrado.')

        try:
            selecaoDataInicial = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaDataInicial)))
            selecaoDataInicial.click()
            selecaoDataInicial.send_keys(self.lDataInicial)
        except:
            pass
            logger.warning('Elemento selecaoDataInicial não encontrado.')

        try:
            bt_filial = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lBotaoFilial)))
            bt_filial.click()
        except:
            pass
            logger.warning('Elemento bt_filial não encontrado.')

        try:
            selecaoSaida = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaSaida)))
            selecaoSaida_object = Select(selecaoSaida)
            selecaoSaida.click()
            selecaoSaida_object.select_by_value('excel')
        except:
            pass
            logger.warning('Elemento selecaoSaida não encontrado.')

        try:
            bt_buscar = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lBuscar)))
            bt_buscar.click()
        except:
            pass
            logger.warning('Elemento bt_buscar não encontrado.')

        self.barra_progresso(lBarraProgress, lDownload)
    
    def uploadSharePoint(self):
        lEmail: str = '//*[@type="email"]'
        lAvançar: str = '//*[@type="submit"]'
        lEsperaSenha: str = '//*[@id="loginHeader"]/div[contains(text(),"senha")]'
        lPassword: str = '//*[@type="password"]'
        lConfirmar: str = '//div[contains(text(),"Continuar")]'
        lEntrar: str = '//*[@id="idSIButton9"]'
        lTitulo: str = '//*[@id="appRoot"]/div[1]/div[2]/div[3]/div/div[2]/div[1]/div/div/div/div/div[2]/div/div[2]/span/div/span'
        lBotao: str = '//*[@name="Carregar"]'
        lArquivo: str = '//*[@aria-label="Arquivos"]'
        lUpload: str = '/html/body/div/input'
        lCarregar: str = '//*[@data-icon-name="Sync"]'
        lSubstituir: str = '//*[@name="Substituir"]'
        
        self.driver.get(self.urlSharePoint)

        try:
            botao = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lEmail)))
            botao.send_keys(self.usuarioSP)
        except:
            pass
            logger.warning('Elemento botao não encontrado.')

        try:
            botao = self.wait2.until(
                condicaoEsperada.element_to_be_clickable((By.XPATH, lAvançar)))
            botao.click()
        except:
            pass
            logger.warning('Elemento botao não encontrado.')
        
        try:
            bt_espera_senha = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lEsperaSenha)))
        except:
            pass
            logger.warning('Elemento botao não encontrado.')

        try:
            botao = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lPassword)))
            botao.send_keys(self.senhaSP)
        except:
            pass
            logger.warning('Elemento botao não encontrado.')
        
        try:
            botao = self.wait2.until(
                condicaoEsperada.element_to_be_clickable((By.XPATH, lEntrar)))
            botao.click()
        except:
            pass
            logger.warning('Elemento botao não encontrado.')

        try:
            bt_espera_confirma = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lConfirmar)))
        except:
            pass
            logger.warning('Elemento botao não encontrado.')

        try:
            botao = self.wait2.until(
                condicaoEsperada.element_to_be_clickable((By.XPATH, lEntrar)))
            botao.click()
        except:
            pass
            logger.warning('Elemento botao não encontrado.')

        try:
            self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lTitulo)))
        except TimeoutException as e:
            logger.warning('Tempo de Login atingido.\nVerifique sua conexão e tente novamente.')
            alert(
                'Tempo de Login atingido.\nVerifique sua conexão e tente novamente.', "Tempo de Login")
            self.driver.quit()

        try:
            botao = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lBotao)))
            botao.click()
        except:
            pass
            logger.warning('Elemento botao não encontrado.')
        
        try:
            bt_arquivo = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lArquivo)))
            bt_arquivo.click()
        except:
            pass
            logger.warning('Elemento botao não encontrado.')

        try:
            bt_upload = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lUpload)))
        except:
            pass
            logger.warning('Elemento botao não encontrado.')
        
        # ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

        try: 
            bt_upload.send_keys(str(self.arquivoUpload).replace("//", "/"))
        
            while self.valida_elemento(By.XPATH, lCarregar): time.sleep(5)

            try:
                bt_arquivo = self.wait2.until(
                    condicaoEsperada.presence_of_element_located((By.XPATH, lSubstituir)))
                bt_arquivo.click()

                while self.valida_elemento(By.XPATH, lCarregar): time.sleep(5)
            except:
                pass
                logger.warning('Elemento botao não encontrado.')
        except:
            logger.warning('Arquivo não encontrado')

    def arquivo_atual(self, nomeArquivo, diretorio, indice: int = 1):
        l_arquivos = os.listdir(diretorio)
        l_datas = []
        time.sleep(2)
        
        for arquivo in l_arquivos:
            if nomeArquivo in arquivo:
                data = os.path.getmtime(os.path.join(os.path.realpath(diretorio), arquivo))
                l_datas.append((data, arquivo))

        try:
            l_datas.sort(reverse=True)
            # for i in l_datas:
            #     print(i)
            ult_arquivo = l_datas[0]
            nome_arquivo = ult_arquivo[1]
            data_arquivo = ult_arquivo[0]
            arq = os.path.join(os.path.realpath(diretorio), nome_arquivo)
            data_mod = self.data_modificacao(arq)
            # return nome_arquivo, data_arquivo
            caminhoArquivo = os.getcwd() + '\\' + nome_arquivo
            return caminhoArquivo
        except:
            return 'Nenhum arquivo Localizado.'

    def data_modificacao(self, arquivo):

        ti_m = os.path.getmtime(arquivo)

        m_ti = time.ctime(ti_m)
        t_obj = time.strptime(m_ti)
        T_stamp = time.strftime("%d/%m/%Y %H:%M:%S", t_obj)

        logger.info(f"Ultima atualização dop arquivo em {T_stamp}")
        return T_stamp

    def aguarda_download(self, caminho):
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
        try:
            self.driver.find_element(by=tipo, value=path)
        except NoSuchElementException as e:
            return False
        return True

    def barra_progresso(self, lBarraProgress, lDownload):
        logger.info('Aguardando barra de progresso')
        time.sleep(3)
        if self.valida_elemento(By.XPATH, lBarraProgress):
            pa = 0
            while True:
                percentual = self.wait2.until(
                    condicaoEsperada.presence_of_element_located((By.XPATH, lBarraProgress))).text
                try:
                    p = int(percentual.replace("%", ""))
                except:
                    p = 0

                if p % 10 == 0 and p != "" and p != pa:
                    logger.debug(f'{percentual}')
                    pa = p
                if percentual == '100%':
                    logger.debug(f'Carregamento {percentual} Concluido.')
                    time.sleep(2)
                    try:
                        download_arquivo = self.wait2.until(
                            condicaoEsperada.presence_of_element_located((By.XPATH, lDownload)))
                        download_arquivo.click()
                        logger.info('Aguardando Download')
                        time.sleep(2)
                    except:
                        pass
                        logger.warning('Elemento download_arquivo não encontrado.')
                    break

    def limpa_pasta(self, caminho, nomeArquivo):
        logger.warning('Limpando pasta...')
        for f in os.listdir(caminho):
            if nomeArquivo[0] in f or '.tmp' in f:
                os.remove(os.path.join(caminho, f))

    def renomear_arquivo(self, diretorio, nomesOrigem, nomesDestino):
        logger.info('Renomeando arquivos baixados.')
        l_arquivos = os.listdir(diretorio)
        l_datas = []
        l_nomesOrigem = nomesOrigem
        l_nomesDestino = nomesDestino

        for arquivo in l_arquivos:
            if l_nomesOrigem[0] in arquivo:
                data = os.path.getmtime(os.path.join(os.path.realpath(diretorio), arquivo))
                l_datas.append((data, arquivo))

        try:
            l_datas.sort(reverse=True)
            ult_arquivo = l_datas[0]
            nome_arquivo = ult_arquivo[1]
            caminhoOrigem = os.getcwd() + '\\' + nome_arquivo
            caminhoDestino = os.getcwd() + '\\' + l_nomesDestino[0]
            os.rename(caminhoOrigem, caminhoDestino)

        except:
            return 'Nenhum arquivo Localizado.'

if __name__ == '__main__':
    executa = Vvlog_UX()
    executa.start()