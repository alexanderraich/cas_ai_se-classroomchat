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
    Flask, abort, flash, g, redirect, render_template, request, session, url_for
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))

# === In-Memory-Store (FA-16) ===
# users:    user_id -> {"name": str}
# groups:   group_id -> {"name": str, "owner_id": str, "members": set[str]}
# messages: group_id -> list[{"id", "author_id", "author_name", "text", "created_at"}]
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
    @wraps(view)
    def wrapper(gid, *args, **kwargs):
        grp = groups.get(gid)
        if not grp:
            abort(404)
        if g.uid not in grp["members"]:
            abort(403)
        return view(gid, *args, **kwargs)
    return wrapper


def require_owner(view):
    @wraps(view)
    def wrapper(gid, *args, **kwargs):
        grp = groups.get(gid)
        if not grp:
            abort(404)
        if g.uid != grp["owner_id"]:
            abort(403)
        return view(gid, *args, **kwargs)
    return wrapper


# === Helpers ===
def my_groups(uid: str) -> list[tuple[str, dict]]:
    return sorted(
        ((gid, grp) for gid, grp in groups.items() if uid in grp["members"]),
        key=lambda kv: kv[1]["name"].lower(),
    )


# === Routes ===
@app.route("/")
def index():
    uid = session.get("uid")
    if not uid or uid not in users:
        return render_template("login.html")
    # Zur ersten eigenen Gruppe (oder Empty-Shell)
    mine = my_groups(uid)
    if mine:
        return redirect(url_for("group_view", gid=mine[0][0]))
    return render_template(
        "group.html",
        me=users[uid]["name"],
        my_groups=[],
        active=None,
        msgs=[],
    )


@app.post("/login")
def login():
    name = validate_name(request.form.get("name", ""))
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
    groups[gid] = {"name": name, "owner_id": g.uid, "members": {g.uid}}
    messages[gid] = []
    return redirect(url_for("group_view", gid=gid))


@app.get("/g/<gid>")
@require_login
@require_member
def group_view(gid):
    grp = groups[gid]
    member_list = sorted(
        ((mid, users[mid]["name"]) for mid in grp["members"]),
        key=lambda x: x[1].lower(),
    )
    return render_template(
        "group.html",
        me=g.uname,
        my_groups=my_groups(g.uid),
        active=(gid, grp),
        msgs=messages.get(gid, []),
        is_owner=(g.uid == grp["owner_id"]),
        member_list=member_list,
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


@app.post("/g/<gid>/members")
@require_login
@require_owner
def add_member(gid):
    name = validate_name(request.form.get("name", ""))
    # Find or create user (TRL4-Vereinfachung: Mitglied wird angelegt, falls noch nicht vorhanden)
    target_uid = next((uid for uid, u in users.items() if u["name"].lower() == name.lower()), None)
    if target_uid is None:
        target_uid = str(uuid.uuid4())
        users[target_uid] = {"name": name}
    groups[gid]["members"].add(target_uid)
    return redirect(url_for("group_view", gid=gid))


@app.post("/g/<gid>/members/<target_uid>/remove")
@require_login
@require_owner
def remove_member(gid, target_uid):
    if target_uid == groups[gid]["owner_id"]:
        abort(400, "Eigentümer kann sich nicht selbst entfernen.")
    groups[gid]["members"].discard(target_uid)
    return redirect(url_for("group_view", gid=gid))


@app.post("/g/<gid>/delete")
@require_login
@require_owner
def delete_group(gid):
    groups.pop(gid, None)
    messages.pop(gid, None)
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
