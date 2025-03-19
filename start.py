from user import User
from CA import CertificateAuthority
import datetime

# Создание УЦ
ca = CertificateAuthority()

# Создание участников
alice = User("alice", "12345")
bob = User("bob", "23445")

# Регистрация участников в УЦ
alice.register_with_ca(ca, validity_days=30)
bob.register_with_ca(ca, validity_days=1)

# Вывод информации о сертификатах
alice.print_certificate_info()
bob.print_certificate_info()

# Попытка входа Алисы
alice.login(ca)

# Попытка входа Боба (без использования чужого сертификата)
bob.login(ca)

# попытка зайти под чужим сертификатом
bob._certificate = alice._certificate  # Боб пытается использовать сертификат Алисы
bob.login(ca)  # Должно завершиться ошибкой

# Проверка сертификатов
print("alice certificate valid:", ca.verify_certificate(alice._certificate))  # True
print("bob certificate valid:", ca.verify_certificate(bob._certificate))  # True

# Искусственно изменяем дату окончания действия сертификата Боба на прошедшую дату
bob._certificate['validity_end'] = datetime.datetime.utcnow() - datetime.timedelta(days=1)

# Проверка сертификатов после истечения срока
print("alice certificate valid after expiration:", ca.verify_certificate(alice._certificate))  # True
print("bob certificate valid after expiration:", ca.verify_certificate(bob._certificate))  # False