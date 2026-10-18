"""Saathi - Mental Health First-Aid Guide (Step 1: helplines + crisis page).

Elastic Beanstalk's Python platform looks for a WSGI callable named
`application` in application.py, so keep that name.
"""
import json
import os
from pathlib import Path

from flask import Flask, abort, redirect, render_template, url_for

BASE_DIR = Path(__file__).parent
SUPPORTED_LANGS = ["en", "hi", "bn", "mr", "ta", "te"]
LANG_NAMES = {
    "en": "English", "hi": "हिन्दी", "bn": "বাংলা",
    "mr": "मराठी", "ta": "தமிழ்", "te": "తెలుగు",
}


def load_json(name):
    with open(BASE_DIR / "data" / name, encoding="utf-8") as f:
        return json.load(f)


TRANSLATIONS = load_json("translations.json")
HELPLINES = load_json("helplines.json")

application = Flask(__name__)


def check_lang(lang):
    if lang not in SUPPORTED_LANGS:
        abort(404)
    return lang


@application.context_processor
def inject_helpers():
    def make_t(lang):
        def t(key):
            return TRANSLATIONS[lang][key]
        return t
    return {
        "make_t": make_t,
        "lang_names": LANG_NAMES,
        "supported_langs": SUPPORTED_LANGS,
        # Set SAATHI_ENV=staging on review deployments to show a draft banner
        "staging": os.environ.get("SAATHI_ENV") == "staging",
    }


@application.route("/")
def root():
    return redirect(url_for("home", lang="en"))


@application.route("/<lang>/")
def home(lang):
    check_lang(lang)
    return render_template("home.html", lang=lang, t=TRANSLATIONS[lang], page="home")


@application.route("/<lang>/helplines")
def helplines(lang):
    check_lang(lang)
    return render_template(
        "helplines.html", lang=lang, t=TRANSLATIONS[lang], page="helplines",
        items=[h for h in HELPLINES if not h.get("emergency_only")],
    )


@application.route("/<lang>/calm")
def calm(lang):
    check_lang(lang)
    return render_template("calm.html", lang=lang, t=TRANSLATIONS[lang], page="calm")


@application.route("/<lang>/crisis")
def crisis(lang):
    check_lang(lang)
    return render_template(
        "crisis.html", lang=lang, t=TRANSLATIONS[lang], page="crisis", items=HELPLINES
    )


@application.route("/health")
def health():
    """Used by the Elastic Beanstalk load balancer health check."""
    return {"status": "ok"}, 200


if __name__ == "__main__":
    application.run(debug=True)
