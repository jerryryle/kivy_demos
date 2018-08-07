# Kivy Demos

These are some quick demos to show some [Kivy](http://kivy.org/) basics. They were built to help Reddit user u/Tanky321 get started with Kivy on a Raspberry Pi

I don't repeat comments in subsequent demos, so you'll want to read them in numerical order to get all of the explanations. 

## demo_1.py

This demo shows how to create a basic app based upon a Grid Layout with two Label widgets. One Label is repeatedly added and removed using a Kivy timer. This shows how to dynamically create a widget and add it to a layout.

You'll notice that the first label ('Text:') moves around as the second label ('Hello!') appears and disappears. This is because the Grid Layout dynamically adjusts as the second label is added/removed.

## demo_2.py

This demo shows how to control how much space a widget consumes in the layout by using size hints and how to add another row to the Grid Layout. It also demonstrates how to show/hide labels by changing their opacity and how to update a label's text.
 