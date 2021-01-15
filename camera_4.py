from tkinter import *
import cv2
from PIL import Image, ImageTk
import time
import serial
import csv
from pypylon import pylon




class App:
    
     
    def __init__(self, video_source=0):
               
        self.appName="CID Camera v1.0"
        self.window=Tk()
        self.window.title(self.appName)
        self.window.geometry("800x1000")
        #self.window.resizable(0,0)
        self.window['bg'] = 'snow2'
        self.video_source =video_source
        #initCamera()
        self.expoInt=50000
        self.gainInt=1.4
        self.label = Label(self.window, text=self.appName, font=15, bg='firebrick3', fg='white').pack(side=TOP, fill=BOTH)
        
        
        
   
        #create a canvas that can fit the above video source size
        self.canvas=Canvas(self.window, width=700, height=700, bg='snow2')
        self.canvas.pack()
        self.frame=Frame(self.window, bg='firebrick3', borderwidth=20)
        self.frame.pack(side=LEFT, fill=BOTH, expand=True)
        #button that lets the user take a snapshot
        self.btn_snapshot=Button(self.window, text="Snapshot", font=('Courier', 15, 'bold'), width=30, bg='#F7941D', activebackground='red', command=self.snapshot)
        self.btn_snapshot.place(x=100, y=950)
        self.button = Button(self.window, text="X Pos", font=('Courier', 13, 'bold'), bg='#69003F', fg='white', command=self.getDirectionXPos)
        self.button.place(x=100, y=785, width=75, height=25)
        self.button = Button(self.window, text="X Neg", font=('Courier', 13, 'bold'), bg='#69003F', fg='white',command=self.getDirectionXNeg)
        self.button.place(x=200, y=785, width=75, height=25)
        self.button = Button(self.window, text="Y Pos", font=('Courier', 13, 'bold'), bg='#69003F', fg='white',command=self.getDirectionYPos)
        self.button.place(x=150, y=750, width=75, height=25)
        self.button = Button(self.window, text="Y Neg", font=('Courier', 13, 'bold'), bg='#69003F', fg='white',command=self.getDirectionYNeg)
        self.button.place(x=150, y=820, width=75, height=25)
        self.button = Button(self.window, text="Z Pos", font=('Courier', 13, 'bold'), bg='#69003F', fg='white',command=self.getDirectionZPos)
        self.button.place(x=280, y=750, width=75, height=25)
        self.button = Button(self.window, text="Z Neg", font=('Courier', 13, 'bold'), bg='#69003F', fg='white',command=self.getDirectionZNeg)
        self.button.place(x=280, y=820, width=75, height=25)
        self.button = Button(self.window, text="CSV File", font=('Courier', 13, 'bold'), bg='#69003F', fg='white',command= self.getcsvFile)
        self.button.place(x=100, y=880, width=100, height=25)
        self.LABL = Label(self.window, text="Enter Well Position:", font=('Courier', 13, 'bold'), bg='#69003F', fg='white')
        self.LABL.place(x=510, y=870, width=240, height=20)
        self.entry1 = Entry(self.window)
        self.entry1.bind("<Return>", self.onReturn)
        self.entry1.place(x=510, y=890)
        self.LABL2 = Label(self.window, text="Exposure:", font=('Courier', 13, 'bold'), bg='#69003F', fg='white')
        self.LABL2.place(x=510, y=745, width=240, height=20)
        self.entry2 = Entry(self.window)
        self.entry2.bind("<Return>", self.onExposure)
        self.entry2.place(x=510, y=775)
        self.LABL3 = Label(self.window, text="Gain:", font=('Courier', 13, 'bold'), bg='#69003F', fg='white')
        self.LABL3.place(x=510, y=805, width=240, height=20)
        self.entry3 = Entry(self.window)
        self.entry3.bind("<Return>", self.onGain)
        self.entry3.place(x=510, y=835)
        #self.button = Button(self.window, text="Enter Data", font=('Courier', 10), command= self.onReturn)
        #self.button.place(x=600, y=905, width=80, height=15)
        #self.btn_snapshot.pack(anchor=CENTER, side = BOTTOM, expand=True)
       
        self.update()
        self.window.mainloop()
        
        
        
    def snapshot(self):
        #get a frame that we have to save as the image
        frame = self.getSingleFrameArray()
        if True:
            image="IMG-"+time.strftime("%H-%M-%S-%d-%m")+".jpg"
            cv2.imwrite(image, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
            #show msg on window that image is saved
            msg=Label(self.window, text='Image Saved'+image, bg='black', fg='green').place(x=430, y=510)
            
    def update(self):
        
        if ser.inWaiting() > 0 and self.nFile < self.numLines:
            
            self.line = ser.readline().decode('utf-8').rstrip()
            print(self.line)
            ser.flush()
            #line = ser.readline().decode('utf-8').rstrip()
            print("Data Recived: "+str(self.line))
            time.sleep(1)
            self.case = str(self.csvFile[self.nFile])
            print(self.case)
            self.strSlice = str(self.case[2:5])
            print (self.strSlice)
            ser.write(self.strSlice.encode() +'\n'.encode())
            self.nFile= self.nFile +1                            
                    
        else:
            print ("Waiting to receive")
            time.sleep(0.2)#line = ser.readline().decode('utf-8').rstrip()                  
        self.photo= ImageTk.PhotoImage(image=Image.fromarray(self.getSingleFrameArray()))
        self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
        self.window.after(50, self.update)
        
    
        
        
    def setExp (self):
        
        camera.Open()
        camera.ExposureAuto.SetValue("Off")
        camera.ExposureTime.SetValue(self.expoInt)
        
    def setGain (self):
        
        camera.Open()
        camera.GainAuto.SetValue("Off")
        camera.Gain.SetValue(self.gainInt)
    
    def getSingleFrameArray(self):
        
        self.setExp()
        self.setGain()
        grabResult = camera.RetrieveResult(1000, pylon.TimeoutHandling_ThrowException)
    
        if grabResult.GrabSucceeded():
        # Access the image data
            image = converter.Convert(grabResult)
            img = image.GetArray()
        
        grabResult.Release()
        return img
    
    def onReturn(self, event):
        print("Return Pressed")
        self.led_number = self.entry1.get();
        print(self.led_number)
        self.entry1.delete(0, 'end')
        print("Sending number" + str(self.led_number) + " to Arduino.")
        ser.write(self.led_number.encode() + '\n'.encode())
        time.sleep(0.1)
        self.callFunc()
        
    def onExposure(self, event):
        print("Exposure entered")
        self.exposure = self.entry2.get();
        self.expoInt = int(self.exposure)
        print(self.expoInt)
        self.entry2.delete(0, 'end')
        
        
        
    def onGain(self, event):
        print("Gain entered")
        self.gain = self.entry3.get();
        self.gainInt = int(self.gain)
        print(self.gainInt)
        self.entry3.delete(0, 'end')
        
        

    
    #def onReturn(self):
        #print("Return Pressed")
        #self.led_number = entry1.get();
        #print(self.led_number)
        #entry1.delete(0, 'end')
        #print("Sending number" + str(self.led_number) + " to Arduino.")
        #ser.write(self.led_number.encode() + '\n'.encode())
        #time.sleep(0.1)
        #self.callFunc()
    
    def snapshot(self):
        #get a frame that we have to save as the image
       
        frame = self.getSingleFrameArray()
        if True:
            image="IMG-"+time.strftime("%H-%M-%S-%d-%m")+".jpg"
            cv2.imwrite(image, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
            #show msg on window that image is saved
            msg=Label(self.window, text='Image Saved'+image, bg='black', fg='green').place(x=430, y=510)
            
    
        
    def callFunc (self):
    
        while True:
            if ser.inWaiting() > 0:
                self.line = ser.readline().decode('utf-8').rstrip()
                self.Txt1=self.line
                #self.Txt2=int(self.Txt1)
                #if self.Txt2 == 3:
                print("Data received: "+str(self.Txt1))
                ser.flush()
                break
            
            else:
                print ("Waiting to receive")
                time.sleep(0.2)
        print("Out of loop")

    
    def getDirectionXPos(self):
        print("Direction X-Pos Pressed")
        self.led_number = "K33"
        print("Sending number" + str(self.led_number) + " to Arduino.")
        ser.write(self.led_number.encode() +'\n'.encode())
        time.sleep(0.1)
        self.callFunc()
        
    def getDirectionXNeg(self):
        print("Direction X-Neg Pressed")
        self.led_number = "L00"
        print("Sending number" + str(self.led_number) + " to Arduino.")
        ser.write(self.led_number.encode() + '\n'.encode())
        time.sleep(0.1)
        self.callFunc()


    def getDirectionYPos(self):
        print("Direction Y-Pos Pressed")
        self.led_number = "M00"
        print("Sending number" + str(self.led_number) + " to Arduino.")
        ser.write(self.led_number.encode() + '\n'.encode())
        time.sleep(0.1)
        self.callFunc()



    def getDirectionYNeg(self):
        print("Direction Y-Neg Pressed")
        self.led_number = "N00"
        print("Sending number" + str(self.led_number) + " to Arduino.")
        ser.write(self.led_number.encode() + '\n'.encode())
        time.sleep(0.1)
        self.callFunc()



    def getDirectionZPos(self):
        print("Direction Z-Pos Pressed")
        self.led_number = "P00"
        print("Sending number" + str(self.led_number) + " to Arduino.")
        ser.write(self.led_number.encode() + '\n'.encode())
        time.sleep(0.1)
        self.callFunc()



    def getDirectionZNeg(self):
        print("Direction Z-Neg Pressed")
        self.led_number = "Q00"
        print("Sending number" + str(self.led_number) + " to Arduino.")
        ser.write(self.led_number.encode() + '\n'.encode())
        time.sleep(0.1)
        self.callFunc()
        
    def getcsvFile (self):
        with open('TestFile2.csv', mode ='r')as file: 
        
      # reading the CSV file 
            self.csvFile = list(csv.reader(file))
            self.numLines = len(self.csvFile)
            print (self.numLines)
            
            self.nFile=1
            self.case = str(self.csvFile[self.nFile])
            print(self.case)
            self.strSlice = str(self.case[2:5])
            print (self.strSlice)
            ser.write(self.strSlice.encode() +'\n'.encode())
            time.sleep(0.1)
            self.nFile= self.nFile +1  
            
            
                

if __name__=="__main__":
    
    
    ser = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1)
    ser.flush()
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    converter = pylon.ImageFormatConverter()
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
    
    App()
    