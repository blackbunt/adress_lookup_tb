# Address_Ally

_"Address_Ally - Where speed meets accuracy."_

AddressAlly is a Python script that allows users to swiftly and accurately search for addresses. Simply enter a rough street name and the program searches for this address, starting from a specified origin point. It then displays this address in DIN 5008 format. Users can then have the full address, or parts of it, copied to the clipboard.

## Getting Started

For Python enthusiasts, this project requires Python 3 to run. After installing Python, download the script and execute it in your console:

```bash
python3 address_ally.py
```

Additionally, you will need to install a few Python packages:

- pyperclip
- geopy
- opencage

You can install the necessary packages using pip:

```bash
pip install -r requirements.txt
```
You can find the requirements.txt in the project root.

For Windows users, I provide ready-to-use releases in .exe format. No installation is necessary for these releases. You can download the latest release here.

## Usage

Execute the script in your console and follow the instructions on the screen:

```bash
python3 address_ally.py
```

After executing the script, you will be prompted to enter an address. The script will then search for the address and display it in DIN 5008 format.
