from pyramid.path import package_name as package_name, package_path as package_path

def resolve_asset_spec(spec, pname: str = '__main__'): ...
def asset_spec_from_abspath(abspath, package): ...
def abspath_from_asset_spec(spec, pname: str = '__main__'): ...
