from machine import Pin, I2C, SPI
import time
from lcd import LCD_1inch28
from touch import Touch_CST816T

# Pin definitions (unchanged)
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

def create_animation_sequence(base_text, frames=4, delay=0.25, duration=5):
    """
    Creates an animation sequence configuration
    
    Args:
        base_text (str): Base text for animation (e.g., "Analyzing" or "Drying")
        frames (int): Number of animation frames
        delay (float): Delay between frames in seconds
        duration (int): Total duration of animation in seconds
    
    Returns:
        dict: Animation configuration
    """
    return {
        'texts': [f"{base_text}{'.' * i}" for i in range(frames)],
        'delay': delay,
        'duration': duration
    }

def display_animation_frame(lcd, text, y_pos=90, countdown=None):
    """
    Displays a single animation frame
    
    Args:
        lcd: LCD display object
        text (str): Text to display
        y_pos (int): Vertical position of text
        countdown (str, optional): Countdown text to display
    """
    lcd.fill(lcd.white)
    lcd.write_text(text, 30, y_pos, 2, lcd.black)
    
    if countdown:
        lcd.write_text(countdown, 100, 130, 2, lcd.black)
    
    lcd.show()

def run_animation_sequence(lcd, animation_config, show_countdown=False):
    """
    Runs a complete animation sequence
    
    Args:
        lcd: LCD display object
        animation_config (dict): Animation configuration
        show_countdown (bool): Whether to show countdown timer
    """
    try:
        for second in range(animation_config['duration'], 0, -1):
            for text in animation_config['texts']:
                display_animation_frame(
                    lcd, 
                    text, 
                    countdown=f"{second}s" if show_countdown else None
                )
                time.sleep(animation_config['delay'])
                
        lcd.display_image('wallpaper.bin')
        
    except KeyboardInterrupt:
        print("Animation stopped by user")

def handle_touch_event(lcd, x, y):
    """
    Handles touch events and triggers appropriate animations
    
    Args:
        lcd: LCD display object
        x (int): X coordinate of touch
        y (int): Y coordinate of touch
    """
    if y < 120:  # Upper half - Analysis mode
        animation = create_animation_sequence("Analyzing", duration=5)
        run_animation_sequence(lcd, animation)
    else:  # Lower half - Drying mode
        animation = create_animation_sequence("Drying", duration=10)
        run_animation_sequence(lcd, animation, show_countdown=True)

def initialize_hardware():
    """
    Initializes LCD and touch hardware
    
    Returns:
        tuple: (LCD object, Touch object)
    """
    lcd = LCD_1inch28()
    lcd.set_bl_pwm(65535)
    
    touch = Touch_CST816T(mode=1, LCD=lcd)
    touch.Flag = 0
    touch.Mode = 1
    touch.Set_Mode(touch.Mode)
    
    return lcd, touch

def main_loop(lcd, touch):
    """
    Main program loop handling touch events
    
    Args:
        lcd: LCD display object
        touch: Touch controller object
    """
    lcd.display_image('wallpaper.bin')
    
    try:
        while True:
            if touch.Flag == 1:
                handle_touch_event(lcd, touch.X_point, touch.Y_point)
                touch.Flag = 0
                
    except KeyboardInterrupt:
        print("Program terminated by user")

def main():
    """Main program entry point"""
    lcd, touch = initialize_hardware()
    main_loop(lcd, touch)

if __name__ == '__main__':
    main()
