import sqlite3
import uuid

db_filepath = 'articles_alpha.db'

def create_tables():
    connection = sqlite3.connect(db_filepath)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS article_configs "
                   "(id TEXT, "
                   "previous_id TEXT,"
                   "previous_type TEXT,"
                   "changed_property_path TEXT,"
                   "new_property_value TEXT)")
    # cursor.execute('DROP TABLE article_config_snapshots')
    # cursor.execute('DROP TABLE article_snapshots')
    cursor.execute("CREATE TABLE IF NOT EXISTS article_snapshots"
                   "(id TEXT,"
                   "latest_config_id TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS article_config_snapshots "
                   "(id TEXT, "
                   "change_number INT,"
                   "article_snapshot_id TEXT,"
                   "article_config_id TEXT)")
    connection.commit()
    connection.close()

def insert_data(id, previous_id, previous_type, changed_property_path, new_property_value):
    connection = sqlite3.connect(db_filepath)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO article_configs values (?,?,?,?,?)", (id, previous_id, previous_type, changed_property_path, new_property_value))
    connection.commit()
    connection.close()

def insert_snapshot_data(snapshot_id, last_config_id, change_ids):
        # id, previous_id, previous_type, changed_property_path, new_property_value):
    connection = sqlite3.connect(db_filepath)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO article_snapshots values (?,?)", (snapshot_id, last_config_id))
    change_number = 0
    for change_id in change_ids:
        snapshot_fragment_id = f'{uuid.uuid4()}'
        cursor.execute("INSERT INTO article_config_snapshots values(?,?,?,?)", (snapshot_fragment_id, change_number, snapshot_id, change_id))
        change_number = change_number + 1
    connection.commit()
    connection.close()

def read_all_changes_from_snapshot(snapshot_id):
    # id, previous_id, previous_type, changed_property_path, new_property_value):
    changes = []
    connection = sqlite3.connect(db_filepath)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM article_config_snapshots WHERE article_snapshot_id=? ORDER BY change_number", (snapshot_id,))
    change_infos = cursor.fetchall()
    connection.close()
    for change_info in change_infos:
        (snapshot_fragment_id, change_number, _, change_id) = change_info
        change = get_article_change_from_db(change_id)
        changes.append((change['changed_property_path'], change['new_property_value']))
    return changes

def get_article_change_from_db(id):
    connection = sqlite3.connect(db_filepath)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM article_configs WHERE id=?", (id,))
    rows = cursor.fetchall()
    connection.close()
    (id, previous_id, previous_type, changed_property_path, new_property_value) = rows[0]
    return {
        'id': id,
        'previous_id': previous_id,
        'previous_type': previous_type,
        'changed_property_path': changed_property_path,
        'new_property_value': new_property_value
    }

def view():
    connection = sqlite3.connect(db_filepath)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM article_configs")
    rows = cursor.fetchall()
    connection.close()
    return rows
