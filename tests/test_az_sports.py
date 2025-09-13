import pytest
from components.az_sports_panel import AZSportsPanel
from pages.live_page import LivePage

@pytest.mark.desktop
@pytest.mark.smoke
def test_check_sport_sorting_tennis(page):
    
    az = AZSportsPanel(page)
    az.open()
    az.go_to_tennis()

    live = LivePage(page)
    live.wait_until_ready()
    assert "/sports/tennis-5" in page.url, "URL does not indicate Tennis"
    assert "tennis" in live.sport_header.inner_text().lower(), "Header does not indicate Tennis"
    assert live.is_tab_active("Tennis"), "Tennis tab is not highlighted"