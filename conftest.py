import pytest
from playwright.sync_api import sync_playwright

URL = "https://www.bwin.com/en/sports/live/betting"

def pytest_addoption(parser):
    parser.addoption(
        "--device",
        action="store",
        default=None,
        help="desktop or mobile (omit for auto by markers)",
    )

def pytest_runtest_setup(item):
    device = getattr(item.config.option, "device", None)
    markers = {m.name for m in item.iter_markers()}

    if device == "desktop" and "mobile" in markers:
        pytest.skip("This test requires mobile")
    if device == "mobile" and "desktop" in markers:
        pytest.skip("This test requires desktop")

@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright):
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def context(request, browser, playwright):
    cli_device = getattr(request.config.option, "device", None)
    markers = {m.name for m in request.node.iter_markers()}

    if cli_device in ("desktop", "mobile"):
        device = cli_device
    else:
        device = "mobile" if "mobile" in markers else "desktop"

    if device == "mobile":
        iphone = playwright.devices["iPhone 13 Pro"]
        ctx = browser.new_context(**iphone)
    else:
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    yield ctx
    ctx.close()

@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    page.set_default_timeout(10_000)
    page.goto(URL)
    return page