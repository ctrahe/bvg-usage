import plotly
import plotly.plotly as py
import plotly.graph_objs as go    
from datetime import datetime


details = input('Cost dict: ')

class PlotBvgUsage():

    def __init__(self):
        plotly.tools.set_credentials_file(username='ctrahe', api_key='22BI8agOwIuFRbsl9L6I')
        
        # Daily cost
        self.plot_bvg_usage('Daily usage', details)
        # monthly cost overview
        monthly_details = self.group_by_month(details)
        self.plot_bvg_usage('Monthly Cost Overview', monthly_details)

    def plot_bvg_usage(self, graph_name, ticket_details):
        x = []
        y = []
        for date, price in ticket_details.items():
            x.append(date)
            y.append(price)
        try:
            py.iplot([ go.Scatter( x=x, y=y, name=graph_name )])
        except:
            pass

    def group_by_month(self, ticket_details):
        monthy_usage = {}
        for date, price in ticket_details.items():
            if price == '0.00' or price == '0':
                continue
            month = self.format_date(date, '%d/%m/%y', '%m/%y')
            if month in monthy_usage:
                monthy_usage[month] = str(float(monthy_usage[month]) + float(price))
            else:
                monthy_usage[month] = price
        
        return monthy_usage

    def format_date(self, date, format, output):
        return datetime.strptime(date, format).strftime(output)

PlotBvgUsage = PlotBvgUsage()