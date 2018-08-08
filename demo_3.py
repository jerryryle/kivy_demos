import collections
from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
import time
import threading


class DemoApp(App):
    _layout = None  # This will hold our root layout widget
    _start_stop_button = None  # This will hold our start/stop button widget
    _10x_button = None  # This will hold our 10x button widget
    _counter_label = None  # This will hold the counting label widget

    _is_running = False  # This will track whether our counter is running
    _worker_thread = None  # This will hold the worker Thread object
    _thread_queue = None  # This will hold a queue for communicating with the worker thread

    def build(self):
        self._layout = GridLayout(cols=2)

        '''Create a start/stop button. We'll hold onto a reference to it because we'll want to alternate its text
        between "start" and "stop" when it's pressed.'''
        self._start_stop_button = Button(text='Start', size_hint=(0.5, 0.1))
        '''Bind our callback method to the button's "on_press" event. This tells Kivy to call our method when this 
        button is pressed.'''
        self._start_stop_button.bind(on_press=self._on_start_button_press)
        '''Add the button to the layout'''
        self._layout.add_widget(self._start_stop_button)

        '''Create a 10x button. We'll hold onto a reference to it because we'll want to enable/disable it when the
        start/stop button is pressed.'''
        self._10x_button = Button(text='10x', size_hint=(0.5, 0.1))
        '''Bind our callback method to the button's "on_press" event. This tells Kivy to call our method when this 
        button is pressed.'''
        self._10x_button.bind(on_press=self._on_10x_button_press)
        '''Add the button to the layout'''
        self._layout.add_widget(self._10x_button)
        '''Set the 10x button to "disabled" so the user can't click it. We only want it enabled after the "start" button
        has been pressed. Note that there seems to be a bug in Kivy v1.10.1 that requires that this property be set
        only after adding the widget to a layout. When this bug is fixed, you should be able to construct a disabled
        button above like so: "Button(text='10x', size_hint=(0.5, 0.1), disabled=True)" But this doesn't currently
        work.'''
        self._10x_button.disabled = True

        '''Create and add a static counter label.'''
        self._layout.add_widget(Label(text="Counter:", font_size=150, size_hint=(0.5, 0.5)))

        '''Create and add the counter label.'''
        self._counter_label = Label(text="0", font_size=150, size_hint=(0.5, 0.5))
        self._layout.add_widget(self._counter_label)

        return self._layout

    def on_start(self):
        """We'll start the counter thread when the user clicks the 'start' button, so there's nothing to do on app
        launch. We could remove the 'on_start()' method override now, but we'll keep it around in case we want to use
        it later. Python's 'pass' keyword lets us declare a method that does nothing."""
        pass

    def on_stop(self):
        """Event handler for the `on_stop` event which is fired when the app is closed."""

        '''If the user closes the app without first hitting the 'stop' button, then the thread will still be running.
        We need to stop it; otherwise, the app window will disappear, but Python will hang indefinitely waiting for the
        thread to terminate. So, we call '_stop_thread()' here to ensure that the thread is shut down. This method
        checks whether the thread is running and only attempts to terminate it if it is. So, it's safe to call here
        without a guard.'''
        self._stop_thread()

    def _start_thread(self):
        """This is our own helper method for starting a worker thread and creating a queue for communicating with it."""

        '''Guard against spawning a second worker thread while the first is running.'''
        if not self._is_running:

            '''Python's deque (double-ended queue: https://docs.python.org/3.7/library/collections.html#collections.deque)
            is safe to use across threads if you write to one end and read from the other. We'll use it as a very simple
            message queue to pass messages from the UI to the worker thread. This could be constructed once upon app 
            startup and reused; however, we'll recreate it and replace any old deque every time we start the thread. This
            isn't very expensive to do and it has the advantage of ensuring the message queue is empty when we start the
            thread.'''
            self._thread_queue = collections.deque()

            '''This creates a Thread object that will run our '_worker()' method in another thread. Our '_worker()' method
            doesn't currently expect any arguments (except 'self'). If we wanted to pass arguments to it, we could change
            its signature to add parameters and then pass them in using the 'args' tuple when we construct the Thread
            object here.'''
            self._worker_thread = threading.Thread(
                target=self._worker,
                args=())

            '''Start the thread running.'''
            self._worker_thread.start()

            '''Update our internal state to indicate that the worker thread is now running.'''
            self._is_running = True

    def _stop_thread(self):
        """This is our own helper method for stopping a worker thread."""

        '''Guard against trying to shut down a worker thread that's already terminated.'''
        if self._is_running:

            '''Append a 'die' message to the message queue. This will signal to the worker thread that we want it to 
            shut down as soon as possible.'''
            self._thread_queue.appendleft(('die', 0))

            '''Use join() to wait for the thread to terminate. It's possible to specify a timeout in case the thread
            hangs, but for this demo, we'll just wait indefinitely. Because this 'join()' blocks the main thread, the UI
            will freeze until the worker thread terminates and this join() call exits, so it's important to have the
            worker thread check its message queue somewhat frequently. Alternatively, if it's safe for your code to 
            spawn a new thread before the old one completely shuts down, you could choose to not use 'join()' here at
            all--you could just send the 'die' message and assume that the thread will eventually terminate. This keeps
            the UI responsive, but it could result in launching multiple threads if they take a while to terminate and
            the user keeps clicking the button.'''
            self._worker_thread.join()

            '''Update our internal state to indicate that the worker thread is no longer running.'''
            self._is_running = False

    def _on_start_button_press(self, instance):
        """_on_start_button_press() is our own private method that we bound to the start/stop button. Kivy will invoke
        this method whenever the button is pressed. Kivy expects a method with one parameter ('instance'). When Kivy
        calls this method, it will pass in the instance of the button that was pressed. This allows you to bind one
        method to a bunch of buttons and then figure out which button was pressed by inspecting the instance inside the
        method. Whether you bind one method to multiple buttons or separate methods to each button is up to you and
        really depends upon what you're doing. In this demo, we bind separate methods to each button, so we know that
        the 'instance' passed to us here will always be the start/stop button object."""

        if instance.text == "Start":
            '''The user just clicked "Start." Update the start/stop button text to "Stop"'''
            instance.text = "Stop"

            '''Enable the 10x button'''
            self._10x_button.disabled = False

            '''Start the worker thread'''
            self._start_thread()

        else:
            '''The user just clicked "Stop." Update the start/stop button text to "Start"'''
            instance.text = "Start"

            '''Disable the 10x button'''
            self._10x_button.disabled = True

            '''Stop the worker thread'''
            self._stop_thread()

    def _on_10x_button_press(self, instance):
        """_on_10x_button_press() is our own private method that we bound to the 10x button. This button is enabled
        once the start button is pressed to start the counter. It is disabled once the stop button is pressed to stop
        the counter. When the 10x button is disabled, it's impossible for the user to click it, so this method will not
        be invoked when the counter is not running. If you wanted to be really paranoid, you could--inside this
        method--check "self._is_running" before performing any action; however, it's reasonable to rely on
        the button being disabled and skip that check. If, for some reason, this method is called while the button is
        supposed to be disabled (and thus when the counter is not running), then that's likely programmer error."""

        '''Add a '10x' message to the queue. This will tell the worker thread to multiply the counter increment by 10.
        We actually append a tuple '('10x', 0)' to demonstrate how to send a command and associated data as a message;
        however, the second value of the tuple ('0') is currently ignored.'''
        self._thread_queue.appendleft(('10x', 0))

    @mainthread
    def _update_data(self, counter_value):
        """This helper method updates the counter label text. We've decorated it with Kivy's '@mainthread' decorator.
        This is 'magic' (a.k.a 'syntactic sugar') that will ensure that this method will always run in the main thread.
        Kivy (and most UI frameworks) are not inherently thread-safe and require that updates to UI elements happen in
        the main thread. The "@mainthread" decorator ensures that any call to our '_update_data()' method is wrapped
        with a call to 'kivy.clock.mainthread()', which schedules the call to occur in next available frame on the main
        thread. If we didn't use the '@mainthread' decorator, we'd need to remember to use
        'kivy.clock.mainthread(_update_data())' anywhere we call this method."""

        self._counter_label.text = "%s" % counter_value

    def _worker(self):
        """This is the method that will be invoked inside a new thread. It's safe to make blocking calls or do
        long-running computations inside this method because it will share time with the main UI thread instead of
        blocking it--so the UI will remain responsive."""

        '''Set up a counter variable and a counter increment variable. The counter increment variable tracks how much
        to add to the counter in each pass through the loop.'''
        counter = 0
        counter_increment = 1

        '''Loop forever. If we receive a 'die' message, we'll break out of this loop with a 'return' statement.'''
        while True:

            '''Sleep for 1 second. This is a blocking call that would normally freeze the UI if it were called on the
            main thread. If you're polling a GPIO or doing something fast periodically, you could just use Kivy's timers
            and avoid the complexity of threads . However, if you need to do something like issue a device read that
            will take some time to return, threads are a useful way to avoid freezing the UI. Note that you always want
            to make calls that time out and return after some reasonably short amount of time so that you can move on
            and service the message queue in a timely manner (1s max timeout is probably a decent guideline as users can
            probably tolerate a 1s delay in waiting for the thread to process a 'die' command and terminate, but 
            timeout values really depend upon your application).'''
            time.sleep(1)

            '''Increment the counter'''
            counter += counter_increment

            '''Update the counter label. Note that although it looks like we're calling this immediately from the worker
            thread, the '@mainthread' decorator on '_update_data()' actually schedules this to be run on the main thread
            at the next opportunity. This ensures that '_update_data()' safely accesses any UI elements from the main
            thread and not unsafely from the worker thread.'''
            self._update_data(counter)

            '''Now check the length of message queue to see if the UI thread sent us any messages. We'll loop and
            process any messages until the queue is empty.'''
            while len(self._thread_queue) > 0:
                '''Pop a tuple from the message queue. The 'command, data =' syntax automatically destructures the tuple
                into separate variables. Note that we're not currently using the 'data' part of the message. That's just
                to demonstrate one way of passing data in addition to a command string.'''
                command, data = self._thread_queue.pop()

                '''Process the message. Note that the commands are arbitrary strings we've chosen.'''
                if command == 'die':
                    '''If the UI sent us the 'die' command, return. Returning from the worker thread method terminates
                    the thread.'''
                    return
                elif command == '10x':
                    '''If the UI sent us the '10x' command, multiply the counter increment by 10. This will cause the
                    counter to count in larger increments. Not that there's any point to this--it's just an
                    easy-to-observe effect for this demo.'''
                    counter_increment *= 10

            '''As a final note, we could have created a second message queue to pass messages back to the main (UI)
            thread from the worker thread. On the main thread, we could have set up a timer to poll that message queue 
            and process messages from the worker thread on the main thread. That approach is just as valid as using the
            '@mainthread' decorator to create a method that's dispatched on the main thread. However, by using the
            '@mainthread' mechanism we can avoid additional polling on the main thread by directly scheduling method
            calls as needed.'''


if __name__ == "__main__":
    '''Construct and run an instance of the DemoApp class.'''
    DemoApp().run()
