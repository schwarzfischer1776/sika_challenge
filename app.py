import panel as pn

import pandas as pd




pn.extension()
journal_entry = pn.widgets.TextInput(name='Put a jounral entry here', placeholder='Enter a string here...').servable()
user_entry = pn.widgets.TextInput(name='Put the name of the journal enterer here', placeholder='Enter a string here...').servable()

user= ["Theo", "Theo", "Theo"]
df = pd.DataFrame({
  'Entry': [
    """Trying new fabrication method, namely to try new high-resolution mask for fabrication of photonic chip. 
        First attempt of using SU8 as a high resolution mask. Made one initial attempt for developuns SU8 using the following parameters: 
        Spin-Coating SU8 Soft Bake (3 min. at 60 degrees)
        Photolithography Exposure (lambda = 450 nm, P = 15 muW, t = 2 min.)
        Development (3 min. in SU8 developer)
        Looking at Chip under microscope;
        This attempt Failed; The development step dissolved all the SU8 for unknown reason""", 
    """As yesterday attempt of using SU8 as a high resolution mask. Made thurther attempts for developing SU8 
        using the same steps as yesterday with various different parameters, all failed. The development step still dissolved all the SU8 for unknown reason""",
    """Third attempt of using SU8 as a high resolution mask. Realised that I skipped a step (the post-expusure step) that was flagged as optional in the SU8 manual. Introducing the step turned out to make the process work. The steps I followed for my working version:1. Spin-Coating SU8
        Soft Bake (3 min. at 60 degrees)
        Photolithography Exposure (lambda = 450 nm, P = 15 muW, t = 2 min.)
        Post-Exposure Bake (4 min.)
        Development (3 min. in SU8 developer)
        Looking at Chip under microscope. This time I saw the SU8 on the chip after the development! --> method worked
    """ ],
}, index=user)

# Create a Panel column to hold the styled panes
styled_panes = []

# Define CSS styles for the panes
pane_style = {
    'background-color': 'white',
    'border-radius': '10px',  # Rounded corners
    'box-shadow': '2px 2px 5px 2px rgba(0, 0, 0, 0.2)',  # Shadow
    'padding': '10px',  # Padding
    'margin': '10px'  # Margin between panes
}

# Iterate through the DataFrame and create a styled pane for each row
for index, row in df.iterrows():
    content = f'Index: {index}, Entry: {row["Entry"]}'
    styled_pane = pn.pane.Str(content, style=pane_style)
    styled_panes.append(styled_pane)

# Create a Panel column to display the styled panes
styled_column = pn.Column(*styled_panes)

# Display the Panel column
styled_column.servable()



# Create a sample DataFrame
data = {'Entry': ['User1', 'User2', 'User3', 'User4']}
df = pd.DataFrame(data)

# Create a custom Panel component for the elaborate rows
class ElaborateRow(pn.Row):
    def __init__(self, index, entry, **params):
        # Create a round box for the index
        index_box = pn.pane.HTML(
            f'<div class="profile-image">{index}</div>',
            sizing_mode='fixed',
            height=40,
            width=40,
            style={'text-align': 'center', 'margin-right': '10px'}
        )
        
        entry_box = pn.pane.Str(
            entry,
            style={'background-color': 'white', 'border-radius': '10px', 'box-shadow': '2px 2px 5px 2px rgba(0, 0, 0, 0.2)', 'padding': '10px'}
        )

        super().__init__(
            index_box,
            entry_box,
            **params
        )

# Create a list of ElaborateRow instances
elaborate_rows = [
    ElaborateRow(index, row['Entry']) for index, row in df.iterrows()
]

# Combine the elaborate rows into a Panel Column
elaborate_column = pn.Column(*elaborate_rows)

# Apply CSS for styling
pn.extension(css_files=["custom_style.css"])

# Serve the Panel app
elaborate_column.servable()