import mysql.connector

class DataBase:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self._connect_to_server()


    def _connect_to_server(self):

            self.connection = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password)
            print(f"Connection is established")
            self.my_cursor = self.connection.cursor()

            self.connection.autocommit = True



    def create_database(self, name_database):

            self.my_cursor.execute(f"CREATE DATABASE {name_database};")
            print(f"DATABASE {name_database} is created")



    def create_table(self, name_database, name_table, commands):

        self.my_cursor.execute(f"USE {name_database};")
        table = f"CREATE TABLE `{name_table}`({', '.join(commands)});"
        print(table)


        self.my_cursor.execute(table)
        print(f"Table {name_table} created")
        self.print_info(name_table)



    def insert_values(self, name_database, name_table, columns_values = None, values = None):

        self.my_cursor.execute(f"USE {name_database};")
        if values:

                    insert_into = f"INSERT INTO {name_table} VALUES ({', '.join(values)});"
                    self.my_cursor.execute(insert_into)
                    self.print_info(name_table)


        if columns_values:

                columns_specific = columns_values.keys()
                values_specific = columns_values.values()
                insert_into = f"INSERT INTO {name_table} ({', '.join(columns_specific)}) VALUES ({','.join(values_specific)});"
                self.my_cursor.execute(insert_into)
                self.print_info(name_table)



    def print_info(self, name_table):
        self.my_cursor.execute(f"SELECT * FROM {name_table}")
        result_select = self.my_cursor.fetchall()
        for row in result_select:
            print(row)


    def update_table(self, name_table, columns_values, condition = None):
        data_update = []
        for key, value in columns_values.items():
            data_update.append(f"{key} = '{value}'")
        if condition:
            update = f"UPDATE {name_table} SET {','.join(data_update)} WHERE {condition};"
        else:
            update = f"UPDATE {name_table} SET {','.join(data_update)};"

            self.my_cursor.execute(update)
            self.print_info(name_table)



    def update_primary_key(self, name_db, name_table, column_for_primary_key):
        self.my_cursor.execute(f"USE {name_db}")
        show_keys = f"SHOW keys FROM {name_db}.{name_table} WHERE Key_name = 'PRIMARY'"
        self.my_cursor.execute(show_keys)
        primaryKeys = self.my_cursor.fetchall()

        if primaryKeys:
            alter_drop = f"ALTER TABLE {name_table} DROP PRIMARY KEY, ADD PRIMARY KEY ({column_for_primary_key});"
            self.my_cursor.execute(alter_drop)
            print(f"Primary key added to {column_for_primary_key}")
        else:
            alter = f"ALTER TABLE {name_table} ADD PRIMARY KEY ({column_for_primary_key})"
            self.my_cursor.execute(alter)
            print(f"Primary key added to {column_for_primary_key}")



first = DataBase('localhost', 'root', 'Soloviov972')
first.create_database('my_first_db')
first.create_table('my_first_db', 'students', ['id INT', 'name VARCHAR(255)'])
first.create_table('my_first_db', 'employee', ['id INT AUTO_INCREMENT PRIMARY KEY', 'name VARCHAR(255)', 'salary INT(6)'])
first.update_primary_key('my_first_db', 'students', 'id')
first.insert_values('my_first_db', 'students', values=['01', "'John'"])
first.insert_values('my_first_db', 'employee', columns_values={'name': "'John'", 'salary': '10000'})