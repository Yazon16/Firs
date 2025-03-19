from useful_function import generate_key_pair
import binascii

class User:
    def __init__(self, user_id, password):
        self._user_id = user_id
        self._password = password
        self._private_key, self._public_key = generate_key_pair()
        self._certificate = None

    def register_with_ca(self, ca, validity_days=365):
        # Регистрация в УЦ с указанием срока действия сертификата
        self._certificate = ca.issue_certificate(self._user_id, self._public_key, validity_days)

    def login(self, ca):
        # Попытка входа в систему
        if self._certificate is None:
            print(f"[User] {self._user_id} has no certificate.")
            return

        # Проверка, что сертификат принадлежит текущему пользователю
        if self._certificate['user_id'] != self._user_id:
            print(f"[User] {self._user_id} cannot use someone else's certificate.")
            return

        if ca.verify_certificate(self._certificate):
            print(f"[User] {self._user_id} logged in successfully")
        else:
            print(f"[User] {self._user_id} login failed")

    def print_certificate_info(self):
        # Вывод информации о сертификате
        if self._certificate is None:
            print("Сертификат отсутствует.")
            return

        print("=== Информация о сертификате ===")
        print(f"Серийный номер: {self._certificate['serial_number']}")
        print(f"Имя пользователя: {self._certificate['user_id']}")
        print(f"Открытый ключ: {binascii.hexlify(self._certificate['public_key']).decode()}")
        print(f"Дата начала действия: {self._certificate['validity_start']}")
        print(f"Дата окончания действия: {self._certificate['validity_end']}")
        print(f"Подпись: {binascii.hexlify(self._certificate['signature']).decode()}")
        print("===============================")