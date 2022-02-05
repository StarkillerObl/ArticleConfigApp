import json
import sqlite3
import uuid
import db_access

def main():
    db_access.create_tables()
    # add_two_first_entries()
    # for row in view():
        # print(row)
    # document = get_article_config('773532b0-233e-4a28-86fb-06a46ad30760')
    # print(json.dumps(document))
    # snapshot_id = create_snapshot('773532b0-233e-4a28-86fb-06a46ad30760')
    # print(f'snapshot id: {snapshot_id}')
    # add_config_using_snapshot()
    document_using_snapshot = get_article_config('da734f24-20d3-4114-b05a-c455e9f5f9ed')
    print(json.dumps(document_using_snapshot, indent=4, sort_keys=True))



def add_two_first_entries():
    first_id = f'{uuid.uuid4()}'
    second_id = f'{uuid.uuid4()}'

    db_access.insert_data(first_id, 'None', 'None', '/article_name', '11000-01')
    db_access.insert_data(second_id, first_id, 'article_config', '/article_name', 'Sample Article')

def add_config_using_snapshot():
    id = f'{uuid.uuid4()}'
    snapshot_id = '3504740e-f255-4622-9fb6-12f66ed2538e'

    db_access.insert_data(id, snapshot_id, 'snapshot', '/label/made_in', 'Truckistan')



def get_article_config(last_config_id):
    document = None
    changes = []

    continueProcessing = True
    processed_id = last_config_id
    while continueProcessing:
        print(f'Processing change with id: {processed_id}')
        change = db_access.get_article_change_from_db(processed_id)
        previous_type = change['previous_type']
        print(f'previous_type: {previous_type}')
        print(f'previous_type Type: {type(previous_type)}')
        if change['previous_type'] == None or previous_type == 'None':
            previous_id = change['previous_id']
            print(f'previous_id: {previous_id}')
            if change['previous_id'] == None or previous_id == 'None':
                document = {}
                continueProcessing = False
            elif change['previous_id'] != None:
                continueProcessing = False
                raise Exception('Article Config has property: previous_id, but property: previous_type is None')
        if change['previous_type'] == 'article_config':
            changes = [(change['changed_property_path'], change['new_property_value'])] + changes
            if change['previous_id'] == None:
                continueProcessing = False
                raise Exception('Article Config has no reference to another id (previous_id is None), but previous_type is article_config')
            else:
                processed_id = change['previous_id']
        elif previous_type == 'snapshot':
            changes = [(change['changed_property_path'], change['new_property_value'])] + changes
            snapshot_changes = db_access.read_all_changes_from_snapshot(change['previous_id'])
            changes = snapshot_changes + changes
            document = {}
            continueProcessing = False
    for property_path, property_value in changes:
        print(f'Property path: {property_path}')
        path_fragments = list(filter(lambda pf: pf != '' and pf != '/', property_path.split('/')))
        current_dictionary = document
        print(f'number of path fragments: {len(path_fragments)}')
        if len(path_fragments) > 1:
            for path_fragment in path_fragments[:-1]:
                if path_fragment in current_dictionary.keys():
                    current_dictionary = current_dictionary[path_fragment]
                else:
                    current_dictionary[path_fragment] = {}
                    current_dictionary = current_dictionary[path_fragment]
        print(f'Type of current_dictionary: {type(current_dictionary)}')
        print(f'path_fragments[-1]: {path_fragments[-1]}')
        current_dictionary[path_fragments[-1]] = property_value

    return document

def create_snapshot(last_config_id):
    # document = None
    changes = []

    continueProcessing = True
    processed_id = last_config_id
    while continueProcessing:
        print(f'Processing change with id: {processed_id}')
        change = db_access.get_article_change_from_db(processed_id)
        previous_type = change['previous_type']
        print(f'previous_type: {previous_type}')
        print(f'previous_type Type: {type(previous_type)}')
        if previous_type == None or previous_type == 'None':
            previous_id = change['previous_id']
            print(f'previous_id: {previous_id}')
            if previous_id == None or previous_id == 'None':
                # document = {}
                changes = [change['id']] + changes
                continueProcessing = False
            elif previous_id != None:
                continueProcessing = False
                raise Exception('Article Config has property: previous_id, but property: previous_type is None')
        if change['previous_type'] == 'article_config':
            changes = [change['id']] + changes
            if change['previous_id'] == None:
                continueProcessing = False
                raise Exception('Article Config has no reference to another id (previous_id is None), but previous_type is article_config')
            else:
                processed_id = change['previous_id']
        # TODO elif previous_type == 'snapshot'
    snapshot_id = f'{uuid.uuid4()}'
    db_access.insert_snapshot_data(snapshot_id=snapshot_id, last_config_id=last_config_id, change_ids=changes)
    return snapshot_id

if __name__ == '__main__':
    main()
