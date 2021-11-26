from flask import Flask, request, render_template, redirect, url_for, flash

app = Flask(__name__)
def has_infos(sites, angles):
    print(sites, angles)
    sites_amount = len(sites)
    angle_amount = len(angles)
    print(sites_amount, angle_amount)
    if sites_amount == 3 and angle_amount == 3:
        print("1")
    elif sites_amount == 2 and angle_amount == 1:
        print("2")
    elif sites_amount == 1 and angle_amount == 2:
        print("3")
    elif sites_amount == 3 and angle_amount == 0:
        print("4")
    else:
        print("6")

site_a = 13
site_b = 28
site_c = 34
angle_a = 2
angle_b = 35
angle_c = 26


triangle = {"sites": {"a": 0, "b": 0, "c": 0}, "angles": {"a": 0, "b": 0, "c": 0}}


@app.route("/")
def home():
    return render_template("html/index.html")


@app.route("/form", methods=['POST'])
def recive_form():
    print("done")
    request.form[""]
    #triangle = {"sites": {"a": request.form['site_a'], "b": request.form['site_b'], "c": request.form['site_c']}, "angles": {"a": request.form['angle_a'], "b": request.form['angle_b'], "c": request.form['angle_c']}}
    print("done")
    if triangle['sites']["a"] != 0:
        print("a!=0")

    if triangle['sites']["b"] != 0:
        print("b!=0")
    if triangle['sites']["c"] != 0:
        print("c!=0")

    if triangle["angles"]["a"] != 0:
        print("a!=0")
    if triangle["angles"]["b"] != 0:
        print("b!=0")
    if triangle["angles"]["c"] != 0:
        print("c!=0")

    return redirect(url_for("home"))


triangle["sites"]["a"] = site_a
triangle["sites"]["b"] = site_b
triangle["sites"]["c"] = site_c

triangle["angles"]["a"] = angle_a
triangle["angles"]["b"] = angle_b
triangle["angles"]["c"] = angle_c

print(triangle)

if __name__ == "__main__":
    app.run()
