from flask import Flask, request, render_template, redirect, url_for, flash
from math import acos, cos, sin, asin, pi, sqrt

app = Flask(__name__)

ROUND_INDICATOR = 2

def getAmountEntries(triangle, what:str):
    amount = 0
    for x in triangle[what]:
        if triangle[what][x] != "":
            amount = amount + 1
    return amount

def checkForNegatives(triangle):
    is_negativ = False
    for x in triangle["sites"]:
        if triangle["sites"][x] != "":
            if float(triangle["sites"][x]) < 0:
                is_negativ = True
                return is_negativ
    for x in triangle["angles"]:
        if triangle["angles"][x] != "":
            if float(triangle["angles"][x]) < 0:
                is_negativ = True
                return is_negativ
    return is_negativ

def checkForAnglesMore180(angles):
    for x in angles:
        if angles[x] != "":
            if float(angles[x]) > 180:
                return True
    return False


def getDegreesFromRadian(value):
    return value / pi * 180

def getRadianFromDegrees(value):
    return value * pi / 180


def getTriangleSSA(triangle):
    if triangle["sites"]["a"] != "" and triangle["sites"]["b"] != "" and triangle["angles"]["c"] != "":
        triangle["sites"]["c"] = round(sqrt(float(triangle["sites"]["a"])**2 + float(triangle["sites"]["b"])**2 - 2 * (float(triangle["sites"]["a"]) * float(triangle["sites"]["b"])) * cos(getRadianFromDegrees(float(triangle["angles"]["c"])))), ROUND_INDICATOR)
        triangle = getTriangleSSS(triangle["sites"]["a"], triangle["sites"]["b"], triangle["sites"]["c"], triangle)

    elif triangle["sites"]["a"] != "" and triangle["sites"]["c"] != "" and triangle["angles"]["b"] != "":
        triangle["sites"]["b"] = round(sqrt(float(triangle["sites"]["a"])**2 + float(triangle["sites"]["c"])**2 - 2 * (float(triangle["sites"]["a"]) * float(triangle["sites"]["c"])) * cos(getRadianFromDegrees(float(triangle["angles"]["b"])))), ROUND_INDICATOR)
        triangle = getTriangleSSS(triangle["sites"]["a"], triangle["sites"]["b"], triangle["sites"]["c"], triangle)

    elif triangle["sites"]["b"] != "" and triangle["sites"]["c"] != "" and triangle["angles"]["a"] != "":
        triangle["sites"]["a"] = round(sqrt(float(triangle["sites"]["b"])**2 + float(triangle["sites"]["c"])**2 - 2 * (float(triangle["sites"]["b"]) * float(triangle["sites"]["c"])) * cos(getRadianFromDegrees(float(triangle["angles"]["a"])))), ROUND_INDICATOR)
        triangle = getTriangleSSS(triangle["sites"]["a"], triangle["sites"]["b"], triangle["sites"]["c"], triangle)


    if triangle["sites"]["a"] != "" and triangle["sites"]["b"] != "" and triangle["angles"]["a"] != "":
        if sin(getRadianFromDegrees(float(triangle["angles"]["a"]))) * float(triangle["sites"]["b"])/ float(triangle["sites"]["a"]) >= -1 and sin(getRadianFromDegrees(float(triangle["angles"]["a"]))) * float(triangle["sites"]["b"])/ float(triangle["sites"]["a"]) <= 1:
            triangle["angles"]["b"] = round(getDegreesFromRadian(asin((sin(getRadianFromDegrees(float(triangle["angles"]["a"]))) * float(triangle["sites"]["b"])/ float(triangle["sites"]["a"])))), ROUND_INDICATOR)
            triangle["angles"]["c"] = round(180 - (float(triangle["angles"]["b"]) + float(triangle["angles"]["a"])), ROUND_INDICATOR)
            triangle["sites"]["c"] = round(float(triangle["sites"]["a"]) / sin(float(triangle["angles"]["a"])) * sin(float(triangle["angles"]["c"])), ROUND_INDICATOR)
            if float(triangle["angles"]["a"]) < 90 and float(triangle["sites"]["a"]) < float(triangle["sites"]["b"]):
                angleb = round(180 - float(triangle["angles"]["b"]), ROUND_INDICATOR)
                anglec = round(180 - (angleb + float["angles"]["a"]), ROUND_INDICATOR)
                sitec = round(float(triangle["sites"]["a"]) / sin(float(triangle["angles"]["a"])) * sin(anglec), ROUND_INDICATOR)
                triangle["angles"]["b"] = str(triangle["angles"]["b"]) + " oder " + str(angleb)
                triangle["angles"]["c"] = str(triangle["angles"]["c"]) + " oder " + str(anglec)
                triangle["sites"]["c"] = str(triangle["sites"]["c"]) +  " oder " + str(sitec)
        else:
            # Return Error
            print("not Possible")

    elif triangle["sites"]["a"] != "" and triangle["sites"]["b"] != "" and triangle["angles"]["b"] != "":
        if sin(getRadianFromDegrees(float(triangle["angles"]["b"]))) * float(triangle["sites"]["a"])/ float(triangle["sites"]["b"]) >= -1 and sin(getRadianFromDegrees(float(triangle["angles"]["b"]))) * float(triangle["sites"]["a"])/ float(triangle["sites"]["b"]) <= 1:
            triangle["angles"]["a"] = round(getDegreesFromRadian(asin((sin(getRadianFromDegrees(float(triangle["angles"]["b"]))) * float(triangle["sites"]["a"])) / float(triangle["sites"]["b"]))), ROUND_INDICATOR)
            triangle["angles"]["c"] = round(180 - (float(triangle["angles"]["b"]) + float(triangle["angles"]["a"])), ROUND_INDICATOR)
            triangle["sites"]["c"] = round(float(triangle["sites"]["a"]) / sin(float(triangle["angles"]["a"])) * sin(float(triangle["angles"]["c"])), ROUND_INDICATOR)
            if float(triangle["angles"]["b"]) < 90 and float(triangle["sites"]["b"]) < float(triangle["sites"]["a"]):
                anglea = round(180 - float(triangle["angles"]["a"]), ROUND_INDICATOR)
                anglec = round(180 - (anglea + float(triangle["angles"]["b"])), ROUND_INDICATOR)
                sitec = round(float(triangle["sites"]["a"]) / sin(float(triangle["angles"]["b"])) * sin(anglec), ROUND_INDICATOR)
                triangle["angles"]["a"] = str(triangle["angles"]["a"]) + " oder " + str(anglea)
                triangle["angles"]["c"] = str(triangle["angles"]["c"]) + " oder " + str(anglec)
                triangle["sites"]["c"] = str(triangle["sites"]["c"]) + " oder " + str(sitec)
        else:
            # Return Error
            print("not Possible")

    elif triangle["sites"]["a"] != "" and triangle["sites"]["c"] != "" and triangle["angles"]["a"] != "":
        if sin(getRadianFromDegrees(float(triangle["angles"]["a"]))) * float(triangle["sites"]["c"]) / float(triangle["sites"]["a"]) >= -1 and sin(getRadianFromDegrees(float(triangle["angles"]["a"]))) * float(triangle["sites"]["c"])/ float(triangle["sites"]["a"]) <= 1:
            triangle["angles"]["c"] = round(getDegreesFromRadian(asin((sin(getRadianFromDegrees(float(triangle["angles"]["a"]))) * float(triangle["sites"]["c"])) / float(triangle["sites"]["a"]))), ROUND_INDICATOR)
            triangle["angles"]["b"] = round(180 - (float(triangle["angles"]["c"]) + float(triangle["angles"]["a"])), ROUND_INDICATOR)
            triangle["sites"]["b"] =  round(float(triangle["sites"]["a"]) / sin(float(triangle["angles"]["a"])) * sin(float(triangle["angles"]["b"])), ROUND_INDICATOR)
            if float(triangle["angles"]["a"]) < 90 and float(triangle["sites"]["a"]) < float(triangle["sites"]["c"]):
                anglec = round(180 - float(triangle["angles"]["c"]), ROUND_INDICATOR)
                angleb = round(180 - (anglec + float(triangle["angles"]["a"])), ROUND_INDICATOR)
                siteb = round(float(triangle["sites"]["a"]) / sin(float(triangle["angles"]["a"])) * sin(angleb), ROUND_INDICATOR)
                triangle["angles"]["c"] = str(triangle["angles"]["c"]) + " oder " + str(anglec)
                triangle["angles"]["b"] = str(triangle["angles"]["b"]) + " oder " + str(angleb)
                triangle["sites"]["b"] = str(triangle["sites"]["b"]) + " oder " + str(siteb)
        else:
            # Return Error
            print("not Possible")

    elif triangle["sites"]["a"] != "" and triangle["sites"]["c"] != "" and triangle["angles"]["c"] != "":
        if sin(getRadianFromDegrees(float(triangle["angles"]["c"]))) * float(triangle["sites"]["a"])/ float(triangle["sites"]["c"]) >= -1 and sin(getRadianFromDegrees(float(triangle["angles"]["c"]))) * float(triangle["sites"]["a"])/ float(triangle["sites"]["c"]) <= 1:
            triangle["angles"]["a"] = round(getDegreesFromRadian(asin((sin(getRadianFromDegrees(float(triangle["angles"]["c"]))) * float(triangle["sites"]["a"])) / float(triangle["sites"]["c"]))), ROUND_INDICATOR)
            triangle["angles"]["b"] = round(180 - (float(triangle["angles"]["c"]) + float(triangle["angles"]["a"])), ROUND_INDICATOR)
            triangle["sites"]["b"] =  round(float(triangle["sites"]["a"]) / sin(float(triangle["angles"]["a"])) * sin(float(triangle["angles"]["b"])), ROUND_INDICATOR)
            if float(triangle["angles"]["c"]) < 90 and float(triangle["sites"]["c"]) < float(triangle["sites"]["a"]):
                anglea = round(180 - float(triangle["angles"]["a"]), ROUND_INDICATOR)
                angleb = round(180 - (anglea + float(triangle["angles"]["c"])), ROUND_INDICATOR)
                siteb = round(float(triangle["sites"]["c"]) / sin(float(triangle["angles"]["c"])) * sin(angleb), ROUND_INDICATOR)
                triangle["angles"]["a"] = str(triangle["angles"]["a"]) + " oder " + str(anglea)
                triangle["angles"]["b"] = str(triangle["angles"]["b"]) + " oder " + str(angleb)
                triangle["sites"]["b"] = str(triangle["sites"]["b"]) + " oder " + str(siteb)

    elif triangle["sites"]["b"] != "" and triangle["sites"]["c"] != "" and triangle["angles"]["b"] != "":
        if sin(getRadianFromDegrees(float(triangle["angles"]["b"]))) * float(triangle["sites"]["c"]) / float(triangle["sites"]["b"]) >= -1 and sin(getRadianFromDegrees(float(triangle["angles"]["b"]))) * float(triangle["sites"]["c"])/ float(triangle["sites"]["b"]) <= 1:
            triangle["angles"]["c"] = round(getDegreesFromRadian(asin((sin(getRadianFromDegrees(float(triangle["angles"]["b"]))) * float(triangle["sites"]["c"])) / float(triangle["sites"]["b"]))), ROUND_INDICATOR)
            triangle["angles"]["a"] = round(180 - (float(triangle["angles"]["b"]) + float(triangle["angles"]["c"])), ROUND_INDICATOR)
            triangle["sites"]["a"] = round(float(triangle["sites"]["c"]) / sin(float(triangle["angles"]["c"])) * sin(float(triangle["angles"]["a"])), ROUND_INDICATOR)
            if float(triangle["angles"]["b"]) < 90 and float(triangle["sites"]["b"]) < float(triangle["sites"]["c"]):
                anglec = round(180 - float(triangle["angles"]["c"]), ROUND_INDICATOR)
                anglea = round(180 - (anglec + float(triangle["angles"]["b"])), ROUND_INDICATOR)
                sitea = round(float(triangle["sites"]["b"]) / sin(float(triangle["angles"]["b"])) * sin(anglea), ROUND_INDICATOR)
                triangle["angles"]["c"] = str(triangle["angles"]["c"]) + " oder " + str(anglec)
                triangle["angles"]["a"] = str(triangle["angles"]["a"]) + " oder " + str(anglea)
                triangle["sites"]["a"] = str(triangle["sites"]["a"]) + " oder " + str(sitea)

    elif triangle["sites"]["b"] != "" and triangle["sites"]["c"] != "" and triangle["angles"]["c"] != "":
        if sin(getRadianFromDegrees(float(triangle["angles"]["c"]))) * float(triangle["sites"]["b"]) / float(triangle["sites"]["c"]) >= -1 and sin(getRadianFromDegrees(float(triangle["angles"]["c"]))) * float(triangle["sites"]["b"])/ float(triangle["sites"]["c"]) <= 1:
            triangle["angles"]["b"] = round(getDegreesFromRadian(asin((sin(getRadianFromDegrees(float(triangle["angles"]["c"]))) * float(triangle["sites"]["b"])) / float(triangle["sites"]["c"]))), ROUND_INDICATOR)
            triangle["angles"]["a"] = round(180 - (float(triangle["angles"]["c"]) + float(triangle["angles"]["b"])), ROUND_INDICATOR)
            triangle["sites"]["a"] = round(float(triangle["sites"]["c"]) / sin(float(triangle["angles"]["c"])) * sin(float(triangle["angles"]["a"])), ROUND_INDICATOR)
            if float(triangle["angles"]["c"]) < 90 and float(triangle["sites"]["c"]) < float(triangle["sites"]["b"]):
                angleb = round(180 - float(triangle["angles"]["b"]), ROUND_INDICATOR)
                anglea = round(180 - (angleb + float(triangle["angles"]["c"])), ROUND_INDICATOR)
                sitea = round(float(triangle["sites"]["c"]) / sin(float(triangle["angles"]["c"])) * sin(anglea), ROUND_INDICATOR)
                triangle["angles"]["b"] = str(triangle["angles"]["b"]) + " oder " + str(angleb)
                triangle["angles"]["a"] = str(triangle["angles"]["a"]) + " oder " + str(anglea)
                triangle["sites"]["a"] = str(triangle["sites"]["a"]) + " oder " + str(sitea)
    return triangle


def getTriangleSAA(triangle):
    if triangle["angles"]["a"] == "":
        triangle["angles"]["a"] = 180 - (float(triangle["angles"]["b"]) + float(triangle["angles"]["c"]))
    elif triangle["angles"]["b"] == "":
        triangle["angles"]["b"] = 180 - (float(triangle["angles"]["a"]) + float(triangle["angles"]["c"]))
    elif triangle["angles"]["c"] == "":
        triangle["angles"]["c"] = 180 - (float(triangle["angles"]["a"]) + float(triangle["angles"]["b"]))


    if triangle["sites"]["a"] != "":
        triangle["sites"]["c"] =  round(float(triangle["sites"]["a"]) / sin(float(triangle["angles"]["a"])) * sin(float(triangle["angles"]["c"])), ROUND_INDICATOR)
        triangle["sites"]["b"] =  round(float(triangle["sites"]["a"]) / sin(float(triangle["angles"]["a"])) * sin(float(triangle["angles"]["b"])), ROUND_INDICATOR)

    elif triangle["sites"]["b"] != "":
        triangle["sites"]["a"] = round(float(triangle["sites"]["b"]) / sin(float(triangle["angles"]["b"])) * sin(float(triangle["angles"]["a"])), ROUND_INDICATOR)
        triangle["sites"]["c"] = round(float(triangle["sites"]["b"]) / sin(float(triangle["angles"]["b"])) * sin(float(triangle["angles"]["c"])), ROUND_INDICATOR)

    elif triangle["sites"]["c"] != "":
        triangle["sites"]["a"] = round(float(triangle["sites"]["c"]) / sin(float(triangle["angles"]["c"])) * sin(float(triangle["angles"]["a"])), ROUND_INDICATOR)
        triangle["sites"]["b"] = round(float(triangle["sites"]["c"]) / sin(float(triangle["angles"]["c"])) * sin(float(triangle["angles"]["b"])), ROUND_INDICATOR)
    return triangle


def getTriangleSSS(sa, sb, sc, triangle):

    if (float(sa)**2 + float(sb)**2 - float(sc)**2) / (2 * float(sa) * float(sb)) >= -1 and (float(sa)**2 + float(sb)**2 - float(sc)**2) / (2 * float(sa) * float(sb)) <= 1:
        if triangle["angles"]["c"] == "":
            triangle["angles"]["c"] = round((acos((float(sa)**2 + float(sb)**2 - float(sc)**2) / (2 * float(sa) * float(sb)))) / pi * 180, ROUND_INDICATOR)
        if triangle["angles"]["b"] == "":
            triangle["angles"]["b"] = round((acos((float(sc)**2 + float(sa)**2 - float(sb)**2) / (2 * float(sc) * float(sa)))) / pi * 180, ROUND_INDICATOR)
        if triangle["angles"]["a"] == "":
            triangle["angles"]["a"] = round((acos((float(sb)**2 + float(sc)**2 - float(sa)**2) / (2 * float(sb) * float(sc)))) / pi * 180, ROUND_INDICATOR)
        return triangle
    else:
        # Return Error
        print("Keine Lösung")

def has_info(triangle):
    sites_amount = getAmountEntries(triangle, "sites")
    angle_amount = getAmountEntries(triangle, "angles")
    if sites_amount == 3 and angle_amount == 3:
        return triangle
    elif sites_amount == 2 and angle_amount == 1:
        triangle = getTriangleSSA(triangle)
    elif sites_amount == 1 and angle_amount == 2:
        triangle = getTriangleSAA(triangle)
    elif sites_amount == 3 and angle_amount == 0:
        triangle = getTriangleSSS(triangle["sites"]["a"], triangle["sites"]["b"], triangle["sites"]["c"], triangle)
    else:
        # Return Error
        print("6")
    return triangle

@app.route("/")
def home(site_a = "", site_b = "", site_c = "", angle_a = "", angle_b = "", angle_c = "", right_angled = False, isosceles =  False, equilateral = False, height = "", area = "" ):
    return render_template("html/index.html", site_a = site_a, site_b = site_b, site_c = site_c, angle_a = angle_a, angle_b = angle_b, angle_c = angle_c, area = area)

@app.route("/form", methods=['POST'])
def recive_form():
    # try:
    global triangle
    triangle = {"sites": {"a": request.form['site_a'], "b": request.form['site_b'], "c": request.form['site_c']}, "angles": {"a": request.form['angle_a'], "b": request.form['angle_b'], "c": request.form['angle_c']}, "properties": {"right_angled": False, "isosceles": False, "equilateral": False, "height": 0, "area": 0}}
    print("Got Data: ", triangle)

    if checkForNegatives(triangle) != True or checkForAnglesMore180(triangle["angles"]) != True :

        triangle = has_info(triangle)
        #
        # # ob das rechteck RECHTWINKLIG ist
        # for angle in triangle["angles"]:
        #     if float(triangle["angles"][angle]) == 90:
        #         triangle["properties"]["right_angled"] = True
        #
        # # ob das dreieck GLEICHSCHENKLIG ist mit winkeln
        # if triangle["angles"]["a"] == triangle["angles"]["b"] or triangle["angles"]["a"] == triangle["angles"]["c"] or triangle["angles"]["b"] == triangle["angles"]["c"]:
        #     triangle["properties"]["isosceles"] = True
        #
        # # ob das dreieck GLEICHSEITIG ist
        # if triangle["sites"]["a"] == triangle["sites"]["b"] == triangle["sites"]["c"]:
        #     triangle["properties"]["equilateral"] = True
        # # except ValueError as e:
        # #     print("Value missing or not a number")
        # #     print("Error: ", e)
        # # finally:
        # #     print(triangle)

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
    else:
        return redirect(url_for("home"))

if __name__ == "__main__":
    app.run()
