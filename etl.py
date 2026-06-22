# Cargamos las librerias
import pandas as pd
import os
# Carga de datos, como hay muchos dataset cargamos los principales: orders, order_items, products y category

df_orders = pd.read_csv('mi-primer-etl/data/ecommerce_orders.csv')
df_order_items = pd.read_csv('mi-primer-etl/data/ecommerce_order_items.csv')
df_products = pd.read_csv('mi-primer-etl/data/ecommerce_products.csv')
df_categories = pd.read_csv('mi-primer-etl/data/ecommerce_categories.csv')

#Realizamos una primera exploración
print(f" RESUMEN \n")
print(f"El dataset Orders, tiene {len(df_orders)} registros y {len(df_orders.columns)} columnas\n")
print(f"El dataset Order Items, tiene {len(df_order_items)} registros y {len(df_order_items.columns)} columnas\n")
print(f"El dataset Products, tiene {len(df_products)} registros y {len(df_products.columns)} columnas\n")
print(f"El dataset Categories, tiene {len(df_categories)} registros y {len(df_categories.columns)} columnas\n")

# Ahora vamos a usar info para obtener los detalles de un dataset y con head vemos como esta construido, en este caso Orders
print(f"Por medio de info vemos que Orders tiene:\n")
print(df_orders.info())
print("\nVeamos las primeras 3 filas usando head:\n")
print(df_orders.head(3))

#Vamos a identificar y manejar los valores nulos de Orders, aunque info nos ha dado ya una pista
print("\nLos valores nulos encontrados por columnas son:\n")
print(df_orders.isnull().sum())

'''Vemos que promotion_id tiene 73 valores nulos y notes tiene 91. Si decidieramos eliminar dicho valores nulos perderiamos mucha información
con lo cual hay que tener cuidado y analizar en profundidad que nos quieren decir estos valores. Como promotion_id es una columna clave a la hora
de combinar datos con la tabla ecommerce_promotions, lo que vamos a hacer es obsevar que información nos da la columna notes'''
print("\nResumen de notes:\n")
print(df_orders.dropna(subset='notes'))

''' A la vista de lo obtenido, podemos ver que dichas observaciones no tendrían mucho peso si las valorará el departamento de ventas, sin embargo esta información
es de vital importancia para el departamento de logística, ya que da detalles de la entrega. Con lo cual, eliminamos dicha columna '''

df_orders_clean = df_orders.drop(columns='notes')

# Estudio de elementos duplicados

print(f"\nEl nº de valores duplicados en la tabla Orders es de: {df_orders_clean.duplicated().sum()}")

#Como podemos  ver, la tabla Orders no tiene valores duplicados, lo cual nos dice que nuestros datos no tienen errores

# A continuación, vamos a transformar los datos (Corregir el tipo de los datos)

print("\nCon dtypes vemos el tipo de los datos \n")
print(df_orders_clean.dtypes)

# Tenemos que cambiar el tipo de datos en las columnas: order_date y promotion_id
df_orders_clean["order_date"] = pd.to_datetime(df_orders_clean['order_date'])
df_orders_clean["promotion_id"] = df_orders_clean["promotion_id"].astype('Int64')

print("\nLos tipos de datos después de la conversión:")
print(df_orders_clean.dtypes)

# Llegados a este punto, vamos a responder preguntas de negocio

#Primera pregunta: ¿Cuáles son los clientes que más gastaron?
top_5_clientes = df_orders_clean.groupby('customer_id').agg(total_gastado=('total_amount','sum')).sort_values('total_gastado',ascending=False).reset_index()
print(f"\n Los clientes con más ventas son: \n {top_5_clientes.head()}")

#Segunda pregunta: ¿Cuál es el producto más vendido (por cantidad)?
top_cantidad = df_order_items.groupby('product_id').agg(total_cantidad=('quantity','sum')).sort_values('total_cantidad',ascending=False).reset_index()
print(f"\n El producto más vendido en cantidad es: \n {top_cantidad.head(1)}")

#Tercera pregunta: ¿Cómo evolucionaron las ventas mes a mes
#Creamos primero la columna mes en Orders
df_orders_clean['Mes'] = df_orders_clean['order_date'].dt.to_period('M')

ventas_mensuales = df_orders_clean.groupby('Mes').agg(ventas_meses=('total_amount','sum')).reset_index()
print(f"\n Las ventas mensuales han sido: \n {ventas_mensuales}")

#Antes de terminar, guardamos la información de negocio
top_5_clientes.to_csv('mi-primer-etl/output/top_5_clientes.csv',index=False)
top_cantidad.to_csv('mi-primer-etl/output/top_cantidad.csv',index=False)
ventas_mensuales.to_csv('mi-primer-etl/output/ventas_mensuales.csv',index=False)

# Y también guardamos los datos limpios
df_orders_clean.to_csv('mi-primer-etl/output/orders_clean.csv',index=False)

# Por último, vamos a hacer una comparación de formatos, guardamos nuestros datos limpios en formato parquet
df_orders_clean.to_parquet('mi-primer-etl/output/orders_clean.parquet',index=False)

#Comparamos tamaño csv y parquet
csv_size = os.path.getsize('mi-primer-etl/output/orders_clean.csv') / 1024
parquet_size = os.path.getsize('mi-primer-etl/output/orders_clean.parquet') / 1024

print(f"\n Tamaño CSV: {csv_size:.1f} KB")
print(f"\n Tamaño Parquet: {parquet_size:.1f} KB")
print("\n En este caso el formato CSV es menor que el formato Parquet, lo más normal es que el segundo sea mucho menor")