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



















