using Microsoft.Data.SqlClient;

namespace NSQObj;

public class QObj
{
    public virtual void fetch(SqlDataReader reader, ref int pos) { }

    public virtual List<string> toList()
    {
        return new();
    }
}

/* EOF */
