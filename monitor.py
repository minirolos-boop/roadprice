# monitor.py
import os
import json
import sqlite3
import argparse
import logging
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

API_URL = "https://api-catalog.weroad.fr/travels"


# -------------------- Utils --------------------
def g(d, path, default=None):
    cur = d
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def num(x):
    return x if isinstance(x, (int, float)) else None


def to_month(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").strftime("%Y-%m")
    except Exception:
        return None


def _sanitize_scalars(d: dict) -> dict:
    """Convertit dict/list en JSON str pour compatibilité SQLite."""
    out = {}
    for k, v in d.items():
        if isinstance(v, (dict, list)):
            out[k] = json.dumps(v, ensure_ascii=False)
        else:
            out[k] = v
    return out


# -------------------- Fetch + normalize --------------------
def fetch_travels():
    s = requests.Session()
    headers = {"accept": "application/json, text/plain, */*"}
    token = os.getenv("WEROAD_TOKEN")  # optionnel
    if token:
        headers["authorization"] = f"Bearer {token}"
    s.headers.update(headers)

    r = s.get(API_URL, timeout=30)
    r.raise_for_status()
    data = r.json()
    items = data.get("data", data) or []
    return items if isinstance(items, list) else []


def normalize(travels):
    rows = []
    for t in travels:
        bt = t.get("bestTour") or {}
        price = num(g(bt, ["price", "EUR"]))
        base = num(g(bt, ["basePrice", "EUR"]))

        disc_val = disc_pct = None
        if price is not None and base is not None and base > price:
            disc_val = base - price
            disc_pct = round((base - price) / base * 100, 1)

        if price is None and base is None:
            min_p = max_p = None
        elif price is None:
            min_p = max_p = base
        elif base is None:
            min_p = max_p = price
        else:
            min_p = min(price, base)
            max_p = max(price, base)

        rows.append(
            {
                "id": t.get("id"),
                "slug": t.get("slug"),
                "url": f"https://www.weroad.fr/voyages/{t.get('slug')}" if t.get("slug") else None,
                "title": t.get("title") or t.get("destinationLabel") or t.get("slug"),
                "destination_label": t.get("destinationLabel"),
                "country_name": g(t, ["primaryDestination", "name"]),
                "continent": g(t, ["primaryDestination", "primaryContinent", "name"]),
                "status": t.get("status"),
                "isBookable": t.get("isBookable"),
                "days": t.get("numberOfDays"),
                "style": g(t, ["travelStyle", "displayName"]),
                "types": ", ".join(
                    [x.get("displayName") for x in t.get("travelTypes", []) if x.get("displayName")]
                ),
                "price_eur": price,
                "base_price_eur": base,
                "discount_value_eur": disc_val,
                "discount_pct": disc_pct,
                "sales_status": g(bt, ["salesStatus"]),
                "seatsToConfirm": g(bt, ["seatsToConfirm"]),
                "maxPax": g(bt, ["maxPax"]),
                "weroadersCount": g(bt, ["groupInfo", "weroadersCount"]),
                "min_price_eur": min_p,
                "max_price_eur": max_p,
                "best_starting_date": g(bt, ["startingDate"]),
                "best_ending_date": g(bt, ["endingDate"]),
                "rating": g(t, ["userRating", "rating"]),
                "rating_count": g(t, ["userRating", "count"]),
            }
        )

    df = pd.DataFrame(rows)
    df["month"] = df["best_starting_date"].map(to_month)

    # 🔴 Filtre : retirer voyages sans sales_status défini
    if not df.empty:
        df = df.dropna(subset=["sales_status"])
        df = df[df["sales_status"].astype(str).str.strip() != ""]

    return df
