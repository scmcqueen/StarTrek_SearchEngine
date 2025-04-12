import hvplot.pandas
import numpy as np
import pandas as pd
import panel as pn
import re
import csv
# This is a demo file: It doesn't actually search, it emulates what the search would look like

# sets the background color as grey
pn.extension( global_css=[''':root { --design-primary-color: black;
    --mdc-theme-background: #eaeaea; 
    body {
    --mdc-theme-background: #eaeaea;
}
'''])

pn.extension(raw_css=['''.custom-button {
        background-color: #83f1b2;
        color: white;
        primary-color: red;
        border-radius: 5px;
        border-width: 0px;
    }
    '''])

craines = pn.widgets.Button(name='Craines')


def pretty_print(event):
    global search_results, ranking, craines
    temp_open = pn.pane.Markdown('### Results')
    column = pn.Column(temp_open)

    column.append(pn.pane.Markdown('''
        RIKER: I don't like fudge.
        **TROI: Really. I never met a chocolate I didn't like.**
        RIKER: Doesn't it taste good?

        _Star Trek: The Next Generation_, “The Game”
    '''))
    column.append(pn.pane.Markdown('''
        RIKER: Sure. I'll catch up with you later.
        **RIKER: Chocolate ice cream. Chocolate fudge. Chocolate chips. You're not depressed, are you?**
        TROI: I'm fine, Commander.

        _Star Trek: The Next Generation_, “The Game”
    '''))

    column.append(pn.pane.Markdown('''
        RIKER: I never knew it was a ritual. 
        **TROI: Chocolate is a serious thing.**
        RIKER: You know... I brought something back from Risa. It's better than chocolate.

        _Star Trek: The Next Generation_, “The Game”
    '''))
    column.append(pn.pane.Markdown('''
        WORF: I believe Commander Data's painting is making me dizzy... 
        **WORF: I thought this cake was chocolate... **
        TROI: Don't I wish.

        _Star Trek: The Next Generation_, “Parallels”
    '''))
    column.append(pn.pane.Markdown('''
        TROI: Transfer my mother's letters to my viewer...
        **TROI : ... and computer, I'd like a... a real chocolate sundae.**
        COMPUTER: Define ""real"" in context, please.

        _Star Trek: The Next Generation_, “The Price”
    '''))
    column.append(pn.pane.Markdown('''
        DATA: When Counselor Troi is in an unhappy mood, she often has something chocolate... 
        **Q: Chocolate...**
        DATA: For example, a hot fudge sundae. I cannot speak from personal experience, but I have seen it often has a profound psychological impact.
        
        _Star Trek: The Next Generation_, “Deja Q”
    '''))
    return(column)



# Set Widget
text_input = pn.widgets.TextInput( placeholder='Try "candle"',width = 550)
search_button = pn.widgets.Button(name='Search',css_classes=['custom-button'],
    button_type='light',button_style='outline', align="center")
# bind
search_button.on_click(lambda event: search(test_engine,text_input.value))

title_text = pn.pane.Markdown('## A _Star Trek_ Search Engine that prioritizes humor', align="center")

# Serve
pn.template.MaterialTemplate(
    title="Ad Aspera per Data",
    main=pn.Column(title_text,
    pn.Row(
        text_input,
        search_button,
        ),
    pn.bind(pretty_print,event=search_button)),
).servable()
