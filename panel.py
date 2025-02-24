import hvplot.pandas
import numpy as np
import pandas as pd
import panel as pn
import simple_search_func as ss

# Set global variables
PRIMARY_COLOR = "#0072B5"
SECONDARY_COLOR = "#B54300"
CSV_FILE = (
    "https://raw.githubusercontent.com/holoviz/panel/main/examples/assets/occupancy.csv"
)

pn.extension(design="material", sizing_mode="stretch_width")

@pn.cache
def get_data():
    return pd.read_csv(CSV_FILE, parse_dates=["date"], index_col="date")

data = get_data()

data.tail()

# Functions


# Set Widget
text_input = pn.widgets.TextInput(name='Text Input', placeholder='Enter a string here...')

# Serve
pn.template.MaterialTemplate(
    site="SI 699 Final Project",
    title="Star Trek Search Engine",
    sidebar=['hellow', text_input],
    main=['good bue'],
).servable() # The ; is needed in the notebook to not display the template. Its not needed in a script