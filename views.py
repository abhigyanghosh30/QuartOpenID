import quart
from quart import render_template
from decorators import login_required

from login import user_info


async def render_index():
    return await render_template("index.html")


@login_required
async def dashboard():
    user = user_info(quart.session)

    return await render_template(
        "dashboard.html", email=user["email"], fullname=user["fullname"]
    )
