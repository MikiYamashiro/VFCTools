from . import function


def getVisibleObjectList(camera_name=None, fromRenderSetting=True):
	(cam_dag, cam_mfn) = function.getCameraDagPath(camera_name)
	if (not cam_dag):
		raise Exception, "select a camera"
	frustum_obj = function.CustumTraversal(cam_dag, cam_mfn)
	frustum_obj.culling(fromRenderSetting)
	return frustum_obj.getItems()

