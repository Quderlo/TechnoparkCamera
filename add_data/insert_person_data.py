import cv2
import psycopg2
from data_Base_Connect import connection


def insert_person_data(last_name, first_name, patronymic, face_encoding, photo):
    try:
        cursor = connection.cursor()

        # Преобразование изображения и дескриптора в строковое представление с помощью pickle
        face_descriptor = face_encoding.tobytes()
        _, image_encoded = cv2.imencode('.jpg', photo)
        image_bytes = image_encoded.tobytes()

        # SQL-запрос на вставку данных в таблицу Persons
        sql_query = """
            INSERT INTO "CameraUI_person" (last_name, first_name, patronymic, face_descriptor, photo)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql_query,
                       (last_name, first_name, patronymic, psycopg2.Binary(face_descriptor),
                        psycopg2.Binary(image_bytes)))

        connection.commit()
        print("Данные успешно добавлены в таблицу Persons.")

        connection.close()
    except psycopg2.Error as ex:
        print(f"Ошибка: {ex}. Не удалось добавить данные в таблицу Persons.")
    except Exception as e:
        print(f"Ошибка: {e}. Неожиданная ошибка при вставке данных в таблицу Persons.")


