import re

import scrapy


class MteCrawlerSpider(scrapy.Spider):
    name = "mte_crawler"
    allowed_domains = ["consultations-publiques.developpement-durable.gouv.fr"]
    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": '1',
        "DOWNLOAD_DELAY": '5',
    }

    # ## Modifier le nom de la consultation ci-dessous
    _start_url = "http://www.consultations-publiques.developpement-durable.gouv.fr/projet-de-decret-pris-en-application-de-l-article-a2569.html"
    _max_pages = None
    _page = 0
    _p_com = re.compile(r" (\d*) commentaires")

    def start_requests(self):
        ## La première page permet de calculer le nombre de pages à télécharger
        self.logger.info("Téléchargement de la première page")
        yield scrapy.Request(url=self._start_url, callback=self.parse)


    def parse(self, response):
        ## Au début, détermination du nombre de pages à télécharger
        if self._page == 0:
            ## Extraction du sous-titre de la consultation
            dateart = response.css("div.dateart::text").getall()
            nb_comment = int(self._p_com.search(dateart[0]).group(1))
            self._max_pages = ((nb_comment - 1) // 20) + 1  # 20 commentaires par page
            self.logger.info(
                "Commentaires : %d, pages: %d", nb_comment, self._max_pages
            )

        nb_com = 0
        for ligne in response.css("div.ligne-com"):
            nb_com += 1
            yield {
                "sujet": ligne.css("div.titresujet::text").getall(),
                "texte": ligne.css("div.textesujet *::text").getall(),
            }
        self.logger.info("Extraction de %d commentaires", nb_com)

        if self._page < self._max_pages:
            self._page += 1
            page = "?debut_forums=" + str(20 * self._page)
            self.logger.info("Téléchargement page %s", page)
            yield scrapy.Request(
                self._start_url + page,
                callback=self.parse,
                dont_filter=True,
            )

