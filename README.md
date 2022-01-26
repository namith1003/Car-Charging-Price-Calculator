# FIT2107_S2_2021

## Description of Application

Created a Car Charging Calculator that tells the price to charge your car from a charging station while using 8 different varieties of charging configurations that the user selects and also takes to consideration the weather as the charging station consists of solar panels and takes the weather at the place that the charging is occurring at and the date and time of charging and calculates the total based on the off peak and peak times and whether or not the day is a holiday or a weekend.

## Tests Created 

Tests have been created using multiple different whitebox stategies and have been run through blackbox testing as well and test cases have an 80%+ coverage of the code and 
network related or user input related test data, including weather information and data inputs have been Mocked to allow faster and more efficient test cases.

## Setting up and running the project via the terminal

### Enabling virtualenv
To use virtualenv, you will need to have pip, the Python package installer, already installed on your machine (by default, it should also be installed when you install Python).

1. Windows
    ```
    python3 -m venv env
    .\env\Scripts\activate
    ```

2. Linux/macOS
    ```
    python3 -m venv env
    source env/bin/activate
    ```

    If you are unable to get virtualenv to run, you might need to run the following command first:
    ```
    sudo apt install python3-venv
    ```

### Installing Required Dependencies/Packages
You will need to install project dependencies for the provided code to work. This only needs to be done once.

```
pip install -r requirements.txt
```

### Exiting Virtualenv
Once you are finished working on the project, you can exit virtualenv by running the following command:

```
deactivate
```
