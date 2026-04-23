"""Classroom Chat — Flask-App (TRL4-Prototyp).

Single-File Flask-Applikation mit In-Memory-State.
Siehe docs/schritt6-architektur.md für Endpoints und FA-Mapping.
"""
from __future__ import annotations

import os
import secrets
import uuid
from datetime import datetime, timezone
from functools import wraps

from flask import (
    Flask, abort, flash, g, jsonify, redirect, render_template, request, session, url_for
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))

# === In-Memory-Store (FA-16) ===
# users:    user_id -> {"name": str}
# groups:   group_id -> {"name": str, "owner_id": str}
# messages: group_id -> list[{"id", "author_id", "author_name", "text", "created_at"}]
# Open-Membership-Modell (TRL4): keine explizite Mitgliederliste pro Gruppe —
# jeder eingeloggte Benutzer sieht jede Gruppe.
users: dict[str, dict] = {}
groups: dict[str, dict] = {}
messages: dict[str, list[dict]] = {}


# === Validatoren ===
def validate_name(name: str) -> str:
    name = (name or "").strip()
    if not (1 <= len(name) <= 32):
        abort(400, "Anzeigename muss 1–32 Zeichen haben.")
    return name


def validate_groupname(name: str) -> str:
    name = (name or "").strip()
    if not (1 <= len(name) <= 64):
        abort(400, "Gruppenname muss 1–64 Zeichen haben.")
    return name


def validate_message(text: str) -> str:
    text = (text or "").strip()
    if not (1 <= len(text) <= 2000):
        abort(400, "Nachricht muss 1–2000 Zeichen haben.")
    return text


# === Decorators (FA-10, FA-17, FA-20) ===
def require_login(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        uid = session.get("uid")
        if not uid or uid not in users:
            session.clear()
            return redirect(url_for("index"))
        g.uid = uid
        g.uname = users[uid]["name"]
        return view(*args, **kwargs)
    return wrapper


def require_member(view):
    """TRL4-Vereinfachung: alle eingeloggten User sind in jeder Gruppe.
    Wir prüfen nur, dass die Gruppe existiert."""
    @wraps(view)
    def wrapper(gid, *args, **kwargs):
        if gid not in groups:
            flash("Diese Gruppe existiert nicht (mehr).")
            return redirect(url_for("index"))
        return view(gid, *args, **kwargs)
    return wrapper


def require_owner(view):
    @wraps(view)
    def wrapper(gid, *args, **kwargs):
        grp = groups.get(gid)
        if not grp:
            flash("Diese Gruppe existiert nicht mehr.")
            return redirect(url_for("index"))
        if g.uid != grp["owner_id"]:
            abort(403)
        return view(gid, *args, **kwargs)
    return wrapper


# === Helpers ===
def all_groups_sorted() -> list[tuple[str, dict]]:
    return sorted(groups.items(), key=lambda kv: kv[1]["name"].lower())


def all_users_sorted() -> list[tuple[str, str]]:
    return sorted(((uid, u["name"]) for uid, u in users.items()), key=lambda x: x[1].lower())


# === Routes ===
@app.route("/")
def index():
    uid = session.get("uid")
    if not uid or uid not in users:
        return render_template("login.html")
    # Erste verfügbare Gruppe (oder Empty-Shell)
    grps = all_groups_sorted()
    if grps:
        return redirect(url_for("group_view", gid=grps[0][0]))
    return render_template(
        "group.html",
        me=users[uid]["name"],
        my_groups=[],
        all_users=all_users_sorted(),
        active=None,
        msgs=[],
    )


@app.post("/login")
def login():
    name = validate_name(request.form.get("name", ""))
    # Existierenden User mit gleichem Namen wiederverwenden (case-insensitive),
    # damit Mitgliedschaften, die der Owner vorab angelegt hat, sichtbar sind.
    uid = next(
        (uid for uid, u in users.items() if u["name"].lower() == name.lower()),
        None,
    )
    if uid is None:
        uid = str(uuid.uuid4())
        users[uid] = {"name": name}
    session["uid"] = uid
    return redirect(url_for("index"))


@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.post("/groups")
@require_login
def create_group():
    name = validate_groupname(request.form.get("name", ""))
    gid = str(uuid.uuid4())
    groups[gid] = {"name": name, "owner_id": g.uid}
    messages[gid] = []
    return redirect(url_for("group_view", gid=gid))


@app.get("/g/<gid>")
@require_login
@require_member
def group_view(gid):
    grp = groups[gid]
    return render_template(
        "group.html",
        me=g.uname,
        my_groups=all_groups_sorted(),
        all_users=all_users_sorted(),
        active=(gid, grp),
        msgs=messages.get(gid, []),
        is_owner=(g.uid == grp["owner_id"]),
        owner_name=users[grp["owner_id"]]["name"],
    )


@app.post("/g/<gid>/messages")
@require_login
@require_member
def send_message(gid):
    text = validate_message(request.form.get("text", ""))
    messages[gid].append({
        "id": str(uuid.uuid4()),
        "author_id": g.uid,
        "author_name": g.uname,
        "text": text,
        "created_at": datetime.now(timezone.utc).isoformat(),
    })
    return redirect(url_for("group_view", gid=gid))


@app.post("/g/<gid>/rename")
@require_login
@require_owner
def rename_group(gid):
    new_name = validate_groupname(request.form.get("name", ""))
    groups[gid]["name"] = new_name
    return redirect(url_for("group_view", gid=gid))


@app.post("/g/<gid>/delete")
@require_login
@require_owner
def delete_group(gid):
    groups.pop(gid, None)
    messages.pop(gid, None)
    return redirect(url_for("index"))


# === JSON-API für SPA-artiges Live-Update ===
@app.get("/g/<gid>/state.json")
@require_login
@require_member
def group_state(gid):
    grp = groups[gid]
    return jsonify({
        "active_gid": gid,
        "active_name": grp["name"],
        "owner_name": users[grp["owner_id"]]["name"],
        "is_owner": (g.uid == grp["owner_id"]),
        "messages": [
            {
                "id": m["id"],
                "author_name": m["author_name"],
                "text": m["text"],
                "created_at": m["created_at"],
                "is_me": (m["author_id"] == g.uid),
            }
            for m in messages.get(gid, [])
        ],
        "groups": [
            {
                "gid": gid_,
                "name": grp_["name"],
                "active": gid_ == gid,
                "msg_count": len(messages.get(gid_, [])),
            }
            for gid_, grp_ in all_groups_sorted()
        ],
        "users": [
            {"uid": uid, "name": uname, "is_me": uid == g.uid}
            for uid, uname in all_users_sorted()
        ],
    })


# === Error-Handler ===
@app.get("/favicon.ico")
def favicon():
    """Browser fragt favicon automatisch an — wir liefern leeres 204, damit
    keine 404-Logspam entsteht."""
    return ("", 204)


@app.errorhandler(404)
def handle_404(e):
    """Cold-Start auf Render Free-Plan löscht den In-Memory-Store (FA-16).
    Alte Gruppen-URLs landen sonst im 404 — wir leiten auf die Startseite um.
    """
    return redirect(url_for("index"))


# === Jinja-Filter ===
@app.template_filter("localtime")
def localtime_filter(iso: str) -> str:
    """Hilfsdarstellung — Browser-Anzeige bleibt UTC im <time>-Tag."""
    try:
        dt = datetime.fromisoformat(iso)
        return dt.strftime("%H:%M")
    except Exception:
        return iso


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
