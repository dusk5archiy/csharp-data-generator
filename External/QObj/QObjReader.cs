using Microsoft.Data.SqlClient;
using NSQDatabase;

namespace NSQObj;

static class QObjReader
{
    // ========================================================================
    public static T getDataObj<T>(SqlDataReader reader, ref int pos)
        where T : QObj, new()
    {
        T info = new T();
        info.fetch(reader, ref pos);
        return info;
    }

    public static T getDataObj<T>(SqlDataReader reader, int pos = 0)
        where T : QObj, new()
    {
        return getDataObj<T>(reader, ref pos);
    }
    // ========================================================================
}
