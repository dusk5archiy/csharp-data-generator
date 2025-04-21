using Microsoft.Data.SqlClient;

namespace NSQDatabase;

sealed class QDataReader
{
    // ========================================================================
    public static int getInt(SqlDataReader reader, ref int pos)
    {
        return reader.GetInt32(pos++);
    }

    public static int getInt(SqlDataReader reader, int pos = 0)
    {
        return getInt(reader, ref pos);
    }

    public static double getDouble(SqlDataReader reader, ref int pos)
    {
        return reader.GetDouble(pos++);
    }

    public static double getDouble(SqlDataReader reader, int pos = 0)
    {
        return getDouble(reader, ref pos);
    }

    // ------------------------------------------------------------------------
    public static string getStr(SqlDataReader reader, int pos = 0)
    {
        return reader.GetString(pos++);
    }

    public static string getStr(SqlDataReader reader, ref int pos)
    {
        return reader.GetString(pos++);
    }

    // ------------------------------------------------------------------------
    public static DateOnly getDate(SqlDataReader reader, ref int pos)
    {
        DateTime d = reader.GetDateTime(pos++);
        return new(d.Year, d.Month, d.Day);
    }

    public static DateTime getDateTime(SqlDataReader reader, ref int pos)
    {
        DateTime d = reader.GetDateTime(pos++);
        return d;
    }

    // ------------------------------------------------------------------------
    public static T getEnum<T>(SqlDataReader reader, ref int pos)
        where T : Enum
    {
        return (T)Enum.ToObject(typeof(T), reader.GetInt32(pos++));
    }

    // ========================================================================
}

/* EOF */
