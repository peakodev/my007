# Agent Address Book

This application give you ability to use prepared classes for making Agent Address Book with ability to manipulate with rows of book

## Features

- Add name of person
- Add birthday
- Add list of phones to person
- Get person by query (searching in names and phones)
- Simple iterator for Address Book
- Paginated iterator for Address Book

## Requirements

- Python 3.x

## Installation

To install this application, you'll need Python and `pipenv` installed on your machine. If you don't have `pipenv` installed, you can install it with pip:

```bash
pip install --user pipenv
```

### Steps to Install the Application

1. Clone the repository or download the source code:

```bash
git clone git@github.com:peakodev/team007.git
cd agent_book
```

2. Install the application and its dependencies using `pipenv`:

```bash
pipenv install
```

This command will create a virtual environment and install all the necessary dependencies within it.

## Usage

If you would like to contribute to the development of this application, please follow these steps:

 - AgentBook
 - Record
 - AgentBookIterator
 - PaginatedAgentBookIterator
 - CustomExceptions
 - DATE_FORMAT

To generate random persons and display it using pagination, please run:

```bash
pipenv run python tests/generate_book.py
```

## Contributing

If you would like to contribute to the development of this application, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.
