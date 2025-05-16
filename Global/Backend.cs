using NSQDatabaseTools;

static class Backend
{
    public static void start()
    {
        QDatabase.Init("PC", "DbDotnet");
        // QDatabaseTools.getJsonScheme();
        Gen01.start();
    }
}
