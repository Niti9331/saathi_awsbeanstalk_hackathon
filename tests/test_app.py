import pytest
from application import application, HELPLINES, TRANSLATIONS, SUPPORTED_LANGS

PAGES = ["", "helplines", "calm", "crisis"]


@pytest.fixture
def client():
    return application.test_client()


@pytest.mark.parametrize("lang", SUPPORTED_LANGS)
@pytest.mark.parametrize("page", PAGES)
def test_pages_load(client, lang, page):
    assert client.get(f"/{lang}/{page}").status_code == 200


@pytest.mark.parametrize("lang", SUPPORTED_LANGS)
@pytest.mark.parametrize("page", PAGES)
def test_disclaimer_on_every_page(client, lang, page):
    html = client.get(f"/{lang}/{page}").get_data(as_text=True)
    assert TRANSLATIONS[lang]["disclaimer"] in html


@pytest.mark.parametrize("lang", SUPPORTED_LANGS)
def test_crisis_page_shows_every_number(client, lang):
    html = client.get(f"/{lang}/crisis").get_data(as_text=True)
    for h in HELPLINES:
        assert h["number"] in html


def test_unknown_language_is_404(client):
    assert client.get("/xx/").status_code == 404


def test_health_endpoint(client):
    assert client.get("/health").get_json() == {"status": "ok"}


def test_translation_keys_match_across_languages():
    base = set(TRANSLATIONS["en"])
    for lang in SUPPORTED_LANGS:
        assert set(TRANSLATIONS[lang]) == base, f"{lang} keys differ from en"


def test_every_helpline_has_all_languages():
    for h in HELPLINES:
        for field in ("name", "description", "hours"):
            for lang in SUPPORTED_LANGS:
                assert h[field].get(lang), f"{h['id']} missing {field}/{lang}"


def test_helpline_numbers_look_like_phone_numbers():
    for h in HELPLINES:
        assert h["number"].replace("-", "").isdigit(), h["id"]


def test_non_english_text_is_actually_translated():
    """Catch copy-pasted English left in another language's strings."""
    keep_same = {"chip_247"}
    for lang in SUPPORTED_LANGS:
        if lang == "en":
            continue
        for key, value in TRANSLATIONS[lang].items():
            if key in keep_same:
                continue
            assert value != TRANSLATIONS["en"][key], f"{lang}.{key} is still English"


@pytest.mark.parametrize("lang", SUPPORTED_LANGS)
def test_html_lang_attribute_matches(client, lang):
    html = client.get(f"/{lang}/").get_data(as_text=True)
    assert f'<html lang="{lang}"' in html



@pytest.mark.parametrize("lang", SUPPORTED_LANGS)
def test_theme_toggle_and_quick_exit_present(client, lang):
    html = client.get(f"/{lang}/").get_data(as_text=True)
    assert 'id="theme-toggle"' in html
    assert 'class="quick-exit"' in html


@pytest.mark.parametrize("lang", SUPPORTED_LANGS)
def test_calm_page_has_all_grounding_steps(client, lang):
    html = client.get(f"/{lang}/calm").get_data(as_text=True)
    for key in ("g5", "g4", "g3", "g2", "g1", "breathe_in", "breathe_out"):
        assert TRANSLATIONS[lang][key] in html


@pytest.mark.parametrize("lang", SUPPORTED_LANGS)
def test_browser_auto_translate_is_disabled(client, lang):
    """The app is already localised; stop browsers re-translating it."""
    html = client.get(f"/{lang}/").get_data(as_text=True)
    assert 'translate="no"' in html
    assert 'name="google" content="notranslate"' in html


def test_staging_banner_off_by_default(client, monkeypatch):
    monkeypatch.delenv("SAATHI_ENV", raising=False)
    html = client.get("/en/").get_data(as_text=True)
    assert "staging-banner" not in html and "noindex" not in html


def test_staging_banner_and_noindex_when_staging(client, monkeypatch):
    monkeypatch.setenv("SAATHI_ENV", "staging")
    html = client.get("/en/").get_data(as_text=True)
    assert "staging-banner" in html and 'content="noindex, nofollow"' in html
