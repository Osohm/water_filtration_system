import FreeCAD,Part,math

class Lego:
    '''return a lego brick'''
    def __init__(self,obj, unitsX=4, unitsY=2):
        obj.addProperty("App::PropertyInteger","unitsX","Lego","Size in knobs in X direction.").unitsX = unitsX
        obj.addProperty("App::PropertyInteger","unitsY","Lego","Size in knobs in Y direction.").unitsY = unitsY
        obj.Proxy = self

    def onChanged(self, fp, prop):
        "Do something when a property has changed"
        pass

    def execute(self, fp):
        fp.Shape=Lego.buildshape(fp.unitsX, fp.unitsY)

    @staticmethod
    def buildshape(unitsX, unitsY):
        gap=0.1
        gaps=2*gap
        unitSize = 8
        height=9.6
        knobHeight=1.8
        knobRadius=4.8/2
        wall=1.5
        cylWall = 1.0
        upWall=1.5 #// guessed
        cylRadius = (unitSize*math.sqrt(2)-2*knobRadius)/2
        l,b=unitSize*unitsX-gaps, unitSize*unitsY-gaps
        c1=Part.makeBox(l, b, height,FreeCAD.Vector(-l/2.0,-b/2.0,0))
        c2=Part.makeBox(l-gaps-2*wall, b-gaps-2*wall, height,FreeCAD.Vector(-(l-gaps-2*wall)/2.0,-(b-gaps-2*wall)/2.0,-1*upWall))
        d1=c1.cut(c2)
        knobs=Part.Shape()
        knob=Part.makeCylinder(knobRadius,knobHeight+upWall/2,FreeCAD.Vector(0,0,height-upWall/2.0))
        for x in range(unitsX):
            for y in range(unitsY):
                newknob=knob.copy()
                newknob.translate((x*unitSize, y*unitSize, 0))
                if knobs.isNull():
                    knobs=newknob
                else:
                    knobs=knobs.fuse(newknob)
        knobs.translate(((1-unitsX)*unitSize/2, (1-unitsY)*unitSize/2, 0))
        if unitsX > 1 and unitsY > 1:
            cyl=Part.makeCylinder(cylRadius,height-upWall/2 ).cut(Part.makeCylinder(cylRadius-cylWall,height))
            cyl.translate((0,0,upWall/4))
            cyls=Part.Shape()
            for x in range(unitsX-1):
                for y in range(unitsY-1):
                    newcyl=cyl.copy()
                    newcyl.translate((x*unitSize, y*unitSize, 0))
                    if cyls.isNull():
                        cyls=newcyl
                    else:
                        cyls=cyls.fuse(newcyl)
            cyls.translate(((2-unitsX)*unitSize/2, (2-unitsY)*unitSize/2, 0))
    
            shape=knobs.fuse(d1).fuse(cyls)
        else:
            shape=knobs.fuse(d1)
        #Part.show(d1.common(cyls))
        return shape

def makeLego(x,y,doc=None):
    doc = doc or FreeCAD.ActiveDocument
    obj=doc.addObject("Part::FeaturePython","Lego")
    Lego(obj)
    obj.ViewObject.Proxy=0 # just set it to something different from None (this assignment is needed to run an internal notification)
    doc.recompute()
    return obj    
            
if __name__ == '__main__':
    #nonparametric
    #Part.show(Lego.buildshape(4,2))
    #parametric
    makeLego(4,2)

