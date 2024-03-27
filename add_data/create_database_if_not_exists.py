import psycopg2


def create_database_if_not_exists():
    try:
        # Подключение к созданной базе данных
        connection = psycopg2.connect(
            host='localhost',
            port='5432',
            database='technoparkData',
            user='postgres',
            password='123',
        )
        cursor = connection.cursor()

        # Создание таблиц Persons и Sightings, если они не существуют
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Persons (
                id SERIAL PRIMARY KEY,
                last_name VARCHAR(100) NOT NULL,
                first_name VARCHAR(100) NOT NULL,
                patronymic VARCHAR(100),
                face_encoding BYTEA NOT NULL,
                photo BYTEA NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Sightings (
                id SERIAL PRIMARY KEY,
                person_id INT NOT NULL,
                sighting_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                camera_photo BYTEA NOT NULL,
                FOREIGN KEY (person_id) REFERENCES Persons(id)
            )
        """)

        # Закрытие соединения
        connection.commit()
        connection.close()

    except psycopg2.Error as ex:
        print(f"Ошибка: {ex}. Не удалось подключиться к базе данных или создать таблицы.")
    except Exception as e:
        print(f"Ошибка: {e}. Неожиданная ошибка при создании базы данных или таблиц.")


