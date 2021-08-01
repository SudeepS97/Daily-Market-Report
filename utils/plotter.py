import seaborn as sns
import plotly.graph_objs as go

sns.set()


def get_plot_price_movement(data, stock, width=450, height=350):
    fig = go.Figure()
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'], name='market data')
    )

    fig.update_layout(
        title=f'{stock} Daily Stock Price',
        yaxis_title='Stock Price',
        yaxis_tickformat='$',
        width=width,
        height=height
    )

    fig.update_xaxes(
        rangeslider_visible=False,
    )
    return fig


def save_plot_as_image(fig, path, filename):
    fig.write_image(path + filename)
