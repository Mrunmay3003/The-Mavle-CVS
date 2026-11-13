import unreal

def setup_interactable_actor():
    bp_path = "/Game/Blueprints/BP_BranchInteractable"
    bp = unreal.load_object(None, bp_path)
    
    if not bp:
        unreal.log_error(f"Could not load Blueprint at {bp_path}")
        return

    subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    root_data_handle = subsystem.k2_gather_subobject_data_for_blueprint(bp)

    if not root_data_handle:
        unreal.log_error("No root handle found for blueprint.")
        return

    parent_handle = root_data_handle[0]

    # Add Sphere Component
    sphere_params = unreal.AddNewSubobjectParams(
        parent_handle=parent_handle,
        new_class=unreal.SphereComponent,
        blueprint_context=bp
    )
    sphere_handle, fail_reason = subsystem.add_new_subobject(sphere_params)
    if not fail_reason:
        subsystem.rename_subobject(sphere_handle, "InteractionSphere")
        unreal.log("Successfully added InteractionSphere component!")

    # Add TextRender Component
    text_params = unreal.AddNewSubobjectParams(
        parent_handle=parent_handle,
        new_class=unreal.TextRenderComponent,
        blueprint_context=bp
    )
    text_handle, fail_reason = subsystem.add_new_subobject(text_params)
    if not fail_reason:
        subsystem.rename_subobject(text_handle, "InteractionPrompt")
        unreal.log("Successfully added InteractionPrompt component!")

    # Add StaticMesh Component (Bush/Branch)
    mesh_params = unreal.AddNewSubobjectParams(
        parent_handle=parent_handle,
        new_class=unreal.StaticMeshComponent,
        blueprint_context=bp
    )
    mesh_handle, fail_reason = subsystem.add_new_subobject(mesh_params)
    if not fail_reason:
        subsystem.rename_subobject(mesh_handle, "BranchMesh")
        unreal.log("Successfully added BranchMesh component!")

    unreal.EditorAssetLibrary.save_loaded_asset(bp)
    unreal.log("Saved BP_BranchInteractable successfully!")

def spawn_in_level():
    bp_class = unreal.load_class(None, "/Game/Blueprints/BP_BranchInteractable.BP_BranchInteractable_C")
    
    if not bp_class:
        unreal.log_warning("BP_BranchInteractable ready!")
        return

    location = unreal.Vector(200.0, 0.0, 50.0)
    rotation = unreal.Rotator(0.0, 0.0, 0.0)
    
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(bp_class, location, rotation)
    if actor:
        unreal.log(f"Spawned {actor.get_name()} at {location} in current level!")
        unreal.EditorLevelLibrary.save_current_level()

if __name__ == "__main__":
    setup_interactable_actor()
    spawn_in_level()
