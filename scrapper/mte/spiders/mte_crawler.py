import re

import scrapy


class MteCrawlerSpider(scrapy.Spider):
    name = "mte_crawler"
    allowed_domains = ["developpement-durable.gouv.fr"]
    ## Modifier le nom de la consultation ci-dessous
    start_urls = [
        "http://www.consultations-publiques.developpement-durable.gouv.fr/"
        + "projet-de-decret-pris-en-application-de-l-article-a2569.html"
    ]

    _max_pages = 0  # Pour limiter le nombre de pages, si nécessaire
    _page = 0
    _p_com = re.compile(r" (\d*) commentaires")

    def parse(self, response):
        if self._max_pages == 0:
            dateart = response.css("div.dateart::text").getall()
            nb_comment = int(self._p_com.search(dateart[0]).group(1))
            self._max_pages = ((nb_comment - 1) // 20) + 1
            self.logger.info(
                "Commentaires : %d, pages: %d", nb_comment, self._max_pages
            )

        for ligne in response.css("div.ligne-com"):
            yield {
                "sujet": ligne.css("div.titresujet::text").getall(),
                "texte": ligne.css("div.textesujet *::text").getall(),
            }

        if self._page < self._max_pages:
            self._page += 1
            self.logger.info("Téléchargement page %d", self._page)
            yield scrapy.Request(
                self.start_urls[0] + "?debut_forums=" + str(20 * self._page),
                callback=self.parse,
                dont_filter=True,
            )
