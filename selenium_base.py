import csv
import types

from selenium.webdriver.support.ui import WebDriverWait

from chrome_base import ChromedriverBase
from class_types import List, VectorDict, WebElements
from selenium_utils import ElementHasCssSelector


class SeleniumBase(ChromedriverBase):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        num_methods = len(
            [
                name
                for name, item in SeleniumBase.__dict__.items()
                if isinstance(item, types.FunctionType)
                and name[:2] != "__"
                and name[-2:] != "__"
            ]
        )
        return f"Defines {num_methods-1} utility selenium methods"

    def go_to(self, url: str) -> None:
        """ Navigates to url """
        self.log(f"go to", type=self.REQ, payload=url)
        self.webdriver.get(url)
        self.log(f"go to", type=self.RES, payload=url)

    def go_to_by_href(self, a_tag_selector: str) -> None:
        """ Navigates to url specified by a particular a_tag's href"""
        elements = self.wait_for_elements_by_css_selector(a_tag_selector)
        assert len(elements) == 1
        href = elements[0].get_attribute("href")
        self.go_to(href)

    def wait_for_elements_by_css_selector(
        self, css_selector: str, wait_time: int = 10
    ) -> WebElements:
        """ Waits for a specified DOM element to appear """
        self.log(f"waiting for css selector", type=self.REQ, payload=css_selector)
        elements = WebDriverWait(self.webdriver, wait_time).until(
            ElementHasCssSelector(css_selector)
        )
        self.log(
            f"waiting for css selector",
            type=self.RES,
            payload=f"{len(elements)} elements",
        )
        return elements

    def write_to_csv(
        self, data: VectorDict, columns: List[str], file_name: str
    ) -> None:
        """ Writes data to csv """
        self.log("write to csv", type=self.REQ, payload=file_name)
        with open(self.file_name, "w") as file:
            csvwriter = csv.DictWriter(file, fieldnames=columns)
            csvwriter.writeheader()
            csvwriter.writerows(data)
        self.log("write to csv", type=self.RES, payload=file_name)
