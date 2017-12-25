from bs4 import BeautifulSoup


class Article:
    """ Article object for each article found """

    def __init__(self, link, text):
        self.link = link
        self.text = text

    def set_hero_text(self, hero_text):
        if not hero_text:
            hero_text = ""
        self.trending_articles["hero_text"] = hero_text

    def set_hero_link(self, hero_link):
        if not hero_link:
            hero_link = ""
        self.trending_articles["hero_link"] = hero_link

    def set_headlines(self, headlines):
        if not headlines:
            headlines = ""
        self.trending_articles["headlines"] = headlines


class SiteParser:
    """ Module for parsing news html documents """

    def __init__(self, text, trend_limit=10):
        self._trend_limit = trend_limit
        self._text = text
        # list of parsers to print
        self._parsers = []
        # formatted dictionary of single source
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
        attr = self.soup.select_one(css_selector)
        if attr:
            attr = attr[attribute]
            return attr.strip()

        return ""

    def add_headline(self, selector):
        """
        Helper function to add CSS selector element to headlines array
        """
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
        unique_urls = set()
        # option to pass in a selector
        if soup_selector:
            elements = href_selector
        else:
            elements = self.soup.select(href_selector)
        for e in elements:
            temp = {}
            link = e["href"]
            temp["splash_title"] = e.text.strip()
            temp["link"] = link

            if remove_strings:
                for s in remove_strings:
                    temp["splash_title"] = temp["splash_title"].replace(
                        s, "").strip()

            if link not in unique_urls:
                unique_urls.add(link)
                headlines.append(temp)
        return headlines

    def washingtonpost(self):
        """ https://www.washingtonpost.com/ """
        try:
            # three possible hero tags
            possible_heroes = [
                "section#top-content div[data-chain-name='hp-bignews1']"
                " div.headline a[data-pb-field='web_headline']",
                "section#main-content div.headline.x-large "
                "a[data-pb-field='web_headline']",
                "section#main-content div.headline.xx-large "
                "a[data-pb-field='web_headline']"]

            for p in possible_heroes:
                hero_link = self.get_element_attr(p, "href")
                hero_text = self.get_element_text(p)
                if hero_link:
                    break

            self.trending_articles["hero_text"] = hero_text
            self.trending_articles["hero_link"] = hero_link
            possible_headlines = [
                "section#main-content div[data-chain-name='hp-top-table-main']"
                " div.headline a[data-pb-field='web_headline']",
                "section#top-content div[data-chain-name='hp-bignews3']"
                " div.headline a[data-pb-field='web_headline']"
            ]
            for h in possible_headlines:
                top_stories = self.get_headlines(h)
                if top_stories:
                    break

            self.trending_articles["headlines"] = top_stories
        except Exception as e:
            print("WASHINGTONPOST::Failed to parse with exception:", e)

        return self.trending_articles

    def cbsnews(self):
        """ https://www.cbsnews.com/ """
        try:
            # desktop and mobile renders
            possible_heroes = [
                "div.module-hero h1.title a",
                "div.content-primary header div a"
            ]

            for p in possible_heroes:
                hero_link = self.get_element_attr(p, "href")
                hero_text = self.get_element_text(p)
                if hero_link:
                    break

            self.trending_articles["hero_text"] = hero_text
            self.trending_articles["hero_link"] = hero_link

            possible_headlines = [
                "div.listing-standard-lead li.item-full-lead a",
                "div[data-tb-region='Hard News'] li[data-tb-region-item] "
                "a[data-click-tracking]"
            ]
            for h in possible_headlines:
                top_stories = self.get_headlines(h)
                if top_stories:
                    break

            # limit to 10 - CBS has a long list not self identifying top ones
            self.trending_articles["headlines"] = top_stories[:10]
        except Exception as e:
            print("CBSNEWS::Failed to parse with exception", e)

        return self.trending_articles

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
            hero_link = self.get_element_attr(
                ".photo-spot-region .story-heading a", "href")
            hero_text = self.get_element_text(
                ".photo-spot-region .story-heading a")

            self.trending_articles["hero_text"] = hero_text
            self.trending_articles["hero_link"] = hero_link
            # left column stories
            left_stories = self.get_headlines(
                "#top-news div.a-column div[class=collection]"
                " article.story h2.story-heading a")
            # center stories
            center_stories = self.get_headlines(
                "#top-news div.b-column div[class=collection]"
                " article.story h2.story-heading a")
            left_stories.extend(center_stories)
            self.trending_articles["headlines"] = left_stories
        except Exception as e:
            print("NYTIMES::Failed to parse with exception:", e)

        return self.trending_articles

    def foxnews(self):
        """ http://www.foxnews.com """
        try:
            hero_link = self.get_element_attr(
                ".primary h1 a", "href")
            hero_text = self.get_element_text(
                ".primary h1 a")

            self.trending_articles["hero_text"] = hero_text
            self.trending_articles["hero_link"] = hero_link

            top_stories = self.get_headlines(
                ".top-stories li[data-vr-contentbox] > a")

            self.trending_articles["headlines"] = top_stories
        except Exception as e:
            print("FOXNEWS::Failed to parse with exception:", e)

        return self.trending_articles

    def usatoday(self):
        """ https://www.usatoday.com/ """
        try:
            hero_link = self.get_element_attr(
                "a.hfwmm-primary-hed-link", "href")
            hero_text = self.get_element_text(
                "a.hfwmm-primary-hed-link")
            # exception 09 election heading
            if not hero_link:
                hero_link = self.get_element_attr(
                    "a.big-headline-primary-href", "href")
                hero_text = self.get_element_text(
                    "a.big-headline-primary-href")
            self.trending_articles["hero_text"] = hero_text
            self.trending_articles["hero_link"] = hero_link

            top_stories = self.get_headlines(
                ".hfwmm-list .js-asset-link")
            # exception for 09 election day
            election_stories = self.get_headlines("a.tssm-list-link")
            top_stories.extend(election_stories)
            self.trending_articles["headlines"] = top_stories
        except Exception as e:
            print("USATODAY::Failed to parse with exception:", e)

        return self.trending_articles

    def chicagotribune(self):
        """ http://www.chicagotribune.com/ """
        try:
            hero_link = self.get_element_attr(
                "h2.trb_outfit_primaryItem_article_title"
                ".trb_outfit_featuredArticleTitle a", "href")
            hero_text = self.get_element_text(
                "h2.trb_outfit_primaryItem_article_title"
                ".trb_outfit_featuredArticleTitle a")

            self.trending_articles["hero_text"] = hero_text
            self.trending_articles["hero_link"] = hero_link

            story_list = self.soup.select_one(".trb_outfit_list ")
            stories = story_list.select(".trb_outfit_list_headline_a")
            top_stories = self.get_headlines(stories, soup_selector=True)
            self.trending_articles["headlines"] = top_stories
        except Exception as e:
            print("CHICAGOTRIBUNE::Failed to parse with exception:", e)

        return self.trending_articles

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
            self.trending_articles["headlines"].extend(top_stories)
        except Exception as e:
            print("LATIMES::Failed to parse with exception:", e)

        return self.trending_articles

    def wsj(self):
        """ https://www.wsj.com/ """
        try:
            possible_heroes = [
                "div.lead-story div.LS-SECONDARY-BIG-IMAGE "
                "a.wsj-headline-link",
                "div.lead-story h3.LEAD a.wsj-headline-link",
                "div.lead-story h3.heading-1 a.wsj-headline-link"
            ]
            for p in possible_heroes:
                hero_link = self.get_element_attr(p, "href")
                hero_text = self.get_element_text(p)
                if hero_link:
                    break

            self.trending_articles["hero_text"] = hero_text
            self.trending_articles["hero_link"] = hero_link

            top_stories = self.get_headlines("div.lead-story "
                                             "a.wsj-headline-link")
            self.trending_articles["headlines"].extend(top_stories)
        except Exception as e:
            print("WSJ::Failed to parse with exception:", e)

        return self.trending_articles
