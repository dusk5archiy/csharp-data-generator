using System.Diagnostics;
using Microsoft.Data.SqlClient;

namespace NSQDatabase;

sealed class QDatabase
{
    // ========================================================================
    private static int query_counter = 0;
    public static string server_name = "";
    public static string database_name = "";
    public static string server_only_conn_string = "";
    public static string default_conn_string = "";

    public static void init(string server_name, string database_name)
    {
        QDatabase.server_name = server_name;
        QDatabase.database_name = database_name;
        QDatabase.server_only_conn_string = new SqlConnectionStringBuilder
        {
            DataSource = server_name,
            IntegratedSecurity = true,
            TrustServerCertificate = true,
            ConnectTimeout = 60,
            MultipleActiveResultSets = true,
        }.ConnectionString;

        QDatabase.default_conn_string = new SqlConnectionStringBuilder
        {
            DataSource = server_name,
            InitialCatalog = database_name,
            IntegratedSecurity = true,
            TrustServerCertificate = true,
            ConnectTimeout = 60,
        }.ConnectionString;
    }

    public delegate void ConnFunction(SqlConnection conn);

    // ========================================================================
    public static void exec(ConnFunction conn_function, bool server_only = false)
    {
        string conn_string = server_only ? server_only_conn_string : default_conn_string;
        try
        {
            using (SqlConnection conn = new SqlConnection(conn_string))
            {
                conn.Open();
                conn_function(conn);
            }
        }
        catch (SqlException e)
        {
            Console.WriteLine(e.ToString());
        }
    }

    // ========================================================================
    public static void execQuery(SqlConnection conn, string query)
    {
        int counter = ++query_counter;
        Console.WriteLine($"[START] query #{counter}: {query[..Math.Min(100, query.Length)]}");
        // Console.WriteLine($"[START] query #{counter}: {query}");
        Stopwatch stopwatch = Stopwatch.StartNew();
        QDatabase.execCmd(conn, query, cmd => cmd.ExecuteNonQuery());
        stopwatch.Stop();
        TimeSpan elapsed = stopwatch.Elapsed;
        Console.WriteLine(
            $"[FINISH] query #{counter} - Time taken: {elapsed.TotalMilliseconds} ms"
        );
    }

    // ========================================================================
    public delegate void CmdFunction(SqlCommand cmd);
    public delegate void ReaderFunction(SqlDataReader reader);

    // ========================================================================
    public static void execQuery(SqlConnection conn, string query, ReaderFunction f)
    {
        int counter = ++query_counter;
        Console.WriteLine($"[START] query #{counter}: {query}");
        Stopwatch stopwatch = Stopwatch.StartNew();
        QDatabase.execCmd(
            conn,
            query,
            delegate(SqlCommand cmd)
            {
                using (SqlDataReader reader = cmd.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        f(reader);
                    }
                }
            }
        );
        stopwatch.Stop();
        TimeSpan elapsed = stopwatch.Elapsed;
        Console.WriteLine(
            $"[FINISH] query #{counter} - Time taken: {elapsed.TotalMilliseconds} ms"
        );
    }

    public static void execCmd(SqlConnection conn, string query, CmdFunction f)
    {
        using (SqlCommand command = new SqlCommand(query, conn))
        {
            f(command);
        }
    }

    // ========================================================================
}

/* EOF */
