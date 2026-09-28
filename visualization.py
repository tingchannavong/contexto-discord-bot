# Helper functions to create game scores visualization

import plotly.graph_objects as go
import plotly.express as px
import re

def extract_last_three_numbers(text):
    """To get contexto averages close, medium, far-off."""
    # Split the string by periods and get the last part
    last_part = text.split('.')[-1].strip()

    # Use regular expression to find all numbers (1-3 digits) in the last part
    numbers = re.findall(r'\b\d{1,3}\b', last_part)
    # numbers[-3]

    # Return the last three numbers (or fewer if there aren't three)
    return numbers

def convert_to_int(extracted):
    new_list = []
    for i in extracted:
        converted = int(i)
        new_list.append(converted)
    return new_list

def make_pie_chart(user, user_data):
    """Make a pie chart to visualize contexto guesses in 3 categories: close, medium or far-off guesses. Save as png and return the image."""
    #Create labels and colors"
    labels = ['Close Guesses', 'Medium Guesses', 'Far Off Guesses']
    colors = ['#00FF00', '#ADD8E6', '#FF9999']

    #Calculate percentages
    total = sum(user_data[str(user.id)]['pie_dict'].values())
    percentage = [f'{(each/total)*100:.1f}%' for each in user_data[str(user.id)]['pie_dict'].values()]

    # Create the pie chart
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values= list(user_data[str(user.id)]['pie_dict'].values()),
        textinfo='label+percent',
        hoverinfo='label+percent+value',
        marker=dict(colors=colors, line=dict(color='#000000', width=2)),
        textposition='inside',
        insidetextorientation='radial'
    )])

    # Update layout
    fig.update_layout(
        title={
            'text': f"{user_data[str(user.id)]['name']}'s Average Contexto Guesses Visualized",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        showlegend=True,
        legend_title="Categories",
        font=dict(size=14)
    )

    # Save the figure as an image
    fig.write_image("pie.png")

    # Show the plot
    fig.show()