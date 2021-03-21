class Case:
    def __init__(self,startingColor,startingType):
        self.type=startingType
        self.color=startingColor
    
    def getType(self):
        return self.type

    def getColor(self):
        return self.color

    def setType(self,newType):  
        self.type=newType
    
    def setColor(self,newColor):
        self.color=newColor
    
    def __repr__(self):
        return repr([self.color,self.type])


class Terrain:
    def __init__(self,long,larg):
        self.long=long
        self.larg=larg
        self.plateau = [[ Case(0,0) for x in range(long)] for y in range(larg)]
    
    def getCase(self,x,y):
        return self.plateau[x][y]

    def setColor(self,x,y,color):
        self.plateau[x][y].setColor(color)

    def setType(self,x,y,type):
        self.plateau[x][y].setType(type)
    
    def getLong(self):
        return self.long
    
    def getLarg(self):
        return self.larg
    
    def getColor(self,x,y):
        return self.plateau[x][y].getColor()
    
    def getType(self,x,y):
        return self.plateau[x][y].getType()
    
