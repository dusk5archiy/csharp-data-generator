using System.Reflection;
using System.Text.Json;
using Microsoft.Data.SqlClient;
using NSQDatabase;

public static class StringConstantsExtractor
{
    public static string[] GetStringConstants(Type type)
    {
        return type.GetFields(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static)
            .Where(f => f.IsLiteral && !f.IsInitOnly && f.FieldType == typeof(string))
            .Select(f => (string)f.GetRawConstantValue()!)
            .ToArray()!;
    }
}

static class Gen01
{
    public static void start()
    {
        QDatabase.exec(gen);
    }

    public static void gen(SqlConnection conn)
    {
        List<string> queries = new();
        string[] constants = StringConstantsExtractor.GetStringConstants(typeof(Tbl));
        foreach (string table in constants)
        {
            QDatabase.execQuery(conn, $"DELETE FROM [{table}]");
            string database_config_json = File.ReadAllText($"data/{table}.json");
            var lst = JsonSerializer.Deserialize<List<string>>(database_config_json) ?? new();
            RawQuery.getInsertQueries(ref lst, table, ref queries);

            string big_query = "";
            foreach (var query in queries)
            {
                big_query += $" {query}";
                if (big_query.Length > 1000000)
                {
                    QDatabase.execQuery(conn, big_query);
                    big_query = "";
                }
            }

            if (big_query.Length > 0)
            {
                QDatabase.execQuery(conn, big_query);
            }
            queries.Clear();
        }
    }
}
