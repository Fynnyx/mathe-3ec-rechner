from flask import Flask, request, render_template, redirect, url_for, flash
from math import sqrt, cos

app = Flask(__name__)

def getAmountEntries(triangle, what:str):
    amount = 0
    for x in triangle[what]:
        if triangle[what][x] != "":
            amount = amount + 1
    return amount

def getTriangleSAA(triangle):
    if triangle["angles"]["a"] == "":
        triangle["angles"]["a"] = 180 - (int(triangle["angles"]["b"] + int(triangle["angles"]["c"])))
    elif triangle["angles"]["b"] == "":
        triangle["angles"]["b"] = 180 - (int(triangle["angles"]["a"] + int(triangle["angles"]["c"])))
    elif triangle["angles"]["c"] == "":
        triangle["angles"]["c"] = 180 - (int(triangle["angles"]["a"] + int(triangle["angles"]["b"])))

    print(triangle)



def getTriangleSSS(sa, sb, sc, triangle):
    triangle["angles"]["c"] = cos((sqrt(int(sa)) + sqrt(int(sb)) - sqrt(int(sc)))/(2*(int(sa)*int(sb))))
    triangle["angles"]["b"] = cos((sqrt(int(sc)) + sqrt(int(sa)) + sqrt(int(sb)))/(2*(int(sc)*int(sa))))
    triangle["angles"]["a"] = cos((sqrt(int(sb)) + sqrt(int(sc)) + sqrt(int(sa)))/(2*(int(sb)*int(sc))))
    return triangle

def has_info(triangle):
    sites_amount = getAmountEntries(triangle, "sites")
    angle_amount = getAmountEntries(triangle, "angles")
    print(sites_amount, angle_amount)
    if sites_amount == 3 and angle_amount == 3:
        return triangle
    elif sites_amount == 2 and angle_amount == 1:
        print("2")
    elif sites_amount == 1 and angle_amount == 2:
        triangle = getTriangleSAA(triangle)
    elif sites_amount == 3 and angle_amount == 0:
        triangle = getTriangleSSS(triangle["sites"]["a"], triangle["sites"]["b"], triangle["sites"]["c"], triangle)
    else:
        print("6")
    return triangle

@app.route("/")
def home():
    return render_template("html/index.html")


@app.route("/form", methods=['POST'])
def recive_form():
    try:
        global triangle
        triangle = {"sites": {"a": request.form['site_a'], "b": request.form['site_b'], "c": request.form['site_c']}, "angles": {"a": request.form['angle_a'], "b": request.form['angle_b'], "c": request.form['angle_c']}, "properties": {"right_angled": False, "isosceles": False, "equilateral": False, "height": 0, "area": 0}}
        print("Got Data: ", triangle)

        triangle = has_info(triangle)

        # if triangle["angles"]["a"] == "":
        #     if int(triangle["angles"]["b"]) != 0 and int(triangle["angles"]["c"]) != 0:
        #         triangle["angles"]["a"] = calc_angles(int(triangle["angles"]["b"]), int(triangle["angles"]["c"]))
        #     else:
        #         print("Error occured")
        # if triangle["angles"]["b"] == "":
        #     if int(triangle["angles"]["a"]) != 0 and int(triangle["angles"]["c"]) != 0:
        #         triangle["angles"]["b"] = calc_angles(int(triangle["angles"]["a"]), int(triangle["angles"]["c"]))
        #     else:
        #         print("Error occured")
        # if triangle["angles"]["c"] == "":
        #     if int(triangle["angles"]["a"]) != 0 and int(triangle["angles"]["b"]) != 0:
        #         triangle["angles"]["c"] = calc_angles(int(triangle["angles"]["a"]), int(triangle["angles"]["b"]))
        #     else:
        #         print("Error occured")


        # ob das rechteck RECHTWINKLIG ist
        for angle in triangle["angles"]:
            if int(triangle["angles"][angle]) == 90:
                triangle["properties"]["right_angled"] = True
        # ob das dreieck GLEICHSCHENKLIG ist mit winkeln
        if triangle["angles"]["a"] == triangle["angles"]["b"] or triangle["angles"]["a"] == triangle["angles"]["c"] or triangle["angles"]["b"] == triangle["angles"]["c"]:
            triangle["properties"]["isosceles"] = True


        # if triangle['sites']["a"] == "":
        #     print("a!=0")
        #
        # if triangle['sites']["b"] == "":
        #     print("b!=0")
        #
        # if triangle['sites']["c"] == "":
        #     print("c!=0")


        # ob das dreich GLEICHSEITIG ist
        if triangle["sites"]["a"] == triangle["sites"]["b"] == triangle["sites"]["c"]:
            triangle["properties"]["equilateral"] = True

    except ValueError:
        print("Value missing or not a number")
    finally:
        print(triangle)

    return redirect(url_for("home"))


def calc_angles(angle1, angle2):
    angle3 = 180 - (angle1 + angle2)
    print("angle3: ", angle3)
    return angle3

if __name__ == "__main__":
    app.run()
