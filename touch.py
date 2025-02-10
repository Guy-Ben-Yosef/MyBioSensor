from machine import Pin,I2C,SPI,PWM,Timer,ADC
import time

class Touch_CST816T(object):
    def __init__(self, address=0x15, mode=0, i2c_num=1, i2c_sda=6, i2c_scl=7, int_pin=17, rst_pin=16, LCD=None):
        # Initialize reset pin first
        self.rst = Pin(rst_pin, Pin.OUT)
        
        # Perform reset with extended delays
        self.Reset()
        
        # Initialize I2C with lower initial frequency
        self._bus = I2C(id=i2c_num, scl=Pin(i2c_scl), sda=Pin(i2c_sda), freq=100_000)
        self._address = address
        
        # Initialize interrupt pin
        self.int = Pin(int_pin, Pin.IN, Pin.PULL_UP)
        self.tim = Timer()
        
        # Extended initialization sequence
        time.sleep_ms(50)  # Add delay before first communication
        
        # Wake device first
        self.Stop_Sleep()
        time.sleep_ms(50)  # Add delay after wake
        
        # Now check device ID
        bRet = self.WhoAmI()
        if bRet:
            print("Success: Detected CST816T.")
            Rev = self.Read_Revision()
            print("CST816T Revision = {}".format(Rev))
        else:
            print("Error: Not Detected CST816T.")
            return None
            
        # Now that initialization is complete, increase I2C frequency
        self._bus = I2C(id=i2c_num, scl=Pin(i2c_scl), sda=Pin(i2c_sda), freq=400_000)
        
        self.Mode = 1  # Set to point mode
        self.Set_Mode(self.Mode)  # Configure touch mode
        self.Flag = 0
        self.X_point = self.Y_point = 0
        self.int.irq(handler=self.Int_Callback, trigger=Pin.IRQ_FALLING)
        
        print("Touch initialization complete - ready to detect touches")
        
    def Reset(self):
        self.rst(0)
        time.sleep_ms(20)
        self.rst(1)
        time.sleep_ms(300)
      
    def _read_byte(self, cmd):
        try:
            rec = self._bus.readfrom_mem(int(self._address), int(cmd), 1)
            return rec[0]
        except Exception as e:
            print(f"Error reading from register 0x{cmd:02X}: {str(e)}")
            raise
    
    def _read_block(self, reg, length=1):
        try:
            rec = self._bus.readfrom_mem(int(self._address), int(reg), length)
            return rec
        except Exception as e:
            print(f"Error reading block from register 0x{reg:02X}: {str(e)}")
            raise
    
    def _write_byte(self, cmd, val):
        try:
            self._bus.writeto_mem(int(self._address), int(cmd), bytes([int(val)]))
            time.sleep_ms(10)  # Add delay after writes
        except Exception as e:
            print(f"Error writing to register 0x{cmd:02X}: {str(e)}")
            raise

    def WhoAmI(self):
        return self._read_byte(0xA7) == 0xB5
    
    def Read_Revision(self):
        return self._read_byte(0xA9)
      
    def Stop_Sleep(self):
        self._write_byte(0xFE,0x01)
    
    def Set_Mode(self, mode):
        if mode == 1:      
            self._write_byte(0xFA, 0x41)  # Point mode
        elif mode == 2:
            self._write_byte(0xFA, 0x71)  # Mixed mode
        else:
            self._write_byte(0xFA, 0x11)  # Gesture mode
            self._write_byte(0xEC, 0x01)
     
    def get_point(self):
        try:
            xy_point = self._read_block(0x03, 4)
            x_point = ((xy_point[0] & 0x0f) << 8) + xy_point[1]
            y_point = ((xy_point[2] & 0x0f) << 8) + xy_point[3]
            return x_point, y_point
        except Exception as e:
            print(f"Error getting touch point: {str(e)}")
            return 0, 0

    def Int_Callback(self, pin):
        self.Flag = 1
        x, y = self.get_point()
        self.X_point = x
        self.Y_point = y

    def Timer_callback(self,t):
        self.l += 1
        if self.l > 100:
            self.l = 50
