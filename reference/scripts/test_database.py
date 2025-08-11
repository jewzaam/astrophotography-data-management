import unittest

import database

DATABASE_FILENAME=r"test_data\database.sqlite"

class TestDatabase(unittest.TestCase):
    def test_init(self):
        d = database.Database(DATABASE_FILENAME)
        self.assertFalse(d.isOpen())

    def test_open(self):
        d = database.Database(DATABASE_FILENAME)
        try:
            d.open()
            self.assertTrue(d.isOpen())
        finally:
            d.close()
        self.assertFalse(d.isOpen())

    def test_execute_dryrun(self):
        d = database.Database(DATABASE_FILENAME, dryrun=True)
        stmt = "something"
        output = d.execute(stmt)
        self.assertFalse(d.isOpen())
        self.assertEqual(output, stmt)

    def test_make_where(self):
        where={"name": "somevalue", "stuff": "bob"}
        d = database.Database(DATABASE_FILENAME, dryrun=True)
        where_stmt=d._make_where(where)
        self.assertEqual(where_stmt, "name='somevalue' and stuff='bob'")

    def test_make_value(self):
        values={"name": "somevalue", "stuff": "bob"}
        d = database.Database(DATABASE_FILENAME, dryrun=True)
        value_stmt=d._make_value(values)
        self.assertEqual(value_stmt, "'somevalue','bob'")

    def test_select_stmt(self):
        # just a note to self, columns and where clause do not have to intersect.
        # (could select columns that were not in where clause!)
        columns=['id', 'name', 'stuff']
        table="sometable"
        where={"is_awesome": "1", "pet": "dog"}
        d = database.Database(DATABASE_FILENAME, dryrun=True)
        stmt = d.select_stmt(columns, table, where)
        self.assertIsNotNone(stmt)
        self.assertEqual(stmt, "select id,name,stuff from sometable where is_awesome='1' and pet='dog';")

    def test_select_stmt_like(self):
        # just a note to self, columns and where clause do not have to intersect.
        # (could select columns that were not in where clause!)
        columns=['id', 'name', 'stuff']
        table="sometable"
        where={"is_awesome": "1", "pet": "dog", "thing": "like %"}
        d = database.Database(DATABASE_FILENAME, dryrun=True)
        stmt = d.select_stmt(columns, table, where)
        self.assertIsNotNone(stmt)
        self.assertEqual(stmt, "select id,name,stuff from sometable where is_awesome='1' and pet='dog' and thing like 'like %';")

    def test_insert_stmt(self):
        table="sometable"
        values={"name": "somevalue", "stuff": "bob"}
        d = database.Database(DATABASE_FILENAME, dryrun=True)
        stmt = d.insert_stmt(table, values)
        self.assertIsNotNone(stmt)
        self.assertEqual(stmt, "insert into sometable (name,stuff) values ('somevalue','bob');")

    def test_insert_stmt_ignoreErrors(self):
        table="sometable"
        values={"name": "somevalue", "stuff": "bob"}
        d = database.Database(DATABASE_FILENAME, dryrun=True)
        stmt = d.insert_stmt(table, values, ignoreErrors=True)
        self.assertIsNotNone(stmt)
        self.assertEqual(stmt, "insert or ignore into sometable (name,stuff) values ('somevalue','bob');")

    def test_upsert_stmt(self):
        table="sometable"
        insert_values={"name": "somevalue", "stuff": "bob"}
        update_values={"some": "thing", "else": "foo"}
        conflictColumns=["conflict1", "conflict2"]
        d = database.Database(DATABASE_FILENAME, dryrun=True)
        stmt = d.upsert_stmt(table, insert_values, update_values, conflictColumns)
        self.assertIsNotNone(stmt)
        self.assertEqual(stmt, "insert into sometable (name,stuff) values ('somevalue','bob') on conflict (conflict1,conflict2) do update set some='thing',else='foo',last_updated_date=CURRENT_TIMESTAMP;")

    def test_delete_stmt(self):
        table="sometable"
        where={"name": "bob", "location": "moon"}
        d = database.Database(DATABASE_FILENAME, dryrun=True)
        # in dryrun mode, delete returns the statement
        stmt = d.delete(table, where)
        self.assertIsNotNone(stmt)
        self.assertEqual(stmt, "delete from sometable where name='bob' and location='moon';")


if __name__ == '__main__':
    unittest.main()
