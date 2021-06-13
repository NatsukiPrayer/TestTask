import requests
from bs4 import BeautifulSoup
import threading
import concurrent.futures


class Crawler:
    def __init__(self, main_link):
        self.__links = {}              #Словарь чтобы проверять уже посещённые ссылки и видеть переходы между ссылками
        self.__main_link = main_link   #Домашняя страница
        self.__queue = [main_link]     #Очередь в которую будут добавлять ссылки
        self.__domain = list(map(lambda x: x.split('.'), self.__main_link.split('//')))[1][0]    #Выделение домена из ссылки
        self.__lock = threading.Lock()  #Далее используя это ограничиваем доступ потоков к памяти во избежании ошибок

    def main_crawl(self, depth):   #Основная функция с расспределением потоков
        i = 0
        while self.__queue and i < depth:                                            #Поскольку сайты огромны, особенно последние три
            with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.__queue)) as executor:  #Введено ограничение на глубину, чтобы алгоритм
                executor.map(self.__crawl, [self.__dequeue() for i in range(len(self.__queue))])    #Не работал бесконечно
            i += 1

    def __crawl(self, link):  #Функция которая пробегает по странице и ищет другие переходы на ней
        if link not in self.__links:
            with self.__lock:
                self.__links[link] = []
            try:
                r = requests.get(link, allow_redirects=True)
            except requests.exceptions.TooManyRedirects:
                return
            except requests.exceptions.MissingSchema:
                return
            soup = BeautifulSoup(r.text, 'html.parser')
            for a in soup.find_all('a', href=True):
                rel_link = a['href']
                if rel_link != '':
                    if rel_link[0] == '/':  #Проверка относительности ссылки
                        rel_link = self.__main_link + rel_link
                        print(rel_link)  #Можно расскомментировать чтобы видеть пробегаемые ссылки
                    if rel_link[0] == 'h':  #Проверка наличия протокола, чтобы определить ссылку
                        with self.__lock:
                            if self.__domain not in list((map(lambda x: x.split('.'), rel_link.split('//'))))[1]:
                                return
                            if rel_link not in self.__queue and rel_link not in self.__links:
                                self.__enqueue(rel_link)  #Добавление ссылки в очередь
                                self.__links[link].append(rel_link)  #Добавление ссылки в списк посещённых


    def get_links(self):
        return self.__links

    def __enqueue(self, item):
            self.__queue.append(item)

    def __dequeue(self):
        with self.__lock:
            return self.__queue.pop(0)
