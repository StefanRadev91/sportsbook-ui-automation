import pytest
from components.az_sports_panel import AZSportsPanel
from pages.live_page import LivePage
from pages.event_view_page import EventViewPage
from components.betslip import BetSlip

@pytest.mark.desktop
@pytest.mark.smoke
def test_add_pick_appears_in_betslip(page):
    az = AZSportsPanel(page)
    az.open()
    az.go_to_tennis()

    live = LivePage(page)
    live.wait_until_ready()
    live.open_event_by_index(1)

    event = EventViewPage(page)
    event.wait_until_loaded()
    event.pick_first()
    assert event.wait_until_first_selection_highlighted()

    slip = BetSlip(page)
    slip.open()
    slip.wait_until_badge_count(1)
    assert slip.has_any_selection(), "No selections header in BetSlip"
    assert slip.has_pick("Match Winner"), "Pick not visible in BetSlip"