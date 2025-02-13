# Google Search Web Scraper

This web scraper uses Python to gather data from Google search results based on a given keyword. The extracted data includes the title, description, and link from each search result.

## Features

*   **Keyword Search:** Enter any keyword you want to search for on Google.
*   **Data Extraction:** Retrieves the title, description, and link from each search result.
*   **CSV Format:** Saves the data in an easily processed CSV format.
*   **Anti-Detection:** Uses `undetected-chromedriver` to avoid detection as a bot.

## How to Use

1.  **Preparation:**
    *   Make sure you have Python installed.
    *   Install the required libraries:

    ```bash
    pip install undetected-chromedriver selenium pandas
    ```

2.  **Run the Scraper:**
    *   Download or clone this repository.
    *   Open a terminal or command prompt.
    *   Navigate to the directory where you saved the code.
    *   Run the Python script:

    ```bash
    python your_script_name.py
    ```

    *   Replace `your_script_name.py` with the name of your Python file.

3.  **Results:**
    *   The collected data will be saved in a CSV file named `scraped_results.csv` in the same directory.

## Configuration

You can change the search keyword within the Python script. Look for the line containing:

```python
keyword = "President Prabowo Subianto"  # Change with your keyword