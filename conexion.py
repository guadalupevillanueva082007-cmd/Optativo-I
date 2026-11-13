import psycopg2

conexion = psycopg2.connect(
    host='localhost',
    port=5432,
    dbname='comercio',
    user='postgres',
    password='G080607'
)
print('Conexion exitosa a la base de datos')

cursor = conexion.cursor()

cursor.execute(
    'INSERT INTO clientes (nombre, email, ciudad) VALUES (%s, %s, %s)',
    ('Pedro Lopez', 'pedro@mail.com', 'Capiata')
)
conexion.commit()
print('Cliente insertado correctamente')