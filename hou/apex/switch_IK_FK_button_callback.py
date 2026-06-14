CONTROL_NAME = "%CONTROL_NAME%"
SWITCH_NAME = "%SWITCH_NAME%"
FK_CTRL_TAG = "%FK_CTRL_TAG%"

from apex.scene_2 import *
from apex.constraintutils import updateConstraintMatrices
rigpath = state.primary_control.rpartition("/")[0]
parms = state.scene.getData(f"{rigpath}/graph_parms")
graph = state.scene.getData(f"{rigpath}/graph")
curr_blend = parms.get(f"{CONTROL_NAME}_{SWITCH_NAME}", True)

is_fk = curr_blend
next_state = "IK" if is_fk else "FK"

# print(f"current state: {'FK' if is_fk else 'IK'}")
# print(f"new state: {'FK' if not is_fk else 'IK'}")

new_parms = apex.Dict()
# assign new value
new_parms[f"{CONTROL_NAME}_{SWITCH_NAME}"] = not curr_blend

new_mapping = apex.Dict()

ctrls_path = [state.primary_control, f"{rigpath}/{CONTROL_NAME}"]


# hardcoded, but kind of not configurable from outside
root_ctrl = graph.matchNodes("%tag(module_root)")
if len(root_ctrl):
    root_ctrl = graph.nodeName(root_ctrl[0])
else:
    root_ctrl = "-1"

ik_root = graph.matchNodes("%tag(ik_root)")
if len(ik_root):
    ik_root = graph.nodeName(ik_root[0])
else:
    ik_root = "-1"



# create mapping
mapping = {}
bind_joints = graph.matchNodes("%tag(bindjoint__*) & %tag(bind)")

for nodeid in bind_joints:
    k = graph.nodeName(nodeid)
    fkid = graph.matchNodes(f"%tag({FK_CTRL_TAG}) & %tag({k})")
    if not len(fkid):
        continue
    fkjnt = graph.nodeName(fkid[0])

    ikid = graph.matchNodes(
        f"%tag(bindjoint__{k}) & (%tag(ik_tip) + %tag(ik_root) + %tag(ik_polevec))"
    )
    ikjnt = ""
    if len(ikid):
        ikjnt = graph.nodeName(ikid[0])

    if next_state == "IK":
        if ikjnt:
            mapping[k] = ikjnt
        # reset FK ctrls
        for char in "tr":
            key = f"{fkjnt}_{char}"
            if key in parms.keys():
                new_parms[key] = hou.Vector3()
        ctrls_path.append(f"{rigpath}/{fkjnt}")

    if next_state == "FK":
        mapping[k] = fkjnt
        # reset IK ctrls
        if ikjnt:
            for char in "tr":
                key = f"{ikjnt}_{char}"
                if key in parms.keys():
                    new_parms[key] = hou.Vector3()
            ctrls_path.append(f"{rigpath}/{ikjnt}")

# check if module constrained in animation state
# and not set xform to ik root when switching
def patch_xform_if_ik_constrained(xform, tgt):
    # ignore for FK
    if next_state != "IK":
        return xform

    # if no IK joints found
    if root_ctrl == "-1" or ik_root == "-1":
        return xform

    # if target not ik root
    if tgt != ik_root:
        return xform

    constr_ctrl = getConstrainedControls(state.scene)
    # if not constrained
    if not len(constr_ctrl):
        return xform

    for ctrl in constr_ctrl:
        _, _, b = ctrl.rpartition("/")
        if b == root_ctrl:
            return None # Found!
    return xform

graph_parms = apex.Dict()
graph_parms[rigpath] = new_parms

for src, tgt in mapping.items():
    xform = state.scene.getGraphOutputData(
        f"{rigpath}/control_data", key=f"{src}__xform"
    )
    if xform:
        xform = patch_xform_if_ik_constrained(xform, tgt)
        if xform:
            new_mapping[f"{rigpath}/{tgt}"] = xform
    

with hou.undos.group("my_callback"):
    state.updateControls(graph_parms, ctrls_path)
    state._selectControls([f for f in new_mapping.keys()], update_channel_widget=True)
    state.setControlXforms(new_mapping, smooth_rotate=True)
