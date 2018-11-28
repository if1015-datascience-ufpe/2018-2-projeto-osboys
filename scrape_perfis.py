from bs4 import BeautifulSoup as bs
import requests as rq
import re
import pandas as pd

urlparts = ['http://www2.recife.pe.gov.br/servico/', '?op=NzQ0MQ==']

bairros = { \
    'rpa1': ['bairro-do-recife',
        'boa-vista',
        'cabanga',
        'coelhos',
        'ilha-do-leite',
        'ilha-joana-bezerra',
        'paissandu',
        'santo-amaro',
        'santo-antonio',
        'sao-jose',
        'soledade'],

    'rpa2': ['agua-fria',
        'alto-santa-terezinha',
        'arruda',
        'beberibe',
        'bomba-do-hemeterio',
        'cajueiro',
        'campina-do-barreto',
        'campo-grande',
        'dois-unidos',
        'encruzilhada',
        'fundao',
        'hipodromo',
        'linha-do-tiro',
        'peixinhos',
        'ponto-de-parada',
        'porto-da-madeira',
        'rosarinho',
        'torreao'],

    'rpa3': [#'aflitos',
        'alto-do-mandu',
        #'alto-jose-bonifacio',
        #'alto-jose-do-pinho',
        'apipucos',
        'brejo-da-guabiraba',
        #'brejo-do-beberibe',
        'casa-amarela',
        'casa-forte',
        'corrego-do-jenipapo',
        'derby',
        #'dois-irmaos',
        #'espinheiro',
        #'gracas',
        'guabiraba',
        'jaqueira',
        'macaxeira',
        'mangabeira',
        'monteiro',
        'morro-da-conceicao',
        'nova-descoberta',
        'parnamirim',
        #'passarinho',
        'pau-ferro',
        'poco-da-panela',
        'santana',	
        'sitio-dos-pintos',
        'tamarineira',
        'vasco-da-gama'],

    'rpa4': ['caxanga',
        'cidade-universitaria',
        'cordeiro',
        #'engenho-do-meio',
        'ilha-do-retiro',
        'iputinga',
        'madalena',
        'prado',
        'torre',
        'torroes',
        'varzea',
        'zumbi'],

    'rpa5': ['afogados',
        'areias',
        'barro',
        'bongi',
        'cacote',
        'coqueiral',
        #'curado',
        'estancia',
        'jardim-sao-paulo',
        'jiquia',
        'mangueira',
        'mustardinha',
        'san-martin',
        'sancho',
        'tejipio',
        'toto'],

    'rpa6': ['boa-viagem',
        #'brasilia-teimosa',	
        'cohab',
        'ibura',
        'imbiribeira',
        'ipsep',
        'jordao',
        'pina']
}

urls = { key : ( bairro.join(urlparts) for bairro in bairros[key] ) for key in bairros }

bspages = { key : ( bs(rq.get(url).text, 'html.parser') for url in urls[key] ) for key in urls }

first_attrs = { 'class': 'content-text text-servico' }

def get_nome_bairro(bspage):
    container = bspage.find('div', attrs = first_attrs)
    nome_bairro = container.find('h2').text

    return nome_bairro

def get_dist_marco_zero(bspage):
    container = bspage.find('div', attrs = first_attrs)
    text = container.find('p').text
    dist_texts = re.split('[^0-9.,]+', text)
    dist_text = dist_texts[-5] if len(dist_texts) > 8 else dist_texts[-4]
    dist_text = re.sub(',', '.', dist_text)
    dist = float(dist_text)

    return dist

def get_area_hectare(bspage):
    container = bspage.find('div', attrs = first_attrs)
    text = container.find('p').text
    area_texts = re.split('[^0-9]+', text)
    area_text = area_texts[-4] if len(area_texts) > 11 else area_texts[-3]
    area = int(area_text)

    return area

def get_populacao(bspage):
    container = bspage.find('div', attrs = first_attrs)
    text = container.find('p').text
    pop_texts = re.split('[^0-9.,]+', text)
    pop_text = pop_texts[-1] if pop_texts[-1] != '' else pop_texts[-2]
    pop_text = re.sub('\.', '', pop_text)
    populacao = int(pop_text)

    return populacao

def get_pop_masc(bspage):
    container = bspage.find('tbody')
    pop_masc_text = container.find_all('td')[4].text
    pop_masc_text = re.sub('\.', '', pop_masc_text)
    pop_masc = int(pop_masc_text)

    return pop_masc

def get_pop_fem(bspage):
    container = bspage.find('tbody')
    pop_fem_text = container.find_all('td')[7].text
    pop_fem_text = re.sub('\.', '', pop_fem_text)
    pop_fem = int(pop_fem_text)

    return pop_fem

def get_pop_faixa_etaria(bspage):
    container = bspage.find_all('tbody')[1]
    faixas = ['pop_0_4', 'pop_5_14', 'pop_15_17', 'pop_18_24', 'pop_25_59', 'pop_60_']
    faixa_tds = container.find_all('td')[4:23:3]
    faixa_qtd_txts = [td.text for td in faixa_tds]
    faixa_qtd_txts = [re.sub('\.', '', txt) for txt in faixa_qtd_txts]
    faixa_qtds = [int(txt) for txt in faixa_qtd_txts]
    pop_faixa = dict(zip(faixas, faixa_qtds))

    return pop_faixa

def get_pop_porc_raca(bspage):
    container = bspage.find_all('tbody')[2]
    racas = ['pop_porc_branca', 'pop_porc_preta', 'pop_porc_parda', 'pop_porc_amarela', 'pop_porc_indigena']
    racas_tds = container.find_all('td')[3:14:2]
    racas_porcs_txts = [td.text for td in racas_tds]
    racas_porcs_txts = [re.sub('\.', '', racas_porc_txt) for racas_porc_txt in racas_porcs_txts]
    racas_porcs = [float(re.sub(',', '.', txt)) for txt in racas_porcs_txts]
    racas_porcs = dict(zip(racas, racas_porcs))

    return racas_porcs

def get_alfab_dez_mais(bspage):
    container = bspage.find('div', attrs = first_attrs)
    alfab_ps = [p.text for p in container.find_all('p')]
    alfab_p_text = alfab_ps[1] if alfab_ps[1] != '\xa0' else alfab_ps[2]
    alfab_text = re.split('[^0-9.,]+', alfab_p_text)[3]
    alfab_text = re.sub(',', '.', alfab_text)
    alfab_dez_mais = float(alfab_text)

    return alfab_dez_mais

def get_taxa_m_cresc(bspage):
    container = bspage.find('div', attrs = first_attrs)
    ps = container.find_all('p')
    p_texts = [p.text for p in ps if p.text != '\xa0']
    p_texts = p_texts[1:]
    p_text = ''.join(p_texts)
    info_texts = re.split('[^0-9.,-]+', p_text)
    info_texts = [text for text in info_texts if text != '.' and text != ',' and text != '-' and text != '']
    taxa_text = info_texts[5]
    taxa_text = re.sub(',', '.', taxa_text)
    taxa_m_cresc = float(taxa_text)

    return taxa_m_cresc 

def get_dens_dem(bspage):
    container = bspage.find('div', attrs = first_attrs)
    ps = container.find_all('p')
    p_texts = [p.text for p in ps if p.text != '\xa0']
    p_texts = p_texts[1:]
    p_text = ''.join(p_texts)
    info_texts = re.split('[^0-9.,]+', p_text)
    info_texts = [text for text in info_texts if text != ',' and text != '.' and text != '']
    dens_text = info_texts[6]
    dens_text = re.sub(',', '.', dens_text)
    dens_dem = float(dens_text)

    return dens_dem

def get_num_domic(bspage):
    container = bspage.find('div', attrs = first_attrs)
    ps = container.find_all('p')
    p_texts = [p.text for p in ps if p.text != '\xa0']
    p_texts = p_texts[1:]
    p_text = ''.join(p_texts)
    info_texts = re.split('[^0-9., ]+', p_text)
    info_texts = [text for text in info_texts if text != ',' and text != '.' and text != '' and text != ' ']
    num_text = info_texts[8]
    num_text = re.sub('\.', '', num_text)
    num_text = re.sub(' ', '', num_text)
    num_domic = int(num_text)

    return num_domic

def get_morador_domic(bspage):
    container = bspage.find('div', attrs = first_attrs)
    ul = container.find('ul')
    if ul:
        ul = ul.find('li')
        md_text = re.match('.+:[^0-9]*([0-9,]+)[^0-9]*', ul.text).group(1)
        md_text = re.sub(',', '.', md_text)
        morador_domic = float(md_text)
    else:
        spans = container.find_all('span')
        span_texts = [span.text for span in spans if span.text != '\xa0' and span.text != '']
        span_texts = span_texts[-5:]
        span_text = ''.join(span_texts)
        info_texts = re.split('[^0-9.,]+', span_text)
        info_texts = [text for text in info_texts if text != ',' and text != '.' and text != '']
        md_text = info_texts[0]
        md_text = re.sub(',', '.', md_text)
        morador_domic = float(md_text)

    return morador_domic

def get_prop_resp_fem(bspage):
    container = bspage.find('div', attrs = first_attrs)
    ul = container.find('ul')
    if ul:
        ul = ul.find_all('li')[1]
        resp_text = re.match('.+:[^0-9]*([0-9,]+)[^0-9]*', ul.text).group(1)
        resp_text = re.sub(',', '.', resp_text)
        prop_resp_fem = float(resp_text)
    else:
        spans = container.find_all('span')
        span_texts = [span.text for span in spans if span.text != '\xa0' and span.text != '']
        span_texts = span_texts[-5:]
        span_text = ''.join(span_texts)
        info_texts = re.split('[^0-9.,]+', span_text)
        info_texts = [text for text in info_texts if text != ',' and text != '.' and text != '']
        prop_text = info_texts[1]
        prop_text = re.sub(',', '.', prop_text)
        prop_resp_fem = float(prop_text)

    return prop_resp_fem

def get_rend_medio(bspage):
    container = bspage.find('div', attrs = first_attrs)
    ul = container.find('ul')
    if ul:
        ul = ul.find_all('li')[2]
        rend_text = re.match('.+R\$\s*([0-9.,]+)[^0-9]*', ul.text).group(1)
        rend_text = re.sub('\.', '', rend_text)
        rend_text = re.sub(',', '.', rend_text)
        rend_medio = float(rend_text)
    else:
        spans = container.find_all('span')
        span_texts = [span.text for span in spans if span.text != '\xa0' and span.text != '']
        span_texts = span_texts[-5:]
        span_text = ''.join(span_texts)
        info_texts = re.split('[^0-9.,]+', span_text)
        info_texts = [text for text in info_texts if text != ',' and text != '.' and text != '']
        rend_text = info_texts[2]
        rend_text = re.sub('\.', '', rend_text)
        rend_text = re.sub(',', '.', rend_text)
        rend_medio = float(rend_text)

    return rend_medio

def get_data_dict(bspage):
    data_fields = ['nome_bairro',
                    'dist_marco_zero',
                    'area_hectare',
                    'populacao',
                    'pop_masc',
                    'pop_fem',
                    'alfab_dez_mais',
                    'taxa_m_cresc',
                    'dens_dem',
                    'num_domic',
                    'morador_por_domic',
                    'prop_resp_fem',
                    'rend_medio']

    data_funcs = [get_nome_bairro,
                    get_dist_marco_zero,
                    get_area_hectare,
                    get_populacao,
                    get_pop_masc,
                    get_pop_fem,
                    get_alfab_dez_mais,
                    get_taxa_m_cresc,
                    get_dens_dem,
                    get_num_domic,
                    get_morador_domic,
                    get_prop_resp_fem,
                    get_rend_medio]

    data = [func(bspage) for func in data_funcs]

    pop_faixa_etaria = get_pop_faixa_etaria(bspage)
    pop_porc_raca = get_pop_porc_raca(bspage)

    data_dict = dict(list(zip(data_fields, data)) + list(pop_faixa_etaria.items()) + list(pop_porc_raca.items()))

    return data_dict


dfs = [pd.DataFrame([get_data_dict(bspage) for bspage in bspages[key]]) for key in bairros]

for n, df in enumerate(dfs):
    df['rpa'] = n + 1

left_out_df = pd.DataFrame({
    #Bairros faltando:
    #Aflitos
    #Alto José Bonifácio
    #Alto José do Pinho
    #Brejo do Beberibe
    #Dois Irmãos
    #Espinheiro
    #Graças
    #Passarinho
    #Engenho do Meio
    #Curado
    #Brasília Teimosa
    'nome_bairro': ['Aflitos',
                        'Alto José Bonifácio',
                        'Alto José do Pinho',
                        'Brejo do Beberibe',
                        'Dois Irmãos',
                        'Espinheiro',
                        'Graças',
                        'Passarinho',
                        'Engenho do Meio',
                        'Curado',
                        'Brasília Teimosa'],

    'dist_marco_zero': [3.72, 7.27, 6.05, 9.34, 10.4, 3.09, 3.71, 10.97, 8, 9.68, 2.33],

    'area_hectare': [31, 57, 41, 64, 585, 73, 144, 406, 87, 798, 61],

    'populacao': [5773, 12462, 12334, 8292, 2566, 10438, 20538, 20305, 10211, 16418, 18334],

    'pop_masc': [2541, 5863, 5617, 3938, 1251, 4465, 8842, 9954, 4609, 7753, 8571],

    'pop_fem': [3232, 6599, 6717, 4354, 1315, 5973, 11696, 10371, 5602, 8665, 9773],

    'alfab_dez_mais': [99.2, 91, 91.7, 90.2, 93.1, 98.1, 99.2, 87.1, 96.1, 90.3, 91.8],

    'taxa_m_cresc': [2.8, .07, -0.08, 3.62, -1.7, 1.6, 1.6, 2.79, -0.34, 1.99, -0.44],

    'dens_dem': [187.83, 219.26, 298.4, 129.86, 4.39, 142.56, 143.08, 49.98, 117.54, 20.56, 302.81],

    'num_domic': [1937, 3570, 3510, 2459, 737, 3602, 7015, 5792, 3053, 4900, 5464],

    'morador_por_domic': [3, 3.5, 3.5, 3.4, 3.5, 2.9, 2.9, 3.5, 3.3, 3.3, 3.4],

    'prop_resp_fem': [51.24, 42.64, 53.72, 48.21, 44.1, 49.28, 49.18, 41.31, 46.09, 40.08, 49.57],

    'rend_medio': [1028.96, 908.76, 1101.22, 1058.37, 1936.1, 7299.96, 9484.01, 824.02, 2594.45, 1216.36, 1220.81],

    'pop_0_4': [240, 911, 785, 655, 177, 469, 794, 1733, 486, 1258, 1285],

    'pop_5_14': [546, 2085, 2027, 1514, 427, 892, 1904, 3940, 1204, 2757, 2854],

    'pop_15_17': [224, 696, 644, 450, 151, 327, 838, 1242, 464, 830, 907],

    'pop_18_24': [695, 1596, 1507, 1094, 372, 1285, 2608, 2731, 1170, 1928, 2156],

    'pop_25_59': [3030, 5996, 6022, 3978, 1241, 5415, 10648, 9354, 2242, 8319, 9084],

    'pop_60_': [1038, 1188, 1349, 601, 198, 2050, 3746, 1305, 1645, 1326,   2048],

    'pop_porc_branca': [76.11, 25.49, 29.02, 31.5, 35.39, 70.56, 76.68, 25.24, 43.49, 33.91, 33.05],

    'pop_porc_preta': [1.87, 4.81, 15.65, 9.85, 7.91, 3.43, 2.4, 7.75, 7.56, 8.02, 8.93],

    'pop_porc_parda': [21.13, 58.9, 53.57, 57.18, 55.53, 25.03, 19.85, 66.65, 47.25, 56.94, 56.62],

    'pop_porc_amarela': [.87, .67, 1.39, 1.45, 1.09, .8, .96, .32, 1.24, .9, .99],

    'pop_porc_indigena': [.02, .13, .37, .02, 1.09, .18, .1, .04, .39, .23, .31],

    'rpa': [3, 3, 3, 3, 3, 3, 3, 3, 4, 5, 6]
})

dfs.append(left_out_df)

final_df = pd.concat(dfs, ignore_index = True)
pd.DataFrame.to_csv(final_df, 'dados_preliminares.csv')
