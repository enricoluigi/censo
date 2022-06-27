from base64 import urlsafe_b64encode
import urllib.request
import streamlit as st
import json
import pandas as pd
import zlib
import pydeck as pdk

def load_data(setor):
    #pega os dados do censo
    fromCenso = urllib.request.urlopen("https://servicodados.ibge.gov.br/cnefe.ashx?resp=enderecos&setor="+str(setor))

    #le os dados do censo
    dados = fromCenso.read()
    #decodifica de byte pra utf8 string e remove o ;
    try:
        dados = zlib.decompress(dados, 16 + zlib.MAX_WBITS)
    except:
        print ("Dados não comprimidos")
    #remove ; do final da variavel recebida
    dados = dados.decode('UTF-8').replace(";","")
    #converte pra json
    dados = json.loads(dados)
    #retorna dados
    return dados

def percorre_dados(setor):
	try:
		setor = load_data(setor)
		placemarks = ""
		for x in setor:
			placemarks += gera_ponto(setor[x], x)   
		return placemarks
	except:
		return False

def gera_ponto(domicilio, x):
    placemark = "<Placemark>\n\t<name>"+ x +'</name>\n\t<Snippet maxLines="0"></Snippet>\n'
    placemark += "\t<description>"+ desc_cabecalho(x) + desc_dados(domicilio) +"</description>\n\t<LookAt>"
    placemark += "\t\t<longitude>"+converte_ponto(domicilio["6"])+"</longitude>\n"
    placemark += "\t\t<latitude>"+converte_ponto(domicilio["5"])+"</latitude>\n"
    placemark += "\t\t<altitude>0</altitude>\n\t\t<heading>0</heading>\n\t\t<tilt>0</tilt>\n\t\t<range>1000</range>\n\t\t<altitudeMode>clampToGround</altitudeMode>\n\t</LookAt>\n"
    placemark += "\t<styleUrl>#msn_ltblu-diamond</styleUrl>\n"
    placemark += "\t<Point>\n\t\t<coordinates>"+converte_ponto(domicilio["6"])+","+converte_ponto(domicilio["5"])+"</coordinates>\n\t</Point>\n</Placemark>"
    return(placemark)

def tipo_dom(tipo):
	dict={
		1: "Ocupado",
		2: "Urbano",
		3: "Estabelecimento Agropecuario",
		4: "4",
		5: "5",
		6: "EOF",
	}
	return dict.get(tipo, "Tipo desconhecido")

def converte_ponto(ponto):
	try:
		ponto = ponto.split()
		graus = ponto[0]
		minutos = ponto[1]
		segundos = ponto[2]
		hemisferio = ponto[3]
		ponto = int(graus)+float(minutos)/60+float(segundos)/3600
		if hemisferio == "O" or hemisferio == "S":
			#ponto = ponto * -1
			ponto = "-"+str(ponto)
			#ponto = float(ponto)
			return ponto
	except:
		return ""

def gera_cabecalho(setor):
    cab = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
	<name>"""+ str(setor) +"""</name>
	<open>"""+ str(setor) +"""</open>
	<Snippet maxLines="0"></Snippet>
	<description><![CDATA[<style type='text/css'>*{font-family:Verdana,Arial,Helvetica,Sans-Serif;}</style><table style="width: 300px;"><tr><td style="vertical-align: top;">Fonte</td><td style="width: 100%;">CENSO 2010</td></tr><tr><td>DateTime</td><td>2022-01-14 01:43:22 UTC <br/></td></tr><tr><td colspan="2" style="vertical-align: top;"><br/>Criado por Enrico Mendonca</td></tr></table>]]></description>
	<Style>
		<IconStyle>
			<Icon>
			</Icon>
		</IconStyle>
		<BalloonStyle>
			<text>$[description]</text>
			<textColor>ff000000</textColor>
			<displayMode>default</displayMode>
		</BalloonStyle>
	</Style>
	<Style id="Normal0_0">
		<IconStyle>
			<Icon>
				<href>http://www.earthpoint.us/Dots/GoogleEarth/paddle/ltblu-diamond.png</href>
			</Icon>
			<hotSpot x="32" y="1" xunits="pixels" yunits="pixels"/>
		</IconStyle>
		<BalloonStyle>
			<text>$[description]</text>
		</BalloonStyle>
		<LineStyle>
			<width>2</width>
		</LineStyle>
	</Style>
	<Style id="Highlight0_0">
		<IconStyle>
			<scale>1.1</scale>
			<Icon>
				<href>http://www.earthpoint.us/Dots/GoogleEarth/paddle/ltblu-diamond.png</href>
			</Icon>
			<hotSpot x="32" y="1" xunits="pixels" yunits="pixels"/>
		</IconStyle>
		<BalloonStyle>
			<text>$[description]</text>
		</BalloonStyle>
		<LineStyle>
			<width>3</width>
		</LineStyle>
	</Style>
	<Style id="HighlightErrorReport">
		<IconStyle>
			<color>ff0000ff</color>
			<scale>2.3</scale>
			<Icon>
				<href>http://www.earthpoint.us/Dots/GoogleEarth/shapes/forbidden.png</href>
			</Icon>
		</IconStyle>
		<LabelStyle>
			<color>ff0000ff</color>
			<scale>2</scale>
		</LabelStyle>
		<BalloonStyle>
			<text>$[description]</text>
		</BalloonStyle>
	</Style>
	<Style id="NormalErrorReport">
		<IconStyle>
			<color>ff0000ff</color>
			<scale>2</scale>
			<Icon>
				<href>http://www.earthpoint.us/Dots/GoogleEarth/shapes/forbidden.png</href>
			</Icon>
		</IconStyle>
		<LabelStyle>
			<color>ff0000ff</color>
			<scale>1.5</scale>
		</LabelStyle>
		<BalloonStyle>
			<text>$[description]</text>
		</BalloonStyle>
	</Style>
	<StyleMap id="msn_ltblu-diamond">
		<Pair>
			<key>normal</key>
			<styleUrl>#sn_ltblu-diamond</styleUrl>
		</Pair>
		<Pair>
			<key>highlight</key>
			<styleUrl>#sh_ltblu-diamond</styleUrl>
		</Pair>
	</StyleMap>
	<Style id="sn_ltblu-diamond">
		<IconStyle>
			<Icon>
				<href>http://www.earthpoint.us/Dots/GoogleEarth/paddle/ltblu-diamond.png</href>
			</Icon>
			<hotSpot x="32" y="1" xunits="pixels" yunits="pixels"/>
		</IconStyle>
		<BalloonStyle>
		</BalloonStyle>
		<LineStyle>
			<width>2</width>
		</LineStyle>
	</Style>
	<Style id="sh_ltblu-diamond">
		<IconStyle>
			<scale>1.1</scale>
			<Icon>
				<href>http://www.earthpoint.us/Dots/GoogleEarth/paddle/ltblu-diamond.png</href>
			</Icon>
			<hotSpot x="32" y="1" xunits="pixels" yunits="pixels"/>
		</IconStyle>
		<BalloonStyle>
		</BalloonStyle>
		<LineStyle>
			<width>3</width>
		</LineStyle>
	</Style>
	<StyleMap id="0_0">
		<Pair>
			<key>normal</key>
			<styleUrl>#Normal0_0</styleUrl>
		</Pair>
		<Pair>
			<key>highlight</key>
			<styleUrl>#Highlight0_0</styleUrl>
		</Pair>
	</StyleMap>
	<StyleMap id="ErrorReport">
		<Pair>
			<key>normal</key>
			<styleUrl>#NormalErrorReport</styleUrl>
		</Pair>
		<Pair>
			<key>highlight</key>
			<styleUrl>#HighlightErrorReport</styleUrl>
		</Pair>
	</StyleMap>
	<Folder>
		<name>"""+ str(setor) +"""</name>
		<open>1</open>"""
    return cab

def desc_cabecalho(x):
    return """<![CDATA[
        <style type='text/css'>*{font-family:Verdana,Arial,Helvetica,Sans-Serif;box-sizing:border-box;padding:0px;margin:0px}table{border-collapse:collapse;border-spacing:0px;margin:2px}.trb{background-color:#ddffdd}.ch{vertical-align:top;padding-left:10px;white-space:nowrap}.cv{vertical-align:top;padding-left:6px;padding-right:10px;white-space:nowrap}.cw{vertical-align:top;padding-left:6px;padding-right:10px;width:600px}</style>
        <table>
            <tr>
                <td colspan='2' style='vertical-align: top; padding-left: 10px; padding-right: 10px; white-space: nowrap;'>
                    <b>"""+ x +"""</b>
                </td>
            </tr>
            <tr>
            <td colspan='2' style='vertical-align: top; padding-left: 10px; padding-right: 10px; max-width: 400px; white-space: nowrap;'>&nbsp;</td>
            </tr>"""

def desc_dados(domicilio):
    return """<tr class='trb'>
            <td class='ch'> <b>Logradouro</b> </td>
            <td class='cv'>"""+ domicilio["2"] +"""</td>
            </tr>
            <tr>
            <td class='ch'><b>N&#250;mero no logradouro</b></td>
            <td class='cv'>"""+ domicilio["3"]+"""</td>
            </tr>
        <tr class='trb'>
            <td class='ch'><b>Complemento</b></td>
            <td class='cv'>"""+ domicilio["4"]+"""</td>
            </tr>
        <tr>
            <td class='ch'><b>Localidade</b></td>
            <td class='cv'>"""+ domicilio["7"]+"""</td>
            </tr>
        <tr class='trb'>
            <td class='ch'><b>Ponto de refer&#234;ncia</b></td>
            <td class='cv'>"""+ domicilio["8"]+"""</td>
            </tr>
        <tr>
            <td class='ch'><b>Esp&#233;cie de endere&#231;o</b></td>
            <td class='cv'>"""+ domicilio["9"]+"""</td>
            </tr>
        <tr class='trb'>
            <td class='ch'><b>Tipo de estabelecimento</b></td>
            <td class='cv'>"""+ tipo_dom(domicilio["10"]) +"""</td>
            </tr>
        <tr>
            <td class='ch'><b>Indicador de endere&#231;o</b></td>
            <td class='cv'>"""+ domicilio["11"]+"""</td>
            </tr>
        <tr class='trb'>
            <td class='ch'><b>Identifica&#231;&#227;o domic&#237;lio coletivo</b></td>
            <td class='cv'>"""+ domicilio["12"]+"""</td>
            </tr>
        <tr>
            <td class='ch'><b>N&#250;mero da quadra</b></td>
            <td class='cv'>"""+ domicilio["13"]+"""</td>
            </tr>
        <tr class='trb'>
            <td class='ch'><b>N&#250;mero da face</b></td>
            <td class='cv'>"""+ domicilio["14"]+"""</td>
            </tr>
        </table>]]>"""

def roda(setor):
	kml = gera_cabecalho(setor)
	kml += str(percorre_dados(setor))+"\n</Folder>/n</Document>\n</kml>"
	return kml

def cria_dataframe(dados):
	df = pd.DataFrame(dados)
	df = df.T
	df.columns = ['Tipo', 'Logradouro', 'Num', 'Comp', 'Lat', 'Long','Localidade','P. Ref','Esp. End','Tipo Est.','Ind.','Ident','Q','F', 'CEP']
	for index, row in df.iterrows():
		if row["Lat"] == "" or row["Long"] == "":
			row["Lat"] = float("-20.726053")
			row["Long"] = float("-42.886428")
		else:
			row["Lat"] = float(converte_ponto(row["Lat"]))
			row["Long"] = float(converte_ponto(row["Long"]))
	return df

def copy_df(df):
	df = df.filter(["Lat", "Long"])
	df.columns = ["lat", "lon"]
	return df

st.title('Baixar KML')
setor = st.text_input("Digite o número do setor", value=317130305000071, format="%d", step=1)
if st.button("Gerar KML no sistema"):
	with st.spinner('Processando, por favor aguarde...'):
		dados = load_data(setor)
		df = cria_dataframe(dados)
		map = copy_df(df)
		dados = roda(int(setor))
		#print (len(dados))
	if len(dados) > 10000:
		st.success('Arquivos gerados com sucesso!')
		st.download_button(label="Download do KML", data=dados, file_name="setor.kml", mime='text/kml')
		st.map(map)
		st.dataframe(df)
	else:
		st.error('Número de setor inválido!')




