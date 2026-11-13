import unreal

def create_walk_only_zone():
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    editor_asset_subsystem = unreal.EditorAssetSubsystem()

    package_path = "/Game/Blueprints"
    bp_name = "BP_WalkOnlyZone"

    if not editor_asset_subsystem.does_directory_exist(package_path):
        editor_asset_subsystem.make_directory(package_path)

    full_asset_path = f"{package_path}/{bp_name}"
    
    if not editor_asset_subsystem.does_asset_exist(full_asset_path):
        factory = unreal.BlueprintFactory()
        factory.set_editor_property("parent_class", unreal.Actor)
        bp = asset_tools.create_asset(bp_name, package_path, unreal.Blueprint, factory)
        unreal.log(f"Created Blueprint {full_asset_path}")
    else:
        bp = unreal.load_object(None, full_asset_path)
        unreal.log(f"Loaded existing Blueprint {full_asset_path}")

    if not bp:
        unreal.log_error("Failed to load/create BP_WalkOnlyZone")
        return

    # Add Box Component via SubobjectDataSubsystem
    subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    root_handles = subsystem.k2_gather_subobject_data_for_blueprint(bp)
    
    if root_handles:
        parent_handle = root_handles[0]
        box_params = unreal.AddNewSubobjectParams(
            parent_handle=parent_handle,
            new_class=unreal.BoxComponent,
            blueprint_context=bp
        )
        box_handle, fail_reason = subsystem.add_new_subobject(box_params)
        if not fail_reason:
            subsystem.rename_subobject(box_handle, "ZoneTrigger")
            unreal.log("Successfully added ZoneTrigger (BoxComponent)!")

    unreal.EditorAssetLibrary.save_loaded_asset(bp)
    unreal.log("Saved BP_WalkOnlyZone successfully!")

if __name__ == "__main__":
    create_walk_only_zone()
