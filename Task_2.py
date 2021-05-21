# The Sparks Foundation
# Color Identification in Images
# GRIPMAY21
# Mihir Goyenka

import numpy as np
import pandas as pd
import cv2
import requests

# download csv file
url = "https://raw.githubusercontent.com/codebrainz/color-names/master/output/colors.csv"
res = requests.get(url, allow_redirects=True)
with open('colors.csv', 'wb') as file:
    file.write(res.content)
colors = pd.read_csv('colors.csv')

img = cv2.imread("img1.jpeg")

index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

clicked = False
r = g = b = xpos = ypos = 0


def identify_color(R, G, B):
    global cname
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname


def mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


cv2.namedWindow('Color Identification')
cv2.setMouseCallback('Color Identification', mouse_click)

while 1:
    cv2.imshow("Color Identification", img)
    if clicked:
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
        text = identify_color(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
        clicked = False

    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
