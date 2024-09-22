import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator
from shiny.express import input, render, ui
import numpy as np
from pathlib import Path
from functools import partial
from shiny.ui import page_navbar

# Load CSV data (for simplicity, we're using only the first 1000 rows)
df = pd.read_csv(Path(__file__).parent / "Global YouTube Statistics.csv")
# df = pd.read_csv(r"C:\Users\anyas\OneDrive\Desktop\bioproject\shiny\demo\Global YouTube Statistics.csv", encoding='latin1', nrows=1000)

# Filter the data to only include rows where subscribers are under 50 million
df['subscribers'] = pd.to_numeric(df['subscribers'], errors='coerce')
df_filtered = df[df['subscribers'] < 50_000_000]
df_filtered = df_filtered.dropna(subset=['subscribers'])
df_filtered = df_filtered[np.isfinite(df_filtered['subscribers'])]

ui.page_opts(
    title="Youtuber App",  
    page_fn=partial(page_navbar, id="page"),  
)

with ui.nav_panel("Visualisation"):  
    with ui.layout_sidebar():
        with ui.sidebar(bg="#f8f8f8"):  

            # ui.input_dark_mode() # << 
            ui.input_slider("bins", "Number of bins", 0, 100, 20)
            ui.input_text("text", "Youtuber Search", "") 
        @render.plot(alt="A histogram") 
        def distPlot():
            # Creating the Visualization
            searchtext = input.text().strip().lower()
            if searchtext:
                final_output = df_filtered[df_filtered['Youtuber'].str.lower().str.contains(searchtext, na=False)]
            else: 
                final_output = df_filtered
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(final_output['subscribers'], input.bins(), color='blue', alpha=0.7, density=True)
            ax.set_title('Distribution of Subscribers')
            ax.set_xlabel('Subscribers')
            ax.set_ylabel('Density')

            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x)))  # Correct number format
            plt.xticks(rotation=45)
            plt.grid(True)
                
            return fig

with ui.nav_panel("Data"):  
    with ui.layout_columns():  
        with ui.card(): 


            @render.data_frame  
            def youtuber_df():
                searchtext = input.text().strip().lower()
                if searchtext:
                    final_output = df_filtered[df_filtered['Youtuber'].str.lower().str.contains(searchtext, na=False)]
                else: 
                    final_output = df_filtered
                return render.DataGrid(final_output)  