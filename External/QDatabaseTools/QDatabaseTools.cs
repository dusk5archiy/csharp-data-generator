using Microsoft.Data.SqlClient;

namespace NSQDatabaseTools;

class QDatabaseTools
{
    // public static void dropDatabase()
    // {
    //     QDatabase.Exec(
    //         delegate(SqlConnection conn)
    //         {
    //             string query =
    //                 $"SELECT name FROM sys.databases WHERE name NOT IN ('master', 'tempdb', 'model', 'msdb') AND name = '{QDatabase.database_name}'";

    //             string? result = null;
    //             QDatabase.ExecQuery(conn, query, reader => result = QDataReader.getStr(reader));
    //             if (result != null)
    //                 QDatabase.ExecQuery(
    //                     conn,
    //                     $"DROP DATABASE [{QDatabase.database_name}] CREATE DATABASE [{QDatabase.database_name}]"
    //                 );
    //             else
    //                 QDatabase.ExecQuery(conn, $"CREATE DATABASE [{QDatabase.Database_name}]");
    //         },
    //         server_only: true
    //     );
    // }

    public static void getJsonScheme()
    {
        string query =
            @"
 SELECT (
            SELECT 
                t.name AS table_name,
                SCHEMA_NAME(t.schema_id) AS schema_name,
                (
                    SELECT 
                        c.name AS column_name,
                        ty.name AS data_type,
                        c.max_length,
                        c.precision,
                        c.scale,
                        c.is_nullable,
                        c.is_identity,
                        IIF(EXISTS(
                            SELECT 1 
                            FROM sys.key_constraints kc
                            JOIN sys.index_columns ic ON kc.parent_object_id = ic.object_id AND kc.unique_index_id = ic.index_id
                            WHERE kc.type = 'PK' AND kc.parent_object_id = c.object_id AND ic.column_id = c.column_id
                        ), 1, 0) AS is_primary_key
                    FROM sys.columns c
                    JOIN sys.types ty ON c.user_type_id = ty.user_type_id
                    WHERE c.object_id = t.object_id
                    FOR JSON PATH
                ) AS columns,
                (
                    SELECT 
                        fk.name AS constraint_name,
                        OBJECT_NAME(fk.referenced_object_id) AS referenced_table,
                        COL_NAME(fkc.referenced_object_id, fkc.referenced_column_id) AS referenced_column,
                        COL_NAME(fkc.parent_object_id, fkc.parent_column_id) AS parent_column
                    FROM sys.foreign_keys fk
                    JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
                    WHERE fk.parent_object_id = t.object_id
                    FOR JSON PATH
                ) AS foreign_keys
            FROM sys.tables t
            FOR JSON PATH
        ) AS json_result
        ";

        string result = "";
        QDatabase.Exec(conn =>
        {
            SqlCommand command = new SqlCommand(query, conn);
            result = (string)command.ExecuteScalar();
            command.Dispose();
        }
        );
        File.WriteAllText("schema.json", result);
        Console.WriteLine("Success");
    }
}
