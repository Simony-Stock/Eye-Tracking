#INSTALL LIBRARIES
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np

def heatmap_AOI(dataframe):
    cmap = 'Blues'
    g = sb.heatmap(dataframe, yticklabels=False, cmap = cmap)
    #create labels for x axis (bottom)
    x_labels = ['AOI 3', 'AOI 4']
    g.set_xticklabels(x_labels)
    #create 2nd x axis for top labels
    ax_Top = g.twiny()
    x_labels_top = ['', 'AOI 1', '', '', 'AOI 2']
    ax_Top.set_xticklabels(x_labels_top)
    #set title of heatmap
    g.set_title('Heatmap')
    plt.tight_layout()
    #save AOI heatmap as image
    plt.savefig('AOI_Heatmap.png')
    #display plot
    plt.show()
   

# save data from csv file as dataframe
df = pd.read_csv('q1fixIt2.csv')

#drop all rows with AOI = 0
df = df[df.AOI != 0]

#calculate frequency of points in each AOI
dataFreq = df[['AOI']].value_counts()

#convert series to list
dataFreq = dataFreq.tolist()

#group frequency values, list --> list of lists
N = 2
subList = [dataFreq[n:n+N] for n in range(0, len(dataFreq), N)]

#convert list of lists to dataframe
dfAOI = pd.DataFrame(subList, columns =['AOI 1', 'AOI 2'])

#create heatmap using function
heatmap_AOI(dfAOI)

#SCATTER PLOT/HEATMAP
dfPts = pd.read_csv('q1fix.csv')

#convert dataframe col/series to numpy array
left_x_array = dfPts['Left X'].to_numpy()
left_y_array = dfPts['Left Height'].to_numpy()
right_x_array = dfPts['Right X'].to_numpy()
right_y_array = dfPts['Right Height'].to_numpy()

#account for flipped screen, switch negative <--> positive
left_x_array = [abs(left_x_array[n]) if (left_x_array[n] < 0) else -(left_x_array[n]) for n in range(0, len(left_x_array))]

def heatmap_by_point(x_array, y_array):

    heatmap, xedges, yedges = np.histogram2d(x_array, y_array, bins=20, range=[[-0.4, 0.4], [0, 0.4]])
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    
    plt.clf()
    plt.imshow(heatmap.T, extent=extent, origin='lower', cmap='plasma_r')
    cb = plt.colorbar()
    plt.title('Frequency of Eye Gaze Points')
    plt.ylabel('Normalized Eye Height')
    plt.xlabel('Pupil Position')
    plt.text(-0.37, 0.35, 'AOI 1')
    plt.text(0.3, 0.35, 'AOI 2')
    plt.text(-0.37, 0.05, 'AOI 3')
    plt.text(0.3, 0.05, 'AOI 4')
    #save scatter heatmap as image
    plt.savefig('Scatter_Heatmap.png')
    plt.show()
    

#create heatmap by points using function
heatmap_by_point(left_x_array, left_y_array)

#AOI OVER TIME

# save data from csv file as dataframe
sourceFileName = 'q1fixIt2'
df2 = pd.read_csv(sourceFileName + '.csv')

yAxis = df2['AOI'].tolist()
xAxis = df2['Timestamp'].tolist()
plt.plot(xAxis,yAxis)
plt.title('Eye Fixation Points ' + '(Source: ' + sourceFileName + ')')
plt.xlabel('Time (ms)')
plt.ylabel('AOI (Areas of Interest)')
plt.yticks([0, 1, 2, 3, 4], [0, 1, 2, 3, 4])
#save scatter heatmap as image
plt.savefig('AOIvsTime_LineGraph.png')
plt.show()


plt.scatter(xAxis, yAxis)
plt.title('Eye Fixation Points ' + '(Source: ' + sourceFileName + ')')
plt.xlabel('Time (ms)')
plt.ylabel('AOI (Areas of Interest)')
plt.yticks([0, 1, 2, 3, 4], [0, 1, 2, 3, 4])
#save scatter heatmap as image
plt.savefig('AOIvsTime_Scatter.png')
plt.show()