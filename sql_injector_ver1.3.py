from math import floor
from Tkinter import *
import tkFileDialog
import tempfile

def createSQLQuery(sql_statement, idSize, path_in):
    identifiers = []

    with open(path_in,'r') as f:
        for line in f:
           identifiers.append(line[0:idSize])
            
    size = len(identifiers)
    print("identifiers count: " + str(size))

    if identifiers[size-1].endswith(',') == True:
        identifiers[size-1] = identifiers[size-1].replace(',','')

    if sql_statement.endswith(';') == True:
        sql_statement[size-1] = '';

    sql_to_list = []

    for i in range(len(sql_statement)):
        sql_to_list.append(sql_statement[i])


    if size >= 1000:
        chunks = int(floor(size / 1000)) + 1
    else:
        chunks = 2

    print("chunk size: " + str(chunks))
    final_query1 = []

    for i in range(chunks):
        final_query1.append([])

    itr1 = 0

    for j in range(chunks):

        if j == 0:
            final_query1[j].append("select * from (\n")
        else:
            
            for i in range(len(sql_to_list)):
                
                if j > 0 and i == 0:
                    final_query1[j].append("(")
                
                final_query1[j].append(sql_to_list[i])
                
                if sql_to_list[i] =='(' and itr1 < size:
                    itr2 = 0
                    remainder = size-itr1
                    print("remainder: " + str(remainder))
                    if remainder > 1000:
                        while itr2 < 1000:
                            if identifiers[itr1].endswith(',') != True and itr2 != 999:
                                identifiers[itr1] = identifiers[itr1] + ',\n'
                            final_query1[j].append(identifiers[itr1])
                            itr1 = itr1 + 1
                            itr2 = itr2 + 1
                    else:
                        while itr1 < size:
                            if identifiers[itr1].endswith(',') != True and itr2 != remainder-1:
                                identifiers[itr1] = identifiers[itr1] + ',\n'
                            final_query1[j].append(identifiers[itr1])
                            itr1 = itr1 + 1
                            itr2 = itr2 + 1
                    
                    
        if j != 0 and j != chunks-1:
            final_query1[j].append(") union all \n")
        elif j == chunks-1:
            final_query1[j].append("));")
                
    print("itr1: " + str(itr1))

    savedFile = tkFileDialog.asksaveasfile(initialfile = "new.sql", initialdir = "/",title = "Select file",filetypes = (("SQL files","*.sql"),("all files","*.*")))

    for i in range(chunks):
        for j in range(len(final_query1[i])):
            savedFile.write(final_query1[i][j])
        if i == chunks - 1:
            print("i: " + str(i))
    savedFile.close()
    print("done check!")
        
  



class Application(Frame):

    def only_numbers(self, char):
        return char.isdigit()

    def characterLimit(self, entry):
        if len(entry.get()) > 0:
            entry.set(entry.get()[:3])
        
    def getInputFile(self):
        self.path_in = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("text files","*.txt"),("csv files","*.csv"),("all files","*.*")))

    def validateSQL(self, query):
        valid = False

        if query.upper()[0:6] == 'SELECT' and (query.upper().find("IN()") != -1 or query.upper().find("IN ()") != -1):
            valid = True


        return valid
        

    def reset(self):
        self.frame.destroy()
        self.createMenu()
        
    def generateQuery(self):

        self.browseErrorText.set(" ")
        self.idLengthErrorText.set(" ")
        self.sql_queryErrorText.set(" ")
        
        idSize = int(0 if self.idLengthInputText.get() == "" else self.idLengthInputText.get())
        print("idSize: " + str(idSize))
        sql_query_statement = self.sql_query_Text.get('1.0','end')


        nxt1 = False
        nxt2 = False
        nxt3 = False

        if self.path_in == "":
             self.browseErrorText.set("File not selected!")
             nxt1 = False
        else:
            nxt1 = True
            
        if idSize <= 0:
            self.idLengthErrorText.set("Identifer must be greater than 0!")
            nxt2 = False
        else:
            nxt2 = True
        
        if len(sql_query_statement) <= 0:
            self.sql_queryErrorText.set("SQL query cannot be blank!")
            nxt3 = False
        elif self.validateSQL(sql_query_statement) == False:
            self.sql_queryErrorText.set("Must enter valid SQL query!")
            nxt3 = False
        else:
            nxt3 = True

        if nxt1 == True and nxt2 == True and nxt3 == True:

            createSQLQuery(sql_query_statement,idSize,self.path_in)
            self.doneLabel = Label(self.frame, text="Done!")
            self.doneLabel.grid(row=7,column=1)
                
            
    def createMenu(self):
        self.master.minsize(450,400)
        self.master.maxsize(450,400)
        
        self.path_in = ""
        self.idSize = 0
        self.sql_statement = ""
        self.idLengthInputText = StringVar()
        self.browseErrorText = StringVar()
        self.sql_queryErrorText = StringVar()
        self.idLengthErrorText = StringVar()
        self.query_out = ""

        self.frame = Frame(self)
        self.frame.pack()

        self.step1Label = Label(self.frame, text="Step 1)\n Select file containing\nlist of identifiers")
        self.step1Label.grid(row=1,column=1,pady=10,padx=20)
        
        self.browseButton = Button(self.frame, text="Browse", command=self.getInputFile)
        self.browseButton.grid(row=1,column=2,pady=10,sticky=W)

        self.browseError = Label(self.frame, text="", fg="red", textvariable=self.browseErrorText)
        self.browseError.grid(row=1,column=2,pady=10,sticky=E)

        self.step2Label = Label(self.frame, text="Step 2) \nEnter SQL Query\n **Must contain 'IN ()' within statement\n **'()' cannot have text in between\n(Does not VALIDATE SQL Query)")
        self.step2Label.grid(row=2,column=1,pady=10,padx=20)
        
        self.sql_query_Text = Text(self.frame, width=20, height=4)
        self.sql_query_Text.grid(row=2,column=2,pady=10)

        self.sql_queryError = Label(self.frame, text="", fg="red", textvariable=self.sql_queryErrorText)
        self.sql_queryError.grid(row=3,column=2,pady=10)

        self.step3Label = Label(self.frame, text="Step 3)\n Enter text length of identifier")
        self.step3Label.grid(row=4,column=1,pady=10,padx=20)
        
        self.idLengthLabel = Label(self.frame, text="Length of Identifier:")
        self.idLengthLabel.grid(row=4,column=2,pady=10,sticky=W)

        validation = self.register(self.only_numbers)
        self.idLengthInput = Entry(self.frame, width=4, textvariable=self.idLengthInputText, validatecommand=(validation, '%S'))
        self.idLengthInputText.trace("w", lambda *args: self.characterLimit(self.idLengthInputText))
        self.idLengthInput.grid(row=4,column=2,sticky=E)

        self.idLengthError = Label(self.frame, text="", fg="red", textvariable=self.idLengthErrorText)
        self.idLengthError.grid(row=5,column=2)

        self.step4Label = Label(self.frame, text="Step 4)\n Click button to generate SQL script")
        self.step4Label.grid(row=6,column=1,pady=10,padx=20)
        
        self.generateButton = Button(self.frame, text="Generate", command=self.generateQuery)
        self.generateButton.grid(row=6,column=2)

        self.resetButton = Button(self.frame, text="Reset", command=self.reset)
        self.resetButton.grid(row=7,column=2)

        self.pack()
        
    def __init__(self, master=None):

        Frame.__init__(self, master)
        self.createMenu()
        
        
       
ICON = (b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
        b'\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00'
        b'\x08\x00\x00\x00\x00\x00@\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x01\x00\x00\x00\x01') + b'\x00'*1282 + b'\xff'*64

_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)

    
root = Tk()
app = Application(master=root)
app.master.title("SQL Generator")
app.master.iconbitmap(default=ICON_PATH)
app.mainloop()


		

    

     
                
        


        




