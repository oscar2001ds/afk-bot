from pynput.keyboard import Listener, Key
import pyautogui
import threading
import time

# --- Global Variables ---
app_state = 'running'
lorem_text = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec sapien ante, ornare facilisis ultrices ut, egestas non odio. Maecenas at leo mauris. Phasellus blandit libero in velit condimentum fringilla. Suspendisse sodales ante sit amet felis iaculis consectetur. Mauris turpis justo, pellentesque id sagittis ut, venenatis nec lorem. Maecenas vulputate lobortis lectus, eget blandit ligula dignissim quis. Cras nec laoreet ligula, in laoreet arcu. Maecenas urna urna, sodales quis quam a, hendrerit dictum nunc. Sed arcu metus, malesuada in imperdiet eget, porta a ipsum. Etiam egestas tempus rutrum. Donec ultrices volutpat odio, eget mattis tortor luctus eget. Aenean fermentum aliquet lorem, quis tincidunt massa lobortis at. Ut vel lectus ac lorem consectetur molestie ac ut eros.

Proin congue dui non felis facilisis ultrices. Pellentesque molestie risus ac lectus dictum ultrices. Aliquam erat volutpat. Ut interdum euismod risus. Vestibulum vitae diam sit amet mauris sollicitudin laoreet. Pellentesque et interdum turpis. Vivamus volutpat, mauris a laoreet molestie, massa ligula pulvinar sem, ut sollicitudin quam sem id elit. Aliquam vitae libero erat. Sed lacinia lacinia enim, eget gravida nisl consectetur quis. In hac habitasse platea dictumst. Ut semper enim nec laoreet laoreet. Nullam mattis at velit ut posuere. Vestibulum posuere, dolor eu tincidunt vehicula, nulla felis auctor tortor, non lacinia leo risus et felis.

Nam sed risus bibendum, lobortis enim id, dignissim nulla. Aenean eget urna quis eros blandit blandit. Curabitur congue vulputate porta. Ut tempus scelerisque commodo. Donec quis mattis nisl, ac sollicitudin tortor. Aliquam consectetur, nisi at finibus ultrices, tortor purus vestibulum mauris, vel lobortis risus mauris sit amet nunc. Pellentesque imperdiet, ex in eleifend tempus, augue nisl eleifend nisi, eu semper arcu turpis eget orci. Aliquam tincidunt imperdiet lorem, at consequat nisl ornare in. In facilisis bibendum eros, vitae dignissim mauris congue eu. Duis dolor sem, malesuada eget consectetur at, tempus ut massa. Mauris sed finibus mauris. Cras vel faucibus lectus, et ornare arcu. Nulla nec magna quis mi varius bibendum. In scelerisque nec augue quis rutrum. Pellentesque placerat placerat vulputate.

Morbi lacinia mollis lorem quis dapibus. In vel consectetur lacus, id tempor dui. Vivamus a elit velit. Vivamus vulputate orci tortor, sit amet mollis felis iaculis blandit. Pellentesque imperdiet orci sit amet leo dapibus, ac cursus neque pellentesque. Nullam maximus condimentum nunc vitae consequat. Sed ac scelerisque enim, id consequat urna. Suspendisse potenti. Etiam non mollis ipsum, at porttitor magna. Donec pharetra fringilla ullamcorper. Praesent pretium quam nibh, vel fringilla elit consectetur id. Cras porttitor, odio a sollicitudin interdum, arcu magna lobortis libero, ullamcorper lacinia nisi metus nec magna. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.

Mauris ac semper sem, ac malesuada enim. Vestibulum turpis eros, cursus in congue eget, placerat vel lectus. Morbi justo magna, semper at enim a, dignissim congue sapien. Vestibulum tempus dapibus odio non molestie. Phasellus sed purus non tortor auctor efficitur et eget odio. Praesent eget purus varius, luctus quam non, tristique mi. Donec scelerisque est ac lectus tincidunt porta. Cras aliquet vel justo et volutpat. Vivamus nec ligula vitae leo lobortis mollis. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Aliquam volutpat porta urna, eu blandit arcu dapibus non.
"""
initial_time = 0
elapsed_time = "00:00:00"

# --- Actions ---
def pause_bot():
    global app_state
    if app_state == 'running':
        app_state = 'paused'
        print("\n❄️ Bot paused. Press ↑ to resume or → to stop.")

def resume_bot():
    global app_state
    if app_state == 'paused':
        app_state = 'running'
        print("\n🚀 Bot resumed.")

def stop_bot():
    global app_state
    app_state = 'stopped'
    print("\n🛑 Bot stopped.")

def print_debug_info():
    global app_state, elapsed_time
    print("\n📊 -------------------- Debug Info --------------------")
    print(f"App State: {app_state}")
    print(f"Elapsed Time: {elapsed_time}")

# --- Bot Logic ---
def run_bot():
    global app_state, lorem_text
    lorem_text = lorem_text.replace(': ', ':')
    while app_state != 'stopped':
        if app_state == 'running':
            for char in lorem_text:
                if app_state != 'running':
                    break  # Stop typing if paused or stopped
                pyautogui.write(char)
                time.sleep(1)
            pyautogui.press('enter')
            time.sleep(2)
        else:
            time.sleep(1)

def keyboard_listener():
    def on_press(key):
        if key == Key.up:
            resume_bot()
        elif key == Key.down:
            pause_bot()
        elif key == Key.right:
            stop_bot()
        elif key == Key.left:
            print_debug_info()

    with Listener(on_press=on_press) as listener:
        listener.join()

def timer_thread():
    global app_state, initial_time, elapsed_time
    while app_state != 'stopped':
        if app_state == 'running':
            current_time = round(time.time() - initial_time)
            elapsed_time = time.strftime("%H:%M:%S", time.gmtime(current_time))
            print(f"\rElapsed Time: {elapsed_time}", end="")
        time.sleep(1)

# --- Start Threads ---
if __name__ == "__main__":
    print("🚀 Starting Bot")
    print("Use ↑ to Resume, ↓ to Pause, → to Quit, ← for Status")
    initial_time = time.time()
    threading.Thread(target=keyboard_listener, daemon=True).start()
    threading.Thread(target=timer_thread, daemon=True).start()
    pause_bot()
    run_bot()
