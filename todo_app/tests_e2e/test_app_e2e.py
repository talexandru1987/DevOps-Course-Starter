from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pytest

def test_task_journey(driver, app_with_temp_board):
    driver.get("http://localhost:5000/")

    assert driver.title == "To-Do App"



def test_navigate_to_board(driver, app_with_temp_board):
    driver.get("http://localhost:5000/")
    wait = WebDriverWait(driver, 10)

    
    try:
        # Wait for the details summary to be clickable and click it to reveal the link
        details_summary = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "summary")))
        details_summary.click()
        
        # Wait for the link inside the details to be clickable and click it
        board_link = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "a")))
        board_link.click()
        
        # Wait for the browser to navigate and the new page to load
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")

        # # Wait for the "newItem" element to be visible on the new page
        newItemElement = wait.until(EC.visibility_of_element_located((By.ID, "newItem")))

    except Exception as e:
        print(f"An exception occurred: {e}")
        pytest.fail(f"Test failed due to an exception: {e}")

    # # Assert that the newItem element is not None and thus present and visible
    assert newItemElement is not None, "newItem element not found on the page after navigation."



