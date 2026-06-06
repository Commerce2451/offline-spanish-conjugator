# Offline Spanish Conjugator

A fully offline Spanish verb conjugator built with Python and Flask.

## Features

- Offline operation
- Regular verb conjugation
- Common irregular verb overrides
- English definitions
- Example sentences
- Dark mode
- Linux, Windows, and macOS support

  # Offline Spanish Conjugator

<img src="[https://raw.githubusercontent.com/Commerce2451/offline-spanish-conjugator/refs/heads/main/Screenshot%20from%202026-06-06%2008-00-48.png]" alt="Screenshot" />

## Known Limitations

- Uses mlconjug3 as the primary conjugation engine.
- Some irregular verbs are manually overridden.
- Additional irregular verb coverage is planned.

## Installation

## Linux Mint / Ubuntu

Clone the repository:

```bash
git clone https://github.com/Commerce2451/offline-spanish-conjugator.git
cd offline-spanish-conjugator
```

Create a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Launch the application:

```bash
python3 app.py
```

Your default browser should automatically open to:

```text
http://127.0.0.1:5000
```

## Requirements

* Python 3.10+
* Flask
* mlconjug3

## Tested On

* Linux Mint 22
* Python 3.10+

## Stop the Application

Press:

```text
Ctrl + C
```

in the terminal running the application.


