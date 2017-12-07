import atexit
import win32con
import win32gui
import win32api

inputs = []
low_level_handlers = []
handlers = []
callbacks = []
hooks = []


def listener():

    def process_event(event):
        for h in handlers:
            h(event)

    for i in inputs:
        handler = i.generate_handler()
        handlers.append(i.generate_handler())
        callback = i.generate_callback(handler)
        callbacks.append(callback)
        hook = i.generate_hook(callback)
        hooks.append(hook)

    # Unregister the hook at exit
    def unhook_register():
        print('unhooked')
        for i in inputs:
            i.unhook()

    atexit.register(unhook_register)

    # Retrieves a message from the calling thread's message queue. The function dispatches incoming sent messages until
    # a posted message is available for retrieval.
    print("Begin pumping..")
    win32gui.PumpMessages()


def add_input(inp):
    inputs.append(inp)


def stop_pumping(thread_id):
    # Posts a Quit message to the message queue
    win32api.PostThreadMessage(thread_id, win32con.WM_QUIT, 0, 0)
