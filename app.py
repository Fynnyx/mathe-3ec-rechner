from flask import Flask, request, render_template, redirect, url_for, flash
from math import acos, cos, sin, asin, pi


app = Flask(__name__)

def getAmountEntries(triangle, what:str):
    amount = 0
    for x in triangle[what]:
        if triangle[what][x] != "":
            amount = amount + 1
    return amount

# def isMiddleAngle(triangle):


def getTriagnleSSA(triangle):
    print(triangle)

    if triangle["sites"]["a"] != "" and triangle["sites"]["b"] != "" and triangle["angles"]["c"] != "":
        print(triangle)
    elif triangle["sites"]["a"] != "" and triangle["sites"]["c"] != "" and triangle["angles"]["b"] != "":
        print(triangle)
    elif triangle["sites"]["b"] != "" and triangle["sites"]["c"] != "" and triangle["angles"]["a"] != "":
        print(triangle)
    return triangle

    # if isMiddleAngle(triangle):

#     Ist es der eingeschlossener winkel => cosinus satz benutzen. => SSS
#     ist es nicht der eingeschlossene Winkel => sinus satz => mit evtl. weiterer winkel mit 2 Lösungen.

def getTriangleSAA(triangle):
    if triangle["angles"]["a"] == "":
        triangle["angles"]["a"] = 180 - (float(triangle["angles"]["b"]) + float(triangle["angles"]["c"]))
    elif triangle["angles"]["b"] == "":
        triangle["angles"]["b"] = 180 - (float(triangle["angles"]["a"]) + float(triangle["angles"]["c"]))
    elif triangle["angles"]["c"] == "":
        triangle["angles"]["c"] = 180 - (float(triangle["angles"]["a"]) + float(triangle["angles"]["b"]))


    if triangle["sites"]["a"] != "":
        triangle["sites"]["c"] =  round(((sin(float(triangle["angles"]["a"])) * float(triangle["sites"]["a"])) / sin(float(triangle["angles"]["c"]))) / pi * 180, 2)
        triangle["sites"]["b"] =  round(((sin(float(triangle["angles"]["a"])) * float(triangle["sites"]["a"])) / sin(float(triangle["angles"]["b"]))) / pi * 180, 2)

    elif triangle["sites"]["b"] != "":
        triangle["sites"]["a"] =  round(((sin(float(triangle["angles"]["b"])) * float(triangle["sites"]["b"])) / sin(float(triangle["angles"]["a"]))) / pi * 180, 2)
        triangle["sites"]["c"] =  round(((sin(float(triangle["angles"]["b"])) * float(triangle["sites"]["b"])) / sin(float(triangle["angles"]["c"]))) / pi * 180, 2)

    elif triangle["sites"]["c"] != "":
        triangle["sites"]["b"] =  round(((sin(float(triangle["angles"]["c"])) * float(triangle["sites"]["c"])) / sin(float(triangle["angles"]["b"]))) / pi * 180, 2)
        triangle["sites"]["a"] =  round(((sin(float(triangle["angles"]["c"])) * float(triangle["sites"]["c"])) / sin(float(triangle["angles"]["a"]))) / pi * 180, 2)
    return triangle


def getTriangleSSS(sa, sb, sc, triangle):
    triangle["angles"]["c"] = round((acos((float(sa)**2 + float(sb)**2 - float(sc)**2) / (2 * float(sa) * float(sb)))) / pi * 180, 2)
    triangle["angles"]["b"] = round((acos((float(sc)**2 + float(sa)**2 - float(sb)**2) / (2 * float(sc) * float(sa)))) / pi * 180, 2)
    triangle["angles"]["a"] = round((acos((float(sb)**2 + float(sc)**2 - float(sa)**2) / (2 * float(sb) * float(sc)))) / pi * 180, 2)
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
def home(site_a = "", site_b = "", site_c = "", angle_a = "", angle_b = "", angle_c = "", right_angled = False, isosceles =  False, equilateral = False, height = "", area = "" ):
    return render_template("html/index.html", site_a = site_a, site_b = site_b, site_c = site_c, angle_a = angle_a, angle_b = angle_b, angle_c = angle_c, area = area)

@app.route("/form", methods=['POST'])
def recive_form():
    try:
        global triangle
        triangle = {"sites": {"a": request.form['site_a'], "b": request.form['site_b'], "c": request.form['site_c']}, "angles": {"a": request.form['angle_a'], "b": request.form['angle_b'], "c": request.form['angle_c']}, "properties": {"right_angled": False, "isosceles": False, "equilateral": False, "height": 0, "area": 0}}
        print("Got Data: ", triangle)

        triangle = has_info(triangle)

        # ob das rechteck RECHTWINKLIG ist
        for angle in triangle["angles"]:
            if float(triangle["angles"][angle]) == 90:
                triangle["properties"]["right_angled"] = True
        # ob das dreieck GLEICHSCHENKLIG ist mit winkeln
        if triangle["angles"]["a"] == triangle["angles"]["b"] or triangle["angles"]["a"] == triangle["angles"]["c"] or triangle["angles"]["b"] == triangle["angles"]["c"]:
            triangle["properties"]["isosceles"] = True

        # ob das dreich GLEICHSEITIG ist
        if triangle["sites"]["a"] == triangle["sites"]["b"] == triangle["sites"]["c"]:
            triangle["properties"]["equilateral"] = True

    except ValueError:
        print("Value missing or not a number")
    finally:
        print(triangle)

    return render_template("./html/index.html", site_a = triangle["sites"]["a"],
                    site_b=triangle["sites"]["b"],
                    site_c=triangle["sites"]["c"],
                    angle_a=triangle["angles"]["a"],
                    angle_b=triangle["angles"]["b"],
                    angle_c=triangle["angles"]["c"],
                    rectangle = triangle["properties"]["right_angled"],
                    isosceles = triangle["properties"]["isosceles"],
                    equilateral = triangle["properties"]["equilateral"],
                    height = triangle["properties"]["height"],
                    area = triangle["properties"]["area"]
                    )


def calc_angles(angle1, angle2):
    angle3 = 180 - (angle1 + angle2)
    print("angle3: ", angle3)
    return angle3

if __name__ == "__main__":
    app.run()
