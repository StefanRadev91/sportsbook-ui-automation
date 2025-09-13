import pytest
from components.az_sports_panel import AZSportsPanel
from pages.live_page import LivePage
from pages.event_view_page import EventViewPage
from components.betslip import BetSlip

@pytest.mark.mobile
def test_check_sport_sorting_tennis_mobile(page):
    az = AZSportsPanel(page)
    az.go_to_tennis()

    live = LivePage(page)
    live.wait_until_ready()

    assert "/sports/tennis-5" in page.url, "URL does not indicate Tennis"
    assert "tennis" in live.sport_header.inner_text().lower(), "Header does not indicate Tennis"

@pytest.mark.mobile
def test_add_pick_appears_in_betslip_mobile(page):
    az = AZSportsPanel(page)
    az.go_to_tennis()

    live = LivePage(page)
    live.wait_until_ready()
    live.open_event_by_index(index=2, skip_suspended=True)

    event = EventViewPage(page)
    event.wait_until_loaded()
    event.pick_first()

    slip = BetSlip(page)
    slip.open()                    
    slip.wait_until_badge_count(1)   
    assert slip.has_pick("Match Winner")

@pytest.mark.mobile
def test_live_odds_update_in_event_view_mobile(page):
    az = AZSportsPanel(page)
    az.go_to_tennis()

    live = LivePage(page)
    live.wait_until_ready()
    live.open_event_by_index(index=3, skip_suspended=True)

    event = EventViewPage(page)
    event.wait_until_loaded()

    data = event.wait_for_match_winner_odds_update()

    old_text, new_text = data["old_text"], data["new_text"]
    old_val, new_val = data["old_value"], data["new_value"]
    direction = data["direction"]   

    assert old_text != new_text, "Odds text did not change"

    if old_val is not None and new_val is not None:
        assert old_val != new_val, f"Odds value did not change (still {old_val})"

        if direction == "up":
            assert new_val > old_val, f"Direction 'up' but {old_val} → {new_val} is not increasing"
        elif direction == "down":
            assert new_val < old_val, f"Direction 'down' but {old_val} → {new_val} is not decreasing"

    assert direction in (None, "up", "down")