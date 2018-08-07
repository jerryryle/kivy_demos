from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout


class DemoApp(App):
    """We create an application class called 'DemoApp' that subclasses from the Kivy 'App' class. It will inherit all
    of the 'App' class functionality and we override methods or add our own to introduce new functionality that's
    specific to our application.
    """

    '''Here we declare class instance variables to hold onto widgets that we'll want to access throughout the class.
    It's not strictly necessary to declare these here since Python lets you declare new instance variables anywhere;
    however, it's considered good form to declare all instance variables here or in an '_init_()' method. If you
    create instance variables in random locations throughout the class, you can severely reduce readability.
    
    The underscore at the beginning of the variable name is a convention to indicate that the variable is 'private' to
    this class and not intended to be accessed outside of this class. This is also not strictly necessary and some
    Python developers might claim that private variables are an anti-pattern; however, I come from a C/C++ background, so
    I like the encapsulation and readability hints that private variables provide.'''
    _layout = None  # This will hold our root layout widget
    _disappearing_label = None  # This will hold the label widget

    def build(self):
        """build() is a method provided by the App class. The App object calls this during initialization after run() is
        called. We override build() to create our widget tree and we return the 'root' widget of our tree. The App object
        will embed this widget and all of its children in the main window.
        """

        '''Create a Grid layout to hold our other widgets. A "layout" is a special type of Kivy widget that contains
        other widgets and determines where they appear relative to each other. Read more about the Grid layout here:
        https://kivy.org/docs/api-kivy.uix.gridlayout.html'''
        self._layout = GridLayout(cols=2)

        '''Create a label. We're going to attach this to the grid layout and then never reference it again, so we'll 
        just use a local variable (no 'self') to temporarily hold onto it until we attach it to the layout. Note that,
        at this point, we've created a Label object in memory, but it's not attached to anything that will cause it to
        be displayed. If we did nothing else with this label, you'd never see it. Below, we'll attach the label to a 
        layout, which will be attached to the main window. Note that even though the local variable 'text_label' will go
        out of scope at the end of this function, the Grid layout will hold a reference to the Label object after we
        attach it with 'add_widget()' below, so the Python garbage collector will not delete the Label object.'''
        text_label = Label(text="Text:", font_size=150)

        '''Create another label. We're going to attach this to the grid layout below. Later, we'll detach and reattach 
        it repeatedly, so we want to hold onto it at the class level. (hence 'self')'''
        self._disappearing_label = Label(text="Hello!", font_size=150)

        '''Add the first label to the layout.'''
        self._layout.add_widget(text_label)

        '''Add the second label to the layout.'''
        self._layout.add_widget(self._disappearing_label)

        '''Return the grid layout as our root widget. Kivy will attach this to the main window, which will then display
        the layout and its children (the two labels).'''
        return self._layout

    def on_start(self):
        """Event handler for the `on_start` event which is fired after initialization (after build() has been called)
        but before the application has started running. We're going to use this event to schedule our timer that will
        modify the UI. We could have scheduled this in the 'build()' method above, but it's more proper to keep that
        method limited to code that constructs the UI and put other startup code in this 'on_start()' method instead.
        """

        '''Schedule a Kivy timer to call our _update() method every 1 seconds.'''
        Clock.schedule_interval(self._update, 1.0)

    def _update(self, delta_time):
        """_update() is our own private method that Kivy's Clock will call periodically to add/remove the "disappearing"
        label. The Clock.schedule_interval() call expects a method with one parameter ('delta_time'). The Clock will
        pass the time elapsed since the last call (or the original scheduling in the case of the first call). We do not
        need this value for our purposes, so we'll just leave the parameter unused."""

        if self._disappearing_label is None:
            '''If the '_disappearing_label' instance variable is 'None', then we assume the label has been removed from
            the Grid layout and deleted. Create a new Label and add it to the Grid layout.'''

            '''Add the label to the layout.'''
            self._disappearing_label = Label(text="Hello!", font_size=150)
            '''Add the label to the layout.'''
            self._layout.add_widget(self._disappearing_label)
        else:
            '''If the '_disappearing_label' instance variable is not 'None', then we assume the label is currently 
            attached to the Grid layout. Remove it from the layout and delete it.'''

            '''Remove the label from the layout.'''
            self._layout.remove_widget(self._disappearing_label)

            '''Set the instance variable to 'None'. Now we've 'lost' the Label object since nothing points to it. The
            Python garbage collector will eventually detect this and free the orphaned 'Label' object from memory (but
            we don't have to worry about that).'''
            self._disappearing_label = None


if __name__ == "__main__":
    '''Construct an instance of the DemoApp class.'''
    demo_app = DemoApp()

    '''Start the instance running.'''
    demo_app.run()
