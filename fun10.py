import wx
import pcbnew
import os

def getNetID(netName):
    board = pcbnew.GetBoard()
    net = board.FindNet(netName)
    if net:
        return net.GetNetCode()
    return None

def getLayerID(layerName):
    board = pcbnew.GetBoard()
    layer_id = board.GetLayerID(layerName)
    if layer_id != pcbnew.UNDEFINED_LAYER:
        return layer_id
    return None

def addZone(points, layerName, netName, clearance=0.5, refresh=1):
    board = pcbnew.GetBoard()
    zone = pcbnew.ZONE(board)
    zone.SetNetCode(getNetID(netName))
    zone.SetLayer(getLayerID(layerName))
    zone.SetLocalClearance(pcbnew.FromMM(clearance))
    
    chain = pcbnew.SHAPE_LINE_CHAIN()
    for point in points:
	    chain.Append(pcbnew.FromMM(point[0]), pcbnew.FromMM(point[1]))
    chain.SetClosed(True)
    zone.Outline().AddOutline(chain)
    
    board.Add(zone)

    if refresh == 1:
        pcbnew.Refresh()

def addVia(pos, width, drill, netName, refresh=1):
    board = pcbnew.GetBoard()
    via = pcbnew.PCB_VIA(board)

    # VECTOR2I replaces wxPoint
    via.SetPosition(pcbnew.VECTOR2I(
        pcbnew.FromMM(pos[0]),
        pcbnew.FromMM(pos[1])
    ))
    via.SetDrill(pcbnew.FromMM(drill))
    via.SetWidth(pcbnew.FromMM(width))
    via.SetNetCode(getNetID(netName))
    board.Add(via)

    if refresh == 1:
        pcbnew.Refresh()

def addTrack(start, end, layerName, netName, width, refresh=1):
    board = pcbnew.GetBoard()
    track = pcbnew.PCB_TRACK(board)

    # VECTOR2I replaces wxPoint
    track.SetStart(pcbnew.VECTOR2I(
        pcbnew.FromMM(start[0]),
        pcbnew.FromMM(start[1])
    ))
    track.SetEnd(pcbnew.VECTOR2I(
        pcbnew.FromMM(end[0]),
        pcbnew.FromMM(end[1])
    ))
    track.SetLayer(getLayerID(layerName))
    track.SetNetCode(getNetID(netName))
    track.SetWidth(pcbnew.FromMM(width))
    board.Add(track)

    if refresh == 1:
        pcbnew.Refresh()

def getNetNames():
    board = pcbnew.GetBoard()
    return list(board.GetNetsByName().keys())
