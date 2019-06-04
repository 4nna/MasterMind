import os
import pandas as pd
import matplotlib.pyplot as plt



class Leaderboard():

    def __init__(self):
        sessionlogfile = '.mastermind_session.log'
        if os.path.exists('.mastermind.log'):
            # read in leaderboard
            self.table = pd.read_csv('.mastermind.log')
            # sort leaderboard
            self.table = self.table.sort_values(by=['score'], ascending=False)
            self.N = min(15, self.table.shape[0])
        if os.path.exists(sessionlogfile): #
            self.session = pd.read_csv(sessionlogfile, header=None)
            self.session.columns = ['date', 'game', 'repeat', 'name', 'dt', 'steps', 'col1', 'col2', 'col3', 'col4', 'pin_black', 'pin_white', 'reduced_possibilities']

    def write(self):
        mystring = ''
        for i in range(self.N):
            leaderline = "    ".join([str(entry)
                                     for entry in self.table[['date', 'name', 'score']].iloc[i]])
            mystring += leaderline + '\n'
        return mystring

    def top(self):
        return self.table[['date', 'name', 'score']][0:self.N]


    def stats(self):

        gdf = self.session.groupby(['game'])['steps', 'dt'].max()
       # print('min steps:', gdf.steps.min())
       # print('median steps:', gdf.steps.median())
       # print('min time:', gdf.dt.min())
       # print('median time:', gdf.dt.median())
        #fig, ax = plt.subplots(nrows=1, ncols=1)  # create figure & 1 axis
        fig = plt.figure(figsize=(3, 3))
        ax = fig.add_subplot(111)
        ax.plot(self.session.steps, self.session.reduced_possibilities, 'o')
        fig.savefig('stats.png', dpi=100)  # save the figure to file
        plt.close(fig)  # close the figure
