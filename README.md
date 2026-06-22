# ETL de un comercio electrónico con Python

## Descripción

Proyecto ETL desarrollado en Python para procesar datos de un comercio electrónico. El pipeline realiza tareas de extracción, limpieza, transformación y generación de métricas de negocio.

## Tecnologías usadas
- Python
- Pandas
- PyArrow
- CSV
- Parquet

## Datasets

La datos procesados contienen información de pedidos de un comercio electrónico, incluyendo:

- order_id
- customer_id
- product_id
- quantity
- total_amount
- order_date

## Proceso ETL

### Extracción

Lectura de los datos desde archivos CSV mediante Pandas.

### Transformación

- Estudio de los valores nulos y eliminación, teniendo en cuenta si son campos críticos.
- Identificación y eliminación de registros duplicados.
- Conversión de tipos de datos, especificamente en order_date y promotion_id.

### Carga

Generación de datasets limpios y agregados en formato CSV y Parquet.

## Resultados

- top_5_clientes.csv
- top_cantidad.csv
- ventas_mensuales.csv

## Instalación

``` bash
pip install pandas pyarrow
```

## Ejecución

```bash
python etl.py
```

## Autor

Juan Poma
