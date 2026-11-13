import unreal

def create_branch_interaction():
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    editor_asset_subsystem = unreal.EditorAssetSubsystem()

    package_path = "/Game/Blueprints"
    bp_name = "BP_BranchInteractable"

    # Create folder if it doesn't exist
    if not editor_asset_subsystem.does_directory_exist(package_path):
        editor_asset_subsystem.make_directory(package_path)

    full_asset_path = f"{package_path}/{bp_name}"
    
    # Check if blueprint already exists
    if editor_asset_subsystem.does_asset_exist(full_asset_path):
        unreal.log_warning(f"Asset {full_asset_path} already exists. Skipping creation.")
        return

    # Create Actor Blueprint
    factory = unreal.BlueprintFactory()
    factory.set_editor_property("parent_class", unreal.Actor)

    new_bp = asset_tools.create_asset(bp_name, package_path, unreal.Blueprint, factory)
    
    if new_bp:
        unreal.log(f"Successfully created Blueprint: {full_asset_path}")
        unreal.EditorAssetLibrary.save_loaded_asset(new_bp)
    else:
        unreal.log_error("Failed to create Blueprint.")

if __name__ == "__main__":
    create_branch_interaction()
