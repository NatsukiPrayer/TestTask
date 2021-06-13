import Visualization
import Crawler
import Writer
import DBConnection
import time

if __name__ == '__main__':
    t_start = time.time()
    new = Crawler.Crawler('http://crawler-test.com/')  #Здесь создаётся объект-паучок, в аргументах ссылка на сайт
    new.main_crawl(2)
    print(time.time() - t_start)
    links = new.get_links()
    print(len(links))
    to_file = Writer.Writer('crawler_test', links) #Здесь создаётся сам .xml файл, в аргументах название и ссылки
    to_file.write()
    to_DB = DBConnection.DBConnect('sitemaps') #Здесь задаётся имя базы данных для записи
    to_DB.to_table('crawler_test', links)
    to_DB.commit()
    '''pic = Visualization.Visual(links) #Эту часть расскомментировать при желании получить рисунок
    pic.draw()'''
