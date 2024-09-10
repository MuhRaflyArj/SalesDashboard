import plotly.graph_objects as go
import plotly.express as px

def sales_chart_spbu(df, products, num_col):
    # Create a Plotly figure
    fig = go.Figure()

    for product in products:
        data = df.loc[df["Material Name"] == product]
        # Add a trace for each product
        fig.add_trace(go.Scatter(
            x=data["Calendar Day"],
            y=data[num_col],
            mode='lines+markers',  # Display both lines and markers
            name=product,
            hovertemplate="<b>Product:</b> " + product + "<br><b>Date:</b> %{x}<br><b>" + num_col + ":</b> %{y:.2f}<extra></extra>"
        ))

    # Update the layout
    fig.update_layout(
        title=f"Tren {num_col} per Produk",
        xaxis_title='Date',
        yaxis_title=num_col,
        legend_title='Products',
        template='plotly',
        yaxis=dict(range=[0, df[num_col].max() * 1.25])
    )

    return fig  # Return the Plotly figure object

def sales_chart_region(df, regions, num_col) :
    # Create a Plotly figure
    fig = go.Figure()

    for region in regions:
        data = df.loc[df["Sales District"] == region]

        fig.add_trace(go.Scatter(
            x=data["Calendar Day"],
            y=data[num_col],
            mode="lines+markers",
            name=region,
            hovertemplate="<b>Region:</b>" + region + "<br><b>Date:</b> %{x}<br><b>" + num_col + ":</b> %{y:.2f}<extra></extra>"
        ))

    fig.update_layout(
        title=f"Tren {num_col} per Wilayah",
        xaxis_title="Date",
        yaxis_title=num_col,
        legend_title="Region",
        template="plotly",
        yaxis=dict(range=[0, df[num_col].max() * 1.25])
    )

    return fig

def sales_chart_keseluruhan(df, products, num_col):
    # Create a Plotly figure
    fig = go.Figure()

    for product in products:
        data = df.loc[df["Material Name"] == product]
        # Add a trace for each product
        fig.add_trace(go.Scatter(
            x=data["Calendar Day"],
            y=data[num_col],
            mode='lines+markers',  # Display both lines and markers
            name=product,
            hovertemplate="<b>Product:</b> " + product + "<br><b>Date:</b> %{x}<br><b>" + num_col + ":</b> %{y:.2f}<extra></extra>"
        ))

    # Update the layout
    fig.update_layout(
        title=f"Tren {num_col}",
        xaxis_title='Date',
        yaxis_title=num_col,
        legend_title='Products',
        template='plotly',
        yaxis=dict(range=[0, df[num_col].max() * 1.25])
    )

    return fig  # Return the Plotly figure object

def sales_chart_sh(df, products, num_col):
    # Create a Plotly figure
    fig = go.Figure()

    for product in products:
        data = df.loc[df["Material Name"] == product]
        # Add a trace for each product
        fig.add_trace(go.Scatter(
            x=data["Calendar Day"],
            y=data[num_col],
            mode='lines+markers',  # Display both lines and markers
            name=product,
            hovertemplate="<b>Product:</b> " + product + "<br><b>Date:</b> %{x}<br><b>" + num_col + ":</b> %{y:.2f}<extra></extra>"
        ))

    # Update the layout
    fig.update_layout(
        title=f"Tren {num_col} per Produk",
        xaxis_title='Date',
        yaxis_title=num_col,
        legend_title='Products',
        template='plotly',
        yaxis=dict(range=[0, df[num_col].max() * 1.25])
    )

    return fig  # Return the Plotly figure object


def sales_piechart(sales_data, value) :
    labels = list(sales_data.keys())
    values = [abs(i) for i in sales_data.values()]

    # Create a pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

    # Update layout for better visuals
    fig.update_layout(
        title_text=f'Rasio {value}',
    )

    return fig

def sales_barchart(data, value, title):
    # Extract labels and values from the dictionary
    labels = list(data.keys())
    values = list(data.values())
    formatted_values = [f"{value:,.0f}" for value in values]

    # Create a bar chart
    fig = go.Figure(data=[go.Bar(
        x=labels, 
        y=values, 
        text=formatted_values,  # Display the values on top of the bars
        textposition='inside'  # Position the text outside the bars
    )])

    # Update layout for better visuals
    fig.update_layout(
        title=title,
        xaxis_title=value,
        yaxis_title='Jumlah',
        template='plotly'
    )

    return fig

def sales_stacked_barchart(data, value, title) :

    # Extract data for the bar chart
    locations = list(data.keys())
    fuel_types = list({key for location in data.values() for key in location})

    # Create traces for each fuel type
    traces = []
    for fuel_type in fuel_types:
        values = [data[location].get(fuel_type, 0) for location in locations]
        traces.append(go.Bar(name=fuel_type, x=locations, y=values))

    # Create a stacked bar chart
    fig = go.Figure(data=traces)

    # Update the layout to be stacked
    fig.update_layout(
        title=title,
        barmode='group',
        xaxis_title="Region",
        yaxis_title=value,
        legend=dict(
            x=0.9,
            y=0.95, 
            bgcolor='rgba(225, 225, 225, 0.5)',  
            bordercolor='Black', 
        ),
    )

    return fig