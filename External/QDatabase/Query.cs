using Microsoft.Data.SqlClient;

namespace NSQDatabase;

class Query
{
    // ========================================================================
    protected string? table = null;
    private List<string> output_fields = new();
    private List<string> conditions = new();
    private List<string> inner_joins = new();
    private List<string> order_bys = new();
    private List<string> set_fields = new();
    private List<string> group_bys = new();
    private string? offset_string = null;

    // ========================================================================
    // INFO: Bắt đầu với một bảng
    public Query(string? table = null, string? alias = null)
    {
        this.table = QPiece.tableAlias(table, alias);
    }

    // ========================================================================
    // INFO: Thêm trường vào danh sách trường cần lấy
    public void outputClause(params List<string> fields)
    {
        foreach (var field in fields)
        {
            if (field.Length > 0)
                output_fields.Add(field);
        }
    }

    public void outputAvgCastFloat(string field, string? alias = null)
    {
        outputClause(QPiece.avg(QPiece.castFloat(QPiece.dot(field, alias))));
    }

    public void outputAvg(string field, string? alias = null)
    {
        outputClause(QPiece.avg(QPiece.dot(field, alias)));
    }

    public void output(string field, string? alias = null)
    {
        outputClause(QPiece.dot(field, alias));
    }

    public void outputTop(string field_, int top = 1, string? alias_ = null)
    {
        outputClause($"TOP {top} {QPiece.dot(field_, alias_)}");
    }

    public void outputQuery(string query)
    {
        outputClause($"({query})");
    }

    public void groupByClause(params List<string> fields)
    {
        foreach (var field in fields)
        {
            if (field.Length > 0)
                group_bys.Add(field);
        }
    }

    public void groupBy(string field_, string? alias_ = null)
    {
        groupByClause(QPiece.dot(field_, alias_));
    }

    // ========================================================================
    public void offset(int page, int num_objs)
    {
        offset_string = $"OFFSET {(page - 1) * num_objs} ROWS FETCH NEXT {num_objs} ROWS ONLY";
    }

    // ========================================================================
    public void removeOffset()
    {
        offset_string = null;
    }

    // ========================================================================
    public void WhereClause(params List<string> condition)
    {
        foreach (var cond in condition)
        {
            if (cond.Length > 0)
                conditions.Add(cond);
        }
    }

    // ------------------------------------------------------------------------
    public void Where<T>(string field, T value, string? alias_ = null)
    {
        WhereClause(QPiece.eq(QPiece.dot(field, alias_), value));
    }

    public void Where(string field, string value, string? alias_ = null)
    {
        WhereClause(QPiece.eq(QPiece.dot(field, alias_), value));
    }

    public void Where(string field, DateOnly value, string? alias_ = null)
    {
        WhereClause(QPiece.eq(QPiece.dot(field, alias_), value));
    }

    // ------------------------------------------------------------------------
    public void WhereQuery(string field, string query, string? alias_ = null)
    {
        WhereClause($"{QPiece.dot(field, alias_)} = ({query})");
    }

    public void WhereField(
        string field_1,
        string field_2,
        string? alias_1 = null,
        string? alias_2 = null
    )
    {
        WhereClause($"{QPiece.dot(field_1, alias_1)} = {QPiece.dot(field_2, alias_2)}");
    }

    // ------------------------------------------------------------------------
    public void WhereNStr(string field, string value, string? alias_ = null)
    {
        WhereClause($"{QPiece.dot(field, alias_)} = N'{value}'");
    }

    // ------------------------------------------------------------------------
    public void Where<T>(string field, List<T> value, string? alias_ = null)
    {
        WhereClause(QPiece.inList(QPiece.dot(field, alias_), value));
    }

    public void Where(string field, List<string> value, string? alias_ = null)
    {
        WhereClause(QPiece.inList(QPiece.dot(field, alias_), value));
    }

    // ========================================================================
    public void orderByClause(params List<string> order_by)
    {
        foreach (var field in order_by)
        {
            if (field.Length > 0)
                order_bys.Add(field);
        }
    }

    public void orderBy(string field_, bool desc = false, string? alias_ = null)
    {
        orderByClause(QPiece.orderBy(QPiece.dot(field_, alias_), desc: desc));
    }

    // ========================================================================
    public void SetClause(params List<string> set_fields)
    {
        foreach (var field in set_fields)
        {
            if (field.Length > 0)
                this.set_fields.Add(field);
        }
    }

    public void Set(string field, int value, string? alias_ = null)
    {
        SetClause($"{QPiece.dot(field, alias_)} = {value}");
    }

    public void Set(string field, string value, string? alias_ = null)
    {
        SetClause($"{QPiece.dot(field, alias_)} = '{value}'");
    }

    public void Set(string field, DateOnly value, string? alias_ = null)
    {
        SetClause($"{QPiece.dot(field, alias_)} = {QPiece.toStr(value)}");
    }

    // ------------------------------------------------------------------------
    public void JoinClause(params List<string> join_cmd)
    {
        foreach (var cmd in join_cmd)
        {
            if (cmd.Length > 0)
                inner_joins.Add(cmd);
        }
    }

    public void join(string field_1, string field_2, string? alias_1 = null, string? alias_2 = null)
    {
        string table_1 = field_1.Split('.')[0][1..^1];
        JoinClause(
            QPiece.join(
                QPiece.fieldAlias(table_1, alias_1),
                QPiece.dot(field_1, alias_1),
                QPiece.dot(field_2, alias_2)
            )
        );
    }

    // ========================================================================
    public string getWhereClause()
    {
        var conditions_str = string.Join(" AND ", conditions);
        string query = "";
        if (conditions_str.Length > 0)
            query += $" WHERE {conditions_str}";
        return query;
    }

    // ========================================================================
    private string getJoinClause()
    {
        if (inner_joins.Count == 0)
            return "";
        return " " + string.Join(" ", inner_joins);
    }

    // ========================================================================
    private string getGroupByClause()
    {
        string query = "";
        if (group_bys.Count > 0)
        {
            var s = string.Join(", ", group_bys);
            query += $" GROUP BY {s}";
        }
        return query;
    }

    // ========================================================================
    private string getOrderClause()
    {
        string query = "";
        if (order_bys.Count > 0)
        {
            var s = string.Join(", ", order_bys);
            query += $" ORDER BY {s}";
        }
        return query;
    }

    // ------------------------------------------------------------------------
    // INFO: Trả về truy vấn SELECT
    public string selectQuery()
    {
        var output_fields_str = output_fields.Count > 0 ? string.Join(", ", output_fields) : "*";
        string query = $"SELECT {output_fields_str}";
        if (table is not null)
        {
            query += $" FROM {table}";
        }
        query += getJoinClause();
        query += getWhereClause();
        query += getGroupByClause();
        query += getOrderClause();
        if (offset_string is not null)
        {
            if (order_bys.Count == 0)
                query += " ORDER BY (SELECT NULL)";
            query += " " + offset_string;
        }
        return query;
    }

    // ------------------------------------------------------------------------
    // INFO: Trả về truy vấn DELETE
    public string deleteQuery()
    {
        return $"DELETE FROM {table}" + getWhereClause();
    }

    // ------------------------------------------------------------------------
    public string updateQuery()
    {
        string query = $"UPDATE {table} SET ";
        string set_fields_str = string.Join(", ", set_fields);
        query += set_fields_str + getWhereClause();
        return query;
    }

    public string insertQuery(string data)
    {
        string query = $"INSERT INTO {table} VALUES ({data})";
        return query;
    }

    // ========================================================================
    public void select(SqlConnection conn, QDatabase.ReaderFunction f) =>
        QDatabase.execQuery(conn, selectQuery(), f);

    // ------------------------------------------------------------------------
    public T scalar<T>(SqlConnection conn)
    {
        SqlCommand command = new SqlCommand(selectQuery(), conn);
        return (T)command.ExecuteScalar();
    }

    public int scalar(SqlConnection conn)
    {
        return scalar<int>(conn);
    }

    // ------------------------------------------------------------------------
    public void delete(SqlConnection conn) => QDatabase.execQuery(conn, deleteQuery());

    // ------------------------------------------------------------------------
    public void insert(SqlConnection conn, string data) =>
        QDatabase.execQuery(conn, insertQuery(data));

    // ------------------------------------------------------------------------
    public void update(SqlConnection conn) => QDatabase.execQuery(conn, updateQuery());

    // ========================================================================
}

/* EOF */
