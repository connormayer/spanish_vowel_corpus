import matplotlib
import numpy as np
import pandas as pd
from sklearn.manifold import MDS
import matplotlib.pyplot as plt

def perceptual_map():

    file = "C:\\Users\\Danny\\Desktop\\LSCI MAYER\\confusion_matrix.csv"

    data = pd.read_csv(file)
    data.drop('vowel', inplace=True, axis=1)
    print(data)
    matrixData = data.to_numpy(dtype=float)
    print(matrixData)

    #get normalized values
    sums = np.sum(matrixData, axis=1)
    sums = sums.reshape(-1, 1)
    normalized = matrixData / sums
    print(normalized)

    similarity = np.zeros([5, 5], dtype=float)

    for r in range(5):
        for c in range(5):
            similarity[r][c] = (normalized[r][c] + normalized[c][r]) / \
                               (normalized[c][c] + normalized[r][r])

    print(similarity)

    dissimilarity = -np.log(similarity)
    print("diss:")
    print(dissimilarity)

    mds = MDS(random_state=0, dissimilarity='precomputed')
    X_transform = mds.fit_transform(dissimilarity)
    print(X_transform)

    #plot = plt.scatter(X_transform[:,0], X_transform[:,1], label=['a', 'e', 'i', 'o', 'u'])
    #plt.legend()
    fig, ax = plt.subplots()
    ax.scatter(X_transform[:,0], X_transform[:,1])

    labels = ['a', 'e', 'i', 'o', 'u']
    for i, txt in enumerate(labels):
        ax.annotate(txt, (X_transform[i,0], X_transform[i,1]))
    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    perceptual_map()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
