import os.path

class Writer:
    def __init__(self, filename, urlest):
        self.__filename = '{}.xml'.format(filename)
        self.__urlset = urlest

    def write(self, rewrite=True):
        if rewrite:
            self.__writing()
        else:
            if os.path.isfile(self.__filename):
                Exception('File already exist')
            else:
                self.__writing()

    def __writing(self):
        with open(self.__filename, 'w') as xml:
            xml.write('<?xml version = "1.0" encoding = "UTF-8"?>\n')
            xml.write('<urlset xmlns = "http://www.sitemaps.org/schemas/sitemap/0.9">\n')
            for url in self.__urlset:
                xml.write("<url>\n")
                xml.write("<loc>\n")
                xml.write('{}\n'.format(str(url.encode("utf-8")))[1:].replace("'", '').replace('&', '&amp;'))
                xml.write("</loc>\n")
                xml.write("</url>\n")
            xml.write('</urlset>')
