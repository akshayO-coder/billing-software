from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql
from PIL import ImageTk
from tkinter import filedialog


window = Tk()
window.geometry("1350x700")
window.title("Billing")

user1nameVar = StringVar()
pass1wordVar = StringVar()



billsTV = ttk.Treeview(height=30,column=('Item Name','Quantity','Amount','size','rate'))

updateTV = ttk.Treeview(height=30, columns=('Names','Rates','types','StoredType'))

def quantityFieldListener(a,b,c):
    global quantityVar
    global costVar
    global itemRate
    quantity = quantityVar.get()
    if quantity != "":
        try:
            quantity=float(quantity)
            cost = quantity*itemRate
            quantityVar.set("%.2f"%quantity)
            costVar.set("%.2f"%cost)
        except ValueError:
            quantity=quantity[:-1]
            quantityVar.set(quantity)
    else:
        quantity=0
        quantityVar.set("%.2f"%quantity)

options = []
rateDict={}
itemVariable = StringVar()
quantityVar = StringVar()
itemRate =100
costVar = StringVar()
rateVar = StringVar()
rateVar.set("%.2f"%itemRate)

addItemNameVar = StringVar()
addItemRateVar = StringVar()
addItemTypeVar = StringVar()
storeOptions = ['IN STOCK','OUT STOCK']
addstoredVar = StringVar()
addstoredVar.set(storeOptions[0])
quantityVar.trace('w',quantityFieldListener)
# costVar.trace('w',costFieldListener)
itemLists = list()
totalCost=0.0
totalCostVar = StringVar()
totalCostVar.set(f'total cost is {totalCost}')
updateItemId=""


def updateItem():
    global addItemNameVar
    global addItemRateVar
    global addItemTypeVar
    global addstoredVar
    global updateItemId

    name = addItemNameVar.get()
    rate = addItemRateVar.get()
    Type = addItemTypeVar.get()
    storeType= addstoredVar.get()
    conn = pymysql.connect(host="localhost", user="root", passwd="", db="SA")
    cursor = conn.cursor()
    query = "update  itzlist set names='{}',rates='{}',types='{}',storedtype='{}' where namesid='{}'".format(name,rate,Type,storeType,updateItemId)
    cursor.execute(query)
    conn.commit()
    conn.close()

    addItemNameVar.set("")
    addItemRateVar.set("")
    addItemTypeVar.set("")
    getItemLists()

def getItemLists():
    records=updateTV.get_children()

    for element in records:
        updateTV.delete(element)

    conn = pymysql.connect(host="localhost", user="root", passwd="", db="SA")
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query="select * from itzlist"
    cursor.execute(query)
    data = cursor.fetchall()
    for row in data:
        updateTV.insert('','end',text=row['namesid'],values=(row['names'],row['rates'],row['types'],row['storedtype']))
    updateTV.bind("<Double-1>",OnDoubleClick)

    conn.close()



def generate_bill():
    global itemVariable
    global quantityVar
    global itemRate
    global amountVar
    global itemLists
    global totalCost
    global totalCostVar
    itemName = itemVariable.get()
    quantity=quantityVar.get()
    amount = costVar.get()
    conn = pymysql.connect(host="localhost", user="root", passwd="", db="SA")
    cursor = conn.cursor()

    query="insert into bill (name,quantity, rate, amount) values('{}','{}','{}','{}')".format(itemName,quantity,itemRate,amount)
    cursor.execute(query)
    conn.commit()
    conn.close()
    listDict = {"name":itemName, "rate":itemRate,"quantity":quantity, "amount":amount}
    itemLists.append(listDict)
    totalCost+=float(amount)
    quantityVar.set("0")
    costVar.set("0")
    # updateBillsData()
    updateListView()
    print(totalCost)
    totalCostVar.set("Total Cost = {}".format(totalCost))

def updateListView():
    records = billsTV.get_children()

    for element in records:
        billsTV.delete(element)

    for row in itemLists:
        billsTV.insert('', 'end',text=row['name'],values=(row["rate"],row["quantity"],row["amount"]))


def updateBillsData():
    records = billsTV.get_children()

    for element in records:

        billsTV.delete(element)


    conn = pymysql.connect(host="localhost", user="root", passwd="", db="SA")
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    query = "select * from bill"
    cursor.execute(query)
    data = cursor.fetchall()

    for row in data:
        billsTV.insert('', 'end',text=row['name'],values=(row["rate"],row["quantity"],row["amount"]))
    conn.close()


def LogOut():
    remove_all_widgets()
    loginWindow()

def movetoBills():
    remove_all_widgets()
    viewAllBills()


def print_bill():
    global itemLists
    global totalCost

    billString = ""
    billString+="=====================Receipt==========================\n\n"
    billString+="======================================================\n"
    billString+="{:<20}{:<10}{:<15}{:<10}\ns".format("Name", "Rate", "Quantity", "amount")
    billString+="======================================================\n"




    for item in itemLists:
        billString+="{:<20}{:<10}{:<15}{:<10}\n".format(item["name"],item["rate"],item["quantity"],item["amount"])

    billString+="======================================================\n"
    billString+="{:<20}{:<10}{:<15}{:<10}\n".format("Total Cost"," "," ",totalCost)

    # window.billString =  filedialog.asksaveasfilename(initialdir = "/home/aaron/Desktop",title = "Select file",filetypes = (("jpeg files","*.txt"),("all files","*.*")))
    # print(window.billString)

    with open('/home/aaron/Desktop/akshay/bill.txt',mode='a') as file:
        text = file.write(billString)

    # with open('/home/aaron/Desktop/akshay/bill.txt',mode='a') as file2:
        # text2 = file2.write(file2)
        # file2.writelines(lines)

    # window.billFile = filedialog.asksaveasfilename(initialdir = "/",title = "billing file",filetypes= (('text files','*.txt'),('all files','*.*')))

    # window.filename =  filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*"))

    # oot.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    # if billFile is None:
    #     messagebox.showerror("Invalid file Name", "Please enter valid name")
    # # else:
    # window.billFile.write(billString)
    # window.billFile.close()
    #
    # print(window.billFile)


    itemLists =[]
    totalCost=0.0
    updateListView()
    totalCostVar.set("Total Cost = {}".format(totalCost))


def OnDoubleClick(event):
    global addItemNameVar
    global addItemRateVar
    global addItemTypeVar
    # global addstoredVar
    global updateItemId
    item = updateTV.selection()
    updateItemId= updateTV.item(item,"text")
    item_detail= updateTV.item(item,"values")
    item_index=storeOptions.index(item_detail[3])
    addItemTypeVar.set(item_detail[2])
    addItemRateVar.set(item_detail[1])
    addItemNameVar.set(item_detail[0])
    addstoredVar.set(storeOptions[item_index])
    print(item_index)

def readAllData():
    global options
    global rateDict
    global itemVariable
    global itemRate
    global rateVar
    options=[]
    rateDict={}
    conn = pymysql.connect(host="localhost", user="root", passwd="", db="SA")
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    query = "select * from itzlist"
    cursor.execute(query)
    data = cursor.fetchall()
    count=0
    for row in data:
        count+=1
        options.append(row['namesid'])
        rateDict[row['namesid']]=row['rates']
        itemVariable.set(options[0])
        itemRate=int(rateDict[options[0]])
    conn.close()
    rateVar.set("%.2f"%itemRate)
    if count ==0:
        remove_all_widgets()
        itemAddWindow()
    else:
        remove_all_widgets()
        mainwindow()

def optionMenuListener(event):
    global itemVariable
    global rateDict
    global itemRate
    item = itemVariable.get()
    itemRate= int(rateDict[item])
    rateVar.set("%.2f"%itemRate)

def addItemListener():
    remove_all_widgets()
    itemAddWindow()



def addItem():
    global addItemNameVar
    global addItemRateVar
    global addItemTypeVar
    global addstoredVar
    names = addItemNameVar.get()
    rates = addItemRateVar.get()
    Types = addItemTypeVar.get()
    storedType= addstoredVar.get()
    namesId=names.replace(" ","_")
    conn = pymysql.connect(host="localhost", user="root", passwd="", db="SA")
    cursor = conn.cursor()
    query = "insert into itzlist (names,namesid,rates,types,storedtype) value('{}','{}','{}','{}','{}')".format(names, namesId, rates, Types, storedType)
    cursor.execute(query)
    conn.commit()
    conn.close()
    addItemNameVar.set("")
    addItemRateVar.set("")
    addItemTypeVar.set("")



def loginWindow():

    titleLabel = Label(window,text=" Billing Software",font="Arial 40",fg="black")
    titleLabel.grid(row=2,column=6,columnspan=1, padx=(15,0),pady=(10,0))

    loginLabel = Label(window,text="Admin Login",font="Arial 30")
    loginLabel.grid(row=2, column=6,padx=(50,0),columnspan=2, pady=(120,0))

    usernameLabel = Label(window, text="Username",font=('new roman',14,'bold'))
    usernameLabel.grid(row=4, column=4,padx=10)

    passwordLabel = Label(window, text="Password",font=('new roman',14,'bold'))
    passwordLabel.grid(row=5, column=4,padx=10)

    usernameEntry= Entry(window, textvariable=user1nameVar)
    usernameEntry.grid(row=4, column=6,padx=(25,0),pady=5)

    passwordEntry = Entry (window, textvariable=pass1wordVar,show="*")
    passwordEntry.grid(row=5,column=6,padx=(25,0),pady=5)

    loginButton=Button(window, text="Login",width=20,relief=GROOVE, fg='white',bg='red',height=2,font=('new roman',10,'bold'), command=lambda:adminLogin())
    loginButton.grid(row=6, column=6,padx=(20,0),pady=(10,0))

bg_img = ImageTk.PhotoImage(file='20202.jpg')
bg_label= Label(window,image=bg_img).grid(row=2,column=0,padx=(100,0))

bg_img1 = ImageTk.PhotoImage(file='20201.jpg')
bg_label1= Label(window,image=bg_img1).grid(row=2,column=8,padx=(100,0))


def remove_all_widgets():
    global window
    for widget in window.winfo_children():
        widget.grid_remove()

def updateBillsData():
    records = billsTV.get_children()

    for element in records:

        billsTV.delete(element)


    conn = pymysql.connect(host="localhost", user="root", passwd="", db="SA")
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    query = "select * from bill"
    cursor.execute(query)
    data = cursor.fetchall()

    for row in data:
        billsTV.insert('', 'end',text=row['name'],values=(row["rate"],row["quantity"],row["amount"]))
    conn.close()


def adminLogin():
    global usernameVar
    global passwordVar

    user1name = user1nameVar.get()
    pass1word = pass1wordVar.get()

    conn = pymysql.connect(host="localhost", user="root", passwd="", db="SA")
    cursor = conn.cursor()

    query = "select * from us1 where user1name='{}' and pass1word='{}'".format(user1name, pass1word)
    cursor.execute(query)
    data = cursor.fetchall()
    admin = False
    for row in data:
        admin = True
    conn.close()
    if admin:
        readAllData()
    else:
        messagebox.showerror("Invalid user", "Credentials enters are invalid")

def moveToUpdate():
    remove_all_widgets()
    updateItemWindow()

def mainwindow():
    titleLabel = Label(window, text="Billing System", font="Arial 30", fg="white",bg='black')
    titleLabel.grid(row=0, column=1, columnspan=3, padx=(400, 0),pady=(10,0))

    addNewItem = Button(window, text="Add Item",fg='black',bg='white',font=('new roman',10,'bold'), width=14, height=2, command=lambda : addItemListener())
    addNewItem.grid(row=1, column=0, padx=(10, 0), pady=(10, 0))

    updateItem = Button(window, text="Update Item",fg='black',bg='white',font=('new roman',10,'bold'), width=15, height=2, command=lambda: moveToUpdate())
    updateItem.grid(row=1, column=1, padx=(10, 0), pady=(10, 0))

    showall_Entry = Button(window, text="show entries",fg='black',bg='white',font=('new roman',10,'bold'), width=15, height=2,command=lambda:movetoBills())
    showall_Entry.grid(row=1, column=2, padx=(150, 0), pady=(10, 0))

    logoutBtn = Button(window, text="Logout",fg='black',bg='white',font=('new roman',10,'bold'), width=14, height=2, command=lambda: LogOut())
    logoutBtn.grid(row=1, column=4, pady=(10, 0),padx=(350,0))

    itemLabel = Label(window, text="Select Item",font=('new roman',10,'bold'))
    itemLabel.grid(row=2, column=0, padx=(5, 0), pady=(10, 0))
    #
    itemDropDown = OptionMenu(window, itemVariable, *options,command=optionMenuListener)  # for list options
    itemDropDown.grid(row=2, column=1, padx=(10, 0), pady=(10, 0))
    #
    rateLabel = Label(window, text="Rate",font=('new roman',10,'bold'))
    rateLabel.grid(row=2, column=2, padx=(10, 0), pady=(10, 0))
    rateValue = Label(window, textvariable=rateVar)
    rateValue.grid(row=2, column=3, padx=(10, 0), pady=(10, 0))
    #
    quantityLabel = Label(window, text="Quantity",font=('new roman',10,'bold'))
    quantityLabel.grid(row=3, column=0, padx=(5, 0), pady=(10, 0))
    quantityEntry = Entry(window, textvariable=quantityVar,width=15)
    quantityEntry.grid(row=3, column=1, padx=(5, 0), pady=(10, 0))
    #
    costLabel = Label(window, text="Amount",font=('new roman',10,'bold'))
    costLabel.grid(row=3, column=2, padx=(10, 0), pady=(10, 0))
    costEntry = Entry(window, textvariable=costVar)
    costEntry.grid(row=3, column=3, padx=(10, 0), pady=(10, 0))
    #
    buttonBill = Button(window, text="Add to List", fg='black',bg='white',font=('new roman',10,'bold'),width=15,command=lambda:generate_bill())
    buttonBill.grid(row=2, column=4, padx=(40, 0), pady=(10, 0))
    #
    billLabel = Label(window, text="Bills", font=("new roman", 15))
    billLabel.grid(row=4, column=2)
    #
    billsTV.grid(row=5, column=0, columnspan=5)
    #
    scrollBar = Scrollbar(window, orient="vertical", command=billsTV.yview)
    scrollBar.grid(row=5, column=4, sticky="NSE")
    #
    billsTV.configure(yscrollcommand=scrollBar.set)
    #
    billsTV.heading('#0', text="ITEM NAME")
    billsTV.heading('#1', text="RATE")
    billsTV.heading('#2', text="QUANTITY")
    billsTV.heading('#3', text="TOTAL")
    billsTV.heading('#4', text="AMOUNT")
    billsTV.heading('#5',text="SIZE")

    # totalCostLabel = Label(window, textvariable=totalCostVar)
    # totalCostLabel.grid(row=6,column=1)
    totalCostLabel = Label(window, textvariable=totalCostVar,font=('new roman',10,'bold'))
    totalCostLabel.grid(row=3,column=4,padx=(10,0),pady=(10,0))
    generateBill = Button(window, text="Generate Bill",bg='green',fg='white',font=('new roman',10,'bold'), width=14, height=2,command=lambda:print_bill())
    generateBill.grid(row=3,column=4,padx=(350,0),pady=(10,0))

    updateListView()

def itemAddWindow():
    backButton = Button(window, text="Back",font=('new roman',10,'bold'), command=lambda: readAllData())
    backButton.grid(row=0, column=1)
    titleLabel = Label(window, text=" Billing System", width=40, font=('new roman',18,'bold'), fg="black")
    titleLabel.grid(row=0, column=2, columnspan=4, pady=(10, 0),padx=(270,0))

    itemNameLabel = Label(window, text="Name",font=('new roman',12,'bold'))
    itemNameLabel.grid(row=1, column=1, pady=(10, 0),padx=(10,0))
    itemNameEntry = Entry(window, textvariable=addItemNameVar)
    itemNameEntry.grid(row=1, column=2, pady=(10, 0))
    #
    itemRateLabel = Label(window, text="Amount",font=('new roman',12,'bold'))
    itemRateLabel.grid(row=1, column=3, pady=(10, 0))
    itemRateEntry = Entry(window, textvariable=addItemRateVar)
    itemRateEntry.grid(row=1, column=4, pady=(10, 0))
    #
    itemtypeLabel = Label(window, text="Type",font=('new roman',12,'bold'))
    itemtypeLabel.grid(row=2, column=1, pady=(10, 0))
    itemTypeEntry = Entry(window, textvariable=addItemTypeVar)
    itemTypeEntry.grid(row=2, column=2, pady=(10, 0))
    #
    storeTypeLabel = Label(window, text="Stored Type",font=('new roman',12,'bold'))
    storeTypeLabel.grid(row=2, column=3, pady=(10, 0))
    storeEntry = OptionMenu(window, addstoredVar, *storeOptions)
    storeEntry.grid(row=2, column=4, pady=(10, 0))
    #
    AddItemButton = Button(window, text="Add Item", width=20,font=('new roman',10,'bold'),fg='black',bg='white', height=2,command=lambda:addItem())
    AddItemButton.grid(row=3, column=3, pady=(10, 0))


def updateItemWindow():
    backButton = Button(window, text="Back" , command=lambda:readAllData())
    backButton.grid(row=0, column=1)
    titleLabel = Label(window,text="WE-UP DEVELOPERS", width=40,font="Arial 30",fg="black",bg='white')
    titleLabel.grid(row=0,column=2,columnspan=4,pady=(10,0))

    itemNameLabel= Label(window, text="Name")
    itemNameLabel.grid(row=1, column=1, pady=(10,0))

    itemNameEntry= Entry(window, textvariable=addItemNameVar)
    itemNameEntry.grid(row=1, column=2, pady=(10,0))

    itemRateLabel= Label(window, text="Rate")
    itemRateLabel.grid(row=1, column=3, pady=(10,0))

    itemRateEntry= Entry(window, textvariable=addItemRateVar)
    itemRateEntry.grid(row=1, column=4, pady=(10,0))


    itemtypeLabel= Label(window, text="Type")
    itemtypeLabel.grid(row=2, column=1, pady=(10,0))
    itemTypeEntry= Entry(window, textvariable=addItemTypeVar)
    itemTypeEntry.grid(row=2, column=2, pady=(10,0))

    storeTypeLabel= Label(window, text="Stored Type")
    storeTypeLabel.grid(row=2, column=3, pady=(10,0))
    storeEntry= OptionMenu(window, addstoredVar,*storeOptions)
    storeEntry.grid(row=2, column=4, pady=(10,0))

    AddItemButton = Button(window, text="Update Item", width=20, height=2, command=lambda:updateItem())
    AddItemButton.grid(row=3, column=3,pady=(10,0))

    updateTV.grid(row=4,column=0, columnspan=5)
    scrollBar = Scrollbar(window, orient="vertical", command=billsTV.yview)
    scrollBar.grid(row=5, column=4, sticky="NSE")
    #
    updateTV.configure(yscrollcommand=scrollBar.set)
    #
    updateTV.heading('#0', text="Names ID")
    updateTV.heading('#1', text="Names")
    updateTV.heading('#2', text="Rates")
    updateTV.heading('#3', text="Types")
    updateTV.heading('#4', text="StoredType")
    # updateTV.heading('#5',text="SIZE")
    getItemLists()

def viewAllBills():
    backButton = Button(window, text="Back" , command=lambda:readAllData())
    backButton.grid(row=0, column=1)
    titleLabel = Label(window,text="WE-UP DEVELOPERS", width=40,font=('new roman',12,'bold'),fg='white',bg='white')
    titleLabel.grid(row=0,column=2,columnspan=4,pady=(10,0))
    billsTV.grid(row=1, column=0, columnspan=5)

    scrollBar = Scrollbar(window, orient="vertical",command=billsTV.yview)
    scrollBar.grid(row=1, column=4, sticky="NSE")

    billsTV.configure(yscrollcommand=scrollBar.set)

    billsTV.heading('#0',text="Item Name")
    billsTV.heading('#1',text="Rate")
    billsTV.heading('#2',text="Quantity")
    billsTV.heading('#3',text="Amount")

    updateBillsData()

loginWindow()
# itemAddWindow()
window.mainloop()
