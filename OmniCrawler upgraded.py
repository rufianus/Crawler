
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from DataStructure.StringManipulator import Enumerate, Manipulate
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import os


class Selenium:
    
    sleep_time_default = 0.1
    max_try_count_default = 2
    sleep_time = sleep_time_default
    max_try_count = max_try_count_default
    xpath = None
    link = None
    record_triggers = True
    debug_level = 2
    triggers_list = []
    element = None
    elements = None
    elements_count = None
    extract = None

    def __init__(self, extension_directory_path=None, operating_system="windows", implicitly_wait=5):

        if operating_system == "linux":
            chrome_driver_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "chromedriver")
        elif operating_system == "windows":
            chrome_driver_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "chromedriver.exe")

        if extension_directory_path is not None:
            chrome_options = Options()
            chrome_options.add_argument(''.join(["--load-extension=", '"', extension_directory_path, '"']))
            self.Driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=chrome_options)

        elif extension_directory_path is None:
            self.Driver = webdriver.Chrome(executable_path=chrome_driver_path)

        self.Driver.set_window_size(2500, 15000)
        self.Driver.implicitly_wait(implicitly_wait)


    def Close(self):

        self.Driver.close()


    def ResetParameter(self, parameter):

        if parameter == "sleep_time" or parameter is None:
            self.sleep_time = self.sleep_time_default
        if parameter == "max_try_count" or parameter is None:
            self.max_try_count = self.max_try_count_default
        if parameter == "link" or parameter is None:
            self.link = None
        if parameter == "triggers_list" or parameter is None:
            self.triggers_list = []
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

    def Load(self, link=None, reset_triggers=True):

        if link is not None:
            self.link = link
        if self.debug_level >= 2:
            print("Loading:", self.link)
        self.Driver.get(self.link)
        time.sleep(self.sleep_time)
        if reset_triggers is True:
            self.ResetParameters("triggers_list")

    def ErrorHandling(self, e, try_count):

        if self.debug_level >= 1:
            print(str(e))
        if self.max_try_count - try_count != 1:  # Prevents unnecessary refresh at last try count
            sleep_time_temp = self.sleep_time * (try_count + 1)
            if self.debug_level >= 2:
                print("Error sleep time:", sleep_time_temp)
            self.Load(self.link, reset_triggers=False)
            time.sleep(sleep_time_temp)
            if self.debug_level >= 2:
                print("Re-triggers:", self.triggers_list)
            for trigger in self.triggers_list:
                if isinstance(trigger, list):
                    if trigger[0] == "hover_element":
                        self.HoverElement(trigger[1], reserve=False)
                    if trigger[0] == "hover_path":
                        self.HoverPath(trigger[1], reserve=False)
                    if trigger[0] == "click_element":
                        self.ClickElement(trigger[1], reserve=False)
                    if trigger[0] == "click_path":
                        self.ClickPath(trigger[1], reserve=False)
                    if trigger[0] == "insert_element":
                        self.InsertElement(trigger[1], element=trigger[2], clear=trigger[3], reserve=False)
                    if trigger[0] == "insert_path":
                        self.InsertPath(trigger[1], xpath=trigger[2], clear=trigger[3], reserve=False)
                    if trigger[0] == "input_element":
                        self.InputElement(trigger[1], element=trigger[2], clear=trigger[3], reserve=False)
                    if trigger[0] == "input_path":
                        self.InputPath(trigger[1], xpath=trigger[2], clear=trigger[3], reserve=False)
                    if trigger[0] == "clear_element":
                        self.ClearElement(trigger[1], reserve=False)
                time.sleep(sleep_time_temp)

    def ExtractElementProcess(self):

        for try_count in range(0, self.max_try_count):
            try:
                self.element = self.Driver.find_element_by_xpath(self.xpath)
                if self.debug_level >= 2:
                    print("Extracted element:", self.xpath)
                break
            except Exception as e:
                self.ErrorHandling(e, try_count)

    def ExtractElement(self, xpath=None):

        self.element = None
        self.extract = None
        if isinstance(xpath, list): # xpath in list used for trying multiple xpath for changing xpaths
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
                if self.debug_level >= 2:
                    print("Extracted", str(self.elements_count), "elements:", self.xpath)
                break
            elif self.elements_count == 0:
                e = "Possible error: elements_count is 0"
                self.ErrorHandling(e, try_count)

    def ExtractElements(self, xpath=None, return_type=None):

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

    def HoverElement(self, element=None, reserve=True):

        if element is not None:
            self.element = element
        for try_count in range(0, self.max_try_count):
            try:
                if self.element is not None:
                    ActionChains(self.Driver).move_to_element(self.element).perform()
                    if reserve is True and self.record_triggers is True:
                        self.triggers_list.append(["hover_element", self.element])
                    time.sleep(self.sleep_time)
                    break
            except Exception as e:
                self.ErrorHandling(e, try_count)

    def HoverPath(self, hover_xpath, reserve=True):

        self.ExtractElement(hover_xpath)
        self.HoverElement(reserve=False)
        if reserve is True and self.record_triggers is True:
            self.triggers_list.append(["hover_path", hover_xpath])

    def ClickElement(self, element=None, reserve=True):

        if element is not None:
            self.element = element
        for try_count in range(0, self.max_try_count):
            try:
                if self.element is not None:
                    self.element.click()
                    if reserve is True and self.record_triggers is True:
                        self.triggers_list.append(["click_element", self.element])
                    time.sleep(self.sleep_time)
                    break
            except Exception as e:
                self.ErrorHandling(e, try_count)

    def ClickPath(self, click_xpath, reserve=True):

        self.ExtractElement(click_xpath)
        self.ClickElement(reserve=False)
        if reserve is True and self.record_triggers is True:
            self.triggers_list.append(["click_path", click_xpath])

    def ClearElement(self, element, reserve=True):

        if element is not None:
            self.element = element
        for try_count in range(0, self.max_try_count):
            try:
                self.element.send_keys(Keys.CONTROL + "a")
                self.element.send_keys(Keys.DELETE)
                if reserve is True and self.record_triggers is True:
                    self.triggers_list.append(["clear_element", self.element])
                break
            except Exception as e:
                self.ErrorHandling(e, try_count)

    def InsertElement(self, text, element=None, reserve=True, clear=True):

        if element is not None:
            self.element = element
        if clear is True:
            self.ClearElement(self.element)
        self.element.send_keys(text)
        if reserve is True and self.record_triggers is True:
            self.triggers_list.append(["insert_element", text, self.element, clear])
        time.sleep(self.sleep_time)

    def InsertPath(self, text, xpath=None, reserve=True, clear=True):
        
        if xpath is not None:
            self.xpath = xpath
        self.ExtractElement(self.xpath)
        self.InsertElement(text, reserve=False, clear=clear)
        if reserve is True and self.record_triggers is True:
            self.triggers_list.append(["insert_path", text, self.xpath, clear])

    def InputElement(self, text, element=None, reserve=True, clear=True):
        
        if element is not None:
            self.element = element
        self.InsertElement(text, element=self.element, reserve=False, clear=clear)
        element.send_keys(Keys.ENTER)
        if reserve is True and self.record_triggers is True:
            self.triggers_list.append(["input_element", text, self.element, clear])

    def InputPath(self, text, xpath=None, reserve=True, clear=True):
        
        if xpath is not None:
            self.xpath = xpath
        self.ExtractElement(self.xpath)
        self.InputElement(text, reserve=False, clear=clear)
        if reserve is True and self.record_triggers is True:
            self.triggers_list.append(["input_path", text, self.xpath, clear])

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
        if self.debug_level >= 2:
            print("Extracted text:", self.extract)
        return self.extract


    def ExtractAttribute(self, attribute, element=None):

        if element is not None:
            self.element = element
        if self.element is not None:
            self.extract = self.element.get_attribute(attribute)
        if self.debug_level >= 2:
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
