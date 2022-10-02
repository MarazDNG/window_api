import logging
import time
import pygetwindow as gw
import win32process
import win32gui
import win32ui
import win32con
import re

from PIL import Image


def window_activate(partial_title: str):
    win = gw.getWindowsWithTitle(partial_title)[0]
    logging.debug(win)
    win.activate()
    time.sleep(2)


def window_activate_by_handler(hwnd: int):
    gw.Win32Window(hWnd=hwnd).activate()
    time.sleep(2)


# def window_start_pixel(window_id: int) -> tuple:
#     hwnd = win32process.GetWindowThreadProcessId(window_id)
#     x, y, _, _ = win32gui.GetWindowRect(hwnd)
#     return x, y


def window_start_pixel_by_title(partial_title: str) -> tuple:
    win = gw.getWindowsWithTitle(partial_title)[0]
    x, y, _, _ = win32gui.GetWindowRect(win._hWnd)
    return x, y


def window_id_by_title(partial_title: str):
    """Get mu game window process id with given player name.
    """
    win = gw.getWindowsWithTitle(partial_title)[0]
    return win32process.GetWindowThreadProcessId(win._hWnd)[1]


def window_title_by_title(partial_title: str) -> str:
    """Get whole window title from partial title.
    """
    win = gw.getWindowsWithTitle(partial_title)[0]
    return win32gui.GetWindowText(win._hWnd)


def window_handler_by_title(partial_title: str) -> int:
    """Get window handler from partial title.
    """
    return gw.getWindowsWithTitle(partial_title)[0]._hWnd


def window_title_by_handler(hwnd: int) -> str:
    return gw.Win32Window(hWnd=hwnd).title


def window_grab_image(hwnd, x: int, y: int, w: int, h: int) -> Image:
    """Return image with coordinates."""
    xw, yw, _, _ = win32gui.GetWindowRect(hwnd)
    win_start_pixel = (xw, yw)
    hdesktop = win32gui.GetDesktopWindow()
    hwndDC = win32gui.GetWindowDC(hdesktop)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    result = saveDC.BitBlt((0, 0), (w, h), mfcDC,
                           (win_start_pixel[0] + x, win_start_pixel[1] + y), win32con.SRCCOPY)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hdesktop, hwndDC)
    return im


def window_pixel_to_screen_pixel(hwnd, x: int, y: int) -> tuple:
    xw, yw, _, _ = win32gui.GetWindowRect(hwnd)
    return xw + x, yw + y


def window_handler_by_regex(regex: str) -> int:
    windows = gw.getAllWindows()
    windows = [w for w in windows if re.findall(regex, w.title)]
    return windows[0]._hWnd


if __name__ == '__main__':
    # id = window_id_by_title("Silco")
    # print(id)
    res = window_handler_by_regex("^MU$")
    print(res)
    print(window_title_by_handler(res))
    