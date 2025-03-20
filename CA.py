from useful_function import generate_key_pair, streebog_hash
import binascii
import datetime

# класс сертификационног центра, отвечает за создание экземпляра класса и работу 
class CertificateAuthority:
    # инициализация
    def __init__(self):
        self._private_key, self._public_key = generate_key_pair()
        self._certificates = {}  # {user_id: certificate}
        self._revoked_certificates = set()  # Set of serial numbers

    # создание сертификата
    def issue_certificate(self, user_id, public_key, validity_days=365):
        # серийный номер
        serial_number = len(self._certificates) + 1
        
        # Даты начала и окончания действия
        validity_start = datetime.datetime.utcnow()
        validity_end = validity_start + datetime.timedelta(days=validity_days)
        
        # данные для подписи
        data = f"{serial_number}{user_id}{binascii.hexlify(public_key).decode()}".encode()

        # подпись сертификата
        signature = streebog_hash(self._private_key + data)

        # создание сертификата
        certificate = {
            'serial_number': serial_number,
            'user_id': user_id,
            'public_key': public_key,
            'validity_start': validity_start,
            'validity_end': validity_end,
            'signature': signature
        }
        self._certificates[user_id] = certificate
        return certificate

    def revoke_certificate(self, serial_number):
        # аннулирование сертификата
        self._revoked_certificates.add(serial_number)

    def verify_certificate(self, certificate):
        # проверка аннулирования
        if certificate['serial_number'] in self._revoked_certificates:
            return False
        
        # проверка срока действия
        current_time = datetime.datetime.utcnow()
        if current_time < certificate['validity_start'] or current_time > certificate['validity_end']:
            return False

        # проверка подписи
        data = f"{certificate['serial_number']}{certificate['user_id']}{binascii.hexlify(certificate['public_key']).decode()}".encode()
        expected_signature = streebog_hash(self._private_key + data)
        return certificate['signature'] == expected_signature