import tkinter
from tkinter import *
from PIL import ImageTk
import pandas as pd
import openpyxl
from tkinter import ttk, filedialog
import face_recognition
import numpy as num
import cv2
import os
from datetime import datetime
from time import sleep
import csv

Registration=tkinter.Tk()
Registration.title("Attendance Manager")
Registration.minsize(500, 500)


Registration.rowconfigure(0, weight=1)
Registration.columnconfigure(0, weight=1)

Height=500
Width=500
rootHeight = Registration.winfo_height()/2
rootWidth = Registration.winfo_width()/2

frame1=tkinter.Frame(Registration)
frame2=tkinter.Frame(Registration)
frame3=tkinter.Frame(Registration)
frame4=tkinter.Frame(Registration)
frame5=tkinter.Frame(frame4)
frame6=tkinter.Frame(Registration)
frame7=tkinter.Frame(frame6)
frame8=tkinter.Frame(Registration)
frame9=tkinter.Frame(frame8)


details_tree=ttk.Treeview(frame5)
attendance_tree=ttk.Treeview(frame7)
checkatt_tree=ttk.Treeview(frame9)


def show_frame(frame):
    frame.tkraise()
def pack_tree(tree):
    tree.pack()
def unpack_tree(tree):
    tree.pack_forget

frame1_image=ImageTk.PhotoImage(file= 'img1.jpg')
bg_label=tkinter.Label(frame1, image=frame1_image)
bg_label.place(relwidth=1,relheight=1)

frame2_image=ImageTk.PhotoImage(file='img1.jpg')
bg_label=tkinter.Label(frame2, image=frame2_image)
bg_label.place(relwidth=1,relheight=1)

frame3_image=ImageTk.PhotoImage(file='img1.jpg')
bg_label=tkinter.Label(frame3, image=frame3_image)
bg_label.place(relwidth=1,relheight=1)


for frame in (frame1, frame2, frame3, frame4,frame5,frame6,frame7,frame8,frame9):
    frame.grid(row=0,column=0,stick='nsew')


checkatt_tree["columns"]=("abname")
checkatt_tree["show"]="headings"
checkatt_tree.column("abname",width=500)
checkatt_tree.heading("abname",text="Absent Students")

def check_absent():
    checkatt_tree.delete(*checkatt_tree.get_children())
    with open('attendance.csv') as file:
        attfile=csv.reader(file,delimiter=",")
        attendance_row=list(attfile)
        detfile=pd.read_excel('regdata.xlsx')
        SeriesRollNo=detfile['Roll No']
        
        for rollno in SeriesRollNo:
            count=0 
            for row in attendance_row:
                if(rollno == int(row[0])):
                    count=1
                    break
            if count==0:
                children=checkatt_tree.get_children()
                if not children:
                    checkatt_tree.insert("","end",values=(rollno))
                else:
                    for child in children:
                        array=checkatt_tree.set(child)
                        if(rollno == int(array["abname"])):
                            pass
                        else:
                            checkatt_tree.insert("","end",values=(rollno))
            else:
                pass

attendance_tree['columns']=("Roll No","Time")
attendance_tree['show']="headings"
attendance_tree.column("Roll No", width=250)
attendance_tree.column("Time", width=250)


def show_attendance_file():
    attendance_tree.delete(*attendance_tree.get_children())
    with open('attendance.csv') as file:
        attendance_file=csv.reader(file,delimiter=',')

        attendance_tree.heading("Roll No",text="Roll No")
        attendance_tree.heading("Time",text="Time")

        for row in attendance_file:
            attendance_tree.insert("","end",values=row)


def new_student():
    student_name=RollNo_entry.get()
    key = cv2.waitKey(1)
    webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    sleep(2)
    while True:
        try:
            ret, frame = webcam.read()
            print(ret)  # prints true as long as the webcam is running
            print(frame)  # prints matrix values of each framecd
            cv2.imshow("Capturing", frame)
            key = cv2.waitKey(1)
            if key == ord('s'):
                cv2.imwrite(filename="photos/" + student_name + ".jpg", img=frame)
                webcam.release()
                cv2.destroyAllWindows()
                break
            elif key == ord('q'):
                webcam.release()
                cv2.destroyAllWindows()
                break

        except KeyboardInterrupt:
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break

def attendance_management():
    listimages = []
    listnames = []
    mylist = []
    path = "photos"
    mylist = os.listdir(path)

    for cl in mylist:
        curImg = cv2.imread(f'{path}/{cl}')
        listimages.append(curImg)
        listnames.append(os.path.splitext(cl)[0])

    def encoding():
        encodelist = []
        global count
        count=0
        for image in listimages:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(image)
            if not len(encode):
                count=count+1
                print("can't be encoded and count is ",count)
            else:
                encodelist.append(encode[0])
        return encodelist

    face_encodings = encoding()

    def marknow(present_rollno):
        with open('Attendance.csv', 'r+') as f:
            myData = f.readlines()
            rollno_list = []
            for line in myData:
                entry = line.split(',')
                rollno_list.append(entry[0])
            if present_rollno not in rollno_list:
                now = datetime.now()
                dtstring = now.strftime('%H:%M:%S')
                f.writelines(f'\n{present_rollno},{dtstring}')

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while (True):
        success, img = cap.read()
        curFrameS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        curFrameS = cv2.cvtColor(curFrameS, cv2.COLOR_BGR2RGB)

        curFrameS_faceLoc = face_recognition.face_locations(curFrameS)
        curFrameS_encoding = face_recognition.face_encodings(curFrameS, curFrameS_faceLoc)

        for faceLoc, encodeFace in zip(curFrameS_faceLoc, curFrameS_encoding):
            encode_result = face_recognition.compare_faces(face_encodings, encodeFace)
            faceDis_result = face_recognition.face_distance(face_encodings, encodeFace)

            minIndex = num.argmin(faceDis_result)

            if (encode_result[minIndex]):
                present_rollno = listnames[minIndex+count].upper()
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, present_rollno, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                marknow(present_rollno)
        cv2.imshow('webcam', img)
        k=cv2.waitKey(1)
        if (k == ord('q')):
            break
    cap.release()
    cv2.destroyAllWindows()


#---------------------------------------------------CODE START FOR MAIN PAGE---------------------------------------------------------------


main_menu = Menu(Registration)
Registration.config(menu=main_menu)


option_menu= Menu(main_menu,tearoff=False)
option_menu.add_command(label="Registration", command=lambda:show_frame(frame2))
option_menu.add_command(label="Student Details", command=lambda:[show_frame(frame4),pack_tree(details_tree)])

admin_menu= Menu(main_menu,tearoff=False)
admin_menu.add_command(label="About Us")
admin_menu.add_command(label="Complaint")

main_menu.add_cascade(label="Menu",menu=option_menu)
main_menu.add_cascade(label="Help",menu=admin_menu)

mrk_atndc=tkinter.Button(frame1, text="Mark Attendance",command=lambda:attendance_management())
mrk_atndc.place(relx=0.30,rely=0.20,relwidth=0.40, relheight=0.1)

chab_button=tkinter.Button(frame1,text="Check Absent Students", command=lambda:[check_absent(),show_frame(frame8),pack_tree(checkatt_tree)])
chab_button.place(relx=0.12,rely=0.35,relwidth=0.35,relheight=0.08)

show_attendance=tkinter.Button(frame1, text="Show Attendance",command=lambda:[show_attendance_file(),show_frame(frame6),pack_tree(attendance_tree)])
show_attendance.place(relx=0.54,rely=0.35,relwidth=0.35, relheight=0.08)

reg_button=tkinter.Button(frame1, text="Registration",command=lambda:show_frame(frame2))
reg_button.place(relx=0.12,rely=0.55,relwidth=0.35, relheight=0.08)

showdata_button=tkinter.Button(frame1, text="Show Student Details",command=lambda:[show_frame(frame4),pack_tree(details_tree)])
showdata_button.place(relx=0.54,rely=0.55,relwidth=0.35, relheight=0.08)


exit_btn=tkinter.Button(frame1,text="Exit",command=exit)
exit_btn.place(relx=0.65,rely=0.8,relwidth=0.20,relheight=0.06)


#-------------------------------------- CODE START FOR REGISTRATION PAGE--------------------------------------


def submit_data():
    path="regdata.xlsx"
    df1 = pd.read_excel(path)
    
    SeriesA = df1['Name']
    SeriesB = df1['Course']
    SeriesC = df1['Branch']
    SeriesD = df1['Year']
    SeriesE = df1['Semester']
    SeriesF = df1['12 Passing Year']
    SeriesG = df1['Address']
    SeriesRN = df1['Roll No']

    A = pd.Series(Name_entry.get())
    B = pd.Series(Course_entry.get())
    C = pd.Series(Branch_entry.get())
    D = pd.Series(Year_entry.get())
    E = pd.Series(Sem_entry.get())
    F = pd.Series(SenSec_entry.get())
    G = pd.Series(Address_entry.get())
    RN = pd.Series(RollNo_entry.get())

    SeriesA = SeriesA.append(A)
    SeriesB = SeriesB.append(B)
    SeriesC = SeriesC.append(C)
    SeriesD = SeriesD.append(D)
    SeriesE = SeriesE.append(E)
    SeriesF = SeriesF.append(F)
    SeriesG = SeriesG.append(G)
    SeriesRN = SeriesRN.append(RN)

    df2 = pd.DataFrame({"Roll No":SeriesRN,"Name":SeriesA,"Course":SeriesB,"Branch":SeriesC,"Year":SeriesD,"Semester":SeriesE,"12 Passing Year":SeriesF,"Address":SeriesG})
    df2.to_excel(path, index=False)

RollNo_label=tkinter.Label(frame2, text="Roll No")
RollNo_label.place(relx=0.05,rely=0.45,relheight=0.05, relwidth=0.1)
RollNo_entry = tkinter.Entry(frame2)
RollNo_entry.place(relx=0.16,rely=0.45,relheight=0.05, relwidth=0.28)

Name_label=tkinter.Label(frame2, text="Name")
Name_label.place(relx=0.05,rely=0.05,relheight=0.05, relwidth=0.1)
Name_entry = tkinter.Entry(frame2)
Name_entry.place(relx=0.16,rely=0.05,relheight=0.05, relwidth=0.22)

Course_label = tkinter.Label(frame2, text="Course")
Course_label.place(relx=0.50, rely=0.05, relheight=0.05, relwidth=0.1)
Course_entry = tkinter.Entry(frame2)
Course_entry.place(relx=0.61, rely=0.05, relheight=0.05, relwidth=0.22)

Branch_label = tkinter.Label(frame2, text="Branch")
Branch_label.place(relx=0.05, rely=0.15, relheight=0.05, relwidth=0.1)
Branch_entry = tkinter.Entry(frame2)
Branch_entry.place(relx=0.16, rely=0.15, relheight=0.05, relwidth=0.22)

Year_label = tkinter.Label(frame2, text="Year")
Year_label.place(relx=0.50, rely=0.15, relheight=0.05, relwidth=0.1)
Year_entry = tkinter.Entry(frame2)
Year_entry.place(relx=0.61, rely=0.15, relheight=0.05, relwidth=0.15)

Sem_label = tkinter.Label(frame2, text="Semester")
Sem_label.place(relx=0.05, rely=0.25, relheight=0.05, relwidth=0.1)
Sem_entry = tkinter.Entry(frame2)
Sem_entry.place(relx=0.16, rely=0.25, relheight=0.05, relwidth=0.1)

SenSec_label = tkinter.Label(frame2, text="12th Passing Year")
SenSec_label.place(relx=0.50, rely=0.25, relheight=0.05, relwidth=0.2)
SenSec_entry = tkinter.Entry(frame2)
SenSec_entry.place(relx=0.71, rely=0.25, relheight=0.05, relwidth=0.22)

Address_label = tkinter.Label(frame2, text="Address")
Address_label.place(relx=0.05, rely=0.35, relheight=0.05, relwidth=0.1)
Address_entry = tkinter.Entry(frame2)
Address_entry.place(relx=0.16, rely=0.35, relheight=0.05, relwidth=0.6)

Submit_btn=tkinter.Button(frame2, text="Submit",bg="#5293F3", command=lambda:[submit_data(),new_student()])
Submit_btn.place(relx=0.05, rely=0.60, relheight=0.05, relwidth=0.22)

back_btn=tkinter.Button(frame2,text="Back",command=lambda:show_frame(frame1))
back_btn.place(relx=0.5,rely=0.8,relwidth=0.20,relheight=0.06)

exit_btn=tkinter.Button(frame2,text="Exit",command=exit)
exit_btn.place(relx=0.73,rely=0.8,relwidth=0.20,relheight=0.06)


#----------------------------------------CODE FOR STUDENT DATA--------------------------------------------------


df=pd.read_excel("regdata.xlsx")

details_tree["column"]=list(df.columns)
details_tree["show"]="headings"

for column in details_tree["column"]:
    details_tree.column(column,anchor=W,width=100)
    details_tree.heading(column, text=column)

df_rows=df.to_numpy().tolist()
for row in df_rows:
    details_tree.insert("","end",values=row)

back_btn=tkinter.Button(frame4,text="Back",command=lambda:[show_frame(frame1),unpack_tree(details_tree)])
back_btn.place(relx=0.5,rely=0.8,relwidth=0.20,relheight=0.06)

exit_btn=tkinter.Button(frame4,text="Exit",command=exit)
exit_btn.place(relx=0.73,rely=0.8,relwidth=0.20,relheight=0.06)

                                       #backbutton for frame6,frame8

back_btn=tkinter.Button(frame6,text="Back",command=lambda:show_frame(frame1))
back_btn.place(relx=0.5,rely=0.8,relwidth=0.20,relheight=0.06)

exit_btn=tkinter.Button(frame6,text="Exit",command=exit)
exit_btn.place(relx=0.73,rely=0.8,relwidth=0.20,relheight=0.06)

back_btn=tkinter.Button(frame8,text="Back",command=lambda:show_frame(frame1))
back_btn.place(relx=0.5,rely=0.8,relwidth=0.20,relheight=0.06)

exit_btn=tkinter.Button(frame8,text="Exit",command=exit)
exit_btn.place(relx=0.73,rely=0.8,relwidth=0.20,relheight=0.06)

show_frame(frame1)

Registration.mainloop()