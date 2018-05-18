import pandas as pd
import numpy as np
import transcription
from transcription import phrase_transformer


__dist_matrix__ = pd.read_csv('phon_data/distance_matrix.csv', index_col='index')


def __lev_distance__(a, b):

    """
	Расстояние Левенштейна для двух транскрипций. 
	Штраф за перестановки, удаление, вставку символа - 1. 
	Штраф за замену - расстояние между двумя звуками, вычисляемом по формуле: 
			1 - S_rows/ C_rows + Unc_rows*2
    """

    dis = np.zeros((len(a) + 1, len(b) + 1))
    i = 0
    row = 0
    col = 0

    while i < dis.size:

        if row == 0:
            if col != 0:
                dis[row, col] = dis[row, col-1] + 1

        elif col == 0:
            if row != 0:
                dis[row, col] = dis[row - 1, col] + 1

        elif row > 1 and col > 1 and a[row-1] == b[col-2] and a[row-2] == b[col-1]:
            dis[row, col] = dis[row - 3][col - 3] + 1

        else:
            dis[row, col] = np.min([dis[row, col - 1] + 1,  # левый
                                    dis[row - 1, col - 1] + __dist_matrix__[a[row-1]][b[col-1]],  # диаг      
                                    dis[row - 1, col] + 1])  # верхний

        col += 1
        i += 1
        if col == len(b) + 1:
            col = 0
            row += 1

    return dis[len(a), len(b)]

	
def phonetic_distance(word1, word2, stresses=False, transcription=False):
    
    """
    Расстояние между двумя словами на русском языке.
    Если варинатов транскрипции больше одного - выводятся все вохможные варианты.
    Если параметр transcription == True, будут выведены еще и сам разбор слов.
	
    >>> phonetic_distance('ехать', 'съехать', transcription=True)
    [['jехът’', 'сjехът’', 1.0]]
	
    >>> phonetic_distance('замок', 'замер', transcription=True)
    [['замък', 'зам’ьр', 0.6416666666666666],
    ['замък', 'зам’ер', 0.7666666666666666],
    ['замок', 'зам’ьр', 0.8916666666666666],
    ['замок', 'зам’ер', 0.7666666666666666]]
 	
    >>> phonetic_distance('замок', 'замок')
    [0.0, 0.25, 0.25, 0.0]

    """

    if not isinstance(word1, str) or not isinstance(word2, str):
        raise ValueError('Wrong data type')
    
    if word1 == '':
        return len(word2)
    
    if word2 == '':
        return len(word1)

    if stresses:

        if not isinstance(stresses, list):
            raise ValueError('Wrong data type')

        if len(stresses) != 2:
            raise ValueError('The number of stresses must be the same as the number of words')

        if not all(isinstance(x, int) for x in stresses):
            raise ValaueError('The stress values type must be int')

        word1 = phrase_transformer(word1, stresses=[(stresses[0])])
        word2 = phrase_transformer(word2, stresses=[(stresses[1])])

    else:
        word1 = phrase_transformer(word1)
        word2 = phrase_transformer(word2)

    if len(word1[0]) > 1:
        raise ValueError('Enter values must be words, not phrases')

    if len(word1[0]) > 1:
        raise ValueError('Enter values must be words, not phrases')

    answer = []

    for w1 in word1:
        for w2 in word2:

            if transcription:
                answer.append([''.join(w1[0]), ''.join(w2[0]), __lev_distance__(w1[0], w2[0])])
            else:
                answer.append(__lev_distance__(w1[0], w2[0]))

    return answer
