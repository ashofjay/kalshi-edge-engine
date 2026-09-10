from kalshi_edge_engine.strategy import normalize_market, detect_two_leg_candidate

def test_detects_candidate():
    m = {"yes_ask": 0.46, "no_ask": 0.49}
    s = detect_two_leg_candidate(m, 3)
    assert s is not None
    assert abs(s["estimated_margin"] - 0.02) < 1e-9

def test_rejects_no_margin():
    m = {"yes_ask": 0.50, "no_ask": 0.50}
    assert detect_two_leg_candidate(m, 3) is None

def test_dollar_fields():
    raw = {
        "ticker": "TEST",
        "yes_ask_dollars": "0.5100",
        "no_ask_dollars": "0.5200",
        "volume_fp": "12.00",
    }
    m = normalize_market(raw)
    assert m["yes_ask"] == 0.51
    assert m["no_ask"] == 0.52
    assert m["volume"] == 12.0
