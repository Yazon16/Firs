from useful_function import generate_key_pair
import binascii

# класс юзер, используется для добавления и создания пользователя
class User:
    # инициализация пользователя
    def __init__(self, user_id, password):
        self._user_id = user_id
        self._password = password
        self._private_key, self._public_key = generate_key_pair()
        self._certificate = None

    # ргистрация в УЦ с указанием срока действия сертификата
    def register_with_ca(self, ca, validity_days=365):
        self._certificate = ca.issue_certificate(self._user_id, self._public_key, validity_days)

    def login(self, ca):
        # попытка входа в систему
        if self._certificate is None:
            print(f"{self._user_id} has no certificate.")
            return

        # проверка, что сертификат принадлежит текущему пользователю
        if self._certificate['user_id'] != self._user_id:
            print(f"{self._user_id} cannot use someone else's certificate.")
            return
        
        # попытка верификации сертификата 
        if ca.verify_certificate(self._certificate):
            print(f"{self._user_id} logged in successfully")
        else:
            print(f"{self._user_id} login failed")

    # вывод информации о сертификате
    def print_certificate_info(self):        
        if self._certificate is None:
            print("Сертификат отсутствует.")
            return
        print(f"= Информация о сертификате {self._certificate['serial_number']} =")
        print(f"Серийный номер: {self._certificate['serial_number']}")
        print(f"Имя пользователя: {self._certificate['user_id']}")
        print(f"Открытый ключ: {binascii.hexlify(self._certificate['public_key']).decode()}")
        print(f"Дата начала действия: {self._certificate['validity_start']}")
        print(f"Дата окончания действия: {self._certificate['validity_end']}")
        print(f"Подпись: {binascii.hexlify(self._certificate['signature']).decode()}")
        print("===============================")