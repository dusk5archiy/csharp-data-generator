using NSQDatabaseTools;

static class Backend
{
    public static void start()
    {
        QDatabase.Init("PC", "DbCnpm");
        // QDatabaseTools.getJsonScheme();
        Gen01.start();
    }
}
