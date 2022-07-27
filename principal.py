from bs4 import BeautifulSoup
import requests
import os

class App:

    pais = '(Brazil)'
    time1 = 'Nautico Recife'
    time2 = 'Sport Recife'

    def __init__(self, time1, time2):
        self.time1 = time1
        self.time2 = time2
        url = requests.get(f'https://www.statarea.com/compare/teams/{time1} {self.pais}/{time2} {self.pais}').content
        self.site = BeautifulSoup(url, 'html.parser')

    def sequencia_jogos(self):
        ultparts = self.site.find('div', class_='lastteamsmatches')
        timesparts = ultparts.find_all('div', class_='formastext')
        contadorpart = 1

        for timepart in timesparts:
            if contadorpart == 1:
                time1 = timepart.text
                time1 = list(time1)
            elif contadorpart == 2:
                time2 = timepart.text
                time2 = list(time2)
            else:
                break
            contadorpart += 1

        return time1, time2

    def contasequencia(self, sequencia):
        score_sequencia = 0
        for letter in sequencia:
            if letter == 'D':
                score_sequencia += 0
            elif letter == 'W':
                score_sequencia += 1
            elif letter == 'L':
                score_sequencia += -1
            else:
                print('Erro score_sequencia')
                pass

        return score_sequencia

    def confrontos(self):

        areaconfrontos = self.site.find('div', class_='facts')
        if areaconfrontos == None:
            confrontos = {'disputas': '0', f'{self.time1}-ganhou' : '0', f'{self.time2}-ganhou' : '0', 'empates' : '0'}
            return confrontos
        confrontosgeral = areaconfrontos.find_all('div', class_='datarow')
        confrontos = {}
        confcontador = 0
        for dadoconfronto in confrontosgeral:
            dadotemporario = dadoconfronto.find_next('div', class_='value')
            if confcontador == 0:
                confrontos['disputas'] = dadotemporario.text
            if confcontador == 1:
                confrontos[f'{self.time1}-ganhou'] = dadotemporario.text
            if confcontador == 2:
                confrontos[f'{self.time2}-ganhou'] = dadotemporario.text
            if confcontador == 3:
                confrontos['empates'] = dadotemporario.text
            if confcontador > 3:
                break
            confcontador += 1

        return confrontos

    def estatisticas10jogos(self):

        statsdezjogos = self.site.find('div', class_='teamsstatistics')
        time1stats = statsdezjogos.find_all('div', class_='halfcontainer')[0]
        time2stats = statsdezjogos.find_all('div', class_='halfcontainer')[1]
        doistimesstats = [time1stats, time2stats]
        doistimescont = 0
        time1dict = None
        time2dict = None

        for timesstat in doistimesstats:
            stats10 = timesstat.find_all_next('div', class_='factitem')

            for factitem in stats10:
                tdict_temp = {}
                if doistimescont == 0:
                    time_temp = self.time1
                elif doistimescont == 1:
                    time_temp = self.time2
                tdict_temp['time'] = time_temp
                tdict_temp['vitorias'] = stats10[0].find('div', class_='value').text
                tdict_temp['empates'] = stats10[1].find('div', class_='value').text
                tdict_temp['derrotas'] = stats10[2].find('div', class_='value').text
                tdict_temp['media-gols-feitos'] = stats10[3].find('div', class_='value').text
                tdict_temp['media-gols-tomados'] = stats10[4].find('div', class_='value').text
                tdict_temp['fara-gol'] = stats10[5].find('div', class_='value').text
                tdict_temp['levara-gol'] = stats10[6].find('div', class_='value').text
                tdict_temp['nao-levou-gols'] = stats10[7].find('div', class_='value').text
                tdict_temp['nao-marcou-gols'] = stats10[8].find('div', class_='value').text
                tdict_temp['gols-acima-25'] = stats10[9].find('div', class_='value').text
                tdict_temp['gols-abaixo-25'] = stats10[10].find('div', class_='value').text
                tdict_temp['tempo-sem-marcar'] = stats10[11].find('div', class_='value').text
                tdict_temp['tempo-sem-levar'] = stats10[12].find('div', class_='value').text

            if doistimescont == 0:
                time1dict = tdict_temp
            else:
                time2dict = tdict_temp
            doistimescont += 1

        estatisticas10 = [time1dict, time2dict]

        return estatisticas10

    def gols10jogos(self):
        dadosgerais = self.site.find('div', class_='teamsbetstatistics')
        timesdados = dadosgerais.find_all('div', class_='halfcontainer')
        time1dados = timesdados[0]
        time2dados = timesdados[1]
        doistimesdados = [time1dados, time2dados]
        doistimescont = 0
        time1dict = None
        time2dict = None
        for timedado in doistimesdados:
            dadodict_temp = {}
            tdados = timedado.find_all_next('div', class_='barchart')
            for dado in tdados:
                if doistimescont == 0:
                    dadodict_temp['time'] = self.time1
                else:
                    dadodict_temp['time'] = self.time2

                if dadodict_temp['time'] == None:
                    continue
                dadodict_temp['time-ganha'] = dado.find_all_next('div', class_='bar')[0].text
                dadodict_temp['time-empata'] = dado.find_all_next('div', class_='bar')[1].text
                dadodict_temp['time-perde'] = dado.find_all_next('div', class_='bar')[2].text
                dadodict_temp['time-ganha-1t'] = dado.find_all_next('div', class_='bar')[3].text
                dadodict_temp['time-empata-1t'] = dado.find_all_next('div', class_='bar')[4].text
                dadodict_temp['time-perde-1t'] = dado.find_all_next('div', class_='bar')[5].text
                dadodict_temp['time-ganha-2t'] = dado.find_all_next('div', class_='bar')[6].text
                dadodict_temp['time-empata-2t'] = dado.find_all_next('div', class_='bar')[7].text
                dadodict_temp['time-perde-2t'] = dado.find_all_next('div', class_='bar')[8].text
                dadodict_temp['acima-1.5-geral'] = dado.find_all_next('div', class_='bar')[9].text
                dadodict_temp['abaixo-1.5-geral'] = dado.find_all_next('div', class_='bar')[10].text
                dadodict_temp['acima-1.5-time'] = dado.find_all_next('div', class_='bar')[11].text
                dadodict_temp['abaixo-1.5-time'] = dado.find_all_next('div', class_='bar')[12].text
                dadodict_temp['acima-2.5-geral'] = dado.find_all_next('div', class_='bar')[13].text
                dadodict_temp['abaixo-2.5-geral'] = dado.find_all_next('div', class_='bar')[14].text
                dadodict_temp['acima-2.5-time'] = dado.find_all_next('div', class_='bar')[15].text
                dadodict_temp['abaixo-2.5-time'] = dado.find_all_next('div', class_='bar')[16].text
                dadodict_temp['acima-3.5-geral'] = dado.find_all_next('div', class_='bar')[17].text
                dadodict_temp['abaixo-3.5-geral'] = dado.find_all_next('div', class_='bar')[18].text
                dadodict_temp['acima-3.5-time'] = dado.find_all_next('div', class_='bar')[19].text
                dadodict_temp['abaixo-3.5-time'] = dado.find_all_next('div', class_='bar')[20].text
                dadodict_temp['totalgols-0-1'] = dado.find_all_next('div', class_='bar')[21].text
                dadodict_temp['totalgols-2-3'] = dado.find_all_next('div', class_='bar')[22].text
                dadodict_temp['totalgols-4mais'] = dado.find_all_next('div', class_='bar')[23].text
                dadodict_temp['ambos-marcam'] = dado.find_all_next('div', class_='bar')[24].text
                dadodict_temp['so-um-marca'] = dado.find_all_next('div', class_='bar')[25].text
                dadodict_temp['nenhum-marca'] = dado.find_all_next('div', class_='bar')[26].text
                dadodict_temp['placar-impar'] = dado.find_all_next('div', class_='bar')[27].text
                dadodict_temp['placar-par'] = dado.find_all_next('div', class_='bar')[28].text
                dadodict_temp['gol-minuto-0-15'] = dado.find_all_next('div', class_='bar')[29].text
                dadodict_temp['gol-minuto-16-30'] = dado.find_all_next('div', class_='bar')[30].text
                dadodict_temp['gol-minuto-31-45'] = dado.find_all_next('div', class_='bar')[31].text
                dadodict_temp['gol-minuto-46-60'] = dado.find_all_next('div', class_='bar')[32].text
                dadodict_temp['gol-minuto-61-75'] = dado.find_all_next('div', class_='bar')[33].text
                dadodict_temp['gol-minuto-76-90'] = dado.find_all_next('div', class_='bar')[34].text
                dadodict_temp['time-gol-minuto-0-15'] = dado.find_all_next('div', class_='bar')[35].text
                dadodict_temp['time-gol-minuto-16-30'] = dado.find_all_next('div', class_='bar')[36].text
                dadodict_temp['time-gol-minuto-31-45'] = dado.find_all_next('div', class_='bar')[37].text
                dadodict_temp['time-gol-minuto-46-60'] = dado.find_all_next('div', class_='bar')[38].text
                dadodict_temp['time-gol-minuto-61-75'] = dado.find_all_next('div', class_='bar')[39].text
                dadodict_temp['time-gol-minuto-76-90'] = dado.find_all_next('div', class_='bar')[40].text
                dadodict_temp['primeirogol-sai-0-10'] = dado.find_all_next('div', class_='bar')[41].text
                dadodict_temp['primeirogol-sai-11-20'] = dado.find_all_next('div', class_='bar')[42].text
                dadodict_temp['primeirogol-sai-21-30'] = dado.find_all_next('div', class_='bar')[43].text
                dadodict_temp['primeirogol-sai-31-40'] = dado.find_all_next('div', class_='bar')[44].text
                dadodict_temp['primeirogol-sai-41-50'] = dado.find_all_next('div', class_='bar')[45].text
                dadodict_temp['primeirogol-sai-51-60'] = dado.find_all_next('div', class_='bar')[46].text
                dadodict_temp['primeirogol-sai-61-70'] = dado.find_all_next('div', class_='bar')[47].text
                dadodict_temp['primeirogol-sai-71-80'] = dado.find_all_next('div', class_='bar')[48].text
                dadodict_temp['primeirogol-sai-81-90'] = dado.find_all_next('div', class_='bar')[49].text
                dadodict_temp['primeirogol-nao-sai'] = dado.find_all_next('div', class_='bar')[50].text
                dadodict_temp['time-primeirogol-sai-0-10'] = dado.find_all_next('div', class_='bar')[51].text
                dadodict_temp['time-primeirogol-sai-11-20'] = dado.find_all_next('div', class_='bar')[52].text
                dadodict_temp['time-primeirogol-sai-21-30'] = dado.find_all_next('div', class_='bar')[53].text
                dadodict_temp['time-primeirogol-sai-31-40'] = dado.find_all_next('div', class_='bar')[54].text
                dadodict_temp['time-primeirogol-sai-41-50'] = dado.find_all_next('div', class_='bar')[55].text
                dadodict_temp['time-primeirogol-sai-51-60'] = dado.find_all_next('div', class_='bar')[56].text
                dadodict_temp['time-primeirogol-sai-61-70'] = dado.find_all_next('div', class_='bar')[57].text
                dadodict_temp['time-primeirogol-sai-71-80'] = dado.find_all_next('div', class_='bar')[58].text
                dadodict_temp['time-primeirogol-sai-81-90'] = dado.find_all_next('div', class_='bar')[59].text
                dadodict_temp['time-primeirogol-nao-sai'] = dado.find_all_next('div', class_='bar')[60].text
                dadodict_temp['time-faz-primeirogol'] = dado.find_all_next('div', class_='bar')[61].text
                dadodict_temp['oponente-faz-primeirogol'] = dado.find_all_next('div', class_='bar')[62].text
                dadodict_temp['ninguem-faz-primeirogol'] = dado.find_all_next('div', class_='bar')[63].text
                dadodict_temp['time-ganhando-aos-15'] = dado.find_all_next('div', class_='bar')[64].text
                dadodict_temp['time-perdendo-aos-15'] = dado.find_all_next('div', class_='bar')[65].text
                dadodict_temp['time-empatando-aos-15'] = dado.find_all_next('div', class_='bar')[66].text
                dadodict_temp['time-ganhando-aos-30'] = dado.find_all_next('div', class_='bar')[67].text
                dadodict_temp['time-perdendo-aos-30'] = dado.find_all_next('div', class_='bar')[68].text
                dadodict_temp['time-empatando-aos-30'] = dado.find_all_next('div', class_='bar')[69].text
                dadodict_temp['time-ganhando-aos-45'] = dado.find_all_next('div', class_='bar')[70].text
                dadodict_temp['time-perdendo-aos-45'] = dado.find_all_next('div', class_='bar')[71].text
                dadodict_temp['time-empatando-aos-45'] = dado.find_all_next('div', class_='bar')[72].text
                dadodict_temp['time-ganhando-aos-60'] = dado.find_all_next('div', class_='bar')[73].text
                dadodict_temp['time-perdendo-aos-60'] = dado.find_all_next('div', class_='bar')[74].text
                dadodict_temp['time-empatando-aos-60'] = dado.find_all_next('div', class_='bar')[75].text
                dadodict_temp['time-ganhando-aos-75'] = dado.find_all_next('div', class_='bar')[76].text
                dadodict_temp['time-perdendo-aos-75'] = dado.find_all_next('div', class_='bar')[77].text
                dadodict_temp['time-empatando-aos-75'] = dado.find_all_next('div', class_='bar')[78].text
                dadodict_temp['time-ganhando-aos-90'] = dado.find_all_next('div', class_='bar')[79].text
                dadodict_temp['time-perdendo-aos-90'] = dado.find_all_next('div', class_='bar')[80].text
                dadodict_temp['time-empatando-aos-90'] = dado.find_all_next('div', class_='bar')[81].text
                dadodict_temp['diferenca-gols-0-1'] = dado.find_all_next('div', class_='bar')[82].text
                dadodict_temp['diferenca-gols-2-3'] = dado.find_all_next('div', class_='bar')[83].text
                dadodict_temp['diferenca-gols-4mais'] = dado.find_all_next('div', class_='bar')[84].text
                dadodict_temp['maisgols-primeirotempo'] = dado.find_all_next('div', class_='bar')[85].text
                dadodict_temp['maisgols-segundotempo'] = dado.find_all_next('div', class_='bar')[86].text
                dadodict_temp['maisgols-tempo-igual'] = dado.find_all_next('div', class_='bar')[87].text

                if doistimescont == 0:
                    time1dict = dadodict_temp
                else:
                    time2dict = dadodict_temp
                doistimescont += 1
                break

        gols10 = [time1dict, time2dict]
        return gols10

    def posicoes(self):
        standings = self.site.find('div', class_='teamstandings')
        if standings == None: standings = self.site.find('div', class_='teamsstandings')
        tabelas = standings.find_all('div', class_='halfcontainer')
        posicao = {}
        if len(tabelas) < 2:
            tabelas = standings.find('div', class_='data')
            linhas = tabelas.find_all_next('div', class_='standingrow highlite')
            for time in linhas:
                nomedotime = time.findNext('div', class_='name').text
                colocacao = time.findNext('div', class_='pos').text
                posicao[nomedotime] = colocacao
        else:
            for linha in tabelas:
                nomedotime = linha.findNext('div', class_='name').text
                pos_um = linha.find_next('div', class_='standingrow highlite')
                if pos_um == None: pos_um = linha.find_next('div', class_='standingrow highlite mark')
                colocacao = pos_um.findNext('div', class_='pos').text
                posicao[nomedotime] = colocacao

        return posicao

    def prever(self):
        estatisticas = self.estatisticas10jogos()
        gols = self.gols10jogos()
        posicoes = self.posicoes()
        confrontos = self.confrontos()

        time1stat = estatisticas[0]
        time2stat = estatisticas[1]
        time1gols = gols[0]
        time2gols = gols[1]
        time1pos = int(posicoes[self.time1])
        time2pos = int(posicoes[self.time2])
        if time1pos < time2pos:
            campanha_similar = (time1pos / time2pos) * 100
            campanha_similar = str(round(campanha_similar, 2)) + '%'
        else:
            campanha_similar = (time2pos / time1pos) * 100
            campanha_similar = str(round(campanha_similar, 2)) + '%'
        if float(campanha_similar.strip('%')) < 65:
            if time1pos < time2pos:
                favoritismo = self.time1
            else:
                favoritismo = self.time2
        else:
            favoritismo = '(Neutro)'

        try:
            historico_time = int(confrontos[f'{self.time1}-ganhou']) / int(confrontos['disputas'])
            historico_adversario = int(confrontos[f'{self.time2}-ganhou']) / int(confrontos['disputas'])
            historico_empates = int(confrontos['empates']) / int(confrontos['disputas'])
        except ZeroDivisionError:
            historico_time = 0
            historico_adversario = 0
            historico_empates = 0
        time_fazgol = (int(time1stat['fara-gol'].strip('%')) + int(time2stat['levara-gol'].strip('%'))) / 2
        time_levagol = (int(time1stat['levara-gol'].strip('%')) + int(time2stat['fara-gol'].strip('%'))) / 2
        time_mediagol = (float(time1stat['media-gols-feitos']) + float(time2stat['media-gols-tomados'])) / 2
        adversario_mediagol = (float(time2stat['media-gols-feitos']) + float(time1stat['media-gols-tomados'])) / 2
        time1vencedor = (int(time1gols['time-ganha'].strip('%')) + int(time2gols['time-perde'].strip('%'))) / 2
        time2vencedor = (int(time2gols['time-ganha'].strip('%')) + int(time1gols['time-perde'].strip('%'))) / 2
        empate = (int(time1gols['time-empata'].strip('%')) + int(time2gols['time-empata'].strip('%'))) / 2
        acima1_5geral = (int(time1gols['acima-1.5-geral'].strip('%')) + int(
            time2gols['acima-1.5-geral'].strip('%'))) / 2
        abaixo1_5geral = (int(time1gols['abaixo-1.5-geral'].strip('%')) + int(
            time2gols['abaixo-1.5-geral'].strip('%'))) / 2
        acima2_5geral = (int(time1gols['acima-2.5-geral'].strip('%')) + int(
            time2gols['acima-2.5-geral'].strip('%'))) / 2
        abaixo2_5geral = (int(time1gols['abaixo-2.5-geral'].strip('%')) + int(
            time2gols['abaixo-2.5-geral'].strip('%'))) / 2
        acima3_5geral = (int(time1gols['acima-3.5-geral'].strip('%')) + int(
            time2gols['acima-3.5-geral'].strip('%'))) / 2
        abaixo3_5geral = (int(time1gols['abaixo-3.5-geral'].strip('%')) + int(
            time2gols['abaixo-3.5-geral'].strip('%'))) / 2
        totalgols_01 = (int(time1gols['totalgols-0-1'].strip('%')) + int(time2gols['totalgols-0-1'].strip('%'))) / 2
        totalgols_23 = (int(time1gols['totalgols-2-3'].strip('%')) + int(time2gols['totalgols-2-3'].strip('%'))) / 2
        totalgols_4mais = (int(time1gols['totalgols-4mais'].strip('%')) + int(
            time2gols['totalgols-4mais'].strip('%'))) / 2
        ambos_marcam = (int(time1gols['ambos-marcam'].strip('%')) + int(time2gols['ambos-marcam'].strip('%'))) / 2
        so_um_marca = (int(time1gols['so-um-marca'].strip('%')) + int(time2gols['so-um-marca'].strip('%'))) / 2
        nenhum_marca = (int(time1gols['nenhum-marca'].strip('%')) + int(time2gols['nenhum-marca'].strip('%'))) / 2
        placar_impar = (int(time1gols['placar-impar'].strip('%')) + int(time2gols['placar-impar'].strip('%'))) / 2
        placar_par = (int(time1gols['placar-par'].strip('%')) + int(time2gols['placar-par'].strip('%'))) / 2
        gol_min_0_15 = (int(time1gols['gol-minuto-0-15'].strip('%')) + int(time2gols['gol-minuto-0-15'].strip('%'))) / 2
        gol_min_16_30 = (int(time1gols['gol-minuto-16-30'].strip('%')) + int(
            time2gols['gol-minuto-16-30'].strip('%'))) / 2
        gol_min_31_45 = (int(time1gols['gol-minuto-31-45'].strip('%')) + int(
            time2gols['gol-minuto-31-45'].strip('%'))) / 2
        gol_min_46_60 = (int(time1gols['gol-minuto-46-60'].strip('%')) + int(
            time2gols['gol-minuto-46-60'].strip('%'))) / 2
        gol_min_61_75 = (int(time1gols['gol-minuto-61-75'].strip('%')) + int(
            time2gols['gol-minuto-61-75'].strip('%'))) / 2
        gol_min_76_90 = (int(time1gols['gol-minuto-76-90'].strip('%')) + int(
            time2gols['gol-minuto-76-90'].strip('%'))) / 2
        primeirogol_10 = (int(time1gols['primeirogol-sai-0-10'].strip('%')) + int(
            time2gols['primeirogol-sai-0-10'].strip('%'))) / 2
        primeirogol_20 = (int(time1gols['primeirogol-sai-11-20'].strip('%')) + int(
            time2gols['primeirogol-sai-11-20'].strip('%'))) / 2
        primeirogol_30 = (int(time1gols['primeirogol-sai-21-30'].strip('%')) + int(
            time2gols['primeirogol-sai-21-30'].strip('%'))) / 2
        primeirogol_40 = (int(time1gols['primeirogol-sai-31-40'].strip('%')) + int(
            time2gols['primeirogol-sai-31-40'].strip('%'))) / 2
        primeirogol_50 = (int(time1gols['primeirogol-sai-41-50'].strip('%')) + int(
            time2gols['primeirogol-sai-41-50'].strip('%'))) / 2
        primeirogol_60 = (int(time1gols['primeirogol-sai-51-60'].strip('%')) + int(
            time2gols['primeirogol-sai-51-60'].strip('%'))) / 2
        primeirogol_70 = (int(time1gols['primeirogol-sai-61-70'].strip('%')) + int(
            time2gols['primeirogol-sai-61-70'].strip('%'))) / 2
        primeirogol_80 = (int(time1gols['primeirogol-sai-71-80'].strip('%')) + int(
            time2gols['primeirogol-sai-71-80'].strip('%'))) / 2
        primeirogol_90 = (int(time1gols['primeirogol-sai-81-90'].strip('%')) + int(
            time2gols['primeirogol-sai-81-90'].strip('%'))) / 2
        primeirogol_naosai = (int(time1gols['primeirogol-nao-sai'].strip('%')) + int(
            time2gols['primeirogol-nao-sai'].strip('%'))) / 2
        time_primeirogol = (int(time1gols['time-faz-primeirogol'].strip('%')) + int(
            time2gols['oponente-faz-primeirogol'].strip('%'))) / 2
        oponente_primeirogol = (int(time2gols['time-faz-primeirogol'].strip('%')) + int(
            time1gols['oponente-faz-primeirogol'].strip('%'))) / 2
        ninguem_primeirogol = (int(time1gols['ninguem-faz-primeirogol'].strip('%')) + int(
            time2gols['ninguem-faz-primeirogol'].strip('%'))) / 2
        time_ganhando_15 = (int(time1gols['time-ganhando-aos-15'].strip('%')) + int(
            time2gols['time-perdendo-aos-15'].strip('%'))) / 2
        oponente_ganhando_15 = (int(time2gols['time-perdendo-aos-15'].strip('%')) + int(
            time1gols['time-ganhando-aos-15'].strip('%'))) / 2
        empate_aos15 = (int(time1gols['time-empatando-aos-15'].strip('%')) + int(
            time2gols['time-empatando-aos-15'].strip('%'))) / 2
        time_ganhando_30 = (int(time1gols['time-ganhando-aos-30'].strip('%')) + int(
            time2gols['time-perdendo-aos-30'].strip('%'))) / 2
        oponente_ganhando_30 = (int(time2gols['time-perdendo-aos-30'].strip('%')) + int(
            time1gols['time-ganhando-aos-30'].strip('%'))) / 2
        empate_aos30 = (int(time1gols['time-empatando-aos-30'].strip('%')) + int(
            time2gols['time-empatando-aos-30'].strip('%'))) / 2
        time_ganhando_45 = (int(time1gols['time-ganhando-aos-45'].strip('%')) + int(
            time2gols['time-perdendo-aos-45'].strip('%'))) / 2
        oponente_ganhando_45 = (int(time2gols['time-perdendo-aos-45'].strip('%')) + int(
            time1gols['time-ganhando-aos-45'].strip('%'))) / 2
        empate_aos45 = (int(time1gols['time-empatando-aos-45'].strip('%')) + int(
            time2gols['time-empatando-aos-45'].strip('%'))) / 2
        time_ganhando_60 = (int(time1gols['time-ganhando-aos-60'].strip('%')) + int(
            time2gols['time-perdendo-aos-60'].strip('%'))) / 2
        oponente_ganhando_60 = (int(time2gols['time-perdendo-aos-60'].strip('%')) + int(
            time1gols['time-ganhando-aos-60'].strip('%'))) / 2
        empate_aos60 = (int(time1gols['time-empatando-aos-60'].strip('%')) + int(
            time2gols['time-empatando-aos-60'].strip('%'))) / 2
        time_ganhando_75 = (int(time1gols['time-ganhando-aos-75'].strip('%')) + int(
            time2gols['time-perdendo-aos-75'].strip('%'))) / 2
        oponente_ganhando_75 = (int(time2gols['time-perdendo-aos-75'].strip('%')) + int(
            time1gols['time-ganhando-aos-75'].strip('%'))) / 2
        empate_aos75 = (int(time1gols['time-empatando-aos-75'].strip('%')) + int(
            time2gols['time-empatando-aos-75'].strip('%'))) / 2
        time_ganhando_90 = (int(time1gols['time-ganhando-aos-90'].strip('%')) + int(
            time2gols['time-perdendo-aos-90'].strip('%'))) / 2
        oponente_ganhando_90 = (int(time2gols['time-perdendo-aos-90'].strip('%')) + int(
            time1gols['time-ganhando-aos-90'].strip('%'))) / 2
        empate_aos90 = (int(time1gols['time-empatando-aos-90'].strip('%')) + int(
            time2gols['time-empatando-aos-90'].strip('%'))) / 2
        diferenca_gols_01 = (int(time1gols['diferenca-gols-0-1'].strip('%')) + int(
            time2gols['diferenca-gols-0-1'].strip('%'))) / 2
        diferenca_gols_23 = (int(time1gols['diferenca-gols-2-3'].strip('%')) + int(
            time2gols['diferenca-gols-2-3'].strip('%'))) / 2
        diferenca_gols_4mais = (int(time1gols['diferenca-gols-4mais'].strip('%')) + int(
            time2gols['diferenca-gols-4mais'].strip('%'))) / 2
        maisgols_no1tempo = (int(time1gols['maisgols-primeirotempo'].strip('%')) + int(
            time2gols['maisgols-primeirotempo'].strip('%'))) / 2
        maisgols_no2tempo = (int(time1gols['maisgols-segundotempo'].strip('%')) + int(
            time2gols['maisgols-segundotempo'].strip('%'))) / 2
        maisgols_equilibrado = (int(time1gols['maisgols-tempo-igual'].strip('%')) + int(
            time2gols['maisgols-tempo-igual'].strip('%'))) / 2

        previsao = {
            f'favoritismo': favoritismo,
            f'tradição-{self.time1}': historico_time,
            f'tradição-{self.time2}': historico_adversario,
            f'tradição-empates': historico_empates,
            f'{self.time1}-fara-gols': time_fazgol,
            f'{self.time2}-fara-gols': time_levagol,
            f'{self.time1}-chances-reais': time_mediagol,
            f'{self.time2}-chances-reais': adversario_mediagol,
            f'{self.time1}-ganha': time1vencedor,
            f'{self.time2}-ganha': time2vencedor,
            f'empate': empate,
            'acimade-1.5gols': acima1_5geral,
            'acimade-2.5gols': acima2_5geral,
            'acimade-3.5gols': acima3_5geral,
            'abaixode-1.5gols': abaixo1_5geral,
            'abaixode-2.5gols': abaixo2_5geral,
            'abaixode-3.5gols': abaixo3_5geral,
            'total-gols-0-1': totalgols_01,
            'total-gols-2-3': totalgols_23,
            'total-gols-4mais': totalgols_4mais,
            'ambos-marcam': ambos_marcam,
            'so-um-marca': so_um_marca,
            'nenhum-marca': nenhum_marca,
            'placar-impar': placar_impar,
            'placar-par': placar_par,
            'gol-minuto-0-15': gol_min_0_15,
            'gol-minuto-16-30': gol_min_16_30,
            'gol-minuto-31-45': gol_min_31_45,
            'gol-minuto-46-60': gol_min_46_60,
            'gol-minuto-61-75': gol_min_61_75,
            'gol-minuto-76-90': gol_min_76_90,
            'primeirogol-sai-0-10': primeirogol_10,
            'primeirogol-sai-11-20': primeirogol_20,
            'primeirogol-sai-21-30': primeirogol_30,
            'primeirogol-sai-31-40': primeirogol_40,
            'primeirogol-sai-41-50': primeirogol_50,
            'primeirogol-sai-51-60': primeirogol_60,
            'primeirogol-sai-61-70': primeirogol_70,
            'primeirogol-sai-71-80': primeirogol_80,
            'primeirogol-sai-81-90': primeirogol_90,
            'primeirogol-nao-sai': primeirogol_naosai,
            f'{self.time1}-faz-primeirogol': time_primeirogol,
            f'{self.time2}-faz-primeirogol': oponente_primeirogol,
            f'ninguem-faz-primeirogol': ninguem_primeirogol,
            f'ninguem-faz-primeirogol': ninguem_primeirogol,
            f'{self.time1}-ganhando-aos-15': time_ganhando_15,
            f'{self.time1}-ganhando-aos-30': time_ganhando_30,
            f'{self.time1}-ganhando-aos-45': time_ganhando_45,
            f'{self.time1}-ganhando-aos-60': time_ganhando_60,
            f'{self.time1}-ganhando-aos-75': time_ganhando_75,
            f'{self.time1}-ganhando-aos-90': time_ganhando_90,
            f'{self.time2}-ganhando-aos-15': oponente_ganhando_15,
            f'{self.time2}-ganhando-aos-30': oponente_ganhando_30,
            f'{self.time2}-ganhando-aos-45': oponente_ganhando_45,
            f'{self.time2}-ganhando-aos-60': oponente_ganhando_60,
            f'{self.time2}-ganhando-aos-75': oponente_ganhando_75,
            f'{self.time2}-ganhando-aos-90': oponente_ganhando_90,
            f'empate-aos-15': empate_aos15,
            f'empate-aos-30': empate_aos30,
            f'empate-aos-45': empate_aos45,
            f'empate-aos-60': empate_aos60,
            f'empate-aos-75': empate_aos75,
            f'empate-aos-90': empate_aos90,
            'diferenca-gols-0-1': diferenca_gols_01,
            'diferenca-gols-2-3': diferenca_gols_23,
            'diferenca-gols-4mais': diferenca_gols_4mais,
            'mais-gols-no1tempo': maisgols_no1tempo,
            'mais-gols-no2tempo': maisgols_no2tempo,
            'mais-gols-temposiguais': maisgols_equilibrado,

        }

        return previsao


# app = App('Nautico Recife', 'Sport Recife')
# for k, v in app.prever().items():
#     print(f'{k}: {v}')

hometeam = input('Insira o nome do time 1: ')
awayteam = input('Insira o nome do time 2: ')
app = App(hometeam, awayteam)
previsao = app.prever()
print('')
print('Calculando estatísticas. Aguarde...')
print('')
print('\t== Dados históricos == ')
print(f'\nSe enfrentaram:{app.confrontos()[f"disputas"]} vezes'
      f'\n{hometeam} venceu: {app.confrontos()[f"{hometeam}-ganhou"]} vezes'
      f'\n{awayteam} venceu: {app.confrontos()[f"{awayteam}-ganhou"]} vezes'
      f'\nEmpataram: {app.confrontos()[f"empates"]} vezes')
print('')
print(f'Com base na história, as chances...')
print(f'... do {hometeam} ganhar é de {float(previsao[f"tradição-{hometeam}"])*100:.2f}%')
print(f'... do {awayteam} ganhar é de {float(previsao[f"tradição-{awayteam}"])*100:.2f}%')
print(f'... de dar empate é de {float(previsao[f"tradição-empates"])*100:.2f}%')
print('')
print('\t== Momento atual == ')
print(f'\n> {hometeam}: {app.posicoes()[hometeam]}º lugar.\n> {awayteam}: {app.posicoes()[awayteam]}º lugar.')
print('')
print(f'Com base no momento atual o favoritismo é para: {previsao["favoritismo"]}.')
print('')
print('\t== Previsão de dados == ')
print('')
print(f'{hometeam} fará gols: {previsao[f"{hometeam}-fara-gols"]}% de chance')
print(f'{awayteam} fará gols: {previsao[f"{hometeam}-fara-gols"]}% de chance')
print(f'Média de gols do {hometeam} nesta partida: {float(previsao[f"{hometeam}-chances-reais"]):.2f}')
print(f'Média de gols do {awayteam} nesta partida: {float(previsao[f"{awayteam}-chances-reais"]):.2f}')
print(f'Chance de vitória para {hometeam}: {previsao[f"{hometeam}-ganha"]}%')
print(f'Chance de vitória para {awayteam}: {previsao[f"{awayteam}-ganha"]}%')
print(f'Chance de empate entre {hometeam} e {awayteam}: {previsao[f"empate"]}%')
print(f'Chance de ter mais de 1.5 gols no jogo: {previsao[f"acimade-1.5gols"]}%')
print(f'Chance de ter mais de 2.5 gols no jogo: {previsao[f"acimade-2.5gols"]}%')
print(f'Chance de ter mais de 3.5 gols no jogo: {previsao[f"acimade-3.5gols"]}%')
print(f'Chance de ter menos de 1.5 gols no jogo: {previsao[f"abaixode-1.5gols"]}%')
print(f'Chance de ter menos de 2.5 gols no jogo: {previsao[f"abaixode-2.5gols"]}%')
print(f'Chance de ter menos de 3.5 gols no jogo: {previsao[f"abaixode-3.5gols"]}%')
print(f'Chance de ter menos de 3.5 gols no jogo: {previsao[f"abaixode-3.5gols"]}%')
print(f'A soma do placar será 0 ou 1: {previsao[f"total-gols-0-1"]}%')
print(f'A soma do placar será 2 ou 3: {previsao[f"total-gols-2-3"]}%')
print(f'A soma do placar será 4 ou mais: {previsao[f"total-gols-4mais"]}%')
print(f'Ambos os times marcam: {previsao[f"ambos-marcam"]}%')
print(f'Só um dos times marca: {previsao[f"so-um-marca"]}%')
print(f'Nenhum dos times marca: {previsao[f"nenhum-marca"]}%')
print(f'O placar será ímpar: {previsao[f"placar-impar"]}%')
print(f'O placar será par: {previsao[f"placar-par"]}%')
print(f'Chance sair gol entre os minutos 0 a 15: {previsao[f"gol-minuto-0-15"]}%')
print(f'Chance sair gol entre os minutos 16 a 30: {previsao[f"gol-minuto-16-30"]}%')
print(f'Chance sair gol entre os minutos 31 a 45: {previsao[f"gol-minuto-31-45"]}%')
print(f'Chance sair gol entre os minutos 46 a 60: {previsao[f"gol-minuto-46-60"]}%')
print(f'Chance sair gol entre os minutos 61 a 75: {previsao[f"gol-minuto-61-75"]}%')
print(f'Chance sair gol entre os minutos 76 a 90: {previsao[f"gol-minuto-76-90"]}%')
print(f'O primeiro gol da partida será no minuto 0-10: {previsao[f"primeirogol-sai-0-10"]}%')
print(f'O primeiro gol da partida será no minuto 0-20: {previsao[f"primeirogol-sai-11-20"]}%')
print(f'O primeiro gol da partida será no minuto 0-30: {previsao[f"primeirogol-sai-21-30"]}%')
print(f'O primeiro gol da partida será no minuto 0-40: {previsao[f"primeirogol-sai-31-40"]}%')
print(f'O primeiro gol da partida será no minuto 0-50: {previsao[f"primeirogol-sai-41-50"]}%')
print(f'O primeiro gol da partida será no minuto 0-60: {previsao[f"primeirogol-sai-51-60"]}%')
print(f'O primeiro gol da partida será no minuto 0-70: {previsao[f"primeirogol-sai-61-70"]}%')
print(f'O primeiro gol da partida será no minuto 0-80: {previsao[f"primeirogol-sai-71-80"]}%')
print(f'O primeiro gol da partida será no minuto 0-90: {previsao[f"primeirogol-sai-81-90"]}%')
print(f'O primeiro gol da partida não sai: {previsao[f"primeirogol-nao-sai"]}%')
print(f'{hometeam} fará o primeiro gol: {previsao[f"{hometeam}-faz-primeirogol"]}%')
print(f'{awayteam} fará o primeiro gol: {previsao[f"{awayteam}-faz-primeirogol"]}%')
print(f'Ninguem fará o primeiro gol: {previsao[f"ninguem-faz-primeirogol"]}%')
print(f'{hometeam} estará ganhando entre os minutos 0 a 15: {previsao[f"{hometeam}-ganhando-aos-15"]}%')
print(f'{hometeam} estará ganhando entre os minutos 16 a 30: {previsao[f"{hometeam}-ganhando-aos-30"]}%')
print(f'{hometeam} estará ganhando entre os minutos 31 a 45: {previsao[f"{hometeam}-ganhando-aos-45"]}%')
print(f'{hometeam} estará ganhando entre os minutos 46 a 60: {previsao[f"{hometeam}-ganhando-aos-60"]}%')
print(f'{hometeam} estará ganhando entre os minutos 61 a 75: {previsao[f"{hometeam}-ganhando-aos-75"]}%')
print(f'{hometeam} estará ganhando entre os minutos 76 a 90: {previsao[f"{hometeam}-ganhando-aos-90"]}%')
print(f'{awayteam} estará ganhando entre os minutos 0 a 15: {previsao[f"{awayteam}-ganhando-aos-15"]}%')
print(f'{awayteam} estará ganhando entre os minutos 16 a 30: {previsao[f"{awayteam}-ganhando-aos-30"]}%')
print(f'{awayteam} estará ganhando entre os minutos 31 a 45: {previsao[f"{awayteam}-ganhando-aos-45"]}%')
print(f'{awayteam} estará ganhando entre os minutos 46 a 60: {previsao[f"{awayteam}-ganhando-aos-60"]}%')
print(f'{awayteam} estará ganhando entre os minutos 61 a 75: {previsao[f"{awayteam}-ganhando-aos-75"]}%')
print(f'{awayteam} estará ganhando entre os minutos 76 a 90: {previsao[f"{awayteam}-ganhando-aos-90"]}%')
print(f'A partida estará empate entre os minutos 0 a 15: {previsao[f"empate-aos-15"]}%')
print(f'A partida estará empate entre os minutos 16 a 30: {previsao[f"empate-aos-30"]}%')
print(f'A partida estará empate entre os minutos 31 a 45: {previsao[f"empate-aos-45"]}%')
print(f'A partida estará empate entre os minutos 46 a 60: {previsao[f"empate-aos-60"]}%')
print(f'A partida estará empate entre os minutos 61 a 75: {previsao[f"empate-aos-75"]}%')
print(f'A partida estará empate entre os minutos 76 a 90: {previsao[f"empate-aos-90"]}%')
print(f'O vencedor e o perdedor terão uma diferença de gols entre 0-1: {previsao[f"diferenca-gols-0-1"]}%')
print(f'O vencedor e o perdedor terão uma diferença de gols entre 2-3: {previsao[f"diferenca-gols-2-3"]}%')
print(f'O vencedor e o perdedor terão uma diferença de gols maior que 4: {previsao[f"diferenca-gols-4mais"]}%')
print(f'O primeiro tempo será o tempo com mais gols: {previsao[f"mais-gols-no1tempo"]}%')
print(f'O segundo tempo será o tempo com mais gols: {previsao[f"mais-gols-no2tempo"]}%')
print(f'Os dois tempos terão o mesmo número de gols: {previsao[f"mais-gols-temposiguais"]}%')
print('')
os.system('pause')