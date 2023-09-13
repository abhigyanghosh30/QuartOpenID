from quart import Quart
from login import login_handler, logout
from views import render_index, dashboard

app = Quart(
    __name__,
    template_folder="./templates",
)
app.secret_key = "secret"

app.add_url_rule("/login", methods=["GET", "POST"], view_func=login_handler)
app.add_url_rule("/logout", view_func=logout)

app.add_url_rule("/", view_func=render_index)
app.add_url_rule("/dashboard", view_func=dashboard)

if __name__ == "__main__":
    app.run()
