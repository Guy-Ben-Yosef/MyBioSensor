from machine import Pin,I2C,SPI,PWM,Timer,ADC
import framebuf
import time

# Pin definition
I2C_SDA = 6
I2C_SDL = 7
I2C_INT = 17
I2C_RST = 16

DC = 14
CS = 9
SCK = 10
MOSI = 11
MISO = 12
RST = 8

BL = 15

# LCD Driver
class LCD_1inch28(framebuf.FrameBuffer):
    def __init__(self): # SPI initialization
        self.width = 240
        self.height = 240
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1,100_000_000,polarity=0, phase=0,bits= 8,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        # Define color, Micropython fixed to BRG format
        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff
        self.black =   0x0000
        self.brown =   0X8430
        
        self.fill(self.white) # Clear screen
        self.show()# Show

        self.pwm = PWM(Pin(BL))
        self.pwm.freq(5000) # Turn on the backlight
        
    def write_cmd(self, cmd): # Write command
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf): # Write data
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)
        
    def set_bl_pwm(self,duty): # Set screen brightness
        self.pwm.duty_u16(duty)# max 65535
        
    def init_display(self): # LCD initialization
        """Initialize dispaly"""  
        self.rst(1)
        time.sleep(0.01)
        self.rst(0)
        time.sleep(0.01)
        self.rst(1)
        time.sleep(0.05)
        
        self.write_cmd(0xEF)
        self.write_cmd(0xEB)
        self.write_data(0x14) 
        
        self.write_cmd(0xFE) 
        self.write_cmd(0xEF) 

        self.write_cmd(0xEB)
        self.write_data(0x14) 

        self.write_cmd(0x84)
        self.write_data(0x40) 

        self.write_cmd(0x85)
        self.write_data(0xFF) 

        self.write_cmd(0x86)
        self.write_data(0xFF) 

        self.write_cmd(0x87)
        self.write_data(0xFF)

        self.write_cmd(0x88)
        self.write_data(0x0A)

        self.write_cmd(0x89)
        self.write_data(0x21) 

        self.write_cmd(0x8A)
        self.write_data(0x00) 

        self.write_cmd(0x8B)
        self.write_data(0x80) 

        self.write_cmd(0x8C)
        self.write_data(0x01) 

        self.write_cmd(0x8D)
        self.write_data(0x01) 

        self.write_cmd(0x8E)
        self.write_data(0xFF) 

        self.write_cmd(0x8F)
        self.write_data(0xFF) 


        self.write_cmd(0xB6)
        self.write_data(0x00)
        self.write_data(0x20)

        self.write_cmd(0x36)
        self.write_data(0x98)

        self.write_cmd(0x3A)
        self.write_data(0x05) 


        self.write_cmd(0x90)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x08) 

        self.write_cmd(0xBD)
        self.write_data(0x06)
        
        self.write_cmd(0xBC)
        self.write_data(0x00)

        self.write_cmd(0xFF)
        self.write_data(0x60)
        self.write_data(0x01)
        self.write_data(0x04)

        self.write_cmd(0xC3)
        self.write_data(0x13)
        self.write_cmd(0xC4)
        self.write_data(0x13)

        self.write_cmd(0xC9)
        self.write_data(0x22)

        self.write_cmd(0xBE)
        self.write_data(0x11) 

        self.write_cmd(0xE1)
        self.write_data(0x10)
        self.write_data(0x0E)

        self.write_cmd(0xDF)
        self.write_data(0x21)
        self.write_data(0x0c)
        self.write_data(0x02)

        self.write_cmd(0xF0)   
        self.write_data(0x45)
        self.write_data(0x09)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x26)
        self.write_data(0x2A)

        self.write_cmd(0xF1)    
        self.write_data(0x43)
        self.write_data(0x70)
        self.write_data(0x72)
        self.write_data(0x36)
        self.write_data(0x37)  
        self.write_data(0x6F)


        self.write_cmd(0xF2)   
        self.write_data(0x45)
        self.write_data(0x09)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x26)
        self.write_data(0x2A)

        self.write_cmd(0xF3)   
        self.write_data(0x43)
        self.write_data(0x70)
        self.write_data(0x72)
        self.write_data(0x36)
        self.write_data(0x37) 
        self.write_data(0x6F)

        self.write_cmd(0xED)
        self.write_data(0x1B) 
        self.write_data(0x0B) 

        self.write_cmd(0xAE)
        self.write_data(0x77)
        
        self.write_cmd(0xCD)
        self.write_data(0x63)


        self.write_cmd(0x70)
        self.write_data(0x07)
        self.write_data(0x07)
        self.write_data(0x04)
        self.write_data(0x0E) 
        self.write_data(0x0F) 
        self.write_data(0x09)
        self.write_data(0x07)
        self.write_data(0x08)
        self.write_data(0x03)

        self.write_cmd(0xE8)
        self.write_data(0x34)

        self.write_cmd(0x62)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x71)
        self.write_data(0xED)
        self.write_data(0x70) 
        self.write_data(0x70)
        self.write_data(0x18)
        self.write_data(0x0F)
        self.write_data(0x71)
        self.write_data(0xEF)
        self.write_data(0x70) 
        self.write_data(0x70)

        self.write_cmd(0x63)
        self.write_data(0x18)
        self.write_data(0x11)
        self.write_data(0x71)
        self.write_data(0xF1)
        self.write_data(0x70) 
        self.write_data(0x70)
        self.write_data(0x18)
        self.write_data(0x13)
        self.write_data(0x71)
        self.write_data(0xF3)
        self.write_data(0x70) 
        self.write_data(0x70)

        self.write_cmd(0x64)
        self.write_data(0x28)
        self.write_data(0x29)
        self.write_data(0xF1)
        self.write_data(0x01)
        self.write_data(0xF1)
        self.write_data(0x00)
        self.write_data(0x07)

        self.write_cmd(0x66)
        self.write_data(0x3C)
        self.write_data(0x00)
        self.write_data(0xCD)
        self.write_data(0x67)
        self.write_data(0x45)
        self.write_data(0x45)
        self.write_data(0x10)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)

        self.write_cmd(0x67)
        self.write_data(0x00)
        self.write_data(0x3C)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x54)
        self.write_data(0x10)
        self.write_data(0x32)
        self.write_data(0x98)

        self.write_cmd(0x74)
        self.write_data(0x10)
        self.write_data(0x85)
        self.write_data(0x80)
        self.write_data(0x00) 
        self.write_data(0x00) 
        self.write_data(0x4E)
        self.write_data(0x00)
        
        self.write_cmd(0x98)
        self.write_data(0x3e)
        self.write_data(0x07)

        self.write_cmd(0x35)
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)
    
    def setWindows(self,Xstart,Ystart,Xend,Yend): 
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(Xstart)
        self.write_data(0x00)
        self.write_data(Xend-1)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(Ystart)
        self.write_data(0x00)
        self.write_data(Yend-1)
        
        self.write_cmd(0x2C)
     
    def show(self): 
        self.setWindows(0,0,self.width,self.height)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
        
    '''
        Partial display, the starting point of the local
        display here is reduced by 10, and the end point
        is increased by 10
    '''
    #Partial display, the starting point of the local display here is reduced by 10, and the end point is increased by 10
    def Windows_show(self,Xstart,Ystart,Xend,Yend):
        if Xstart > Xend:
            data = Xstart
            Xstart = Xend
            Xend = data
            
        if (Ystart > Yend):        
            data = Ystart
            Ystart = Yend
            Yend = data
            
        if Xstart <= 10:
            Xstart = 10
        if Ystart <= 10:
            Ystart = 10
            
        Xstart -= 10;Xend += 10
        Ystart -= 10;Yend += 10
        
        self.setWindows(Xstart,Ystart,Xend,Yend)      
        self.cs(1)
        self.dc(1)
        self.cs(0)
        for i in range (Ystart,Yend-1):             
            Addr = (Xstart * 2) + (i * 240 * 2)                
            self.spi.write(self.buffer[Addr : Addr+((Xend-Xstart)*2)])
        self.cs(1)
        
    # Write characters, size is the font size, the minimum is 1  
    def write_text(self,text,x,y,size,color):
        ''' Method to write Text on OLED/LCD Displays
            with a variable font size

            Args:
                text: the string of chars to be displayed
                x: x co-ordinate of starting position
                y: y co-ordinate of starting position
                size: font size of text
                color: color of text to be displayed
        '''
        background = self.pixel(x,y)
        info = []
        # Creating reference charaters to read their values
        self.text(text,x,y,color)
        for i in range(x,x+(8*len(text))):
            for j in range(y,y+8):
                # Fetching amd saving details of pixels, such as
                # x co-ordinate, y co-ordinate, and color of the pixel
                px_color = self.pixel(i,j)
                info.append((i,j,px_color)) if px_color == color else None
        # Clearing the reference characters from the screen
        self.text(text,x,y,background)
        # Writing the custom-sized font characters on screen
        for px_info in info:
            self.fill_rect(size*px_info[0] - (size-1)*x , size*px_info[1] - (size-1)*y, size, size, px_info[2]) 
    
        
# Draw line and show
def Touch_HandWriting():
    x = y = data = 0
    color = 0
    Touch.Flgh = 0
    Touch.Flag = 0
    Touch.Mode = 1
    Touch.Set_Mode(Touch.Mode)
    
    LCD.fill(LCD.white)
    LCD.rect(0, 0, 35, 208,LCD.red,True)
    LCD.rect(0, 0, 208, 35,LCD.green,True)
    LCD.rect(205, 0, 240, 240,LCD.blue,True)
    LCD.rect(0, 205, 240, 240,LCD.brown,True)
    LCD.show()
    
    Touch.tim.init(period=1, callback=Touch.Timer_callback)
    try:
        while True:
            if Touch.Flgh == 0 and Touch.X_point != 0:
                Touch.Flgh = 1
                x = Touch.X_point
                y = Touch.Y_point
                
            if Touch.Flag == 1:
                if (Touch.X_point > 34 and Touch.X_point < 205) and (Touch.Y_point > 34 and Touch.Y_point < 205):
                    Touch.Flgh = 3
                else:
                    if (Touch.X_point > 0 and Touch.X_point < 33) and (Touch.Y_point > 0 and Touch.Y_point < 208):
                        color = LCD.red
                        
                    if (Touch.X_point > 0 and Touch.X_point < 208) and (Touch.Y_point > 0 and Touch.Y_point < 33):
                        color = LCD.green
                        
                    if (Touch.X_point > 208 and Touch.X_point < 240) and (Touch.Y_point > 0 and Touch.Y_point < 240):
                        color = LCD.blue
                        
                    if (Touch.X_point > 0 and Touch.X_point < 240) and (Touch.Y_point > 208 and Touch.Y_point < 240):
                        LCD.fill(LCD.white)
                        LCD.rect(0, 0, 35, 208,LCD.red,True)
                        LCD.rect(0, 0, 208, 35,LCD.green,True)
                        LCD.rect(205, 0, 240, 240,LCD.blue,True)
                        LCD.rect(0, 205, 240, 240,LCD.brown,True)
                        LCD.show()
                    Touch.Flgh = 4
                    
                if Touch.Flgh == 3:
                    time.sleep(0.001) #Prevent disconnection  防止断触
                    if Touch.l < 25:           
                        Touch.Flag = 0
                        LCD.line(x,y,Touch.X_point,Touch.Y_point,color)
                        LCD.Windows_show(x,y,Touch.X_point,Touch.Y_point)
                        Touch.l=0
                    else:
                        Touch.Flag = 0
                        LCD.pixel(Touch.X_point,Touch.Y_point,color)
                        LCD.Windows_show(x,y,Touch.X_point,Touch.Y_point)
                        Touch.l=0
                        
                    x = Touch.X_point
                    y = Touch.Y_point
    except KeyboardInterrupt:
        pass

# Gesture
def Touch_Gesture():
    Touch.Mode = 0
    Touch.Set_Mode(Touch.Mode)
    LCD.fill(LCD.white)
#     LCD.show()
    LCD.write_text('Gesture test',70,90,1,LCD.black)
    LCD.write_text('Complete as prompted',35,120,1,LCD.black)
    LCD.show()
    time.sleep(1)
    LCD.fill(LCD.white)
    while Touch.Gestures != 0x01:
        LCD.fill(LCD.white)
        LCD.write_text('UP',100,110,3,LCD.black)
        LCD.show()
        time.sleep(0.1)
        
    while Touch.Gestures != 0x02:
        LCD.fill(LCD.white)
        LCD.write_text('DOWM',70,110,3,LCD.black)
        LCD.show()
        time.sleep(0.1)
        
    while Touch.Gestures != 0x03:
        LCD.fill(LCD.white)
        LCD.write_text('LEFT',70,110,3,LCD.black)
        LCD.show()
        time.sleep(0.1)
        
    while Touch.Gestures != 0x04:
        LCD.fill(LCD.white)
        LCD.write_text('RIGHT',60,110,3,LCD.black)
        LCD.show()
        time.sleep(0.1)
        
    while Touch.Gestures != 0x0C:
        LCD.fill(LCD.white)
        LCD.write_text('Long Press',40,110,2,LCD.black)
        LCD.show()
        time.sleep(0.1)
        
    while Touch.Gestures != 0x0B:
        LCD.fill(LCD.white)
        LCD.write_text('Double Click',25,110,2,LCD.black)
        LCD.show() 
        time.sleep(0.1)
        

        
if __name__=='__main__':
  
    LCD = LCD_1inch28()
    LCD.set_bl_pwm(65535)

    Touch = Touch_CST816T(mode=1,LCD=LCD)
    
    try:
        while True:
            if Touch.Flag:
                Touch.Flag = 0
            time.sleep_ms(100)
            
    except KeyboardInterrupt:
        print("\nTest ended by user")
    
    


#    Touch_Gesture()
    
#    Touch_HandWriting()



















