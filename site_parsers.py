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

    def add_headline(self, selector):
        link = self.get_element_attr(selector, "href")
        title = self.get_element_text(selector)
        headline = {"splash_title": title, "link": link}
        self.trending_articles["headlines"].append(headline)

    def get_headlines(self, href_selector, soup_selector=False,
                      remove_strings=None):
        """
        Helper function to get multiple headline stories
        """
        headlines = []
        # option to pass in a selector
        if soup_selector:
            elements = href_selector
        else:
            elements = self.soup.select(href_selector)
        for e in elements:
            temp = {}
            temp["splash_title"] = e.text.strip()
            temp["link"] = e["href"]
            headlines.append(temp)
            if remove_strings:
                for s in remove_strings:
                    temp["splash_title"] = temp["splash_title"].replace(
                        s, "").strip()
        return headlines

    def washingtonpost(self):
        """ https://www.washingtonpost.com/ """

    def cbsnews(self):
        """ https://www.cbsnews.com/ """
        try:
            for tag in self.soup.find_all("div", {"class": "tweets-text"}):
                print(tag.get("id"), "|", tag.text)

        except Exception as e:
            print("CBSNEWS::Failed to parse with exception", e)

    def abcnews(self):
        """ http://abcnews.go.com/ """

        try:
            # Hero story - one usually with a bloated image
            # indicating the main story
            hero_link = self.get_element_attr("div #row-1 picture a", "href")
            hero_text = self.get_element_text("div #row-1 figcaption h1")

            self.trending_articles["hero_text"] = hero_text
            self.trending_articles["hero_link"] = hero_link
            self.trending_articles["headlines"] = self.get_headlines(
                "div #row-1 .headlines-li-div a.black-ln")

        except Exception as e:
            print("ABCNEWS::Failed to parse with exception:", e)

        return self.trending_articles

    def nytimes(self):
        """ https://www.nytimes.com/ """

        try:
            # `Top Stories` defined by abcnews
            stories_section = self.soup.find("section", {"id": "top-news"})

            hero_pic = stories_section.find(
                "div", {"class": "photo-spot-region"})
            hero_link = hero_pic.find("a")["href"]
            hero_text = stories_section.find(
                "figcaption").find("h1").text.strip()

            self.trending_articles["hero_text"] = hero_text
            self.trending_articles["hero_link"] = hero_link

            stories = stories_section.find_all(
                "div", {"class": "headlines-li-div"})
            for tag in stories:
                links = tag.find_all("a", {"class": "black-ln"})
                for link in links:
                    self.trending_articles["headlines"].append(link["href"])
        except Exception as e:
            print("NYTIMES::Failed to parse with exception:", e)

        return self.trending_articles

    def foxnews(self):
        """ http://www.foxnews.com """

    def usatoday(self):
        """ https://www.usatoday.com/ """

    def chicagotribune(self):
        """ http://www.chicagotribune.com/ """

    def nbcnews(self):
        """ https://www.nbcnews.com/ """
        try:
            hero_link = self.get_element_attr(
                ".js-top-stories-content .panel-txt a", "href")
            hero_text = self.get_element_text(
                ".js-top-stories-content .panel-txt_overlay a")
            # print(hero_text, hero_link)
            self.trending_articles["hero_text"] = hero_text
            self.trending_articles["hero_link"] = hero_link

            type_strings = ["Video\n\n",
                            "Gallery\n\n", "Data\n\n", "Photo\n\n"]
            top_stories = self.get_headlines(
                ".js-top-stories-content div .story-link .media-body > a",
                remove_strings=type_strings)
            secondary_stories = self.get_headlines(
                ".js-top-stories-content div .story-link > a",
                remove_strings=type_strings)
            top_stories.extend(secondary_stories)
            self.trending_articles["headlines"] = top_stories
        except Exception as e:
            print("NBCNEWS::Failed to parse with exception:", e)

        return self.trending_articles

    def latimes(self):
        """ http://www.latimes.com/ """
        try:
            hero_link = self.get_element_attr(
                "section:nth-of-type(1) .trb_outfit_primaryItem "
                ".trb_outfit_primaryItem_article_title > a", "href")
            hero_text = self.get_element_text(
                "section:nth-of-type(1) .trb_outfit_primaryItem "
                ".trb_outfit_primaryItem_article_title > a")

            self.trending_articles["hero_text"] = hero_text
            self.trending_articles["hero_link"] = hero_link

            top_story_section = self.soup.select_one(
                "ul.trb_outfit_group_list")
            top_stories = top_story_section.select(
                ".trb_outfit_relatedListTitle_a")
            top_stories = self.get_headlines(top_stories,
                                             soup_selector=True)
            self.trending_articles["headlines"] = top_stories
        except Exception as e:
            print("LATIMES::Failed to parse with exception:", e)

        return self.trending_articles

    def npr(self):
        """ https://www.npr.org/ """
        try:
            hero_link = self.get_element_attr(
                ".stories-wrap-featured .story-text "
                "a[data-metrics*='Click Story 1']", "href")
            hero_text = self.get_element_text(
                ".stories-wrap-featured .story-text "
                "a[data-metrics*='Click Story 1']")

            self.trending_articles["hero_text"] = hero_text
            self.trending_articles["hero_link"] = hero_link

            # second_story
            self.add_headline(".stories-wrap-featured .story-text "
                              "a[data-metrics*='Click Story 2']")

            top_stories = self.get_headlines(".nib-container .item-nib a")
            self.trending_articles["headlines"] = top_stories
        except Exception as e:
            print("LATIMES::Failed to parse with exception:", e)

        return self.trending_articles

    def wsj(self):
        """ https://www.wsj.com/ """
