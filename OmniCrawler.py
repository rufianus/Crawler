
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from DataStructure.StringManipulator import Enumerate, Manipulate
from selenium.webdriver.common.keys import Keys


class Selenium:

    sleep_time_default = 0.1
    max_try_count_default = 2
    sleep_time = sleep_time_default
    max_try_count = max_try_count_default
    xpath = None
    link = None
    trigger_xpaths_list = []
    element = None
    elements = None
    elements_count = None
    extract = None

    def __init__(self, extension_directory_path=None):

        chrome_driver_path = "/home/rufi/Desktop/Selenium/Toraja/chromedriver"

        if extension_directory_path is not None:
            chrome_options = Options()
            chrome_options.add_argument("--load-extension=" + extension_directory_path)
            self.Driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=chrome_options)

        elif extension_directory_path is None:
            self.Driver = webdriver.Chrome(executable_path=chrome_driver_path)

        self.Driver.set_window_size(2500, 15000)


    def Close(self):

        self.Driver.close()


    def ResetParameter(self, parameter):

        if parameter == "sleep_time" or parameter is None:
            self.sleep_time = self.sleep_time_default
        if parameter == "max_try_count" or parameter is None:
            self.max_try_count = self.max_try_count_default
        if parameter == "link" or parameter is None:
            self.link = None
        if parameter == "trigger_xpaths_list" or parameter is None:
            self.trigger_xpaths_list = []
        if parameter == "element" or parameter is None:
            self.element = None
        if parameter == "elements" or parameter is None:
            self.elements = None
        if parameter == "elements count" or parameter is None:
            self.elements = None
        if parameter == "extract" or parameter is None:
            self.extract = None

    def ResetParameters(self, parameters=None):

        if isinstance(parameters, list):
            for parameter in parameters:
                self.ResetParameter(parameter)
        else:
            self.ResetParameter(parameters)


    def Load(self, link=None):

        if link is not None:
            self.link = link
        print("Loading:", self.link)
        self.Driver.get(self.link)
        self.ResetParameters("trigger_xpaths_list")

    def ErrorHandling(self, e, try_count):

        self.element = None
        print(str(e))
        if self.max_try_count - try_count != 1:  # Prevents unneccesary refresh at last try count
            self.Load(self.link)
            time.sleep(self.sleep_time * try_count)
            print("Re-clicks:", self.trigger_xpaths_list)
            for trigger_xpath in self.trigger_xpaths_list:
                self.ClickIt(trigger_xpath, reserve_trigger=False)
                time.sleep(self.sleep_time * try_count)

    def ExtractElementProcess(self):

        for try_count in range(0, self.max_try_count):
            try:
                self.element = self.Driver.find_element_by_xpath(self.xpath)
                print("Extracted element:", self.xpath)
                break
            except Exception as e:
                self.ErrorHandling(e, try_count)

    def ExtractElement(self, xpath=None):

        self.element = None
        self.extract = None
        if isinstance(xpath, list):
            for self.xpath in xpath:
                self.ExtractElementProcess()
                if self.element is not None:
                    return self.element
        elif xpath is not None:
            self.xpath = xpath
            self.ExtractElementProcess()
        return self.element

    def ExtractElementsProcess(self):

        for try_count in range(0, self.max_try_count):
            self.elements = self.Driver.find_elements_by_xpath(self.xpath)
            self.elements_count = len(self.elements)
            if self.elements_count != 0:
                print("Extracted", str(self.elements_count), "elements:", self.xpath)
                break
            elif self.elements_count == 0:
                e = "Possible error: elements_count is 0"
                self.ErrorHandling(e, try_count)

    def ExtractElements(self, xpath=None, return_type = None):

        self.elements = None
        self.extract = None
        self.elements_count = None
        if xpath is not None:
            self.xpath = xpath
        if isinstance(xpath, list):
            for self.xpath in xpath:
                self.ExtractElementsProcess()
                if self.elements_count != 0:
                    if return_type is None:
                        return self.elements
                    elif return_type == "elements_count":
                        return self.elements_count
        elif xpath is not None:
            self.xpath = xpath
            self.ExtractElementsProcess()
        if return_type is None:
            return self.elements
        elif return_type == "elements_count":
            return self.elements_count


    def ClickIt(self, trigger_xpath=None, reserve_trigger=True):

        if trigger_xpath is not None:
            self.trigger_xpath = trigger_xpath
        self.trigger_xpath = trigger_xpath
        for try_count in range(0, self.max_try_count):
            try:
                self.ExtractElement(self.trigger_xpath)
                click_this = self.element
                if click_this is not None:
                    click_this.click()
                    if reserve_trigger is True:
                        self.trigger_xpaths_list.append(self.trigger_xpath)
                    break
            except Exception as e:
                self.ErrorHandling(e, try_count)


    def ExtractElementsToSeparatedText(self, separator=", ", xpath=None):

        if xpath is not None:
            self.xpath = xpath
        self.ExtractElements(self.xpath)
        if self.elements is []:
            self.extract = None
        elif self.elements != [] and self.elements is not None:
            self.extract = []
            for element in self.elements:
                self.element = element
                self.extract.append(self.element.text)
                if separator is not None:
                    self.extract.append(separator)
            self.extract.pop(-1)
            self.extract = ''.join(self.extract)
        return self.extract

    def ExtractElementText(self, xpath=None):

        if xpath is not None:
            self.xpath = xpath
        self.ExtractElement(self.xpath)
        if self.element is not None:
            self.extract = self.element.text
            if self.extract is not None:
                self.extract = Manipulate().RemoveLargeEmos(self.extract)
        print("Extracted text:", self.extract)
        return self.extract


    def ExtractAttribute(self, attribute):

        if self.element is not None:
            self.extract = self.element.get_attribute(attribute)
        print("Extracted attribute:", self.extract)
        return self.extract


    def ExtractElementAttribute(self, attribute, xpath=None):

        if xpath is not None:
            self.xpath = xpath
        self.ExtractElement(self.xpath)
        self.ExtractAttribute(attribute)
        return self.extract


    def ExtractElementToNumber(self, xpath=None):

        if xpath is not None:
            self.xpath = xpath
        self.ExtractElementText(self.xpath)
        self.extract = Enumerate().ReformToNumber(self.extract)
        return self.extract


    def ActivateKeywordsEverywhere(self):

        keywords_everywhere_options_path = "chrome-extension://hbapdpeemoojbophdfndmlgdhppljgmp/html/options.html"
        self.Load(keywords_everywhere_options_path)
        API_key_text_box = self.ExtractElement("//input[contains(@id, 'apiKey')]")
        API_key_text_box.send_keys("3d0ecbbfbba59de3f447")
        API_key_text_box.send_keys(Keys.ENTER)

        self.Load("https://www.google.com/")
        self.Driver.switch_to.window(self.Driver.window_handles[-1])
        self.Driver.close()
        self.Driver.switch_to.window(self.Driver.window_handles[-1])

    def ClearTextBox(self, element):

        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)

    def InsertClearedTextBox(self, element, text):

        self.ClearTextBox(element)
        element.send_keys(text)

    def InputClearedTextBox(self, element, text):

        self.InsertClearedTextBox(element, text)
        element.send_keys(Keys.ENTER)
