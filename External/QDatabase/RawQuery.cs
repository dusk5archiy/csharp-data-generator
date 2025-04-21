namespace NSQDatabase;

sealed class RawQuery
{
    // ------------------------------------------------------------------------
    public static string insertQuery(ref List<string> data, string table)
    {
        string query = $"INSERT INTO {table} VALUES";
        foreach (var record in data)
        {
            query += $" ({record}),";
        }
        query = query.TrimEnd(',');
        query += ";";
        return query;
    }

    // ------------------------------------------------------------------------
    public static void getInsertQueries(
        ref List<string> data,
        string table,
        ref List<string> queries,
        int batch_size = 1000
    )
    {
        int total_batches = (int)Math.Ceiling((double)data.Count / batch_size);

        for (int batch_number = 0; batch_number < total_batches; batch_number++)
        {
            var batch = data.Skip(batch_number * batch_size).Take(batch_size).ToList();
            string query = insertQuery(ref batch, table);
            queries.Add(query);
        }
    }

    // ========================================================================
}

/* EOF */
