import random
from faker import Faker
from django.core.management.base import BaseCommand
from users.models import User
from customers.models import Customer

# Faker 라이브러리 인스턴스 생성
faker = Faker("ko_KR")  # 한국어 데이터 생성

class Command(BaseCommand):
    help = "유저와 고객 더미 데이터를 생성합니다."

    def handle(self, *args, **kwargs):
        self.stdout.write("더미 데이터 생성을 시작합니다...")
        self.create_dummy_users_and_customers()

    def create_dummy_users_and_customers(self):
        try:
            # 유저 생성
            users = []
            for i in range(30):
                phone_number = f"010-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
                user = User.objects.create_user(
                    phone_number=phone_number,
                    name=faker.name(),
                    gender=random.choice(['Male', 'Female']),
                    date_of_birth=faker.date_of_birth(),
                    address=faker.address(),
                    password="password123"
                )
                users.append(user)
                self.stdout.write(f"유저 생성 완료: {user.phone_number}")

            # 고객 생성
            for user in users:
                customers = []
                for j in range(30):
                    customer = Customer(
                        user=user,
                        name=faker.name(),
                        gender=random.choice(['Male', 'Female']),
                        phone_number=f"010-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
                        address=faker.address(),
                        key=f"{random.randint(100000, 999999)}"
                    )
                    customers.append(customer)
                Customer.objects.bulk_create(customers)  # 한 번에 고객 데이터 생성
                self.stdout.write(f"{user.phone_number}의 고객 30명 생성 완료")

            self.stdout.write("더미 데이터 생성이 완료되었습니다!")

        except Exception as e:
            self.stderr.write(f"오류 발생: {e}")
