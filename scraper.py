from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests
import json
import io
import plotly.express as px
from plotly.graph_objs import Pie, Layout,Figure
import plotly.graph_objects as go

import pandas as pd
class Page:

    def __init__(self):
        #self.browser = webdriver.Firefox()
        self.url = "https://www.tradingview.com/symbols/NASDAQ-TSLA/ideas/?sort=recent"
        self.request,self.soap,self.data_div = self.set_page_parsing()

    def set_page_parsing(self):
        # self.browser.get(self.tsla)
        page = requests.get(self.url)
        soap = bs(page.content, features="lxml")
        mydivs = soap.find_all('div', class_='tv-feed__item js_cb_class tv-feed-layout__card-item')
        return page,soap,mydivs

    def set_data_div(self):
        pass
    def long_or_short(self):
        position = []
        for idea in self.data_div:
            long_short_flag = 0 # -1 = short , 1 = long , 0 = NonePosition Of the user
            temp_next=idea.next()
            temp_slice= temp_next[2]
            for i in temp_slice.contents:
                temp = str(i)
                if "</span>Short</span>" in temp:
                    position.append("Short")
                    long_short_flag = -1
                elif "</div>Long</span>" in temp:
                    position.append("Long")
                    long_short_flag = 1
            if long_short_flag == 0:
                position.append("None")
        return position

    def idea_info(self):
        mydivs = self.soap.find_all('div', class_='tv-feed__item js_cb_class tv-feed-layout__card-item')
        jsonlist = []
        for i in mydivs:
            jsonlist.append(json.loads(i.get('data-card')))

        return jsonlist


    def get_user_pos(self):
        temp_dict = {}
        pos = self.long_or_short()
        info = self.idea_info()
        for i in range(len(pos)):
            temp_dict[info[i]["author"]["username"]] = pos[i]
        return temp_dict

    def users_positon_table(self):
        df= self.user_pos_to_df(html_string=True).copy()

        str_io = io.StringIO()
        df.to_html(buf=str_io, classes='table',index=False)
        html_str = str_io.getvalue()
        return html_str
    def user_pos_to_df(self,html_string=False):
        ls = [[], []]
        data = self.get_user_pos()
        for key in data:
            ls[0].append(key)
            ls[1].append(data[key])
        dic = {"users": ls[0], "positions": ls[1]}

        df = pd.DataFrame.from_dict(dic)
        if not html_string:
            df.set_index('users', inplace=True)
        return df
    def pie_chart(self):
        self.users_positon_table()
        user_pos_df = self.user_pos_to_df()
        labels = ["Long", "Short"]
        values = [user_pos_df[user_pos_df["positions"] == "Long"].count().to_list()[0],
                  user_pos_df[user_pos_df["positions"] == "Short"].count().to_list()[0]]
        print(values)
        colors = ['Lime', 'Red']
        config = dict({"responsive": True, "displaylogo": False})
        fig = go.Figure(data=[go.Pie(labels=labels, values=values,title="Tsla")])
        fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                          marker=dict(colors=colors, line=dict(color='#000000', width=2)))
        fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)",
                           'paper_bgcolor': 'rgba(0, 0, 0, 0)'},title={
        'text': "Plot Title",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},title_font_size=50)

        return fig.to_json()


#test = {'Bullishcharts': 'Long', 'quanttraderX': 'Long', 'cyclewave': 'None', 'BlockchainYahoo': 'Long', 'thestocksking': 'None', 'ashwinpv9': 'Short', 'contemplatingcrypto': 'None', 'tusheet': 'None', 'Apple_Tesla_trader': 'Long', 'SFCAtrader': 'Short', 'IngenuityTrading': 'None', 'MohammadAlajami': 'None', 'AftabAli': 'Short', 'jdlev': 'Long', 'holmes4': 'None', 'Deepthoughts': 'Long'}



#<div class="tv-feed__item js_cb_class tv-feed-layout__card-item js-feed__item--inited" data-card='{"data":{"id":9392173,"name":"TSLA breakout update","short_name":"TSLA","image_url":"vskuobFo","published_url":"https://www.tradingview.com/chart/TSLA/vskuobFo-TSLA-breakout-update/","is_script":false,"is_public":true,"base_url":"https://www.tradingview.com"},"author":{"username":"StrikeTrading","is_broker":false}}' data-uid="vskuobFo" data-widget-data='{"id":9392173,"image_url":"vskuobFo","like_score":4,"result_score":4,"user":{"id":14350939},"current_user":{"votedForChart":false},"chart_owner":false,"status":{"is_active":true},"published_chart_url":"/chart/TSLA/vskuobFo-TSLA-breakout-update/","name":"TSLA breakout update","short_symbol":"TSLA"}' data-widget-type="idea"><div class="tv-widget-idea js-userlink-popup-anchor">

#<div class="tv-widget-idea__symbol-info"><a class="tv-widget-idea__symbol apply-overflow-tooltip" href="/symbols/NASDAQ-TSLA/">TSLA</a></div>