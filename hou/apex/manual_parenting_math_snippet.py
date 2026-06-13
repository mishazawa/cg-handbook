guidesource: String = BindInput("Guides.skel", preset_kwargs={"label": "Guide Source"})
guides = character.findCharacterElement(primpath=guidesource)

fk_tag = "FK"
fk_nodes = graph.findNodes(f"%tag({fk_tag})")

for node in fk_nodes:
    ptnum = apex.skel.FindJoint(guides, node.name())
    if ptnum != -1:
        # save local rest xform to matrix value
        mat = apex.skel.getPointLocalTransform(guides, node.name())
        value_xform = graph.addNode(f"{node.name()}_rest_local", "Value<Matrix>")
        value_xform.setParms({"parm": mat})

        # and connect local rest to combine parm xform
        comb_xform = graph.addNode(
            f"{node.name()}_combine", "rig::CombineParmTransform::2.0"
        )
        value_xform.value_out.connect(comb_xform.restlocal_in)

        # combine local mat and parent ws mat to get ws mat
        ws_xform = graph.addNode(f"{node.name()}_ws", "Multiply<Matrix>")

        # BUT!
        parent = apex.skel.GetParent(guides, ptnum)
        if parent != -1:
            name = apex.skel.JointData(guides, parent)
            # parent xform should be animated. 
            parent_to = graph.FindFirstNode(name)
            parent_to.xform_out.connect(ws_xform.b_in)

        comb_xform.localxform_out.connect(ws_xform.a_in)

        ws_xform.result_out.connect(node.xform_in)

        # don't forget to promote animated ports
        r_port = graph.getConnectedPorts(node.r_in)[0]
        r_port.connect(comb_xform.r_in)
