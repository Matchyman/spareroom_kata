import pytest
import sqlite3
from unittest.mock import MagicMock, patch, mock_open
from src.database.dbConnectionFactory import DBConnectionFactory


class TestDBConnectionFactoryInit:

    @patch('builtins.open', new_callable=mock_open, read_data="dbpath: ':memory:'")
    @patch('yaml.load')
    def test_init_success(self, mock_yaml_load, mock_file):
        # Test successful startup with valid config
        mock_yaml_load.return_value = {"dbpath": ":memory:"}
        
        factory = DBConnectionFactory()
        
        assert factory.config == {"dbpath": ":memory:"}
        assert factory.dbpath == ":memory:"
        assert factory.logger is not None
        mock_file.assert_called_once()

    @patch('builtins.open', new_callable=mock_open, read_data="dbpath: './test.db'")
    @patch('yaml.load')
    def test_init_with_file_path(self, mock_yaml_load, mock_file):
        # Test startup with file path config
        mock_yaml_load.return_value = {"dbpath": "./test.db"}
        
        factory = DBConnectionFactory()
        
        assert factory.dbpath == "./test.db"

    @patch('builtins.open', new_callable=mock_open)
    @patch('yaml.load')
    def test_init_file_reading(self, mock_yaml_load, mock_file):
        # Test file read correctly
        mock_yaml_load.return_value = {"dbpath": ":memory:"}
        
        factory = DBConnectionFactory()
        
        # Verify file was opened with correct parameters
        mock_file.assert_called_once_with("config\\config.yml", "r")


class TestDBConnectionConnect:


    @patch('builtins.open', new_callable=mock_open, read_data="dbpath: ':memory:'")
    @patch('yaml.load')
    @patch('sqlite3.connect')
    def test_connect_success(self, mock_sqlite_connect, mock_yaml_load, mock_file):
        
        mock_yaml_load.return_value = {"dbpath": ":memory:"}
        mock_connection = MagicMock(spec=sqlite3.Connection)
        mock_sqlite_connect.return_value = mock_connection
        
        factory = DBConnectionFactory()
        result = factory.connect()
        
        assert result == mock_connection
        mock_sqlite_connect.assert_called_once_with(":memory:")

    @patch('builtins.open', new_callable=mock_open, read_data="dbpath: './error.db'")
    @patch('yaml.load')
    @patch('sqlite3.connect')
    def test_connect_general_exception(self, mock_sqlite_connect, mock_yaml_load, mock_file):
        # Test execprtio handling
        mock_yaml_load.return_value = {"dbpath": "./error.db"}
        mock_sqlite_connect.side_effect = Exception("Unexpected error")
        
        factory = DBConnectionFactory()
        result = factory.connect()
        
        assert result is None


class TestDBConnectionAddData:


    @patch('builtins.open', new_callable=mock_open, read_data="dbpath: ':memory:'")
    @patch('yaml.load')
    def test_add_data_success(self, mock_yaml_load, mock_file):

        mock_yaml_load.return_value = {"dbpath": ":memory:"}
        factory = DBConnectionFactory()
        
        mock_connection = MagicMock(spec=sqlite3.Connection)
        mock_cursor = MagicMock(spec=sqlite3.Cursor)
        mock_connection.cursor.return_value = mock_cursor
        
        query = "INSERT INTO prices (code, price) VALUES ('A', 50)"
        factory.addData(mock_connection, query)
        
        mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with(query)
        mock_connection.commit.assert_called_once()

    @patch('builtins.open', new_callable=mock_open, read_data="dbpath: ':memory:'")
    @patch('yaml.load')
    def test_add_data_multiple_inserts(self, mock_yaml_load, mock_file):

        mock_yaml_load.return_value = {"dbpath": ":memory:"}
        factory = DBConnectionFactory()
        
        mock_connection = MagicMock(spec=sqlite3.Connection)
        mock_cursor = MagicMock(spec=sqlite3.Cursor)
        mock_connection.cursor.return_value = mock_cursor
        
        queries = [
            "INSERT INTO prices (code, price) VALUES ('A', 50)",
            "INSERT INTO prices (code, price) VALUES ('B', 35)"
        ]
        
        for query in queries:
            factory.addData(mock_connection, query)
        
        assert mock_cursor.execute.call_count == 2
        assert mock_connection.commit.call_count == 2


class TestDBConnectionCheckTable:

    @patch('builtins.open', new_callable=mock_open, read_data="dbpath: ':memory:'")
    @patch('yaml.load')
    def test_check_table_exists(self, mock_yaml_load, mock_file):
        
        mock_yaml_load.return_value = {"dbpath": ":memory:"}
        factory = DBConnectionFactory()
        
        mock_connection = MagicMock(spec=sqlite3.Connection)
        mock_cursor = MagicMock(spec=sqlite3.Cursor)
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.execute.return_value.fetchall.return_value = [("prices",)]
        
        result = factory.checkTable(mock_connection, "prices")
        
        assert result is True
        mock_cursor.execute.assert_called_once_with(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'prices'"
        )

    @patch('builtins.open', new_callable=mock_open, read_data="dbpath: ':memory:'")
    @patch('yaml.load')
    def test_check_table_not_exists(self, mock_yaml_load, mock_file):
       
        mock_yaml_load.return_value = {"dbpath": ":memory:"}
        factory = DBConnectionFactory()
        
        mock_connection = MagicMock(spec=sqlite3.Connection)
        mock_cursor = MagicMock(spec=sqlite3.Cursor)
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.execute.return_value.fetchall.return_value = []
        
        result = factory.checkTable(mock_connection, "nonexistent")
        
        assert result is False



class TestDBConnectionGetData:

    @patch('builtins.open', new_callable=mock_open, read_data="dbpath: ':memory:'")
    @patch('yaml.load')
    def test_get_data_success(self, mock_yaml_load, mock_file):
        
        mock_yaml_load.return_value = {"dbpath": ":memory:"}
        factory = DBConnectionFactory()
        
        mock_connection = MagicMock(spec=sqlite3.Connection)
        mock_cursor = MagicMock(spec=sqlite3.Cursor)
        mock_connection.cursor.return_value = mock_cursor
        expected_data = [("A", 50), ("B", 35)]
        mock_cursor.execute.return_value.fetchall.return_value = expected_data
        
        query = "SELECT code, price FROM prices"
        result = factory.getData(mock_connection, query)
        
        assert result == expected_data
        mock_cursor.execute.assert_called_once_with(query)

    @patch('builtins.open', new_callable=mock_open, read_data="dbpath: ':memory:'")
    @patch('yaml.load')
    def test_get_data_empty_result(self, mock_yaml_load, mock_file):
       
        mock_yaml_load.return_value = {"dbpath": ":memory:"}
        factory = DBConnectionFactory()
        
        mock_connection = MagicMock(spec=sqlite3.Connection)
        mock_cursor = MagicMock(spec=sqlite3.Cursor)
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.execute.return_value.fetchall.return_value = []
        
        query = "SELECT code, price FROM prices WHERE code = 'X'"
        result = factory.getData(mock_connection, query)
        
        assert result == []

    @patch('builtins.open', new_callable=mock_open, read_data="dbpath: ':memory:'")
    @patch('yaml.load')
    def test_get_data_single_row(self, mock_yaml_load, mock_file):
        
        mock_yaml_load.return_value = {"dbpath": ":memory:"}
        factory = DBConnectionFactory()
        
        mock_connection = MagicMock(spec=sqlite3.Connection)
        mock_cursor = MagicMock(spec=sqlite3.Cursor)
        mock_connection.cursor.return_value = mock_cursor
        expected_data = [("A", 50)]
        mock_cursor.execute.return_value.fetchall.return_value = expected_data
        
        query = "SELECT code, price FROM prices WHERE code = 'A'"
        result = factory.getData(mock_connection, query)
        
        assert result == expected_data
        assert len(result) == 1

    @patch('builtins.open', new_callable=mock_open, read_data="dbpath: ':memory:'")
    @patch('yaml.load')
    def test_get_data_multiple_rows(self, mock_yaml_load, mock_file):
        
        mock_yaml_load.return_value = {"dbpath": ":memory:"}
        factory = DBConnectionFactory()
        
        mock_connection = MagicMock(spec=sqlite3.Connection)
        mock_cursor = MagicMock(spec=sqlite3.Cursor)
        mock_connection.cursor.return_value = mock_cursor
        expected_data = [
            ("A", 50),
            ("B", 35),
            ("C", 25),
            ("D", 12)
        ]
        mock_cursor.execute.return_value.fetchall.return_value = expected_data
        
        query = "SELECT code, price FROM prices"
        result = factory.getData(mock_connection, query)
        
        assert result == expected_data
        assert len(result) == 4

    @patch('builtins.open', new_callable=mock_open, read_data="dbpath: ':memory:'")
    @patch('yaml.load')
    def test_get_data_with_where_clause(self, mock_yaml_load, mock_file):
        
        mock_yaml_load.return_value = {"dbpath": ":memory:"}
        factory = DBConnectionFactory()
        
        mock_connection = MagicMock(spec=sqlite3.Connection)
        mock_cursor = MagicMock(spec=sqlite3.Cursor)
        mock_connection.cursor.return_value = mock_cursor
        expected_data = [("A", 50)]
        mock_cursor.execute.return_value.fetchall.return_value = expected_data
        
        query = "SELECT code, price FROM prices WHERE price > 40"
        result = factory.getData(mock_connection, query)
        
        assert result == expected_data
        mock_cursor.execute.assert_called_once_with(query)

    @patch('builtins.open', new_callable=mock_open, read_data="dbpath: ':memory:'")
    @patch('yaml.load')
    def test_get_data_join_query(self, mock_yaml_load, mock_file):
        
        mock_yaml_load.return_value = {"dbpath": ":memory:"}
        factory = DBConnectionFactory()
        
        mock_connection = MagicMock(spec=sqlite3.Connection)
        mock_cursor = MagicMock(spec=sqlite3.Cursor)
        mock_connection.cursor.return_value = mock_cursor
        expected_data = [
            ("A", 50, 3, 140),
            ("B", 35, 2, 60)
        ]
        mock_cursor.execute.return_value.fetchall.return_value = expected_data
        
        query = """
            SELECT p.code, p.price, o.offeramount, o.offerprice 
            FROM prices p 
            JOIN offers o ON p.code = o.code
        """
        result = factory.getData(mock_connection, query)
        
        assert result == expected_data
        assert len(result) == 2


class TestDBConnectionCloseConnection:


    @patch('builtins.open', new_callable=mock_open, read_data="dbpath: ':memory:'")
    @patch('yaml.load')
    def test_close_connection_success(self, mock_yaml_load, mock_file):
        
        mock_yaml_load.return_value = {"dbpath": ":memory:"}
        factory = DBConnectionFactory()
        
        mock_connection = MagicMock(spec=sqlite3.Connection)
        factory.closeConnection(mock_connection)
        
        mock_connection.close.assert_called_once()


class TestDBConnectionFactoryIntegration:

    @patch('builtins.open', new_callable=mock_open, read_data="dbpath: ':memory:'")
    @patch('yaml.load')
    @patch('sqlite3.connect')
    def test_full_workflow_connect_add_check_get_close(
        self, mock_sqlite_connect, mock_yaml_load, mock_file
    ):
        """Test complete workflow: init -> connect -> add -> check -> get -> close"""
        mock_yaml_load.return_value = {"dbpath": ":memory:"}
        
        mock_connection = MagicMock(spec=sqlite3.Connection)
        mock_cursor = MagicMock(spec=sqlite3.Cursor)
        mock_connection.cursor.return_value = mock_cursor
        mock_sqlite_connect.return_value = mock_connection
        
        # Setup different return values for different query types
        mock_cursor.execute.return_value.fetchall.side_effect = [
            [("prices",)],  # For checkTable
            [("A", 50), ("B", 35)]  # For getData
        ]
        
        # Initialize factory
        factory = DBConnectionFactory()
        
        # Connect
        con = factory.connect()
        assert con == mock_connection
        
        # Add data
        factory.addData(con, "INSERT INTO prices (code, price) VALUES ('A', 50)")
        
        # Check table exists
        table_exists = factory.checkTable(con, "prices")
        assert table_exists is True
        
        # Get data
        data = factory.getData(con, "SELECT code, price FROM prices")
        assert data == [("A", 50), ("B", 35)]
        
        # Close connection
        factory.closeConnection(con)
        con.close.assert_called()

    @patch('builtins.open', new_callable=mock_open, read_data="dbpath: ':memory:'")
    @patch('yaml.load')
    def test_workflow_with_multiple_tables(self, mock_yaml_load, mock_file):
        """Test workflow with prices and offers tables"""
        mock_yaml_load.return_value = {"dbpath": ":memory:"}
        factory = DBConnectionFactory()
        
        mock_connection = MagicMock(spec=sqlite3.Connection)
        mock_cursor = MagicMock(spec=sqlite3.Cursor)
        mock_connection.cursor.return_value = mock_cursor
        
        # Setup return values for prices table
        mock_cursor.execute.return_value.fetchall.return_value = [
            ("A", 50),
            ("B", 35)
        ]
        
        prices = factory.getData(
            mock_connection,
            "SELECT code, price FROM prices"
        )
        assert len(prices) == 2
        
        # Setup return values for offers table
        mock_cursor.execute.return_value.fetchall.return_value = [
            ("A", 3, 140),
            ("B", 2, 60)
        ]
        
        offers = factory.getData(
            mock_connection,
            "SELECT code, offeramount, offerprice FROM offers"
        )
        assert len(offers) == 2

    @patch('builtins.open', new_callable=mock_open, read_data="dbpath: ':memory:'")
    @patch('yaml.load')
    def test_error_handling_throughout_workflow(self, mock_yaml_load, mock_file):

        mock_yaml_load.return_value = {"dbpath": ":memory:"}
        factory = DBConnectionFactory()
        
        mock_connection = MagicMock(spec=sqlite3.Connection)
        mock_cursor = MagicMock(spec=sqlite3.Cursor)
        mock_connection.cursor.return_value = mock_cursor
        

        mock_cursor.execute.side_effect = sqlite3.DatabaseError("Constraint violation")
        with pytest.raises(sqlite3.DatabaseError):
            factory.addData(mock_connection, "INSERT INTO prices VALUES ('A', 50)")


class TestDBConnectionFactoryEdgeCases:
    """Tests for edge cases and boundary conditions"""

    @patch('builtins.open', new_callable=mock_open, read_data="dbpath: ':memory:'")
    @patch('yaml.load')
    def test_add_data_with_special_characters(self, mock_yaml_load, mock_file):
        """Test adding data with special characters"""
        mock_yaml_load.return_value = {"dbpath": ":memory:"}
        factory = DBConnectionFactory()
        
        mock_connection = MagicMock(spec=sqlite3.Connection)
        mock_cursor = MagicMock(spec=sqlite3.Cursor)
        mock_connection.cursor.return_value = mock_cursor
        
        query = "INSERT INTO prices (code, price) VALUES ('A''B', 50)"
        factory.addData(mock_connection, query)
        
        mock_cursor.execute.assert_called_once_with(query)

    @patch('builtins.open', new_callable=mock_open, read_data="dbpath: ':memory:'")
    @patch('yaml.load')
    def test_get_data_with_null_values(self, mock_yaml_load, mock_file):
        """Test retrieving data with NULL values"""
        mock_yaml_load.return_value = {"dbpath": ":memory:"}
        factory = DBConnectionFactory()
        
        mock_connection = MagicMock(spec=sqlite3.Connection)
        mock_cursor = MagicMock(spec=sqlite3.Cursor)
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.execute.return_value.fetchall.return_value = [("A", None)]
        
        result = factory.getData(mock_connection, "SELECT code, price FROM prices WHERE code = 'A'")
        
        assert result == [("A", None)]

    @patch('builtins.open', new_callable=mock_open, read_data="dbpath: ':memory:'")
    @patch('yaml.load')
    def test_check_table_with_empty_string(self, mock_yaml_load, mock_file):

        mock_yaml_load.return_value = {"dbpath": ":memory:"}
        factory = DBConnectionFactory()
        
        mock_connection = MagicMock(spec=sqlite3.Connection)
        mock_cursor = MagicMock(spec=sqlite3.Cursor)
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.execute.return_value.fetchall.return_value = []
        
        result = factory.checkTable(mock_connection, "")
        
        assert result is False
        mock_cursor.execute.assert_called_once()