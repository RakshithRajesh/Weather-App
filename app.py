from requests_html import HTMLSession
from flask import Flask, render_template, request
from datetime import datetime


def get_weather(city_name):
    url = f"https://www.google.com/search?q={city_name}+weather"
    s = HTMLSession()
    r = s.get(url)
    
    details = {
        "location": r.html.find('div[id="wob_loc"]', first=True).text,
        "celsius": r.html.find('span[class="wob_t TVtOme"]', first=True).text,
        "weather": r.html.find('span[id="wob_dc"]', first=True).text,
        "precipitation": r.html.find('span[id="wob_pp"]', first=True).text,
        "humidity": r.html.find('span[id="wob_hm"]', first=True).text,
        "wind": r.html.find('span[id="wob_ws"]', first=True).text,
    }

    return details


app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecretkey"



details = ""


@app.route("/", methods=["GET", "POST"])
def home():
    global details
    if request.method == "POST":
        city_name = request.form.get("cityname")
        details = get_weather(city_name)

    return render_template("index.html", details=details)


if __name__ == "__main__":
    app.run(debug=True)
