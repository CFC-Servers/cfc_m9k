import os

CFC_FOLDER_PREFIX = 'cfc_m9k_'
M9K_FOLDER_PREFIX = 'm9k_'

THIS_DIR = os.path.abspath('.')

LUA_HEADER =  'if SERVER then AddCSLuaFile() end\n\n'
LUA_HEADER += 'CFC_M9k_Stubber.registerStub( function()\n'

LUA_FOOTER = 'end )'

OUTPUT_DIR = 'test'

SENT_FIRST_LINE = '    local sent = scripted_ents.GetStored( "{}" ).t\n'
SENT_VAR_LINES  = '    sent.{} = {}\n'
WEP_FIRST_LINE  = '    local weapon = weapons.GetStored( "{}" )\n'
WEP_VAR_LINES   = '    weapon.{} = {}\n'


def safe_file_open(filename, mode='r'):
    try:
        f = open(filename, mode)
    except:
        print("ERROR: Could not open {}".format(filename))
        return None

    return f


def get_file_contents(filename):
    f = safe_file_open(filename)
    if not f:
        return ''

    return f.read()


def is_lua_file(filename):
    return filename.endswith('.lua')


def get_key_value_from_line(line):
    split = line.split('=')
    if len(split) < 2 or not (line.startswith('SWEP') or line.startswith('ENT')):
        return None, None

    if split[0].find('SWEP.') >= 0:
        key = split[0].strip().replace("SWEP.", "")
    elif split[0].find('ENT.') >= 0:
        key = split[0].strip().replace("ENT.", "")

    value = split[1]

    index = value.find('--')
    if index >= 0:
        value = value[:index]

    value = value.strip()

    return key, value


def get_key_values_from_lua(filename):
    key_value_pairs = {}

    contents = get_file_contents(filename)
    if not contents:
        return {}

    lines = contents.split('\n')
    for line in lines:
        key, value = get_key_value_from_line(line)
        if not key or not value:
            continue

        key_value_pairs[key] = value

    return key_value_pairs


def diff_lua_files(m9k, cfc):
    diff = {}

    m9k_dict = get_key_values_from_lua(m9k)
    cfc_dict = get_key_values_from_lua(cfc)

    for key in cfc_dict:
        cfc_value = cfc_dict[key]

        if key in m9k_dict:
            m9k_value = m9k_dict[key]

            if cfc_value != m9k_value:
                diff[key] = {
                    'm9k_value': m9k_value,
                    'cfc_value': cfc_value
                }
        else:
            diff[key] = {
                'cfc_value': cfc_value,
                'm9k_value': ''
            }

    return diff


def get_lua_files_from_list(files):
    lua_files = []
    for file in files:
        if is_lua_file(file):
            lua_files.append(file)

    return lua_files


def get_cfc_and_m9k_folders():
    this_dir = os.listdir()

    cfc_folders = []
    m9k_folders = []

    for d in this_dir:
        if d.startswith(CFC_FOLDER_PREFIX) and os.path.isdir(d):
            cfc_folders.append(d)
        elif d.startswith(M9K_FOLDER_PREFIX) and os.path.isdir(d):
            m9k_folders.append(d)

    return cfc_folders, m9k_folders


def get_first_lua_line_from_item(item_type, name):
    lua_line = ''

    if item_type == 'entities':
        lua_line = SENT_FIRST_LINE.format(name)
    elif item_type == 'weapons':
        lua_line = WEP_FIRST_LINE.format(name)

    return lua_line


def get_var_lua_line_from_item(item_type, key, value):
    lua_line = ''

    if item_type == 'entities':
        lua_line = SENT_VAR_LINES.format(key, value)
    elif item_type == 'weapons':
        lua_line = WEP_VAR_LINES.format(key, value)

    return lua_line


def write_weapon_or_ent_to_lua(file_ref, name, item):
    file_ref.write(LUA_HEADER)

    contents = ''

    item_type = item['item_type']

    contents += get_first_lua_line_from_item(item_type, name)
    contents += '\n'

    for key in item:
        if key == 'item_type':
            continue
        value = item[key]['cfc_value']

        contents += get_var_lua_line_from_item(item_type, key, value)

    file_ref.write(contents)

    file_ref.write(LUA_FOOTER)


def safe_create_folder(folder):
    try:
        os.mkdir(folder)
    except OSError:
        print('Directory {} already exists!'.format(folder))


def create_output_folder():
    safe_create_folder(OUTPUT_DIR)


def get_output_pack_path(pack):
    pack_path = '{}{}{}'.format(OUTPUT_DIR, os.sep, pack)

    return pack_path


def create_pack_folder(name):
    pack_path = get_output_pack_path(name)
    ent_dir = '{}{}{}'.format(pack_path, os.sep, 'entities')
    wep_dir = '{}{}{}'.format(pack_path, os.sep, 'weapons')

    safe_create_folder(pack_path)

    # To be used if we decide to separate weapons/ents
    #safe_create_folder(ent_dir)
    #safe_create_folder(wep_dir)

    return pack_path


def write_pack_to_lua(name, pack):
    pack_path = create_pack_folder(name)

    for key in pack:
        item = pack[key]

        #filename = '{}{}{}{}{}.lua'.format(pack_path, os.sep, item['item_type'], os.sep, key)
        filename = '{}{}{}.lua'.format(pack_path, os.sep, key)
        file = safe_file_open(filename, 'w')
        if not file:
            continue

        write_weapon_or_ent_to_lua(file, key, item)


def export_to_lua(diffs):
    create_output_folder()

    for key in diffs:
        pack = diffs[key]
        write_pack_to_lua(key, pack)


def main():
    cfc_folders, m9k_folders = get_cfc_and_m9k_folders()

    diffs = {}

    for d in m9k_folders:
        pack = d

        pack_diffs = {}

        for root, dirs, files in os.walk(d):
            for file in get_lua_files_from_list(files):
                split = root.split(os.sep)
                weapon_or_ent = split[-2]
                name = split[-1]

                m9k_filepath = '{}\\{}\\{}'.format(THIS_DIR, root, file)
                cfc_filepath = '{}\\cfc_{}\\{}'.format(THIS_DIR, root, file)

                diff = diff_lua_files(m9k_filepath, cfc_filepath)
                if diff:
                    pack_diffs[name] = diff
                    pack_diffs[name]['item_type'] = weapon_or_ent

        diffs[pack] = pack_diffs

    export_to_lua(diffs)


if __name__ == "__main__":
    main()
