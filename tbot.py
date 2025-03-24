from PIL import ImageGrab
import time
import win32api
import win32con

# Разрешение экрана
screen_width, screen_height = 1920, 1440

# Координаты центра экрана (прицела)
target_x, target_y = screen_width // 2, screen_height // 2

# Цвет прицела без противника (белый)
default_color = (255, 255, 255)

# Цвет прицела с противником (красный)
enemy_color = (255, 0, 0)

# Флаг активации бота
active = False

# Флаг состояния ЛКМ (нажата/отжата)
left_mouse_down = False

def get_pixel_color(x, y):
    """Получает цвет пикселя на экране по координатам (x, y)."""
    screenshot = ImageGrab.grab(bbox=(x, y, x+1, y+1))
    return screenshot.getpixel((0, 0))

def is_enemy_in_sight():
    """Проверяет, стал ли цвет пикселя в прицеле красным."""
    current_color = get_pixel_color(target_x, target_y)
    print(f"Цвет прицела: {current_color}")  # Отладка: вывод цвета прицела
    return current_color == enemy_color

def is_right_mouse_down():
    """Проверяет, зажата ли правая кнопка мыши (ПКМ)."""
    return win32api.GetAsyncKeyState(win32con.VK_RBUTTON) & 0x8000 != 0

def is_key_e_pressed():
    """Проверяет, зажата ли клавиша E."""
    return win32api.GetAsyncKeyState(ord('E')) & 0x8000 != 0

def press_left_mouse_button():
    """Нажимает левую кнопку мыши (ЛКМ)."""
    global left_mouse_down
    if not left_mouse_down:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)  # Нажатие ЛКМ
        left_mouse_down = True
        print("ЛКМ нажата")  # Отладка: подтверждение нажатия ЛКМ

def release_left_mouse_button():
    """Отпускает левую кнопку мыши (ЛКМ)."""
    global left_mouse_down
    if left_mouse_down:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)  # Отпускание ЛКМ
        left_mouse_down = False
        print("ЛКМ отжата")  # Отладка: подтверждение отпускания ЛКМ

def main():
    global active
    print("Ожидание активации бота... (Зажмите ПКМ и E для активации)")
    while True:
        # Активация бота при зажатии ПКМ и E
        if is_right_mouse_down() and is_key_e_pressed():
            if not active:
                active = True
                print("Бот активирован")  # Отладка: подтверждение активации
                time.sleep(0.1)  # Задержка для предотвращения ложного выстрела
        else:
            if active:
                active = False
                print("Бот деактивирован")  # Отладка: подтверждение деактивации
                release_left_mouse_button()  # Отпустить ЛКМ при деактивации

        if active:
            if is_enemy_in_sight():
                press_left_mouse_button()  # Нажать ЛКМ, если противник в прицеле
            else:
                release_left_mouse_button()  # Отпустить ЛКМ, если противник не в прицеле

        time.sleep(0.01)  # Задержка для снижения нагрузки на CPU

if __name__ == "__main__":
    main()
