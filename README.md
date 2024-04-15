# Software Development Engineer in Test Take-Home-Test
This project demonstrates a multi-threaded approach to automated web testing using Selenium. It is designed to identify a fake bar among a set of bars by weighing them in different groups. The script utilizes multiple threads to perform simultaneous testing, increasing efficiency and reducing overall test execution time.
## Project Structure
- `main.py`: Contains the main script for initializing the WebDriver, defining test functions, and managing threads.
## Requirements
- Python 3.8+
- Selenium WebDriver
- ChromeDriver (or any other driver compatible with your browser version)

## Setup
1. **Install Python**: Ensure Python 3.8 or higher is installed on your system.
2. **Clone the Repository**: Clone this project to your local machine.
3. **ChromeDriver**: Download the ChromeDriver that matches your Chrome version. Ensure it is placed in your PATH or specify its location directly in the script.
4. **Install selenium**: Run the following command in your terminal to install Selenium
```
pip install selenium
```
## Running the Test
To run the tests, execute the script from your command line:
```
python3 main.py
```