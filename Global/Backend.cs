using NSQDatabase;
using NSQDatabaseTools;

namespace BasementBackend;

static class Backend
{
    public static void start()
    {
        QDatabase.init("PC", "DbDemo");
        // QDatabaseTools.getJsonScheme();
        // Gen01.start();
    }
}
