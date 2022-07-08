import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import plotly.express as px
import datetime as dt 
from datetime import date, timedelta





col1, col2, col3 = st.columns([2,2,1])

with col2:
    st.image('take2.png', width=100,)
st.markdown('---')
st.markdown("<h2 style='text-align: center; color: black;'>Modo Manual Estrategia</h2>", unsafe_allow_html=True)
st.markdown('---')
st.markdown("<h5 style='text-align: center; color: black;'>Filtro para Teste</h5>", unsafe_allow_html=True)

with st.form(key= 'form1'):
    col1, col2 = st.columns(2)
    with col1:
        data_incio = st.date_input('Data de incio do teste') 
    with col2:
        data_Fim = st.date_input('Data de Fim do teste')    
    acoes = [   'RRRP3.SA'  ,
                'ALPA4.SA'	,
                'ABEV3.SA'	,
                'AMER3.SA'	,
                'ASAI3.SA'	,
                'AZUL4.SA'	,
                'B3SA3.SA'	,
                'BPAN4.SA'	,
                'BBSE3.SA'	,
                'BRML3.SA'	,
                'BBDC3.SA'	,
                'BBDC4.SA'	,
                'BRAP4.SA'	,
                'BBAS3.SA'	,
                'BRKM5.SA'	,
                'BRFS3.SA'	,
                'BPAC11.SA'	,
                'CRFB3.SA'	,
                'CCRO3.SA'	,
                'CMIG4.SA'	,
                'CIEL3.SA'	,
                'COGN3.SA'	,
                'CPLE6.SA'	,
                'CSAN3.SA'	,
                'CPFE3.SA'	,
                'CMIN3.SA'	,
                'CVCB3.SA'	,
                'CYRE3.SA'	,
                'DXCO3.SA'	,
                'ECOR3.SA'	,
                'ELET3.SA'	,
                'ELET6.SA'	,
                'EMBR3.SA'	,
                'ENBR3.SA'	,
                'ENGI11.SA'	,
                'ENEV3.SA'	,
                'EGIE3.SA'	,
                'EQTL3.SA'	,
                'EZTC3.SA'	,
                'FLRY3.SA'	,
                'GGBR4.SA'	,
                'GOAU4.SA'	,
                'GOLL4.SA'	,
                'NTCO3.SA'	,
                'SOMA3.SA'	,
                'HAPV3.SA'	,
                'HYPE3.SA'	,
                'IGTI11.SA'	,
                'IRBR3.SA'	,
                'ITSA4.SA'	,
                'ITUB4.SA'	,
                'JBSS3.SA'	,
                'JHSF3.SA'	,
                'KLBN11.SA'	,
                'RENT3.SA'	,
                'LWSA3.SA'	,
                'LREN3.SA'	,
                'MGLU3.SA'	,
                'MRFG3.SA'	,
                'CASH3.SA'	,
                'BEEF3.SA'	,
                'MRVE3.SA'	,
                'MULT3.SA'	,
                'PCAR3.SA'	,
                'PETR3.SA'	,
                'PETR4.SA'	,
                'PRIO3.SA'	,
                'PETZ3.SA'	,
                'POSI3.SA'	,
                'QUAL3.SA'	,
                'RADL3.SA'	,
                'RDOR3.SA'  ,
                'RAIL3.SA'	,
                'SBSP3.SA'	,
                'SANB11.SA'	,
                'CSNA3.SA'	,
                'SLCE3.SA'	,
                'SULA11.SA'	,
                'SUZB3.SA'	,
                'TAEE11.SA'	,
                'VIVT3.SA'	,
                'TIMS3.SA'	,
                'TOTS3.SA'	,
                'UGPA3.SA'	,
                'USIM5.SA'	,
                'VALE3.SA'	,
                'VIIA3.SA'	,
                'VBBR3.SA'	,
                'WEGE3.SA'	,
                'YDUQ3.SA'  ,
                'CBAV3.SA'  ,
                'NUBR33.SA',
                'MEGA3.SA' ,
                'PARD3.SA' , 
                'BOAS3.SA' ,
                'IVVB11.SA',
                'LOGG3.SA' ,
                'LOGN3.SA' ,
                'CEAB3.SA' ,
                'SEQL3.SA' ,
                'ANIM3.SA' ,
                'ABCB4.SA' ,
                'BLAU3.SA' ,
                'AALR3.SA']
    col1, col2 = st.columns(2)
    with col1:
        Ncontrato = st.number_input('Quantidade Açoes', min_value=100)
    with col2:
        porcentagem = st.number_input('Adicione a % queda', max_value=0.00)
    selecao = st.selectbox('Selecione a ação', acoes)
    Botao_filtrar = st.form_submit_button('Filtrar')
if Botao_filtrar == True:
    data_incio = pd.to_datetime(data_incio)
    data_Fim = pd.to_datetime(data_Fim)
    data_Fim = data_Fim + timedelta(1)
    acoes_df =  yf.download(selecao, data_incio, data_Fim, auto_adjust=True)
    acoes_df = acoes_df.drop(columns=['Volume'])
    acoes_df['Close A'] = acoes_df['Close'].shift(1)
    acoes_df.dropna(inplace=True)
    acoes_df['Minima %'] = (acoes_df['Close A'] - acoes_df['Low'])/ acoes_df['Close A'] *(-100)
    acoes_df['Fechamento %'] = (acoes_df['Close A'] - acoes_df['Close'])/ acoes_df['Close A'] *(-100)
    acoes_df = acoes_df.sort_values('Date',ascending = False)
    filtro_df = acoes_df['Minima %'] < porcentagem
    filtrado_df = acoes_df[filtro_df]
    filtrado_df['Resultado'] = filtrado_df['Fechamento %'] - porcentagem
    filtrado_df['Valor'] = ((filtrado_df['Resultado']/100)* filtrado_df['Close'])* Ncontrato
    valortotal = filtrado_df['Valor'].sum()
    porc_total = filtrado_df['Resultado'].sum()
    valortotal = round(valortotal,2)
    porc_total = round(porc_total,2)
    contotal = len(filtrado_df['Resultado'])
    acerto = 0
    erro = 0
    for i in filtrado_df['Resultado']:
        if i > 0:
            acerto = acerto+1
        if i < 0:
            erro = erro+1
    porc_acerto = (acerto*100)/contotal
    porc_erro = (erro*100)/contotal
    porc_acerto = round(porc_acerto)
    porc_erro = round((porc_erro)*-1)
    v_entrada = acoes_df['Close'][0]
    su_valor = porcentagem/100
    su_valor_a = (su_valor * v_entrada )+ v_entrada
    su_valor_a = round(su_valor_a,2)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(selecao, value = valortotal, delta= str(porc_total)+'%')
    with col2:
        st.metric('Total Entradas:', value= contotal)
    with col3:
        st.metric('Total Ganhos:', value= acerto, delta=str(porc_acerto)+'%')
    with col4:
        st.metric('Total Perdas:', value= erro, delta=str(porc_erro)+'%')
    st.metric('Valor Compra Proximo dia', value= su_valor_a )
    
    grafico_df = filtrado_df.sort_values('Date',ascending = True)
    grafico_df['Acumulado'] = grafico_df['Valor'].cumsum()
    grafico = grafico_df['Acumulado']
    st.line_chart(grafico)
    st.markdown("<h5 style='text-align: center; color: black;'>Tabela filtrada</h5>", unsafe_allow_html=True)
    filtrado_df = filtrado_df.drop(columns=['Close A'])
    acoes_df = acoes_df.drop(columns=['Close A'])
    st.dataframe(filtrado_df, width=1200)
    st.markdown("<h5 style='text-align: center; color: black;'>Tabela Completa</h5>", unsafe_allow_html=True)
    st.dataframe(acoes_df, width=900)


