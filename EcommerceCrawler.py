
from OmniCrawler import Selenium
from Google.Cloud import MySQL
from datetime import datetime
from DataStructure.StringManipulator import Concatenate, Enumerate, Manipulate
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
import traceback
import time


class Run:

    RunningLog = None
    Selenium = None
    Search = None
    Product = None
    Merchant = None

    MySQL = MySQL(database_name="Ecommerce", operating_system = "linux")

    class Ecommerce_login(MySQL.Base):
        __tablename__ = "Ecommerce_login"
        user_ID = Column(Integer, primary_key=True)
        username = Column(String(255))
        password = Column(String(255))
        access_type = Column(String(255))
        record_lastupdate_datetime = Column(DateTime)
        RunningLog = relationship("Ecommerce_running_log", backref="Ecommerce_login")

    class Ecommerce_running_log(MySQL.Base):
        __tablename__ = "Ecommerce_running_log"
        running_ID = Column(Integer, primary_key=True)
        user_ID = Column(Integer, ForeignKey('Ecommerce_login.user_ID'))
        platform_source = Column(String(255))
        crawl_source_type = Column(String(255))
        crawl_max_ordinal = Column(Integer, default=50)
        crawl_max_page = Column(Integer, default=5)
        crawl_search = Column(Boolean, default=True)
        crawl_product = Column(Boolean, default=True)
        crawl_merchant = Column(Boolean, default=True)
        search_input = Column(String(255))
        search_order_by = Column(String(255))
        title_or_description_required_words = Column(String(255))
        running_status = Column(String(255))
        running_scheduler_days = Column(Integer)
        record_creation_datetime = Column(DateTime)
        record_lastupdate_datetime = Column(DateTime)
        Search = relationship("Ecommerce_search", backref="Ecommerce_running_log")
        Product = relationship("Ecommerce_product", backref="Ecommerce_running_log")
        Merchant = relationship("Ecommerce_merchant", backref="Ecommerce_running_log")

    class Ecommerce_search(MySQL.Base):
        __tablename__ = "Ecommerce_search"
        record_ID = Column(Integer, primary_key=True)
        running_ID = Column(Integer, ForeignKey("Ecommerce_running_log.running_ID"))
        product_number_of_results = Column(Integer)
        product_page = Column(Integer)
        product_ordinal = Column(Integer)
        product_name = Column(String(255))
        product_type = Column(String(255))
        product_price = Column(Integer)
        merchant_type = Column(String(255))
        merchant_sending_from = Column(String(255))
        product_rating_value = Column(Float(24))
        product_review_count_total = Column(Integer)
        product_wishlist = Column(Integer)
        product_delivery_promo = Column(Text)
        product_html_path = Column(Text)
        merchant_html_path = Column(Text)
        record_lastupdate_datetime = Column(DateTime)

    class Ecommerce_product(MySQL.Base):
        __tablename__ = "Ecommerce_product"
        record_ID = Column(Integer, primary_key=True)
        running_ID = Column(Integer, ForeignKey("Ecommerce_running_log.running_ID"))
        product_name = Column(Text)
        product_tree = Column(Text)
        product_review_count_total = Column(Integer)
        product_rating_value = Column(Float(24))
        product_review_count_5 = Column(Integer)
        product_review_count_4 = Column(Integer)
        product_review_count_3 = Column(Integer)
        product_review_count_2 = Column(Integer)
        product_review_count_1 = Column(Integer)
        product_percent_successful_transaction = Column(Float(24))
        product_transaction_count = Column(Integer)
        product_price = Column(Integer)
        product_available_stock = Column(Integer)
        product_wishlist = Column(Integer)
        product_mortgage_interest_percent = Column(Integer)
        product_minimum_mortgage = Column(Integer)
        product_coupon = Column(String(255))
        product_coupon_description = Column(String(255))
        product_delivery_promo = Column(String(255))
        product_view = Column(Integer)
        product_qty_sold = Column(Integer)
        product_condition = Column(String(255))
        product_minimum_purchase = Column(Integer)
        product_insurance = Column(String(255))
        product_discussion_count = Column(Integer)
        product_specifications = Column(Text)
        product_description = Column(Text)
        product_reviewers_list = Column(Text)
        product_discussers_list = Column(Text)
        product_hit_status = Column(String(255))
        product_comment_count_total = Column(Integer)
        product_html_path = Column(Text)
        merchant_name = Column(String(255))
        merchant_type = Column(String(255))
        merchant_reputation_score = Column(Integer)
        merchant_sending_from = Column(String(255))
        merchant_last_online = Column(String(255))
        merchant_percent_successful_transaction = Column(Float(24))
        merchant_product_qty_sold = Column(Integer)
        merchant_discussion_replied_percent = Column(Float(24))
        merchant_chat_replied_percent = Column(Float(24))
        merchant_discussion_replied_average_time = Column(String(255))
        merchant_chat_replied_average_time = Column(String(255))
        merchant_total_active_products = Column(Integer)
        merchant_followers = Column(Integer)
        merchant_open_since = Column(String(255))
        merchant_html_path = Column(Text)
        record_lastupdate_datetime = Column(DateTime)

    class Ecommerce_merchant(MySQL.Base):
        __tablename__ = "Ecommerce_merchant"
        record_ID = Column(Integer, primary_key=True)
        running_ID = Column(Integer, ForeignKey("Ecommerce_running_log.running_ID"))
        merchant_name = Column(String(255))
        merchant_type = Column(String(255))
        merchant_slogan_short = Column(String(255))
        merchant_slogan_long = Column(Text)
        merchant_reputation_score = Column(Integer)
        merchant_last_online = Column(String(255))
        merchant_chat_replied_percent = Column(Float(24))
        merchant_sending_from = Column(String(255))
        merchant_offline_status = Column(String(255))
        merchant_open_since = Column(String(255))
        merchant_following = Column(Integer)
        merchant_followers = Column(Integer)
        merchant_product_quality_score = Column(Float(24))
        merchant_product_quality_reviews_count_total = Column(Integer)
        merchant_product_quality_reviews_count_5stars = Column(Integer)
        merchant_product_quality_reviews_count_4stars = Column(Integer)
        merchant_product_quality_reviews_count_3stars = Column(Integer)
        merchant_product_quality_reviews_count_2stars = Column(Integer)
        merchant_product_quality_reviews_count_1star = Column(Integer)
        merchant_satisfaction_1_month_positive = Column(Integer)
        merchant_satisfaction_1_month_neutral = Column(Integer)
        merchant_satisfaction_1_month_negative = Column(Integer)
        merchant_satisfaction_6_month_positive = Column(Integer)
        merchant_satisfaction_6_month_neutral = Column(Integer)
        merchant_satisfaction_6_month_negative = Column(Integer)
        merchant_satisfaction_12_month_positive = Column(Integer)
        merchant_satisfaction_12_month_neutral = Column(Integer)
        merchant_satisfaction_12_month_negative = Column(Integer)
        merchant_transaction_1_month_success_percent = Column(Float(24))
        merchant_transaction_6_month_success_percent = Column(Float(24))
        merchant_transaction_12_month_success_percent = Column(Float(24))
        merchant_transaction_1_month_count = Column(Integer)
        merchant_transaction_6_month_count = Column(Integer)
        merchant_transaction_12_month_count = Column(Integer)
        merchant_transaction_1_month_speed = Column(String(255))
        merchant_transaction_6_month_speed = Column(String(255))
        merchant_transaction_12_month_speed = Column(String(255))
        merchant_packing_duration = Column(String(255))
        merchant_product_qty_sold = Column(Integer)
        merchant_total_showcase = Column(Integer)
        merchant_total_active_products = Column(Integer)
        merchant_location = Column(Text)
        merchant_product_variation_list = Column(Text)
        merchant_transaction_total = Column(Integer)
        merchant_coupon = Column(String(255))
        merchant_coupon_description = Column(String(255))
        merchant_drop_rate = Column(Float(24))
        merchant_html_path = Column(Text)
        record_lastupdate_datetime = Column(DateTime)

    def CrawlTokopediaSearch(self):

        self.Search.product_page = 0
        word_separator = "+"
        self.Selenium.link = "https://www.tokopedia.com/search?st=product&q="
        self.Selenium.Load(''.join([self.Selenium.link, Concatenate().InfuseSeparator(main=self.RunningLog.search_input, separator=word_separator)]))
        self.Selenium.ExtractElements("//a")
        for element in self.Selenium.elements:
            if "Hot List" in element.text:
                self.Selenium.link = Manipulate().RemoveParts("&page=2", self.Selenium.ExtractElementAttribute("href", xpath="//a[contains(@class, 'GUHElpkt')]"))
                self.Selenium.root_xpath = "//div[contains(@class, '_29iRsaHv')]/div"
            else:
                self.Selenium.root_xpath = "//div[contains(@class, '_1hoMwZCy')]/div"
        product_last_result_number_in_page = self.Selenium.ExtractElementText("//div[contains(@class, '_1lUX-bZg')]/span/strong[2]").split()[2]
        self.Search.product_number_of_results = Enumerate().CleanNumber(self.Selenium.ExtractElementText("//div[contains(@class, '_1lUX-bZg')]/span/strong[3]"))
        self.Search.product_ordinal = 0
        while self.Search.product_page == 0 or (int(self.Search.product_number_of_results) != int(product_last_result_number_in_page) and (self.Search.product_page < self.RunningLog.crawl_max_page or self.RunningLog.crawl_max_page == 0) and (self.Search.product_ordinal < self.RunningLog.crawl_max_ordinal or self.RunningLog.crawl_max_ordinal == 0)):
            self.Search.product_page += 1
            if self.Search.product_page != 1:
                self.Selenium.Load(''.join([self.Selenium.link, "&page=", str(self.Search.product_page)]))
                product_last_result_number_in_page = self.Selenium.ExtractElementText("//div[contains(@class, '_1lUX-bZg')]/span/strong[2]").split()[2]
                self.Search.product_number_of_results = Enumerate().CleanNumber(self.Selenium.ExtractElementText("//div[contains(@class, '_1lUX-bZg')]/span/strong[3]"))
            if self.Search.product_ordinal < self.RunningLog.crawl_max_ordinal or self.RunningLog.crawl_max_ordinal == 0:
                product_elements_count = len(self.Selenium.ExtractElements(self.Selenium.root_xpath))
                self.Search.element_ordinal = 0
                while (self.Search.element_ordinal < product_elements_count) and (self.Search.product_ordinal < self.RunningLog.crawl_max_ordinal or self.RunningLog.crawl_max_ordinal == 0):
                    self.Search.element_ordinal += 1
                    sub_root_xpath = ''.join([self.Selenium.root_xpath, "[", str(self.Search.element_ordinal), "]"])
                    product_wrapper_class_type = self.Selenium.ExtractElementAttribute("class", sub_root_xpath)
                    if product_wrapper_class_type == "ta-inventory":
                        self.Search.product_type = "Top Ads"
                        subelement_ordinal = 0
                        topads_elements_count = len(self.Selenium.ExtractElements(''.join([sub_root_xpath, "/div[4]/div"])))
                        self.Selenium.max_try_count = 1
                        while subelement_ordinal < topads_elements_count:
                            subelement_ordinal += 1
                            self.Search.product_ordinal += 1
                            subsub_root_xpath = ''.join([sub_root_xpath, "/div[4]/div[", str(subelement_ordinal), "]/div"])
                            self.Search.product_name = self.Selenium.ExtractElementText(''.join([subsub_root_xpath, "/a/div[2]/span"]))
                            self.Search.product_price = Enumerate().CleanNumber(self.Selenium.ExtractElementText(''.join([subsub_root_xpath, "/a/div[2]/div/span/span"])))
                            self.Selenium.max_try_count = 1
                            self.Search.merchant_sending_from = self.Selenium.ExtractElementText(''.join([subsub_root_xpath, "/a/div[2]/div/div/div[contains(@class, 'ta-product-shop-location-wrapper')]/span"]))
                            self.Search.product_review_count_total = Enumerate().CleanNumber(self.Selenium.ExtractElementText(''.join([subsub_root_xpath, "/a/div[2]/div/div[2]/span"])))
                            if self.Search.product_review_count_total == "TERBARU":
                                self.Search.product_review_count_total = 0
                            self.Selenium.ResetParameters("max_try_count")
                            self.Search.product_html_path = self.Selenium.ExtractElementAttribute("href", ''.join([subsub_root_xpath, "/a[2]"]))
                            self.Search.merchant_html_path = self.Search.product_html_path.split("/")
                            self.Search.merchant_html_path = ''.join([self.Search.merchant_html_path[0],  "/",  self.Search.merchant_html_path[1],  "/",  self.Search.merchant_html_path[2],  "/",  self.Search.merchant_html_path[3]])
                            self.MySQL.Insert(self.Search)
                    elif product_wrapper_class_type == "_33JN2R1i pcr":
                        self.Search.product_type = "Normal"
                        self.Search.product_ordinal = 1
                        subsub_root_xpath = ''.join([sub_root_xpath, "/div"])
                        self.Selenium.max_try_count = 1
                        self.Search.product_name = self.Selenium.ExtractElementText(''.join([subsub_root_xpath, "/a/div[2]/h3"]))
                        self.Search.product_price = Enumerate().CleanNumber(self.Selenium.ExtractElementText(''.join([subsub_root_xpath, "/a/div[2]/div/span/span"])))
                        self.Search.merchant_sending_from = self.Selenium.ExtractElementText(''.join([subsub_root_xpath, "/a/div[2]/div/div[1]/div[1]/span[1]"]))
                        self.Search.product_review_count_total = Enumerate().CleanNumber(self.Selenium.ExtractElementText(''.join([subsub_root_xpath, "/a/div[2]/div/div[2]/span"])))
                        self.Search.product_html_path = self.Selenium.ExtractElementText(''.join([subsub_root_xpath, "/a"]))
                        self.MySQL.Insert(self.Search)
                    self.Selenium.ResetParameters("max_try_count")

    def CrawlTokopediaProduct(self):

        html_path_temp = self.Product.product_html_path.split("/")
        spliced_search_path_properties = html_path_temp[4].split("?")
        product_review_html_path = self.Product.merchant_html_path + "/" + spliced_search_path_properties[0] + "/review?" + spliced_search_path_properties[1]
        product_discussion_html_path = self.Product.merchant_html_path + "/" + spliced_search_path_properties[0] + "/talk?" + spliced_search_path_properties[1]
        self.Product.product_tree = self.Selenium.ExtractElementsToSeparatedText(separator=" > ", xpath="//*[contains(@id, 'breadcrumb-container')]/*/li/h2")
        self.Product.product_name = self.Selenium.ExtractElementText("//*[contains(@class, 'rvm-product-title')]")
        self.Product.product_review_count_total = self.Selenium.ExtractElementText("//*[contains(@class, 'review-count')]")
        self.Product.product_percent_successful_transaction = Enumerate().CleanNumber(self.Selenium.ExtractElementText("//span[contains(@class, 'fw-600 success-transaction-percent')]"))
        self.Product.product_transaction_count = self.Selenium.ExtractElementToNumber("//span[contains(@class, 'fw-600 all-transaction-count')]")
        self.Product.product_price = self.Selenium.ExtractElementAttribute("value", "//*[contains(@id, 'product_price_int')]")
        self.Product.product_wishlist = Manipulate().RemoveParts(" Wishlist", self.Selenium.ExtractElementText("//div[contains(@class, 'rvm-left-column--right')]/div/div[2]/a/div/span"))
        self.Product.product_minimum_mortgage = Enumerate().CleanNumber(self.Selenium.ExtractElementText("//*[contains(@class, 'installment-min-price')]"))
        self.Selenium.max_try_count = 1
        self.Product.product_coupon = self.Selenium.ExtractElementText("//*[contains(@class, 'shop-coupon__title')]")
        self.Selenium.ResetParameters("max_try_count")
        if self.Product.product_coupon is not None:
            self.Product.product_coupon_description = self.Selenium.ExtractElementText("//*[contains(@class, 'shop-coupon__desc')]")
        self.Product.merchant_name = self.Selenium.ExtractElementText("//span[contains(@class, 'inline-block va-middle shop-name')]")
        self.Product.merchant_type = self.Selenium.ExtractElementAttribute("data-original-title", "//div[contains(@class, 'rvm-merchat-name')]/*")
        if self.Product.merchant_type == None:
            self.Product.merchant_type = "Normal"
        self.Product.merchant_reputation_score = Manipulate().RemoveParts(" points", Enumerate().CleanNumber(self.Selenium.ExtractElementAttribute("data-original-title", "//div[contains(@class, 'rvm-merchat-reputation ta-center mt-10')]/img")))
        self.Product.merchant_sending_from = self.Selenium.ExtractElementText("//div[contains(@class, 'rvm-merchat-city mt-10')]/span")
        self.Product.merchant_last_online = self.Selenium.ExtractElementText("//div[contains(@class, 'rvm-merchant-last-active')]/span/span")
        merchant_successful_transaction = self.Selenium.ExtractElementText("//div[contains(@data-original-title, 'Dihitung dalam 30 hari terakhir')]/div[2]")
        if merchant_successful_transaction is not None and merchant_successful_transaction != "":
            merchant_successful_transaction_splited = merchant_successful_transaction.split("% (")
            self.Product.merchant_percent_successful_transaction = Enumerate().CleanNumber(merchant_successful_transaction_splited[0])
            self.Product.merchant_product_qty_sold = Enumerate().ReformToNumber(Manipulate().RemoveParts(" Produk)", merchant_successful_transaction_splited[1]))
        merchant_discussion_replied = self.Selenium.ExtractElementText("//div[contains(@id, 'shop-response-rate-talk')]/div[2]")
        if merchant_discussion_replied is not None and merchant_discussion_replied != "":
            merchant_discussion_replied_splited = merchant_discussion_replied.split("% (± ")
            self.Product.merchant_discussion_replied_percent = merchant_discussion_replied_splited[0]
            self.Product.merchant_discussion_replied_average_time = Enumerate().CleanNumber(merchant_discussion_replied_splited[1])
        merchant_chat_replied = self.Selenium.ExtractElementText("//div[contains(@id, 'shop-response-rate-topchat')]/div[2]")
        if merchant_chat_replied is not None and merchant_chat_replied != "":
            merchant_chat_replied_splited = merchant_chat_replied.split("% (± ")
            self.Product.merchant_chat_replied_percent = merchant_chat_replied_splited[0]
            self.Product.merchant_chat_replied_average_time = Enumerate().CleanNumber(merchant_chat_replied_splited[1])
        self.Product.product_view = self.Selenium.ExtractElementToNumber("//div[contains(@class, 'mt-30')]/div/div[1]/div/div[2]")
        self.Product.product_qty_sold = self.Selenium.ExtractElementToNumber("//div[contains(@class, 'mt-30')]/div/div[2]/div/div[2]")
        self.Product.product_condition = self.Selenium.ExtractElementText("//div[contains(@class, 'mt-30')]/div/div[3]/div/div[2]")
        self.Product.product_minimum_purchase = self.Selenium.ExtractElementText("//div[contains(@class, 'mt-30')]/div/div[4]/div/div[2]")
        self.Product.product_insurance = self.Selenium.ExtractElementText("//div[contains(@class, 'mt-30')]/div/div[5]/div/div[2]")
        self.Product.product_discussion_count = Manipulate().RemoveParts(["Diskusi Produk ", "(", ")"], self.Selenium.ExtractElementText("//span[contains(@class, 'inline-block va-middle talk-container')]"))
        self.Product.product_description = self.Selenium.ExtractElementText("//div[contains(@class, 'tab-content product-summary__content-box mb-30')]/*[contains(@id, 'info')]")
        self.Selenium.Load(product_review_html_path)
        self.Selenium.max_try_count = 1
        self.Product.product_rating_value = self.Selenium.ExtractElementAttribute("content", "//meta[contains(@itemprop, 'ratingValue')]")
        self.Product.product_review_count_5 = self.Selenium.ExtractElementText("//table[contains(@id, 'rating-review-table-desktop')]/tbody/tr[1]/td[3]/div")
        self.Selenium.ResetParameters("max_try_count")
        if self.Product.product_review_count_5 is not None:
            self.Product.product_review_count_4 = self.Selenium.ExtractElementText("//table[contains(@id, 'rating-review-table-desktop')]/tbody/tr[2]/td[3]/div")
            self.Product.product_review_count_3 = self.Selenium.ExtractElementText("//table[contains(@id, 'rating-review-table-desktop')]/tbody/tr[3]/td[3]/div")
            self.Product.product_review_count_2 = self.Selenium.ExtractElementText("//table[contains(@id, 'rating-review-table-desktop')]/tbody/tr[4]/td[3]/div")
            self.Product.product_review_count_1 = self.Selenium.ExtractElementText("//table[contains(@id, 'rating-review-table-desktop')]/tbody/tr[5]/td[3]/div")
        self.Product.product_reviewers_list = self.Selenium.ExtractElementsToSeparatedText(separator="@", xpath="//div[contains(@id, 'ulasan')]//*[contains(@class, 'text-black-7 fw-600')]")
        self.Selenium.Load(product_discussion_html_path)
        self.Product.product_discussers_list = self.Selenium.ExtractElementsToSeparatedText(separator="@", xpath="//div[contains(@id, 'diskusi')]//*[contains(@class, 'product-talk__name ng-binding')]")
        title_or_description_required_words = self.RunningLog.title_or_description_required_words.lower()
        title_or_description_required_words_splited = title_or_description_required_words.split()
        self.Product.product_hit_status = "HIT"
        for title_or_description_required_word in title_or_description_required_words_splited:
            if title_or_description_required_word not in self.Product.product_name.lower() and title_or_description_required_word not in self.Product.product_description.lower() and title_or_description_required_word not in self.Product.product_specifications.lower():
                self.Product.product_hit_status = "NO HIT"
        self.MySQL.Insert(self.Product)

    def CrawlTokopediaMerchant(self):

        self.Selenium.max_try_count = 1
        self.Merchant.merchant_type = self.Selenium.ExtractElementAttribute("data-original-title", "//i[contains(@class, 'image-power-merchant cursor-default inline-block va-middle')]")
        if self.Merchant.merchant_type is None:
            self.Merchant.merchant_type = self.Selenium.ExtractElementAttribute("data-original-title", "//i[contains(@class, 'image-official-badge cursor-default inline-block va-middle')]")
            if self.Merchant.merchant_type is None:
                self.Merchant.merchant_type = "Normal"
        self.Selenium.ResetParameters("max_try_count")
        if self.Merchant.merchant_type != "Official Store":
            self.Merchant.merchant_product_variation_list = self.Selenium.ExtractElementsToSeparatedText("//ul[contains(@id, 'etalase_container')]/li/a/span")
            self.Selenium.ClickIt("//a[contains(@class, 'view-stat-btn text-center btn btn-second')]")
            self.Merchant.merchant_name = self.Selenium.ExtractElementText("//*[contains(@itemprop, 'name')]")
            self.Merchant.merchant_slogan_long = self.Selenium.ExtractElementText("//*[contains(@class, 'shop-slogan')]")
            self.Merchant.merchant_reputation_score = Enumerate().CleanNumber(Manipulate().RemoveParts(" points", self.Selenium.ExtractElementAttribute("data-original-title", "//*[contains(@id, 'shop-reputation-points')]")))
            self.Merchant.merchant_followers = self.Selenium.ExtractElementToNumber("//*[contains(@id, 'favorit-shop')]")
            merchant_header_extraction_type = "not baited"
            for bait in self.Selenium.ExtractElements("//div[contains(@id, 'gold-stat')]"):
                if "lalu" in bait.text or "Online" in bait.text or "Offline" in bait.text:
                    merchant_header_extraction_type = "baited"
            if merchant_header_extraction_type == "not baited":
                self.Merchant.merchant_last_online = self.Selenium.ExtractElementText("//div[contains(@class, 'span4')]/ul/li[1]")
                self.Merchant.merchant_sending_from = self.Selenium.ExtractElementText("//div[contains(@class, 'span4')]/ul/li[2]")
                self.Merchant.merchant_offline_status = self.Selenium.ExtractElementText("//div[contains(@class, 'span4')]/ul/li[3]")
                self.Merchant.merchant_open_since = self.Selenium.ExtractElementText("//div[contains(@class, 'span4')]/ul/li[4]")
            elif merchant_header_extraction_type == "baited":
                self.Merchant.merchant_last_online = self.Selenium.ExtractElementText("//div[contains(@id, 'gold-stat')]/ul/li[1]/small")
                self.Merchant.merchant_sending_from = self.Selenium.ExtractElementText("//div[contains(@id, 'gold-stat')]/ul/li[2]/small")
                self.Merchant.merchant_offline_status = self.Selenium.ExtractElementText("//div[contains(@id, 'gold-stat')]/ul/li[3]/small")
                self.Merchant.merchant_open_since = self.Selenium.ExtractElementText("//div[contains(@id, 'gold-stat')]/ul/li[4]/small")
            self.Merchant.merchant_slogan_short = self.Selenium.ExtractElementText("//div[contains(@class, 'css-2msupa')]/div/p")
            if self.Merchant.merchant_slogan_short is None:
                self.Merchant.merchant_slogan_short = self.Selenium.ExtractElementText("//p[contains(@class, 'white shop-gold-b_shadow')]/small")
                if self.Merchant.merchant_slogan_short is None:
                    self.Merchant.merchant_slogan_short = self.Selenium.ExtractElementText("//div[contains(@class, 'span10')]/div[2]")
            self.Merchant.merchant_product_quality_score = Manipulate().RemoveParts("/ 5", self.Selenium.ExtractElementText("//div[contains(@class, 'score fw-600 mt-5')]"))
            self.Merchant.merchant_product_quality_reviews_count_total = self.Selenium.ExtractElementText("//span[contains(@class, 'reviews-num')]")
            self.Selenium.max_try_count = 1
            self.Merchant.merchant_product_quality_reviews_count_5stars = self.Selenium.ExtractElementText("//div[contains(@class, 'rating-bar-container five')]/span[3]")
            self.Selenium.ResetParameters("max_try_count")
            if self.Merchant.merchant_product_quality_reviews_count_5stars is not None:
                self.Merchant.merchant_product_quality_reviews_count_4stars = self.Selenium.ExtractElementText("//div[contains(@class, 'rating-bar-container four')]/span[3]")
                self.Merchant.merchant_product_quality_reviews_count_3stars = self.Selenium.ExtractElementText("//div[contains(@class, 'rating-bar-container three')]/span[3]")
                self.Merchant.merchant_product_quality_reviews_count_2stars = self.Selenium.ExtractElementText("//div[contains(@class, 'rating-bar-container two')]/span[3]")
                self.Merchant.merchant_product_quality_reviews_count_1star = self.Selenium.ExtractElementText("//div[contains(@class, 'rating-bar-container one')]/span[3]")
            self.Selenium.max_try_count = 1
            self.Merchant.merchant_satisfaction_1_month_positive = Enumerate().CleanNumber(self.Selenium.ExtractElementText("//div[contains(@class, 'mt-5 shop-satisfaction')]/table/tbody/tr[1]/td[2]"))
            self.Selenium.ResetParameters("max_try_count")
            if self.Merchant.merchant_satisfaction_1_month_positive is not None:
                self.Merchant.merchant_satisfaction_6_month_positive = Enumerate().CleanNumber(self.Selenium.ExtractElementText("//div[contains(@class, 'mt-5 shop-satisfaction')]/table/tbody/tr[1]/td[3]"))
                self.Merchant.merchant_satisfaction_12_month_positive = Enumerate().CleanNumber(self.Selenium.ExtractElementText("//div[contains(@class, 'mt-5 shop-satisfaction')]/table/tbody/tr[1]/td[4]"))
                self.Merchant.merchant_satisfaction_1_month_neutral = Enumerate().CleanNumber(self.Selenium.ExtractElementText("//div[contains(@class, 'mt-5 shop-satisfaction')]/table/tbody/tr[2]/td[2]"))
                self.Merchant.merchant_satisfaction_6_month_neutral = Enumerate().CleanNumber(self.Selenium.ExtractElementText("//div[contains(@class, 'mt-5 shop-satisfaction')]/table/tbody/tr[2]/td[3]"))
                self.Merchant.merchant_satisfaction_12_month_neutral = Enumerate().CleanNumber(self.Selenium.ExtractElementText("//div[contains(@class, 'mt-5 shop-satisfaction')]/table/tbody/tr[2]/td[4]"))
                self.Merchant.merchant_satisfaction_1_month_negative = Enumerate().CleanNumber(self.Selenium.ExtractElementText("//div[contains(@class, 'mt-5 shop-satisfaction')]/table/tbody/tr[3]/td[2]"))
                self.Merchant.merchant_satisfaction_6_month_negative = Enumerate().CleanNumber(self.Selenium.ExtractElementText("//div[contains(@class, 'mt-5 shop-satisfaction')]/table/tbody/tr[3]/td[3]"))
                self.Merchant.merchant_satisfaction_12_month_negative = Enumerate().CleanNumber(self.Selenium.ExtractElementText("//div[contains(@class, 'mt-5 shop-satisfaction')]/table/tbody/tr[3]/td[4]"))
            self.Selenium.max_try_count = 1
            self.Merchant.merchant_transaction_1_month_success_percent = Enumerate().CleanNumber(self.Selenium.ExtractElementText("//div[contains(@class, 'trans data-trans1')]/div[contains(@class, 'chart-container')]/div[1]/p"))
            self.Selenium.ResetParameters("max_try_count")
            if self.Merchant.merchant_transaction_1_month_success_percent is not None:
                self.Merchant.merchant_transaction_1_month_count = Enumerate().CleanNumber(Manipulate().RemoveParts(["Dari ", " Transaksi"], self.Selenium.ExtractElementText("//div[contains(@class, 'trans data-trans1')]/div[contains(@class, 'chart-container')]/div[2]/p")))
                self.Selenium.ClickIt("//ul[contains(@class, 'text-center mt-15')]/li[contains(@data-trans, '2')]")
                self.Merchant.merchant_transaction_6_month_success_percent = Enumerate().CleanNumber(self.Selenium.ExtractElementText("//div[contains(@class, 'trans data-trans2')]/div[contains(@class, 'chart-container')]/div[1]/p"))
                self.Merchant.merchant_transaction_6_month_count = Enumerate().CleanNumber(Manipulate().RemoveParts(["Dari ", " Transaksi"], self.Selenium.ExtractElementText("//div[contains(@class, 'trans data-trans2')]/div[contains(@class, 'chart-container')]/div[2]/p")))
                self.Selenium.trigger_xpaths_list.pop(-1)
                self.Selenium.ClickIt("//ul[contains(@class, 'text-center mt-15')]/li[contains(@data-trans, '3')]")
                self.Merchant.merchant_transaction_12_month_success_percent = Enumerate().CleanNumber(self.Selenium.ExtractElementText("//div[contains(@class, 'trans data-trans3')]/div[contains(@class, 'chart-container')]/div[1]/p"))
                self.Merchant.merchant_transaction_12_month_count = Enumerate().CleanNumber(Manipulate().RemoveParts(["Dari ", " Transaksi"], self.Selenium.ExtractElementText("//div[contains(@class, 'trans data-trans3')]/div[contains(@class, 'chart-container')]/div[2]/p")))
                self.Selenium.trigger_xpaths_list.pop(-1)
            self.Selenium.ClickIt("//div[contains(@class, 'row-fluid notif-top chartnotif')]/li[2]")
            time.sleep(1)
            self.Selenium.max_try_count = 1
            self.Selenium.sleep_time = 1.5
            self.Merchant.merchant_transaction_1_month_speed = self.Selenium.ExtractElementText("//div[contains(@class, 'trans data-trans1')]/div[contains(@class, 'speed-container')]/div[2]/h3")
            self.Selenium.ResetParameters("max_try_count")
            if self.Merchant.merchant_transaction_1_month_speed is not None:
                self.Selenium.ClickIt("//ul[contains(@class, 'text-center mt-5')]/li[contains(@data-trans, '2')]")
                self.Merchant.merchant_transaction_6_month_speed = self.Selenium.ExtractElementText("//div[contains(@class, 'trans data-trans2')]/div[contains(@class, 'speed-container')]/div[2]/h3")
                self.Selenium.trigger_xpaths_list.pop(-1)
                self.Selenium.ClickIt("//ul[contains(@class, 'text-center mt-5')]/li[contains(@data-trans, '3')]")
                self.Merchant.merchant_transaction_12_month_speed = self.Selenium.ExtractElementText("//div[contains(@class, 'trans data-trans3')]/div[contains(@class, 'speed-container')]/div[2]/h3")
            self.Selenium.ResetParameters()
            merchant_html_info_path = ''.join([self.Merchant.merchant_html_path, "/info"])
            self.Selenium.Load(merchant_html_info_path)
            self.Merchant.merchant_transaction_total = Enumerate().CleanNumber(self.Selenium.ExtractElementText("//ul[contains(@class, 'css-117z4we')]/li[1]/div"))
            self.Merchant.merchant_product_qty_sold = Enumerate().CleanNumber(self.Selenium.ExtractElementText("//ul[contains(@class, 'css-117z4we')]/li[2]/div"))
            self.Merchant.merchant_total_showcase = Enumerate().CleanNumber(self.Selenium.ExtractElementText("//ul[contains(@class, 'css-117z4we')]/li[3]/div"))
            self.Merchant.merchant_total_active_products = Enumerate().CleanNumber(self.Selenium.ExtractElementText("//ul[contains(@class, 'css-117z4we')]/li[4]/div"))
            self.Merchant.merchant_location = self.Selenium.ExtractElementText("//div[contains(@class, 'css-merchant-3nuwWR1y')]")
        elif self.Merchant.merchant_type == "Official Store":
            self.Merchant.merchant_name = self.Selenium.ExtractElementText("//div[contains(@class, 'shop-official__name pt-20 clearfix')]/h1")
            self.Merchant.merchant_slogan_short = self.Selenium.ExtractElementText("//div[contains(@class, 'shop-official__slogan row-fluid')]")
            self.Merchant.merchant_product_variation_list = self.Selenium.ExtractElementsToSeparatedText("//ul[contains(@id, 'etalase_container')]/li/a/span")
            self.Merchant.merchant_followers = self.Selenium.ExtractElementToNumber("//*[contains(@id, 'favorit-shop')]")
            self.Merchant.merchant_transaction_1_month_speed = self.Selenium.ExtractElementAttribute("title", "//span[contains(@id, 'shop-speed')]")
            self.Merchant.merchant_coupon = self.Selenium.ExtractElementText("//div[contains(@class, 'coupon__info-desc')]/h3")
            self.Merchant.merchant_coupon_description = self.Selenium.ExtractElementText("//div[contains(@class, 'coupon__info-desc')]/p")
            merchant_html_info_path = ''.join([self.Merchant.merchant_html_path, "/info"])
            self.Selenium.Load(merchant_html_info_path)
            self.Merchant.merchant_total_showcase = self.Selenium.ExtractElementText("//ul[contains(@class, 'css-1f1fgzs')]/li[1]/div")
            self.Merchant.merchant_total_active_products = self.Selenium.ExtractElementText("//ul[contains(@class, 'css-1f1fgzs')]/li[2]/div")
            self.Merchant.merchant_location = self.Selenium.ExtractElementText("//div[contains(@class, 'css-1triptv')]/div[4]/div")
        self.Selenium.ResetParameters()
        self.MySQL.Insert(self.Merchant)

    def CrawlTokopediaMerchantSearch(self):

        time.sleep(2)
        self.Search.product_page = 1
        self.Search.product_ordinal = 0
        keep_trying_next_page = "YES"
        self.Selenium.root_xpath = "//div[contains(@id, 'showcase-container')]/div[1]/div"
        Selenium.sleep_time = 2
        while keep_trying_next_page == "YES":
            merchant_product_elements_count = self.Selenium.ExtractElements()
            for retry_count in range(0, 20):
                if merchant_product_elements_count is not None:
                    if "Memuat..." in merchant_product_elements_count[0].text:
                        time.sleep(2)
                        merchant_product_elements_count = self.Selenium.ExtractElements()
            merchant_product_elements_count = len(merchant_product_elements_count)
        self.Search.element_ordinal = 0
        if merchant_product_elements_count is not None:
            while self.Search.element_ordinal < merchant_product_elements_count:
                self.Search.element_ordinal += 1
                self.Search.product_ordinal += 1
                sub_root_xpath = ''.join([self.Selenium.root_xpath, "[", str(self.Search.element_ordinal), "]"])
                self.Search.product_name = self.Selenium.ExtractElementText(''.join([sub_root_xpath, "/a/div/div[2]/div[1]"]))
                self.Search.product_type = "From Merchant Page"
                self.Selenium.max_try_count = 1
                self.Search.product_price = Enumerate().CleanNumber(self.Selenium.ExtractElementText(''.join([sub_root_xpath, "/a/div/div[2]/div[2]/div/div[2]/span"])))
                self.Selenium.ResetParameters("max_try_count")
                self.Search.merchant_type = Enumerate().CleanNumber(self.Selenium.ExtractElementText(''.join([sub_root_xpath, "/a/div/div[2]/div[2]/div/span"])))
                if self.Merchant.merchant_type != "Official Store":
                    Selenium.max_try_count = 1
                    self.Search.product_review_count_total = Enumerate().CleanNumber(self.Selenium.ExtractElementText(''.join([sub_root_xpath, "/a/div/div[2]/div[3]/div/span[2]"])))
                    self.Selenium.ResetParameters("max_try_count")
                self.Search.product_html_path = Enumerate().CleanNumber(self.Selenium.ExtractElementAttribute("href", ''.join([sub_root_xpath, "/a"])))
                self.MySQL.Insert(self.Search)
        self.Selenium.ResetParameters()

    def ExtractShopeeSearchProducts(self, sub_root_xpath, subsub_root_xpath):
        self.Selenium.sleep_time = 0.5
        self.Search.product_name = self.Selenium.ExtractElementText([''.join([subsub_root_xpath, "/div[1]/div"]), ''.join([subsub_root_xpath, "/div[1]"])])
        self.Selenium.sleep_time = 1
        self.Search.product_price = Enumerate().CleanNumber(self.Selenium.ExtractElementText([''.join([subsub_root_xpath, "/div[2]/div/span[2]"]), ''.join([subsub_root_xpath, "/div[2]/div[2]"])]))
        if self.Search.product_price is not None:
            if " - " in self.Search.product_price:
                self.Search.product_price = self.Search.product_price.split(" - ")[0]
        self.Selenium.sleep_time = 0.5
        self.Search.product_wishlist = self.Selenium.ExtractElementText(''.join([subsub_root_xpath, "/div[4]/div/div"]))
        if self.Search.product_wishlist == "":
            self.Search.product_wishlist = 0
        self.Search.product_review_count_total = Enumerate().CleanNumber(
            self.Selenium.ExtractElementText(''.join([subsub_root_xpath, "/div[4]/div/div[3]/span"])))
        if self.Search.product_review_count_total == 'Belum ada penilaian':
            self.Search.product_review_count_total = 0
        self.Search.product_delivery_promo = self.Selenium.ExtractElementAttribute("class", ''.join([subsub_root_xpath, "/div[2]/div[2]/svg"]))
        self.Search.product_html_path = self.Selenium.ExtractElementAttribute('href', sub_root_xpath)
        self.MySQL.Insert(self.Search)

    def CrawlShopeeSearch(self):

        self.Search.product_page = 1
        word_separator = "%20"
        self.Selenium.link = "https://shopee.co.id/search?keyword="
        self.Selenium.Load(''.join([self.Selenium.link, Concatenate().InfuseSeparator(main=self.RunningLog.search_input, separator=word_separator)]))
        self.Search.product_ordinal = 0
        self.Search.product_page = 0
        highest_page = int(self.Selenium.ExtractElementText("//*[contains(@class, 'shopee-mini-page-controller__total')]"))
        self.Selenium.root_xpath = "//div[contains(@class, 'shopee-search-item-result')]/div/div[2]/div"
        while (self.Search.product_page < self.RunningLog.crawl_max_page or self.RunningLog.crawl_max_page == 0) and self.Search.product_page < highest_page:
            self.Search.product_page += 1
            self.Search.element_ordinal = 0
            if self.Search.product_page != 1:
                self.Selenium.Load(''.join([self.Selenium.link, "&page=", str(self.Search.product_page), "&sortBy=relevancy"]))
            self.Selenium.sleep_time = 2
            merchant_product_elements_count = len(self.Selenium.ExtractElements(self.Selenium.root_xpath))
            while self.Search.element_ordinal < merchant_product_elements_count and (self.Search.element_ordinal < self.RunningLog.crawl_max_ordinal or self.RunningLog.crawl_max_ordinal == 0):
                self.Search.element_ordinal += 1
                self.Search.product_ordinal += 1
                sub_root_xpath = ''.join([self.Selenium.root_xpath, "[", str(self.Search.element_ordinal), "]/div/a"])
                subsub_root_xpath = ''.join([self.Selenium.root_xpath, "[", str(self.Search.element_ordinal), "]/div/a/div/div[2]"])
                self.Search.product_type = "Normal"
                self.ExtractShopeeSearchProducts(sub_root_xpath, subsub_root_xpath)

    def CrawlShopeeProduct(self):
        self.Selenium.sleep_time = 1
        self.Product.product_tree = self.Selenium.ExtractElementsToSeparatedText(separator=" > ", xpath="//div[contains(@class, 'flex items-center _1z1CEl page-product__breadcrumb')]/a")
        self.Selenium.max_try_count = 1
        self.Product.merchant_type = self.Selenium.ExtractElementText("//div[contains(@class, 'horizontal-badge shopee-preferred-seller-badge horizontal-badge--no-triangle _1hOh3l _1lhNV3 items-center')]")
        self.Selenium.ResetParameters("max_try_count")
        if self.Product.merchant_type == None:
            self.Product.merchant_type = "Normal"
        self.Product.product_name = self.Selenium.ExtractElementText("//div[contains(@class, 'qaNIZv')]")
        self.Product.product_rating_value = self.Selenium.ExtractElementText("//div[contains(@class, '_3Oj5_n _2z6cUg')]")
        self.Product.product_review_count_total = Enumerate().CleanNumber(self.Selenium.ExtractElementText("//div[contains(@class, 'flex _32fuIU')]/div[2]/div"))
        if self.Product.product_review_count_total == 'Belum ada penilaian':
            self.Product.product_review_count_total = 0
        self.Product.product_qty_sold = self.Selenium.ExtractElementText("//div[contains(@class, 'flex SbDIui')]/div")
        self.Product.product_price = Enumerate().CleanNumber(self.Selenium.ExtractElementAttribute("//div[contains(@class, '_3n5NQx')]"))
        if self.Product.product_price is not None:
            if " - " in self.Product.product_price:
                self.Product.product_price = self.Product.product_price.split(" - ")[0]
        self.Selenium.max_try_count = 1
        self.Product.product_delivery_promo = self.Selenium.ExtractElementText("//div[contains(@class, '_5y6zF4')]")
        self.Selenium.ResetParameters("max_try_count")
        self.Product.product_available_stock = Manipulate().RemoveParts(["tersisa", "buah"], self.Selenium.ExtractElementText("//div[contains(@class, 'flex _3dRJGI _3a2wD-')]/div/div/div[2]/div[2]"))
        self.Product.product_wishlist = Manipulate().RemoveParts(["Favorite (", ")"], self.Selenium.ExtractElementText("//div[contains(@class, 'flex items-center _25DJo1')]/div"))
        self.Selenium.sleep_time = 1
        self.Product.merchant_name = self.Selenium.ExtractElementText("//*[contains(@class, '_3Lybjn')]")
        self.Product.merchant_last_online = self.Selenium.ExtractElementText("//div[contains(@class, '_1h7HJr')]")
        self.Product.merchant_reputation_score = self.Selenium.ExtractElementText("//div[contains(@class, '_3mK1I2')]/div/div/span")
        self.Product.merchant_total_active_products = self.Selenium.ExtractElementText("//div[contains(@class, '_3mK1I2')]/div/a/span")
        self.Product.merchant_chat_replied_percent = Enumerate().CleanNumber(self.Selenium.ExtractElementText("//div[contains(@class, '_3mK1I2')]/div[2]/div/span"))
        self.Product.merchant_chat_replied_average_time = self.Selenium.ExtractElementText("//div[contains(@class, '_3mK1I2')]/div[2]/div[2]/span")
        self.Product.merchant_open_since = self.Selenium.ExtractElementText("//div[contains(@class, '_3mK1I2')]/div[3]/div/span")
        self.Product.merchant_followers = self.Selenium.ExtractElementText("//div[contains(@class, '_3mK1I2')]/div[3]/div[2]/span")
        self.Product.product_specifications = self.Selenium.ExtractElementText("//div[contains(@class, 'product-detail page-product__detail')]/div[1]/div[2]")
        self.Product.product_description = self.Selenium.ExtractElementText("//div[contains(@class, 'product-detail page-product__detail')]/div[2]/div[2]")
        self.Product.product_review_count_5 = Manipulate().RemoveParts("5 Bintang", Enumerate().CleanNumber(self.Selenium.ExtractElementText("//div[contains(@class, 'product-rating-overview__filters')]/div[2]")))
        if self.Product.product_review_count_5 is not None:
            self.Product.product_review_count_4 = Manipulate().RemoveParts("4 Bintang", Enumerate().CleanNumber(self.Selenium.ExtractElementText("//div[contains(@class, 'product-rating-overview__filters')]/div[3]")))
            self.Product.product_review_count_3 = Manipulate().RemoveParts("3 Bintang", Enumerate().CleanNumber(self.Selenium.ExtractElementText("//div[contains(@class, 'product-rating-overview__filters')]/div[4]")))
            self.Product.product_review_count_2 = Manipulate().RemoveParts("2 Bintang", Enumerate().CleanNumber(self.Selenium.ExtractElementText("//div[contains(@class, 'product-rating-overview__filters')]/div[5]")))
            self.Product.product_review_count_1 = Manipulate().RemoveParts("1 Bintang", Enumerate().CleanNumber(self.Selenium.ExtractElementText("//div[contains(@class, 'product-rating-overview__filters')]/div[6]")))
            self.Product.product_discussion_count = Manipulate().RemoveParts("Dengan Komentar", Enumerate().CleanNumber(self.Selenium.ExtractElementText("//div[contains(@class, 'product-rating-overview__filters')]/div[7]")))
        self.Product.mercant_html_path = self.Selenium.ExtractElementAttribute("href", "//a[contains(@class, 'btn btn-light btn--s btn--inline btn-light--link Ed2lAD')]")
        self.MySQL.Insert(self.Product)
        self.Selenium.ResetParameters()

    def CrawlShopeeMerchant(self):

        self.Merchant.merchant_type = self.Selenium.ExtractElementText("//div[contains(@class, 'horizontal-badge shopee-preferred-seller-badge horizontal-badge--no-triangle')]")
        if self.Merchant.merchant_type is None:
            self.Merchant.merchant_type = "Normal"
        self.Merchant.merchant_name = self.Selenium.ExtractElementText("//h1[contains(@class, 'section-seller-overview-horizontal__portrait-name')]")
        self.Merchant.merchant_last_online = self.Selenium.ExtractElementText("//div[contains(@class, 'section-seller-overview-horizontal__active-time')]")
        self.Selenium.root_xpath = "//div[contains(@class, 'section-seller-overview-horizontal__seller-info-list')]/div"
        self.Selenium.sleep_time = 2
        merchant_shopee_box_elements_count = len(self.Selenium.ExtractElements(self.Selenium.root_xpath))
        self.Selenium.ResetParameters("sleep_time")
        self.Merchant.merchant_elements_ordinal = 0
        while self.Merchant.merchant_elements_ordinal < merchant_shopee_box_elements_count:
            self.Merchant.merchant_elements_ordinal += 1
            sub_root_xpath = ''.join([self.Selenium.root_xpath, "[" + str(self.Merchant.merchant_elements_ordinal), "]"])
            merchant_element_extract = self.Selenium.ExtractElementText(sub_root_xpath)
            if merchant_element_extract is not None:
                merchant_element_extract = merchant_element_extract.split(": ")
                if "Produk" in merchant_element_extract:
                    self.Merchant.merchant_total_active_products = merchant_element_extract[1]
                if "Waktu Pengemasan" in merchant_element_extract:
                    self.Merchant.merchant_packing_duration = merchant_element_extract[1]
                if "Mengikuti" in merchant_element_extract:
                    self.Merchant.merchant_following = merchant_element_extract[1]
                if "Performa Chat" in merchant_element_extract:
                    self.Merchant.merchant_chat_replied_percent = merchant_element_extract[1].replace("% (hitungan Jam)", "")
                if "Pengikut" in merchant_element_extract:
                    self.Merchant.merchant_followers = merchant_element_extract[1]
                if "Penilaian" in merchant_element_extract:
                    merchant_score = merchant_element_extract[1].split(" (")
                    self.Merchant.merchant_reputation_score = merchant_score[0]
                    self.Merchant.merchant_product_quality_score = merchant_score[1].replace(" Penilaian)", "")
                if "Bergabung" in merchant_element_extract:
                    self.Merchant.merchant_open_since = merchant_element_extract[1]
                if "Tingkat Pembatalan" in merchant_element_extract:
                    self.Merchant.merchant_drop_rate = merchant_element_extract[1].replace("%", "")
        self.Merchant.merchant_slogan_long = self.Selenium.ExtractElementText("//div[contains(@class, 'shop-page-shop-description')]/span")
        self.MySQL.Insert(self.Merchant)
        self.Selenium.ResetParameters()

    def CrawlShopeeMerchantSearch(self):

        self.Search.product_page = 0
        self.Search.product_ordinal = 0
        keep_trying_next_page = "YES"
        self.Selenium.root_xpath = "//div[contains(@class, 'shop-search-result-view')]/div/div"
        self.Selenium.sleep_time = 2
        while keep_trying_next_page == "YES":
            self.Search.product_page += 1
            try_fail_max = 2
            for try_fail_count in range(0, try_fail_max):
                merchant_product_elements_count = self.Selenium.ExtractElements()
                if merchant_product_elements_count is not None:
                    merchant_product_elements_count = len(merchant_product_elements_count)
                    if merchant_product_elements_count != 0:
                        break
                    elif merchant_product_elements_count == 0:
                        if try_fail_count >= (try_fail_max - 1):
                            self.keep_trying_next_page = "NO"
                        elif try_fail_count < (try_fail_max - 1):
                            time.sleep(2)
            self.Search.element_ordinal = 0
            while self.Search.element_ordinal < merchant_product_elements_count and keep_trying_next_page == "YES":
                self.Search.element_ordinal += 1
                self.Search.product_ordinal += 1
                sub_root_xpath = ''.join([self.Selenium.root_xpath, "[", str(self.Search.element_ordinal), "]/div/a"])
                self.Search.product_type = "From Merchant Page"
                self.ExtractShopeeSearchProducts(sub_root_xpath, subsub_root_xpath)


    def CrawlProducts(self, Searches):
        for Search in Searches:
            self.Search = Search
            product_html_path_list = []
            self.Product = self.Ecommerce_product()
            self.Product.running_ID = self.RunningLog.running_ID
            self.Product.product_html_path = self.Search.product_html_path
            self.Product.merchant_html_path = self.Search.merchant_html_path
            if self.Product.product_html_path not in product_html_path_list:
                product_html_path_list.append(self.Product.product_html_path)
                self.Selenium.Load(self.Product.product_html_path)
                if self.RunningLog.platform_source == "Tokopedia":
                    self.CrawlTokopediaProduct()
                elif self.RunningLog.platform_source == "Shopee":
                    self.CrawlShopeeProduct()

    def CrawlMerchants(self, Searches):
        for Search in Searches:
            self.Search = Search
            merchant_html_path_list = []
            self.Merchant = self.Ecommerce_merchant()
            self.Merchant.running_ID = self.RunningLog.running_ID
            if self.RunningLog.platform_source == "Tokopedia":
                self.Merchant.merchant_html_path = self.Search.merchant_html_path
            elif self.RunningLog.platform_source == "Shopee":
                self.Merchant.merchant_html_path = self.Product.merchant_html_path
            if self.Merchant.merchant_html_path not in merchant_html_path_list:
                merchant_html_path_list.append(self.Merchant.merchant_html_path)
                self.Selenium.Load(self.Product.merchant_html_path)
                if self.RunningLog.platform_source == "Tokopedia":
                    self.CrawlTokopediaMerchant()
                elif self.RunningLog.platform_source == "Shopee":
                    self.CrawlShopeeMerchant()

    def Main(self):

        try:
            self.RunningLog = self.MySQL.Session.query(self.Ecommerce_running_log).filter(self.Ecommerce_running_log.running_status == "QUEUEING").first()
            self.RunningLog.running_status = "RUNNING"
            if self.RunningLog.title_or_description_required_words is None:
                self.RunningLog.title_or_description_required_words = self.RunningLog.search_input
            self.MySQL.Session.commit()
            self.Selenium = Selenium()
            if self.RunningLog.crawl_source_type == "product-to-merchants":
                if self.RunningLog.crawl_search is True:
                    self.Search = self.Ecommerce_search()
                    self.Search.running_ID = self.RunningLog.running_ID
                    if self.RunningLog.platform_source == "Tokopedia":
                        self.CrawlTokopediaSearch()
                    elif self.RunningLog.platform_source == "Shopee":
                        self.CrawlShopeeSearch()
                if self.RunningLog.crawl_product is True or self.RunningLog.crawl_merchant is True:
                    Searches = self.MySQL.Session.query(self.Ecommerce_search).filter(self.Ecommerce_search.running_ID == self.RunningLog.running_ID).all()
                    if self.RunningLog.crawl_product is True:
                        self.CrawlProducts(Searches)
                    if self.RunningLog.crawl_merchant is True:
                        self.CrawlMerchants(Searches)
            elif self.RunningLog.crawl_source_type == "merchants-to-products":
                if self.RunningLog.crawl_merchant is True:
                    self.Merchant = self.Ecommerce_merchant()
                    if self.RunningLog.platform_source == "Tokopedia":
                        self.Merchant.merchant_html_path = ''.join(["https://www.tokopedia.com/", self.RunningLog.search_input])
                        self.CrawlTokopediaMerchant()
                    if self.RunningLog.platform_source == "Shopee":
                        self.Merchant.merchant_html_path = ''.join(["https://shopee.co.id/", self.RunningLog.search_input])
                        self.CrawlShopeeMerchant()
                if self.Search.crawl_search is True:
                    if self.Selenium.link != self.Merchant.merchant_html_path:
                        self.Selenium.Load(self.Merchant.merchant_html_path)
                    if self.RunningLog.platform_source == "Tokopedia":
                        self.CrawlTokopediaMerchantSearch()
                    elif self.RunningLog.platform_source == "Shopee":
                        self.CrawlShopeeMerchantSearch()
                if self.RunningLog.crawl_product is True:
                    Searches = self.MySQL.Session.query(self.Ecommerce_search).filter(self.Ecommerce_search.running_ID == self.RunningLog.running_ID).all()
                    self.CrawlProducts(Searches)
            self.RunningLog.running_status = "DONE"
            self.MySQL.Session.commit()
            self.MySQL.Session.close()
            self.Selenium.Close()
        except Exception as e:
            print(traceback.format_exc())
            self.RunningLog.running_status = "ERROR"
            self.MySQL.Session.commit()
            self.MySQL.Session.close()
            time.sleep(500) # For debugging purposes
            self.Selenium.Close()

    def Create(self):

        self.MySQL.Base.metadata.create_all(bind=self.MySQL.AlchemyEngine)

    def CreateDummies(self):

        Login = self.Ecommerce_login()
        Login.username = "blembong"
        Login.password = "RagnarTargaryen"
        self.MySQL.Insert(Login)
        RunningLog = self.Ecommerce_running_log()
        RunningLog.user_ID = 1
        RunningLog.platform_source = "Tokopedia"
        RunningLog.crawl_source_type = "product-to-merchants"
        RunningLog.crawl_max_ordinal = 3
        RunningLog.crawl_max_page = 1
        RunningLog.search_input = "tolak angin"
        RunningLog.running_status = "QUEUEING"
        RunningLog.record_creation_datetime = datetime.now()
        self.MySQL.Insert(RunningLog)


#Run().Create()
Run().CreateDummies()
Run().Main()
