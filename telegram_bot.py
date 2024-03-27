import os
import tempfile

import numpy as np
from telegram import Bot

import settings
import telegram_settings as t_settings
from data_Base_Connect import connection
import cv2
from datetime import datetime, timedelta


class Telegram_bot:
    def __init__(self):
        self.bot = Bot(token=t_settings.bot_token)
        self.chat_id = t_settings.user_chat_id

    async def send_data(self, image, photo, message):
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=message)

            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                temp_filename = temp_file.name
                cv2.imwrite(temp_filename, image)

                # Закрываем временный файл явно
                temp_file.close()
                await self.bot.send_photo(chat_id=self.chat_id, photo=temp_filename)

                os.unlink(temp_filename)

            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                temp_filename = temp_file.name
                cv2.imwrite(temp_filename, photo)

                # Закрываем временный файл явно
                temp_file.close()
                await self.bot.send_photo(chat_id=self.chat_id, photo=temp_filename)

                os.unlink(temp_filename)

        except Exception as e:
            print(f"Error in sending message! {e}")

    def check_data(self, descriptor, image):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Persons")
        persons = cursor.fetchall()

        for person in persons:
            data_base_descriptor = np.frombuffer(person[4], dtype=np.float64)
            distance = np.linalg.norm(np.array(data_base_descriptor) - np.array(descriptor))

            last_name = person[1]
            first_name = person[2]
            patronymic = person[3]
            photo_array = np.frombuffer(person[5], dtype=np.uint8)
            photo = cv2.imdecode(photo_array, cv2.IMREAD_COLOR)

            if distance < 0.55:
                person_id = person[0]
                cursor.execute("SELECT * FROM Sightings WHERE person_id = %s", (person_id,))
                sighting = cursor.fetchall()
                if sighting:
                    sighting_time = sighting[len(sighting) - 1][2]
                    if datetime.now() - sighting_time > timedelta(seconds=settings.timeout):
                        cursor.execute("INSERT INTO Sightings (person_id, camera_photo) VALUES (%s, %s) RETURNING id",
                                       (person_id, cv2.imencode('.jpg', image)[1].tobytes()))
                        connection.commit()
                        cursor.close()
                        return True, self.create_message(last_name, first_name, patronymic), photo
                    else:
                        cursor.close()
                        return None, None, None
                else:
                    cursor.execute("INSERT INTO Sightings (person_id, camera_photo) VALUES (%s, %s) RETURNING id",
                                   (person_id, cv2.imencode('.jpg', photo)[1].tobytes()))
                    connection.commit()
                    cursor.close()
                    return True, self.create_message(last_name, first_name, patronymic), photo
            else:
                continue

        return None, None, None

    def create_message(self, last_name, first_name, patronymic):
        return f"{last_name} {first_name} {patronymic} был замечен в {datetime.now().strftime('%H:%M:%S')}"
