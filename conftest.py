def pytest_addoption(parser):
    parser.addoption("--no-cleanup", action="store_true", default=False,
                     help="Leave directory structure after tests are run.")
