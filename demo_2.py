from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout


class DemoApp(App):
    _layout = None  # This will hold our root layout widget
    _disappearing_label = None  # This will hold the disappearing label widget
    _counter_label = None  # This will hold the counting label widget

    _counter = 0  # This will be our counter

    def build(self):

        self._layout = GridLayout(cols=2)

        '''Add a label to the layout. Note that, because we don't need to reference it outside of this 'build()' method,
        we can forego the local variable from demo_1 and construct the Label object directly in the call to 
        add_widget(). We're also setting the 'size_hint' property of the label to tell the parent that the label should
        take up 50% of the parent in the X dimension and 50% of the parent in the Y direction. You'll want to read more
        about layouts to understand what this means.'''
        self._layout.add_widget(Label(text="Text:", font_size=150, size_hint=(0.5, 0.5)))

        '''Create and add the disappearing label.'''
        self._disappearing_label = Label(text="Hello!", font_size=150, size_hint=(0.5, 0.5))
        self._layout.add_widget(self._disappearing_label)

        '''Now create and add yet another label. When we created the Grid Layout, we specified that it should contain
        two columns. Because we already added two labels above, adding this third label will cause the Grid Layout to
        create a new row. This label will appear in the first column of the second row.'''
        self._layout.add_widget(Label(text="Counter:", font_size=150, size_hint=(0.5, 0.5)))

        '''Create and add a counter label. We'll use Python's string formatting operator ('%') to dynamically create the
        label's text from our counter variable. Read more about this operator at:
        https://docs.python.org/3/library/stdtypes.html#printf-style-string-formatting'''
        self._counter_label = Label(text="%s" % self._counter, font_size=150, size_hint=(0.5, 0.5))
        self._layout.add_widget(self._counter_label)

        return self._layout

    def on_start(self):
        Clock.schedule_interval(self._update, 1.0)

    def _update(self, delta_time):
        if self._disappearing_label.opacity > 0:
            '''To prevent the text from jumping around, we're going to change the opacity of the label to hide/show it
            instead of adding/removing it from the layout. If the opacity is greater than zero, assume the label is
            already visible and hide it.'''

            '''Set the label's opacity to zero (0%) to hide it, while keeping it attached to the layout.'''
            self._disappearing_label.opacity = 0
        else:
            '''If the opacity is less than or equal to zero, assume the label is already hidden, so make it visible.'''

            '''Set the label's opacity to one (100%) to show it. FYI: you can also choose values between 0 and 1 to make
            the label semi-transparent.'''
            self._disappearing_label.opacity = 1

        '''Increment the counter and update the counter label's text.'''
        self._counter += 1
        self._counter_label.text = "%s" % self._counter


if __name__ == "__main__":
    '''Construct and run an instance of the DemoApp class.'''
    DemoApp().run()
