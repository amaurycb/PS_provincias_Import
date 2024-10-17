import json
import mysql.connector

# Función para conectar a la base de datos
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",      # Cambia por el host de tu base de datos
        user="amaurycb",      # Cambia por tu usuario de la base de datos
        password="rootpass",  # Cambia por la contraseña de la base de datos
        database="mhlocal"  # Cambia por el nombre de la base de datos
    )

# Cargar los datos del archivo JSON
def load_json_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        return json.load(file)

# Escapar apóstrofes en cadenas de texto para evitar errores de SQL
def escape_sql_string(value):
    return value.replace("'", "''")

# Obtener países, estados y zonas de las tablas ps_country, ps_state y ps_zone
def get_countries_states_zones_from_db(cursor):
    # Obtener países y sus zonas
    cursor.execute("SELECT id_country, iso_code, id_zone FROM ps_country")
    countries_db = cursor.fetchall()

    # Obtener estados
    cursor.execute("SELECT id_state, id_country, name FROM ps_state")
    states_db = cursor.fetchall()

    # Obtener zonas
    cursor.execute("SELECT id_zone, name FROM ps_zone")
    zones_db = cursor.fetchall()

    return countries_db, states_db, zones_db

# Comparar y generar estados faltantes, incluyendo id_zone, active, y tax_behavior
def compare_and_generate_inserts(countries_db, states_db, zones_db, json_data):
    insert_statements = []
    country_iso_to_id = {iso: (id_country, id_zone) for id_country, iso, id_zone in countries_db}
    zones_dict = {name: id_zone for id_zone, name in zones_db}

    # Revisar cada país en el JSON
    for country_iso, country_info in json_data.items():
        country_name = country_info['name']
        divisions = country_info.get('divisions', {})
        
        if country_iso in country_iso_to_id:
            id_country, id_zone = country_iso_to_id[country_iso]

            # Revisar divisiones (estados) para el país actual
            for division_code, division_name in divisions.items():
                # Verificar si el estado ya existe en la base de datos
                if not any(state[2] == division_name and state[1] == id_country for state in states_db):
                    # Escapar apóstrofes en los valores
                    escaped_division_name = escape_sql_string(division_name)
                    escaped_division_code = escape_sql_string(division_code)
                    
                    # Crear la consulta de inserción para los estados faltantes, incluyendo id_zone, active y tax_behavior
                    insert_statement = f"INSERT INTO ps_state (id_country, name, iso_code, id_zone, active, tax_behavior) VALUES ({id_country}, '{escaped_division_name}', '{escaped_division_code}', {id_zone}, 1, 0);"
                    insert_statements.append(insert_statement)

    return insert_statements

# Insertar los estados faltantes en la base de datos
def insert_missing_states(cursor, insert_statements):
    for insert_statement in insert_statements:
        cursor.execute(insert_statement)

# Script principal
def main():
    # Cargar el archivo JSON con los países y estados
    json_file = 'iso-3166-2.json'  # Cambia por la ruta del archivo JSON
    json_data = load_json_data(json_file)

    # Conectar a la base de datos
    db_connection = connect_to_db()
    cursor = db_connection.cursor()

    try:
        # Obtener países, estados y zonas de la base de datos
        countries_db, states_db, zones_db = get_countries_states_zones_from_db(cursor)

        # Comparar y generar las consultas de inserción
        insert_statements = compare_and_generate_inserts(countries_db, states_db, zones_db, json_data)

        # Ejecutar las inserciones si hay estados faltantes
        if insert_statements:
            insert_missing_states(cursor, insert_statements)
            db_connection.commit()
            print(f"Se han insertado {len(insert_statements)} estados faltantes.")
        else:
            print("No se encontraron estados faltantes.")
    finally:
        # Cerrar la conexión
        cursor.close()
        db_connection.close()

if __name__ == "__main__":
    main()
