from create_database_if_not_exists import create_database_if_not_exists
from capture_photo import capture_photo
from compute_face_descriptor import compute_face_descriptor
from enter_person_data import enter_person_data
from insert_person_data import insert_person_data


def main():
    create_database_if_not_exists()
    image = capture_photo()
    descriptor = compute_face_descriptor(image)

    if descriptor is not None:
        print("Дескриптор лица вычислен успешно.")
    else:
        print("Не удалось вычислить дескриптор лица.")
        return

    last_name, first_name, patronymic = enter_person_data()

    insert_person_data(last_name, first_name, patronymic, descriptor, image)


if __name__ == "__main__":
    main()
