from bs4 import BeautifulSoup


class SiteParser:
    def __init__(self, text, trend_limit=10):
        self._trend_limit = trend_limit
        self._text = text
        # list of parsers to print
        self._parsers = []
        # aggregated dictionary of all sources
        self._trending_articles = {"hero_text": "",
                                   "hero_link": "", "headlines": []}
        self._soup = BeautifulSoup(self.text, 'html.parser')

    @property
    def trend_limit(self):
        return self._trend_limit

    @property
    def trend_limit(self):
        return self._trend_limit

    @property
    def text(self):
        return self._text

    @property
    def soup(self):
        return self._soup

    @property
    def trending_articles(self):
        return self._trending_articles

    def get_element_text(self, css_selector):
        """
        Helper function to select a single html element based on a CSS selector
        and then return the text
        Returns "" if element not found
        """
        element = self.soup.select_one(css_selector)
        if element:
            return element.text.strip()

        return ""

    def get_element_attr(self, css_selector, attribute):
        """
        Helper function to select an attribute from an element based on a CSS
        selector and then return the text
        Returns "" if attribute not found
        """
        attr = self.soup.select_one(css_selector)[attribute]
        if attr:
            return attr.strip()

        return ""

    def washingtonpost(self):
        """ https://www.washingtonpost.com/ """

    def cbsnews(self):
        """ https://www.cbsnews.com/ """
        trending_articles = {"hero_text": "", "hero_link": "", "headlines": []}
        try:
            for tag in self.soup.find_all("div", {"class": "tweets-text"}):
                print(tag.get("id"), "|", tag.text)

        except Exception as e:
            print("CBSNEWS::Failed to parse with exception", e)

    def abcnews(self):
        """ http://abcnews.go.com/ """
        trending_articles = {"hero_text": "", "hero_link": "", "headlines": []}
        try:
            # `Top Stories` defined by abcnews
            stories_section = self.soup.find("div", {"id": "row-1"})
            # trying with select
            hero_link = self.get_element_attr("div #row-1 picture a", "href")
            hero_text = self.get_element_text("div #row-1 figcaption h1")
            print(hero_text, hero_link)

            # Hero story - one usually with a bloated image
            # indicating the main story
            hero_pic = stories_section.find("picture")
            hero_text = stories_section.find(
                "figcaption").find("h1").text.strip()
            hero_link = hero_pic.find("a")["href"]

            trending_articles["hero_text"] = hero_text
            trending_articles["hero_link"] = hero_link

            stories = stories_section.find_all(
                "div", {"class": "headlines-li-div"})
            for tag in stories:
                links = tag.find_all("a", {"class": "black-ln"})
                for link in links:
                    trending_articles["headlines"].append(link["href"])
        except Exception as e:
            print("ABCNEWS::Failed to parse with exception:", e)

        return trending_articles

    def nytimes(self):
        """ https://www.nytimes.com/ """
        trending_articles = {"hero_text": "", "hero_link": "", "headlines": []}
        try:
            # `Top Stories` defined by abcnews
            stories_section = self.soup.find("section", {"id": "top-news"})

            hero_pic = stories_section.find(
                "div", {"class": "photo-spot-region"})
            hero_link = hero_pic.find("a")["href"]
            hero_text = stories_section.find(
                "figcaption").find("h1").text.strip()

            trending_articles["hero_text"] = hero_text
            trending_articles["hero_link"] = hero_link

            stories = stories_section.find_all(
                "div", {"class": "headlines-li-div"})
            for tag in stories:
                links = tag.find_all("a", {"class": "black-ln"})
                for link in links:
                    trending_articles["headlines"].append(link["href"])
        except Exception as e:
            print("NYTIMES::Failed to parse with exception:", e)

        return trending_articles

    def foxnews(self):
        """ http://www.foxnews.com """

    def usatoday(self):
        """ https://www.usatoday.com/ """

    def chicagotribune(self):
        """ http://www.chicagotribune.com/ """

    def nbcnews(self):
        """ https://www.nbcnews.com/ """

    def latimes(self):
        """ http://www.latimes.com/ """

    def npr(self):
        """ https://www.npr.org/ """

    def wsj(self):
        """ https://www.wsj.com/ """
