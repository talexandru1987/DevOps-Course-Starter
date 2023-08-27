from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_task_journey(driver, app_with_temp_board):
    driver.get("http://localhost:5000/")

    assert driver.title == "To-Do App"


def test_navigate_to_board(driver, app_with_temp_board):
    try:
        driver.get("http://localhost:5000/")
        wait = WebDriverWait(driver, 10)
        print("after element not found")
        dropDawn = wait.until(EC.element_to_be_clickable((By.ID, "dropdownMenuButton")))
        dropDawn.click()
        dropDawnElement = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "dropdown"))
        ).find_element(By.CLASS_NAME, "dropdown-item")

        dropDawnElement.click()
        addItemForm = wait.until(EC.element_to_be_clickable((By.ID, "newItem")))

    except Exception as e:
        print(f"An exception occured {e}")
    assert addItemForm is not None
