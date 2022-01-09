# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 19:26:45 2022

@author: Luis Mauricio García Noverola
"""
# se importa la librería pandas
import pandas as pd
#%%

# se lee el archivo .csv con pandas y se guarda en un dataframe
synergy_dataframe = pd.read_csv('synergy_logistics_database.csv', index_col=0,
                                encoding='utf-8', 
                                parse_dates=[4, 5])
#%%

# se separa el dataframe original en importaciones/exportaciones
exports = synergy_dataframe[synergy_dataframe['direction'] == 'Exports']
imports = synergy_dataframe[synergy_dataframe['direction'] == 'Imports']
#%%

# se define la funcion que resuelve la consigna 1
def consigna_1(df, num_rutas):
    routes = df.groupby(by=['origin', 'destination', 'transport_mode'])
    descrip_routes = routes.describe()['total_value']
    routes_freq = descrip_routes['count']
    routes_freq_sort = routes_freq.sort_values(ascending=False)
    routes_freq_sort_df = routes_freq_sort.to_frame().reset_index()
    lista_rutas_demanda = routes_freq_sort_df.head(num_rutas)
    
    return lista_rutas_demanda
#%%
# se pide al usuario el núm. de rutas con mayor demanda
demanda_rutas = int(input('Número mínimo de rutas más demandadas de exportaciones/importaciones: '))

# se obtienen en variables los dataframes con las respuestas a la consigna 1 para
# importaciones y exportaciones
result1_exp = consigna_1(exports, demanda_rutas)
result1_imp = consigna_1(imports, demanda_rutas)

# se imprime en consola los resultados
print('\nSolución a la consigna 1 para exportaciones:\n')
print(result1_exp)
print('\nSolución a la consigna 1 para importaciones:\n')
print(result1_imp)
#%%

# se importa la librería seaborn
import seaborn as sns
#%%

# se define la funcion que resuelve la consigna 2
def consigna_2(df):
    # se copian los datos en un nuevo dataframe
    datos_transport = df.copy()
    # se crea la columna de year_month para usar como marca
    datos_transport['year_month'] = datos_transport['date'].dt.strftime('%Y-%m')
    datos_year_month = datos_transport.groupby(['year_month', 'transport_mode'])
    # La serie que nos interesa es la de mean para el valor total.
    serie = datos_year_month.mean()['total_value']
    # se convierte la serie a df
    transport_dym = serie.to_frame().reset_index()
    # le damos la forma que queremos
    transport_dym = transport_dym.pivot('year_month', 'transport_mode', 'total_value')
    # Grafico
    sns.lineplot(data=transport_dym)
#%%

# se obtiene el análisis de los medios de transporte en una gráfica para
# responder a la consigna 2
consigna_2(synergy_dataframe)
#%%

# se define la funcion que resuelve la consigna 3
def consigna_3(df, porcentaje):
    pais_total_value = df.groupby('origin').sum()['total_value'].reset_index()
    total_value_for_percent = pais_total_value['total_value'].sum()
    pais_total_value['percent'] = 100 * pais_total_value['total_value'] / total_value_for_percent
    pais_total_value.sort_values(by='percent', ascending=False, inplace=True)
    pais_total_value['percent accum'] = pais_total_value['percent'].cumsum()
    lista_acumulada = pais_total_value[pais_total_value['percent accum'] < porcentaje]
    
    return lista_acumulada
#%%

# se pide al usuario el porcentaje del valor total generado
porcent_util = int(input('¿Qué porcentaje del valor total generado por las operaciones le resulta útil a SynergyLogistics?: '))

# se obtienen en variables los dataframes con las respuestas a la consigna 3 para
# importaciones y exportaciones
result3_exp = consigna_3(exports, porcent_util)
result3_imp = consigna_3(imports, porcent_util)

# se imprime en consola los resultados
print('\nSolución a la consigna 3 para exportaciones:\n')
print(result3_exp)
print('\nSolución a la consigna 3 para importaciones:\n')
print(result3_imp)