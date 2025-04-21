using Microsoft.Data.SqlClient;
using NSQDatabase;

namespace NSQObj;

class QObjQuery : Query
{
    // ------------------------------------------------------------------------
    // INFO: Trả về truy vấn INSERT
    public string insertQuery<T>(T obj)
        where T : QObj, new()
    {
        List<string> parts = obj.toList();
        string query = $"INSERT INTO {table} VALUES ({string.Join(", ", parts)})";
        return query;
    }

    // ------------------------------------------------------------------------
    public void insert<T>(SqlConnection conn, T obj)
        where T : QObj, new() => QDatabase.execQuery(conn, insertQuery<T>(obj));

    // ------------------------------------------------------------------------
    public List<T> select<T>(SqlConnection conn)
        where T : QObj, new()
    {
        return QObjExec.execQuery<T>(conn, selectQuery());
    }

    // ------------------------------------------------------------------------
}
