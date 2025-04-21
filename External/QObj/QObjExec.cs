using Microsoft.Data.SqlClient;
using NSQDatabase;

namespace NSQObj;

class QObjExec
{
    public static List<T> execQuery<T>(SqlConnection conn, string query)
        where T : QObj, new()
    {
        List<T> results = new List<T>();
        QDatabase.execQuery(conn, query, reader => results.Add(QObjReader.getDataObj<T>(reader)));
        return results;
    }
}
