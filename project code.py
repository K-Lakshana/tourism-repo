from tkinter import *
import mysql.connector
import cv2
from PIL import Image, ImageTk
from tkinter import ttk

start = Tk()
start.attributes('-fullscreen',True)
cap = cv2.VideoCapture("Video.mp4")
canvas = Canvas(start,width=500,height=1000)
canvas.pack()

while True:
    ret,frame = cap.read()
    if not ret:
        break
    
    # Convert the frame to a Tkinter-compatible image
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (500,1000))
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(image=img)
    
    # Update the canvas with the new image
    canvas.create_image(0, 0, anchor=NW, image=img)
    start.update()
    
    # Wait for few milliseconds, then move on to the next frame
    start.after(10, cap.read)
cap.release()
cv2.destroyAllWindows()
canvas.destroy()

def destroy():
    start.destroy()

def start_window():
    global start,start_button,bg,photo

    #Adding background image
    bg=PhotoImage(file='BG.png')
    photo=Label(start,image=bg)
    photo.place(x=310,y=0)

    #Creating close buttons
    exit_button=Button(start,text=' X ',command=destroy,bg='red',font=(20))
    exit_button.pack(side='top',anchor='se')
    
    #Creatiing start buttons
    start_button=Button(start,text='Open',command=begin,font=('Segoe UI Variable Text',20))
    start_button.pack(side='top',anchor='center')
    mainloop()
        
def begin():
    global start,label,scrollbar,listbox,btn,bg,photo

    #Destroying start window
    start_button.destroy()

    #Select type label
    label=Label(start,text='Select place type:',font=('Segoe UI Variable Text',20))
    label.pack(side='top',anchor='nw')
    
    #types scrollbar
    scrollbar=Scrollbar(start)
    scrollbar.pack(side=LEFT,fill=BOTH)

    #types listbar
    listbox=Listbox(start,yscrollcommand=scrollbar.set,font=('Segoe UI Variable Text',15))
    for i in ['Hillstation','Beach','Falls','Heritage Site']:
        listbox.insert(END,i)

    #place_type select button
    btn=Button(start,text='select',command=input_place_type,font=('Segoe UI Variable Text',20))
    btn.pack(anchor='nw',side='bottom')

    listbox.pack(side=LEFT,fill=BOTH)

    scrollbar.config(command=listbox.yview)
    scrollbar.pack()

    mainloop()
        
def input_place_type():
    global scrollbar,btn,label,label2,start,place_type

    #Storing selected type in variable 'type'
    for i in listbox.curselection():
            place_type=listbox.get(i)
    if len(listbox.curselection())==0:
        place_type='Any type'
    
    #Closing
    scrollbar.destroy()
    btn.destroy()
    label.destroy()
    listbox.destroy()

    #Displaying entered place_type
    label2=Label(start,text='Entered place_type: '+place_type,font=('Segoe UI Variable Text',20))
    label2.pack(anchor='nw')
    input_state()

def input_state():
    global start,label3,scrollbar2,listbox,btn2

    #Select state label
    label3=Label(start,text='Select the state which you wish to :',font=('Segoe UI Variable Text',20))
    label3.pack(side=LEFT,anchor='nw')

    #Cities scrollbar
    scrollbar2=Scrollbar(start,orient='vertical')
    scrollbar2.pack(side=LEFT,fill=BOTH)

    #Cities listbar
    listbox=Listbox(start,yscrollcommand=scrollbar2.set,font=('Segoe UI Variable Text',15))
    for i in ['Tamil Nadu','Kerala','Andhra Pradesh','Karnataka','Telengana','Goa']:
        listbox.insert(END,i)

    #state select button
    btn2=Button(start,text='select',command=state_listbox,font=('Segoe UI Variable Text',20))
    btn2.pack(anchor='sw',side='bottom')

    listbox.pack(side=LEFT,fill=BOTH)
    
    scrollbar2.config(command=listbox.yview)
    scrollbar2.pack()

    mainloop()
    
def state_listbox():
    global listbox,btn3,label4,state,max_distance

    #Storing selected type in variable 'state'
    for i in listbox.curselection(): #listbox.curselection() stores the selected state's index 
            state=listbox.get(i)      #in a single-element tuple
    if len(listbox.curselection())==0:
        state='Any state'
        
    #Destroying
    scrollbar2.destroy()
    btn2.destroy()
    label3.destroy()
    listbox.destroy()

    #Displaying entered state
    label4=Label(start,text='Entered state: '+state,font=('Segoe UI Variable Text',20))
    label4.pack(anchor='nw')

    btn3=Button(start,text='show places',command=display_places,font=('Segoe UI Variable Text',20))
    btn3.pack(anchor='sw',side='top')

def display_places():  
    log = Toplevel(start,bg='Light Green')
    log.transient(start)
    log.title('Destination Suggestions')

    # setup treeview
    columns = ('Place','Type','District','State')
    tree = ttk.Treeview(log, height=20, columns=columns, show='headings')
    tree.grid(row=0, column=0, sticky='news')
    style=ttk.Style()
    style.configure('Treeview.Heading',font=('Segoe UI Variable Text',18))
    
    # setup columns attributes
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=200, anchor=CENTER)

    #Retrieving data from Database 'project'
    my_conn=mysql.connector.connect(host='localhost',user='root',passwd='unicornsquad')
    
    cursor=my_conn.cursor()
    cursor.execute('use project')
   
    if state!='Any state' and place_type!='Any type':
        cursor.execute("select * from TOUR where STATE='{}' and PLACE_TYPE='{}'".format(state,place_type))
    elif state=='Any state' and place_type!='Any type':
        cursor.execute("select * from TOUR where PLACE_TYPE='{}'".format(place_type))
    elif state!='Any state' and place_type=='Any type':
        cursor.execute("select * from TOUR where STATE='{}'".format(state))
    else:
        cursor.execute("select * from TOUR")
        
    # populate data to treeview
    for rec in cursor:
        tree.insert('', 'end', value=rec)

    # scrollbar
    sb = Scrollbar(log, orient=VERTICAL, command=tree.yview)
    sb.grid(row=0, column=1, sticky='ns')
    tree.config(yscrollcommand=sb.set)

    btn = Button(log, text='Exit', command=log.destroy, width=20, bd=2, fg='#eb4d4b')
    btn.grid(row=1, column=0, columnspan=2)
    
start_window()
#the end