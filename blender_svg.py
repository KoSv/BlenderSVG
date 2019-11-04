###############TO DO: make rgb to hex//  make fill
##### bpy.context.object.data.splines.active.points for non bezier curves
##### FIRST COLOR IS BORDER SECOND IS FILL

import bpy
import xml.etree.cElementTree as ET

ET.register_namespace("","http://www.w3.org/2000/svg")

file_name = "test.svg" #your filename here!
doc_width = "1000px"
doc_height = "1000px"
factor = 30 # Path Size not Document
            
def spline_options(object):
    color_rgb = [0,0,0]
    global style
    #Border Color 1st Material Slot
    try:
        color_r = object.data.materials[0].diffuse_color[0]
        color_g = object.data.materials[0].diffuse_color[1]
        color_b = object.data.materials[0].diffuse_color[2]
        color_rgb[0] = int(color_r*255)
        color_rgb[1] = int(color_g*255)
        color_rgb[2] = int(color_b*255)
        strokecolor = hexify(color_rgb)
        borderalpha = object.data.materials[0].alpha
    except:
        strokecolor = "none"
        borderalpha = 1
        
    #Fill Color 2nd  Material Slot
    
    try:
        color_r = object.data.materials[1].diffuse_color[0]
        color_g = object.data.materials[1].diffuse_color[1]
        color_b = object.data.materials[1].diffuse_color[2]
        color_rgb[0] = int(color_r*255)
        color_rgb[1] = int(color_g*255)
        color_rgb[2] = int(color_b*255)
        fillcolor = hexify(color_rgb)
        fillalpha = object.data.materials[1].alpha
        
    except:
        fillcolor = "none"
        fillalpha = 1
        
    
    #APPLY STYLE#
    style = "fill:%s;fill-rule:evenodd;fill-opacity:%s;stroke:%s;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1" % (fillcolor, fillalpha,strokecolor)
        
def hexify(color):
    strip_n_pad = lambda stp: str(stp[2:]).zfill(2)
    return "#" + "".join([strip_n_pad(hex(col)) for col in color]) 

def find_curves(container):
    data_ob = bpy.data.objects
    for ob in data_ob:
        if ob.type == 'CURVE':
            
            string = ""
            for spline in ob.data.splines:
                
                string = string + str(Path_Creator(spline,ob))
            makePath(container, string, ob.name)

def makeContainer():
    global container
    global g_tag
    global doc_width
    global doc_height
    
    container = ET.Element("svg") # mach einen container
    container.set("xmlns:svg", "http://www.w3.org/2000/svg")
    container.set("xmlns", "http://www.w3.org/2000/svg")
    container.set("width", doc_width)
    container.set("height", doc_height)
    container.set("id", "svg1")
    container.set("version", "1.1")
    g_tag = ET.SubElement(container, "g")
    
    return container

def makePath(container, string, name):
    global g_tag
    path = ET.SubElement(g_tag, "path")
    path.set("style",style)
    path.set("d",string)
    path.set("name", name)
    
    
def makeFile(container):
    indent(container)
    tree = ET.ElementTree(container)
    tree.write(file_name, xml_declaration=True,encoding='utf-8',method="xml")

def indent(elem, level=0):
  i = "\n" + level*"  "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "  "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      indent(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
      elem.tail = i
    
def Path_Creator(spline,ob):
    global factor
    world_coords = ob.matrix_world
    string = "M "
    point_list = []
    
    try:
        spline.bezier_points[0].co # check if it is a bezier curve
    except:
        return
    
    c = 0
    points = spline.bezier_points
    first_point = points[0]
    for point in points:
        if c == 0: # prints the first point and only right handle
            string = string + str((ob.matrix_world * point.co)[0]*factor)
            string = string + ","
            string = string + str(((ob.matrix_world*point.co)[1]*-1)*factor)
            string = string + " C "
            string = string + str((ob.matrix_world * point.handle_right)[0]*factor)
            string = string + ","
            string = string + str(((ob.matrix_world * point.handle_right)[1]*-1)*factor)
            string = string + " "
        
        elif c == len(points)-1:# prints last left handle and last point
            string = string + str((ob.matrix_world * point.handle_left)[0]*factor)
            string = string + ","
            string = string + str(((ob.matrix_world * point.handle_left)[1]*-1)*factor)
            string = string + " "
            string = string + str((ob.matrix_world * point.co)[0]*factor)
            string = string + ","
            string = string + str(((ob.matrix_world * point.co)[1]*-1)*factor)
            
            if spline.use_cyclic_u:
                string = string + " "
                string = string + str((ob.matrix_world * point.handle_right)[0]*factor)
                string = string + ","
                string = string + str(((ob.matrix_world * point.handle_right)[1]*-1)*factor)
                string = string + " "
                string = string + str((ob.matrix_world * first_point.handle_left)[0]*factor)
                string = string + ","
                string = string + str(((ob.matrix_world * first_point.handle_left)[1]*-1)*factor)
                string = string + " "
                string = string + str((ob.matrix_world * first_point.co)[0]*factor)
                string = string + ","
                string = string + str(((ob.matrix_world * first_point.co)[1]*-1)*factor)
                string = string + " Z "
                
        else:#prints the rest
            string = string + str((ob.matrix_world * point.handle_left)[0]*factor)
            string = string + ","
            string = string + str(((ob.matrix_world * point.handle_left)[1]*-1)*factor)
            string = string + " "
            string = string + str((ob.matrix_world * point.co)[0]*factor)
            string = string + ","
            string = string + str(((ob.matrix_world * point.co)[1]*-1)*factor)
            string = string + " "
            string = string + str((ob.matrix_world * point.handle_right)[0]*factor)
            string = string + ","
            string = string + str(((ob.matrix_world * point.handle_right)[1]*-1)*factor)
            string = string + " "
            
        c += 1
    spline_options(ob)
    return string
    
def start_process():
    xml_file = makeContainer()
    find_curves(xml_file)
    makeFile(xml_file)

start_process()