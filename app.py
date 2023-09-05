from quart import Quart, render_template, session, request, redirect, url_for
from openid.extensions import sreg, pape
from openid.consumer import consumer
from openid.store.filestore import FileOpenIDStore

OPENID_PROVIDER_URL = "https://login.ubuntu.com/"

app = Quart("__name__")
app.secret_key = "secret"

def getConsumer():
    store = FileOpenIDStore("/tmp/openid")
    return consumer.Consumer(session, store)

@app.route("/callback")
def callback():
    oidconsumer = getConsumer()
    url = "http://" + request.headers.get("Host") + "/process"
    info = oidconsumer.complete(request.args.to_dict(), url)
    display_identifier = info.getDisplayIdentifier()
    if info.status == consumer.SUCCESS:
        sreg_response = sreg.SRegResponse.fromSuccessResponse(info)
        pape_response = pape.Response.fromSuccessResponse(info)
        session["username"] = sreg_response.get("nickname")
        session["email"] = sreg_response.get("email")
        session["fullname"] = sreg_response.get("fullname")
        return redirect(url_for("dashboard"))

@app.route("/login")
def login():
    oidconsumer = getConsumer()
    try:
        oid_request = oidconsumer.begin(OPENID_PROVIDER_URL)
    except consumer.DiscoveryFailure as e:
        return render_template("error.html", error=e)
    else:
        if oid_request is None:
            return render_template("error.html", error="No OpenID services found")  
        else:
            sreg_request = sreg.SRegRequest(required=['nickname', 'email'],optional=['fullname'])
            pape_request = pape.Request([pape.AUTH_PHISHING_RESISTANT])
            oid_request.addExtension(sreg_request)
            oid_request.addExtension(pape_request)
            redirect_url = oid_request.redirectURL("http://0.0.0.0:5000","http://0.0.0.0:5000/callback", immediate=False)
            return redirect(redirect_url)

@app.route("/")
def dashboard():
        if "username" not in session or session["username"] is None:
            return redirect(url_for("login"))
        return render_template("success.html", username=session["username"], email=session["email"], fullname=session["fullname"])

if __name__ == "__main__":
    app.run()