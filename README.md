# Daily-Market-Report
Consolidated email report displaying market information on configured stocks

## Table Of Contents
* Overview
* Requirements
* Installation
* Usage
* Args

## Overview
Reporting script that emails a table of price/volume stats and individual candlestick charts for a list of configurable stocks.

## Requirements
* An email account to send the reports from (if using gmail, you will need to use an account without two-factor authentication and less secure apps toggled ON: https://myaccount.google.com/u/1/lesssecureapps
* See Requirements.txt for dependencies

## Installation
Clone the repo to somewhere on your desktop
<code> git clone https://github.com/SudeepS97/Daily-Market-Report.git </code>

Configure the stocks you want to receive in your report in <code> utils/inputs.py </code>

## Usage
The report allows for an easy way to see how your watchlist performed on a given day, in an easily-automatable email.

Run the <code> market_report.py </code> script, listing at minimum the sender email, sender password, and recipient email:
![image](https://user-images.githubusercontent.com/32913961/127758916-267d5216-7a91-48ac-badf-b8062dd60ddf.png)

Plotting details can be configured in <code> utils/plotter.py </code> if you want to customize them.

The email will return an overview table and individual candlestick charts:
![image](https://user-images.githubusercontent.com/32913961/127759132-6d39c841-3a52-4204-b600-5c62c35f2948.png)


## Args
Required Args:
* <code>-s, --sender</code>
* <code>-p, --password</code>
* <code>-r, --receiver</code>

Optional Args:
* <code>-i, --img_path, default='images/'</code>
* <code>-e, --host, default='smtp.gmail.com'</code>
* <code>-n, --port, default=587</code>
* <code>-t, --subject, default='Daily Market Report (DATE)</code>
