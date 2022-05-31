#!/usr/bin/env python

from tkinter import *
import json
import requests
from tkinter import ttk
import tkinter.messagebox as msgbox
import re

root = Tk()
root.title("Nationwide Elantra N Locator")
root.geometry("1040x500+800+400")

root.resizable(True, True)

Label(root, text="Enter zipcode and Choose your preference").pack(side="top")
CCDict = {0: "XFB", 1: "C5G", 2: "S3B", 3: "WAW", 4: "YP5"}
TRDict = {0: "MANUAL", 1:"AUTO"}

def warning():
    msgbox.showwarning("Error", "Invalid Zipcode")

def errorOccur():
    msgbox.showwarning("Error", "Error Occured\nLeave note in GitHub discussion")

def badZip():
    msgbox.showwarning("Error", "Enter Zipcode")

def btncmd(event=None):
    try:
        parseJSON(zipText.get(), CCDict[ExtColor.get()],TRDict[Transmission.get()])
    except (RuntimeError, TypeError, OSError, KeyError, ConnectionError, ValueError, NameError):
        errorOccur()

def parseJSON(zip, color, trans):
    headers = {'referer': 'https://www.hyundaiusa.com/us/en/vehicles'}
    url = "https://www.hyundaiusa.com/var/hyundai/services/inventory/vehicleList.json?zip={}&year=2022&model=ELANTRAN&radius=3000".format(zip)
    resp = requests.get(url=url, headers=headers)
    data = resp.json()
    try:
        if data["HTTP Status Code"] == '400':
            badZip()
            return
    except KeyError:
        pass

    if data["data"][0]["dealerInfo"] == None:
        warning()
        return

    vehicleList = []
    for item in table.get_children():
        table.delete(item)
    index = 0

    dealerLength = len(data["data"][0]["dealerInfo"])
    statusdict = {"IR": "In route", "TN": "Transit", "AA": "At sea", "PA": "Port allocated", "DS": "Dealer Stock", "IT": "IT"}
    for i in range(dealerLength):
        if data["data"][0]["dealerInfo"][i]['vehicles'] is None:
            pass
        else:
            for j in range(len(data["data"][0]["dealerInfo"][i]['vehicles'])):
                if data["data"][0]["dealerInfo"][i]['vehicles'][j]['exteriorColorCd'] == color:
                    if data["data"][0]["dealerInfo"][i]['vehicles'][j]['transmissionDesc'] == trans:
                        Dealership = data["data"][0]["dealerInfo"][i]['dealerNm']
                        Location = "{}, {}".format(data["data"][0]["dealerInfo"][i]['state'], data["data"][0]["dealerInfo"][i]['zip'])
                        Distance = float(data["data"][0]["dealerInfo"][i]["distance"])
                        VIN = data["data"][0]["dealerInfo"][i]['vehicles'][j]['vin']
                        if data["data"][0]["dealerInfo"][i]['vehicles'][j]["PlannedDeliveryDate"] != None:
                            Arriving = re.search(r'[0-9]*-[0-9]*-[0-9]*',data["data"][0]["dealerInfo"][i]['vehicles'][j]["PlannedDeliveryDate"]).group(0)
                        else:
                            Arriving = ""
                        Status = statusdict[data["data"][0]["dealerInfo"][i]['vehicles'][j]["inventoryStatus"]]
                        vehicleList.append([Dealership, Location, Distance, VIN, Arriving, Status])
    vehicleList.sort(key = lambda x: x[2])
    for i in vehicleList:
        table.insert(parent="", index="end", iid=index, text='', values=(i[0], i[1], i[2], i[3], i[4], i[5]))
        index += 1

zipText = Entry(root, width=10)
zipText.pack()
#  enter your zipcode here
zipText.insert(0,"")
# Bind the Enter key to the Search function
root.bind('<Return>', btncmd)
btn1 = Button(root, fg="blue", text="Search", command=btncmd)
btn1.pack()

frame_Color = LabelFrame(root, text="Exterior Color")
frame_Color.pack(side="left")
ExtColor = IntVar()
ColorB = []
ColorDict = {0: "Performance Blue", 1: "Cyber Gray", 2: "Phantom Black", 3: "Ceramic White", 4: "Intense Blue"}
for i in range(len(ColorDict)):
    ColorB.append(Checkbutton(frame_Color, text=ColorDict[i], onvalue=i, variable=ExtColor))
    # enter exterior color here
    if ColorDict[i] == "Performance Blue":
        ColorB[i].select()
    ColorB[i].pack()

frame_Trans = LabelFrame(root, text="Transmission")
frame_Trans.pack(side="right", )
Transmission = IntVar()
TransB = []
TransDict = {0: "Manual", 1: "Automatic"}
for i in range(len(TransDict)):
    TransB.append(Checkbutton(frame_Trans, text=TransDict[i], onvalue=i, variable=Transmission))
    # enter transmission type here
    if TransDict[i] == "Automatic":
        TransB[i].select()
    TransB[i].pack()

frame_Search = LabelFrame(root, text="Result")
frame_Search.pack(side="bottom", fill="both", expand=True)
scroll = Scrollbar(frame_Search)
scroll.pack(side=RIGHT, fill=Y)
table = ttk.Treeview(frame_Search, yscrollcommand=scroll.set, height = 20)
table.pack()
scroll.config(command=table.yview)

table['columns'] = ("vehicle_Dealership", "vehicle_Location", "vehicle_Distance", "vehicle_VIN", "vehicle_Arriving", "vehicle_Status")

table.column("#0", width=0, stretch=NO)
table.column("vehicle_Dealership", anchor=CENTER, width=200)
table.column("vehicle_Location", anchor=CENTER, width=80)
table.column("vehicle_Distance", anchor=CENTER, width=80)
table.column("vehicle_VIN", anchor=CENTER, width=160)
table.column("vehicle_Arriving", anchor=CENTER, width=100)
table.column("vehicle_Status", anchor=CENTER, width=110)

table.heading("#0", text="", anchor=CENTER)
table.heading("vehicle_Dealership", text="Dealership", anchor=CENTER)
table.heading("vehicle_Location", text="Location", anchor=CENTER)
table.heading("vehicle_Distance", text="Distance", anchor=CENTER)
table.heading("vehicle_VIN", text="VIN", anchor=CENTER)
table.heading("vehicle_Arriving", text="Arriving", anchor=CENTER)
table.heading("vehicle_Status", text="Status", anchor=CENTER)

root.mainloop()
