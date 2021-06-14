import os
import time

import psutil


class TestCase:
    def __init__(self, tc_id, name):
        self.tc_id = tc_id
        self.name = name

    def prep(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError

    def clean_up(self):
        raise NotImplementedError

    def execute(self):
        try:
            print(f'TestCase "{self.name}" №{self.tc_id}: этап подготовки')
            self.prep()
            print(f'TestCase "{self.name}" №{self.tc_id}: этап выполнения')
            self.run()
            msg = f'TestCase №{self.tc_id}: OK'
        except Exception as err:
            print(err)
            msg = f'TestCase №{self.tc_id}: Failed'
        finally:   
            print(f'TestCase "{self.name}" №{self.tc_id}: этап завершения')
            self.clean_up()
            return msg


class TestCase1(TestCase):
    def __init__(self, tc_id, name):
        super().__init__(tc_id, name)

    def prep(self):
        unix_starttime = int(time.time())
        if unix_starttime % 2 == 0:
            print(f"Время четное: {unix_starttime}, начинаем тест!")
        else:
            raise Exception(f"Нечетное время: {unix_starttime}!")

    def run(self):
        home_dir = os.path.expanduser(path="~")
        list_of_files = os.listdir(path=home_dir)
        print(f"Список файлов домашней директории: {list_of_files}")

    def clean_up(self):
        print("Действий по завершению не требуется!")


class TestCase2(TestCase):
    def __init__(self, tc_id, name):
        super().__init__(tc_id, name)

    def prep(self):
        mem_total_GB = psutil.virtual_memory().total / (1024 ** 3)
        if mem_total_GB > 1:
            print(f"Память машины больше 1 Гб, выполняем TestCase №{self.tc_id}.")
        else:
            raise Exception(
                "Машина, на которой исполняется код, имеет память меньше 1 Гб!"
            )

    def run(self):
        with open("test", "wb") as f:
            f.write(os.urandom(1024 * 1024))
            print("Файл размером 1024 Кб создан.")

    def clean_up(self):
        if os.path.exists("test"):
            os.remove("test")
            print("Файл успешно удален!")


test1 = TestCase1(1, "Список файлов")
print(test1.execute(), "\n")

test2 = TestCase2(2, "Случайный файл")
print(test2.execute())
