"""
GUI Dashboard to display the current positions, unrealized PNL and the over all balance 
of the Futures Wallet. 
"""

import PySimpleGUI as sg
from client_wrapper import futures_account
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Settings
UPDATE_TIME = 30000     # milliseconds to wait between the data updates (default: 30s)

def draw_figure(fig, canvas):
   """ draw the "fig" matplotlib figure into the "canvas" PySimpleGUI widget """

   if canvas.children:
      # destroy left over children
      for child in canvas.winfo_children():
         child.destroy()
   
   # draw figure into canvas
   figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
   figure_canvas_agg.draw()
   figure_canvas_agg.get_tk_widget().pack(side='left', fill='both', expand=1)
   return


def hex_color(num):
   """ convert number into hex number in format: 'XX' """
   hex_c = hex(int(min(num, 255)))[2:]
   if len(hex_c) == 0:
      return '00'
   if len(hex_c) == 1:
      return '0' + hex_c
   return hex_c


def update_data(window):
   account_data = futures_account()
   
   positions = account_data['positions']
   pos_labels = []
   pos_sizes = []
   pos_colors = []            # for coloring according to unrealized PNL (0%: orange, otherwise color relative to scale between +-0% and +-100%)
   total_pnl = 0
   for pos in positions:
      pos_amt = float(pos['positionAmt'])
      if pos_amt < 0:
         pos_labels.append(f"SHORT {abs(pos_amt)} {pos['symbol']} ({pos['leverage']}x)\nmargin: {round(float(pos['initialMargin']), 2)}")
         pos_sizes.append(float(pos['positionInitialMargin']))
      elif pos_amt > 0:
         pos_labels.append(f"LONG {pos_amt} {pos['symbol']} ({pos['leverage']}x)\nmargin: {round(float(pos['initialMargin']), 2)}")
         pos_sizes.append(float(pos['positionInitialMargin']))

      if pos_amt != 0:
         uPNL = float(pos['unrealizedProfit'])
         total_pnl += uPNL
         if float(pos['positionInitialMargin']) != 0:
            rel_profit = uPNL / float(pos['positionInitialMargin'])
         else:
            rel_profit = 0

         if rel_profit > 0:
            # in profit
            pos_colors.append(f"#00{hex_color(50 + rel_profit * 255)}00")           # add 50 for not too dark
         elif rel_profit < 0:
            # in profit
            pos_colors.append(f"#{hex_color(50 + abs(rel_profit * 255))}0000")      # add 50 for not too dark
         else:
            pos_colors.append(f"#ff8400")

   # total margin in positions
   total_margin = sum(pos_sizes)

   total_wallet = 0
   assets = account_data['assets']
   for a in assets:
      if a['asset'] == 'USDT' or a['asset'] == 'BUSD':
         total_wallet += float(a['walletBalance'])

   # create a figure with identifier 0, to always reuse the same figure
   fig = plt.figure(0)
   fig.clf()      # clear figure
   fig.patch.set_facecolor('#2c2825')
 
   # Change color of text
   plt.rcParams['text.color'] = '#fdca52'
   
   # Create a circle at the center of the plot
   my_circle = plt.Circle( (0,0), 0.7, color='#2c2825')

   # Pieplot + circle on it
   plt.pie(pos_sizes, labels=pos_labels, colors=pos_colors)
   p = plt.gcf()
   p.gca().add_artist(my_circle)

   if total_margin != 0:
      total_rel_pnl = round(100 * total_pnl / total_margin, 2)
   else:
      total_rel_pnl = 0.0
   if total_rel_pnl > 0:
      p.text(0.5, 0.5, f"+{str(total_rel_pnl)}%", horizontalalignment='center', verticalalignment='center', fontsize=24, color='green')
   else: 
      p.text(0.5, 0.5, f"-{str(total_rel_pnl)}%", horizontalalignment='center', verticalalignment='center', fontsize=24, color='red')
   

   draw_figure(fig, window['fig_cv'].TKCanvas)
   window['-Balance-'].update(round(total_margin, 2))
   window['-PNL-'].update(round(total_pnl, 2))
   window['-Wallet-'].update(round(total_wallet, 2))
   return


def run_dashboard():
   # set theme
   sg.theme('DarkAmber')

   layout = [
      [sg.Text(text='Binance Futures Dashboard', size=(30,1), font=('Any', 24)), sg.Push(), sg.Button(button_text='Refresh', size=(8,1))],
      [sg.Column(
         layout=[[sg.Text(text='Futures Wallet Balance:\t', size=(30,1), font=('Any', 16)), sg.Text(text='0 USD', key='-Wallet-', size=(20,1), font=('Any', 16))],
         [sg.Text(text='Balance in Position:\t', size=(30,1), font=('Any', 16)), sg.Text(text='0 USD', key='-Balance-', size=(20,1), font=('Any', 16))],
         [sg.Text(text='Total unrealized PNL:\t', size=(30,1), font=('Any', 16)), sg.Text(text='0 USD', key='-PNL-', size=(20,1), font=('Any', 16))]]), sg.Push(), sg.Column(
         layout=[[sg.Canvas(key='fig_cv',size=(400, 300))]], background_color='#2c2825', pad=(0, 0))]  # canvas for graph
   ]

   # create window
   window = sg.Window(title='Binance Futures Dashboard', layout=layout, margins=(100, 80), resizable=True)

   window.read(timeout=0)
   update_data(window)

   # create event loop
   while True:
      # wait for an event or UPDATE_TIME milliseconds
      event, values = window.read(timeout=UPDATE_TIME)

      if event == sg.WIN_CLOSED:
         # End program if user closes window
         break
      
      # update data on dashboard
      update_data(window)

   window.close()
   return

if __name__ == '__main___':
   run_dashboard()
   