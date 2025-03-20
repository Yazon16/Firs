from user import User
from CA import CertificateAuthority
import datetime

# Создание УЦ
ca = CertificateAuthority()

# Создание участников
alice = User("alice", "12345")
bob = User("bob", "23445")

# Регистрация участников в УЦ (если у них ещё нет сертификатов)
alice.register_with_ca(ca, validity_days=30)
bob.register_with_ca(ca, validity_days=1)

# Вывод информации о сертификатах
alice.print_certificate_info()
bob.print_certificate_info()

# Попытка входа Алисы
alice.login(ca)

# Попытка входа Боба
bob.login(ca)

# Попытка Боба использовать сертификат Алисы
print("\nПопытка Боба использовать сертификат Алисы:")
bob._certificate = alice._certificate  # Боб пытается использовать сертификат Алисы
bob.login(ca)  # Должно завершиться ошибкой

# Проверка сертификатов
print("\nПроверка сертификатов:")
print("alice certificate valid:", ca.verify_certificate(alice._certificate))  # True
print("bob certificate valid:", ca.verify_certificate(bob._certificate))  # True

# Искусственно изменяем дату окончания действия сертификата Боба на прошедшую дату
bob._certificate['validity_end'] = datetime.datetime.utcnow() - datetime.timedelta(days=1)

# Проверка сертификата Боба после истечения срока
print("\nПроверка сертификата Боба после истечения срока:")
print("bob certificate valid after expiration:", ca.verify_certificate(bob._certificate))  # False