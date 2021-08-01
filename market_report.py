import os
import argparse
import pandas as pd
import datetime as dt
from utils.inputs import stocks
from utils.market_data_puller import get_stock_data, calc_market_stats
from utils.plotter import get_plot_price_movement, save_plot_as_image
from utils.reporter import Reporter
import dataframe_image as dfi
import warnings

warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--img_path', type=str, default='images/')
parser.add_argument('-s', '--sender', type=str)
parser.add_argument('-p', '--password', type=str)
parser.add_argument('-r', '--receiver', type=str)
parser.add_argument('-e', '--host', type=str, default="smtp.gmail.com")
parser.add_argument('-n', '--port', type=int, default=587)
parser.add_argument('-t', '--subject', type=str, default='Daily Market Report (' + str(dt.datetime.now().date()) + ')')
args = parser.parse_args()

img_path = args.img_path
sender = args.sender
password = args.password
receiver = args.receiver
host = args.host
port = args.port
subject = args.subject


def build_stats_and_plots(stocks, img_path='images/'):
    format_dict = {}
    stats = pd.DataFrame(
        columns=['Open', 'High', 'Low', 'Close', 'Change', '%_Change', 'Total Volume (K)', 'Turnover (M)'])
    for stock in stocks:
        stock = stock.upper()
        data = get_stock_data(stock)
        stats = stats.append(calc_market_stats(data, stock))
        fig = get_plot_price_movement(data, stock)
        save_plot_as_image(fig, img_path, f'{stock}.png')

    for col in stats.columns.tolist():
        if '%' in col:
            format_dict[col] = '{:,.2f}%'
        elif 'Volume' in col:
            format_dict[col] = '{:,.0f}'
        elif 'Turnover' in col:
            format_dict[col] = '${:,.0f}'
        else:
            format_dict[col] = '${:,.2f}'

    dfi.export(stats.style. \
               bar(align='mid', color=['salmon', 'darkseagreen'], subset=['%_Change']). \
               bar(align='mid', color=['darkseagreen'], subset=['Total Volume (K)', 'Turnover (M)']). \
               format(format_dict), f"{img_path}stats_table.png")


if __name__ == "__main__":
    build_stats_and_plots(stocks, img_path)
    email = Reporter(sender, password, receiver, host, port, subject)
    images = [f"{img_path}{img}" for img in os.listdir(img_path) if img.split('.')[0] in stocks]

    email.build_message()
    email.build_image_grid(image_list=images, img_path=img_path, cols=3, offset=1)
    email.send_message()