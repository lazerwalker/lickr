import kivy
kivy.require('1.0.6')
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Point, GraphicException
from random import random
from math import sqrt

def calculate_points(x1, y1, x2, y2, steps=5):
    dx = x2 - x1
    dy = y2 - y1
    dist = sqrt(dx * dx + dy * dy)
    if dist < steps:
        return None
    o = []
    m = dist / steps
    for i in range(1, int(m)):
        mi = i / m
        lastx = x1 + dx * mi
        lasty = y1 + dy * mi
        o.extend([lastx, lasty])
    return o


class lickr(FloatLayout):

    def on_touch_down(self, touch):
        win = self.get_parent_window()
        ud = touch.ud
        ud['group'] = g = str(touch.uid)
        pointsize = 5

        with self.canvas:
            ud['lines'] = [
                Rectangle(pos=(touch.x, 0), size=(1, win.height), group=g),
                Rectangle(pos=(0, touch.y), size=(win.width, 1), group=g),
                Point(points=(touch.x, touch.y), group=g)]

        ud['label'] = Label(size_hint=(None, None))
        self.update_touch_label(ud['label'], touch)
        self.add_widget(ud['label'])
        touch.grab(self)
        return True

    def on_touch_move(self, touch):
        if touch.grab_current is not self:
            return
        ud = touch.ud
        ud['lines'][0].pos = touch.x, 0
        ud['lines'][1].pos = 0, touch.y
        index = -1

        while True:
            try:
                points = ud['lines'][index].points
                prevX, prevY = points[-2], points[-1]
                break
            except:
                index -= 1

        points = calculate_points(prevX, prevY, touch.x, touch.y)

        if points:
            try:
                lp = ud['lines'][-1].add_point
                for idx in range(0, len(points), 2):
                    lp(points[idx], points[idx + 1])
            except GraphicException:
                pass
        #Coordinates redraw
        ud['label'].pos = touch.pos
        import time
        t = int(time.time())
        if t not in ud:
            ud[t] = 1
        else:
            ud[t] += 1
        self.update_touch_label(ud['label'], touch)

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return
        touch.ungrab(self)
        ud = touch.ud
        self.canvas.remove_group(ud['group'])
        self.remove_widget(ud['label'])
################################################################################
################################################################################
################################################################################
#Updating Coordinates. Here we need to package the coordinates into a buffer
#that will then be sent to the Gestalt modules using the Gestalt code.
################################################################################
################################################################################
################################################################################
    def update_touch_label(self, label, touch):
        label.text = 'Coordinates: (%d, %d)' % (
             touch.x, touch.y)
        print(int(touch.x),int(touch.y))
        label.texture_update()
        label.pos = touch.pos

class lickrApp(App):
    def build(self):
        return lickr()

    def on_pause(self):
        return True

if __name__ == '__main__':
    lickrApp().run()
