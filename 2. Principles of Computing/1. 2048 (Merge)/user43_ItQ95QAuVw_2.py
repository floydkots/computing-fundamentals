"""
Author: Floyd Kots ~ github.com/floydkots
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """ 
    return slide_tiles(sum_tiles(slide_tiles(line)))
           
           
def sum_tiles(line):
    """
    Sums adjascent tiles of equal value
    """
    for index, _ in enumerate(line):
        if index + 1 < len(line) and line[index] == line[index+1]:
            line[index] += line[index + 1]
            line[index + 1] = 0
    return line


def slide_tiles(line):
    """
    Slides tiles to the left
    """
    slid = []
    for tile in line:
        if tile:
            slid.append(tile)
    slid += [0 for _ in range(len(line) - len(slid))]
    return slid
    
#line1 = [2, 0, 2, 4]
#line2 = [0, 0, 2, 2]
#line3 = [2, 2, 0, 0]
#line4 = [2, 2, 2, 2, 2]
#line5 = [8, 16, 16, 8]

#print line1, "->", merge(line1)
#print line2, "->", merge(line2)
#print line3, "->", merge(line3)
#print line4, "->", merge(line4)
#print line5, "->", merge(line5)
            
