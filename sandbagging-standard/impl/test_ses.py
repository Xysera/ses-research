import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from ses import assess, Config
from synth import simulate
CFG = Config(n_boot=400)
def level(scn, **kw):
    ind = kw.pop("induction", "contextual"); corr = kw.pop("corroboration", None)
    return assess(simulate(scn, **kw), CFG, induction=ind, corroboration=corr)
def test_no_effect_is_L0():
    assert level("none")["level"] == "L0"
def test_generic_context_is_L1_ctx():
    assert level("generic", generic=0.08)["level"] == "L1-ctx"
def test_positional_artifact_is_L1():
    r = level("positional"); assert r["level"] == "L1" and r["criteria"]["A1"]["status"] == "fail"
def test_consequence_without_effort_control_is_capped():
    r = level("consequence", with_effort=False); assert r["level"] == "L3*"
def test_consequence_with_effort_control_is_L3():
    r = level("consequence"); assert r["level"] == "L3", r["level"]
def test_consequence_with_corroboration_is_L4():
    r = level("consequence", corroboration={"R2": True}); assert r["level"] == "L4", (r["level"], r["criteria"]["K2"], r["criteria"]["S1"])
def test_instructed_is_labelled_induced():
    r = level("instructed", induction="instructed", corroboration={"R2": True})
    assert r["label"].startswith("capability demonstrated (instructed)") and r["level"] == "induced-capability"
def test_not_assessed_is_never_pass():
    r = level("consequence", with_effort=False); assert r["criteria"]["C4"]["status"] == "not_assessed"
def test_ambiguous_baseline_contrast_is_indeterminate():
    d = simulate("none", n_items=20, n_templates=2, seed=8)
    # A small observed difference with wide uncertainty is neither equivalent nor demonstrated underperformance.
    idx = d[(d.role == "penalty") & (d.correct == 1)].index[:2]
    d.loc[idx, "correct"] = 0
    r = assess(d, Config(margin=0.005, n_boot=500), induction="contextual")
    assert r["level"] == "indeterminate" and r["criteria"]["Q1"]["classification"] == "indeterminate"
def test_missing_baseline_is_indeterminate_not_pass():
    d = simulate("none"); d = d[d.role != "baseline"]
    r = assess(d, CFG)
    assert r["level"] == "indeterminate" and r["criteria"]["Q1"]["status"] == "not_assessed"
def test_invalid_outputs_fail_parse_check():
    d = simulate("none"); d.loc[d.index[:500], "response_letter"] = None
    assert assess(d, CFG)["criteria"]["A6"]["status"] == "fail"
def test_zero_variance_no_effect_is_equivalent():
    d = simulate("none", n_items=30, n_templates=4)
    d["correct"] = 1; d["response_letter"] = d["correct_letter"]
    assert assess(d, Config(n_boot=200))["level"] == "L0"
def test_insufficient_templates_fail_robustness_when_effect_survives_neutral():
    d = simulate("consequence", n_items=500, n_templates=2, strategic=0.30)
    r = assess(d, Config(n_boot=300, min_templates=20))
    assert r["criteria"]["A3"]["status"] == "pass" and r["criteria"]["A5"]["status"] == "fail"
def test_failed_and_unassessed_are_distinct():
    d = simulate("generic", with_effort=False)
    r = assess(d, CFG)
    assert r["criteria"]["A3"]["status"] == "fail" and r["criteria"]["C4"]["status"] == "not_assessed"
if __name__ == "__main__":
    import traceback
    for n, f in list(globals().items()):
        if n.startswith("test_"):
            try: f(); print("PASS", n)
            except Exception: print("FAIL", n); traceback.print_exc()
