# Preparation

Tạo 2 project gồm:

1. Project chính (project sẽ được đem đi nộp)
2. Project ngầm (là project này này)

## Tại project chính

Tạo dự án MVC:

```bash
dotnet new mvc
```

Chạy các lệnh sau trong terminal để cài đặt các gói cần thiết:

```bash
dotnet add package Microsoft.Data.SqlCLient
dotnet add package Microsoft.EntityFrameworkCore
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
dotnet add package Microsoft.EntityFrameworkCore.Tools
dotnet add package Microsoft.EntityFrameworkCore.Design
dotnet tool install dotnet-ef --create-manifest-if-needed
```

Viết các class trong thư mục model

```cs
// Model/User.cs
static class UserRole
{
    public const string Admin = "Admin";
    public const string Author = "Author";
}

public class User
{
    public int Id { get; set; }
    public string Name { get; set; } = "";
    public DateOnly Birthday { get; set; }
    public string Email { get; set; } = "";
    public string Username { get; set; } = "";
    public string Password { get; set; } = "";
    public string Role { get; set; } = UserRole.Author;
}
```

```cs
// Model/Article.cs
static class ArticleStatus
{
    public const string Pending = "Pending";
    public const string Approved = "Approved";
    public const string Rejected = "Rejected";
}

public class Article
{
    public int Id { get; set; }
    public string Title { get; set; } = "";
    public int AuthorId { get; set; }
    public DateOnly DatePublished { get; set; }
    public string Abstract { get; set; } = "";
    public string Content { get; set; } = "";
    public string Topic { get; set; } = "";
    public string Status { get; set; } = ArticleStatus.Pending;
}
```

```cs
// Model/IdCounter.cs
public class IdCounter
{
    public string Name { get; set; } = "";
    public int Count { get; set; }
}
```

Viết MainContext

```cs
// Model/MainContext.cs
using Microsoft.Data.SqlClient;
using Microsoft.EntityFrameworkCore;

public class MainContext : DbContext
{
    public required DbSet<Article> Article { get; set; } = null!;
    public required DbSet<User> User { get; set; } = null!;
    public required DbSet<IdCounter> IdCounter { get; set; } = null!;

    public MainContext() { }

    public MainContext(DbContextOptions<MainContext> options)
        : base(options) { }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        string conn_string = new SqlConnectionStringBuilder
        {
            DataSource = "PC",// Thay bằng tên server trên máy của bạn, ví dụ @"PC\SQLEXPRESS"
            InitialCatalog = "DbDemo", // Tên của database
            IntegratedSecurity = true,
            TrustServerCertificate = true,
            ConnectTimeout = 60,
        }.ConnectionString;
        optionsBuilder.UseSqlServer(conn_string);
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Khai báo "HasNoKey" để loại bỏ tính năng kiểm soát khóa chính
        modelBuilder.Entity<Article>().HasNoKey();
        modelBuilder.Entity<User>().HasNoKey();
        modelBuilder.Entity<IdCounter>().HasNoKey();
    }
}
```

Tiến hành tạo Database:

```bash
dotnet ef migrations add new

# Đặt lại database, nếu database không tồn tại thì không cần chạy
donet ef database drop

dotnet ef database update
```

## Tại project ngầm

Trong file Global/Backend.cs có 2 lệnh bị comment:

```cs
        QDatabase.init("PC", "DbDemo");
        // QDatabaseTools.getJsonScheme(); // uncomment cái này
        // Gen01.start();
```

- Uncomment lệnh đầu tiên `QDatabaseTools.getJsonScheme()` rồi chạy dotnet run
để lấy thông tin các trường rồi lưu vào file schema.json

- Chạy file python tools/gen_code.py

```bash
python tools/gen_code.py
```

Output của chương trình này là file `Output/Field.cs`, copy file này vào trong project chính.

Copy thư mục `External/QDatabase` vào project chính.

- Viết file gen dữ liệu cho dự án chính (tham khảo tools/gen01.py) rồi chạy nó.

Sau khi gen được dữ liệu qua file json, quay lại backend

```cs
        QDatabase.init("PC", "DbDemo");
        // QDatabaseTools.getJsonScheme(); // comment cái này
        // Gen01.start(); // uncomment cái này
```

Cho chạy để chuyển dữ liệu từ các file json lên db.

**Hết**

Sau này có thêm trường hoặc thêm class mới:

- Xóa thư mục Migrations

Chạy các lệnh sau:

```cs
dotnet ef migrations add new
dotnet ef database drop
dotnet ef database update
```
