from maya.OpenMaya import *
from maya.OpenMayaUI import *
from maya import cmds
import math


NODE_FILTER = [MFn.kMesh, MFn.kNurbsCurve, MFn.kNurbsSurface]


class CustumTraversal(MDrawTraversal):
    def __init__(self, dag, mfn):
        super(CustumTraversal, self).__init__()
        self.dag_camera = dag
        self.mfn_camera = mfn

    ## doesn`t work?
    # def filterNode(self, dag):
    #     return False

    #def filterItems(self, filter_list):

    def culling(self, from_rendersetting=True):
        if from_rendersetting:
            aspect_ratio = getRenderAspectRatio()
        else:
            aspect_ratio = self.mfn_camera.aspectRatio()

        fov = self.mfn_camera.horizontalFieldOfView()
        cam_matrix = self.dag_camera.inclusiveMatrix()
        near = self.mfn_camera.nearClippingPlane()
        far = self.mfn_camera.farClippingPlane()

        self.setPerspFrustum(fov, aspect_ratio, near, far, cam_matrix)
        self.traverse()

    def filterByNodeType(self, dag_node):
        for typ in NODE_FILTER:
            if dag_node.hasFn(typ):
                return True
        return False

    def getItems(self):
        return_list = []
        dag = MDagPath()
        for i in range(self.numberOfItems()):
            self.itemPath(i, dag)
            if self.filterByNodeType(dag):
                return_list.append(dag.partialPathName())
        return return_list


def getRenderAspectRatio():
    width = cmds.getAttr("defaultResolution.width")
    height = cmds.getAttr("defaultResolution.height")
    return (width / float(height))


def getCameraDagPath(camera_name=None):
    selection = MSelectionList()
    if camera_name == None:
        MGlobal.getActiveSelectionList(selection)
    else:
        selection.add(camera_name)
    if selection.length() == 0:
        return (None, None)

    dag = MDagPath()
    selection.getDagPath(0, dag)

    if dag.hasFn(MFn.kCamera) == False:
        return (None, None)

    return (dag, MFnCamera(dag))
