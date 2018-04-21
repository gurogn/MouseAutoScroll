# !usr/bin/python
# -*- coding: utf-8 -*- 
import pythoncom
import pyHook
import win32api
import win32con
import threading

# Ctrl + Alt + L start or stop the scroll
# Alt + Up speed the scroll
# Alt + Down low the scroll

class MouseScroll:
    scroll_interval_list = [0.006, 0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 1.0]
    scroll_index = 3
    m_bIsScroll = False
    timer = 0

    def start_scroll(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -1)
        self.timer = threading.Timer(self.scroll_interval_list[self.scroll_index], self.start_scroll)
        self.timer.start()
        self.m_bIsScroll = True

    def stop_scroll(self):
        self.timer.cancel()
        self.m_bIsScroll = False

    def low_speed(self):
        if self.scroll_index < (len(self.scroll_interval_list) - 1):
            self.scroll_index += 1
        self.start_scroll()

    def high_speed(self):
        if self.scroll_index > 0:
            self.scroll_index -= 1
        self.start_scroll()

    def is_scrolling(self):
        return self.m_bIsScroll


class KeyboardMgr:
    m_bLKeyPressed = False
    m_bControlKeyPressed = False
    m_bCtrlAlt = False
    m_scroll = MouseScroll()
    m_bAnyAlt = False

    def on_key_down(self, event):
        if str(event.Key) == 'Lcontrol' or str(event.Key) == 'Rcontrol' and not self.m_bLKeyPressed:
            self.m_bControlKeyPressed = True
        if (str(event.Key) == 'Lmenu' or str(event.Key) == 'Rmenu'):
            if self.m_bControlKeyPressed:
                self.m_bCtrlAlt = True
            else:
                self.m_bAnyAlt = True

        if str(event.Key == 'L'):
            self.m_bLKeyPressed = True

        if self.m_bCtrlAlt and str(event.Key) == 'L' and self.m_bControlKeyPressed:
            if not self.m_scroll.is_scrolling():
                self.m_scroll.start_scroll()
            else:
                self.m_scroll.stop_scroll()
        if self.m_scroll.is_scrolling() and self.m_bAnyAlt:
            if str(event.Key) == 'Up':
                self.m_scroll.stop_scroll()
                self.m_scroll.high_speed()
            elif str(event.Key) == 'Down':
                self.m_scroll.stop_scroll()
                self.m_scroll.low_speed()
        return True

    def on_key_up(self, event):
        if str(event.Key) == 'Lcontrol' or str(event.Key) == 'Rcontrol':
            self.m_bCtrlAlt = False
            self.m_bControlKeyPressed = False
        elif str(event.Key) == 'Lmenu':
            self.m_bCtrlAlt = False
            self.m_bAnyAlt = False
        elif str(event.Key) == 'L':
            self.m_bLKeyPressed = False
        return True


# # 创建钩子管理对象
keyMgr = KeyboardMgr()
hm = pyHook.HookManager()

# # #监听键盘事件
hm.KeyDown = keyMgr.on_key_down
hm.KeyUp = keyMgr.on_key_up

hm.HookKeyboard()
# #一直监听，直到手动退出
pythoncom.PumpMessages()
