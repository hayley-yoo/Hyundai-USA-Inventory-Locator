#!/usr/bin/env python

from operator import index
from tkinter import *
import json
import requests
from tkinter import ttk
import tkinter.messagebox as msgbox
import re

root = Tk()
root.update_idletasks()
root.title("U.S. Nationwide Elantra N Locator")
root.geometry("1040x500+800+400")

root.eval('tk::PlaceWindow . center')

root.resizable(True, True)

Label(root, text="Enter zipcode and choose your preferences").pack(side="top")
ColorCodeDict = {0: ["XFB", "Performance Blue"], 1: ["C5G", "Cyber Gray"], 2: ["S3B", "Phantom Black"], 3: ["WAW", "Ceramic White"], 4: ["YP5", "Intense Blue"]}
ColorNameDict = {"XFB": "Performance Blue", "C5G": "Cyber Gray", "S3B": "Phantom Black", "WAW": "Ceramic White", "YP5": "Intense Blue"}
# TRDict = {0: "MANUAL", 1:"AUTO"}
global data
global table
global TransType
global SelectedColors

def warning():
    msgbox.showwarning("Error", "Invalid Zipcode")

def errorOccur():
    msgbox.showwarning("Error", "Error Occured\nLeave note in GitHub discussion")

def blankZip():
    msgbox.showwarning("Error", "Enter Zipcode")

def copy(event):
    sel = table.selection() # get selected items
    root.clipboard_clear()  # clear clipboard
    # copy headers
    headings = [table.heading("#{}".format(i), "text") for i in range(len(table.cget("columns")) + 1)]
    root.clipboard_append("\t".join(headings) + "\n")
    for item in sel:
        # retrieve the values of the row
        values = [table.item(item, 'text')]
        values.extend(table.item(item, 'values'))
        # append the values separated by \t to the clipboard
        root.clipboard_append("\t".join(values) + "\n")

def callBackFunc():
    global TransType
    global SelectedColors
    TransType[0] = TransAuto.get()
    TransType[1] = TransManual.get()
    SelectedColors[0] = ColorCeramicWhite.get()
    SelectedColors[1] = ColorCyberGray.get()
    SelectedColors[2] = ColorIntenseBlue.get()
    SelectedColors[3] = ColorPerformanceBlue.get()
    SelectedColors[4] = ColorPhantomBlack.get()
    vehicleTableUpdate(SelectedColors, TransType)

def btncmd(event=None):
    if len(zipText.get()) == 5:
        try:
            parseJSON(zipText.get())
            callBackFunc()
        except (RuntimeError, TypeError, OSError, KeyError, ConnectionError, ValueError, NameError):
            errorOccur()
    elif zipText.get() == "":
        blankZip()
    else: warning()

def parseJSON(zip):
    global data
    headers = {'referer': 'https://www.hyundaiusa.com/us/en/vehicles'}
    url = "https://www.hyundaiusa.com/var/hyundai/services/inventory/vehicleList.json?zip={}&year=2022&model=ELANTRAN&radius=3000".format(zip)
    resp = requests.get(url=url, headers=headers)
    data = resp.json()
    try:
        if data["HTTP Status Code"] == '400'or data["status"] == '400':
            blankZip()
            return
    except KeyError:
        pass

    if data["data"][0]["dealerInfo"] == None:
        warning()
        return

def vehicleTableUpdate(color, trans):
    global data
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
                if data["data"][0]["dealerInfo"][i]['vehicles'][j]['exteriorColorCd'] in color:
                    if data["data"][0]["dealerInfo"][i]['vehicles'][j]['transmissionDesc'] in trans:
                        Dealership = data["data"][0]["dealerInfo"][i]['dealerNm']
                        Location = "{}, {}".format(data["data"][0]["dealerInfo"][i]['state'], data["data"][0]["dealerInfo"][i]['zip'])
                        Distance = float(data["data"][0]["dealerInfo"][i]["distance"])
                        VIN = data["data"][0]["dealerInfo"][i]['vehicles'][j]['vin']
                        Color = ColorNameDict[data["data"][0]["dealerInfo"][i]['vehicles'][j]['exteriorColorCd']]
                        Transmission = data["data"][0]["dealerInfo"][i]['vehicles'][j]['transmissionDesc']
                        if data["data"][0]["dealerInfo"][i]['vehicles'][j]["PlannedDeliveryDate"] != None:
                            Arriving = re.search(r'[0-9]*-[0-9]*-[0-9]*',data["data"][0]["dealerInfo"][i]['vehicles'][j]["PlannedDeliveryDate"]).group(0)
                        else:
                            Arriving = ""
                        Status = statusdict[data["data"][0]["dealerInfo"][i]['vehicles'][j]["inventoryStatus"]]
                        vehicleList.append([Dealership, Location, Distance, VIN, Color, Transmission, Arriving, Status])
    vehicleList.sort(key = lambda x: x[2])
    
    # Set colors for banded rows
    table.tag_configure("oddrow", background='#e8f3f8')
    table.tag_configure("evenrow", background='white')
    
    for i in vehicleList:
        # Determine if row is even or odd and tag so that we can use banded rows in the table
        if index % 2 == 0:
            table.insert(parent="", index="end", iid=index, text='', values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]), tags=('evenrow',))
        if index % 2 != 0:
            table.insert(parent="", index="end", iid=index, text='', values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]), tags=('oddrow',))
        index += 1
        frame_Search.configure(text=str(index) + " Elantra N records returned")

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
ColorPerformanceBlue = StringVar()
ColorCyberGray = StringVar()
ColorPhantomBlack = StringVar()
ColorCeramicWhite = StringVar()
ColorIntenseBlue = StringVar()
SelectedColors =[None] * 5
ColorB = []
ColorB.append(Checkbutton(frame_Color, text=ColorCodeDict[0][1], offvalue="", onvalue=ColorCodeDict[0][0], variable=ColorPerformanceBlue, command=callBackFunc))
ColorB[0].pack(anchor=NW)
ColorB.append(Checkbutton(frame_Color, text=ColorCodeDict[1][1], offvalue="", onvalue=ColorCodeDict[1][0], variable=ColorCyberGray, command=callBackFunc))
ColorB[1].pack(anchor=NW)
ColorB.append(Checkbutton(frame_Color, text=ColorCodeDict[2][1], offvalue="", onvalue=ColorCodeDict[2][0], variable=ColorPhantomBlack, command=callBackFunc))
ColorB[2].pack(anchor=NW)
ColorB.append(Checkbutton(frame_Color, text=ColorCodeDict[3][1], offvalue="", onvalue=ColorCodeDict[3][0], variable=ColorCeramicWhite, command=callBackFunc))
ColorB[3].pack(anchor=NW)
ColorB.append(Checkbutton(frame_Color, text=ColorCodeDict[4][1], offvalue="", onvalue=ColorCodeDict[4][0], variable=ColorIntenseBlue, command=callBackFunc))
ColorB[4].pack(anchor=NW)
# Set default exterior color to Performance Blue
ColorB[0].select()
ColorB[0].pack(anchor=NW)

frame_Trans = LabelFrame(root, text="Transmission")
frame_Trans.pack(side="right", )
TransManual = StringVar()
TransAuto = StringVar()
TransType = [None] * 2
TransB = []
TransB.append(Checkbutton(frame_Trans, text="Manual", offvalue="", onvalue="MANUAL", variable=TransManual, command=callBackFunc))
TransB[0].pack(anchor=NW)
TransB.append(Checkbutton(frame_Trans, text="Automatic", offvalue="", onvalue="AUTO", variable=TransAuto, command=callBackFunc))
TransB[1].pack(anchor=NW)
# Set default transmission type to Automatic
TransB[1].select()

frame_Search = LabelFrame(root, text=("Enter zip to return Elantra N records"))
frame_Search.pack(side="bottom", fill="both", expand=True)
scroll = Scrollbar(frame_Search)
scroll.pack(side=RIGHT, fill=Y)
table = ttk.Treeview(frame_Search, yscrollcommand=scroll.set, height = 20)
# Bind Ctrl + C to the 'Copy' command
table.bind('<Control-c>', copy)
table.pack()
scroll.config(command=table.yview)

table['columns'] = ("vehicle_Dealership", "vehicle_Location", "vehicle_Distance", "vehicle_VIN", "vehicle_Color", "vehicle_Transmission", "vehicle_Arriving", "vehicle_Status")

table.column("#0", width=0, stretch=NO)
table.column("vehicle_Dealership", anchor=CENTER, width=200)
table.column("vehicle_Location", anchor=CENTER, width=70)
table.column("vehicle_Distance", anchor=CENTER, width=60)
table.column("vehicle_VIN", anchor=CENTER, width=140)
table.column("vehicle_Color", anchor=CENTER, width=105)
table.column("vehicle_Transmission", anchor=CENTER, width=60)
table.column("vehicle_Arriving", anchor=CENTER, width=75)
table.column("vehicle_Status", anchor=CENTER, width=90)

table.heading("#0", text="", anchor=CENTER)
table.heading("vehicle_Dealership", text="Dealership", anchor=CENTER)
table.heading("vehicle_Location", text="Location", anchor=CENTER)
table.heading("vehicle_Distance", text="Distance", anchor=CENTER)
table.heading("vehicle_VIN", text="VIN", anchor=CENTER)
table.heading("vehicle_Color", text="Color", anchor=CENTER)
table.heading("vehicle_Transmission", text="Trans", anchor=CENTER)
table.heading("vehicle_Arriving", text="Arriving", anchor=CENTER)
table.heading("vehicle_Status", text="Status", anchor=CENTER)

root.mainloop()